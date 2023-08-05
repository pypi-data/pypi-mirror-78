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
    'GetVirtualNetworkGatewayResult',
    'AwaitableGetVirtualNetworkGatewayResult',
    'get_virtual_network_gateway',
]

@pulumi.output_type
class GetVirtualNetworkGatewayResult:
    """
    A collection of values returned by getVirtualNetworkGateway.
    """
    def __init__(__self__, active_active=None, bgp_settings=None, default_local_network_gateway_id=None, enable_bgp=None, generation=None, id=None, ip_configurations=None, location=None, name=None, resource_group_name=None, sku=None, tags=None, type=None, vpn_client_configurations=None, vpn_type=None):
        if active_active and not isinstance(active_active, bool):
            raise TypeError("Expected argument 'active_active' to be a bool")
        pulumi.set(__self__, "active_active", active_active)
        if bgp_settings and not isinstance(bgp_settings, list):
            raise TypeError("Expected argument 'bgp_settings' to be a list")
        pulumi.set(__self__, "bgp_settings", bgp_settings)
        if default_local_network_gateway_id and not isinstance(default_local_network_gateway_id, str):
            raise TypeError("Expected argument 'default_local_network_gateway_id' to be a str")
        pulumi.set(__self__, "default_local_network_gateway_id", default_local_network_gateway_id)
        if enable_bgp and not isinstance(enable_bgp, bool):
            raise TypeError("Expected argument 'enable_bgp' to be a bool")
        pulumi.set(__self__, "enable_bgp", enable_bgp)
        if generation and not isinstance(generation, str):
            raise TypeError("Expected argument 'generation' to be a str")
        pulumi.set(__self__, "generation", generation)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ip_configurations and not isinstance(ip_configurations, list):
            raise TypeError("Expected argument 'ip_configurations' to be a list")
        pulumi.set(__self__, "ip_configurations", ip_configurations)
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
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if vpn_client_configurations and not isinstance(vpn_client_configurations, list):
            raise TypeError("Expected argument 'vpn_client_configurations' to be a list")
        pulumi.set(__self__, "vpn_client_configurations", vpn_client_configurations)
        if vpn_type and not isinstance(vpn_type, str):
            raise TypeError("Expected argument 'vpn_type' to be a str")
        pulumi.set(__self__, "vpn_type", vpn_type)

    @property
    @pulumi.getter(name="activeActive")
    def active_active(self) -> bool:
        """
        Is this an Active-Active Gateway?
        """
        return pulumi.get(self, "active_active")

    @property
    @pulumi.getter(name="bgpSettings")
    def bgp_settings(self) -> List['outputs.GetVirtualNetworkGatewayBgpSettingResult']:
        return pulumi.get(self, "bgp_settings")

    @property
    @pulumi.getter(name="defaultLocalNetworkGatewayId")
    def default_local_network_gateway_id(self) -> str:
        """
        The ID of the local network gateway
        through which outbound Internet traffic from the virtual network in which the
        gateway is created will be routed (*forced tunneling*). Refer to the
        [Azure documentation on forced tunneling](https://docs.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-forced-tunneling-rm).
        """
        return pulumi.get(self, "default_local_network_gateway_id")

    @property
    @pulumi.getter(name="enableBgp")
    def enable_bgp(self) -> bool:
        """
        Will BGP (Border Gateway Protocol) will be enabled
        for this Virtual Network Gateway.
        """
        return pulumi.get(self, "enable_bgp")

    @property
    @pulumi.getter
    def generation(self) -> str:
        """
        The Generation of the Virtual Network Gateway.
        """
        return pulumi.get(self, "generation")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="ipConfigurations")
    def ip_configurations(self) -> List['outputs.GetVirtualNetworkGatewayIpConfigurationResult']:
        """
        One or two `ip_configuration` blocks documented below.
        """
        return pulumi.get(self, "ip_configurations")

    @property
    @pulumi.getter
    def location(self) -> str:
        """
        The location/region where the Virtual Network Gateway is located.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The user-defined name of the revoked certificate.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def sku(self) -> str:
        """
        Configuration of the size and capacity of the Virtual Network Gateway.
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
    @pulumi.getter
    def type(self) -> str:
        """
        The type of the Virtual Network Gateway.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="vpnClientConfigurations")
    def vpn_client_configurations(self) -> List['outputs.GetVirtualNetworkGatewayVpnClientConfigurationResult']:
        """
        A `vpn_client_configuration` block which is documented below.
        """
        return pulumi.get(self, "vpn_client_configurations")

    @property
    @pulumi.getter(name="vpnType")
    def vpn_type(self) -> str:
        """
        The routing type of the Virtual Network Gateway.
        """
        return pulumi.get(self, "vpn_type")


class AwaitableGetVirtualNetworkGatewayResult(GetVirtualNetworkGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetVirtualNetworkGatewayResult(
            active_active=self.active_active,
            bgp_settings=self.bgp_settings,
            default_local_network_gateway_id=self.default_local_network_gateway_id,
            enable_bgp=self.enable_bgp,
            generation=self.generation,
            id=self.id,
            ip_configurations=self.ip_configurations,
            location=self.location,
            name=self.name,
            resource_group_name=self.resource_group_name,
            sku=self.sku,
            tags=self.tags,
            type=self.type,
            vpn_client_configurations=self.vpn_client_configurations,
            vpn_type=self.vpn_type)


def get_virtual_network_gateway(name: Optional[str] = None,
                                resource_group_name: Optional[str] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetVirtualNetworkGatewayResult:
    """
    Use this data source to access information about an existing Virtual Network Gateway.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.network.get_virtual_network_gateway(name="production",
        resource_group_name="networking")
    pulumi.export("virtualNetworkGatewayId", example.id)
    ```


    :param str name: Specifies the name of the Virtual Network Gateway.
    :param str resource_group_name: Specifies the name of the resource group the Virtual Network Gateway is located in.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['resourceGroupName'] = resource_group_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:network/getVirtualNetworkGateway:getVirtualNetworkGateway', __args__, opts=opts, typ=GetVirtualNetworkGatewayResult).value

    return AwaitableGetVirtualNetworkGatewayResult(
        active_active=__ret__.active_active,
        bgp_settings=__ret__.bgp_settings,
        default_local_network_gateway_id=__ret__.default_local_network_gateway_id,
        enable_bgp=__ret__.enable_bgp,
        generation=__ret__.generation,
        id=__ret__.id,
        ip_configurations=__ret__.ip_configurations,
        location=__ret__.location,
        name=__ret__.name,
        resource_group_name=__ret__.resource_group_name,
        sku=__ret__.sku,
        tags=__ret__.tags,
        type=__ret__.type,
        vpn_client_configurations=__ret__.vpn_client_configurations,
        vpn_type=__ret__.vpn_type)
