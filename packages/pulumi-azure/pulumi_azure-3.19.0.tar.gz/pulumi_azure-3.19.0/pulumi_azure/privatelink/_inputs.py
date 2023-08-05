# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'EndpointCustomDnsConfigArgs',
    'EndpointPrivateDnsZoneConfigArgs',
    'EndpointPrivateDnsZoneConfigRecordSetArgs',
    'EndpointPrivateDnsZoneGroupArgs',
    'EndpointPrivateServiceConnectionArgs',
]

@pulumi.input_type
class EndpointCustomDnsConfigArgs:
    def __init__(__self__, *,
                 fqdn: Optional[pulumi.Input[str]] = None,
                 ip_addresses: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[str] fqdn: The fully qualified domain name to the `private_dns_zone`.
        :param pulumi.Input[List[pulumi.Input[str]]] ip_addresses: A list of all IP Addresses that map to the `private_dns_zone` fqdn.
        """
        if fqdn is not None:
            pulumi.set(__self__, "fqdn", fqdn)
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)

    @property
    @pulumi.getter
    def fqdn(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified domain name to the `private_dns_zone`.
        """
        return pulumi.get(self, "fqdn")

    @fqdn.setter
    def fqdn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "fqdn", value)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[pulumi.Input[List[pulumi.Input[str]]]]:
        """
        A list of all IP Addresses that map to the `private_dns_zone` fqdn.
        """
        return pulumi.get(self, "ip_addresses")

    @ip_addresses.setter
    def ip_addresses(self, value: Optional[pulumi.Input[List[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_addresses", value)


@pulumi.input_type
class EndpointPrivateDnsZoneConfigArgs:
    def __init__(__self__, *,
                 id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 private_dns_zone_id: Optional[pulumi.Input[str]] = None,
                 record_sets: Optional[pulumi.Input[List[pulumi.Input['EndpointPrivateDnsZoneConfigRecordSetArgs']]]] = None):
        """
        :param pulumi.Input[str] id: The ID of the Private DNS Zone Config.
        :param pulumi.Input[str] name: Specifies the Name of the Private Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[str] private_dns_zone_id: A list of IP Addresses
        :param pulumi.Input[List[pulumi.Input['EndpointPrivateDnsZoneConfigRecordSetArgs']]] record_sets: A `record_sets` block as defined below.
        """
        if id is not None:
            pulumi.set(__self__, "id", id)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if private_dns_zone_id is not None:
            pulumi.set(__self__, "private_dns_zone_id", private_dns_zone_id)
        if record_sets is not None:
            pulumi.set(__self__, "record_sets", record_sets)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Private DNS Zone Config.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Name of the Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="privateDnsZoneId")
    def private_dns_zone_id(self) -> Optional[pulumi.Input[str]]:
        """
        A list of IP Addresses
        """
        return pulumi.get(self, "private_dns_zone_id")

    @private_dns_zone_id.setter
    def private_dns_zone_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_dns_zone_id", value)

    @property
    @pulumi.getter(name="recordSets")
    def record_sets(self) -> Optional[pulumi.Input[List[pulumi.Input['EndpointPrivateDnsZoneConfigRecordSetArgs']]]]:
        """
        A `record_sets` block as defined below.
        """
        return pulumi.get(self, "record_sets")

    @record_sets.setter
    def record_sets(self, value: Optional[pulumi.Input[List[pulumi.Input['EndpointPrivateDnsZoneConfigRecordSetArgs']]]]):
        pulumi.set(self, "record_sets", value)


@pulumi.input_type
class EndpointPrivateDnsZoneConfigRecordSetArgs:
    def __init__(__self__, *,
                 fqdn: Optional[pulumi.Input[str]] = None,
                 ip_addresses: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 ttl: Optional[pulumi.Input[float]] = None,
                 type: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] fqdn: The fully qualified domain name to the `private_dns_zone`.
        :param pulumi.Input[List[pulumi.Input[str]]] ip_addresses: A list of all IP Addresses that map to the `private_dns_zone` fqdn.
        :param pulumi.Input[str] name: Specifies the Name of the Private Endpoint. Changing this forces a new resource to be created.
        :param pulumi.Input[float] ttl: The time to live for each connection to the `private_dns_zone`.
        :param pulumi.Input[str] type: The type of DNS record.
        """
        if fqdn is not None:
            pulumi.set(__self__, "fqdn", fqdn)
        if ip_addresses is not None:
            pulumi.set(__self__, "ip_addresses", ip_addresses)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if ttl is not None:
            pulumi.set(__self__, "ttl", ttl)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def fqdn(self) -> Optional[pulumi.Input[str]]:
        """
        The fully qualified domain name to the `private_dns_zone`.
        """
        return pulumi.get(self, "fqdn")

    @fqdn.setter
    def fqdn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "fqdn", value)

    @property
    @pulumi.getter(name="ipAddresses")
    def ip_addresses(self) -> Optional[pulumi.Input[List[pulumi.Input[str]]]]:
        """
        A list of all IP Addresses that map to the `private_dns_zone` fqdn.
        """
        return pulumi.get(self, "ip_addresses")

    @ip_addresses.setter
    def ip_addresses(self, value: Optional[pulumi.Input[List[pulumi.Input[str]]]]):
        pulumi.set(self, "ip_addresses", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Specifies the Name of the Private Endpoint. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def ttl(self) -> Optional[pulumi.Input[float]]:
        """
        The time to live for each connection to the `private_dns_zone`.
        """
        return pulumi.get(self, "ttl")

    @ttl.setter
    def ttl(self, value: Optional[pulumi.Input[float]]):
        pulumi.set(self, "ttl", value)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of DNS record.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class EndpointPrivateDnsZoneGroupArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 private_dns_zone_ids: pulumi.Input[List[pulumi.Input[str]]],
                 id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: Specifies the Name of the Private DNS Zone Group. Changing this forces a new `private_dns_zone_group` resource to be created.
        :param pulumi.Input[List[pulumi.Input[str]]] private_dns_zone_ids: Specifies the list of Private DNS Zones to include within the `private_dns_zone_group`.
        :param pulumi.Input[str] id: The ID of the Private DNS Zone Config.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "private_dns_zone_ids", private_dns_zone_ids)
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Specifies the Name of the Private DNS Zone Group. Changing this forces a new `private_dns_zone_group` resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="privateDnsZoneIds")
    def private_dns_zone_ids(self) -> pulumi.Input[List[pulumi.Input[str]]]:
        """
        Specifies the list of Private DNS Zones to include within the `private_dns_zone_group`.
        """
        return pulumi.get(self, "private_dns_zone_ids")

    @private_dns_zone_ids.setter
    def private_dns_zone_ids(self, value: pulumi.Input[List[pulumi.Input[str]]]):
        pulumi.set(self, "private_dns_zone_ids", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Private DNS Zone Config.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)


@pulumi.input_type
class EndpointPrivateServiceConnectionArgs:
    def __init__(__self__, *,
                 is_manual_connection: pulumi.Input[bool],
                 name: pulumi.Input[str],
                 private_connection_resource_id: pulumi.Input[str],
                 private_ip_address: Optional[pulumi.Input[str]] = None,
                 request_message: Optional[pulumi.Input[str]] = None,
                 subresource_names: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None):
        """
        :param pulumi.Input[bool] is_manual_connection: Does the Private Endpoint require Manual Approval from the remote resource owner? Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the Name of the Private Service Connection. Changing this forces a new resource to be created.
        :param pulumi.Input[str] private_connection_resource_id: The ID of the Private Link Enabled Remote Resource which this Private Endpoint should be connected to. Changing this forces a new resource to be created.
        :param pulumi.Input[str] private_ip_address: The private IP address associated with the private endpoint, note that you will have a private IP address assigned to the private endpoint even if the connection request was `Rejected`.
        :param pulumi.Input[str] request_message: A message passed to the owner of the remote resource when the private endpoint attempts to establish the connection to the remote resource. The request message can be a maximum of `140` characters in length. Only valid if `is_manual_connection` is set to `true`.
        :param pulumi.Input[List[pulumi.Input[str]]] subresource_names: A list of subresource names which the Private Endpoint is able to connect to. `subresource_names` corresponds to `group_id`. Changing this forces a new resource to be created.
        """
        pulumi.set(__self__, "is_manual_connection", is_manual_connection)
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "private_connection_resource_id", private_connection_resource_id)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)
        if request_message is not None:
            pulumi.set(__self__, "request_message", request_message)
        if subresource_names is not None:
            pulumi.set(__self__, "subresource_names", subresource_names)

    @property
    @pulumi.getter(name="isManualConnection")
    def is_manual_connection(self) -> pulumi.Input[bool]:
        """
        Does the Private Endpoint require Manual Approval from the remote resource owner? Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "is_manual_connection")

    @is_manual_connection.setter
    def is_manual_connection(self, value: pulumi.Input[bool]):
        pulumi.set(self, "is_manual_connection", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Specifies the Name of the Private Service Connection. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="privateConnectionResourceId")
    def private_connection_resource_id(self) -> pulumi.Input[str]:
        """
        The ID of the Private Link Enabled Remote Resource which this Private Endpoint should be connected to. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "private_connection_resource_id")

    @private_connection_resource_id.setter
    def private_connection_resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "private_connection_resource_id", value)

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        The private IP address associated with the private endpoint, note that you will have a private IP address assigned to the private endpoint even if the connection request was `Rejected`.
        """
        return pulumi.get(self, "private_ip_address")

    @private_ip_address.setter
    def private_ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_ip_address", value)

    @property
    @pulumi.getter(name="requestMessage")
    def request_message(self) -> Optional[pulumi.Input[str]]:
        """
        A message passed to the owner of the remote resource when the private endpoint attempts to establish the connection to the remote resource. The request message can be a maximum of `140` characters in length. Only valid if `is_manual_connection` is set to `true`.
        """
        return pulumi.get(self, "request_message")

    @request_message.setter
    def request_message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "request_message", value)

    @property
    @pulumi.getter(name="subresourceNames")
    def subresource_names(self) -> Optional[pulumi.Input[List[pulumi.Input[str]]]]:
        """
        A list of subresource names which the Private Endpoint is able to connect to. `subresource_names` corresponds to `group_id`. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "subresource_names")

    @subresource_names.setter
    def subresource_names(self, value: Optional[pulumi.Input[List[pulumi.Input[str]]]]):
        pulumi.set(self, "subresource_names", value)


