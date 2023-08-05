# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['IdentityNotificationTopic']


class IdentityNotificationTopic(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 identity: Optional[pulumi.Input[str]] = None,
                 include_original_headers: Optional[pulumi.Input[bool]] = None,
                 notification_type: Optional[pulumi.Input[str]] = None,
                 topic_arn: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Resource for managing SES Identity Notification Topics

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        test = aws.ses.IdentityNotificationTopic("test",
            identity=aws_ses_domain_identity["example"]["domain"],
            include_original_headers=True,
            notification_type="Bounce",
            topic_arn=aws_sns_topic["example"]["arn"])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] identity: The identity for which the Amazon SNS topic will be set. You can specify an identity by using its name or by using its Amazon Resource Name (ARN).
        :param pulumi.Input[bool] include_original_headers: Whether SES should include original email headers in SNS notifications of this type. *false* by default.
        :param pulumi.Input[str] notification_type: The type of notifications that will be published to the specified Amazon SNS topic. Valid Values: *Bounce*, *Complaint* or *Delivery*.
        :param pulumi.Input[str] topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic. Can be set to "" (an empty string) to disable publishing.
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

            if identity is None:
                raise TypeError("Missing required property 'identity'")
            __props__['identity'] = identity
            __props__['include_original_headers'] = include_original_headers
            if notification_type is None:
                raise TypeError("Missing required property 'notification_type'")
            __props__['notification_type'] = notification_type
            __props__['topic_arn'] = topic_arn
        super(IdentityNotificationTopic, __self__).__init__(
            'aws:ses/identityNotificationTopic:IdentityNotificationTopic',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            identity: Optional[pulumi.Input[str]] = None,
            include_original_headers: Optional[pulumi.Input[bool]] = None,
            notification_type: Optional[pulumi.Input[str]] = None,
            topic_arn: Optional[pulumi.Input[str]] = None) -> 'IdentityNotificationTopic':
        """
        Get an existing IdentityNotificationTopic resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] identity: The identity for which the Amazon SNS topic will be set. You can specify an identity by using its name or by using its Amazon Resource Name (ARN).
        :param pulumi.Input[bool] include_original_headers: Whether SES should include original email headers in SNS notifications of this type. *false* by default.
        :param pulumi.Input[str] notification_type: The type of notifications that will be published to the specified Amazon SNS topic. Valid Values: *Bounce*, *Complaint* or *Delivery*.
        :param pulumi.Input[str] topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic. Can be set to "" (an empty string) to disable publishing.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["identity"] = identity
        __props__["include_original_headers"] = include_original_headers
        __props__["notification_type"] = notification_type
        __props__["topic_arn"] = topic_arn
        return IdentityNotificationTopic(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def identity(self) -> pulumi.Output[str]:
        """
        The identity for which the Amazon SNS topic will be set. You can specify an identity by using its name or by using its Amazon Resource Name (ARN).
        """
        return pulumi.get(self, "identity")

    @property
    @pulumi.getter(name="includeOriginalHeaders")
    def include_original_headers(self) -> pulumi.Output[Optional[bool]]:
        """
        Whether SES should include original email headers in SNS notifications of this type. *false* by default.
        """
        return pulumi.get(self, "include_original_headers")

    @property
    @pulumi.getter(name="notificationType")
    def notification_type(self) -> pulumi.Output[str]:
        """
        The type of notifications that will be published to the specified Amazon SNS topic. Valid Values: *Bounce*, *Complaint* or *Delivery*.
        """
        return pulumi.get(self, "notification_type")

    @property
    @pulumi.getter(name="topicArn")
    def topic_arn(self) -> pulumi.Output[Optional[str]]:
        """
        The Amazon Resource Name (ARN) of the Amazon SNS topic. Can be set to "" (an empty string) to disable publishing.
        """
        return pulumi.get(self, "topic_arn")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

