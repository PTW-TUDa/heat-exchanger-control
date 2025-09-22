ETA General Python Project
==========================

This repository provides a basic setup for a Python project using Poetry, including GitLab CI/CD.
Suitable for most Python projects.
For experiments using ``eta-ctrl``, use the dedicated `ETA Experiment Template <https://git.ptw.maschinenbau.tu-darmstadt.de/eta-fabrik/templates/eta-experiment-project>`_ instead.

Usage guide
===========

1. **Copy** the template

  - Copy all files and directories from this template to your new project.

2. **Rename and Configure**:

  - Rename the `eta_general_python_project` directory to your actual project name.
  - Update pyproject.toml with your:

    - ``name``, ``version``, ``description``
    - ``authors``, ``keywords``, ``dependencies``
  
3. **Initialize** the environment:

  - If you haven't already installed Poetry, see their `installation docs <https://python-poetry.org/docs/#installation>`_

  - Sync dependencies::

        poetry sync

  - Install pre-commit hooks::

        poetry run pre-commit install

Recommended GitLab Configuration
================================

Naming convention
-----------------

GitLab Project Title (project name):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Use title case (capitalize words)
- Spaces are allowed
- Example: ``ETA General Python Project``

Python Package Slug (project slug):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Used for the repository URL and local directory name
- Use lowercase letters
- Use hyphens (-)
- Example: ``eta-general-python-project``

Python Package Directory (import name):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Used as the actual Python package folder name inside the repo
- Use lowercase letters
- Use underscores (_)
- Example: ``eta_general_python_project``

Project Information Naming Convention:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Option 1 - Thesis (Master/Bachelor/Student Project)**

  **Format**::

    StartYear.StartMonth-Type of Work (MT/BT/SA)-Student Name-Topic-Research Associate Initials

  **Description**:

  - **StartYear.StartMonth**: two-digit year and month of project start (e.g. ``16.01`` for January 2016)
  - **Type of Work (MT/BT/SA)**: type of work (``MT`` = Master Thesis, ``BT`` = Bachelor Thesis, ``SA`` = Student Project)
  - **Student Name**: surname of the student
  - **Topic**: short, descriptive project title
  - **Research Associate Initials**: initials of the supervising research associate

  **Example**::

    16.01-MT-Mustermann-Sample Thesis Machine Tool Optimisation-XY

  ---

- **Option 2 - Project Assignment According to Proposal Structure**

  **Format**::

    Consortium Project Acronym-Work Package Number-Title of the Work Package

  **Description**:

  - **Consortium Project Acronym**: e.g. ``SynErgie``
  - **Work Package Number**: official work package ID from the proposal (e.g. ``MS III.2.9.4``)
  - **Title of the Work Package**: descriptive title according to the proposal

  **Example**::

    SynErgie-MS III.2.9.4-Produktionsanlagen flexibilisiert und Methodik für Anlagenpools erweitert



Settings
----------

Branch Management
~~~~~~~~~~~~~~~~~~
- **Default Branch**: Set ``development`` as the default branch
  *(Repository -> Branch defaults)*
- **Protected Branches**:
  - Protect both ``development`` and ``main``
  - Restrict write access to **Maintainers**
  *(Repository -> Protected branches)*
- **Protected Tags**:
  - Add wildcard pattern ``v*`` (for version tags)
  - Restrict creation to **Maintainers**
  *(Repository -> Protected tags)*

Merge Request Settings
~~~~~~~~~~~~~~~~~~~~~~~
- **Squash Commits**: Set to *"Encourage"*
  *(Merge Requests -> Squash commits option)*
- **Merge Checks**:
  - Require *"Pipelines must succeed"* before merging
  *(Merge Requests -> Merge checks)*

Pipeline Configuration
~~~~~~~~~~~~~~~~~~~~~~~
- Disable *"Public pipelines"* to restrict pipeline visibility
  *(CI/CD -> General Pipelines)*



GitLab CI/CD
==============

Additional Tools
-----------------
These tools are used to improve code quality. They are run in pipelines and also in pre-commit.

- **ruff**: Improves the code quality by linting and formatting it
- **codespell**: Checks for spelling mistakes (english only)
- **mypy**: Static type checking

Pipelines (CI)
---------------
The pipeline consists of four stages:

1. **setup**: Dependency caching for Poetry and pip
2. **check**: Static analysis and linting
3. **test**: Test the code using pytest
4. **deploy**: Publish Python package to the local GitLab registry

It automatically runs on:

- New commits in Merge Requests
- Push to the default branch
- Tag creation

The **deploy** stage is only run when a version tag is created.

Each job specified in ``.gitlab-ci.yml`` will run and show whether it was successful or not.
Merge Requests will be unable to merge until the pipeline passes.
Every job is optional, but recommended.


Deployment (CD)
----------------
All deployments originate from the ``main`` branch.
Ensure the version number in ``pyproject.toml`` is updated.
Packages are automatically published to GitLab's Package Registry when a new version tag is pushed.
Version tags **must** follow semantic versioning: `vX.Y.Z`, e.g. `v1.0.0`.
They can be created in the GitLab web interface or via terminal::

    git switch main
    git pull
    git tag -a v1.0.0 -m "Release version 1.0.0"
    git push origin v1.0.0
