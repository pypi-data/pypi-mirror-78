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

__all__ = ['SqlInjectionMatchSet']


class SqlInjectionMatchSet(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 sql_injection_match_tuples: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['SqlInjectionMatchSetSqlInjectionMatchTupleArgs']]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a WAF Regional SQL Injection Match Set Resource for use with Application Load Balancer.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        sql_injection_match_set = aws.wafregional.SqlInjectionMatchSet("sqlInjectionMatchSet", sql_injection_match_tuples=[aws.wafregional.SqlInjectionMatchSetSqlInjectionMatchTupleArgs(
            field_to_match=aws.wafregional.SqlInjectionMatchSetSqlInjectionMatchTupleFieldToMatchArgs(
                type="QUERY_STRING",
            ),
            text_transformation="URL_DECODE",
        )])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name or description of the SizeConstraintSet.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['SqlInjectionMatchSetSqlInjectionMatchTupleArgs']]]] sql_injection_match_tuples: The parts of web requests that you want AWS WAF to inspect for malicious SQL code and, if you want AWS WAF to inspect a header, the name of the header.
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

            __props__['name'] = name
            __props__['sql_injection_match_tuples'] = sql_injection_match_tuples
        super(SqlInjectionMatchSet, __self__).__init__(
            'aws:wafregional/sqlInjectionMatchSet:SqlInjectionMatchSet',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            name: Optional[pulumi.Input[str]] = None,
            sql_injection_match_tuples: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['SqlInjectionMatchSetSqlInjectionMatchTupleArgs']]]]] = None) -> 'SqlInjectionMatchSet':
        """
        Get an existing SqlInjectionMatchSet resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] name: The name or description of the SizeConstraintSet.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['SqlInjectionMatchSetSqlInjectionMatchTupleArgs']]]] sql_injection_match_tuples: The parts of web requests that you want AWS WAF to inspect for malicious SQL code and, if you want AWS WAF to inspect a header, the name of the header.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["name"] = name
        __props__["sql_injection_match_tuples"] = sql_injection_match_tuples
        return SqlInjectionMatchSet(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name or description of the SizeConstraintSet.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="sqlInjectionMatchTuples")
    def sql_injection_match_tuples(self) -> pulumi.Output[Optional[List['outputs.SqlInjectionMatchSetSqlInjectionMatchTuple']]]:
        """
        The parts of web requests that you want AWS WAF to inspect for malicious SQL code and, if you want AWS WAF to inspect a header, the name of the header.
        """
        return pulumi.get(self, "sql_injection_match_tuples")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

