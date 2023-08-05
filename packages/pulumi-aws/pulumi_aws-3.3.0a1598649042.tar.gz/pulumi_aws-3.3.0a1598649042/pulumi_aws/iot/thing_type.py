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

__all__ = ['ThingType']


class ThingType(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 deprecated: Optional[pulumi.Input[bool]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 properties: Optional[pulumi.Input[pulumi.InputType['ThingTypePropertiesArgs']]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Creates and manages an AWS IoT Thing Type.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        foo = aws.iot.ThingType("foo")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] deprecated: Whether the thing type is deprecated. If true, no new things could be associated with this type.
        :param pulumi.Input[str] name: The name of the thing type.
        :param pulumi.Input[pulumi.InputType['ThingTypePropertiesArgs']] properties: , Configuration block that can contain the following properties of the thing type:
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

            __props__['deprecated'] = deprecated
            __props__['name'] = name
            __props__['properties'] = properties
            __props__['arn'] = None
        super(ThingType, __self__).__init__(
            'aws:iot/thingType:ThingType',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            deprecated: Optional[pulumi.Input[bool]] = None,
            name: Optional[pulumi.Input[str]] = None,
            properties: Optional[pulumi.Input[pulumi.InputType['ThingTypePropertiesArgs']]] = None) -> 'ThingType':
        """
        Get an existing ThingType resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the created AWS IoT Thing Type.
        :param pulumi.Input[bool] deprecated: Whether the thing type is deprecated. If true, no new things could be associated with this type.
        :param pulumi.Input[str] name: The name of the thing type.
        :param pulumi.Input[pulumi.InputType['ThingTypePropertiesArgs']] properties: , Configuration block that can contain the following properties of the thing type:
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["deprecated"] = deprecated
        __props__["name"] = name
        __props__["properties"] = properties
        return ThingType(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the created AWS IoT Thing Type.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def deprecated(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether the thing type is deprecated. If true, no new things could be associated with this type.
        """
        return pulumi.get(self, "deprecated")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the thing type.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def properties(self) -> pulumi.Output[Optional['outputs.ThingTypeProperties']]:
        """
        , Configuration block that can contain the following properties of the thing type:
        """
        return pulumi.get(self, "properties")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

