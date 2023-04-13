# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
"""Anatomical post-processing workflows."""
from nipype import Function, logging
from nipype.interfaces import utility as niu
from nipype.interfaces.ants import CompositeTransformUtil  # MB
from nipype.interfaces.freesurfer import MRIsConvert
from nipype.pipeline import engine as pe
from niworkflows.engine.workflows import LiterateWorkflow as Workflow
from pkg_resources import resource_filename as pkgrf
from templateflow.api import get as get_template

from xcp_d.interfaces.ants import (
    ApplyTransforms,
    CompositeInvTransformUtil,
    ConvertTransformFile,
)
from xcp_d.interfaces.bids import DerivativesDataSink
from xcp_d.interfaces.c3 import C3d  # TM
from xcp_d.interfaces.nilearn import BinaryMath, Merge
from xcp_d.interfaces.workbench import (  # MB,TM
    ApplyAffine,
    ApplyWarpfield,
    ChangeXfmType,
    CiftiSurfaceResample,
    ConvertAffine,
    SurfaceAverage,
    SurfaceGenerateInflated,
    SurfaceSphereProjectUnproject,
)
from xcp_d.utils.bids import get_freesurfer_dir, get_freesurfer_sphere
from xcp_d.utils.doc import fill_doc
from xcp_d.workflows.execsummary import (
    init_brainsprite_figures_wf,
    init_execsummary_anatomical_plots_wf,
)
from xcp_d.workflows.outputs import init_copy_inputs_to_outputs_wf

LOGGER = logging.getLogger("nipype.workflow")


