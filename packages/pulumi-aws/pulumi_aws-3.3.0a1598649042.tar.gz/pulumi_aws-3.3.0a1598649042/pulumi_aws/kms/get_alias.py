# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'GetAliasResult',
    'AwaitableGetAliasResult',
    'get_alias',
]

@pulumi.output_type
class GetAliasResult:
    """
    A collection of values returned by getAlias.
    """
    def __init__(__self__, arn=None, id=None, name=None, target_key_arn=None, target_key_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if target_key_arn and not isinstance(target_key_arn, str):
            raise TypeError("Expected argument 'target_key_arn' to be a str")
        pulumi.set(__self__, "target_key_arn", target_key_arn)
        if target_key_id and not isinstance(target_key_id, str):
            raise TypeError("Expected argument 'target_key_id' to be a str")
        pulumi.set(__self__, "target_key_id", target_key_id)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Amazon Resource Name(ARN) of the key alias.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="targetKeyArn")
    def target_key_arn(self) -> str:
        """
        ARN pointed to by the alias.
        """
        return pulumi.get(self, "target_key_arn")

    @property
    @pulumi.getter(name="targetKeyId")
    def target_key_id(self) -> str:
        """
        Key identifier pointed to by the alias.
        """
        return pulumi.get(self, "target_key_id")


class AwaitableGetAliasResult(GetAliasResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAliasResult(
            arn=self.arn,
            id=self.id,
            name=self.name,
            target_key_arn=self.target_key_arn,
            target_key_id=self.target_key_id)


def get_alias(name: Optional[str] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAliasResult:
    """
    Use this data source to get the ARN of a KMS key alias.
    By using this data source, you can reference key alias
    without having to hard code the ARN as input.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    s3 = aws.kms.get_alias(name="alias/aws/s3")
    ```


    :param str name: The display name of the alias. The name must start with the word "alias" followed by a forward slash (alias/)
    """
    __args__ = dict()
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:kms/getAlias:getAlias', __args__, opts=opts, typ=GetAliasResult).value

    return AwaitableGetAliasResult(
        arn=__ret__.arn,
        id=__ret__.id,
        name=__ret__.name,
        target_key_arn=__ret__.target_key_arn,
        target_key_id=__ret__.target_key_id)
