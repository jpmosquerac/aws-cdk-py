from aws_cdk import (
    App,
    Stack,
)

from aws_cdk.pipelines import (
    ShellStep,
    CodePipeline,
    CodePipelineSource,
)

from aws_cdk_py.backend_stage import BackendStage
from aws_cdk_py.frontend_stage import FrontendStage


class Pipeline(Stack):
    def __init__(self, app: App, id: str, props, **kwargs) -> None:
        super().__init__(app, id, **kwargs)

        source = CodePipelineSource.git_hub("jpmosquerac/aws-cdk-py", "main")

        synth_step = ShellStep("Synth", 
                        input = source,
                        commands = ["npm install -g aws-cdk",
                        "python -m pip install -r requirements.txt",
                        "cdk synth",
                        ]
                    )

        pipeline = CodePipeline(self, f"{props['namespace']}-Pipeline", 
                        pipeline_name = f"{props['namespace']}-Pipeline",
                        synth = synth_step
                    )

        backendStage = pipeline.add_stage(BackendStage(self, f"{props['namespace']}-BackendStage", props))

        frontendStage = pipeline.add_stage(FrontendStage(self, f"{props['namespace']}-FrontendStage", props))

        self.output_props = props.copy()
        self.output_props['pipeline'] = pipeline

    @property
    def outputs(self):
        return self.output_props