@fill_doc
def init_postprocess_anat_wf(
    output_dir,
    input_type,
    t1w_available,
    t2w_available,
    target_space,
    dcan_qc,
    omp_nthreads,
    mem_gb,
    name="postprocess_anat_wf",
):
    """Copy T1w, segmentation, and, optionally, T2w to the derivative directory.

    If necessary, this workflow will also warp the images to standard space.

    Workflow Graph
        .. workflow::
            :graph2use: orig
            :simple_form: yes

            from xcp_d.workflows.anatomical import init_postprocess_anat_wf

            wf = init_postprocess_anat_wf(
                output_dir=".",
                input_type="fmriprep",
                t1w_available=True,
                t2w_available=True,
                target_space="MNI152NLin6Asym",
                dcan_qc=True,
                omp_nthreads=1,
                mem_gb=0.1,
                name="postprocess_anat_wf",
            )

    Parameters
    ----------
    %(output_dir)s
    %(input_type)s
    t1w_available : bool
        True if a preprocessed T1w is available, False if not.
    t2w_available : bool
        True if a preprocessed T2w is available, False if not.
    target_space : :obj:`str`
        Target NIFTI template for T1w.
    %(dcan_qc)s
    %(omp_nthreads)s
    %(mem_gb)s
    %(name)s
        Default is "postprocess_anat_wf".

    Inputs
    ------
    t1w : :obj:`str`
        Path to the preprocessed T1w file.
        This file may be in standard space or native T1w space.
    t2w : :obj:`str` or None
        Path to the preprocessed T2w file.
        This file may be in standard space or native T1w space.
    anat_dseg : :obj:`str`
        Path to the T1w segmentation file.
    %(anat_to_template_xfm)s
        We need to use MNI152NLin6Asym for the template.
    template : :obj:`str`
        The target template.

    Outputs
    -------
    t1w : :obj:`str`
        Path to the preprocessed T1w file in standard space.
    t2w : :obj:`str` or None
        Path to the preprocessed T2w file in standard space.
    """
    workflow = Workflow(name=name)

    inputnode = pe.Node(
        niu.IdentityInterface(
            fields=[
                "t1w",
                "t2w",
                "anat_dseg",
                "anat_to_template_xfm",
                "template",
            ]
        ),
        name="inputnode",
    )

    outputnode = pe.Node(
        niu.IdentityInterface(fields=["t1w", "t2w"]),
        name="outputnode",
    )

    # Split cohort out of the space for MNIInfant templates.
    cohort = None
    if "+" in target_space:
        target_space, cohort = target_space.split("+")

    template_file = str(
        get_template(template=target_space, cohort=cohort, resolution=1, desc=None, suffix="T1w")
    )
    inputnode.inputs.template = template_file

    ds_anat_dseg_std = pe.Node(
        DerivativesDataSink(
            base_directory=output_dir,
            space=target_space,
            cohort=cohort,
            extension=".nii.gz",
        ),
        name="ds_anat_dseg_std",
        run_without_submitting=False,
    )

    # fmt:off
    workflow.connect([(inputnode, ds_anat_dseg_std, [("anat_dseg", "source_file")])])
    # fmt:on

    if t1w_available:
        ds_t1w_std = pe.Node(
            DerivativesDataSink(
                base_directory=output_dir,
                space=target_space,
                cohort=cohort,
                extension=".nii.gz",
            ),
            name="ds_t1w_std",
            run_without_submitting=False,
        )

        # fmt:off
        workflow.connect([
            (inputnode, ds_t1w_std, [("t1w", "source_file")]),
            (ds_t1w_std, outputnode, [("out_file", "t1w")]),
        ])
        # fmt:on

    if t2w_available:
        ds_t2w_std = pe.Node(
            DerivativesDataSink(
                base_directory=output_dir,
                space=target_space,
                cohort=cohort,
                extension=".nii.gz",
            ),
            name="ds_t2w_std",
            run_without_submitting=False,
        )

        # fmt:off
        workflow.connect([
            (inputnode, ds_t2w_std, [("t2w", "source_file")]),
            (ds_t2w_std, outputnode, [("out_file", "t2w")]),
        ])
        # fmt:on

    if input_type in ("dcan", "hcp"):
        # Assume that the T1w, T1w segmentation, and T2w files are in standard space,
        # but don't have the "space" entity, for the "dcan" and "hcp" derivatives.
        # This is a bug, and the converted filenames are inaccurate, so we have this
        # workaround in place.
        # fmt:off
        workflow.connect([(inputnode, ds_anat_dseg_std, [("anat_dseg", "in_file")])])
        # fmt:on

        if t1w_available:
            # fmt:off
            workflow.connect([(inputnode, ds_t1w_std, [("t1w", "in_file")])])
            # fmt:on

        if t2w_available:
            # fmt:off
            workflow.connect([(inputnode, ds_t2w_std, [("t2w", "in_file")])])
            # fmt:on

    else:
        warp_anat_dseg_to_template = pe.Node(
            ApplyTransforms(
                num_threads=2,
                interpolation="GenericLabel",
                input_image_type=3,
                dimension=3,
            ),
            name="warp_anat_dseg_to_template",
            mem_gb=mem_gb,
            n_procs=omp_nthreads,
        )

        # fmt:off
        workflow.connect([
            (inputnode, warp_anat_dseg_to_template, [
                ("anat_dseg", "input_image"),
                ("anat_to_template_xfm", "transforms"),
                ("template", "reference_image"),
            ]),
            (warp_anat_dseg_to_template, ds_anat_dseg_std, [("output_image", "in_file")]),
        ])
        # fmt:on

        if t1w_available:
            # Warp the native T1w-space T1w, T1w segmentation, and T2w files to standard space.
            warp_t1w_to_template = pe.Node(
                ApplyTransforms(
                    num_threads=2,
                    interpolation="LanczosWindowedSinc",
                    input_image_type=3,
                    dimension=3,
                ),
                name="warp_t1w_to_template",
                mem_gb=mem_gb,
                n_procs=omp_nthreads,
            )

            # fmt:off
            workflow.connect([
                (inputnode, warp_t1w_to_template, [
                    ("t1w", "input_image"),
                    ("anat_to_template_xfm", "transforms"),
                    ("template", "reference_image"),
                ]),
                (warp_t1w_to_template, ds_t1w_std, [("output_image", "in_file")]),
            ])
            # fmt:on

        if t2w_available:
            warp_t2w_to_template = pe.Node(
                ApplyTransforms(
                    num_threads=2,
                    interpolation="LanczosWindowedSinc",
                    input_image_type=3,
                    dimension=3,
                ),
                name="warp_t2w_to_template",
                mem_gb=mem_gb,
                n_procs=omp_nthreads,
            )

            # fmt:off
            workflow.connect([
                (inputnode, warp_t2w_to_template, [
                    ("t2w", "input_image"),
                    ("anat_to_template_xfm", "transforms"),
                    ("template", "reference_image"),
                ]),
                (warp_t2w_to_template, ds_t2w_std, [("output_image", "in_file")]),
            ])
            # fmt:on

    if dcan_qc:
        execsummary_anatomical_plots_wf = init_execsummary_anatomical_plots_wf(
            t1w_available=t1w_available,
            t2w_available=t2w_available,
            output_dir=output_dir,
            name="execsummary_anatomical_plots_wf",
        )

        # fmt:off
        workflow.connect([
            (inputnode, execsummary_anatomical_plots_wf, [("template", "inputnode.template")]),
        ])
        # fmt:on

        if t1w_available:
            # fmt:off
            workflow.connect([
                (ds_t1w_std, execsummary_anatomical_plots_wf, [("out_file", "inputnode.t1w")]),
            ])
            # fmt:on

        if t2w_available:
            # fmt:off
            workflow.connect([
                (ds_t2w_std, execsummary_anatomical_plots_wf, [("out_file", "inputnode.t2w")]),
            ])
            # fmt:on

    return workflow


