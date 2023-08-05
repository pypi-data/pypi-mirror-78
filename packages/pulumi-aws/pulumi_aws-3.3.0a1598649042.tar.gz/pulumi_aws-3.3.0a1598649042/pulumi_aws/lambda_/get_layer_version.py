# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'GetLayerVersionResult',
    'AwaitableGetLayerVersionResult',
    'get_layer_version',
]

@pulumi.output_type
class GetLayerVersionResult:
    """
    A collection of values returned by getLayerVersion.
    """
    def __init__(__self__, arn=None, compatible_runtime=None, compatible_runtimes=None, created_date=None, description=None, id=None, layer_arn=None, layer_name=None, license_info=None, source_code_hash=None, source_code_size=None, version=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if compatible_runtime and not isinstance(compatible_runtime, str):
            raise TypeError("Expected argument 'compatible_runtime' to be a str")
        pulumi.set(__self__, "compatible_runtime", compatible_runtime)
        if compatible_runtimes and not isinstance(compatible_runtimes, list):
            raise TypeError("Expected argument 'compatible_runtimes' to be a list")
        pulumi.set(__self__, "compatible_runtimes", compatible_runtimes)
        if created_date and not isinstance(created_date, str):
            raise TypeError("Expected argument 'created_date' to be a str")
        pulumi.set(__self__, "created_date", created_date)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if layer_arn and not isinstance(layer_arn, str):
            raise TypeError("Expected argument 'layer_arn' to be a str")
        pulumi.set(__self__, "layer_arn", layer_arn)
        if layer_name and not isinstance(layer_name, str):
            raise TypeError("Expected argument 'layer_name' to be a str")
        pulumi.set(__self__, "layer_name", layer_name)
        if license_info and not isinstance(license_info, str):
            raise TypeError("Expected argument 'license_info' to be a str")
        pulumi.set(__self__, "license_info", license_info)
        if source_code_hash and not isinstance(source_code_hash, str):
            raise TypeError("Expected argument 'source_code_hash' to be a str")
        pulumi.set(__self__, "source_code_hash", source_code_hash)
        if source_code_size and not isinstance(source_code_size, float):
            raise TypeError("Expected argument 'source_code_size' to be a float")
        pulumi.set(__self__, "source_code_size", source_code_size)
        if version and not isinstance(version, float):
            raise TypeError("Expected argument 'version' to be a float")
        pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the Lambda Layer with version.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="compatibleRuntime")
    def compatible_runtime(self) -> Optional[str]:
        return pulumi.get(self, "compatible_runtime")

    @property
    @pulumi.getter(name="compatibleRuntimes")
    def compatible_runtimes(self) -> List[str]:
        """
        A list of [Runtimes](https://docs.aws.amazon.com/lambda/latest/dg/API_GetLayerVersion.html#SSS-GetLayerVersion-response-CompatibleRuntimes) the specific Lambda Layer version is compatible with.
        """
        return pulumi.get(self, "compatible_runtimes")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> str:
        """
        The date this resource was created.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the specific Lambda Layer version.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="layerArn")
    def layer_arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the Lambda Layer without version.
        """
        return pulumi.get(self, "layer_arn")

    @property
    @pulumi.getter(name="layerName")
    def layer_name(self) -> str:
        return pulumi.get(self, "layer_name")

    @property
    @pulumi.getter(name="licenseInfo")
    def license_info(self) -> str:
        """
        License info associated with the specific Lambda Layer version.
        """
        return pulumi.get(self, "license_info")

    @property
    @pulumi.getter(name="sourceCodeHash")
    def source_code_hash(self) -> str:
        """
        Base64-encoded representation of raw SHA-256 sum of the zip file.
        """
        return pulumi.get(self, "source_code_hash")

    @property
    @pulumi.getter(name="sourceCodeSize")
    def source_code_size(self) -> float:
        """
        The size in bytes of the function .zip file.
        """
        return pulumi.get(self, "source_code_size")

    @property
    @pulumi.getter
    def version(self) -> float:
        """
        This Lamba Layer version.
        """
        return pulumi.get(self, "version")


class AwaitableGetLayerVersionResult(GetLayerVersionResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLayerVersionResult(
            arn=self.arn,
            compatible_runtime=self.compatible_runtime,
            compatible_runtimes=self.compatible_runtimes,
            created_date=self.created_date,
            description=self.description,
            id=self.id,
            layer_arn=self.layer_arn,
            layer_name=self.layer_name,
            license_info=self.license_info,
            source_code_hash=self.source_code_hash,
            source_code_size=self.source_code_size,
            version=self.version)


def get_layer_version(compatible_runtime: Optional[str] = None,
                      layer_name: Optional[str] = None,
                      version: Optional[float] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLayerVersionResult:
    """
    Provides information about a Lambda Layer Version.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    config = pulumi.Config()
    layer_name = config.require("layerName")
    existing = aws.lambda.get_layer_version(layer_name=layer_name)
    ```


    :param str compatible_runtime: Specific runtime the layer version must support. Conflicts with `version`. If specified, the latest available layer version supporting the provided runtime will be used.
    :param str layer_name: Name of the lambda layer.
    :param float version: Specific layer version. Conflicts with `compatible_runtime`. If omitted, the latest available layer version will be used.
    """
    __args__ = dict()
    __args__['compatibleRuntime'] = compatible_runtime
    __args__['layerName'] = layer_name
    __args__['version'] = version
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:lambda/getLayerVersion:getLayerVersion', __args__, opts=opts, typ=GetLayerVersionResult).value

    return AwaitableGetLayerVersionResult(
        arn=__ret__.arn,
        compatible_runtime=__ret__.compatible_runtime,
        compatible_runtimes=__ret__.compatible_runtimes,
        created_date=__ret__.created_date,
        description=__ret__.description,
        id=__ret__.id,
        layer_arn=__ret__.layer_arn,
        layer_name=__ret__.layer_name,
        license_info=__ret__.license_info,
        source_code_hash=__ret__.source_code_hash,
        source_code_size=__ret__.source_code_size,
        version=__ret__.version)
