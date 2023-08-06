:notoc:

=============
Dask Clusters
=============

Coiled manages Dask clusters.  It manages cloud resources, networking, software
environments, and everything you need to scale Python in the cloud robustly and
easily.

.. currentmodule:: coiled

.. toctree::
   :maxdepth: 1
   :hidden:

   cluster_configuration
   cluster_creation

Simple Example
--------------

The main entry point to launch a Coiled cluster is the ``coiled`` Python API.
In the simplest case you can run the following from anywhere that
you can run Python.

.. code-block:: python

   import coiled

   cluster = coiled.Cluster()

And then you can connect to that cluster with Dask

.. code-block:: python

   from dask.distributed import Client

   client = Client(cluster)


Configuration
-------------

In full generality though there are many parameters that we may want to control:

-  The software used in each worker (see :doc:`software_environment`)
-  The amount of RAM and number of CPUs in each worker, and whether or not to use GPUs (see :doc:`cluster_configuration`)
-  The number of workers to use (see the ``Cluster.scale`` method)

These are included in this longer example:

.. code-block:: python

    import coiled

    # Create a new software environment with the libraries you want
    coiled.create_software_environment(
        name="my-conda-env", conda=["dask", "xarray==0.15.1", "numba"]
    )

    # Control the resources of your cluster by creating a new cluster configuration
    coiled.create_cluster_configuration(
        name="my-cluster-config",
        worker_memory="16 GiB",
        worker_cpu=4,
        scheduler_memory="4 GiB",
        scheduler_cpu=1,
        software="my-conda-env",
    )

    # Spin up a Dask cluster using Coiled
    cluster = coiled.Cluster(n_workers=5, configuration="my-cluster-config")

    # Connect Dask to that cluster
    from dask.distributed import Client

    client = Client(cluster)

Learn more
----------

In the next sections we'll learn more about how to configure and launch Dask
clusters.

.. toctree::
   :maxdepth: 1

   cluster_configuration
   cluster_creation
