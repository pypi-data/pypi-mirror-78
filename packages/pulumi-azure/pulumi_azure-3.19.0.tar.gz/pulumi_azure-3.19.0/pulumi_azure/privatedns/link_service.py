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

__all__ = ['LinkService']


class LinkService(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_approval_subscription_ids: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 enable_proxy_protocol: Optional[pulumi.Input[bool]] = None,
                 load_balancer_frontend_ip_configuration_ids: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 location: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 nat_ip_configurations: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['LinkServiceNatIpConfigurationArgs']]]]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 visibility_subscription_ids: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages a Private Link Service.

        > **NOTE** Private Link is now in [GA](https://docs.microsoft.com/en-gb/azure/private-link/).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West Europe")
        example_virtual_network = azure.network.VirtualNetwork("exampleVirtualNetwork",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            address_spaces=["10.5.0.0/16"])
        example_subnet = azure.network.Subnet("exampleSubnet",
            resource_group_name=example_resource_group.name,
            virtual_network_name=example_virtual_network.name,
            address_prefix="10.5.1.0/24",
            enforce_private_link_service_network_policies=True)
        example_public_ip = azure.network.PublicIp("examplePublicIp",
            sku="Standard",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            allocation_method="Static")
        example_load_balancer = azure.lb.LoadBalancer("exampleLoadBalancer",
            sku="Standard",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            frontend_ip_configurations=[azure.lb.LoadBalancerFrontendIpConfigurationArgs(
                name=example_public_ip.name,
                public_ip_address_id=example_public_ip.id,
            )])
        example_link_service = azure.privatedns.LinkService("exampleLinkService",
            resource_group_name=example_resource_group.name,
            location=example_resource_group.location,
            auto_approval_subscription_ids=["00000000-0000-0000-0000-000000000000"],
            visibility_subscription_ids=["00000000-0000-0000-0000-000000000000"],
            load_balancer_frontend_ip_configuration_ids=[example_load_balancer.frontend_ip_configurations[0].id],
            nat_ip_configurations=[
                azure.privatedns.LinkServiceNatIpConfigurationArgs(
                    name="primary",
                    private_ip_address="10.5.1.17",
                    private_ip_address_version="IPv4",
                    subnet_id=example_subnet.id,
                    primary=True,
                ),
                azure.privatedns.LinkServiceNatIpConfigurationArgs(
                    name="secondary",
                    private_ip_address="10.5.1.18",
                    private_ip_address_version="IPv4",
                    subnet_id=example_subnet.id,
                    primary=False,
                ),
            ])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[List[pulumi.Input[str]]] auto_approval_subscription_ids: A list of Subscription UUID/GUID's that will be automatically be able to use this Private Link Service.
        :param pulumi.Input[bool] enable_proxy_protocol: Should the Private Link Service support the Proxy Protocol? Defaults to `false`.
        :param pulumi.Input[List[pulumi.Input[str]]] load_balancer_frontend_ip_configuration_ids: A list of Frontend IP Configuration ID's from a Standard Load Balancer, where traffic from the Private Link Service should be routed. You can use Load Balancer Rules to direct this traffic to appropriate backend pools where your applications are running.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of this Private Link Service. Changing this forces a new resource to be created.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['LinkServiceNatIpConfigurationArgs']]]] nat_ip_configurations: One or more (up to 8) `nat_ip_configuration` block as defined below.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Private Link Service should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource. Changing this forces a new resource to be created.
        :param pulumi.Input[List[pulumi.Input[str]]] visibility_subscription_ids: A list of Subscription UUID/GUID's that will be able to see this Private Link Service.
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

            __props__['auto_approval_subscription_ids'] = auto_approval_subscription_ids
            __props__['enable_proxy_protocol'] = enable_proxy_protocol
            if load_balancer_frontend_ip_configuration_ids is None:
                raise TypeError("Missing required property 'load_balancer_frontend_ip_configuration_ids'")
            __props__['load_balancer_frontend_ip_configuration_ids'] = load_balancer_frontend_ip_configuration_ids
            __props__['location'] = location
            __props__['name'] = name
            if nat_ip_configurations is None:
                raise TypeError("Missing required property 'nat_ip_configurations'")
            __props__['nat_ip_configurations'] = nat_ip_configurations
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['tags'] = tags
            __props__['visibility_subscription_ids'] = visibility_subscription_ids
            __props__['alias'] = None
        super(LinkService, __self__).__init__(
            'azure:privatedns/linkService:LinkService',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            alias: Optional[pulumi.Input[str]] = None,
            auto_approval_subscription_ids: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            enable_proxy_protocol: Optional[pulumi.Input[bool]] = None,
            load_balancer_frontend_ip_configuration_ids: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            location: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            nat_ip_configurations: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['LinkServiceNatIpConfigurationArgs']]]]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            visibility_subscription_ids: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None) -> 'LinkService':
        """
        Get an existing LinkService resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] alias: A globally unique DNS Name for your Private Link Service. You can use this alias to request a connection to your Private Link Service.
        :param pulumi.Input[List[pulumi.Input[str]]] auto_approval_subscription_ids: A list of Subscription UUID/GUID's that will be automatically be able to use this Private Link Service.
        :param pulumi.Input[bool] enable_proxy_protocol: Should the Private Link Service support the Proxy Protocol? Defaults to `false`.
        :param pulumi.Input[List[pulumi.Input[str]]] load_balancer_frontend_ip_configuration_ids: A list of Frontend IP Configuration ID's from a Standard Load Balancer, where traffic from the Private Link Service should be routed. You can use Load Balancer Rules to direct this traffic to appropriate backend pools where your applications are running.
        :param pulumi.Input[str] location: Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] name: Specifies the name of this Private Link Service. Changing this forces a new resource to be created.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['LinkServiceNatIpConfigurationArgs']]]] nat_ip_configurations: One or more (up to 8) `nat_ip_configuration` block as defined below.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group where the Private Link Service should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource. Changing this forces a new resource to be created.
        :param pulumi.Input[List[pulumi.Input[str]]] visibility_subscription_ids: A list of Subscription UUID/GUID's that will be able to see this Private Link Service.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["alias"] = alias
        __props__["auto_approval_subscription_ids"] = auto_approval_subscription_ids
        __props__["enable_proxy_protocol"] = enable_proxy_protocol
        __props__["load_balancer_frontend_ip_configuration_ids"] = load_balancer_frontend_ip_configuration_ids
        __props__["location"] = location
        __props__["name"] = name
        __props__["nat_ip_configurations"] = nat_ip_configurations
        __props__["resource_group_name"] = resource_group_name
        __props__["tags"] = tags
        __props__["visibility_subscription_ids"] = visibility_subscription_ids
        return LinkService(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def alias(self) -> pulumi.Output[str]:
        """
        A globally unique DNS Name for your Private Link Service. You can use this alias to request a connection to your Private Link Service.
        """
        return pulumi.get(self, "alias")

    @property
    @pulumi.getter(name="autoApprovalSubscriptionIds")
    def auto_approval_subscription_ids(self) -> pulumi.Output[Optional[List[str]]]:
        """
        A list of Subscription UUID/GUID's that will be automatically be able to use this Private Link Service.
        """
        return pulumi.get(self, "auto_approval_subscription_ids")

    @property
    @pulumi.getter(name="enableProxyProtocol")
    def enable_proxy_protocol(self) -> pulumi.Output[Optional[bool]]:
        """
        Should the Private Link Service support the Proxy Protocol? Defaults to `false`.
        """
        return pulumi.get(self, "enable_proxy_protocol")

    @property
    @pulumi.getter(name="loadBalancerFrontendIpConfigurationIds")
    def load_balancer_frontend_ip_configuration_ids(self) -> pulumi.Output[List[str]]:
        """
        A list of Frontend IP Configuration ID's from a Standard Load Balancer, where traffic from the Private Link Service should be routed. You can use Load Balancer Rules to direct this traffic to appropriate backend pools where your applications are running.
        """
        return pulumi.get(self, "load_balancer_frontend_ip_configuration_ids")

    @property
    @pulumi.getter
    def location(self) -> pulumi.Output[str]:
        """
        Specifies the supported Azure location where the resource exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "location")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Specifies the name of this Private Link Service. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="natIpConfigurations")
    def nat_ip_configurations(self) -> pulumi.Output[List['outputs.LinkServiceNatIpConfiguration']]:
        """
        One or more (up to 8) `nat_ip_configuration` block as defined below.
        """
        return pulumi.get(self, "nat_ip_configurations")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group where the Private Link Service should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="visibilitySubscriptionIds")
    def visibility_subscription_ids(self) -> pulumi.Output[Optional[List[str]]]:
        """
        A list of Subscription UUID/GUID's that will be able to see this Private Link Service.
        """
        return pulumi.get(self, "visibility_subscription_ids")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

