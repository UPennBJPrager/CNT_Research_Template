.
├── README.md
├── core_libraries
│   ├── README.md
│   ├── build
│   │   └── python
│   │       ├── RNS
│   │       │   └── build_RNS_toolbox
│   │       │       ├── LICENSE
│   │       │       ├── README.md
│   │       │       ├── dist
│   │       │       │   ├── RNS_toolbox-0.0.1-py3-none-any.whl
│   │       │       │   └── RNS_toolbox-0.0.1.tar.gz
│   │       │       ├── pyproject.toml
│   │       │       └── src
│   │       │           ├── RNS_toolbox -> ../../../../../submodules/RNS_processing_toolbox
│   │       │           └── RNS_toolbox.egg-info
│   │       │               ├── PKG-INFO
│   │       │               ├── SOURCES.txt
│   │       │               ├── dependency_links.txt
│   │       │               └── top_level.txt
│   │       ├── active_wear
│   │       │   └── build_LB3_processing
│   │       │       ├── LICENSE
│   │       │       ├── README.md
│   │       │       ├── dist
│   │       │       │   ├── LB3_processing-0.0.1-py3-none-any.whl
│   │       │       │   └── LB3_processing-0.0.1.tar.gz
│   │       │       ├── pyproject.toml
│   │       │       └── src
│   │       │           ├── LB3_processing -> ../../../../../submodules/LB3_processing/wearables/tools
│   │       │           └── LB3_processing.egg-info
│   │       │               ├── PKG-INFO
│   │       │               ├── SOURCES.txt
│   │       │               ├── dependency_links.txt
│   │       │               └── top_level.txt
│   │       ├── ieeg
│   │       │   ├── build_CNT_research_tools
│   │       │   │   ├── LICENSE
│   │       │   │   ├── README.md
│   │       │   │   ├── dist
│   │       │   │   │   ├── CNT_research_tools-0.0.1-py3-none-any.whl
│   │       │   │   │   └── CNT_research_tools-0.0.1.tar.gz
│   │       │   │   ├── pyproject.toml
│   │       │   │   └── src
│   │       │   │       ├── CNT_research_tools
│   │       │   │       │   ├── __init__.py -> ../../../../../../submodules/CNT_research_tools/python/tools/__init__.py
│   │       │   │       │   ├── automatic_bipolar_montage.py -> ../../../../../../submodules/CNT_research_tools/python/tools/automatic_bipolar_montage.py
│   │       │   │       │   ├── bandpower.py -> ../../../../../../submodules/CNT_research_tools/python/tools/bandpower.py
│   │       │   │       │   ├── clean_labels.py -> ../../../../../../submodules/CNT_research_tools/python/tools/clean_labels.py
│   │       │   │       │   ├── find_non_ieeg.py -> ../../../../../../submodules/CNT_research_tools/python/tools/find_non_ieeg.py
│   │       │   │       │   ├── get_iEEG_data.py -> ../../../../../../submodules/CNT_research_tools/python/tools/get_iEEG_data.py
│   │       │   │       │   ├── gini.py -> ../../../../../../submodules/CNT_research_tools/python/tools/gini.py
│   │       │   │       │   ├── line_length.py -> ../../../../../../submodules/CNT_research_tools/python/tools/line_length.py
│   │       │   │       │   ├── movmean.py -> ../../../../../../submodules/CNT_research_tools/python/tools/movmean.py
│   │       │   │       │   ├── plot_iEEG_data.py -> ../../../../../../submodules/CNT_research_tools/python/tools/plot_iEEG_data.py
│   │       │   │       │   ├── pull_patient_localization.py -> ../../../../../../submodules/CNT_research_tools/python/tools/pull_patient_localization.py
│   │       │   │       │   ├── pull_sz_ends.py -> ../../../../../../submodules/CNT_research_tools/python/tools/pull_sz_ends.py
│   │       │   │       │   └── pull_sz_starts.py -> ../../../../../../submodules/CNT_research_tools/python/tools/pull_sz_starts.py
│   │       │   │       └── CNT_research_tools.egg-info
│   │       │   │           ├── PKG-INFO
│   │       │   │           ├── SOURCES.txt
│   │       │   │           ├── dependency_links.txt
│   │       │   │           └── top_level.txt
│   │       │   ├── build_CNT_unit_tests
│   │       │   │   ├── LICENSE
│   │       │   │   ├── README.md
│   │       │   │   ├── dist
│   │       │   │   │   ├── CNT_unit_tests-0.0.1-py3-none-any.whl
│   │       │   │   │   └── CNT_unit_tests-0.0.1.tar.gz
│   │       │   │   ├── pyproject.toml
│   │       │   │   └── src
│   │       │   │       ├── CNT_unit_tests
│   │       │   │       │   ├── __init__.py
│   │       │   │       │   ├── machine_level
│   │       │   │       │   │   ├── __init__.py
│   │       │   │       │   │   └── array_unit_tests.py -> /Users/bjprager/Documents/REPOSITORIES/CNT_PROJECT_TEMPLATE/CNT_Development/unit_tests/machine_level/array_unit_tests.py
│   │       │   │       │   └── model_level
│   │       │   │       │       ├── __init__.py
│   │       │   │       │       └── classification_f1_score.py -> /Users/bjprager/Documents/REPOSITORIES/CNT_PROJECT_TEMPLATE/CNT_Development/unit_tests/model_level/classification_f1_score.py
│   │       │   │       └── CNT_unit_tests.egg-info
│   │       │   │           ├── PKG-INFO
│   │       │   │           ├── SOURCES.txt
│   │       │   │           ├── dependency_links.txt
│   │       │   │           └── top_level.txt
│   │       │   ├── build_ieegpy
│   │       │   │   ├── LICENSE.md -> ../../../../submodules/ieegpy/LICENSE.md
│   │       │   │   ├── README.md -> ../../../../submodules/ieegpy/README.md
│   │       │   │   ├── build
│   │       │   │   │   ├── bdist.macosx-10.9-x86_64
│   │       │   │   │   └── lib
│   │       │   │   │       └── ieeg
│   │       │   │   │           ├── __init__.py
│   │       │   │   │           ├── annotation_processing.py
│   │       │   │   │           ├── auth.py
│   │       │   │   │           ├── dataset.py
│   │       │   │   │           ├── ieeg_api.py
│   │       │   │   │           ├── ieeg_auth.py
│   │       │   │   │           ├── mprov_listener.py
│   │       │   │   │           └── processing.py
│   │       │   │   ├── examples -> ../../../../submodules/ieegpy/examples
│   │       │   │   ├── ieeg -> ../../../../submodules/ieegpy/ieeg
│   │       │   │   ├── ieeg-1.6-py3-none-any.whl
│   │       │   │   ├── ieeg.egg-info
│   │       │   │   │   ├── PKG-INFO
│   │       │   │   │   ├── SOURCES.txt
│   │       │   │   │   ├── dependency_links.txt
│   │       │   │   │   ├── requires.txt
│   │       │   │   │   └── top_level.txt
│   │       │   │   ├── read_sample.py -> ../../../../submodules/ieegpy/read_sample.py
│   │       │   │   └── setup.py -> ../../../../submodules/ieegpy/setup.py
│   │       │   └── build_pipeline_ieeg
│   │       │       ├── LICENSE
│   │       │       ├── README.md
│   │       │       ├── dist
│   │       │       │   ├── pipeline_ieeg-0.0.1-py3-none-any.whl
│   │       │       │   └── pipeline_ieeg-0.0.1.tar.gz
│   │       │       ├── pyproject.toml
│   │       │       └── src
│   │       │           ├── pipeline_ieeg
│   │       │           │   ├── __init__.py
│   │       │           │   ├── data_pull
│   │       │           │   │   ├── __init__.py
│   │       │           │   │   ├── check_data_repository.py -> /Users/bjprager/Documents/REPOSITORIES/CNT_PROJECT_TEMPLATE/CNT_Development/scripts/python/users/bjprager/pipeline_ieeg/data_pull/check_data_repository.py
│   │       │           │   │   ├── get_dummy_data.py -> /Users/bjprager/Documents/REPOSITORIES/CNT_PROJECT_TEMPLATE/CNT_Development/scripts/python/users/bjprager/pipeline_ieeg/data_pull/get_dummy_data.py
│   │       │           │   │   └── pipeline_datapull_ieeg.py -> /Users/bjprager/Documents/REPOSITORIES/CNT_PROJECT_TEMPLATE/CNT_Development/scripts/python/users/bjprager/pipeline_ieeg/data_pull/pipeline_datapull_ieeg.py
│   │       │           │   ├── data_quality
│   │       │           │   │   ├── __init__.py
│   │       │           │   │   ├── dataframe_properties_check.py -> /Users/bjprager/Documents/REPOSITORIES/CNT_PROJECT_TEMPLATE/CNT_Development/scripts/python/users/bjprager/pipeline_ieeg/data_quality/dataframe_properties_check.py
│   │       │           │   │   ├── hash_check.py -> /Users/bjprager/Documents/REPOSITORIES/CNT_PROJECT_TEMPLATE/CNT_Development/scripts/python/users/bjprager/pipeline_ieeg/data_quality/hash_check.py
│   │       │           │   │   └── variance_check.py -> /Users/bjprager/Documents/REPOSITORIES/CNT_PROJECT_TEMPLATE/CNT_Development/scripts/python/users/bjprager/pipeline_ieeg/data_quality/variance_check.py
│   │       │           │   ├── feature_selection
│   │       │           │   │   ├── __init__.py
│   │       │           │   │   └── pipeline_feature_selection_ieeg.py -> /Users/bjprager/Documents/REPOSITORIES/CNT_PROJECT_TEMPLATE/CNT_Development/scripts/python/users/bjprager/pipeline_ieeg/feature_selection/pipeline_feature_selection_ieeg.py
│   │       │           │   └── preprocessing
│   │       │           │       ├── __init__.py
│   │       │           │       └── pipeline_preprocessing_ieeg.py -> /Users/bjprager/Documents/REPOSITORIES/CNT_PROJECT_TEMPLATE/CNT_Development/scripts/python/users/bjprager/pipeline_ieeg/preprocessing/pipeline_preprocessing_ieeg.py
│   │       │           └── pipeline_ieeg.egg-info
│   │       │               ├── PKG-INFO
│   │       │               ├── SOURCES.txt
│   │       │               ├── dependency_links.txt
│   │       │               └── top_level.txt
│   │       └── imaging
│   │           └── build_bctpy
│   │               ├── bctpy-0.6.0-py3-none-any.whl
│   │               └── bctpy-0.6.0.tar.gz
│   ├── matlab
│   │   └── README.md
│   ├── python
│   │   ├── RNS
│   │   │   ├── README.txt
│   │   │   ├── RNS_toolbox-0.0.1-py3-none-any.whl
│   │   │   └── RNS_toolbox-0.0.1.tar.gz
│   │   ├── active_wear
│   │   │   ├── LB3_processing-0.0.1-py3-none-any.whl
│   │   │   ├── LB3_processing-0.0.1.tar.gz
│   │   │   └── README.txt
│   │   ├── ieeg
│   │   │   ├── CNT_research_tools-0.0.1-py3-none-any.whl
│   │   │   ├── CNT_unit_tests-0.0.1-py3-none-any.whl
│   │   │   ├── README.md
│   │   │   ├── ieeg-1.6-py3-none-any.whl
│   │   │   ├── ieeg_environment.yml
│   │   │   └── pipeline_ieeg-0.0.1-py3-none-any.whl
│   │   └── imaging
│   │       ├── README.txt
│   │       ├── bctpy-0.6.0-py3-none-any.whl
│   │       └── bctpy-0.6.0.tar.gz
│   └── submodules
│       ├── CNT_research_tools
│       │   ├── Matlab
│       │   │   ├── ReadMe.m
│       │   │   ├── artifact_identification
│       │   │   │   └── identify_bad_chs.m
│       │   │   ├── channel_processing
│       │   │   │   ├── decompose_labels.m
│       │   │   │   ├── find_non_intracranial.m
│       │   │   │   └── reconcile_ch_names.m
│       │   │   ├── data_import
│       │   │   │   └── download_ieeg_data.m
│       │   │   ├── filters
│       │   │   │   ├── bandpass_filter.m
│       │   │   │   └── notch_filter.m
│       │   │   ├── other_eeg_processing
│       │   │   │   └── pre_whiten.m
│       │   │   ├── references
│       │   │   │   ├── bipolar_montage.m
│       │   │   │   ├── common_average_reference.m
│       │   │   │   └── laplacian_reference.m
│       │   │   ├── testing
│       │   │   │   └── pipeline_test_clip.m
│       │   │   └── visualization
│       │   │       └── show_eeg.m
│       │   ├── README.md
│       │   ├── config_example.json
│       │   └── python
│       │       ├── 99-example_ieeg.py
│       │       ├── ieegpy-base.yml
│       │       ├── ieegpy.yml
│       │       └── tools
│       │           ├── __init__.py
│       │           ├── __pycache__
│       │           │   ├── __init__.cpython-38.pyc
│       │           │   ├── add_img_to_ppt.cpython-38.pyc
│       │           │   ├── automatic_bipolar_montage.cpython-38.pyc
│       │           │   ├── bandpower.cpython-38.pyc
│       │           │   ├── clean_channels.cpython-38.pyc
│       │           │   ├── get_iEEG_data.cpython-310.pyc
│       │           │   ├── get_iEEG_data.cpython-36.pyc
│       │           │   ├── get_iEEG_data.cpython-37.pyc
│       │           │   ├── get_iEEG_data.cpython-38.pyc
│       │           │   ├── gini.cpython-38.pyc
│       │           │   ├── line_length.cpython-38.pyc
│       │           │   ├── movmean.cpython-38.pyc
│       │           │   ├── plot_iEEG_data.cpython-38.pyc
│       │           │   ├── pull_patient_localization.cpython-310.pyc
│       │           │   ├── pull_patient_localization.cpython-37.pyc
│       │           │   ├── pull_patient_localization.cpython-38.pyc
│       │           │   ├── pull_sz_ends.cpython-38.pyc
│       │           │   └── pull_sz_starts.cpython-38.pyc
│       │           ├── automatic_bipolar_montage.py
│       │           ├── bandpower.py
│       │           ├── clean_labels.py
│       │           ├── find_non_ieeg.py
│       │           ├── get_iEEG_data.py
│       │           ├── gini.py
│       │           ├── line_length.py
│       │           ├── movmean.py
│       │           ├── plot_iEEG_data.py
│       │           ├── pull_patient_localization.py
│       │           ├── pull_sz_ends.py
│       │           └── pull_sz_starts.py
│       ├── LB3_processing
│       │   └── wearables
│       │       └── tools
│       │           ├── apple_parse.py
│       │           ├── helpers_jp.py
│       │           ├── parse_convert_hr_acc_data.ipynb
│       │           ├── patient_summary.ipynb
│       │           ├── plot_timeline.py
│       │           ├── sleep_parser.ipynb
│       │           └── subject_metadata_jp.json
│       ├── README.md
│       ├── RNS_processing_toolbox
│       │   ├── README.md
│       │   ├── config_example.JSON
│       │   ├── lib
│       │   │   └── MEF_writer.jar
│       │   ├── matlab_tools
│       │   │   ├── ecog
│       │   │   │   ├── RNShistogram.m
│       │   │   │   ├── classifyECoG.m
│       │   │   │   ├── findStim.m
│       │   │   │   └── getFeatures.m
│       │   │   ├── example_analysis.m
│       │   │   ├── pipelines
│       │   │   │   ├── RNS_raw_feature_pipeline.m
│       │   │   │   ├── episode_detection_pipeline.m
│       │   │   │   ├── process_raw.m
│       │   │   │   └── stim_detection_pipeline.m
│       │   │   ├── test
│       │   │   │   └── test_filter_windows.m
│       │   │   ├── utils
│       │   │   │   ├── filterWindows.m
│       │   │   │   ├── getDetectionsInRecordedEvents.m
│       │   │   │   ├── getEpisodeDurationsFileInfo.m
│       │   │   │   ├── idx2event.m
│       │   │   │   ├── idx2time.m
│       │   │   │   ├── loadRNSptData.m
│       │   │   │   ├── parsePDMS_file.m
│       │   │   │   ├── parsePDMSdetections.m
│       │   │   │   └── ptPth.m
│       │   │   └── visualize
│       │   │       └── vis_event.m
│       │   ├── props
│       │   │   ├── data_system.png
│       │   │   └── system_docs.pptx
│       │   ├── rns_processing_toolbox.yml
│       │   └── rns_py_tools
│       │       ├── LICENSE
│       │       ├── functions
│       │       │   ├── NPDataHandler.py
│       │       │   ├── PDMSpdf_to_csv.py
│       │       │   ├── __init__.py
│       │       │   ├── pennsieve_tools.py
│       │       │   ├── utils.py
│       │       │   └── visualize.py
│       │       ├── pennsieve_pipeline.py
│       │       ├── process_raw.py
│       │       └── test_pytools.py
│       ├── bctpy
│       │   ├── CHANGELOG.md
│       │   ├── CREDITS
│       │   ├── LICENSE
│       │   ├── README.md
│       │   ├── bct
│       │   │   ├── __init__.py
│       │   │   ├── algorithms
│       │   │   │   ├── __init__.py
│       │   │   │   ├── centrality.py
│       │   │   │   ├── clustering.py
│       │   │   │   ├── core.py
│       │   │   │   ├── degree.py
│       │   │   │   ├── distance.py
│       │   │   │   ├── generative.py
│       │   │   │   ├── modularity.py
│       │   │   │   ├── motifs.py
│       │   │   │   ├── physical_connectivity.py
│       │   │   │   ├── reference.py
│       │   │   │   └── similarity.py
│       │   │   ├── citations.py
│       │   │   ├── due.py
│       │   │   ├── motif34lib.mat
│       │   │   ├── nbs.py
│       │   │   ├── utils
│       │   │   │   ├── __init__.py
│       │   │   │   ├── miscellaneous_utilities.py
│       │   │   │   ├── other.py
│       │   │   │   └── visualization.py
│       │   │   └── version.py
│       │   ├── bctpy.egg-info
│       │   │   ├── PKG-INFO
│       │   │   ├── SOURCES.txt
│       │   │   ├── dependency_links.txt
│       │   │   ├── requires.txt
│       │   │   └── top_level.txt
│       │   ├── docs
│       │   │   ├── Makefile
│       │   │   ├── _build
│       │   │   │   ├── doctrees
│       │   │   │   │   ├── _templates
│       │   │   │   │   │   └── function.doctree
│       │   │   │   │   ├── bct.doctree
│       │   │   │   │   ├── environment.pickle
│       │   │   │   │   ├── index.doctree
│       │   │   │   │   ├── modules.doctree
│       │   │   │   │   └── stupid.doctree
│       │   │   │   └── html
│       │   │   │       ├── _sources
│       │   │   │       │   ├── _templates
│       │   │   │       │   │   └── function.txt
│       │   │   │       │   ├── bct.txt
│       │   │   │       │   ├── index.txt
│       │   │   │       │   ├── modules.txt
│       │   │   │       │   └── stupid.txt
│       │   │   │       ├── _static
│       │   │   │       │   ├── ajax-loader.gif
│       │   │   │       │   ├── basic.css
│       │   │   │       │   ├── comment-bright.png
│       │   │   │       │   ├── comment-close.png
│       │   │   │       │   ├── comment.png
│       │   │   │       │   ├── default.css
│       │   │   │       │   ├── doctools.js
│       │   │   │       │   ├── down-pressed.png
│       │   │   │       │   ├── down.png
│       │   │   │       │   ├── file.png
│       │   │   │       │   ├── jquery.js
│       │   │   │       │   ├── minus.png
│       │   │   │       │   ├── plus.png
│       │   │   │       │   ├── pygments.css
│       │   │   │       │   ├── searchtools.js
│       │   │   │       │   ├── sidebar.js
│       │   │   │       │   ├── underscore.js
│       │   │   │       │   ├── up-pressed.png
│       │   │   │       │   ├── up.png
│       │   │   │       │   └── websupport.js
│       │   │   │       ├── _templates
│       │   │   │       │   └── function.html
│       │   │   │       ├── bct.html
│       │   │   │       ├── genindex.html
│       │   │   │       ├── index.html
│       │   │   │       ├── modules.html
│       │   │   │       ├── np-modindex.html
│       │   │   │       ├── objects.inv
│       │   │   │       ├── py-modindex.html
│       │   │   │       ├── search.html
│       │   │   │       ├── searchindex.js
│       │   │   │       └── stupid.html
│       │   │   ├── _templates
│       │   │   │   └── function.rst
│       │   │   ├── bct.rst
│       │   │   ├── conf.py
│       │   │   ├── index.rst
│       │   │   ├── modules.rst
│       │   │   └── sphinxext
│       │   │       └── numpy_ext
│       │   │           ├── __init__.py
│       │   │           ├── docscrape.py
│       │   │           ├── docscrape_sphinx.py
│       │   │           └── numpydoc.py
│       │   ├── function_reference.html
│       │   ├── requirements.txt
│       │   ├── setup.py
│       │   ├── test
│       │   │   ├── __init__.py
│       │   │   ├── basic_test.py
│       │   │   ├── centrality_test.py
│       │   │   ├── clustering_test.py
│       │   │   ├── conftest.py
│       │   │   ├── core_test.py
│       │   │   ├── distance_test.py
│       │   │   ├── duecredit_test.py
│       │   │   ├── failing_cases
│       │   │   │   └── modularity_dir_example.csv
│       │   │   ├── load_samples.py
│       │   │   ├── mats
│       │   │   │   ├── sample_data.mat
│       │   │   │   ├── sample_data.npy
│       │   │   │   ├── sample_directed.mat
│       │   │   │   ├── sample_directed.npy
│       │   │   │   ├── sample_directed_gc.mat
│       │   │   │   ├── sample_directed_gc.npy
│       │   │   │   ├── sample_group_dsi.mat
│       │   │   │   ├── sample_group_dsi.npy
│       │   │   │   ├── sample_group_fmri.mat
│       │   │   │   ├── sample_group_fmri.npy
│       │   │   │   ├── sample_group_qball.mat
│       │   │   │   ├── sample_group_qball.npy
│       │   │   │   ├── sample_partition.mat
│       │   │   │   ├── sample_partition.npy
│       │   │   │   ├── sample_pc.mat
│       │   │   │   ├── sample_pc.npy
│       │   │   │   ├── sample_signed.mat
│       │   │   │   ├── sample_signed.npy
│       │   │   │   ├── sample_signed_partition.mat
│       │   │   │   ├── sample_zi.mat
│       │   │   │   └── sample_zi.npy
│       │   │   ├── modularity_derived_metrics_test.py
│       │   │   ├── modularity_test.py
│       │   │   ├── nbs_test.py
│       │   │   ├── nodals_test.py
│       │   │   ├── partition_distance_test.py
│       │   │   ├── reference_test.py
│       │   │   ├── simple_script.py
│       │   │   └── very_long_test.py
│       │   └── tox.ini
│       ├── epycom
│       │   ├── LICENSE.txt
│       │   ├── doc
│       │   │   ├── Makefile
│       │   │   ├── conf.py
│       │   │   ├── feature_extraction.rst
│       │   │   └── index.rst
│       │   ├── epycom
│       │   │   ├── __init__.py
│       │   │   ├── artifact_detection
│       │   │   │   ├── __init__.py
│       │   │   │   ├── powerline_noise.py
│       │   │   │   ├── saturation.py
│       │   │   │   └── tests
│       │   │   │       ├── conftest.py
│       │   │   │       └── test_artifact_detection.py
│       │   │   ├── bivariate
│       │   │   │   ├── __init__.py
│       │   │   │   ├── coherence.py
│       │   │   │   ├── linear_correlation.py
│       │   │   │   ├── phase_consistency.py
│       │   │   │   ├── phase_lag_index.py
│       │   │   │   ├── phase_synchrony.py
│       │   │   │   ├── relative_entropy.py
│       │   │   │   ├── spectra_multiplication.py
│       │   │   │   └── tests
│       │   │   │       ├── conftest.py
│       │   │   │       └── test_bivariate.py
│       │   │   ├── event_detection
│       │   │   │   ├── __init__.py
│       │   │   │   ├── hfo
│       │   │   │   │   ├── __init__.py
│       │   │   │   │   ├── cs_detector.py
│       │   │   │   │   ├── hilbert_detector.py
│       │   │   │   │   ├── ll_detector.py
│       │   │   │   │   └── rms_detector.py
│       │   │   │   ├── spike
│       │   │   │   │   ├── __init__.py
│       │   │   │   │   └── barkmeier_detector.py
│       │   │   │   └── tests
│       │   │   │       ├── conftest.py
│       │   │   │       └── test_event_detection.py
│       │   │   ├── simulation
│       │   │   │   ├── __init__.py
│       │   │   │   ├── create_simulated.py
│       │   │   │   └── tests
│       │   │   │       └── test_simulation.py
│       │   │   ├── univariate
│       │   │   │   ├── __init__.py
│       │   │   │   ├── approximate_entropy.py
│       │   │   │   ├── arr.py
│       │   │   │   ├── hjorth_complexity.py
│       │   │   │   ├── hjorth_mobility.py
│       │   │   │   ├── lyapunov_exponent.py
│       │   │   │   ├── mean_vector_length.py
│       │   │   │   ├── modulation_index.py
│       │   │   │   ├── phase_locking_value.py
│       │   │   │   ├── power_spectral_entropy.py
│       │   │   │   ├── sample_entropy.py
│       │   │   │   ├── shannon_entropy.py
│       │   │   │   ├── signal_stats.py
│       │   │   │   └── tests
│       │   │   │       ├── conftest.py
│       │   │   │       └── test_univariate.py
│       │   │   ├── utils
│       │   │   │   ├── __init__.py
│       │   │   │   ├── data_operations.py
│       │   │   │   ├── method.py
│       │   │   │   ├── signal_transforms.py
│       │   │   │   ├── tests
│       │   │   │   │   ├── conftest.py
│       │   │   │   │   └── test_utils.py
│       │   │   │   ├── thresholds.py
│       │   │   │   └── tools.py
│       │   │   └── validation
│       │   │       ├── __init__.py
│       │   │       ├── feature_evaluation.py
│       │   │       ├── precision_recall.py
│       │   │       ├── tests
│       │   │       │   ├── conftest.py
│       │   │       │   └── test_validation.py
│       │   │       └── util.py
│       │   ├── readme.rst
│       │   ├── setup.cfg
│       │   └── setup.py
│       └── ieegpy
│           ├── LICENSE.md
│           ├── README.md
│           ├── examples
│           │   ├── annotations.py
│           │   ├── dataset_start_time.py
│           │   ├── get_data.py
│           │   ├── montages.py
│           │   └── mprov_example.py
│           ├── ieeg
│           │   ├── __init__.py
│           │   ├── annotation_processing.py
│           │   ├── auth.py
│           │   ├── dataset.py
│           │   ├── ieeg_api.py
│           │   ├── ieeg_auth.py
│           │   ├── mprov_listener.py
│           │   └── processing.py
│           ├── read_sample.py
│           └── setup.py
├── data_pointers
│   ├── active_wear
│   │   └── notes.txt
│   ├── ieeg
│   │   ├── cached_ieeg_data.csv
│   │   └── notes.txt
│   └── images
│       └── notes.txt
├── documents
│   ├── SOP
│   │   └── Pioneer
│   │       └── Pioneer-iEEG-v0_2.docx
│   ├── libraries
│   │   ├── CNT_research_tools
│   │   │   └── Modules.md
│   │   └── epycom
│   │       ├── artifact_detection
│   │       │   └── Modules.md
│   │       ├── bivariate
│   │       │   └── Modules.md
│   │       ├── event_detection
│   │       │   └── Modules.md
│   │       ├── simulation
│   │       │   └── Modules.md
│   │       ├── univariate
│   │       │   └── Modules.md
│   │       ├── utils
│   │       │   └── Modules.md
│   │       └── validation
│   │           └── Modules.md
│   └── workflows
│       └── Pioneer
│           ├── Pioneer_Chatbot_v0.2.drawio.png
│           └── Pioneer_iEEG_v0.2.drawio.png
├── examples
│   ├── ieeg
│   │   └── README.md
│   └── pipeline
│       ├── RNS
│       │   └── README.md
│       └── ieeg
│           ├── README.md
│           ├── iEEG_example.ipynb
│           └── ieeg_workflow.py -> /Users/bjprager/Documents/REPOSITORIES/CNT_PROJECT_TEMPLATE/CNT_Development/scripts/python/users/bjprager/ieeg_workflow.py
├── reference_data
│   ├── README.txt
│   ├── ieeg
│   │   └── manual_validation
│   │       ├── DATA
│   │       │   ├── All
│   │       │   │   └── All.csv
│   │       │   ├── AllSeizureTimes
│   │       │   │   └── AllSeizureTimes.csv
│   │       │   ├── Coherence run
│   │       │   │   └── Coherence run.csv
│   │       │   ├── EDF pipeline
│   │       │   │   └── EDF pipeline.csv
│   │       │   ├── FileStartTimes
│   │       │   │   └── FileStartTimes.csv
│   │       │   ├── Jim SOZ
│   │       │   │   └── Jim SOZ.csv
│   │       │   ├── Peri-ictal
│   │       │   │   └── Peri-ictal.csv
│   │       │   ├── Pre-implant data
│   │       │   │   └── Pre-implant data.csv
│   │       │   ├── SOZ
│   │       │   │   └── SOZ.csv
│   │       │   ├── SpikeCounts
│   │       │   │   └── SpikeCounts.csv
│   │       │   ├── Stereo
│   │       │   │   └── Stereo.csv
│   │       │   └── Validation Sw
│   │       │       └── Validation Sw.csv
│   │       ├── README.txt
│   │       ├── manual_validation.xlsx
│   │       └── validation_to_csv.py
│   └── imaging
│       └── PLACEHOLDER.txt
├── repository_structure.md
├── sample_data
│   ├── active_wear
│   │   └── PLACEHOLDER.txt
│   ├── ieeg
│   │   └── notes.txt
│   └── imaging
│       └── Sirius_Mira_01.jpg
├── scripts
│   ├── linux_setenv.sh
│   ├── mac_setenv.sh
│   ├── matlab
│   │   └── PLACEHOLDER.txt
│   └── python
│       ├── build_template
│       │   ├── LICENSE
│       │   ├── README.md
│       │   ├── dist
│       │   │   ├── pipeline_ieeg-0.0.1-py3-none-any.whl
│       │   │   └── pipeline_ieeg-0.0.1.tar.gz
│       │   ├── pyproject.toml
│       │   └── src
│       │       ├── pipeline_ieeg
│       │       │   ├── __init__.py
│       │       │   ├── data_pull
│       │       │   │   ├── __init__.py
│       │       │   │   ├── check_data_repository.py
│       │       │   │   ├── get_dummy_data.py
│       │       │   │   └── pipeline_datapull_ieeg.py
│       │       │   ├── data_quality
│       │       │   │   ├── __init__.py
│       │       │   │   ├── dataframe_properties_check.py
│       │       │   │   ├── hash_check.py
│       │       │   │   └── variance_check.py
│       │       │   ├── feature_selection
│       │       │   │   ├── __init__.py
│       │       │   │   └── pipeline_feature_selection_ieeg.py
│       │       │   └── preprocessing
│       │       │       ├── __init__.py
│       │       │       └── pipeline_preprocessing_ieeg.py
│       │       └── pipeline_ieeg.egg-info
│       │           ├── PKG-INFO
│       │           ├── SOURCES.txt
│       │           ├── dependency_links.txt
│       │           └── top_level.txt
│       └── users
│           ├── README.md
│           └── bjprager
│               ├── ieeg_workflow.py
│               ├── make_library_docs.py
│               └── pipeline_ieeg
│                   ├── data_pull
│                   │   ├── check_data_repository.py
│                   │   ├── get_dummy_data.py
│                   │   └── pipeline_datapull_ieeg.py
│                   ├── data_push
│                   │   └── PLACEHOLDER.txt
│                   ├── data_quality
│                   │   ├── dataframe_properties_check.py
│                   │   ├── hash_check.py
│                   │   └── variance_check.py
│                   ├── feature_selection
│                   │   └── pipeline_feature_selection_ieeg.py
│                   ├── preprocessing
│                   │   └── pipeline_preprocessing_ieeg.py
│                   ├── testing
│                   │   ├── __init__.py
│                   │   └── acceptance_criteria.py
│                   └── training
│                       ├── PLACEHOLDER.txt
│                       └── __init__.py
├── unit_tests
│   ├── __pycache__
│   │   ├── array_unit_tests.cpython-39.pyc
│   │   └── classification_f1_score.cpython-39.pyc
│   ├── machine_level
│   │   ├── README.txt
│   │   └── array_unit_tests.py
│   └── model_level
│       └── classification_f1_score.py
└── user_data
    ├── I004_A0003_D001-13090000_100000
    │   └── data.pickle
    └── README.txt

197 directories, 506 files
