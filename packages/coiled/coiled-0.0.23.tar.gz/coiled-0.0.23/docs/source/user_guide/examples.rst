.. _examples:

========
Examples
========

The Coiled community maintains a `Coiled Examples GitHub repository <https://github.com/coiled/coiled-examples/>`_
containing several easy-to-run Jupyter notebooks which illustrate how Dask and Coiled scale
data- and compute-intensive workloads.

Setup
-----

Each example notebook can be run locally by first downloading a local copy of the ``coiled-examples``
repository. For example, using ``git clone``:

.. code-block:: bash

    $ git clone https://github.com/coiled/coiled-examples.git
    $ cd coiled-examples

Each notebook has a :ref:`software environment <software-envs>` containing the libraries needed to run
the notebook which can be installed locally using ``coiled install``. The :ref:`next section <example-notebooks>`
lists the software environment used for each example notebook.

For example, the software environment used by the
`Scaling XGBoost with Dask and Coiled <https://github.com/coiled/coiled-examples/blob/master/scaling-xgboost/scaling-xgboost.ipynb>`_
notebook can be installed locally and activated with:

.. code-block:: bash

    # Install coiled-examples/xgboost locally
    $ coiled install coiled-examples/xgboost
    # Activate the environment
    $ conda activate coiled-coiled-examples-xgboost
    # Install JupyterLab
    $ conda install jupyterlab


.. admonition:: Tip
    :class: tip

    Check out our :ref:`configuring JupyterLab docs <jupyterlab-guide>` for instructions on how to
    set up JupyterLab extensions that works well with Dask and Coiled.

Finally you can launch the example notebook you would like to run in JupyterLab. Again, using the XGBoost notebook
as an example:

.. code-block:: bash

    # Launch an example notebook in JupyterLab
    $ jupyter lab scaling-xgboost/scaling-xgboost.ipynb


.. _example-notebooks:

Example notebooks
-----------------

Machine Learning
""""""""""""""""

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Notebook
     - Install software environment
   * - `Scaling XGBoost with Dask and Coiled <https://github.com/coiled/coiled-examples/blob/master/scaling-xgboost/scaling-xgboost.ipynb>`_
     - ``coiled install coiled-examples/xgboost``
   * - `Hyperparameter Optimization with Dask and Coiled <https://github.com/coiled/coiled-examples/blob/master/hyper-parameter-optimmization/hyper-parameter-optimization.ipynb>`_
     - ``coiled install coiled-examples/pytorch``

Geoscience
""""""""""

.. list-table::
   :widths: 50 50
   :header-rows: 1

   * - Notebook
     - Install software environment
   * - `Analyzing MUR SST with Coiled <https://github.com/coiled/coiled-examples/blob/master/pangeo/murs_sst.ipynb>`_
     - ``coiled install coiled-examples/pangeo``
   * - `Analyzing Landsat-8 data with Coiled <https://github.com/coiled/coiled-examples/blob/master/pangeo/landsat8.ipynb>`_
     - ``coiled install coiled-examples/pangeo``
