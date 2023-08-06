.. _creating-software-environments:

==============================
Creating software environments
==============================

.. currentmodule:: coiled

Creating software environments with Coiled is handled by a single :meth:`coiled.create_software_environment`
function. You must provide each software environment you create with a name to identify the environment,
the set of packages you want installed into the environment, and (optionally) any additional setup steps
that you want to run. Coiled will then build a software environment for you which can be used locally or
remotely on a Dask cluster.

.. _software-specifications:

Software specifications
-----------------------

You can specify how to build a Coiled software environment in a variety of ways: using conda, pip, and/or
Docker images.

Conda
^^^^^

To create a software environment with conda packages installed, use the ``conda=`` keyword
argument of ``coiled.create_software_environment``. The input to ``conda=`` can be formatted in three
different ways. First you can provide a list of packages to be install into the environment. For example:

.. code-block:: python

    coiled.create_software_environment(
        name="my-conda-env", conda=["dask", "xarray==0.15.1", "numba"],
    )

will build a software environment named "my-conda-env" and use conda to
install dask, version 0.15.1 of xarray, and numba from the ``defaults`` conda
channel.

Additionally, more complex package specifications, like installing packages from
additional conda channels, are supported by passing a dictionary to ``conda=``.
For example:

.. code-block::

    coiled.create_software_environment(
        name="my-conda-env",
        conda={"channels": ["conda-forge", "defaults"],
               "dependencies": ["dask", "xarray=0.15.1", "numba"]},
    )

will search for packages in both the ``conda-forge`` and ``defaults`` channels. Equivalently,
you can also provide an input conda environment YAML file:

.. code-block:: python

    coiled.create_software_environment(
        name="my-conda-env", conda="environment.yml",
    )

where ``environment.yml`` is a local file with the following content:

.. code-block:: yaml

    # environment.yml
    channels:
      - conda-forge
      - defaults
    dependencies:
      - dask
      - xarray=0.15.1
      - numba


Pip
^^^

To create a software environment with pip packages installed, use the ``pip=`` keyword
argument of ``coiled.create_software_environment``. The input to ``pip=`` can be formatted in two
different ways: a list of packages (on `PyPI <https://pypi.org/>`_) to install or a pip requirements file.

For example:

.. code-block:: python

    coiled.create_software_environment(
        name="my-pip-env", pip=["dask", "xarray==0.15.1", "numba"],
    )

will build a software environment named "my-pip-env" and use pip to install dask, version 0.15.1 of xarray,
and numba.

Equivalently, you may specify a pip requirements file:

.. code-block:: python

    coiled.create_software_environment(
        name="my-pip-env", pip="requirements.txt",
    )

where ``requirements.txt`` is a local file with the following content:

.. code-block::

    # requirements.txt
    dask
    xarray==0.15.1
    numba


Docker
^^^^^^

Any Docker image on `Docker Hub <https://hub.docker.com/>`_ can be used to
build a custom software environment for your cluster by using the ``container=``
keyword argument of of :meth:`coiled.create_software_environment`.
For example:

.. code-block::

    coiled.create_software_environment(
        name="my-docker-env",
        container="rapidsai/rapidsai:latest",
    )

will build a software environment named "my-docker-env" using latest
RAPIDS Docker image.


Post build commands
-------------------

Sometimes installing packages with pip and conda isn't enough to fully set up the software
environment you want. For example, JupyterLab extensions require additional command(s) to be
run as part of their installation. To support these use cases, ``coiled.create_software_environment``
has a ``post_build=`` keyword argument for running a series of commands after conda and pip
packages have been installed.

For example, the following creates a software environment with conda packages for Dask, JupyterLab,
Node.js, and the `Dask JupyterLab extension <https://github.com/dask/dask-labextension>`_ installed,
then runs two additional commands to complete the JupyterLab extension installation:

.. code-block::

    coiled.create_software_environment(
        name="my-jupyterlab-env",
        conda=["dask", "jupyterlab", "nodejs", "dask-labextension"],
        post_build=["jupyter labextension install dask-labextension",
                    "jupyter serverextension enable dask_labextension"],
    )

Note that if the input to ``post_build`` is a list of commands, then they are assumed to be run as
part of a bash script. If this is not the case, you may also pass an executable file to ``post_build``
with a non-bash shebang line (e.g. ``#!/bin/zsh``).


Composing software specifications
---------------------------------

As discussed in the :ref:`software-specifications` section, you can use conda, pip, and Docker images
together to construct a software environment. However, there are some assumptions that are made during
the build process, in particular when using a custom Docker image, that are important to know about.

Conda and pip packages are installed in a fairly straightforward way. First, if any conda packages are
specified, they are installed into a conda environment. The name of the conda environment can be specified
using the ``conda_env_name=`` keyword argument of ``coiled.create_software_environment`` (defaults to ``"base"``),
though this is only primarily needed when using a custom Docker image for the software environment.

Next, if any pip packages are specified, they are pip installed. If any conda packages were installed, then
pip packages will also be installed into the same conda environment -- otherwise they will be installed using
the current system-wide Python.

Finally, when using a custom Docker image as a base for the software environment, conda must be installed,
and on the current ``PATH``, in order to install conda packages. Likewise, pip must be installed, and on the current
``PATH``, for pip packages to be installed. If your Docker image uses a conda environment not named ``"base"``,
then you must pass the name of the conda environment to the ``conda_env_name=`` keyword for ``coiled.create_software_environment``.
