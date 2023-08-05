# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'GroupResourceQuery',
]

@pulumi.output_type
class GroupResourceQuery(dict):
    def __init__(__self__, *,
                 query: str,
                 type: Optional[str] = None):
        """
        :param str query: The resource query as a JSON string.
        :param str type: The type of the resource query. Defaults to `TAG_FILTERS_1_0`.
        """
        pulumi.set(__self__, "query", query)
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def query(self) -> str:
        """
        The resource query as a JSON string.
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        """
        The type of the resource query. Defaults to `TAG_FILTERS_1_0`.
        """
        return pulumi.get(self, "type")

    def _translate_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop


