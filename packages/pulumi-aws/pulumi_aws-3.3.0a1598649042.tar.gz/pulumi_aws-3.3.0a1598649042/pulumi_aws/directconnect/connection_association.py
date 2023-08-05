# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['ConnectionAssociation']


class ConnectionAssociation(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 connection_id: Optional[pulumi.Input[str]] = None,
                 lag_id: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Associates a Direct Connect Connection with a LAG.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_connection = aws.directconnect.Connection("exampleConnection",
            bandwidth="1Gbps",
            location="EqSe2")
        example_link_aggregation_group = aws.directconnect.LinkAggregationGroup("exampleLinkAggregationGroup",
            connections_bandwidth="1Gbps",
            location="EqSe2")
        example_connection_association = aws.directconnect.ConnectionAssociation("exampleConnectionAssociation",
            connection_id=example_connection.id,
            lag_id=example_link_aggregation_group.id)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_id: The ID of the connection.
        :param pulumi.Input[str] lag_id: The ID of the LAG with which to associate the connection.
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

            if connection_id is None:
                raise TypeError("Missing required property 'connection_id'")
            __props__['connection_id'] = connection_id
            if lag_id is None:
                raise TypeError("Missing required property 'lag_id'")
            __props__['lag_id'] = lag_id
        super(ConnectionAssociation, __self__).__init__(
            'aws:directconnect/connectionAssociation:ConnectionAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            connection_id: Optional[pulumi.Input[str]] = None,
            lag_id: Optional[pulumi.Input[str]] = None) -> 'ConnectionAssociation':
        """
        Get an existing ConnectionAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_id: The ID of the connection.
        :param pulumi.Input[str] lag_id: The ID of the LAG with which to associate the connection.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["connection_id"] = connection_id
        __props__["lag_id"] = lag_id
        return ConnectionAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="connectionId")
    def connection_id(self) -> pulumi.Output[str]:
        """
        The ID of the connection.
        """
        return pulumi.get(self, "connection_id")

    @property
    @pulumi.getter(name="lagId")
    def lag_id(self) -> pulumi.Output[str]:
        """
        The ID of the LAG with which to associate the connection.
        """
        return pulumi.get(self, "lag_id")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

