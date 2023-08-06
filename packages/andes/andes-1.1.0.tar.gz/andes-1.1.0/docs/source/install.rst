.. _install:

*************************
Installation
*************************

ANDES can be installed in Python 3.6+.

Environment
===========

Setting Up Miniconda
--------------------
We recommend the Miniconda distribution that includes the conda package manager and Python.
Downloaded and install the latest Miniconda (x64, with Python 3)
from https://conda.io/miniconda.html.

Step 1: Open terminal (for Linux or maxOS) or `Anaconda Prompt` (for Windows, not the `cmd`
program).
Create a conda environment for ANDES (recommended)

.. code:: bash

     conda create --name andes python=3.7

Activate the new environment with

.. code:: bash

     conda activate andes

Environment activation needs to be executed every time a new Anaconda Prompt or shell is open.

Step 2: Add the ``conda-forge`` channel and set it as default

.. code:: bash

     conda config --add channels conda-forge
     conda config --set channel_priority flexible

Existing Python Environment (Advanced)
--------------------------------------
This is for advanced user only and is not recommended on Microsoft Windows.
Please skip it if you have set up a Conda environment.

Instead of using Conda, if you prefer an existing Python environment,
you can install ANDES with `pip`:

.. code:: bash

      python3 -m pip install andes

If you see a `Permission denied` error, you will need to
install the packages locally with `--user`

Install ANDES
=============

ANDES can be installed in the user mode and the development mode.

User Mode
---------
If you want to use ANDES without modifying the source code, you can install it in the user mode.

In the Anaconda environment, run

.. code:: bash

    conda install andes


Developer Mode (Recommended)
----------------------------
If you want to hack into the code and, for example, develop new models or routines, please install it in the
development mode (recommended). The development mode has the same usage as the user mode.
In addition, changes to the source code will be reflected immediately without having to re-install the package.

Step 1: Get ANDES source code

As a developer, you are strongly encouraged to clone the source code using ``git``
from either your fork or the original repository:

.. code:: bash

    git clone https://github.com/cuihantao/andes

In this way, you can easily update to the latest source code using ``git``.

Alternatively, you can download the ANDES source code from
https://github.com/cuihantao/andes and extract all files to the path of your choice.
Although this will work, we don't recommend this method, since it is cumbersome
to update the source code and push back changes.

Step 2: Install dependencies

In the Anaconda environment, use ``cd`` to change directory to the ANDES root folder.

Install dependencies with

.. code:: bash

    conda install --file requirements.txt
    conda install --file requirements-dev.txt

Step 3: Install ANDES in the development mode using

.. code:: bash

      python3 -m pip install -e .

Note the dot at the end. Pip will take care of the rest.

Update ANDES
============

Regular ANDES updates will be pushed to both ``conda-forge`` and Python package index.
It is recommended to use the latest version for bug fixes and new features.
We also recommended you to check the :ref:`ReleaseNotes` before updating to stay informed
of changes that might break your downstream code.

Depending you how you installed ANDES, you will use one of the following ways to upgrade.

If you installed it from conda (most common for users), run

.. code:: bash

    conda install -c conda-forge --yes andes

If you install it from PyPI (namely, through ``pip``), run

.. code:: bash

    python3 -m pip install --yes andes

If you installed ANDES from source code, and the source was cloned using ``git``,
you can use ``git pull`` to pull in changes from remote. However, if your source
code was downloaded, you will have to download the new source code again and manually
overwrite the existing one.

In rare cases, after updating the source code, command-line ``andes`` will complain
about missing dependency. If this ever happens, it means the new ANDES has introduced
new dependencies. In such cases, reinstall andes in the development mode to fix.
Change directory to the ANDES source code folder that contains ``setup.py`` and run

.. code:: bash

    python3 -m pip install -e .

Troubleshooting
===============

- ImportError: DLL load failed: The specified module could not be found.

This usually happens when andes is not installed in a Conda environment
but instead in a system-wide Python whose library path was not correctly
set in environment variables.

The easiest fix is to install andes in a Conda environment.

Performance Packages (Advanced)
===============================
The following two forks of ``cvxopt``, ``cvxoptklu``, ``cvxopt`` with ``spmatrix.ipadd``
are optional but can significantly boost the performance of ANDES.
**Installation requires a C compiler**, ``openblas`` and ``SuiteSparse`` libraries.

.. note::

    Performance packages can be safely skipped and will not affect the
    functionality of ANDES.

.. warning::

    We have not tried to compile either package on Windows.
    Refer to the CVXOPT installation instructions for Windows at
    http://cvxopt.org/install/index.html#windows

cxvoptklu
---------
``cvxoptklu`` is a fork of the CVXOPT with KLU by Uriel Sandoval (@sanurielf).
In addition to UMFPACK, ``cvxoptklu`` interfaces ``cvxopt`` to KLU, which is
roughly 20% faster than UMFPACK for circuit simulation based on our testing.

To install ``cvxoptklu``, on Debian GNU/Linux, one can do

.. code:: bash

      sudo apt install libopenblas-dev libsuitesparse-dev
      pip install cvxoptklu

On macOS, one can install with homebrew using

.. code:: bash

    brew install openblas suitesparse
    pip install cvxoptklu

To install from source code, use the repository at
https://github.com/cuihantao/cvxoptklu.

CVXOPT with ipadd
-----------------
To install our fork of ``cvxopt`` with ``spmatrix.ipadd``, one need to clone the
repository and compile from source.

.. code:: bash

    git clone https://github.com/curent/cvxopt
    cd cvxopt
    python setup.py build

The compilation may display some warnings, but make sure there is no error.
Then, install it with

.. code:: bash

    python setup.py install
