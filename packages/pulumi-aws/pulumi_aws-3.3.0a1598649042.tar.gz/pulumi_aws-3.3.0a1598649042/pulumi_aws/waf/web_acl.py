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

__all__ = ['WebAcl']


class WebAcl(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 default_action: Optional[pulumi.Input[pulumi.InputType['WebAclDefaultActionArgs']]] = None,
                 logging_configuration: Optional[pulumi.Input[pulumi.InputType['WebAclLoggingConfigurationArgs']]] = None,
                 metric_name: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 rules: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['WebAclRuleArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a WAF Web ACL Resource

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        ipset = aws.waf.IpSet("ipset", ip_set_descriptors=[aws.waf.IpSetIpSetDescriptorArgs(
            type="IPV4",
            value="192.0.7.0/24",
        )])
        wafrule = aws.waf.Rule("wafrule",
            metric_name="tfWAFRule",
            predicates=[aws.waf.RulePredicateArgs(
                data_id=ipset.id,
                negated=False,
                type="IPMatch",
            )],
            opts=ResourceOptions(depends_on=[ipset]))
        waf_acl = aws.waf.WebAcl("wafAcl",
            metric_name="tfWebACL",
            default_action=aws.waf.WebAclDefaultActionArgs(
                type="ALLOW",
            ),
            rules=[aws.waf.WebAclRuleArgs(
                action=aws.waf.WebAclRuleActionArgs(
                    type="BLOCK",
                ),
                priority=1,
                rule_id=wafrule.id,
                type="REGULAR",
            )],
            opts=ResourceOptions(depends_on=[
                    ipset,
                    wafrule,
                ]))
        ```
        ### Logging

        > *NOTE:* The Kinesis Firehose Delivery Stream name must begin with `aws-waf-logs-` and be located in `us-east-1` region. See the [AWS WAF Developer Guide](https://docs.aws.amazon.com/waf/latest/developerguide/logging.html) for more information about enabling WAF logging.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.waf.WebAcl("example", logging_configuration=aws.waf.WebAclLoggingConfigurationArgs(
            log_destination=aws_kinesis_firehose_delivery_stream["example"]["arn"],
            redacted_fields={
                "fieldToMatches": [
                    {
                        "type": "URI",
                    },
                    {
                        "data": "referer",
                        "type": "HEADER",
                    },
                ],
            },
        ))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['WebAclDefaultActionArgs']] default_action: Configuration block with action that you want AWS WAF to take when a request doesn't match the criteria in any of the rules that are associated with the web ACL. Detailed below.
        :param pulumi.Input[pulumi.InputType['WebAclLoggingConfigurationArgs']] logging_configuration: Configuration block to enable WAF logging. Detailed below.
        :param pulumi.Input[str] metric_name: The name or description for the Amazon CloudWatch metric of this web ACL.
        :param pulumi.Input[str] name: The name or description of the web ACL.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['WebAclRuleArgs']]]] rules: Configuration blocks containing rules to associate with the web ACL and the settings for each rule. Detailed below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags
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

            if default_action is None:
                raise TypeError("Missing required property 'default_action'")
            __props__['default_action'] = default_action
            __props__['logging_configuration'] = logging_configuration
            if metric_name is None:
                raise TypeError("Missing required property 'metric_name'")
            __props__['metric_name'] = metric_name
            __props__['name'] = name
            __props__['rules'] = rules
            __props__['tags'] = tags
            __props__['arn'] = None
        super(WebAcl, __self__).__init__(
            'aws:waf/webAcl:WebAcl',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            default_action: Optional[pulumi.Input[pulumi.InputType['WebAclDefaultActionArgs']]] = None,
            logging_configuration: Optional[pulumi.Input[pulumi.InputType['WebAclLoggingConfigurationArgs']]] = None,
            metric_name: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            rules: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['WebAclRuleArgs']]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'WebAcl':
        """
        Get an existing WebAcl resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the WAF WebACL.
        :param pulumi.Input[pulumi.InputType['WebAclDefaultActionArgs']] default_action: Configuration block with action that you want AWS WAF to take when a request doesn't match the criteria in any of the rules that are associated with the web ACL. Detailed below.
        :param pulumi.Input[pulumi.InputType['WebAclLoggingConfigurationArgs']] logging_configuration: Configuration block to enable WAF logging. Detailed below.
        :param pulumi.Input[str] metric_name: The name or description for the Amazon CloudWatch metric of this web ACL.
        :param pulumi.Input[str] name: The name or description of the web ACL.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['WebAclRuleArgs']]]] rules: Configuration blocks containing rules to associate with the web ACL and the settings for each rule. Detailed below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value map of resource tags
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["default_action"] = default_action
        __props__["logging_configuration"] = logging_configuration
        __props__["metric_name"] = metric_name
        __props__["name"] = name
        __props__["rules"] = rules
        __props__["tags"] = tags
        return WebAcl(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the WAF WebACL.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="defaultAction")
    def default_action(self) -> pulumi.Output['outputs.WebAclDefaultAction']:
        """
        Configuration block with action that you want AWS WAF to take when a request doesn't match the criteria in any of the rules that are associated with the web ACL. Detailed below.
        """
        return pulumi.get(self, "default_action")

    @property
    @pulumi.getter(name="loggingConfiguration")
    def logging_configuration(self) -> pulumi.Output[Optional['outputs.WebAclLoggingConfiguration']]:
        """
        Configuration block to enable WAF logging. Detailed below.
        """
        return pulumi.get(self, "logging_configuration")

    @property
    @pulumi.getter(name="metricName")
    def metric_name(self) -> pulumi.Output[str]:
        """
        The name or description for the Amazon CloudWatch metric of this web ACL.
        """
        return pulumi.get(self, "metric_name")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name or description of the web ACL.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def rules(self) -> pulumi.Output[Optional[List['outputs.WebAclRule']]]:
        """
        Configuration blocks containing rules to associate with the web ACL and the settings for each rule. Detailed below.
        """
        return pulumi.get(self, "rules")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value map of resource tags
        """
        return pulumi.get(self, "tags")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

