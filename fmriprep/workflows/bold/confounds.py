# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
#
# Copyright 2023 The NiPreps Developers <nipreps@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# We support and encourage derived works from this project, please read
# about our expectations at
#
#     https://www.nipreps.org/community/licensing/
#
"""
Calculate BOLD confounds
^^^^^^^^^^^^^^^^^^^^^^^^

.. autofunction:: init_bold_confs_wf

"""
from os import getenv

from nipype.algorithms import confounds as nac
from nipype.interfaces import fsl
from nipype.interfaces import utility as niu
from nipype.pipeline import engine as pe
from templateflow.api import get as get_template

from fmriprep import config

from ...config import DEFAULT_MEMORY_MIN_GB
from ...interfaces import DerivativesDataSink
from ...interfaces.confounds import (
    FilterDropped,
    FMRISummary,
    GatherConfounds,
    RenameACompCor,
)


def init_bold_confs_wf(
    mem_gb: float,
    metadata: dict,
    regressors_all_comps: bool,
    regressors_dvars_th: float,
    regressors_fd_th: float,
    freesurfer: bool = False,
    name: str = "bold_confs_wf",
):
    """
    Build a workflow to generate and write out confounding signals.

    This workflow calculates confounds for a BOLD series, and aggregates them
    into a :abbr:`TSV (tab-separated value)` file, for use as nuisance
    regressors in a :abbr:`GLM (general linear model)`.
    The following confounds are calculated, with column headings in parentheses:

    #. Region-wise average signal (``csf``, ``white_matter``, ``global_signal``)
    #. DVARS - original and standardized variants (``dvars``, ``std_dvars``)
    #. Framewise displacement, based on head-motion parameters
       (``framewise_displacement``)
    #. Temporal CompCor (``t_comp_cor_XX``)
    #. Anatomical CompCor (``a_comp_cor_XX``)
    #. Cosine basis set for high-pass filtering w/ 0.008 Hz cut-off
       (``cosine_XX``)
    #. Non-steady-state volumes (``non_steady_state_XX``)
    #. Estimated head-motion parameters, in mm and rad
       (``trans_x``, ``trans_y``, ``trans_z``, ``rot_x``, ``rot_y``, ``rot_z``)


    Prior to estimating aCompCor and tCompCor, non-steady-state volumes are
    censored and high-pass filtered using a :abbr:`DCT (discrete cosine
    transform)` basis.
    The cosine basis, as well as one regressor per censored volume, are included
    for convenience.

    Workflow Graph
        .. workflow::
            :graph2use: orig
            :simple_form: yes

            from fmriprep.workflows.bold.confounds import init_bold_confs_wf
            wf = init_bold_confs_wf(
                mem_gb=1,
                metadata={},
                regressors_all_comps=False,
                regressors_dvars_th=1.5,
                regressors_fd_th=0.5,
            )

    Parameters
    ----------
    mem_gb : :obj:`float`
        Size of BOLD file in GB - please note that this size
        should be calculated after resamplings that may extend
        the FoV
    metadata : :obj:`dict`
        BIDS metadata for BOLD file
    name : :obj:`str`
        Name of workflow (default: ``bold_confs_wf``)
    regressors_all_comps : :obj:`bool`
        Indicates whether CompCor decompositions should return all
        components instead of the minimal number of components necessary
        to explain 50 percent of the variance in the decomposition mask.
    regressors_dvars_th : :obj:`float`
        Criterion for flagging DVARS outliers
    regressors_fd_th : :obj:`float`
        Criterion for flagging framewise displacement outliers

    Inputs
    ------
    bold
        BOLD image, after the prescribed corrections (STC, HMC and SDC)
        when available.
    bold_mask
        BOLD series mask
    movpar_file
        SPM-formatted motion parameters file
    rmsd_file
        Framewise displacement as measured by ``fsl_motion_outliers``.
    skip_vols
        number of non steady state volumes
    t1w_mask
        Mask of the skull-stripped template image
    t1w_tpms
        List of tissue probability maps in T1w space
    t1_bold_xform
        Affine matrix that maps the T1w space into alignment with
        the native BOLD space

    Outputs
    -------
    confounds_file
        TSV of all aggregated confounds
    rois_report
        Reportlet visualizing white-matter/CSF mask used for aCompCor,
        the ROI for tCompCor and the BOLD brain mask.
    confounds_metadata
        Confounds metadata dictionary.
    crown_mask
        Mask of brain edge voxels

    """
    from niworkflows.engine.workflows import LiterateWorkflow as Workflow
    from niworkflows.interfaces.confounds import ExpandModel, SpikeRegressors
    from niworkflows.interfaces.fixes import FixHeaderApplyTransforms as ApplyTransforms
    from niworkflows.interfaces.images import SignalExtraction
    from niworkflows.interfaces.morphology import BinaryDilation, BinarySubtraction
    from niworkflows.interfaces.nibabel import ApplyMask, Binarize
    from niworkflows.interfaces.patches import RobustACompCor as ACompCor
    from niworkflows.interfaces.patches import RobustTCompCor as TCompCor
    from niworkflows.interfaces.plotting import (
        CompCorVariancePlot,
        ConfoundsCorrelationPlot,
    )
    from niworkflows.interfaces.reportlets.masks import ROIsPlot
    from niworkflows.interfaces.utility import TSV2JSON, AddTSVHeader, DictMerge

    from ...interfaces.confounds import aCompCorMasks

    gm_desc = (
        "dilating a GM mask extracted from the FreeSurfer's *aseg* segmentation"
        if freesurfer
        else "thresholding the corresponding partial volume map at 0.05"
    )

    workflow = Workflow(name=name)
    workflow.__desc__ = f"""\
Several confounding time-series were calculated based on the
*preprocessed BOLD*: framewise displacement (FD), DVARS and
three region-wise global signals.
FD was computed using two formulations following Power (absolute sum of
relative motions, @power_fd_dvars) and Jenkinson (relative root mean square
displacement between affines, @mcflirt).
FD and DVARS are calculated for each functional run, both using their
implementations in *Nipype* [following the definitions by @power_fd_dvars].
The three global signals are extracted within the CSF, the WM, and
the whole-brain masks.
Additionally, a set of physiological regressors were extracted to
allow for component-based noise correction [*CompCor*, @compcor].
Principal components are estimated after high-pass filtering the
*preprocessed BOLD* time-series (using a discrete cosine filter with
128s cut-off) for the two *CompCor* variants: temporal (tCompCor)
and anatomical (aCompCor).
tCompCor components are then calculated from the top 2% variable
voxels within the brain mask.
For aCompCor, three probabilistic masks (CSF, WM and combined CSF+WM)
are generated in anatomical space.
The implementation differs from that of Behzadi et al. in that instead
of eroding the masks by 2 pixels on BOLD space, a mask of pixels that
likely contain a volume fraction of GM is subtracted from the aCompCor masks.
This mask is obtained by {gm_desc}, and it ensures components are not extracted
from voxels containing a minimal fraction of GM.
Finally, these masks are resampled into BOLD space and binarized by
thresholding at 0.99 (as in the original implementation).
Components are also calculated separately within the WM and CSF masks.
For each CompCor decomposition, the *k* components with the largest singular
values are retained, such that the retained components' time series are
sufficient to explain 50 percent of variance across the nuisance mask (CSF,
WM, combined, or temporal). The remaining components are dropped from
consideration.
The head-motion estimates calculated in the correction step were also
placed within the corresponding confounds file.
The confound time series derived from head motion estimates and global
signals were expanded with the inclusion of temporal derivatives and
quadratic terms for each [@confounds_satterthwaite_2013].
Frames that exceeded a threshold of {regressors_fd_th} mm FD or
{regressors_dvars_th} standardized DVARS were annotated as motion outliers.
Additional nuisance timeseries are calculated by means of principal components
analysis of the signal found within a thin band (*crown*) of voxels around
the edge of the brain, as proposed by [@patriat_improved_2017].
"""
    inputnode = pe.Node(
        niu.IdentityInterface(
            fields=[
                "bold",
                "bold_mask",
                "movpar_file",
                "rmsd_file",
                "skip_vols",
                "t1w_mask",
                "t1w_tpms",
                "t1_bold_xform",
            ]
        ),
        name="inputnode",
    )
    outputnode = pe.Node(
        niu.IdentityInterface(
            fields=[
                "confounds_file",
                "confounds_metadata",
                "acompcor_masks",
                "tcompcor_mask",
                "crown_mask",
            ]
        ),
        name="outputnode",
    )

    # Project T1w mask into BOLD space and merge with BOLD brainmask
    t1w_mask_tfm = pe.Node(
        ApplyTransforms(interpolation="MultiLabel"),
        name="t1w_mask_tfm",
    )
    union_mask = pe.Node(niu.Function(function=_binary_union), name="union_mask")

    # Create the crown mask
    dilated_mask = pe.Node(BinaryDilation(), name="dilated_mask")
    subtract_mask = pe.Node(BinarySubtraction(), name="subtract_mask")

    # DVARS
    dvars = pe.Node(
        nac.ComputeDVARS(save_nstd=True, save_std=True, remove_zerovariance=True),
        name="dvars",
        mem_gb=mem_gb,
    )

    # Frame displacement
    fdisp = pe.Node(nac.FramewiseDisplacement(parameter_source="SPM"), name="fdisp", mem_gb=mem_gb)

    # Generate aCompCor probseg maps
    acc_masks = pe.Node(aCompCorMasks(is_aseg=freesurfer), name="acc_masks")

    # Resample probseg maps in BOLD space via T1w-to-BOLD transform
    acc_msk_tfm = pe.MapNode(
        ApplyTransforms(interpolation="Gaussian"),
        iterfield=["input_image"],
        name="acc_msk_tfm",
        mem_gb=0.1,
    )
    acc_msk_brain = pe.MapNode(ApplyMask(), name="acc_msk_brain", iterfield=["in_file"])
    acc_msk_bin = pe.MapNode(Binarize(thresh_low=0.99), name="acc_msk_bin", iterfield=["in_file"])
    acompcor = pe.Node(
        ACompCor(
            components_file="acompcor.tsv",
            header_prefix="a_comp_cor_",
            pre_filter="cosine",
            save_pre_filter=True,
            save_metadata=True,
            mask_names=["CSF", "WM", "combined"],
            merge_method="none",
            failure_mode="NaN",
        ),
        name="acompcor",
        mem_gb=mem_gb,
    )

    crowncompcor = pe.Node(
        ACompCor(
            components_file="crown_compcor.tsv",
            header_prefix="edge_comp_",
            pre_filter="cosine",
            save_pre_filter=True,
            save_metadata=True,
            mask_names=["Edge"],
            merge_method="none",
            failure_mode="NaN",
            num_components=24,
        ),
        name="crowncompcor",
        mem_gb=mem_gb,
    )

    tcompcor = pe.Node(
        TCompCor(
            components_file="tcompcor.tsv",
            header_prefix="t_comp_cor_",
            pre_filter="cosine",
            save_pre_filter=True,
            save_metadata=True,
            percentile_threshold=0.02,
            failure_mode="NaN",
        ),
        name="tcompcor",
        mem_gb=mem_gb,
    )

    # Set number of components
    if regressors_all_comps:
        acompcor.inputs.num_components = "all"
        tcompcor.inputs.num_components = "all"
    else:
        acompcor.inputs.variance_threshold = 0.5
        tcompcor.inputs.variance_threshold = 0.5

    # Set TR if present
    if "RepetitionTime" in metadata:
        tcompcor.inputs.repetition_time = metadata["RepetitionTime"]
        acompcor.inputs.repetition_time = metadata["RepetitionTime"]
        crowncompcor.inputs.repetition_time = metadata["RepetitionTime"]

    # Split aCompCor results into a_comp_cor, c_comp_cor, w_comp_cor
    rename_acompcor = pe.Node(RenameACompCor(), name="rename_acompcor")

    # Global and segment regressors
    signals_class_labels = [
        "global_signal",
        "csf",
        "white_matter",
        "csf_wm",
        "tcompcor",
    ]
    merge_rois = pe.Node(
        niu.Merge(3, ravel_inputs=True), name="merge_rois", run_without_submitting=True
    )
    signals = pe.Node(
        SignalExtraction(class_labels=signals_class_labels), name="signals", mem_gb=mem_gb
    )

    # Arrange confounds
    add_dvars_header = pe.Node(
        AddTSVHeader(columns=["dvars"]),
        name="add_dvars_header",
        mem_gb=0.01,
        run_without_submitting=True,
    )
    add_std_dvars_header = pe.Node(
        AddTSVHeader(columns=["std_dvars"]),
        name="add_std_dvars_header",
        mem_gb=0.01,
        run_without_submitting=True,
    )
    add_motion_headers = pe.Node(
        AddTSVHeader(columns=["trans_x", "trans_y", "trans_z", "rot_x", "rot_y", "rot_z"]),
        name="add_motion_headers",
        mem_gb=0.01,
        run_without_submitting=True,
    )
    add_rmsd_header = pe.Node(
        AddTSVHeader(columns=["rmsd"]),
        name="add_rmsd_header",
        mem_gb=0.01,
        run_without_submitting=True,
    )
    concat = pe.Node(GatherConfounds(), name="concat", mem_gb=0.01, run_without_submitting=True)

    # CompCor metadata
    tcc_metadata_filter = pe.Node(FilterDropped(), name="tcc_metadata_filter")
    acc_metadata_filter = pe.Node(FilterDropped(), name="acc_metadata_filter")
    tcc_metadata_fmt = pe.Node(
        TSV2JSON(
            index_column="component",
            drop_columns=["mask"],
            output=None,
            additional_metadata={"Method": "tCompCor"},
            enforce_case=True,
        ),
        name="tcc_metadata_fmt",
    )
    acc_metadata_fmt = pe.Node(
        TSV2JSON(
            index_column="component",
            output=None,
            additional_metadata={"Method": "aCompCor"},
            enforce_case=True,
        ),
        name="acc_metadata_fmt",
    )
    crowncc_metadata_fmt = pe.Node(
        TSV2JSON(
            index_column="component",
            output=None,
            additional_metadata={"Method": "EdgeRegressor"},
            enforce_case=True,
        ),
        name="crowncc_metadata_fmt",
    )

    mrg_conf_metadata = pe.Node(
        niu.Merge(3), name="merge_confound_metadata", run_without_submitting=True
    )
    mrg_conf_metadata.inputs.in3 = {label: {"Method": "Mean"} for label in signals_class_labels}
    mrg_conf_metadata2 = pe.Node(
        DictMerge(), name="merge_confound_metadata2", run_without_submitting=True
    )

    # Expand model to include derivatives and quadratics
    model_expand = pe.Node(
        ExpandModel(model_formula="(dd1(rps + wm + csf + gsr))^^2 + others"),
        name="model_expansion",
    )

    # Add spike regressors
    spike_regress = pe.Node(
        SpikeRegressors(fd_thresh=regressors_fd_th, dvars_thresh=regressors_dvars_th),
        name="spike_regressors",
    )

    # Generate reportlet (ROIs)
    mrg_compcor = pe.Node(
        niu.Merge(3, ravel_inputs=True), name="mrg_compcor", run_without_submitting=True
    )
    rois_plot = pe.Node(
        ROIsPlot(colors=["b", "magenta", "g"], generate_report=True),
        name="rois_plot",
        mem_gb=mem_gb,
    )

    ds_report_bold_rois = pe.Node(
        DerivativesDataSink(desc="rois", datatype="figures", dismiss_entities=("echo",)),
        name="ds_report_bold_rois",
        run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB,
    )

    # Generate reportlet (CompCor)
    mrg_cc_metadata = pe.Node(
        niu.Merge(2), name="merge_compcor_metadata", run_without_submitting=True
    )
    compcor_plot = pe.Node(
        CompCorVariancePlot(
            variance_thresholds=(0.5, 0.7, 0.9),
            metadata_sources=["tCompCor", "aCompCor", "crownCompCor"],
        ),
        name="compcor_plot",
    )

    ds_report_compcor = pe.Node(
        DerivativesDataSink(desc="compcorvar", datatype="figures", dismiss_entities=("echo",)),
        name="ds_report_compcor",
        run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB,
    )

    # Generate reportlet (Confound correlation)
    conf_corr_plot = pe.Node(
        ConfoundsCorrelationPlot(reference_column="global_signal", max_dim=20),
        name="conf_corr_plot",
    )
    ds_report_conf_corr = pe.Node(
        DerivativesDataSink(desc="confoundcorr", datatype="figures", dismiss_entities=("echo",)),
        name="ds_report_conf_corr",
        run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB,
    )

    def _last(inlist):
        return inlist[-1]

    def _select_cols(table):
        import pandas as pd

        return [
            col
            for col in pd.read_table(table, nrows=2).columns
            if not col.startswith(("a_comp_cor_", "t_comp_cor_", "std_dvars"))
        ]

    # fmt:off
    workflow.connect([
        # connect inputnode to each non-anatomical confound node
        (inputnode, dvars, [("bold", "in_file"),
                            ("bold_mask", "in_mask")]),
        (inputnode, fdisp, [("movpar_file", "in_file")]),
        # Brain mask
        (inputnode, t1w_mask_tfm, [("t1w_mask", "input_image"),
                                   ("bold_mask", "reference_image"),
                                   ("t1_bold_xform", "transforms")]),
        (inputnode, union_mask, [("bold_mask", "mask1")]),
        (t1w_mask_tfm, union_mask, [("output_image", "mask2")]),
        (union_mask, dilated_mask, [("out", "in_mask")]),
        (union_mask, subtract_mask, [("out", "in_subtract")]),
        (dilated_mask, subtract_mask, [("out_mask", "in_base")]),
        (subtract_mask, outputnode, [("out_mask", "crown_mask")]),
        # aCompCor
        (inputnode, acompcor, [("bold", "realigned_file"),
                               ("skip_vols", "ignore_initial_volumes")]),
        (inputnode, acc_masks, [("t1w_tpms", "in_vfs"),
                                (("bold", _get_zooms), "bold_zooms")]),
        (inputnode, acc_msk_tfm, [("t1_bold_xform", "transforms"),
                                  ("bold_mask", "reference_image")]),
        (inputnode, acc_msk_brain, [("bold_mask", "in_mask")]),
        (acc_masks, acc_msk_tfm, [("out_masks", "input_image")]),
        (acc_msk_tfm, acc_msk_brain, [("output_image", "in_file")]),
        (acc_msk_brain, acc_msk_bin, [("out_file", "in_file")]),
        (acc_msk_bin, acompcor, [("out_file", "mask_files")]),
        (acompcor, rename_acompcor, [("components_file", "components_file"),
                                     ("metadata_file", "metadata_file")]),

        # crownCompCor
        (inputnode, crowncompcor, [("bold", "realigned_file"),
                                   ("skip_vols", "ignore_initial_volumes")]),
        (subtract_mask, crowncompcor, [("out_mask", "mask_files")]),

        # tCompCor
        (inputnode, tcompcor, [("bold", "realigned_file"),
                               ("skip_vols", "ignore_initial_volumes"),
                               ("bold_mask", "mask_files")]),
        # Global signals extraction (constrained by anatomy)
        (inputnode, signals, [("bold", "in_file")]),
        (inputnode, merge_rois, [("bold_mask", "in1")]),
        (acc_msk_bin, merge_rois, [("out_file", "in2")]),
        (tcompcor, merge_rois, [("high_variance_masks", "in3")]),
        (merge_rois, signals, [("out", "label_files")]),

        # Collate computed confounds together
        (inputnode, add_motion_headers, [("movpar_file", "in_file")]),
        (inputnode, add_rmsd_header, [("rmsd_file", "in_file")]),
        (dvars, add_dvars_header, [("out_nstd", "in_file")]),
        (dvars, add_std_dvars_header, [("out_std", "in_file")]),
        (signals, concat, [("out_file", "signals")]),
        (fdisp, concat, [("out_file", "fd")]),
        (tcompcor, concat, [("components_file", "tcompcor"),
                            ("pre_filter_file", "cos_basis")]),
        (rename_acompcor, concat, [("components_file", "acompcor")]),
        (crowncompcor, concat, [("components_file", "crowncompcor")]),
        (add_motion_headers, concat, [("out_file", "motion")]),
        (add_rmsd_header, concat, [("out_file", "rmsd")]),
        (add_dvars_header, concat, [("out_file", "dvars")]),
        (add_std_dvars_header, concat, [("out_file", "std_dvars")]),

        # Confounds metadata
        (tcompcor, tcc_metadata_filter, [("metadata_file", "in_file")]),
        (tcc_metadata_filter, tcc_metadata_fmt, [("out_file", "in_file")]),
        (rename_acompcor, acc_metadata_filter, [("metadata_file", "in_file")]),
        (acc_metadata_filter, acc_metadata_fmt, [("out_file", "in_file")]),
        (crowncompcor, crowncc_metadata_fmt, [("metadata_file", "in_file")]),
        (tcc_metadata_fmt, mrg_conf_metadata, [("output", "in1")]),
        (acc_metadata_fmt, mrg_conf_metadata, [("output", "in2")]),
        (crowncc_metadata_fmt, mrg_conf_metadata, [("output", "in3")]),
        (mrg_conf_metadata, mrg_conf_metadata2, [("out", "in_dicts")]),

        # Expand the model with derivatives, quadratics, and spikes
        (concat, model_expand, [("confounds_file", "confounds_file")]),
        (model_expand, spike_regress, [("confounds_file", "confounds_file")]),

        # Set outputs
        (spike_regress, outputnode, [("confounds_file", "confounds_file")]),
        (mrg_conf_metadata2, outputnode, [("out_dict", "confounds_metadata")]),
        (tcompcor, outputnode, [("high_variance_masks", "tcompcor_mask")]),
        (acc_msk_bin, outputnode, [("out_file", "acompcor_masks")]),
        (inputnode, rois_plot, [("bold", "in_file"),
                                ("bold_mask", "in_mask")]),
        (tcompcor, mrg_compcor, [("high_variance_masks", "in1")]),
        (acc_msk_bin, mrg_compcor, [(("out_file", _last), "in2")]),
        (subtract_mask, mrg_compcor, [("out_mask", "in3")]),
        (mrg_compcor, rois_plot, [("out", "in_rois")]),
        (rois_plot, ds_report_bold_rois, [("out_report", "in_file")]),
        (tcompcor, mrg_cc_metadata, [("metadata_file", "in1")]),
        (acompcor, mrg_cc_metadata, [("metadata_file", "in2")]),
        (crowncompcor, mrg_cc_metadata, [("metadata_file", "in3")]),
        (mrg_cc_metadata, compcor_plot, [("out", "metadata_files")]),
        (compcor_plot, ds_report_compcor, [("out_file", "in_file")]),
        (concat, conf_corr_plot, [("confounds_file", "confounds_file"),
                                  (("confounds_file", _select_cols), "columns")]),
        (conf_corr_plot, ds_report_conf_corr, [("out_file", "in_file")]),
    ])
    # fmt: on

    return workflow


