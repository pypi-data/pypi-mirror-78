# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'GetResourceShareFilterArgs',
]

@pulumi.input_type
class GetResourceShareFilterArgs:
    def __init__(__self__, *,
                 name: str,
                 values: List[str]):
        """
        :param str name: The name of the tag key to filter on.
        :param List[str] values: The value of the tag key.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        The name of the tag key to filter on.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: str):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def values(self) -> List[str]:
        """
        The value of the tag key.
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: List[str]):
        pulumi.set(self, "values", value)


