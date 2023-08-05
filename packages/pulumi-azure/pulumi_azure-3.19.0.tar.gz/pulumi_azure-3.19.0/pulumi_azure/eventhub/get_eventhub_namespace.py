# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'GetEventhubNamespaceResult',
    'AwaitableGetEventhubNamespaceResult',
    'get_eventhub_namespace',
]

warnings.warn("azure.eventhub.getEventhubNamespace has been deprecated in favor of azure.eventhub.getNamespace", DeprecationWarning)

@pulumi.output_type
class GetEventhubNamespaceResult:
    """
    A collection of values returned by getEventhubNamespace.
    """
    def __init__(__self__, auto_inflate_enabled=None, capacity=None, dedicated_cluster_id=None, default_primary_connection_string=None, default_primary_connection_string_alias=None, default_primary_key=None, default_secondary_connection_string=None, default_secondary_connection_string_alias=None, default_secondary_key=None, id=None, kafka_enabled=None, location=None, maximum_throughput_units=None, name=None, resource_group_name=None, sku=None, tags=None, zone_redundant=None):
        if auto_inflate_enabled and not isinstance(auto_inflate_enabled, bool):
            raise TypeError("Expected argument 'auto_inflate_enabled' to be a bool")
        pulumi.set(__self__, "auto_inflate_enabled", auto_inflate_enabled)
        if capacity and not isinstance(capacity, float):
            raise TypeError("Expected argument 'capacity' to be a float")
        pulumi.set(__self__, "capacity", capacity)
        if dedicated_cluster_id and not isinstance(dedicated_cluster_id, str):
            raise TypeError("Expected argument 'dedicated_cluster_id' to be a str")
        pulumi.set(__self__, "dedicated_cluster_id", dedicated_cluster_id)
        if default_primary_connection_string and not isinstance(default_primary_connection_string, str):
            raise TypeError("Expected argument 'default_primary_connection_string' to be a str")
        pulumi.set(__self__, "default_primary_connection_string", default_primary_connection_string)
        if default_primary_connection_string_alias and not isinstance(default_primary_connection_string_alias, str):
            raise TypeError("Expected argument 'default_primary_connection_string_alias' to be a str")
        pulumi.set(__self__, "default_primary_connection_string_alias", default_primary_connection_string_alias)
        if default_primary_key and not isinstance(default_primary_key, str):
            raise TypeError("Expected argument 'default_primary_key' to be a str")
        pulumi.set(__self__, "default_primary_key", default_primary_key)
        if default_secondary_connection_string and not isinstance(default_secondary_connection_string, str):
            raise TypeError("Expected argument 'default_secondary_connection_string' to be a str")
        pulumi.set(__self__, "default_secondary_connection_string", default_secondary_connection_string)
        if default_secondary_connection_string_alias and not isinstance(default_secondary_connection_string_alias, str):
            raise TypeError("Expected argument 'default_secondary_connection_string_alias' to be a str")
        pulumi.set(__self__, "default_secondary_connection_string_alias", default_secondary_connection_string_alias)
        if default_secondary_key and not isinstance(default_secondary_key, str):
            raise TypeError("Expected argument 'default_secondary_key' to be a str")
        pulumi.set(__self__, "default_secondary_key", default_secondary_key)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kafka_enabled and not isinstance(kafka_enabled, bool):
            raise TypeError("Expected argument 'kafka_enabled' to be a bool")
        pulumi.set(__self__, "kafka_enabled", kafka_enabled)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
        if maximum_throughput_units and not isinstance(maximum_throughput_units, float):
            raise TypeError("Expected argument 'maximum_throughput_units' to be a float")
        pulumi.set(__self__, "maximum_throughput_units", maximum_throughput_units)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if sku and not isinstance(sku, str):
            raise TypeError("Expected argument 'sku' to be a str")
        pulumi.set(__self__, "sku", sku)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if zone_redundant and not isinstance(zone_redundant, bool):
            raise TypeError("Expected argument 'zone_redundant' to be a bool")
        pulumi.set(__self__, "zone_redundant", zone_redundant)

    @property
    @pulumi.getter(name="autoInflateEnabled")
    def auto_inflate_enabled(self) -> bool:
        """
        Is Auto Inflate enabled for the EventHub Namespace?
        """
        return pulumi.get(self, "auto_inflate_enabled")

    @property
    @pulumi.getter
    def capacity(self) -> float:
        """
        The Capacity / Throughput Units for a `Standard` SKU namespace.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter(name="dedicatedClusterId")
    def dedicated_cluster_id(self) -> str:
        """
        The ID of the EventHub Dedicated Cluster where this Namespace exists.
        """
        return pulumi.get(self, "dedicated_cluster_id")

    @property
    @pulumi.getter(name="defaultPrimaryConnectionString")
    def default_primary_connection_string(self) -> str:
        """
        The primary connection string for the authorization
        rule `RootManageSharedAccessKey`.
        """
        return pulumi.get(self, "default_primary_connection_string")

    @property
    @pulumi.getter(name="defaultPrimaryConnectionStringAlias")
    def default_primary_connection_string_alias(self) -> str:
        """
        The alias of the primary connection string for the authorization
        rule `RootManageSharedAccessKey`.
        """
        return pulumi.get(self, "default_primary_connection_string_alias")

    @property
    @pulumi.getter(name="defaultPrimaryKey")
    def default_primary_key(self) -> str:
        """
        The primary access key for the authorization rule `RootManageSharedAccessKey`.
        """
        return pulumi.get(self, "default_primary_key")

    @property
    @pulumi.getter(name="defaultSecondaryConnectionString")
    def default_secondary_connection_string(self) -> str:
        """
        The secondary connection string for the
        authorization rule `RootManageSharedAccessKey`.
        """
        return pulumi.get(self, "default_secondary_connection_string")

    @property
    @pulumi.getter(name="defaultSecondaryConnectionStringAlias")
    def default_secondary_connection_string_alias(self) -> str:
        """
        The alias of the secondary connection string for the
        authorization rule `RootManageSharedAccessKey`.
        """
        return pulumi.get(self, "default_secondary_connection_string_alias")

    @property
    @pulumi.getter(name="defaultSecondaryKey")
    def default_secondary_key(self) -> str:
        """
        The secondary access key for the authorization rule `RootManageSharedAccessKey`.
        """
        return pulumi.get(self, "default_secondary_key")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="kafkaEnabled")
    def kafka_enabled(self) -> bool:
        return pulumi.get(self, "kafka_enabled")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The Azure location where the EventHub Namespace exists
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter(name="maximumThroughputUnits")
    def maximum_throughput_units(self) -> float:
        """
        Specifies the maximum number of throughput units when Auto Inflate is Enabled.
        """
        return pulumi.get(self, "maximum_throughput_units")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def sku(self) -> str:
        """
        Defines which tier to use.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags to assign to the EventHub Namespace.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="zoneRedundant")
    def zone_redundant(self) -> bool:
        """
        Is this EventHub Namespace deployed across Availability Zones?
        """
        return pulumi.get(self, "zone_redundant")


