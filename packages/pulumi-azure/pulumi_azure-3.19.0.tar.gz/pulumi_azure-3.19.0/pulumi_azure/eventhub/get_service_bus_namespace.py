# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'GetServiceBusNamespaceResult',
    'AwaitableGetServiceBusNamespaceResult',
    'get_service_bus_namespace',
]

warnings.warn("azure.eventhub.getServiceBusNamespace has been deprecated in favor of azure.servicebus.getNamespace", DeprecationWarning)

@pulumi.output_type
class GetServiceBusNamespaceResult:
    """
    A collection of values returned by getServiceBusNamespace.
    """
    def __init__(__self__, capacity=None, default_primary_connection_string=None, default_primary_key=None, default_secondary_connection_string=None, default_secondary_key=None, id=None, location=None, name=None, resource_group_name=None, sku=None, tags=None, zone_redundant=None):
        if capacity and not isinstance(capacity, float):
            raise TypeError("Expected argument 'capacity' to be a float")
        pulumi.set(__self__, "capacity", capacity)
        if default_primary_connection_string and not isinstance(default_primary_connection_string, str):
            raise TypeError("Expected argument 'default_primary_connection_string' to be a str")
        pulumi.set(__self__, "default_primary_connection_string", default_primary_connection_string)
        if default_primary_key and not isinstance(default_primary_key, str):
            raise TypeError("Expected argument 'default_primary_key' to be a str")
        pulumi.set(__self__, "default_primary_key", default_primary_key)
        if default_secondary_connection_string and not isinstance(default_secondary_connection_string, str):
            raise TypeError("Expected argument 'default_secondary_connection_string' to be a str")
        pulumi.set(__self__, "default_secondary_connection_string", default_secondary_connection_string)
        if default_secondary_key and not isinstance(default_secondary_key, str):
            raise TypeError("Expected argument 'default_secondary_key' to be a str")
        pulumi.set(__self__, "default_secondary_key", default_secondary_key)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if location and not isinstance(location, str):
            raise TypeError("Expected argument 'location' to be a str")
        pulumi.set(__self__, "location", location)
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
    @pulumi.getter
    def capacity(self) -> float:
        """
        The capacity of the ServiceBus Namespace.
        """
        return pulumi.get(self, "capacity")

    @property
    @pulumi.getter(name="defaultPrimaryConnectionString")
    def default_primary_connection_string(self) -> str:
        """
        The primary connection string for the authorization
        rule `RootManageSharedAccessKey`.
        """
        return pulumi.get(self, "default_primary_connection_string")

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
    @pulumi.getter
    def location(self) -> str:
        """
        The location of the Resource Group in which the ServiceBus Namespace exists.
        """
        return pulumi.get(self, "location")

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
        The Tier used for the ServiceBus Namespace.
        """
        return pulumi.get(self, "sku")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        A mapping of tags assigned to the resource.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="zoneRedundant")
    def zone_redundant(self) -> bool:
        """
        Whether or not this ServiceBus Namespace is zone redundant.
        """
        return pulumi.get(self, "zone_redundant")


class AwaitableGetServiceBusNamespaceResult(GetServiceBusNamespaceResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetServiceBusNamespaceResult(
            capacity=self.capacity,
            default_primary_connection_string=self.default_primary_connection_string,
            default_primary_key=self.default_primary_key,
            default_secondary_connection_string=self.default_secondary_connection_string,
            default_secondary_key=self.default_secondary_key,
            id=self.id,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            sku=self.sku,
            tags=self.tags,
            zone_redundant=self.zone_redundant)


def get_service_bus_namespace(name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetServiceBusNamespaceResult:
    """
    Use this data source to access information about an existing ServiceBus Namespace.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.servicebus.get_namespace(name="examplenamespace",
        resource_group_name="example-resources")
    pulumi.export("location", example.location)
    ```


    :param str name: Specifies the name of the ServiceBus Namespace.
    :param str resource_group_name: Specifies the name of the Resource Group where the ServiceBus Namespace exists.
    """
    pulumi.log.warn("get_service_bus_namespace is deprecated: azure.eventhub.getServiceBusNamespace has been deprecated in favor of azure.servicebus.getNamespace")
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:eventhub/getServiceBusNamespace:getServiceBusNamespace', __args__, opts=opts, typ=GetServiceBusNamespaceResult).value

    return AwaitableGetServiceBusNamespaceResult(
        capacity=__ret__.capacity,
        default_primary_connection_string=__ret__.default_primary_connection_string,
        default_primary_key=__ret__.default_primary_key,
        default_secondary_connection_string=__ret__.default_secondary_connection_string,
        default_secondary_key=__ret__.default_secondary_key,
        id=__ret__.id,
        location=__ret__.location,
        name=__ret__.name,
        resource_group_name=__ret__.resource_group_name,
        sku=__ret__.sku,
        tags=__ret__.tags,
        zone_redundant=__ret__.zone_redundant)