def init_carpetplot_wf(
    mem_gb: float, metadata: dict, cifti_output: bool, name: str = "bold_carpet_wf"
):
    """
    Build a workflow to generate *carpet* plots.

    Resamples the MNI parcellation (ad-hoc parcellation derived from the
    Harvard-Oxford template and others).

    Parameters
    ----------
    mem_gb : :obj:`float`
        Size of BOLD file in GB - please note that this size
        should be calculated after resamplings that may extend
        the FoV
    metadata : :obj:`dict`
        BIDS metadata for BOLD file
    name : :obj:`str`
        Name of workflow (default: ``bold_carpet_wf``)

    Inputs
    ------
    bold
        BOLD image, after the prescribed corrections (STC, HMC and SDC)
        when available.
    bold_mask
        BOLD series mask
    confounds_file
        TSV of all aggregated confounds
    t1_bold_xform
        Affine matrix that maps the T1w space into alignment with
        the native BOLD space
    std2anat_xfm
        ANTs-compatible affine-and-warp transform file
    cifti_bold
        BOLD image in CIFTI format, to be used in place of volumetric BOLD
    crown_mask
        Mask of brain edge voxels
    acompcor_mask
        Mask of deep WM+CSF
    dummy_scans
        Number of nonsteady states to be dropped at the beginning of the timeseries.

    Outputs
    -------
    out_carpetplot
        Path of the generated SVG file

    """
    from niworkflows.engine.workflows import LiterateWorkflow as Workflow
    from niworkflows.interfaces.fixes import FixHeaderApplyTransforms as ApplyTransforms

    inputnode = pe.Node(
        niu.IdentityInterface(
            fields=[
                "bold",
                "bold_mask",
                "confounds_file",
                "t1_bold_xform",
                "std2anat_xfm",
                "cifti_bold",
                "crown_mask",
                "acompcor_mask",
                "dummy_scans",
            ]
        ),
        name="inputnode",
    )

    outputnode = pe.Node(niu.IdentityInterface(fields=["out_carpetplot"]), name="outputnode")

    # Carpetplot and confounds plot
    conf_plot = pe.Node(
        FMRISummary(
            tr=metadata["RepetitionTime"],
            confounds_list=[
                ("global_signal", None, "GS"),
                ("csf", None, "GSCSF"),
                ("white_matter", None, "GSWM"),
                ("std_dvars", None, "DVARS"),
                ("framewise_displacement", "mm", "FD"),
            ],
        ),
        name="conf_plot",
        mem_gb=mem_gb,
    )
    ds_report_bold_conf = pe.Node(
        DerivativesDataSink(
            desc="carpetplot", datatype="figures", extension="svg", dismiss_entities=("echo",)
        ),
        name="ds_report_bold_conf",
        run_without_submitting=True,
        mem_gb=DEFAULT_MEMORY_MIN_GB,
    )

    parcels = pe.Node(niu.Function(function=_carpet_parcellation), name="parcels")
    parcels.inputs.nifti = not cifti_output
    # List transforms
    mrg_xfms = pe.Node(niu.Merge(2), name="mrg_xfms")

    # Warp segmentation into EPI space
    resample_parc = pe.Node(
        ApplyTransforms(
            dimension=3,
            input_image=str(
                get_template(
                    "MNI152NLin2009cAsym",
                    resolution=1,
                    desc="carpet",
                    suffix="dseg",
                    extension=[".nii", ".nii.gz"],
                )
            ),
            interpolation="MultiLabel",
            args="-u int",
        ),
        name="resample_parc",
    )

    workflow = Workflow(name=name)
    if cifti_output:
        workflow.connect(inputnode, "cifti_bold", conf_plot, "in_cifti")

    # fmt:off
    workflow.connect([
        (inputnode, mrg_xfms, [("t1_bold_xform", "in1"),
                               ("std2anat_xfm", "in2")]),
        (inputnode, resample_parc, [("bold_mask", "reference_image")]),
        (inputnode, parcels, [("crown_mask", "crown_mask")]),
        (inputnode, parcels, [("acompcor_mask", "acompcor_mask")]),
        (inputnode, conf_plot, [("bold", "in_nifti"),
                                ("confounds_file", "confounds_file"),
                                ("dummy_scans", "drop_trs")]),
        (mrg_xfms, resample_parc, [("out", "transforms")]),
        (resample_parc, parcels, [("output_image", "segmentation")]),
        (parcels, conf_plot, [("out", "in_segm")]),
        (conf_plot, ds_report_bold_conf, [("out_file", "in_file")]),
        (conf_plot, outputnode, [("out_file", "out_carpetplot")]),
    ])
    # fmt:on
    return workflow


