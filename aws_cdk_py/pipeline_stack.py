from aws_cdk import (
    App,
    Stack
)
from aws_cdk.pipelines import (
    ShellStep,
    CodePipeline,
    CodePipelineSource
)


class Pipeline(Stack):
    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        source   = CodePipelineSource.git_hub("OWNER/REPO", "main")

        synth_step = ShellStep("Synth", 
                        input = source,
                        commands = ["npm install -g aws-cdk",
                        "python -m pip install -r requirements.txt",
                        "cdk synth"])

        pipeline   = CodePipeline(self, f"{props['namespace']}-Pipeline", 
                        pipeline_name = f"{props['namespace']}-Pipeline",
                        synth = synth_step)