class AwaitableGetEventhubNamespaceResult(GetEventhubNamespaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEventhubNamespaceResult(
            auto_inflate_enabled=self.auto_inflate_enabled,
            capacity=self.capacity,
            dedicated_cluster_id=self.dedicated_cluster_id,
            default_primary_connection_string=self.default_primary_connection_string,
            default_primary_connection_string_alias=self.default_primary_connection_string_alias,
            default_primary_key=self.default_primary_key,
            default_secondary_connection_string=self.default_secondary_connection_string,
            default_secondary_connection_string_alias=self.default_secondary_connection_string_alias,
            default_secondary_key=self.default_secondary_key,
            id=self.id,
            kafka_enabled=self.kafka_enabled,
            location=self.location,
            maximum_throughput_units=self.maximum_throughput_units,
            name=self.name,
            resource_group_name=self.resource_group_name,
            sku=self.sku,
            tags=self.tags,
            zone_redundant=self.zone_redundant)


def get_eventhub_namespace(name: Optional[str] = None,
                           resource_group_name: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEventhubNamespaceResult:
    """
    Use this data source to access information about an existing EventHub Namespace.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.eventhub.get_namespace(name="search-eventhubns",
        resource_group_name="search-service")
    pulumi.export("eventhubNamespaceId", example.id)
    ```


    :param str name: The name of the EventHub Namespace.
    :param str resource_group_name: The Name of the Resource Group where the EventHub Namespace exists.
    """
    pulumi.log.warn("get_eventhub_namespace is deprecated: azure.eventhub.getEventhubNamespace has been deprecated in favor of azure.eventhub.getNamespace")
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:eventhub/getEventhubNamespace:getEventhubNamespace', __args__, opts=opts, typ=GetEventhubNamespaceResult).value

    return AwaitableGetEventhubNamespaceResult(
        auto_inflate_enabled=__ret__.auto_inflate_enabled,
        capacity=__ret__.capacity,
        dedicated_cluster_id=__ret__.dedicated_cluster_id,
        default_primary_connection_string=__ret__.default_primary_connection_string,
        default_primary_connection_string_alias=__ret__.default_primary_connection_string_alias,
        default_primary_key=__ret__.default_primary_key,
        default_secondary_connection_string=__ret__.default_secondary_connection_string,
        default_secondary_connection_string_alias=__ret__.default_secondary_connection_string_alias,
        default_secondary_key=__ret__.default_secondary_key,
        id=__ret__.id,
        kafka_enabled=__ret__.kafka_enabled,
        location=__ret__.location,
        maximum_throughput_units=__ret__.maximum_throughput_units,
        name=__ret__.name,
        resource_group_name=__ret__.resource_group_name,
        sku=__ret__.sku,
        tags=__ret__.tags,
        zone_redundant=__ret__.zone_redundant)
