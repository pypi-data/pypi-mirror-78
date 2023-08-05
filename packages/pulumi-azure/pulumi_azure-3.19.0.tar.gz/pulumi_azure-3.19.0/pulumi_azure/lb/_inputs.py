# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'LoadBalancerFrontendIpConfigurationArgs',
    'OutboundRuleFrontendIpConfigurationArgs',
]

@pulumi.input_type
class LoadBalancerFrontendIpConfigurationArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 id: Optional[pulumi.Input[str]] = None,
                 inbound_nat_rules: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 load_balancer_rules: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 outbound_rules: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 private_ip_address: Optional[pulumi.Input[str]] = None,
                 private_ip_address_allocation: Optional[pulumi.Input[str]] = None,
                 private_ip_address_version: Optional[pulumi.Input[str]] = None,
                 public_ip_address_id: Optional[pulumi.Input[str]] = None,
                 public_ip_prefix_id: Optional[pulumi.Input[str]] = None,
                 subnet_id: Optional[pulumi.Input[str]] = None,
                 zones: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: Specifies the name of the frontend ip configuration.
        :param pulumi.Input[str] id: The id of the Frontend IP Configuration.
        :param pulumi.Input[List[pulumi.Input[str]]] inbound_nat_rules: The list of IDs of inbound rules that use this frontend IP.
        :param pulumi.Input[List[pulumi.Input[str]]] load_balancer_rules: The list of IDs of load balancing rules that use this frontend IP.
        :param pulumi.Input[List[pulumi.Input[str]]] outbound_rules: The list of IDs outbound rules that use this frontend IP.
        :param pulumi.Input[str] private_ip_address: Private IP Address to assign to the Load Balancer. The last one and first four IPs in any range are reserved and cannot be manually assigned.
        :param pulumi.Input[str] private_ip_address_allocation: The allocation method for the Private IP Address used by this Load Balancer. Possible values as `Dynamic` and `Static`.
        :param pulumi.Input[str] private_ip_address_version: The version of IP that the Private IP Address is. Possible values are `IPv4` or `IPv6`.
        :param pulumi.Input[str] public_ip_address_id: The ID of a Public IP Address which should be associated with the Load Balancer.
        :param pulumi.Input[str] public_ip_prefix_id: The ID of a Public IP Prefix which should be associated with the Load Balancer. Public IP Prefix can only be used with outbound rules.
        :param pulumi.Input[str] subnet_id: The ID of the Subnet which should be associated with the IP Configuration.
        :param pulumi.Input[str] zones: A list of Availability Zones which the Load Balancer's IP Addresses should be created in.
        """
        pulumi.set(__self__, "name", name)
        if id is not None:
            pulumi.set(__self__, "id", id)
        if inbound_nat_rules is not None:
            pulumi.set(__self__, "inbound_nat_rules", inbound_nat_rules)
        if load_balancer_rules is not None:
            pulumi.set(__self__, "load_balancer_rules", load_balancer_rules)
        if outbound_rules is not None:
            pulumi.set(__self__, "outbound_rules", outbound_rules)
        if private_ip_address is not None:
            pulumi.set(__self__, "private_ip_address", private_ip_address)
        if private_ip_address_allocation is not None:
            pulumi.set(__self__, "private_ip_address_allocation", private_ip_address_allocation)
        if private_ip_address_version is not None:
            pulumi.set(__self__, "private_ip_address_version", private_ip_address_version)
        if public_ip_address_id is not None:
            pulumi.set(__self__, "public_ip_address_id", public_ip_address_id)
        if public_ip_prefix_id is not None:
            pulumi.set(__self__, "public_ip_prefix_id", public_ip_prefix_id)
        if subnet_id is not None:
            pulumi.set(__self__, "subnet_id", subnet_id)
        if zones is not None:
            pulumi.set(__self__, "zones", zones)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Specifies the name of the frontend ip configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the Frontend IP Configuration.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)

    @property
    @pulumi.getter(name="inboundNatRules")
    def inbound_nat_rules(self) -> Optional[pulumi.Input[List[pulumi.Input[str]]]]:
        """
        The list of IDs of inbound rules that use this frontend IP.
        """
        return pulumi.get(self, "inbound_nat_rules")

    @inbound_nat_rules.setter
    def inbound_nat_rules(self, value: Optional[pulumi.Input[List[pulumi.Input[str]]]]):
        pulumi.set(self, "inbound_nat_rules", value)

    @property
    @pulumi.getter(name="loadBalancerRules")
    def load_balancer_rules(self) -> Optional[pulumi.Input[List[pulumi.Input[str]]]]:
        """
        The list of IDs of load balancing rules that use this frontend IP.
        """
        return pulumi.get(self, "load_balancer_rules")

    @load_balancer_rules.setter
    def load_balancer_rules(self, value: Optional[pulumi.Input[List[pulumi.Input[str]]]]):
        pulumi.set(self, "load_balancer_rules", value)

    @property
    @pulumi.getter(name="outboundRules")
    def outbound_rules(self) -> Optional[pulumi.Input[List[pulumi.Input[str]]]]:
        """
        The list of IDs outbound rules that use this frontend IP.
        """
        return pulumi.get(self, "outbound_rules")

    @outbound_rules.setter
    def outbound_rules(self, value: Optional[pulumi.Input[List[pulumi.Input[str]]]]):
        pulumi.set(self, "outbound_rules", value)

    @property
    @pulumi.getter(name="privateIpAddress")
    def private_ip_address(self) -> Optional[pulumi.Input[str]]:
        """
        Private IP Address to assign to the Load Balancer. The last one and first four IPs in any range are reserved and cannot be manually assigned.
        """
        return pulumi.get(self, "private_ip_address")

    @private_ip_address.setter
    def private_ip_address(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_ip_address", value)

    @property
    @pulumi.getter(name="privateIpAddressAllocation")
    def private_ip_address_allocation(self) -> Optional[pulumi.Input[str]]:
        """
        The allocation method for the Private IP Address used by this Load Balancer. Possible values as `Dynamic` and `Static`.
        """
        return pulumi.get(self, "private_ip_address_allocation")

    @private_ip_address_allocation.setter
    def private_ip_address_allocation(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_ip_address_allocation", value)

    @property
    @pulumi.getter(name="privateIpAddressVersion")
    def private_ip_address_version(self) -> Optional[pulumi.Input[str]]:
        """
        The version of IP that the Private IP Address is. Possible values are `IPv4` or `IPv6`.
        """
        return pulumi.get(self, "private_ip_address_version")

    @private_ip_address_version.setter
    def private_ip_address_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "private_ip_address_version", value)

    @property
    @pulumi.getter(name="publicIpAddressId")
    def public_ip_address_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of a Public IP Address which should be associated with the Load Balancer.
        """
        return pulumi.get(self, "public_ip_address_id")

    @public_ip_address_id.setter
    def public_ip_address_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_ip_address_id", value)

    @property
    @pulumi.getter(name="publicIpPrefixId")
    def public_ip_prefix_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of a Public IP Prefix which should be associated with the Load Balancer. Public IP Prefix can only be used with outbound rules.
        """
        return pulumi.get(self, "public_ip_prefix_id")

    @public_ip_prefix_id.setter
    def public_ip_prefix_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "public_ip_prefix_id", value)

    @property
    @pulumi.getter(name="subnetId")
    def subnet_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Subnet which should be associated with the IP Configuration.
        """
        return pulumi.get(self, "subnet_id")

    @subnet_id.setter
    def subnet_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "subnet_id", value)

    @property
    @pulumi.getter
    def zones(self) -> Optional[pulumi.Input[str]]:
        """
        A list of Availability Zones which the Load Balancer's IP Addresses should be created in.
        """
        return pulumi.get(self, "zones")

    @zones.setter
    def zones(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "zones", value)


@pulumi.input_type
class OutboundRuleFrontendIpConfigurationArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 id: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] name: The name of the Frontend IP Configuration.
        :param pulumi.Input[str] id: The ID of the Load Balancer Outbound Rule.
        """
        pulumi.set(__self__, "name", name)
        if id is not None:
            pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        The name of the Frontend IP Configuration.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the Load Balancer Outbound Rule.
        """
        return pulumi.get(self, "id")

    @id.setter
    def id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "id", value)