def _binary_union(mask1, mask2):
    """Generate the union of two masks."""
    from pathlib import Path

    import nibabel as nb
    import numpy as np

    img = nb.load(mask1)
    mskarr1 = np.asanyarray(img.dataobj, dtype=int) > 0
    mskarr2 = np.asanyarray(nb.load(mask2).dataobj, dtype=int) > 0
    out = img.__class__(mskarr1 | mskarr2, img.affine, img.header)
    out.set_data_dtype("uint8")
    out_name = Path("mask_union.nii.gz").absolute()
    out.to_filename(out_name)
    return str(out_name)


def _carpet_parcellation(segmentation, crown_mask, acompcor_mask, nifti=False):
    """Generate the union of two masks."""
    from pathlib import Path

    import nibabel as nb
    import numpy as np

    img = nb.load(segmentation)

    lut = np.zeros((256,), dtype="uint8")
    lut[100:201] = 1 if nifti else 0  # Ctx GM
    lut[30:99] = 2 if nifti else 0  # dGM
    lut[1:11] = 3 if nifti else 1  # WM+CSF
    lut[255] = 5 if nifti else 0  # Cerebellum
    # Apply lookup table
    seg = lut[np.uint16(img.dataobj)]
    seg[np.bool_(nb.load(crown_mask).dataobj)] = 6 if nifti else 2
    # Separate deep from shallow WM+CSF
    seg[np.bool_(nb.load(acompcor_mask).dataobj)] = 4 if nifti else 1

    outimg = img.__class__(seg.astype("uint8"), img.affine, img.header)
    outimg.set_data_dtype("uint8")
    out_file = Path("segments.nii.gz").absolute()
    outimg.to_filename(out_file)
    return str(out_file)


def _get_zooms(in_file):
    import nibabel as nb

    return tuple(nb.load(in_file).header.get_zooms()[:3])
