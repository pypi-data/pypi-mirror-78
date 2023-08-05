# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'GetVirtualNetworkResult',
    'AwaitableGetVirtualNetworkResult',
    'get_virtual_network',
]

@pulumi.output_type
class GetVirtualNetworkResult:
    """
    A collection of values returned by getVirtualNetwork.
    """
    def __init__(__self__, allowed_subnets=None, id=None, lab_name=None, name=None, resource_group_name=None, subnet_overrides=None, unique_identifier=None):
        if allowed_subnets and not isinstance(allowed_subnets, list):
            raise TypeError("Expected argument 'allowed_subnets' to be a list")
        pulumi.set(__self__, "allowed_subnets", allowed_subnets)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if lab_name and not isinstance(lab_name, str):
            raise TypeError("Expected argument 'lab_name' to be a str")
        pulumi.set(__self__, "lab_name", lab_name)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if subnet_overrides and not isinstance(subnet_overrides, list):
            raise TypeError("Expected argument 'subnet_overrides' to be a list")
        pulumi.set(__self__, "subnet_overrides", subnet_overrides)
        if unique_identifier and not isinstance(unique_identifier, str):
            raise TypeError("Expected argument 'unique_identifier' to be a str")
        pulumi.set(__self__, "unique_identifier", unique_identifier)

    @property
    @pulumi.getter(name="allowedSubnets")
    def allowed_subnets(self) -> List['outputs.GetVirtualNetworkAllowedSubnetResult']:
        """
        The list of subnets enabled for the virtual network as defined below.
        """
        return pulumi.get(self, "allowed_subnets")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="labName")
    def lab_name(self) -> str:
        return pulumi.get(self, "lab_name")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="subnetOverrides")
    def subnet_overrides(self) -> List['outputs.GetVirtualNetworkSubnetOverrideResult']:
        """
        The list of permission overrides for the subnets as defined below.
        """
        return pulumi.get(self, "subnet_overrides")

    @property
    @pulumi.getter(name="uniqueIdentifier")
    def unique_identifier(self) -> str:
        """
        The unique immutable identifier of the virtual network.
        """
        return pulumi.get(self, "unique_identifier")


class AwaitableGetVirtualNetworkResult(GetVirtualNetworkResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualNetworkResult(
            allowed_subnets=self.allowed_subnets,
            id=self.id,
            lab_name=self.lab_name,
            name=self.name,
            resource_group_name=self.resource_group_name,
            subnet_overrides=self.subnet_overrides,
            unique_identifier=self.unique_identifier)


def get_virtual_network(lab_name: Optional[str] = None,
                        name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualNetworkResult:
    """
    Use this data source to access information about an existing Dev Test Lab Virtual Network.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.devtest.get_virtual_network(name="example-network",
        lab_name="examplelab",
        resource_group_name="example-resource")
    pulumi.export("labSubnetName", example.allowed_subnets[0].lab_subnet_name)
    ```


    :param str lab_name: Specifies the name of the Dev Test Lab.
    :param str name: Specifies the name of the Virtual Network.
    :param str resource_group_name: Specifies the name of the resource group that contains the Virtual Network.
    """
    __args__ = dict()
    __args__['labName'] = lab_name
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:devtest/getVirtualNetwork:getVirtualNetwork', __args__, opts=opts, typ=GetVirtualNetworkResult).value

    return AwaitableGetVirtualNetworkResult(
        allowed_subnets=__ret__.allowed_subnets,
        id=__ret__.id,
        lab_name=__ret__.lab_name,
        name=__ret__.name,
        resource_group_name=__ret__.resource_group_name,
        subnet_overrides=__ret__.subnet_overrides,
        unique_identifier=__ret__.unique_identifier)
