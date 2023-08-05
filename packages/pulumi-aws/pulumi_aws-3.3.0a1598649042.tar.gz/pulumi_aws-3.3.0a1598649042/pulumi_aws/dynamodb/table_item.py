# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['TableItem']


class TableItem(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 hash_key: Optional[pulumi.Input[str]] = None,
                 item: Optional[pulumi.Input[str]] = None,
                 range_key: Optional[pulumi.Input[str]] = None,
                 table_name: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a DynamoDB table item resource

        > **Note:** This resource is not meant to be used for managing large amounts of data in your table, it is not designed to scale.
          You should perform **regular backups** of all data in the table, see [AWS docs for more](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BackupRestore.html).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example_table = aws.dynamodb.Table("exampleTable",
            read_capacity=10,
            write_capacity=10,
            hash_key="exampleHashKey",
            attributes=[aws.dynamodb.TableAttributeArgs(
                name="exampleHashKey",
                type="S",
            )])
        example_table_item = aws.dynamodb.TableItem("exampleTableItem",
            table_name=example_table.name,
            hash_key=example_table.hash_key,
            item=\"\"\"{
          "exampleHashKey": {"S": "something"},
          "one": {"N": "11111"},
          "two": {"N": "22222"},
          "three": {"N": "33333"},
          "four": {"N": "44444"}
        }
        \"\"\")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] hash_key: Hash key to use for lookups and identification of the item
        :param pulumi.Input[str] item: JSON representation of a map of attribute name/value pairs, one for each attribute.
               Only the primary key attributes are required; you can optionally provide other attribute name-value pairs for the item.
        :param pulumi.Input[str] range_key: Range key to use for lookups and identification of the item. Required if there is range key defined in the table.
        :param pulumi.Input[str] table_name: The name of the table to contain the item.
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

            if hash_key is None:
                raise TypeError("Missing required property 'hash_key'")
            __props__['hash_key'] = hash_key
            if item is None:
                raise TypeError("Missing required property 'item'")
            __props__['item'] = item
            __props__['range_key'] = range_key
            if table_name is None:
                raise TypeError("Missing required property 'table_name'")
            __props__['table_name'] = table_name
        super(TableItem, __self__).__init__(
            'aws:dynamodb/tableItem:TableItem',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            hash_key: Optional[pulumi.Input[str]] = None,
            item: Optional[pulumi.Input[str]] = None,
            range_key: Optional[pulumi.Input[str]] = None,
            table_name: Optional[pulumi.Input[str]] = None) -> 'TableItem':
        """
        Get an existing TableItem resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] hash_key: Hash key to use for lookups and identification of the item
        :param pulumi.Input[str] item: JSON representation of a map of attribute name/value pairs, one for each attribute.
               Only the primary key attributes are required; you can optionally provide other attribute name-value pairs for the item.
        :param pulumi.Input[str] range_key: Range key to use for lookups and identification of the item. Required if there is range key defined in the table.
        :param pulumi.Input[str] table_name: The name of the table to contain the item.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["hash_key"] = hash_key
        __props__["item"] = item
        __props__["range_key"] = range_key
        __props__["table_name"] = table_name
        return TableItem(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="hashKey")
    def hash_key(self) -> pulumi.Output[str]:
        """
        Hash key to use for lookups and identification of the item
        """
        return pulumi.get(self, "hash_key")

    @property
    @pulumi.getter
    def item(self) -> pulumi.Output[str]:
        """
        JSON representation of a map of attribute name/value pairs, one for each attribute.
        Only the primary key attributes are required; you can optionally provide other attribute name-value pairs for the item.
        """
        return pulumi.get(self, "item")

    @property
    @pulumi.getter(name="rangeKey")
    def range_key(self) -> pulumi.Output[Optional[str]]:
        """
        Range key to use for lookups and identification of the item. Required if there is range key defined in the table.
        """
        return pulumi.get(self, "range_key")

    @property
    @pulumi.getter(name="tableName")
    def table_name(self) -> pulumi.Output[str]:
        """
        The name of the table to contain the item.
        """
        return pulumi.get(self, "table_name")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