@fill_doc
def init_postprocess_surfaces_wf(
    fmri_dir,
    subject_id,
    dcan_qc,
    process_surfaces,
    mesh_available,
    standard_space_mesh,
    shape_available,
    output_dir,
    t1w_available,
    t2w_available,
    mem_gb,
    omp_nthreads,
    name="postprocess_surfaces_wf",
):
    """Postprocess surfaces.

    Workflow Graph
        .. workflow::
            :graph2use: orig
            :simple_form: yes

            from xcp_d.workflows.anatomical import init_postprocess_surfaces_wf

            wf = init_postprocess_surfaces_wf(
                fmri_dir=".",
                subject_id="01",
                dcan_qc=True,
                process_surfaces=True,
                mesh_available=True,
                standard_space_mesh=False,
                shape_available=True,
                output_dir=".",
                t1w_available=True,
                t2w_available=True,
                mem_gb=0.1,
                omp_nthreads=1,
                name="postprocess_surfaces_wf",
            )

    Parameters
    ----------
    fmri_dir
    subject_id
    %(dcan_qc)s
    process_surfaces : bool
    mesh_available : bool
    standard_space_mesh : bool
    shape_available : bool
    %(output_dir)s
    t1w_available : bool
        True if a T1w image is available.
    t2w_available : bool
        True if a T2w image is available.
    %(mem_gb)s
    %(omp_nthreads)s
    %(name)s
        Default is "postprocess_surfaces_wf".

    Inputs
    ------
    t1w
        Preprocessed T1w file. May be in native or standard space.
    t2w
        Preprocessed T2w file. May be in native or standard space.
    %(anat_to_template_xfm)s
    %(template_to_anat_xfm)s
    lh_pial_surf, rh_pial_surf
    lh_wm_surf, rh_wm_surf
    lh_sulcal_depth, rh_sulcal_depth
    lh_sulcal_curv, rh_sulcal_curv
    lh_cortical_thickness, rh_cortical_thickness
    """
    workflow = Workflow(name=name)

    inputnode = pe.Node(
        niu.IdentityInterface(
            fields=[
                "t1w",
                "t2w",
                "anat_to_template_xfm",
                "template_to_anat_xfm",
                "lh_pial_surf",
                "rh_pial_surf",
                "lh_wm_surf",
                "rh_wm_surf",
                "lh_sulcal_depth",
                "rh_sulcal_depth",
                "lh_sulcal_curv",
                "rh_sulcal_curv",
                "lh_cortical_thickness",
                "rh_cortical_thickness",
            ],
        ),
        name="inputnode",
    )

    if dcan_qc and mesh_available:
        # Plot the white and pial surfaces on the brain in a brainsprite figure.
        brainsprite_wf = init_brainsprite_figures_wf(
            output_dir=output_dir,
            t1w_available=t1w_available,
            t2w_available=t2w_available,
            omp_nthreads=omp_nthreads,
            mem_gb=mem_gb,
        )
        # fmt:off
        workflow.connect([
            (inputnode, brainsprite_wf, [
                ("t1w", "inputnode.t1w"),
                ("t2w", "inputnode.t2w"),
            ]),
        ])
        # fmt:on

        if not process_surfaces:
            # Use native-space T1w and surfaces for brainsprite.
            # fmt:off
            workflow.connect([
                (inputnode, brainsprite_wf, [
                    ("lh_pial_surf", "inputnode.lh_pial_surf"),
                    ("rh_pial_surf", "inputnode.rh_pial_surf"),
                    ("lh_wm_surf", "inputnode.lh_wm_surf"),
                    ("rh_wm_surf", "inputnode.rh_wm_surf"),
                ]),
            ])
            # fmt:on

    if not process_surfaces:
        # Return early, as all other steps require process_surfaces.
        return workflow

    if shape_available or (mesh_available and standard_space_mesh):
        # At least some surfaces are already in fsLR space and must be copied,
        # without modification, to the output directory.
        copy_std_surfaces_to_datasink = init_copy_inputs_to_outputs_wf(
            output_dir=output_dir,
            name="copy_std_surfaces_to_datasink",
        )

    if shape_available:
        # fmt:off
        workflow.connect([
            (inputnode, copy_std_surfaces_to_datasink, [
                ("lh_sulcal_depth", "inputnode.lh_sulcal_depth"),
                ("rh_sulcal_depth", "inputnode.rh_sulcal_depth"),
                ("lh_sulcal_curv", "inputnode.lh_sulcal_curv"),
                ("rh_sulcal_curv", "inputnode.rh_sulcal_curv"),
                ("lh_cortical_thickness", "inputnode.lh_cortical_thickness"),
                ("rh_cortical_thickness", "inputnode.rh_cortical_thickness"),
            ]),
        ])
        # fmt:on

    if mesh_available:
        # Generate and output HCP-style surface files.
        hcp_surface_wfs = {
            hemi: init_generate_hcp_surfaces_wf(
                output_dir=output_dir,
                mem_gb=mem_gb,
                omp_nthreads=omp_nthreads,
                name=f"{hemi}_generate_hcp_surfaces_wf",
            )
            for hemi in ["lh", "rh"]
        }
        # fmt:off
        workflow.connect([
            (inputnode, hcp_surface_wfs["lh"], [
                ("lh_pial_surf", "inputnode.name_source"),
            ]),
            (inputnode, hcp_surface_wfs["rh"], [
                ("rh_pial_surf", "inputnode.name_source"),
            ]),
        ])
        # fmt:on

    if mesh_available and standard_space_mesh:
        # Mesh files are already in fsLR.
        # fmt:off
        workflow.connect([
            (inputnode, copy_std_surfaces_to_datasink, [
                ("lh_pial_surf", "inputnode.lh_pial_surf"),
                ("rh_pial_surf", "inputnode.rh_pial_surf"),
                ("lh_wm_surf", "inputnode.lh_wm_surf"),
                ("rh_wm_surf", "inputnode.rh_wm_surf"),
            ]),
            (inputnode, hcp_surface_wfs["lh"], [
                ("lh_pial_surf", "inputnode.pial_surf"),
                ("lh_wm_surf", "inputnode.wm_surf"),
            ]),
            (inputnode, hcp_surface_wfs["rh"], [
                ("rh_pial_surf", "inputnode.pial_surf"),
                ("rh_wm_surf", "inputnode.wm_surf"),
            ]),
        ])
        # fmt:on

    elif mesh_available:
        # Mesh files are in fsnative and must be warped to fsLR.
        warp_surfaces_to_template_wf = init_warp_surfaces_to_template_wf(
            fmri_dir=fmri_dir,
            subject_id=subject_id,
            output_dir=output_dir,
            omp_nthreads=omp_nthreads,
            mem_gb=mem_gb,
            name="warp_surfaces_to_template_wf",
        )

        # fmt:off
        workflow.connect([
            (inputnode, warp_surfaces_to_template_wf, [
                ("lh_pial_surf", "inputnode.lh_pial_surf"),
                ("rh_pial_surf", "inputnode.rh_pial_surf"),
                ("lh_wm_surf", "inputnode.lh_wm_surf"),
                ("rh_wm_surf", "inputnode.rh_wm_surf"),
                ("anat_to_template_xfm", "inputnode.anat_to_template_xfm"),
                ("template_to_anat_xfm", "inputnode.template_to_anat_xfm"),
            ]),
            (warp_surfaces_to_template_wf, hcp_surface_wfs["lh"], [
                ("outputnode.lh_pial_surf", "inputnode.pial_surf"),
                ("outputnode.lh_wm_surf", "inputnode.wm_surf"),
            ]),
            (warp_surfaces_to_template_wf, hcp_surface_wfs["rh"], [
                ("outputnode.rh_pial_surf", "inputnode.pial_surf"),
                ("outputnode.rh_wm_surf", "inputnode.wm_surf"),
            ]),
        ])
        # fmt:on

        if dcan_qc:
            # Use standard-space T1w and surfaces for brainsprite.
            # fmt:off
            workflow.connect([
                (warp_surfaces_to_template_wf, brainsprite_wf, [
                    ("outputnode.lh_pial_surf", "inputnode.lh_pial_surf"),
                    ("outputnode.rh_pial_surf", "inputnode.rh_pial_surf"),
                    ("outputnode.lh_wm_surf", "inputnode.lh_wm_surf"),
                    ("outputnode.rh_wm_surf", "inputnode.rh_wm_surf"),
                ]),
            ])
            # fmt:on

    elif not shape_available:
        raise ValueError(
            "No surfaces found. "
            "Surfaces are required if `--warp-surfaces-native2std` is enabled."
        )

    return workflow


