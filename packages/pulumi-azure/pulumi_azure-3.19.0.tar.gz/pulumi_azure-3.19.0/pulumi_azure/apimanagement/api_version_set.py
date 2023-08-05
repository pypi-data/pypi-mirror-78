# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['ApiVersionSet']


class ApiVersionSet(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 api_management_name: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 display_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 version_header_name: Optional[pulumi.Input[str]] = None,
                 version_query_name: Optional[pulumi.Input[str]] = None,
                 versioning_scheme: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages an API Version Set within an API Management Service.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_azure as azure

        example_resource_group = azure.core.ResourceGroup("exampleResourceGroup", location="West US")
        example_service = azure.apimanagement.Service("exampleService",
            location=example_resource_group.location,
            resource_group_name=example_resource_group.name,
            publisher_name="pub1",
            publisher_email="pub1@email.com",
            sku_name="Developer_1")
        example_api_version_set = azure.apimanagement.ApiVersionSet("exampleApiVersionSet",
            resource_group_name=example_resource_group.name,
            api_management_name=example_service.name,
            display_name="ExampleAPIVersionSet",
            versioning_scheme="Segment")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service in which the API Version Set should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] description: The description of API Version Set.
        :param pulumi.Input[str] display_name: The display name of this API Version Set.
        :param pulumi.Input[str] name: The name of the API Version Set. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the parent API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] version_header_name: The name of the Header which should be read from Inbound Requests which defines the API Version.
        :param pulumi.Input[str] version_query_name: The name of the Query String which should be read from Inbound Requests which defines the API Version.
        :param pulumi.Input[str] versioning_scheme: Specifies where in an Inbound HTTP Request that the API Version should be read from. Possible values are `Header`, `Query` and `Segment`.
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
            __props__['description'] = description
            if display_name is None:
                raise TypeError("Missing required property 'display_name'")
            __props__['display_name'] = display_name
            __props__['name'] = name
            if resource_group_name is None:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__['resource_group_name'] = resource_group_name
            __props__['version_header_name'] = version_header_name
            __props__['version_query_name'] = version_query_name
            if versioning_scheme is None:
                raise TypeError("Missing required property 'versioning_scheme'")
            __props__['versioning_scheme'] = versioning_scheme
        super(ApiVersionSet, __self__).__init__(
            'azure:apimanagement/apiVersionSet:ApiVersionSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            api_management_name: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            display_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            version_header_name: Optional[pulumi.Input[str]] = None,
            version_query_name: Optional[pulumi.Input[str]] = None,
            versioning_scheme: Optional[pulumi.Input[str]] = None) -> 'ApiVersionSet':
        """
        Get an existing ApiVersionSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] api_management_name: The name of the API Management Service in which the API Version Set should exist. Changing this forces a new resource to be created.
        :param pulumi.Input[str] description: The description of API Version Set.
        :param pulumi.Input[str] display_name: The display name of this API Version Set.
        :param pulumi.Input[str] name: The name of the API Version Set. Changing this forces a new resource to be created.
        :param pulumi.Input[str] resource_group_name: The name of the Resource Group in which the parent API Management Service exists. Changing this forces a new resource to be created.
        :param pulumi.Input[str] version_header_name: The name of the Header which should be read from Inbound Requests which defines the API Version.
        :param pulumi.Input[str] version_query_name: The name of the Query String which should be read from Inbound Requests which defines the API Version.
        :param pulumi.Input[str] versioning_scheme: Specifies where in an Inbound HTTP Request that the API Version should be read from. Possible values are `Header`, `Query` and `Segment`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["api_management_name"] = api_management_name
        __props__["description"] = description
        __props__["display_name"] = display_name
        __props__["name"] = name
        __props__["resource_group_name"] = resource_group_name
        __props__["version_header_name"] = version_header_name
        __props__["version_query_name"] = version_query_name
        __props__["versioning_scheme"] = versioning_scheme
        return ApiVersionSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="apiManagementName")
    def api_management_name(self) -> pulumi.Output[str]:
        """
        The name of the API Management Service in which the API Version Set should exist. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "api_management_name")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        The description of API Version Set.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="displayName")
    def display_name(self) -> pulumi.Output[str]:
        """
        The display name of this API Version Set.
        """
        return pulumi.get(self, "display_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the API Version Set. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        The name of the Resource Group in which the parent API Management Service exists. Changing this forces a new resource to be created.
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="versionHeaderName")
    def version_header_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the Header which should be read from Inbound Requests which defines the API Version.
        """
        return pulumi.get(self, "version_header_name")

    @property
    @pulumi.getter(name="versionQueryName")
    def version_query_name(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the Query String which should be read from Inbound Requests which defines the API Version.
        """
        return pulumi.get(self, "version_query_name")

    @property
    @pulumi.getter(name="versioningScheme")
    def versioning_scheme(self) -> pulumi.Output[str]:
        """
        Specifies where in an Inbound HTTP Request that the API Version should be read from. Possible values are `Header`, `Query` and `Segment`.
        """
        return pulumi.get(self, "versioning_scheme")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

