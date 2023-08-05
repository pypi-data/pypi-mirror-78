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

__all__ = ['Pipeline']


class Pipeline(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 artifact_store: Optional[pulumi.Input[pulumi.InputType['PipelineArtifactStoreArgs']]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 stages: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['PipelineStageArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Provides a CodePipeline.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        codepipeline_bucket = aws.s3.Bucket("codepipelineBucket", acl="private")
        codepipeline_role = aws.iam.Role("codepipelineRole", assume_role_policy=\"\"\"{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Effect": "Allow",
              "Principal": {
                "Service": "codepipeline.amazonaws.com"
              },
              "Action": "sts:AssumeRole"
            }
          ]
        }
        \"\"\")
        s3kmskey = aws.kms.get_alias(name="alias/myKmsKey")
        codepipeline = aws.codepipeline.Pipeline("codepipeline",
            role_arn=codepipeline_role.arn,
            artifact_store=aws.codepipeline.PipelineArtifactStoreArgs(
                location=codepipeline_bucket.bucket,
                type="S3",
                encryption_key={
                    "id": s3kmskey.arn,
                    "type": "KMS",
                },
            ),
            stages=[
                aws.codepipeline.PipelineStageArgs(
                    name="Source",
                    actions=[aws.codepipeline.PipelineStageActionArgs(
                        name="Source",
                        category="Source",
                        owner="ThirdParty",
                        provider="GitHub",
                        version="1",
                        output_artifacts=["source_output"],
                        configuration={
                            "Owner": "my-organization",
                            "Repo": "test",
                            "Branch": "master",
                            "OAuthToken": var["github_token"],
                        },
                    )],
                ),
                aws.codepipeline.PipelineStageArgs(
                    name="Build",
                    actions=[aws.codepipeline.PipelineStageActionArgs(
                        name="Build",
                        category="Build",
                        owner="AWS",
                        provider="CodeBuild",
                        input_artifacts=["source_output"],
                        output_artifacts=["build_output"],
                        version="1",
                        configuration={
                            "ProjectName": "test",
                        },
                    )],
                ),
                aws.codepipeline.PipelineStageArgs(
                    name="Deploy",
                    actions=[aws.codepipeline.PipelineStageActionArgs(
                        name="Deploy",
                        category="Deploy",
                        owner="AWS",
                        provider="CloudFormation",
                        input_artifacts=["build_output"],
                        version="1",
                        configuration={
                            "ActionMode": "REPLACE_ON_FAILURE",
                            "Capabilities": "CAPABILITY_AUTO_EXPAND,CAPABILITY_IAM",
                            "OutputFileName": "CreateStackOutput.json",
                            "StackName": "MyStack",
                            "TemplatePath": "build_output::sam-templated.yaml",
                        },
                    )],
                ),
            ])
        codepipeline_policy = aws.iam.RolePolicy("codepipelinePolicy",
            role=codepipeline_role.id,
            policy=pulumi.Output.all(codepipeline_bucket.arn, codepipeline_bucket.arn).apply(lambda codepipelineBucketArn, codepipelineBucketArn1: f\"\"\"{{
          "Version": "2012-10-17",
          "Statement": [
            {{
              "Effect":"Allow",
              "Action": [
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:GetBucketVersioning",
                "s3:PutObject"
              ],
              "Resource": [
                "{codepipeline_bucket_arn}",
                "{codepipeline_bucket_arn1}/*"
              ]
            }},
            {{
              "Effect": "Allow",
              "Action": [
                "codebuild:BatchGetBuilds",
                "codebuild:StartBuild"
              ],
              "Resource": "*"
            }}
          ]
        }}
        \"\"\"))
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['PipelineArtifactStoreArgs']] artifact_store: One or more artifact_store blocks. Artifact stores are documented below.
        :param pulumi.Input[str] name: The name of the pipeline.
        :param pulumi.Input[str] role_arn: A service role Amazon Resource Name (ARN) that grants AWS CodePipeline permission to make calls to AWS services on your behalf.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['PipelineStageArgs']]]] stages: A stage block. Stages are documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
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

            if artifact_store is None:
                raise TypeError("Missing required property 'artifact_store'")
            __props__['artifact_store'] = artifact_store
            __props__['name'] = name
            if role_arn is None:
                raise TypeError("Missing required property 'role_arn'")
            __props__['role_arn'] = role_arn
            if stages is None:
                raise TypeError("Missing required property 'stages'")
            __props__['stages'] = stages
            __props__['tags'] = tags
            __props__['arn'] = None
        super(Pipeline, __self__).__init__(
            'aws:codepipeline/pipeline:Pipeline',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            artifact_store: Optional[pulumi.Input[pulumi.InputType['PipelineArtifactStoreArgs']]] = None,
            name: Optional[pulumi.Input[str]] = None,
            role_arn: Optional[pulumi.Input[str]] = None,
            stages: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['PipelineStageArgs']]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Pipeline':
        """
        Get an existing Pipeline resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The codepipeline ARN.
        :param pulumi.Input[pulumi.InputType['PipelineArtifactStoreArgs']] artifact_store: One or more artifact_store blocks. Artifact stores are documented below.
        :param pulumi.Input[str] name: The name of the pipeline.
        :param pulumi.Input[str] role_arn: A service role Amazon Resource Name (ARN) that grants AWS CodePipeline permission to make calls to AWS services on your behalf.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['PipelineStageArgs']]]] stages: A stage block. Stages are documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["arn"] = arn
        __props__["artifact_store"] = artifact_store
        __props__["name"] = name
        __props__["role_arn"] = role_arn
        __props__["stages"] = stages
        __props__["tags"] = tags
        return Pipeline(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The codepipeline ARN.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="artifactStore")
    def artifact_store(self) -> pulumi.Output['outputs.PipelineArtifactStore']:
        """
        One or more artifact_store blocks. Artifact stores are documented below.
        """
        return pulumi.get(self, "artifact_store")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the pipeline.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        """
        A service role Amazon Resource Name (ARN) that grants AWS CodePipeline permission to make calls to AWS services on your behalf.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def stages(self) -> pulumi.Output[List['outputs.PipelineStage']]:
        """
        A stage block. Stages are documented below.
        """
        return pulumi.get(self, "stages")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource.
        """
        return pulumi.get(self, "tags")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