@fill_doc
def init_warp_surfaces_to_template_wf(
    fmri_dir,
    subject_id,
    output_dir,
    omp_nthreads,
    mem_gb,
    name="warp_surfaces_to_template_wf",
):
    """Transform surfaces from native to standard fsLR-32k space.

    Workflow Graph
        .. workflow::
            :graph2use: orig
            :simple_form: yes

            from xcp_d.workflows.anatomical import init_warp_surfaces_to_template_wf

            wf = init_warp_surfaces_to_template_wf(
                fmri_dir=".",
                subject_id="01",
                output_dir=".",
                omp_nthreads=1,
                mem_gb=0.1,
                name="warp_surfaces_to_template_wf",
            )

    Parameters
    ----------
    %(fmri_dir)s
    %(subject_id)s
    %(output_dir)s
    %(omp_nthreads)s
    %(mem_gb)s
    %(name)s
        Default is "warp_surfaces_to_template_wf".

    Inputs
    ------
    %(anat_to_template_xfm)s
        The template in question should match the volumetric space of the BOLD CIFTI files
        being processed by the main xcpd workflow.
        For example, MNI152NLin6Asym for fsLR-space CIFTIs.
    %(template_to_anat_xfm)s
        The template in question should match the volumetric space of the BOLD CIFTI files
        being processed by the main xcpd workflow.
        For example, MNI152NLin6Asym for fsLR-space CIFTIs.
    lh_pial_surf, rh_pial_surf : :obj:`str`
        Left- and right-hemisphere pial surface files in fsnative space.
    lh_wm_surf, rh_wm_surf : :obj:`str`
        Left- and right-hemisphere smoothed white matter surface files in fsnative space.

    Outputs
    -------
    lh_pial_surf, rh_pial_surf : :obj:`str`
        Left- and right-hemisphere pial surface files, in standard space.
    lh_wm_surf, rh_wm_surf : :obj:`str`
        Left- and right-hemisphere smoothed white matter surface files, in standard space.
    """
    workflow = Workflow(name=name)

    inputnode = pe.Node(
        niu.IdentityInterface(
            fields=[
                # transforms
                "anat_to_template_xfm",
                "template_to_anat_xfm",
                # surfaces
                "lh_pial_surf",
                "rh_pial_surf",
                "lh_wm_surf",
                "rh_wm_surf",
            ],
        ),
        name="inputnode",
    )
    # Feed the standard-space pial and white matter surfaces to the outputnode for the brainsprite
    # and the HCP-surface generation workflow.
    outputnode = pe.Node(
        niu.IdentityInterface(
            fields=[
                "lh_pial_surf",
                "rh_pial_surf",
                "lh_wm_surf",
                "rh_wm_surf",
            ],
        ),
        name="outputnode",
    )

    # Warp the surfaces to space-fsLR, den-32k.
    get_freesurfer_dir_node = pe.Node(
        Function(
            function=get_freesurfer_dir,
            input_names=["fmri_dir"],
            output_names=["freesurfer_path"],
        ),
        name="get_freesurfer_dir_node",
    )
    get_freesurfer_dir_node.inputs.fmri_dir = fmri_dir

    # First, we create the Connectome WorkBench-compatible transform files.
    update_xfm_wf = init_ants_xfm_to_fsl_wf(
        mem_gb=mem_gb,
        omp_nthreads=omp_nthreads,
        name="update_xfm_wf",
    )

    # fmt:off
    workflow.connect([
        (inputnode, update_xfm_wf, [
            ("anat_to_template_xfm", "inputnode.anat_to_template_xfm"),
            ("template_to_anat_xfm", "inputnode.template_to_anat_xfm"),
        ]),
    ])
    # fmt:on

    # TODO: It would be nice to replace this for loop with MapNodes or iterables some day.
    for hemi in ["L", "R"]:
        hemi_label = f"{hemi.lower()}h"

        # Place the surfaces in a single node.
        collect_surfaces = pe.Node(
            niu.Merge(2),
            name=f"collect_surfaces_{hemi_label}",
        )

        # fmt:off
        # NOTE: Must match order of split_up_surfaces_fsLR_32k.
        workflow.connect([
            (inputnode, collect_surfaces, [
                (f"{hemi_label}_pial_surf", "in1"),
                (f"{hemi_label}_wm_surf", "in2"),
            ]),
        ])
        # fmt:on

        apply_transforms_wf = init_warp_one_hemisphere_wf(
            participant_id=subject_id,
            hemisphere=hemi,
            mem_gb=mem_gb,
            omp_nthreads=omp_nthreads,
            name=f"{hemi_label}_apply_transforms_wf",
        )

        # fmt:off
        workflow.connect([
            (get_freesurfer_dir_node, apply_transforms_wf, [
                ("freesurfer_path", "inputnode.freesurfer_path"),
            ]),
            (update_xfm_wf, apply_transforms_wf, [
                ("outputnode.merged_warpfield", "inputnode.merged_warpfield"),
                ("outputnode.merged_inv_warpfield", "inputnode.merged_inv_warpfield"),
                ("outputnode.world_xfm", "inputnode.world_xfm"),
            ]),
            (collect_surfaces, apply_transforms_wf, [("out", "inputnode.hemi_files")]),
        ])
        # fmt:on

        # Split up the surfaces
        # NOTE: Must match order of collect_surfaces
        split_up_surfaces_fsLR_32k = pe.Node(
            niu.Split(
                splits=[
                    1,  # pial
                    1,  # wm
                ],
                squeeze=True,
            ),
            name=f"split_up_surfaces_fsLR_32k_{hemi_label}",
        )

        # fmt:off
        workflow.connect([
            (apply_transforms_wf, split_up_surfaces_fsLR_32k, [
                ("outputnode.warped_hemi_files", "inlist"),
            ]),
            (split_up_surfaces_fsLR_32k, outputnode, [
                ("out1", f"{hemi_label}_pial_surf"),
                ("out2", f"{hemi_label}_wm_surf"),
            ]),
        ])
        # fmt:on

        ds_standard_space_surfaces = pe.MapNode(
            DerivativesDataSink(
                base_directory=output_dir,
                space="fsLR",
                den="32k",
                extension=".surf.gii",  # the extension is taken from the in_file by default
            ),
            name=f"ds_standard_space_surfaces_{hemi_label}",
            run_without_submitting=True,
            mem_gb=1,
            iterfield=["in_file", "source_file"],
        )

        # fmt:off
        workflow.connect([
            (collect_surfaces, ds_standard_space_surfaces, [("out", "source_file")]),
            (apply_transforms_wf, ds_standard_space_surfaces, [
                ("outputnode.warped_hemi_files", "in_file"),
            ]),
        ])
        # fmt:on

    return workflow


