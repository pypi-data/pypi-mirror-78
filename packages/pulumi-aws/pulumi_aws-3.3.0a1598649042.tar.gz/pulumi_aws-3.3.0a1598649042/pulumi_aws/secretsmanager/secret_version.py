# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = ['SecretVersion']


class SecretVersion(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 secret_binary: Optional[pulumi.Input[str]] = None,
                 secret_id: Optional[pulumi.Input[str]] = None,
                 secret_string: Optional[pulumi.Input[str]] = None,
                 version_stages: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a resource to manage AWS Secrets Manager secret version including its secret value. To manage secret metadata, see the `secretsmanager.Secret` resource.

        > **NOTE:** If the `AWSCURRENT` staging label is present on this version during resource deletion, that label cannot be removed and will be skipped to prevent errors when fully deleting the secret. That label will leave this secret version active even after the resource is deleted from this provider unless the secret itself is deleted. Move the `AWSCURRENT` staging label before or after deleting this resource from this provider to fully trigger version deprecation if necessary.

        ## Example Usage
        ### Simple String Value

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.secretsmanager.SecretVersion("example",
            secret_id=aws_secretsmanager_secret["example"]["id"],
            secret_string="example-string-to-protect")
        ```
        ### Key-Value Pairs

        Secrets Manager also accepts key-value pairs in JSON.

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        config = pulumi.Config()
        example = config.get_object("example")
        if example is None:
            example = {
                "key1": "value1",
                "key2": "value2",
            }
        example_secret_version = aws.secretsmanager.SecretVersion("exampleSecretVersion",
            secret_id=aws_secretsmanager_secret["example"]["id"],
            secret_string=json.dumps(example))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] secret_binary: Specifies binary data that you want to encrypt and store in this version of the secret. This is required if secret_string is not set. Needs to be encoded to base64.
        :param pulumi.Input[str] secret_id: Specifies the secret to which you want to add a new version. You can specify either the Amazon Resource Name (ARN) or the friendly name of the secret. The secret must already exist.
        :param pulumi.Input[str] secret_string: Specifies text data that you want to encrypt and store in this version of the secret. This is required if secret_binary is not set.
        :param pulumi.Input[List[pulumi.Input[str]]] version_stages: Specifies a list of staging labels that are attached to this version of the secret. A staging label must be unique to a single version of the secret. If you specify a staging label that's already associated with a different version of the same secret then that staging label is automatically removed from the other version and attached to this version. If you do not specify a value, then AWS Secrets Manager automatically moves the staging label `AWSCURRENT` to this new version on creation.
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

            __props__['secret_binary'] = secret_binary
            if secret_id is None:
                raise TypeError("Missing required property 'secret_id'")
            __props__['secret_id'] = secret_id
            __props__['secret_string'] = secret_string
            __props__['version_stages'] = version_stages
            __props__['arn'] = None
            __props__['version_id'] = None
        super(SecretVersion, __self__).__init__(
            'aws:secretsmanager/secretVersion:SecretVersion',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            secret_binary: Optional[pulumi.Input[str]] = None,
            secret_id: Optional[pulumi.Input[str]] = None,
            secret_string: Optional[pulumi.Input[str]] = None,
            version_id: Optional[pulumi.Input[str]] = None,
            version_stages: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None) -> 'SecretVersion':
        """
        Get an existing SecretVersion resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the secret.
        :param pulumi.Input[str] secret_binary: Specifies binary data that you want to encrypt and store in this version of the secret. This is required if secret_string is not set. Needs to be encoded to base64.
        :param pulumi.Input[str] secret_id: Specifies the secret to which you want to add a new version. You can specify either the Amazon Resource Name (ARN) or the friendly name of the secret. The secret must already exist.
        :param pulumi.Input[str] secret_string: Specifies text data that you want to encrypt and store in this version of the secret. This is required if secret_binary is not set.
        :param pulumi.Input[str] version_id: The unique identifier of the version of the secret.
        :param pulumi.Input[List[pulumi.Input[str]]] version_stages: Specifies a list of staging labels that are attached to this version of the secret. A staging label must be unique to a single version of the secret. If you specify a staging label that's already associated with a different version of the same secret then that staging label is automatically removed from the other version and attached to this version. If you do not specify a value, then AWS Secrets Manager automatically moves the staging label `AWSCURRENT` to this new version on creation.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["secret_binary"] = secret_binary
        __props__["secret_id"] = secret_id
        __props__["secret_string"] = secret_string
        __props__["version_id"] = version_id
        __props__["version_stages"] = version_stages
        return SecretVersion(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the secret.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="secretBinary")
    def secret_binary(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies binary data that you want to encrypt and store in this version of the secret. This is required if secret_string is not set. Needs to be encoded to base64.
        """
        return pulumi.get(self, "secret_binary")

    @property
    @pulumi.getter(name="secretId")
    def secret_id(self) -> pulumi.Output[str]:
        """
        Specifies the secret to which you want to add a new version. You can specify either the Amazon Resource Name (ARN) or the friendly name of the secret. The secret must already exist.
        """
        return pulumi.get(self, "secret_id")

    @property
    @pulumi.getter(name="secretString")
    def secret_string(self) -> pulumi.Output[Optional[str]]:
        """
        Specifies text data that you want to encrypt and store in this version of the secret. This is required if secret_binary is not set.
        """
        return pulumi.get(self, "secret_string")

    @property
    @pulumi.getter(name="versionId")
    def version_id(self) -> pulumi.Output[str]:
        """
        The unique identifier of the version of the secret.
        """
        return pulumi.get(self, "version_id")

    @property
    @pulumi.getter(name="versionStages")
    def version_stages(self) -> pulumi.Output[List[str]]:
        """
        Specifies a list of staging labels that are attached to this version of the secret. A staging label must be unique to a single version of the secret. If you specify a staging label that's already associated with a different version of the same secret then that staging label is automatically removed from the other version and attached to this version. If you do not specify a value, then AWS Secrets Manager automatically moves the staging label `AWSCURRENT` to this new version on creation.
        """
        return pulumi.get(self, "version_stages")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

