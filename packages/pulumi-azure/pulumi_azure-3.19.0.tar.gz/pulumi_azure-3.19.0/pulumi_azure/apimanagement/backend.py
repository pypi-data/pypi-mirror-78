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

__all__ = ['Backend']


class Backend(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_management_name: Optional[pulumi.Input[str]] = None,
                 credentials: Optional[pulumi.Input[pulumi.InputType['BackendCredentialsArgs']]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 protocol: Optional[pulumi.Input[str]] = None,
                 proxy: Optional[pulumi.Input[pulumi.InputType['BackendProxyArgs']]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 service_fabric_cluster: Optional[pulumi.Input[pulumi.InputType['BackendServiceFabricClusterArgs']]] = None,
                 title: Optional[pulumi.Input[str]] = None,
                 tls: Optional[pulumi.Input[pulumi.InputType['BackendTlsArgs']]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages a backend within an API Management Service.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The Name of the API Management Service where this backend should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['BackendCredentialsArgs']] credentials: A `credentials` block as documented below.
        :param pulumi.Input[str] description: The description of the backend.
        :param pulumi.Input[str] name: The name of the API Management backend. Changing this forces a new resource to be created.
        :param pulumi.Input[str] protocol: The protocol used by the backend host. Possible values are `http` or `soap`.
        :param pulumi.Input[pulumi.InputType['BackendProxyArgs']] proxy: A `proxy` block as documented below.
        :param pulumi.Input[str] resource_group_name: The Name of the Resource Group where the API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_id: The management URI of the backend host in an external system. This URI can be the ARM Resource ID of Logic Apps, Function Apps or API Apps, or the management endpoint of a Service Fabric cluster.
        :param pulumi.Input[pulumi.InputType['BackendServiceFabricClusterArgs']] service_fabric_cluster: A `service_fabric_cluster` block as documented below.
        :param pulumi.Input[str] title: The title of the backend.
        :param pulumi.Input[pulumi.InputType['BackendTlsArgs']] tls: A `tls` block as documented below.
        :param pulumi.Input[str] url: The URL of the backend host.
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

            if api_management_name is None:
                raise TypeError("Missing required property 'api_management_name'")
            __props__['api_management_name'] = api_management_name
            __props__['credentials'] = credentials
            __props__['description'] = description
            __props__['name'] = name
            if protocol is None:
                raise TypeError("Missing required property 'protocol'")
            __props__['protocol'] = protocol
            __props__['proxy'] = proxy
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['resource_id'] = resource_id
            __props__['service_fabric_cluster'] = service_fabric_cluster
            __props__['title'] = title
            __props__['tls'] = tls
            if url is None:
                raise TypeError("Missing required property 'url'")
            __props__['url'] = url
        super(Backend, __self__).__init__(
            'azure:apimanagement/backend:Backend',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_management_name: Optional[pulumi.Input[str]] = None,
            credentials: Optional[pulumi.Input[pulumi.InputType['BackendCredentialsArgs']]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            protocol: Optional[pulumi.Input[str]] = None,
            proxy: Optional[pulumi.Input[pulumi.InputType['BackendProxyArgs']]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            resource_id: Optional[pulumi.Input[str]] = None,
            service_fabric_cluster: Optional[pulumi.Input[pulumi.InputType['BackendServiceFabricClusterArgs']]] = None,
            title: Optional[pulumi.Input[str]] = None,
            tls: Optional[pulumi.Input[pulumi.InputType['BackendTlsArgs']]] = None,
            url: Optional[pulumi.Input[str]] = None) -> 'Backend':
        """
        Get an existing Backend resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The Name of the API Management Service where this backend should be created. Changing this forces a new resource to be created.
        :param pulumi.Input[pulumi.InputType['BackendCredentialsArgs']] credentials: A `credentials` block as documented below.
        :param pulumi.Input[str] description: The description of the backend.
        :param pulumi.Input[str] name: The name of the API Management backend. Changing this forces a new resource to be created.
        :param pulumi.Input[str] protocol: The protocol used by the backend host. Possible values are `http` or `soap`.
        :param pulumi.Input[pulumi.InputType['BackendProxyArgs']] proxy: A `proxy` block as documented below.
        :param pulumi.Input[str] resource_group_name: The Name of the Resource Group where the API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_id: The management URI of the backend host in an external system. This URI can be the ARM Resource ID of Logic Apps, Function Apps or API Apps, or the management endpoint of a Service Fabric cluster.
        :param pulumi.Input[pulumi.InputType['BackendServiceFabricClusterArgs']] service_fabric_cluster: A `service_fabric_cluster` block as documented below.
        :param pulumi.Input[str] title: The title of the backend.
        :param pulumi.Input[pulumi.InputType['BackendTlsArgs']] tls: A `tls` block as documented below.
        :param pulumi.Input[str] url: The URL of the backend host.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["api_management_name"] = api_management_name
        __props__["credentials"] = credentials
        __props__["description"] = description
        __props__["name"] = name
        __props__["protocol"] = protocol
        __props__["proxy"] = proxy
        __props__["resource_group_name"] = resource_group_name
        __props__["resource_id"] = resource_id
        __props__["service_fabric_cluster"] = service_fabric_cluster
        __props__["title"] = title
        __props__["tls"] = tls
        __props__["url"] = url
        return Backend(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiManagementName")
    def api_management_name(self) -> pulumi.Output[str]:
        """
        The Name of the API Management Service where this backend should be created. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_management_name")

    @property
    @pulumi.getter
    def credentials(self) -> pulumi.Output[Optional['outputs.BackendCredentials']]:
        """
        A `credentials` block as documented below.
        """
        return pulumi.get(self, "credentials")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of the backend.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the API Management backend. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def protocol(self) -> pulumi.Output[str]:
        """
        The protocol used by the backend host. Possible values are `http` or `soap`.
        """
        return pulumi.get(self, "protocol")

    @property
    @pulumi.getter
    def proxy(self) -> pulumi.Output[Optional['outputs.BackendProxy']]:
        """
        A `proxy` block as documented below.
        """
        return pulumi.get(self, "proxy")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The Name of the Resource Group where the API Management Service exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> pulumi.Output[Optional[str]]:
        """
        The management URI of the backend host in an external system. This URI can be the ARM Resource ID of Logic Apps, Function Apps or API Apps, or the management endpoint of a Service Fabric cluster.
        """
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter(name="serviceFabricCluster")
    def service_fabric_cluster(self) -> pulumi.Output[Optional['outputs.BackendServiceFabricCluster']]:
        """
        A `service_fabric_cluster` block as documented below.
        """
        return pulumi.get(self, "service_fabric_cluster")

    @property
    @pulumi.getter
    def title(self) -> pulumi.Output[Optional[str]]:
        """
        The title of the backend.
        """
        return pulumi.get(self, "title")

    @property
    @pulumi.getter
    def tls(self) -> pulumi.Output[Optional['outputs.BackendTls']]:
        """
        A `tls` block as documented below.
        """
        return pulumi.get(self, "tls")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[str]:
        """
        The URL of the backend host.
        """
        return pulumi.get(self, "url")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

