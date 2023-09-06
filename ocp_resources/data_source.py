from kubernetes.dynamic.exceptions import ResourceNotFoundError

from ocp_resources.persistent_volume_claim import PersistentVolumeClaim
from ocp_resources.resource import NamespacedResource


class DataSource(NamespacedResource):
    """
    https://kubevirt.io/cdi-api-reference/main/definitions.html#_v1beta1_datasource
    """

    api_group = NamespacedResource.ApiGroup.CDI_KUBEVIRT_IO

    def __init__(
        self,
        source=None,
        **kwargs,
    ):
        """
        Args:
            source (object): Source is the current source of the data referenced by the DataSource object.
            For more information on DataSourceSource on kubevirt API:
                https://kubevirt.io/cdi-api-reference/main/definitions.html#_v1beta1_datasourcesource
        """
        super().__init__(**kwargs)
        self.source = source

    def to_dict(self):
        super().to_dict()
        if not self.yaml_file:
            self.res.update(
                {
                    "spec": {
                        "source": self.source,
                    },
                }
            )

    @property
    def pvc(self):
        data_source_pvc = self.instance.spec.source.pvc
        pvc_name = data_source_pvc.name
        pvc_namespace = data_source_pvc.namespace
        try:
            return PersistentVolumeClaim(
                client=self.client,
                name=pvc_name,
                namespace=pvc_namespace,
            )
        except ResourceNotFoundError:
            self.logger.warning(
                f"dataSource {self.name} is pointing to a non-existing PVC, name:"
                f" {pvc_name}, namespace: {pvc_namespace}"
            )
