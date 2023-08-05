# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['PolicyAttachment']


class PolicyAttachment(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 target: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an IoT policy attachment.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        pubsub = aws.iot.Policy("pubsub", policy=\"\"\"{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Action": [
                "iot:*"
              ],
              "Effect": "Allow",
              "Resource": "*"
            }
          ]
        }
        \"\"\")
        cert = aws.iot.Certificate("cert",
            csr=(lambda path: open(path).read())("csr.pem"),
            active=True)
        att = aws.iot.PolicyAttachment("att",
            policy=pubsub.name,
            target=cert.arn)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy: The name of the policy to attach.
        :param pulumi.Input[str] target: The identity to which the policy is attached.
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

            if policy is None:
                raise TypeError("Missing required property 'policy'")
            __props__['policy'] = policy
            if target is None:
                raise TypeError("Missing required property 'target'")
            __props__['target'] = target
        super(PolicyAttachment, __self__).__init__(
            'aws:iot/policyAttachment:PolicyAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            policy: Optional[pulumi.Input[str]] = None,
            target: Optional[pulumi.Input[str]] = None) -> 'PolicyAttachment':
        """
        Get an existing PolicyAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] policy: The name of the policy to attach.
        :param pulumi.Input[str] target: The identity to which the policy is attached.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["policy"] = policy
        __props__["target"] = target
        return PolicyAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[str]:
        """
        The name of the policy to attach.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter
    def target(self) -> pulumi.Output[str]:
        """
        The identity to which the policy is attached.
        """
        return pulumi.get(self, "target")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

