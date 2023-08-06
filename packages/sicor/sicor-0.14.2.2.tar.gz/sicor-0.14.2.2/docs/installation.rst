=====
Installation
=====

Sicor depends on some open source packages which are usually installed without problems by the automatic install
routine. However, for some projects, we strongly recommend resolving the dependency before the automatic installer
is run. This approach avoids problems with conflicting versions of the same software.
Using conda_, the recommended approach is:

 .. code-block:: bash

    # create virtual environment for sicor, this is optional
    conda create -y -q --name sicor python=3
    source activate sicor
    conda install -y -q -c conda-forge gdal pytables h5py llvmlite pyfftw scikit-learn

To install Sicor, clone the following repository and install sicor to your local python:

 .. code-block:: bash

    git clone https://gitext.gfz-potsdam.de/EnMAP/sicor.git
    cd sicor; make install



.. _conda: https://conda.io/docs/
.. _git-lfs: https://git-lfs.github.com/
