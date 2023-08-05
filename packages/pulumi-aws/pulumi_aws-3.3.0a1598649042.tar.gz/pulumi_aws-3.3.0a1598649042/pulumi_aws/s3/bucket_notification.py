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

__all__ = ['BucketNotification']


class BucketNotification(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 bucket: Optional[pulumi.Input[str]] = None,
                 lambda_functions: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['BucketNotificationLambdaFunctionArgs']]]]] = None,
                 queues: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['BucketNotificationQueueArgs']]]]] = None,
                 topics: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['BucketNotificationTopicArgs']]]]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        Manages a S3 Bucket Notification Configuration. For additional information, see the [Configuring S3 Event Notifications section in the Amazon S3 Developer Guide](https://docs.aws.amazon.com/AmazonS3/latest/dev/NotificationHowTo.html).

        > **NOTE:** S3 Buckets only support a single notification configuration. Declaring multiple `s3.BucketNotification` resources to the same S3 Bucket will cause a perpetual difference in configuration. See the example "Trigger multiple Lambda functions" for an option.

        ## Example Usage
        ### Add notification configuration to SNS Topic

        ```python
        import pulumi
        import pulumi_aws as aws

        bucket = aws.s3.Bucket("bucket")
        topic = aws.sns.Topic("topic", policy=bucket.arn.apply(lambda arn: f\"\"\"{{
            "Version":"2012-10-17",
            "Statement":[{{
                "Effect": "Allow",
                "Principal": {{"AWS":"*"}},
                "Action": "SNS:Publish",
                "Resource": "arn:aws:sns:*:*:s3-event-notification-topic",
                "Condition":{{
                    "ArnLike":{{"aws:SourceArn":"{arn}"}}
                }}
            }}]
        }}
        \"\"\"))
        bucket_notification = aws.s3.BucketNotification("bucketNotification",
            bucket=bucket.id,
            topics=[aws.s3.BucketNotificationTopicArgs(
                topic_arn=topic.arn,
                events=["s3:ObjectCreated:*"],
                filter_suffix=".log",
            )])
        ```
        ### Add notification configuration to SQS Queue

        ```python
        import pulumi
        import pulumi_aws as aws

        bucket = aws.s3.Bucket("bucket")
        queue = aws.sqs.Queue("queue", policy=bucket.arn.apply(lambda arn: f\"\"\"{{
          "Version": "2012-10-17",
          "Statement": [
            {{
              "Effect": "Allow",
              "Principal": "*",
              "Action": "sqs:SendMessage",
        	  "Resource": "arn:aws:sqs:*:*:s3-event-notification-queue",
              "Condition": {{
                "ArnEquals": {{ "aws:SourceArn": "{arn}" }}
              }}
            }}
          ]
        }}
        \"\"\"))
        bucket_notification = aws.s3.BucketNotification("bucketNotification",
            bucket=bucket.id,
            queues=[aws.s3.BucketNotificationQueueArgs(
                queue_arn=queue.arn,
                events=["s3:ObjectCreated:*"],
                filter_suffix=".log",
            )])
        ```
        ### Add notification configuration to Lambda Function

        ```python
        import pulumi
        import pulumi_aws as aws

        iam_for_lambda = aws.iam.Role("iamForLambda", assume_role_policy=\"\"\"{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Action": "sts:AssumeRole",
              "Principal": {
                "Service": "lambda.amazonaws.com"
              },
              "Effect": "Allow"
            }
          ]
        }
        \"\"\")
        func = aws.lambda_.Function("func",
            code=pulumi.FileArchive("your-function.zip"),
            role=iam_for_lambda.arn,
            handler="exports.example",
            runtime="go1.x")
        bucket = aws.s3.Bucket("bucket")
        allow_bucket = aws.lambda_.Permission("allowBucket",
            action="lambda:InvokeFunction",
            function=func.arn,
            principal="s3.amazonaws.com",
            source_arn=bucket.arn)
        bucket_notification = aws.s3.BucketNotification("bucketNotification",
            bucket=bucket.id,
            lambda_functions=[aws.s3.BucketNotificationLambdaFunctionArgs(
                lambda_function_arn=func.arn,
                events=["s3:ObjectCreated:*"],
                filter_prefix="AWSLogs/",
                filter_suffix=".log",
            )],
            opts=ResourceOptions(depends_on=[allow_bucket]))
        ```
        ### Trigger multiple Lambda functions

        ```python
        import pulumi
        import pulumi_aws as aws

        iam_for_lambda = aws.iam.Role("iamForLambda", assume_role_policy=\"\"\"{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Action": "sts:AssumeRole",
              "Principal": {
                "Service": "lambda.amazonaws.com"
              },
              "Effect": "Allow"
            }
          ]
        }
        \"\"\")
        func1 = aws.lambda_.Function("func1",
            code=pulumi.FileArchive("your-function1.zip"),
            role=iam_for_lambda.arn,
            handler="exports.example",
            runtime="go1.x")
        bucket = aws.s3.Bucket("bucket")
        allow_bucket1 = aws.lambda_.Permission("allowBucket1",
            action="lambda:InvokeFunction",
            function=func1.arn,
            principal="s3.amazonaws.com",
            source_arn=bucket.arn)
        func2 = aws.lambda_.Function("func2",
            code=pulumi.FileArchive("your-function2.zip"),
            role=iam_for_lambda.arn,
            handler="exports.example")
        allow_bucket2 = aws.lambda_.Permission("allowBucket2",
            action="lambda:InvokeFunction",
            function=func2.arn,
            principal="s3.amazonaws.com",
            source_arn=bucket.arn)
        bucket_notification = aws.s3.BucketNotification("bucketNotification",
            bucket=bucket.id,
            lambda_functions=[
                aws.s3.BucketNotificationLambdaFunctionArgs(
                    lambda_function_arn=func1.arn,
                    events=["s3:ObjectCreated:*"],
                    filter_prefix="AWSLogs/",
                    filter_suffix=".log",
                ),
                aws.s3.BucketNotificationLambdaFunctionArgs(
                    lambda_function_arn=func2.arn,
                    events=["s3:ObjectCreated:*"],
                    filter_prefix="OtherLogs/",
                    filter_suffix=".log",
                ),
            ],
            opts=ResourceOptions(depends_on=[
                    allow_bucket1,
                    allow_bucket2,
                ]))
        ```
        ### Add multiple notification configurations to SQS Queue

        ```python
        import pulumi
        import pulumi_aws as aws

        bucket = aws.s3.Bucket("bucket")
        queue = aws.sqs.Queue("queue", policy=bucket.arn.apply(lambda arn: f\"\"\"{{
          "Version": "2012-10-17",
          "Statement": [
            {{
              "Effect": "Allow",
              "Principal": "*",
              "Action": "sqs:SendMessage",
        	  "Resource": "arn:aws:sqs:*:*:s3-event-notification-queue",
              "Condition": {{
                "ArnEquals": {{ "aws:SourceArn": "{arn}" }}
              }}
            }}
          ]
        }}
        \"\"\"))
        bucket_notification = aws.s3.BucketNotification("bucketNotification",
            bucket=bucket.id,
            queues=[
                aws.s3.BucketNotificationQueueArgs(
                    id="image-upload-event",
                    queue_arn=queue.arn,
                    events=["s3:ObjectCreated:*"],
                    filter_prefix="images/",
                ),
                aws.s3.BucketNotificationQueueArgs(
                    id="video-upload-event",
                    queue_arn=queue.arn,
                    events=["s3:ObjectCreated:*"],
                    filter_prefix="videos/",
                ),
            ])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The name of the bucket to put notification configuration.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['BucketNotificationLambdaFunctionArgs']]]] lambda_functions: Used to configure notifications to a Lambda Function (documented below).
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['BucketNotificationQueueArgs']]]] queues: The notification configuration to SQS Queue (documented below).
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['BucketNotificationTopicArgs']]]] topics: The notification configuration to SNS Topic (documented below).
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

            if bucket is None:
                raise TypeError("Missing required property 'bucket'")
            __props__['bucket'] = bucket
            __props__['lambda_functions'] = lambda_functions
            __props__['queues'] = queues
            __props__['topics'] = topics
        super(BucketNotification, __self__).__init__(
            'aws:s3/bucketNotification:BucketNotification',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            bucket: Optional[pulumi.Input[str]] = None,
            lambda_functions: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['BucketNotificationLambdaFunctionArgs']]]]] = None,
            queues: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['BucketNotificationQueueArgs']]]]] = None,
            topics: Optional[pulumi.Input[List[pulumi.Input[pulumi.InputType['BucketNotificationTopicArgs']]]]] = None) -> 'BucketNotification':
        """
        Get an existing BucketNotification resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] bucket: The name of the bucket to put notification configuration.
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['BucketNotificationLambdaFunctionArgs']]]] lambda_functions: Used to configure notifications to a Lambda Function (documented below).
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['BucketNotificationQueueArgs']]]] queues: The notification configuration to SQS Queue (documented below).
        :param pulumi.Input[List[pulumi.Input[pulumi.InputType['BucketNotificationTopicArgs']]]] topics: The notification configuration to SNS Topic (documented below).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["bucket"] = bucket
        __props__["lambda_functions"] = lambda_functions
        __props__["queues"] = queues
        __props__["topics"] = topics
        return BucketNotification(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def bucket(self) -> pulumi.Output[str]:
        """
        The name of the bucket to put notification configuration.
        """
        return pulumi.get(self, "bucket")

    @property
    @pulumi.getter(name="lambdaFunctions")
    def lambda_functions(self) -> pulumi.Output[Optional[List['outputs.BucketNotificationLambdaFunction']]]:
        """
        Used to configure notifications to a Lambda Function (documented below).
        """
        return pulumi.get(self, "lambda_functions")

    @property
    @pulumi.getter
    def queues(self) -> pulumi.Output[Optional[List['outputs.BucketNotificationQueue']]]:
        """
        The notification configuration to SQS Queue (documented below).
        """
        return pulumi.get(self, "queues")

    @property
    @pulumi.getter
    def topics(self) -> pulumi.Output[Optional[List['outputs.BucketNotificationTopic']]]:
        """
        The notification configuration to SNS Topic (documented below).
        """
        return pulumi.get(self, "topics")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

