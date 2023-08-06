.. _cluster-creation:

=================
Creating clusters
=================

.. currentmodule:: coiled


Spinning up Dask clusters with Coiled is done by creating a :class:`coiled.Cluster` instance.
``coiled.Cluster`` objects manage a Dask cluster much like other cluster object you may
have seen before like :class:`distributed.LocalCluster` or :class:`dask_kubernetes.KubeCluster`.

Using a :ref:`cluster configuration <cluster-config>`, you can create a Dask cluster.
For example:

.. code-block:: python

    import coiled

    cluster = coiled.Cluster(n_workers=5, configuration="my-cluster-config")

will create a cluster with 5 workers, each with resources based on the cluster
configuration named "my-cluster-config". If no ``configuration=`` is specified,
then the "coiled/default" cluster configuration will be used.

.. note::

    Creating a cluster involves provisioning various resources on cloud-based
    infrastructure. This process takes about a minute in most cases.

Once a cluster has been created, you can connect Dask to the cluster by creating a
:class:`distributed.Client` instance:

.. code-block:: python

    from dask.distributed import Client

    client = Client(cluster)

To view the
`Dask diagnostic dashboard <https://docs.dask.org/en/latest/diagnostics-distributed.html>`_
for your cluster, navigate to the cluster's ``dashboard_link``:

.. code-block:: python

    cluster.dashboard_link

which should output an address along the lines of
``"https://ec2-...compute.amazonaws.com:8787/status"``.


Listing and deleting clusters
-----------------------------

The :meth:`coiled.list_clusters` method will list all active clusters:

.. code-block:: python

    coiled.list_clusters()

Note that when a cluster is created, by default, a unique name for the cluster
is automatically generated. You can provide your own cluster name using the
``name=`` keyword argument for ``coiled.Cluster``.

:meth:`coiled.delete_cluster` can be used to delete individual clusters.
For example:

.. code-block:: python

    coiled.delete_cluster(name="my-cluster")

deletes the cluster named "my-cluster".


Web interface
-------------

Coiled maintains a web interface where you can, among other things, view your recently created
Dask cluster along with other information like how many workers are in the cluster,
how much has running the cluster cost, etc. For more information, see https://beta.coiled.io/clusters.

.. figure:: images/clusters-table.png
