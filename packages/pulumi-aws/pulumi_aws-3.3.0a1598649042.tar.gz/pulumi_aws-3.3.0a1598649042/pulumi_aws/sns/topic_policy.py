# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['TopicPolicy']


class TopicPolicy(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 arn: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an SNS topic policy resource

        > **NOTE:** If a Principal is specified as just an AWS account ID rather than an ARN, AWS silently converts it to the ARN for the root user, causing future deployments to differ. To avoid this problem, just specify the full ARN, e.g. `arn:aws:iam::123456789012:root`

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.sns.Topic("test")
        sns_topic_policy = test.arn.apply(lambda arn: aws.iam.get_policy_document(policy_id="__default_policy_ID",
            statements=[aws.iam.GetPolicyDocumentStatementArgs(
                actions=[
                    "SNS:Subscribe",
                    "SNS:SetTopicAttributes",
                    "SNS:RemovePermission",
                    "SNS:Receive",
                    "SNS:Publish",
                    "SNS:ListSubscriptionsByTopic",
                    "SNS:GetTopicAttributes",
                    "SNS:DeleteTopic",
                    "SNS:AddPermission",
                ],
                conditions=[aws.iam.GetPolicyDocumentStatementConditionArgs(
                    test="StringEquals",
                    variable="AWS:SourceOwner",
                    values=[var["account-id"]],
                )],
                effect="Allow",
                principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    type="AWS",
                    identifiers=["*"],
                )],
                resources=[arn],
                sid="__default_statement_ID",
            )]))
        default = aws.sns.TopicPolicy("default",
            arn=test.arn,
            policy=sns_topic_policy.json)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the SNS topic
        :param pulumi.Input[str] policy: The fully-formed AWS policy as JSON.
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

            if arn is None:
                raise TypeError("Missing required property 'arn'")
            __props__['arn'] = arn
            if policy is None:
                raise TypeError("Missing required property 'policy'")
            __props__['policy'] = policy
        super(TopicPolicy, __self__).__init__(
            'aws:sns/topicPolicy:TopicPolicy',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            policy: Optional[pulumi.Input[str]] = None) -> 'TopicPolicy':
        """
        Get an existing TopicPolicy resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the SNS topic
        :param pulumi.Input[str] policy: The fully-formed AWS policy as JSON.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["policy"] = policy
        return TopicPolicy(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the SNS topic
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        The fully-formed AWS policy as JSON.
        """
        return pulumi.get(self, "policy")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