@fill_doc
def init_generate_hcp_surfaces_wf(
    output_dir,
    mem_gb,
    omp_nthreads,
    name="generate_hcp_surfaces_wf",
):
    """Generate midthickness, inflated, and very-inflated HCP-style surfaces.

    Workflow Graph
        .. workflow::
            :graph2use: orig
            :simple_form: yes

            from xcp_d.workflows.anatomical import init_generate_hcp_surfaces_wf

            wf = init_generate_hcp_surfaces_wf(
                output_dir=".",
                mem_gb=0.1,
                omp_nthreads=1,
                name="generate_hcp_surfaces_wf",
            )

    Parameters
    ----------
    %(output_dir)s
    %(mem_gb)s
    %(omp_nthreads)s
    %(name)s
        Default is "generate_hcp_surfaces_wf".

    Inputs
    ------
    name_source : :obj:`str`
        Path to the file that will be used as the source_file for datasinks.
    pial_surf : :obj:`str`
        The surface file to inflate.
    wm_surf : :obj:`str`
        The surface file to inflate.
    """
    workflow = Workflow(name=name)

    inputnode = pe.Node(
        niu.IdentityInterface(
            fields=[
                "name_source",
                "pial_surf",
                "wm_surf",
            ],
        ),
        name="inputnode",
    )

    generate_midthickness = pe.Node(
        SurfaceAverage(),
        name="generate_midthickness",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )

    # fmt:off
    workflow.connect([
        (inputnode, generate_midthickness, [
            ("pial_surf", "surface_in1"),
            ("wm_surf", "surface_in2"),
        ]),
    ])
    # fmt:on

    ds_midthickness = pe.Node(
        DerivativesDataSink(
            base_directory=output_dir,
            check_hdr=False,
            space="fsLR",
            den="32k",
            desc="hcp",
            suffix="midthickness",
            extension=".surf.gii",
        ),
        name="ds_midthickness",
        run_without_submitting=False,
        mem_gb=2,
    )

    # fmt:off
    workflow.connect([
        (inputnode, ds_midthickness, [("name_source", "source_file")]),
        (generate_midthickness, ds_midthickness, [("out_file", "in_file")]),
    ])
    # fmt:on

    # Generate (very-)inflated surface from standard-space midthickness surface.
    inflate_surface = pe.Node(
        SurfaceGenerateInflated(iterations_scale_value=0.75),
        mem_gb=mem_gb,
        omp_nthreads=omp_nthreads,
        name="inflate_surface",
    )

    # fmt:off
    workflow.connect([
        (generate_midthickness, inflate_surface, [("out_file", "anatomical_surface_in")]),
    ])
    # fmt:on

    ds_inflated = pe.Node(
        DerivativesDataSink(
            base_directory=output_dir,
            check_hdr=False,
            space="fsLR",
            den="32k",
            desc="hcp",
            suffix="inflated",
            extension=".surf.gii",
        ),
        name="ds_inflated",
        run_without_submitting=False,
        mem_gb=2,
    )

    # fmt:off
    workflow.connect([
        (inputnode, ds_inflated, [("name_source", "source_file")]),
        (inflate_surface, ds_inflated, [("inflated_out_file", "in_file")]),
    ])
    # fmt:on

    ds_vinflated = pe.Node(
        DerivativesDataSink(
            base_directory=output_dir,
            check_hdr=False,
            space="fsLR",
            den="32k",
            desc="hcp",
            suffix="vinflated",
            extension=".surf.gii",
        ),
        name="ds_vinflated",
        run_without_submitting=False,
        mem_gb=2,
    )

    # fmt:off
    workflow.connect([
        (inputnode, ds_vinflated, [("name_source", "source_file")]),
        (inflate_surface, ds_vinflated, [("very_inflated_out_file", "in_file")]),
    ])
    # fmt:on

    return workflow


