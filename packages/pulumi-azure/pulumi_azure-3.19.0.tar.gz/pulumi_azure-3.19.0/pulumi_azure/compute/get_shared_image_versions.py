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
    'GetSharedImageVersionsResult',
    'AwaitableGetSharedImageVersionsResult',
    'get_shared_image_versions',
]

@pulumi.output_type
class GetSharedImageVersionsResult:
    """
    A collection of values returned by getSharedImageVersions.
    """
    def __init__(__self__, gallery_name=None, id=None, image_name=None, images=None, resource_group_name=None, tags_filter=None):
        if gallery_name and not isinstance(gallery_name, str):
            raise TypeError("Expected argument 'gallery_name' to be a str")
        pulumi.set(__self__, "gallery_name", gallery_name)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if image_name and not isinstance(image_name, str):
            raise TypeError("Expected argument 'image_name' to be a str")
        pulumi.set(__self__, "image_name", image_name)
        if images and not isinstance(images, list):
            raise TypeError("Expected argument 'images' to be a list")
        pulumi.set(__self__, "images", images)
        if resource_group_name and not isinstance(resource_group_name, str):
            raise TypeError("Expected argument 'resource_group_name' to be a str")
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags_filter and not isinstance(tags_filter, dict):
            raise TypeError("Expected argument 'tags_filter' to be a dict")
        pulumi.set(__self__, "tags_filter", tags_filter)

    @property
    @pulumi.getter(name="galleryName")
    def gallery_name(self) -> str:
        return pulumi.get(self, "gallery_name")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="imageName")
    def image_name(self) -> str:
        return pulumi.get(self, "image_name")

    @property
    @pulumi.getter
    def images(self) -> List['outputs.GetSharedImageVersionsImageResult']:
        """
        An `images` block as defined below:
        """
        return pulumi.get(self, "images")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> str:
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter(name="tagsFilter")
    def tags_filter(self) -> Optional[Mapping[str, str]]:
        return pulumi.get(self, "tags_filter")


class AwaitableGetSharedImageVersionsResult(GetSharedImageVersionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSharedImageVersionsResult(
            gallery_name=self.gallery_name,
            id=self.id,
            image_name=self.image_name,
            images=self.images,
            resource_group_name=self.resource_group_name,
            tags_filter=self.tags_filter)


def get_shared_image_versions(gallery_name: Optional[str] = None,
                              image_name: Optional[str] = None,
                              resource_group_name: Optional[str] = None,
                              tags_filter: Optional[Mapping[str, str]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSharedImageVersionsResult:
    """
    Use this data source to access information about existing Versions of a Shared Image within a Shared Image Gallery.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_azure as azure

    example = azure.compute.get_shared_image_versions(gallery_name="my-image-gallery",
        image_name="my-image",
        resource_group_name="example-resources")
    ```


    :param str gallery_name: The name of the Shared Image in which the Shared Image exists.
    :param str image_name: The name of the Shared Image in which this Version exists.
    :param str resource_group_name: The name of the Resource Group in which the Shared Image Gallery exists.
    :param Mapping[str, str] tags_filter: A mapping of tags to filter the list of images against.
    """
    __args__ = dict()
    __args__['galleryName'] = gallery_name
    __args__['imageName'] = image_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['tagsFilter'] = tags_filter
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure:compute/getSharedImageVersions:getSharedImageVersions', __args__, opts=opts, typ=GetSharedImageVersionsResult).value

    return AwaitableGetSharedImageVersionsResult(
        gallery_name=__ret__.gallery_name,
        id=__ret__.id,
        image_name=__ret__.image_name,
        images=__ret__.images,
        resource_group_name=__ret__.resource_group_name,
        tags_filter=__ret__.tags_filter)
