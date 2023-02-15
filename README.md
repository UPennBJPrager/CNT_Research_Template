CNT Research Repository Template
================
![version](https://img.shields.io/badge/version-0.2.1-blue)
![pip](https://img.shields.io/pypi/v/pip.svg)
![https://img.shields.io/pypi/pyversions/](https://img.shields.io/pypi/pyversions/4)

The purpose of this template is to consolidate shared libraries and enable consistent workflows and tests for most projects in the CNT lab. Users will be able to quickly load code from tested common libraries, or load their own personal code, in an object oriented manner.

# Prerequisites
In order to use this repository, you must have access to either Python or Matlab. 

We also highly recommend the use of a virtual environment, conda environment, or similar software to manage distributions. Examples for their use can be found in the documentation.

# Installation

In order to install any of the common library code, we provide instructions for both Python and Matlab below.

## Python
For python packages, python wheels and tarballs can be found in: CNT_Development/core_libraries/python/.

To install, run:

pip install foo.whl

**or**

pip install foo.tar.gz

where foo is the name of the library of interest.

## Matlab

:woman_shrugging:

# Documentation
This template is intended to be used as both an environment and a simple wrapper for research code. Before beginning, we highly recommend that a virtual environment is made for each project to ensure dependencies are properly referenced and code can be reproduced across numerous systems. Examples for creating virtual environments is provided below.

## Repository Structure
./. 
├── core_libraries. 
│   ├── python. 
│   └── submodules. 
├── data_pointers. 
│   ├── active_wear. 
│   ├── ieeg. 
│   └── images. 
├── examples  
│   └── environments. 
├── reference_data. 
│   ├── ieeg. 
│   └── imaging. 
├── sample_data. 
│   ├── active_wear. 
│   ├── ieeg. 
│   └── imaging. 
├── scripts. 
│   ├── matlab. 
│   └── python. 
├── unit_tests. 
│   ├── __pycache__. 
│   ├── machine_level. 
│   └── model_level. 
└── user_data. 

# Virtual Environments

## Python

### Conda

#### Creation
conda create --name myenv **where myenv is the name of the environment you wish to create**

#### Listing environments
conda env list

#### Activating Environment
conda activate myenv **where myenv is the name of the environment you wish to activate**

#### Deactivating an environment
conda deactivate

#### More information
For more information, please read: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment

### Virtual Environment

First make sure you have venv installed. If not, you can pip install it as follows: pip install venv

#### Creation
python3 -m venv /path/to/new/virtual/environment

#### Listing environments
*run* lsvirtualenv

You may need to install virutalenvwrapper to use this command. ( pip install virtualenvwrapper. ) If it doesn't populate to your path, check the package directory for the executable.

#### Activating Environment
source /path/to/venv/bin/activate

#### Deactivating an environment
*type* deactivate *in your shell*

## Matlab

🤷‍♂️

# Submodules
CNT_research_tools is a submodule of the CNT repository, where lab wide code should live.

epycom is a submodule of the following repository: https://gitlab.com/icrc-bme/epycom/-/tree/master/epycom

# License
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

# Contact Us
Any questions should be directed to the data science team. Contact information is provided below:

[Brian Prager](mailto:bjprager@seas.upenn.edu)

[Joshua Asuncion](mailto:asuncion@seas.upenn.edu)

