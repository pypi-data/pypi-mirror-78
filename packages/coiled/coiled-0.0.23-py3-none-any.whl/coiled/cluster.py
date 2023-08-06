from typing import Tuple, List, Dict
import asyncio
import aiobotocore
import sys
import uuid

import dask.distributed
import distributed.deploy

from .core import Cloud
from .utils import parse_identifier


class Cluster(distributed.deploy.Cluster):
    """ Create a Dask cluster with Coiled

    Parameters
    ----------
    n_workers
        Number of workers in this cluster. Defaults to 4.
    configuration
        Name of cluster configuration to create cluster from.
        If not specified, defaults to ``coiled/default`` for the
        current Python version.
    name
        Name to use for identifying this cluster. Defaults to ``None``.
    asynchronous
        Set to True if using this Cloud within ``async``/``await`` functions or
        within Tornado ``gen.coroutines``. Otherwise this should remain
        ``False`` for normal use. Default is ``False``.
    cloud
        Cloud object to use for interacting with Coiled.
    account
        Name of Coiled account to use. If not provided, will
        default to the user account for the ``cloud`` object being used.
    shutdown_on_close
        Whether or not to shut down the cluster when it finishes.
        Defaults to True, unless name points to an existing cluster.
    region
        Name of the AWS region to create the cluster in (e.g. "us-east-2").
        If not specified, will check the ``coiled.aws.region``
        configuration value.
    """

    def __init__(
        self,
        n_workers: int = 4,
        configuration: str = None,
        name: str = None,
        asynchronous: bool = False,
        cloud: Cloud = None,
        account: str = None,
        shutdown_on_close=None,
        region: str = None,
    ):
        # we really need to call this first before any of the below code errors
        # out; otherwise because of the fact that this object inherits from
        # deploy.Cloud __del__ (and perhaps __repr__) will have AttributeErrors
        # because the gc will run and attributes like `.status` and
        # `.scheduler_comm` will not have been assigned to the object's instance
        # yet
        super().__init__(asynchronous=asynchronous)

        self.cloud = cloud or Cloud.current(asynchronous=asynchronous)
        self.configuration = configuration
        if self.configuration is None:
            v = "".join(map(str, sys.version_info[:2]))
            self.configuration = f"coiled/default-py{v}"
        self.name = name
        self.account = account
        self._start_n_workers = n_workers
        self._lock = asyncio.Lock(loop=self.loop)
        self._asynchronous = asynchronous
        self.shutdown_on_close = shutdown_on_close
        self.region = region
        self.cluster_id = None

        self._name = "coiled.Cluster"  # Used in Dask's Cluster._ipython_display_

        if not self.asynchronous:
            self.sync(self._start)

    @property
    def loop(self):
        return self.cloud.loop

    async def _start(self):
        self.cloud = await self.cloud
        should_create = True

        if self.name:
            self.cluster_id = await self.cloud._get_cluster_by_name(
                name=self.name, account=self.account, region=self.region
            )
            if self.cluster_id:
                print(f"Using existing cluster: {self.name}")  # TODO: add timer
                should_create = False
                if self.shutdown_on_close is None:
                    self.shutdown_on_close = False

        self.name = self.name or self.cloud.user + "-" + str(uuid.uuid4())[:10]

        if should_create:
            # TODO: should this check also be upstream on the server?
            acct, name = parse_identifier(self.configuration, "configuration")  # type: ignore
            available_configs = await self.cloud.list_cluster_configurations(  # type: ignore
                account=acct or self.account
            )
            if name not in available_configs:
                error_msg = f"Cluster configuration '{self.configuration}' not found."
                if name in await self.cloud.list_software_environments():  # type: ignore
                    error_msg += (
                        "\n"
                        f"We did find a software environment '{self.configuration}'.\n"
                        "You may need to make a cluster configuration with this \n"
                        "software environment:\n\n"
                        f"  coiled.create_cluster_configuration(name='{self.configuration}', software='{self.configuration}')"  # noqa: E501
                    )
                raise ValueError(error_msg)

            self.cluster_id = await self.cloud.create_cluster(
                account=self.account,
                configuration=self.configuration,  # type: ignore
                name=self.name,
                workers=self._start_n_workers,
                region=self.region,
            )

            if self._start_n_workers:
                await self._scale(self._start_n_workers)

        self.security, info = await self.cloud.security(
            cluster_id=self.cluster_id, account=self.account  # type: ignore
        )

        self.scheduler_comm = dask.distributed.rpc(
            info["public_address"],
            connection_args=self.security.get_connection_args("client"),
        )

        async with aiobotocore.get_session().create_client("sts") as sts:
            try:
                credentials = await sts.get_session_token()
                credentials = credentials["Credentials"]
                # TODO: set up TTL, and update these credentials periodically

                await self.scheduler_comm.aws_update_credentials(
                    credentials={
                        k: credentials[k]
                        for k in ["AccessKeyId", "SecretAccessKey", "SessionToken"]
                    }
                )
            except Exception:
                pass

        await super()._start()

    def __await__(self):
        async def _():
            async with self._lock:
                if self.status == "created":
                    await self._start()
                assert self.status == "running"
            return self

        return _().__await__()

    async def _close(self):
        if self.shutdown_on_close in (True, None):
            await self.cloud.delete_cluster(
                account=self.account, cluster_id=self.cluster_id,  # type: ignore
            )
        await super()._close()

    async def _scale(self, n: int) -> Tuple[List[Dict], List[Dict]]:
        return await self.cloud.scale(account=self.account, cluster_id=self.cluster_id, n=n)  # type: ignore

    def scale(self, n: int) -> Tuple[List[Dict], List[Dict]]:
        """ Scale cluster to ``n`` workers

        Parameters
        ----------
        n
            Number of workers to scale cluster size to.
        """
        return self.sync(self._scale, n=n)

    def __enter__(self):
        return self.sync(self.__aenter__)

    def __exit__(self, *args, **kwargs):
        return self.sync(self.__aexit__, *args, **kwargs)

    def get_logs(self, scheduler: bool = True, workers: bool = True) -> dict:
        """ Return logs for the scheduler and workers
        Parameters
        ----------
        scheduler : boolean
            Whether or not to collect logs for the scheduler
        workers : boolean
            Whether or not to collect logs for the workers
        Returns
        -------
        logs: Dict[str]
            A dictionary of logs, with one item for the scheduler and one for
            the workers
        """
        return self.sync(self._get_logs, scheduler=scheduler, workers=workers)

    async def _get_logs(self, scheduler: bool = True, workers: bool = True) -> dict:
        return await self.cloud.logs(
            account=self.account, cluster_id=self.cluster_id, scheduler=scheduler, workers=workers  # type: ignore
        )
