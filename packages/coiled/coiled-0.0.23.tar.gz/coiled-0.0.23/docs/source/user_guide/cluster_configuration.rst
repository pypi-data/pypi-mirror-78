.. _cluster-config:

======================
Cluster configurations
======================

.. currentmodule:: coiled


When creating Dask clusters, there are a variety of ways in which you can customize
the cluster. For example, you can specify the resources (i.e. CPU and memory) available to the
workers in your cluster, the software environment used throughout the cluster, whether
or not to make GPUs available, etc.

Coiled uses the concept of a **cluster configuration** which helps you specify the features
that define a Dask cluster.

It's important to note that creating a cluster configuration doesn't create a
cluster or provision any resources. You can think of a cluster configuration as
a template, or recipe, for a cluster that you can create later.


Creating cluster configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cluster configurations are created using the :meth:`coiled.create_cluster_configuration` function.
You must provide each cluster configuration you create with a name to identify the configuration,
along with a set of optional hardware and software parameters.

For example:

.. code-block:: python

    # Create a software environment named "my-conda-env"
    coiled.create_software_environment(
        name="my-conda-env", conda=["dask", "xarray==0.15.1", "numba"]
    )

    # Create a cluster configuration named "my-cluster-config"
    coiled.create_cluster_configuration(
        name="my-cluster-config",
        scheduler_cpu=2,
        scheduler_memory="8 GiB",
        worker_cpu=4,
        worker_memory="16 GiB",
        software="my-conda-env",
    )

creates a cluster configuration named "my-cluster-config" where the Dask scheduler
has 2 CPU / 8 GiB of memory, workers each have 4 CPUs / 16 GiB of memory, and
the "my-conda-env" software environment (also created in the above code snippet)
is used for the scheduler and all workers.

.. admonition:: Note
    :class: note

    Software environments used in cluster configurations must have ``distributed >= 2.23.0``
    installed as `Distributed <https://distributed.dask.org>`_ is required to
    launch Dask scheduler and worker processes.


Listing and deleting cluster configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In addition to creating cluster configurations, you can also use the
:meth:`coiled.list_cluster_configurations` function to list all available
cluster configurations:

.. code-block:: python

    coiled.list_cluster_configurations()

There is also a ``account=`` keyword argument which lets you specify the account which you
want to list cluster configurations for.

Similarly, the :meth:`coiled.delete_cluster_configuration` function can be used to delete
individual configurations. For example:

.. code-block:: python

    coiled.delete_cluster_configuration(name="alice/my-cluster-config")

deletes the cluster configuration named "my-cluster-config" in the Coiled account named "alice".
