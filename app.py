#!/usr/bin/env python3
import os
import yaml

from aws_cdk import (
    App,
    Tags,
    Environment
)

from aws_cdk_py.aws_cdk_py_stack import AwsCdkPyStack
from aws_cdk_py.pipeline_stack import Pipeline


with open('./parameters.yml') as file:
    parameters = yaml.load(file, Loader=yaml.FullLoader)

with open('./tags.yml') as file:
    tags = yaml.load(file, Loader=yaml.FullLoader)

# map parameters to be passed to the stacks
props = {
    'namespace': parameters['namespace']
}

# Define enviroment to be used on diferent stacks
env_=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))

app = App()

# Set tags to all resources deployed
for tag_name, tag_value in tags.items():
    Tags.of(app).add(
        tag_name,
        tag_value
    )

# Base stack
aws_cdk_py_stack = AwsCdkPyStack(app, f"{props['namespace']}", props, env=env_)

# Pipeline stack
pipeline = Pipeline(app, f"{props['namespace']}-PipelineStack", aws_cdk_py_stack.outputs, env=env_)
pipeline.add_dependency(aws_cdk_py_stack)

app.synth()