@fill_doc
def init_ants_xfm_to_fsl_wf(mem_gb, omp_nthreads, name="ants_xfm_to_fsl_wf"):
    """Modify ANTS-style fMRIPrep transforms to work with Connectome Workbench/FSL FNIRT.

    Workflow Graph
        .. workflow::
            :graph2use: orig
            :simple_form: yes

            from xcp_d.workflows.anatomical import init_ants_xfm_to_fsl_wf

            wf = init_ants_xfm_to_fsl_wf(
                mem_gb=0.1,
                omp_nthreads=1,
                name="ants_xfm_to_fsl_wf",
            )

    Parameters
    ----------
    %(mem_gb)s
    %(omp_nthreads)s
    %(name)s
        Default is "ants_xfm_to_fsl_wf".

    Inputs
    ------
    anat_to_template_xfm
        ANTS/fMRIPrep-style H5 transform from T1w image to template.
    template_to_anat_xfm
        ANTS/fMRIPrep-style H5 transform from template to T1w image.

    Outputs
    -------
    world_xfm
        TODO: Add description.
    merged_warpfield
        TODO: Add description.
    merged_inv_warpfield
        TODO: Add description.
    """
    workflow = Workflow(name=name)

    inputnode = pe.Node(
        niu.IdentityInterface(fields=["anat_to_template_xfm", "template_to_anat_xfm"]),
        name="inputnode",
    )

    outputnode = pe.Node(
        niu.IdentityInterface(fields=["world_xfm", "merged_warpfield", "merged_inv_warpfield"]),
        name="outputnode",
    )

    # Now we can start the actual workflow.
    # use ANTs CompositeTransformUtil to separate the .h5 into affine and warpfield xfms
    disassemble_h5 = pe.Node(
        CompositeTransformUtil(
            process="disassemble",
            output_prefix="T1w_to_MNI152NLin6Asym",
        ),
        name="disassemble_h5",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )  # MB

    # fmt:off
    workflow.connect([(inputnode, disassemble_h5, [("anat_to_template_xfm", "in_file")])])
    # fmt:on

    # Nipype's CompositeTransformUtil assumes a certain file naming and
    # concatenation order of xfms which does not work for the inverse .h5,
    # so we use our modified class, "CompositeInvTransformUtil"
    disassemble_h5_inv = pe.Node(
        CompositeInvTransformUtil(
            process="disassemble",
            output_prefix="MNI152NLin6Asym_to_T1w",
        ),
        name="disassemble_h5_inv",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )

    # fmt:off
    workflow.connect([(inputnode, disassemble_h5_inv, [("template_to_anat_xfm", "in_file")])])
    # fmt:on

    # convert affine from ITK binary to txt
    convert_ants_transform = pe.Node(
        ConvertTransformFile(dimension=3),
        name="convert_ants_transform",
    )

    # fmt:off
    workflow.connect([
        (disassemble_h5, convert_ants_transform, [("affine_transform", "in_transform")]),
    ])
    # fmt:on

    # change xfm type from "AffineTransform" to "MatrixOffsetTransformBase"
    # since wb_command doesn't recognize "AffineTransform"
    # (AffineTransform is a subclass of MatrixOffsetTransformBase
    # which makes this okay to do AFAIK)
    change_xfm_type = pe.Node(ChangeXfmType(), name="change_xfm_type")

    # fmt:off
    workflow.connect([
        (convert_ants_transform, change_xfm_type, [("out_transform", "in_transform")]),
    ])
    # fmt:on

    # convert affine xfm to "world" so it works with -surface-apply-affine
    convert_xfm2world = pe.Node(
        ConvertAffine(fromwhat="itk", towhat="world"),
        name="convert_xfm2world",
    )

    # fmt:off
    workflow.connect([(change_xfm_type, convert_xfm2world, [("out_transform", "in_file")])])
    # fmt:on

    # use C3d to separate the combined warpfield xfm into x, y, and z components
    get_xyz_components = pe.Node(
        C3d(
            is_4d=True,
            multicomp_split=True,
            out_files=["e1.nii.gz", "e2.nii.gz", "e3.nii.gz"],
        ),
        name="get_xyz_components",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )
    get_inv_xyz_components = pe.Node(
        C3d(
            is_4d=True,
            multicomp_split=True,
            out_files=["e1inv.nii.gz", "e2inv.nii.gz", "e3inv.nii.gz"],
        ),
        name="get_inv_xyz_components",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )

    # fmt:off
    workflow.connect([
        (disassemble_h5, get_xyz_components, [("displacement_field", "in_file")]),
        (disassemble_h5_inv, get_inv_xyz_components, [("displacement_field", "in_file")]),
    ])
    # fmt:on

    # select x-component after separating warpfield above
    select_x_component = pe.Node(
        niu.Select(index=[0]),
        name="select_x_component",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )
    select_inv_x_component = pe.Node(
        niu.Select(index=[0]),
        name="select_inv_x_component",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )

    # select y-component
    select_y_component = pe.Node(
        niu.Select(index=[1]),
        name="select_y_component",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )
    select_inv_y_component = pe.Node(
        niu.Select(index=[1]),
        name="select_inv_y_component",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )

    # select z-component
    select_z_component = pe.Node(
        niu.Select(index=[2]),
        name="select_z_component",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )
    select_inv_z_component = pe.Node(
        niu.Select(index=[2]),
        name="select_inv_z_component",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )

    # fmt:off
    workflow.connect([
        (get_xyz_components, select_x_component, [("out_files", "inlist")]),
        (get_xyz_components, select_y_component, [("out_files", "inlist")]),
        (get_xyz_components, select_z_component, [("out_files", "inlist")]),
        (get_inv_xyz_components, select_inv_x_component, [("out_files", "inlist")]),
        (get_inv_xyz_components, select_inv_y_component, [("out_files", "inlist")]),
        (get_inv_xyz_components, select_inv_z_component, [("out_files", "inlist")]),
    ])
    # fmt:on

    # reverse y-component of the warpfield
    # (need to do this when converting a warpfield from ANTs to FNIRT format
    # for use with wb_command -surface-apply-warpfield)
    reverse_y_component = pe.Node(
        BinaryMath(expression="img * -1"),
        name="reverse_y_component",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )
    reverse_inv_y_component = pe.Node(
        BinaryMath(expression="img * -1"),
        name="reverse_inv_y_component",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )

    # fmt:off
    workflow.connect([
        (select_y_component, reverse_y_component, [("out", "in_file")]),
        (select_inv_y_component, reverse_inv_y_component, [("out", "in_file")]),
    ])
    # fmt:on

    # Collect new warpfield components in individual nodes
    collect_new_components = pe.Node(
        niu.Merge(3),
        name="collect_new_components",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )
    collect_new_inv_components = pe.Node(
        niu.Merge(3),
        name="collect_new_inv_components",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )

    # fmt:off
    workflow.connect([
        (select_x_component, collect_new_components, [("out", "in1")]),
        (reverse_y_component, collect_new_components, [("out_file", "in2")]),
        (select_z_component, collect_new_components, [("out", "in3")]),
        (select_inv_x_component, collect_new_inv_components, [("out", "in1")]),
        (reverse_inv_y_component, collect_new_inv_components, [("out_file", "in2")]),
        (select_inv_z_component, collect_new_inv_components, [("out", "in3")]),
    ])
    # fmt:on

    # Merge warpfield components in FSL FNIRT format, with the reversed y-component from above
    remerge_warpfield = pe.Node(
        Merge(),
        name="remerge_warpfield",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )
    remerge_inv_warpfield = pe.Node(
        Merge(),
        name="remerge_inv_warpfield",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )

    # fmt:off
    workflow.connect([
        (collect_new_components, remerge_warpfield, [("out", "in_files")]),
        (collect_new_inv_components, remerge_inv_warpfield, [("out", "in_files")]),
        (convert_xfm2world, outputnode, [("out_file", "world_xfm")]),
        (remerge_warpfield, outputnode, [("out_file", "merged_warpfield")]),
        (remerge_inv_warpfield, outputnode, [("out_file", "merged_inv_warpfield")]),
    ])
    # fmt:on

    return workflow


