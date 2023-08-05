# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['OutboundRule']


class OutboundRule(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 allocated_outbound_ports: Optional[pulumi.Input[float]] = None,
                 backend_address_pool_id: Optional[pulumi.Input[str]] = None,
                 enable_tcp_reset: Optional[pulumi.Input[bool]] = None,
                 frontend_ip_configurations: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['OutboundRuleFrontendIpConfigurationArgs']]]]] = None,
                 idle_timeout_in_minutes: Optional[pulumi.Input[float]] = None,
                 loadbalancer_id: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages a Load Balancer Outbound Rule.

        > **NOTE** When using this resource, the Load Balancer needs to have a FrontEnd IP Configuration and a Backend Address Pool Attached.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West US")
        example_public_ip = azure.network.PublicIp("examplePublicIp",
            location="West US",
            resource_group_name=example_resource_group.name,
            allocation_method="Static")
        example_load_balancer = azure.lb.LoadBalancer("exampleLoadBalancer",
            location="West US",
            resource_group_name=example_resource_group.name,
            frontend_ip_configurations=[azure.lb.LoadBalancerFrontendIpConfigurationArgs(
                name="PublicIPAddress",
                public_ip_address_id=example_public_ip.id,
            )])
        example_backend_address_pool = azure.lb.BackendAddressPool("exampleBackendAddressPool",
            resource_group_name=example_resource_group.name,
            loadbalancer_id=example_load_balancer.id)
        example_outbound_rule = azure.lb.OutboundRule("exampleOutboundRule",
            resource_group_name=example_resource_group.name,
            loadbalancer_id=example_load_balancer.id,
            protocol="Tcp",
            backend_address_pool_id=example_backend_address_pool.id,
            frontend_ip_configurations=[azure.lb.OutboundRuleFrontendIpConfigurationArgs(
                name="PublicIPAddress",
            )])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] allocated_outbound_ports: The number of outbound ports to be used for NAT.
        :param pulumi.Input[str] backend_address_pool_id: The ID of the Backend Address Pool. Outbound traffic is randomly load balanced across IPs in the backend IPs.
        :param pulumi.Input[bool] enable_tcp_reset: Receive bidirectional TCP Reset on TCP flow idle timeout or unexpected connection termination. This element is only used when the protocol is set to TCP.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['OutboundRuleFrontendIpConfigurationArgs']]]] frontend_ip_configurations: One or more `frontend_ip_configuration` blocks as defined below.
        :param pulumi.Input[float] idle_timeout_in_minutes: The timeout for the TCP idle connection
        :param pulumi.Input[str] loadbalancer_id: The ID of the Load Balancer in which to create the Outbound Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Outbound Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] protocol: The transport protocol for the external endpoint. Possible values are `Udp`, `Tcp` or `All`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the resource. Changing this forces a new resource to be created.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['allocated_outbound_ports'] = allocated_outbound_ports
            if backend_address_pool_id is None:
                raise TypeError("Missing required property 'backend_address_pool_id'")
            __props__['backend_address_pool_id'] = backend_address_pool_id
            __props__['enable_tcp_reset'] = enable_tcp_reset
            __props__['frontend_ip_configurations'] = frontend_ip_configurations
            __props__['idle_timeout_in_minutes'] = idle_timeout_in_minutes
            if loadbalancer_id is None:
                raise TypeError("Missing required property 'loadbalancer_id'")
            __props__['loadbalancer_id'] = loadbalancer_id
            __props__['name'] = name
            if protocol is None:
                raise TypeError("Missing required property 'protocol'")
            __props__['protocol'] = protocol
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
        super(OutboundRule, __self__).__init__(
            'azure:lb/outboundRule:OutboundRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            allocated_outbound_ports: Optional[pulumi.Input[float]] = None,
            backend_address_pool_id: Optional[pulumi.Input[str]] = None,
            enable_tcp_reset: Optional[pulumi.Input[bool]] = None,
            frontend_ip_configurations: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['OutboundRuleFrontendIpConfigurationArgs']]]]] = None,
            idle_timeout_in_minutes: Optional[pulumi.Input[float]] = None,
            loadbalancer_id: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            protocol: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None) -> 'OutboundRule':
        """
        Get an existing OutboundRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] allocated_outbound_ports: The number of outbound ports to be used for NAT.
        :param pulumi.Input[str] backend_address_pool_id: The ID of the Backend Address Pool. Outbound traffic is randomly load balanced across IPs in the backend IPs.
        :param pulumi.Input[bool] enable_tcp_reset: Receive bidirectional TCP Reset on TCP flow idle timeout or unexpected connection termination. This element is only used when the protocol is set to TCP.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['OutboundRuleFrontendIpConfigurationArgs']]]] frontend_ip_configurations: One or more `frontend_ip_configuration` blocks as defined below.
        :param pulumi.Input[float] idle_timeout_in_minutes: The timeout for the TCP idle connection
        :param pulumi.Input[str] loadbalancer_id: The ID of the Load Balancer in which to create the Outbound Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of the Outbound Rule. Changing this forces a new resource to be created.
        :param pulumi.Input[str] protocol: The transport protocol for the external endpoint. Possible values are `Udp`, `Tcp` or `All`.
        :param pulumi.Input[str] resource_group_name: The name of the resource group in which to create the resource. Changing this forces a new resource to be created.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["allocated_outbound_ports"] = allocated_outbound_ports
        __props__["backend_address_pool_id"] = backend_address_pool_id
        __props__["enable_tcp_reset"] = enable_tcp_reset
        __props__["frontend_ip_configurations"] = frontend_ip_configurations
        __props__["idle_timeout_in_minutes"] = idle_timeout_in_minutes
        __props__["loadbalancer_id"] = loadbalancer_id
        __props__["name"] = name
        __props__["protocol"] = protocol
        __props__["resource_group_name"] = resource_group_name
        return OutboundRule(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="allocatedOutboundPorts")
    def allocated_outbound_ports(self) -> pulumi.Output[Optional[float]]:
        """
        The number of outbound ports to be used for NAT.
        """
        return pulumi.get(self, "allocated_outbound_ports")

    @property
    @pulumi.getter(name="backendAddressPoolId")
    def backend_address_pool_id(self) -> pulumi.Output[str]:
        """
        The ID of the Backend Address Pool. Outbound traffic is randomly load balanced across IPs in the backend IPs.
        """
        return pulumi.get(self, "backend_address_pool_id")

    @property
    @pulumi.getter(name="enableTcpReset")
    def enable_tcp_reset(self) -> pulumi.Output[Optional[bool]]:
        """
        Receive bidirectional TCP Reset on TCP flow idle timeout or unexpected connection termination. This element is only used when the protocol is set to TCP.
        """
        return pulumi.get(self, "enable_tcp_reset")

    @property
    @pulumi.getter(name="frontendIpConfigurations")
    def frontend_ip_configurations(self) -> pulumi.Output[Optional[List['outputs.OutboundRuleFrontendIpConfiguration']]]:
        """
        One or more `frontend_ip_configuration` blocks as defined below.
        """
        return pulumi.get(self, "frontend_ip_configurations")

    @property
    @pulumi.getter(name="idleTimeoutInMinutes")
    def idle_timeout_in_minutes(self) -> pulumi.Output[Optional[float]]:
        """
        The timeout for the TCP idle connection
        """
        return pulumi.get(self, "idle_timeout_in_minutes")

    @property
    @pulumi.getter(name="loadbalancerId")
    def loadbalancer_id(self) -> pulumi.Output[str]:
        """
        The ID of the Load Balancer in which to create the Outbound Rule. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "loadbalancer_id")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of the Outbound Rule. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[str]:
        """
        The transport protocol for the external endpoint. Possible values are `Udp`, `Tcp` or `All`.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the resource group in which to create the resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

