import os

from aws_cdk import (
    App, Aws,
    Stack, RemovalPolicy,
    aws_iam, aws_s3, aws_s3_deployment
)

class FrontendStack(Stack):

    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)
        
        bucket = aws_s3.Bucket( self, "frontendBucket",
            bucket_name=f"{props['namespace'].lower()}-{Aws.ACCOUNT_ID}",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            public_read_access=True
        )

        aws_s3_deployment.BucketDeployment( self, "DeploymentBucket",
            sources=[aws_s3_deployment.Source.asset("./frontend")],
            destination_bucket=bucket,
            destination_key_prefix="",
            memory_limit=256
        )

        self.output_props = props.copy()
        self.output_props['bucket'] = bucket

    @property
    def outputs(self):
        return self.output_props