@fill_doc
def init_warp_one_hemisphere_wf(
    participant_id,
    hemisphere,
    mem_gb,
    omp_nthreads,
    name="warp_one_hemisphere_wf",
):
    """Apply transforms to warp one hemisphere's surface files into standard space.

    Workflow Graph
        .. workflow::
            :graph2use: orig
            :simple_form: yes

            from xcp_d.workflows.anatomical import init_warp_one_hemisphere_wf

            wf = init_warp_one_hemisphere_wf(
                participant_id="01",
                hemisphere="L",
                mem_gb=0.1,
                omp_nthreads=1,
                name="warp_one_hemisphere_wf",
            )

    Parameters
    ----------
    hemisphere : {"L", "R"}
    %(mem_gb)s
    %(omp_nthreads)s
    %(name)s
        Default is "warp_one_hemisphere_wf".

    Inputs
    ------
    hemi_files : list of str
        A list of surface files for the requested hemisphere, in fsnative space.
    world_xfm
    merged_warpfield
    merged_inv_warpfield
    freesurfer_path
        Path to FreeSurfer derivatives. Used to load the subject's sphere file.
    participant_id
        Set from parameters.

    Outputs
    -------
    warped_hemi_files
    """
    workflow = Workflow(name=name)

    inputnode = pe.Node(
        niu.IdentityInterface(
            fields=[
                "hemi_files",
                "world_xfm",
                "merged_warpfield",
                "merged_inv_warpfield",
                "freesurfer_path",
                "participant_id",
            ],
        ),
        name="inputnode",
    )
    inputnode.inputs.participant_id = participant_id

    # Load the fsaverage-164k sphere
    # NOTE: Why do we need the fsaverage mesh?
    fsaverage_mesh = str(
        get_template(
            template="fsaverage",
            space=None,
            hemi=hemisphere,
            density="164k",
            desc=None,
            suffix="sphere",
        )
    )

    # NOTE: Can we upload these to templateflow?
    fs_hemisphere_to_fsLR = pkgrf(
        "xcp_d",
        (
            f"data/standard_mesh_atlases/fs_{hemisphere}/"
            f"fs_{hemisphere}-to-fs_LR_fsaverage.{hemisphere}_LR.spherical_std."
            f"164k_fs_{hemisphere}.surf.gii"
        ),
    )
    get_freesurfer_sphere_node = pe.Node(
        Function(
            function=get_freesurfer_sphere,
            input_names=["freesurfer_path", "subject_id", "hemisphere"],
            output_names=["sphere_raw"],
        ),
        name="get_freesurfer_sphere_node",
    )
    get_freesurfer_sphere_node.inputs.hemisphere = hemisphere

    # fmt:off
    workflow.connect([
        (inputnode, get_freesurfer_sphere_node, [
            ("freesurfer_path", "freesurfer_path"),
            ("participant_id", "subject_id"),
        ])
    ])
    # fmt:on

    # NOTE: What does this step do?
    sphere_to_surf_gii = pe.Node(
        MRIsConvert(out_datatype="gii"),
        name="sphere_to_surf_gii",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
    )

    # fmt:off
    workflow.connect([
        (get_freesurfer_sphere_node, sphere_to_surf_gii, [("sphere_raw", "in_file")]),
    ])
    # fmt:on

    # NOTE: What does this step do?
    surface_sphere_project_unproject = pe.Node(
        SurfaceSphereProjectUnproject(
            sphere_project_to=fsaverage_mesh,
            sphere_unproject_from=fs_hemisphere_to_fsLR,
        ),
        name="surface_sphere_project_unproject",
    )

    # fmt:off
    workflow.connect([
        (sphere_to_surf_gii, surface_sphere_project_unproject, [("converted", "in_file")]),
    ])
    # fmt:on

    fsLR_sphere = str(
        get_template(
            template="fsLR",
            space=None,
            hemi=hemisphere,
            density="32k",
            desc=None,
            suffix="sphere",
        )
    )

    # resample the surfaces to fsLR-32k
    # NOTE: Does that mean the data are in fsLR-164k before this?
    resample_to_fsLR32k = pe.MapNode(
        CiftiSurfaceResample(
            new_sphere=fsLR_sphere,
            metric=" BARYCENTRIC ",
        ),
        name="resample_to_fsLR32k",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
        iterfield=["in_file"],
    )

    # fmt:off
    workflow.connect([
        (inputnode, resample_to_fsLR32k, [("hemi_files", "in_file")]),
        (surface_sphere_project_unproject, resample_to_fsLR32k, [("out_file", "current_sphere")]),
    ])
    # fmt:on

    # apply affine to 32k surfs
    # NOTE: What does this step do? Aren't the data in fsLR-32k from resample_to_fsLR32k?
    apply_affine_to_fsLR32k = pe.MapNode(
        ApplyAffine(),
        name="apply_affine_to_fsLR32k",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
        iterfield=["in_file"],
    )

    # fmt:off
    workflow.connect([
        (resample_to_fsLR32k, apply_affine_to_fsLR32k, [("out_file", "in_file")]),
        (inputnode, apply_affine_to_fsLR32k, [("world_xfm", "affine")]),
    ])
    # fmt:on

    # apply FNIRT-format warpfield
    # NOTE: What does this step do?
    apply_warpfield_to_fsLR32k = pe.MapNode(
        ApplyWarpfield(),
        name="apply_warpfield_to_fsLR32k",
        mem_gb=mem_gb,
        n_procs=omp_nthreads,
        iterfield=["in_file"],
    )

    # fmt:off
    workflow.connect([
        (inputnode, apply_warpfield_to_fsLR32k, [
            ("merged_warpfield", "forward_warp"),
            ("merged_inv_warpfield", "warpfield"),
        ]),
        (apply_affine_to_fsLR32k, apply_warpfield_to_fsLR32k, [("out_file", "in_file")]),
    ])
    # fmt:on

    outputnode = pe.Node(
        niu.IdentityInterface(fields=["warped_hemi_files"]),
        name="outputnode",
    )

    # fmt:off
    workflow.connect([
        (apply_warpfield_to_fsLR32k, outputnode, [("out_file", "warped_hemi_files")]),
    ])
    # fmt:on

    return workflow
