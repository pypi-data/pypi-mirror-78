# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables
from . import outputs
from ._inputs import *

__all__ = ['Document']


class Document(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 attachments_sources: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DocumentAttachmentsSourceArgs']]]]] = None,
                 content: Optional[pulumi.Input[str]] = None,
                 document_format: Optional[pulumi.Input[str]] = None,
                 document_type: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 permissions: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 target_type: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides an SSM Document resource

        > **NOTE on updating SSM documents:** Only documents with a schema version of 2.0
        or greater can update their content once created, see [SSM Schema Features](http://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-ssm-docs.html#document-schemas-features). To update a document with an older
        schema version you must recreate the resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        foo = aws.ssm.Document("foo",
            content=\"\"\"  {
            "schemaVersion": "1.2",
            "description": "Check ip configuration of a Linux instance.",
            "parameters": {

            },
            "runtimeConfig": {
              "aws:runShellScript": {
                "properties": [
                  {
                    "id": "0.aws:runShellScript",
                    "runCommand": ["ifconfig"]
                  }
                ]
              }
            }
          }

        \"\"\",
            document_type="Command")
        ```
        ## Permissions

        The permissions attribute specifies how you want to share the document. If you share a document privately,
        you must specify the AWS user account IDs for those people who can use the document. If you share a document
        publicly, you must specify All as the account ID.

        The permissions mapping supports the following:

        * `type` - The permission type for the document. The permission type can be `Share`.
        * `account_ids` - The AWS user accounts that should have access to the document. The account IDs can either be a group of account IDs or `All`.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DocumentAttachmentsSourceArgs']]]] attachments_sources: One or more configuration blocks describing attachments sources to a version of a document. Defined below.
        :param pulumi.Input[str] content: The JSON or YAML content of the document.
        :param pulumi.Input[str] document_format: The format of the document. Valid document types include: `JSON` and `YAML`
        :param pulumi.Input[str] document_type: The type of the document. Valid document types include: `Automation`, `Command`, `Package`, `Policy`, and `Session`
        :param pulumi.Input[str] name: The name of the document.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] permissions: Additional Permissions to attach to the document. See Permissions below for details.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the object.
        :param pulumi.Input[str] target_type: The target type which defines the kinds of resources the document can run on. For example, /AWS::EC2::Instance. For a list of valid resource types, see AWS Resource Types Reference (http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)
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

            __props__['attachments_sources'] = attachments_sources
            if content is None:
                raise TypeError("Missing required property 'content'")
            __props__['content'] = content
            __props__['document_format'] = document_format
            if document_type is None:
                raise TypeError("Missing required property 'document_type'")
            __props__['document_type'] = document_type
            __props__['name'] = name
            __props__['permissions'] = permissions
            __props__['tags'] = tags
            __props__['target_type'] = target_type
            __props__['arn'] = None
            __props__['created_date'] = None
            __props__['default_version'] = None
            __props__['description'] = None
            __props__['document_version'] = None
            __props__['hash'] = None
            __props__['hash_type'] = None
            __props__['latest_version'] = None
            __props__['owner'] = None
            __props__['parameters'] = None
            __props__['platform_types'] = None
            __props__['schema_version'] = None
            __props__['status'] = None
        super(Document, __self__).__init__(
            'aws:ssm/document:Document',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            attachments_sources: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DocumentAttachmentsSourceArgs']]]]] = None,
            content: Optional[pulumi.Input[str]] = None,
            created_date: Optional[pulumi.Input[str]] = None,
            default_version: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            document_format: Optional[pulumi.Input[str]] = None,
            document_type: Optional[pulumi.Input[str]] = None,
            document_version: Optional[pulumi.Input[str]] = None,
            hash: Optional[pulumi.Input[str]] = None,
            hash_type: Optional[pulumi.Input[str]] = None,
            latest_version: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            owner: Optional[pulumi.Input[str]] = None,
            parameters: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['DocumentParameterArgs']]]]] = None,
            permissions: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            platform_types: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            schema_version: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            target_type: Optional[pulumi.Input[str]] = None) -> 'Document':
        """
        Get an existing Document resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DocumentAttachmentsSourceArgs']]]] attachments_sources: One or more configuration blocks describing attachments sources to a version of a document. Defined below.
        :param pulumi.Input[str] content: The JSON or YAML content of the document.
        :param pulumi.Input[str] created_date: The date the document was created.
        :param pulumi.Input[str] default_version: The default version of the document.
        :param pulumi.Input[str] description: The description of the document.
        :param pulumi.Input[str] document_format: The format of the document. Valid document types include: `JSON` and `YAML`
        :param pulumi.Input[str] document_type: The type of the document. Valid document types include: `Automation`, `Command`, `Package`, `Policy`, and `Session`
        :param pulumi.Input[str] document_version: The document version.
        :param pulumi.Input[str] hash: The sha1 or sha256 of the document content
        :param pulumi.Input[str] hash_type: "Sha1" "Sha256". The hashing algorithm used when hashing the content.
        :param pulumi.Input[str] latest_version: The latest version of the document.
        :param pulumi.Input[str] name: The name of the document.
        :param pulumi.Input[str] owner: The AWS user account of the person who created the document.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['DocumentParameterArgs']]]] parameters: The parameters that are available to this document.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] permissions: Additional Permissions to attach to the document. See Permissions below for details.
        :param pulumi.Input[List[pulumi.Input[str]]] platform_types: A list of OS platforms compatible with this SSM document, either "Windows" or "Linux".
        :param pulumi.Input[str] schema_version: The schema version of the document.
        :param pulumi.Input[str] status: "Creating", "Active" or "Deleting". The current status of the document.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the object.
        :param pulumi.Input[str] target_type: The target type which defines the kinds of resources the document can run on. For example, /AWS::EC2::Instance. For a list of valid resource types, see AWS Resource Types Reference (http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["attachments_sources"] = attachments_sources
        __props__["content"] = content
        __props__["created_date"] = created_date
        __props__["default_version"] = default_version
        __props__["description"] = description
        __props__["document_format"] = document_format
        __props__["document_type"] = document_type
        __props__["document_version"] = document_version
        __props__["hash"] = hash
        __props__["hash_type"] = hash_type
        __props__["latest_version"] = latest_version
        __props__["name"] = name
        __props__["owner"] = owner
        __props__["parameters"] = parameters
        __props__["permissions"] = permissions
        __props__["platform_types"] = platform_types
        __props__["schema_version"] = schema_version
        __props__["status"] = status
        __props__["tags"] = tags
        __props__["target_type"] = target_type
        return Document(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="attachmentsSources")
    def attachments_sources(self) -> pulumi.Output[Optional[List['outputs.DocumentAttachmentsSource']]]:
        """
        One or more configuration blocks describing attachments sources to a version of a document. Defined below.
        """
        return pulumi.get(self, "attachments_sources")

    @property
    @pulumi.getter
    def content(self) -> pulumi.Output[str]:
        """
        The JSON or YAML content of the document.
        """
        return pulumi.get(self, "content")

    @property
    @pulumi.getter(name="createdDate")
    def created_date(self) -> pulumi.Output[str]:
        """
        The date the document was created.
        """
        return pulumi.get(self, "created_date")

    @property
    @pulumi.getter(name="defaultVersion")
    def default_version(self) -> pulumi.Output[str]:
        """
        The default version of the document.
        """
        return pulumi.get(self, "default_version")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[str]:
        """
        The description of the document.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="documentFormat")
    def document_format(self) -> pulumi.Output[Optional[str]]:
        """
        The format of the document. Valid document types include: `JSON` and `YAML`
        """
        return pulumi.get(self, "document_format")

    @property
    @pulumi.getter(name="documentType")
    def document_type(self) -> pulumi.Output[str]:
        """
        The type of the document. Valid document types include: `Automation`, `Command`, `Package`, `Policy`, and `Session`
        """
        return pulumi.get(self, "document_type")

    @property
    @pulumi.getter(name="documentVersion")
    def document_version(self) -> pulumi.Output[str]:
        """
        The document version.
        """
        return pulumi.get(self, "document_version")

    @property
    @pulumi.getter
    def hash(self) -> pulumi.Output[str]:
        """
        The sha1 or sha256 of the document content
        """
        return pulumi.get(self, "hash")

    @property
    @pulumi.getter(name="hashType")
    def hash_type(self) -> pulumi.Output[str]:
        """
        "Sha1" "Sha256". The hashing algorithm used when hashing the content.
        """
        return pulumi.get(self, "hash_type")

    @property
    @pulumi.getter(name="latestVersion")
    def latest_version(self) -> pulumi.Output[str]:
        """
        The latest version of the document.
        """
        return pulumi.get(self, "latest_version")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the document.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def owner(self) -> pulumi.Output[str]:
        """
        The AWS user account of the person who created the document.
        """
        return pulumi.get(self, "owner")

    @property
    @pulumi.getter
    def parameters(self) -> pulumi.Output[List['outputs.DocumentParameter']]:
        """
        The parameters that are available to this document.
        """
        return pulumi.get(self, "parameters")

    @property
    @pulumi.getter
    def permissions(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Additional Permissions to attach to the document. See Permissions below for details.
        """
        return pulumi.get(self, "permissions")

    @property
    @pulumi.getter(name="platformTypes")
    def platform_types(self) -> pulumi.Output[List[str]]:
        """
        A list of OS platforms compatible with this SSM document, either "Windows" or "Linux".
        """
        return pulumi.get(self, "platform_types")

    @property
    @pulumi.getter(name="schemaVersion")
    def schema_version(self) -> pulumi.Output[str]:
        """
        The schema version of the document.
        """
        return pulumi.get(self, "schema_version")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        "Creating", "Active" or "Deleting". The current status of the document.
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the object.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="targetType")
    def target_type(self) -> pulumi.Output[Optional[str]]:
        """
        The target type which defines the kinds of resources the document can run on. For example, /AWS::EC2::Instance. For a list of valid resource types, see AWS Resource Types Reference (http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html)
        """
        return pulumi.get(self, "target_type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

