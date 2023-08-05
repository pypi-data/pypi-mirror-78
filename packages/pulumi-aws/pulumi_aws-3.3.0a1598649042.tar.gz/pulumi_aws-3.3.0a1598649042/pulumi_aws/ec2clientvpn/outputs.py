# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'EndpointAuthenticationOption',
    'EndpointConnectionLogOptions',
]

@pulumi.output_type
class EndpointAuthenticationOption(dict):
    def __init__(__self__, *,
                 type: str,
                 active_directory_id: Optional[str] = None,
                 root_certificate_chain_arn: Optional[str] = None):
        """
        :param str type: The type of client authentication to be used. Specify `certificate-authentication` to use certificate-based authentication, or `directory-service-authentication` to use Active Directory authentication.
        :param str active_directory_id: The ID of the Active Directory to be used for authentication if type is `directory-service-authentication`.
        :param str root_certificate_chain_arn: The ARN of the client certificate. The certificate must be signed by a certificate authority (CA) and it must be provisioned in AWS Certificate Manager (ACM). Only necessary when type is set to `certificate-authentication`.
        """
        pulumi.set(__self__, "type", type)
        if active_directory_id is not None:
            pulumi.set(__self__, "active_directory_id", active_directory_id)
        if root_certificate_chain_arn is not None:
            pulumi.set(__self__, "root_certificate_chain_arn", root_certificate_chain_arn)

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The type of client authentication to be used. Specify `certificate-authentication` to use certificate-based authentication, or `directory-service-authentication` to use Active Directory authentication.
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter(name="activeDirectoryId")
    def active_directory_id(self) -> Optional[str]:
        """
        The ID of the Active Directory to be used for authentication if type is `directory-service-authentication`.
        """
        return pulumi.get(self, "active_directory_id")

    @property
    @pulumi.getter(name="rootCertificateChainArn")
    def root_certificate_chain_arn(self) -> Optional[str]:
        """
        The ARN of the client certificate. The certificate must be signed by a certificate authority (CA) and it must be provisioned in AWS Certificate Manager (ACM). Only necessary when type is set to `certificate-authentication`.
        """
        return pulumi.get(self, "root_certificate_chain_arn")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


@pulumi.output_type
class EndpointConnectionLogOptions(dict):
    def __init__(__self__, *,
                 enabled: bool,
                 cloudwatch_log_group: Optional[str] = None,
                 cloudwatch_log_stream: Optional[str] = None):
        """
        :param bool enabled: Indicates whether connection logging is enabled.
        :param str cloudwatch_log_group: The name of the CloudWatch Logs log group.
        :param str cloudwatch_log_stream: The name of the CloudWatch Logs log stream to which the connection data is published.
        """
        pulumi.set(__self__, "enabled", enabled)
        if cloudwatch_log_group is not None:
            pulumi.set(__self__, "cloudwatch_log_group", cloudwatch_log_group)
        if cloudwatch_log_stream is not None:
            pulumi.set(__self__, "cloudwatch_log_stream", cloudwatch_log_stream)

    @property
    @pulumi.getter
    def enabled(self) -> bool:
        """
        Indicates whether connection logging is enabled.
        """
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter(name="cloudwatchLogGroup")
    def cloudwatch_log_group(self) -> Optional[str]:
        """
        The name of the CloudWatch Logs log group.
        """
        return pulumi.get(self, "cloudwatch_log_group")

    @property
    @pulumi.getter(name="cloudwatchLogStream")
    def cloudwatch_log_stream(self) -> Optional[str]:
        """
        The name of the CloudWatch Logs log stream to which the connection data is published.
        """
        return pulumi.get(self, "cloudwatch_log_stream")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


