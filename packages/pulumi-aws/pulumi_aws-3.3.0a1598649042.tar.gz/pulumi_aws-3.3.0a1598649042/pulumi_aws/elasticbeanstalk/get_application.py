# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables
from . import outputs

__all__ = [
    'GetApplicationResult',
    'AwaitableGetApplicationResult',
    'get_application',
]

@pulumi.output_type
class GetApplicationResult:
    """
    A collection of values returned by getApplication.
    """
    def __init__(__self__, appversion_lifecycle=None, arn=None, description=None, id=None, name=None):
        if appversion_lifecycle and not isinstance(appversion_lifecycle, dict):
            raise TypeError("Expected argument 'appversion_lifecycle' to be a dict")
        pulumi.set(__self__, "appversion_lifecycle", appversion_lifecycle)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)

    @property
    @pulumi.getter(name="appversionLifecycle")
    def appversion_lifecycle(self) -> 'outputs.GetApplicationAppversionLifecycleResult':
        return pulumi.get(self, "appversion_lifecycle")

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        The Amazon Resource Name (ARN) of the application.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Short description of the application
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
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")


class AwaitableGetApplicationResult(GetApplicationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationResult(
            appversion_lifecycle=self.appversion_lifecycle,
            arn=self.arn,
            description=self.description,
            id=self.id,
            name=self.name)


def get_application(name: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetApplicationResult:
    """
    Retrieve information about an Elastic Beanstalk Application.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.elasticbeanstalk.get_application(name="example")
    pulumi.export("arn", example.arn)
    pulumi.export("description", example.description)
    ```


    :param str name: The name of the application
    """
    __args__ = dict()
    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:elasticbeanstalk/getApplication:getApplication', __args__, opts=opts, typ=GetApplicationResult).value

    return AwaitableGetApplicationResult(
        appversion_lifecycle=__ret__.appversion_lifecycle,
        arn=__ret__.arn,
        description=__ret__.description,
        id=__ret__.id,
        name=__ret__.name)
