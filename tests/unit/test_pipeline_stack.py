import os
import yaml

from aws_cdk import (
    App,
    Environment,
    assertions,
)

from aws_cdk_py.pipeline_stack import Pipeline

def test_backend_stack():
    app = App()

    with open('./parameters.yml') as file:
        parameters = yaml.load(file, Loader=yaml.FullLoader)

    # map parameters to be passed to the stacks
    props = {
        'namespace': parameters['namespace']
    }

    # Define enviroment to be used on diferent stacks
    env_=Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))

    stack = Pipeline(app, f"{props['namespace']}-PipelineStack", props, env=env_)

    template = assertions.Template.from_stack(stack)
    template.resource_count_is('AWS::CodePipeline::Pipeline', 1)