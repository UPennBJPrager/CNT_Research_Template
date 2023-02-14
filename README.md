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

## Python
For python packages, python wheels and tarballs can be found in: CNT_Development/core_libraries/python/.

To install, run:

pip install foo.whl

**or**

pip install foo.tar.gz

where foo is the name of the library of interest.

## Matlab

:man_shrugging:

# Documentation
This template is intended to be used as both an environment and a simple wrapper for research code. Before beginning, we highly recommend that a virtual environment is made for each project to ensure dependencies are properly referenced and code can be reproduced across numerous systems. Examples for creating virtual environments is provided below.

# Virtual Environments

## Python

### Conda

#### Creation
conda create --name myenv **where myenv is the name of the environment you wish to create**

#### Listing environments
conda env list

#### Activating Environment
conda activate myenv **where myenv is the name of the environment you wish to create**

#### Deactivating an environment
conda deactivate

#### More information
For more information, please read: https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#activating-an-environment

### Virtual Environment

virtualenv

# Submodules
CNT_research_tools is a submodule of the CNT repository, where lab wide code should live.

epycom is a submodule of the following repository: https://gitlab.com/icrc-bme/epycom/-/tree/master/epycom
