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

__all__ = ['Table']


class Table(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attributes: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['TableAttributeArgs']]]]] = None,
                 billing_mode: Optional[pulumi.Input[str]] = None,
                 global_secondary_indexes: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['TableGlobalSecondaryIndexArgs']]]]] = None,
                 hash_key: Optional[pulumi.Input[str]] = None,
                 local_secondary_indexes: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['TableLocalSecondaryIndexArgs']]]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 point_in_time_recovery: Optional[pulumi.Input[pulumi.InputType['TablePointInTimeRecoveryArgs']]] = None,
                 range_key: Optional[pulumi.Input[str]] = None,
                 read_capacity: Optional[pulumi.Input[float]] = None,
                 replicas: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['TableReplicaArgs']]]]] = None,
                 server_side_encryption: Optional[pulumi.Input[pulumi.InputType['TableServerSideEncryptionArgs']]] = None,
                 stream_enabled: Optional[pulumi.Input[bool]] = None,
                 stream_view_type: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 ttl: Optional[pulumi.Input[pulumi.InputType['TableTtlArgs']]] = None,
                 write_capacity: Optional[pulumi.Input[float]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a DynamoDB table resource

        > **Note:** It is recommended to use [`ignoreChanges`](https://www.pulumi.com/docs/intro/concepts/programming-model/#ignorechanges) for `read_capacity` and/or `write_capacity` if there's `autoscaling policy` attached to the table.

        ## Example Usage

        The following dynamodb table description models the table and GSI shown
        in the [AWS SDK example documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html)

        ```python
        import pulumi
        import pulumi_aws as aws

        basic_dynamodb_table = aws.dynamodb.Table("basic-dynamodb-table",
            attributes=[
                aws.dynamodb.TableAttributeArgs(
                    name="UserId",
                    type="S",
                ),
                aws.dynamodb.TableAttributeArgs(
                    name="GameTitle",
                    type="S",
                ),
                aws.dynamodb.TableAttributeArgs(
                    name="TopScore",
                    type="N",
                ),
            ],
            billing_mode="PROVISIONED",
            global_secondary_indexes=[aws.dynamodb.TableGlobalSecondaryIndexArgs(
                hash_key="GameTitle",
                name="GameTitleIndex",
                non_key_attributes=["UserId"],
                projection_type="INCLUDE",
                range_key="TopScore",
                read_capacity=10,
                write_capacity=10,
            )],
            hash_key="UserId",
            range_key="GameTitle",
            read_capacity=20,
            tags={
                "Environment": "production",
                "Name": "dynamodb-table-1",
            },
            ttl=aws.dynamodb.TableTtlArgs(
                attribute_name="TimeToExist",
                enabled=False,
            ),
            write_capacity=20)
        ```
        ### Global Tables

        This resource implements support for [DynamoDB Global Tables V2 (version 2019.11.21)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/globaltables.V2.html) via `replica` configuration blocks. For working with [DynamoDB Global Tables V1 (version 2017.11.29)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/globaltables.V1.html), see the `dynamodb.GlobalTable` resource.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.dynamodb.Table("example",
            attributes=[aws.dynamodb.TableAttributeArgs(
                name="TestTableHashKey",
                type="S",
            )],
            billing_mode="PAY_PER_REQUEST",
            hash_key="TestTableHashKey",
            replicas=[
                aws.dynamodb.TableReplicaArgs(
                    region_name="us-east-2",
                ),
                aws.dynamodb.TableReplicaArgs(
                    region_name="us-west-2",
                ),
            ],
            stream_enabled=True,
            stream_view_type="NEW_AND_OLD_IMAGES")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['TableAttributeArgs']]]] attributes: List of nested attribute definitions. Only required for `hash_key` and `range_key` attributes. Each attribute has two properties:
        :param pulumi.Input[str] billing_mode: Controls how you are charged for read and write throughput and how you manage capacity. The valid values are `PROVISIONED` and `PAY_PER_REQUEST`. Defaults to `PROVISIONED`.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['TableGlobalSecondaryIndexArgs']]]] global_secondary_indexes: Describe a GSI for the table;
               subject to the normal limits on the number of GSIs, projected
               attributes, etc.
        :param pulumi.Input[str] hash_key: The name of the hash key in the index; must be
               defined as an attribute in the resource.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['TableLocalSecondaryIndexArgs']]]] local_secondary_indexes: Describe an LSI on the table;
               these can only be allocated *at creation* so you cannot change this
               definition after you have created the resource.
        :param pulumi.Input[str] name: The name of the index
        :param pulumi.Input[pulumi.InputType['TablePointInTimeRecoveryArgs']] point_in_time_recovery: Point-in-time recovery options.
        :param pulumi.Input[str] range_key: The name of the range key; must be defined
        :param pulumi.Input[float] read_capacity: The number of read units for this index. Must be set if billing_mode is set to PROVISIONED.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['TableReplicaArgs']]]] replicas: Configuration block(s) with [DynamoDB Global Tables V2 (version 2019.11.21)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/globaltables.V2.html) replication configurations. Detailed below.
        :param pulumi.Input[pulumi.InputType['TableServerSideEncryptionArgs']] server_side_encryption: Encryption at rest options. AWS DynamoDB tables are automatically encrypted at rest with an AWS owned Customer Master Key if this argument isn't specified.
        :param pulumi.Input[bool] stream_enabled: Indicates whether Streams are to be enabled (true) or disabled (false).
        :param pulumi.Input[str] stream_view_type: When an item in the table is modified, StreamViewType determines what information is written to the table's stream. Valid values are `KEYS_ONLY`, `NEW_IMAGE`, `OLD_IMAGE`, `NEW_AND_OLD_IMAGES`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to populate on the created table.
        :param pulumi.Input[pulumi.InputType['TableTtlArgs']] ttl: Defines ttl, has two properties, and can only be specified once:
        :param pulumi.Input[float] write_capacity: The number of write units for this index. Must be set if billing_mode is set to PROVISIONED.
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

            if attributes is None:
                raise TypeError("Missing required property 'attributes'")
            __props__['attributes'] = attributes
            __props__['billing_mode'] = billing_mode
            __props__['global_secondary_indexes'] = global_secondary_indexes
            if hash_key is None:
                raise TypeError("Missing required property 'hash_key'")
            __props__['hash_key'] = hash_key
            __props__['local_secondary_indexes'] = local_secondary_indexes
            __props__['name'] = name
            __props__['point_in_time_recovery'] = point_in_time_recovery
            __props__['range_key'] = range_key
            __props__['read_capacity'] = read_capacity
            __props__['replicas'] = replicas
            __props__['server_side_encryption'] = server_side_encryption
            __props__['stream_enabled'] = stream_enabled
            __props__['stream_view_type'] = stream_view_type
            __props__['tags'] = tags
            __props__['ttl'] = ttl
            __props__['write_capacity'] = write_capacity
            __props__['arn'] = None
            __props__['stream_arn'] = None
            __props__['stream_label'] = None
        super(Table, __self__).__init__(
            'aws:dynamodb/table:Table',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            attributes: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['TableAttributeArgs']]]]] = None,
            billing_mode: Optional[pulumi.Input[str]] = None,
            global_secondary_indexes: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['TableGlobalSecondaryIndexArgs']]]]] = None,
            hash_key: Optional[pulumi.Input[str]] = None,
            local_secondary_indexes: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['TableLocalSecondaryIndexArgs']]]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            point_in_time_recovery: Optional[pulumi.Input[pulumi.InputType['TablePointInTimeRecoveryArgs']]] = None,
            range_key: Optional[pulumi.Input[str]] = None,
            read_capacity: Optional[pulumi.Input[float]] = None,
            replicas: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['TableReplicaArgs']]]]] = None,
            server_side_encryption: Optional[pulumi.Input[pulumi.InputType['TableServerSideEncryptionArgs']]] = None,
            stream_arn: Optional[pulumi.Input[str]] = None,
            stream_enabled: Optional[pulumi.Input[bool]] = None,
            stream_label: Optional[pulumi.Input[str]] = None,
            stream_view_type: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            ttl: Optional[pulumi.Input[pulumi.InputType['TableTtlArgs']]] = None,
            write_capacity: Optional[pulumi.Input[float]] = None) -> 'Table':
        """
        Get an existing Table resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The arn of the table
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['TableAttributeArgs']]]] attributes: List of nested attribute definitions. Only required for `hash_key` and `range_key` attributes. Each attribute has two properties:
        :param pulumi.Input[str] billing_mode: Controls how you are charged for read and write throughput and how you manage capacity. The valid values are `PROVISIONED` and `PAY_PER_REQUEST`. Defaults to `PROVISIONED`.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['TableGlobalSecondaryIndexArgs']]]] global_secondary_indexes: Describe a GSI for the table;
               subject to the normal limits on the number of GSIs, projected
               attributes, etc.
        :param pulumi.Input[str] hash_key: The name of the hash key in the index; must be
               defined as an attribute in the resource.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['TableLocalSecondaryIndexArgs']]]] local_secondary_indexes: Describe an LSI on the table;
               these can only be allocated *at creation* so you cannot change this
               definition after you have created the resource.
        :param pulumi.Input[str] name: The name of the index
        :param pulumi.Input[pulumi.InputType['TablePointInTimeRecoveryArgs']] point_in_time_recovery: Point-in-time recovery options.
        :param pulumi.Input[str] range_key: The name of the range key; must be defined
        :param pulumi.Input[float] read_capacity: The number of read units for this index. Must be set if billing_mode is set to PROVISIONED.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['TableReplicaArgs']]]] replicas: Configuration block(s) with [DynamoDB Global Tables V2 (version 2019.11.21)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/globaltables.V2.html) replication configurations. Detailed below.
        :param pulumi.Input[pulumi.InputType['TableServerSideEncryptionArgs']] server_side_encryption: Encryption at rest options. AWS DynamoDB tables are automatically encrypted at rest with an AWS owned Customer Master Key if this argument isn't specified.
        :param pulumi.Input[str] stream_arn: The ARN of the Table Stream. Only available when `stream_enabled = true`
        :param pulumi.Input[bool] stream_enabled: Indicates whether Streams are to be enabled (true) or disabled (false).
        :param pulumi.Input[str] stream_label: A timestamp, in ISO 8601 format, for this stream. Note that this timestamp is not
               a unique identifier for the stream on its own. However, the combination of AWS customer ID,
               table name and this field is guaranteed to be unique.
               It can be used for creating CloudWatch Alarms. Only available when `stream_enabled = true`
        :param pulumi.Input[str] stream_view_type: When an item in the table is modified, StreamViewType determines what information is written to the table's stream. Valid values are `KEYS_ONLY`, `NEW_IMAGE`, `OLD_IMAGE`, `NEW_AND_OLD_IMAGES`.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to populate on the created table.
        :param pulumi.Input[pulumi.InputType['TableTtlArgs']] ttl: Defines ttl, has two properties, and can only be specified once:
        :param pulumi.Input[float] write_capacity: The number of write units for this index. Must be set if billing_mode is set to PROVISIONED.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["attributes"] = attributes
        __props__["billing_mode"] = billing_mode
        __props__["global_secondary_indexes"] = global_secondary_indexes
        __props__["hash_key"] = hash_key
        __props__["local_secondary_indexes"] = local_secondary_indexes
        __props__["name"] = name
        __props__["point_in_time_recovery"] = point_in_time_recovery
        __props__["range_key"] = range_key
        __props__["read_capacity"] = read_capacity
        __props__["replicas"] = replicas
        __props__["server_side_encryption"] = server_side_encryption
        __props__["stream_arn"] = stream_arn
        __props__["stream_enabled"] = stream_enabled
        __props__["stream_label"] = stream_label
        __props__["stream_view_type"] = stream_view_type
        __props__["tags"] = tags
        __props__["ttl"] = ttl
        __props__["write_capacity"] = write_capacity
        return Table(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The arn of the table
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def attributes(self) -> pulumi.Output[List['outputs.TableAttribute']]:
        """
        List of nested attribute definitions. Only required for `hash_key` and `range_key` attributes. Each attribute has two properties:
        """
        return pulumi.get(self, "attributes")

    @property
    @pulumi.getter(name="billingMode")
    def billing_mode(self) -> pulumi.Output[Optional[str]]:
        """
        Controls how you are charged for read and write throughput and how you manage capacity. The valid values are `PROVISIONED` and `PAY_PER_REQUEST`. Defaults to `PROVISIONED`.
        """
        return pulumi.get(self, "billing_mode")

    @property
    @pulumi.getter(name="globalSecondaryIndexes")
    def global_secondary_indexes(self) -> pulumi.Output[Optional[List['outputs.TableGlobalSecondaryIndex']]]:
        """
        Describe a GSI for the table;
        subject to the normal limits on the number of GSIs, projected
        attributes, etc.
        """
        return pulumi.get(self, "global_secondary_indexes")

    @property
    @pulumi.getter(name="hashKey")
    def hash_key(self) -> pulumi.Output[str]:
        """
        The name of the hash key in the index; must be
        defined as an attribute in the resource.
        """
        return pulumi.get(self, "hash_key")

    @property
    @pulumi.getter(name="localSecondaryIndexes")
    def local_secondary_indexes(self) -> pulumi.Output[Optional[List['outputs.TableLocalSecondaryIndex']]]:
        """
        Describe an LSI on the table;
        these can only be allocated *at creation* so you cannot change this
        definition after you have created the resource.
        """
        return pulumi.get(self, "local_secondary_indexes")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the index
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="pointInTimeRecovery")
    def point_in_time_recovery(self) -> pulumi.Output['outputs.TablePointInTimeRecovery']:
        """
        Point-in-time recovery options.
        """
        return pulumi.get(self, "point_in_time_recovery")

    @property
    @pulumi.getter(name="rangeKey")
    def range_key(self) -> pulumi.Output[Optional[str]]:
        """
        The name of the range key; must be defined
        """
        return pulumi.get(self, "range_key")

    @property
    @pulumi.getter(name="readCapacity")
    def read_capacity(self) -> pulumi.Output[Optional[float]]:
        """
        The number of read units for this index. Must be set if billing_mode is set to PROVISIONED.
        """
        return pulumi.get(self, "read_capacity")

    @property
    @pulumi.getter
    def replicas(self) -> pulumi.Output[Optional[List['outputs.TableReplica']]]:
        """
        Configuration block(s) with [DynamoDB Global Tables V2 (version 2019.11.21)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/globaltables.V2.html) replication configurations. Detailed below.
        """
        return pulumi.get(self, "replicas")

    @property
    @pulumi.getter(name="serverSideEncryption")
    def server_side_encryption(self) -> pulumi.Output['outputs.TableServerSideEncryption']:
        """
        Encryption at rest options. AWS DynamoDB tables are automatically encrypted at rest with an AWS owned Customer Master Key if this argument isn't specified.
        """
        return pulumi.get(self, "server_side_encryption")

    @property
    @pulumi.getter(name="streamArn")
    def stream_arn(self) -> pulumi.Output[str]:
        """
        The ARN of the Table Stream. Only available when `stream_enabled = true`
        """
        return pulumi.get(self, "stream_arn")

    @property
    @pulumi.getter(name="streamEnabled")
    def stream_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether Streams are to be enabled (true) or disabled (false).
        """
        return pulumi.get(self, "stream_enabled")

    @property
    @pulumi.getter(name="streamLabel")
    def stream_label(self) -> pulumi.Output[str]:
        """
        A timestamp, in ISO 8601 format, for this stream. Note that this timestamp is not
        a unique identifier for the stream on its own. However, the combination of AWS customer ID,
        table name and this field is guaranteed to be unique.
        It can be used for creating CloudWatch Alarms. Only available when `stream_enabled = true`
        """
        return pulumi.get(self, "stream_label")

    @property
    @pulumi.getter(name="streamViewType")
    def stream_view_type(self) -> pulumi.Output[str]:
        """
        When an item in the table is modified, StreamViewType determines what information is written to the table's stream. Valid values are `KEYS_ONLY`, `NEW_IMAGE`, `OLD_IMAGE`, `NEW_AND_OLD_IMAGES`.
        """
        return pulumi.get(self, "stream_view_type")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to populate on the created table.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def ttl(self) -> pulumi.Output[Optional['outputs.TableTtl']]:
        """
        Defines ttl, has two properties, and can only be specified once:
        """
        return pulumi.get(self, "ttl")

    @property
    @pulumi.getter(name="writeCapacity")
    def write_capacity(self) -> pulumi.Output[Optional[float]]:
        """
        The number of write units for this index. Must be set if billing_mode is set to PROVISIONED.
        """
        return pulumi.get(self, "write_capacity")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

