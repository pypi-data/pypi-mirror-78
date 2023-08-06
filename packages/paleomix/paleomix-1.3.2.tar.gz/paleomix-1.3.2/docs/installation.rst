.. highlight:: Bash
.. _installation:


Installation
============

The following instructions will install PALEOMIX for the current user, but does not include specific programs required by the pipelines. For pipeline specific instructions, refer to the requirements sections for the :ref:`BAM <bam_requirements>`, the :ref:`Phylogentic <phylo_requirements>`, and the :ref:`Zonkey <zonkey_requirements>` pipeline.

The recommended way of installing PALEOMIX is by use of the `pip`_ package manager for Python 3. If `pip` is not installed, then please consult the documentation for your operating system. For Debian based operating systems, `pip` may be installed as follows::

    $ sudo apt-get install python3-pip

In addition, some libraries used by PALEOMIX may require additional development files, namely those for `zlib`, `libbz2`, `liblzma`, and for Python 3::

    $ sudo apt-get install libz-dev libbz2-dev liblzma-dev python3-dev

Once all requirements have been installed, PALEOMIX may be installed using `pip`:

.. parsed-literal::

    $ python3 -m pip install paleomix==\ |release|

To verify that the installation was carried out correctly, run the command `paleomix`:

.. parsed-literal::

    $ paleomix
    PALEOMIX - pipelines and tools for NGS data analyses
    Version: \ |release|

    ...

If you have not previously used pip, then you may need to add the pip `bin` folder to your `PATH` and restart your terminal before running the `paleomix` command::

    $ echo 'export PATH=~/.local/bin:$PATH' >> ~/.bashrc


Self-contained installation
---------------------------

The recommended method for installing PALEOMIX is using a virtual environment. Doing so
allows different versions of PALEOMIX to be installed simultaneously and ensures that PALEOMIX and its dependencies are not affected by the addition or removal of other python modules.

This installation method requires the `venv` module. On Debian based systems, this module must be installed separately::

    $ sudo apt-get install python3-venv

Once `venv` is installed, creation of a virtual environment and installation of PALEOMIX may be carried out as shown here:

.. parsed-literal::

    $ python3 -m venv venv
    $ source ./venv/bin/activate
    $ (venv) pip install paleomix==\ |release|
    $ (venv) deactivate

Following successful completion of these commands, the PALEOMIX tools will be accessible in the `./venv/bin/` folder. However, as this folder also contains a copy of Python itself, it is not recommended to add it to your `PATH`. Instead, simply link the `paleomix` commands to a folder in your `PATH`. This can be accomplished as follows::

    $ mkdir -p ~/.local/bin/
    $ ln -s ${PWD}/venv/bin/paleomix ~/.local/bin/

If ~/.local/bin is not already in your PATH, then it can be added as follows:

    $ echo 'export PATH=~/.local/bin:$PATH' >> ~/.bashrc


Upgrading an existing installation
----------------------------------

Upgrade an existing installation of PALEOMIX, installed using the methods described above, may also be accomplished using pip. To upgrade a regular installation, simply run `pip install` with the `--upgrade` option::

    $ pip install --upgrade paleomix

To upgrade an installation a self-contained installation, activate the environment before calling `pip`::

    $ source ./venv/bin/activate
    $ (paleomix) pip install --upgrade paleomix
    $ (paleomix) deactivate


Conda installation
-------------------

To have a completely contained environment that includes all software dependencies, you can create a `conda`_ environment.

To install `conda` and also set it up so it can use the `bioconda`_ bioinformatics tool repository, you can follow the instructions on the bioconda website `here`_.

Once set-up, you can create a conda environment named `paleomix` using the following commands:

.. parsed-literal::

    $ curl https://raw.githubusercontent.com/MikkelSchubert/paleomix/v\ |release|/paleomix_environment.yaml > paleomix_environment.yaml
    $ conda env create -n paleomix -f paleomix_environment.yaml

.. note::
    The above only installs the dependencies for the BAM pipeline.

You can now activate the paleomix environment with::

    $ conda activate paleomix

Next, install PALEOMIX in the activated environment using pip:

.. parsed-literal::

    $ (paleomix) pip install paleomix==\ |release|

PALEOMIX requires that the Picard JAR file can be found in a specific location, so we can symlink the versions in your conda environment into the correct place::

    $ (paleomix) mkdir -p ~/install/jar_root/
    $ (paleomix) ln -s ~/miniconda*/envs/paleomix/share/picard-*/picard.jar ~/install/jar_root/

.. note::
    If you installed miniconda in a different location, then you can obtain the location of the `paleomix` environment by running `conda env list`.

Once completed, you can test the environment works correctly using the pipeline test commands described in :ref:`examples`.

To deactivate the paleomix environment, simply run::

    $ conda deactivate

If you ever need to remove the entire environment, run the following command::

    $ conda env remove -n paleomix


.. _bioconda: https://bioconda.github.io
.. _conda: https://docs.conda.io/projects/conda/en/latest/index.html
.. _here: https://bioconda.github.io/user/install.html#install-conda
.. _pip: https://pip.pypa.io/en/stable/
.. _Pysam: https://github.com/pysam-developers/pysam/
.. _Python: http://www.python.org/
