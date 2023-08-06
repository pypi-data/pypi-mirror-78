import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import (
    CfnOutput as _CfnOutput_1185605a,
    Construct as _Construct_f50a3f53,
    Stage as _Stage_eb8e262d,
)
from ..aws_codebuild import (
    BuildEnvironment as _BuildEnvironment_3f2fec35,
    BuildEnvironmentVariable as _BuildEnvironmentVariable_dda665dd,
    IProject as _IProject_2a66e54e,
)
from ..aws_codepipeline import (
    ActionBindOptions as _ActionBindOptions_530c352f,
    ActionConfig as _ActionConfig_c379766c,
    ActionProperties as _ActionProperties_8f5d7a9d,
    Artifact as _Artifact_af6d98e9,
    ArtifactPath as _ArtifactPath_8730c13b,
    IAction as _IAction_369e77ae,
    IStage as _IStage_b7c853a7,
    Pipeline as _Pipeline_0667258b,
)
from ..aws_events import (
    EventPattern as _EventPattern_8aa7b781,
    IEventBus as _IEventBus_ed4f1700,
    IRuleTarget as _IRuleTarget_41800a77,
    Rule as _Rule_c38e0b39,
    RuleProps as _RuleProps_d60f0abf,
    Schedule as _Schedule_11a70620,
)
from ..aws_iam import (
    IRole as _IRole_e69bbae4, PolicyStatement as _PolicyStatement_f75dc775
)
from ..aws_s3 import IBucket as _IBucket_25bad983
from ..cx_api import (
    CloudFormationStackArtifact as _CloudFormationStackArtifact_64f58f61
)


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.AddManualApprovalOptions",
    jsii_struct_bases=[],
    name_mapping={"action_name": "actionName", "run_order": "runOrder"},
)
class AddManualApprovalOptions:
    def __init__(
        self,
        *,
        action_name: typing.Optional[str] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Options for addManualApproval.

        :param action_name: The name of the manual approval action. Default: 'ManualApproval' with a rolling counter
        :param run_order: The runOrder for this action. Default: - The next sequential runOrder

        stability
        :stability: experimental
        """
        self._values = {}
        if action_name is not None:
            self._values["action_name"] = action_name
        if run_order is not None:
            self._values["run_order"] = run_order

    @builtins.property
    def action_name(self) -> typing.Optional[str]:
        """The name of the manual approval action.

        default
        :default: 'ManualApproval' with a rolling counter

        stability
        :stability: experimental
        """
        return self._values.get("action_name")

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """The runOrder for this action.

        default
        :default: - The next sequential runOrder

        stability
        :stability: experimental
        """
        return self._values.get("run_order")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddManualApprovalOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.AddStackOptions",
    jsii_struct_bases=[],
    name_mapping={"execute_run_order": "executeRunOrder", "run_order": "runOrder"},
)
class AddStackOptions:
    def __init__(
        self,
        *,
        execute_run_order: typing.Optional[jsii.Number] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Additional options for adding a stack deployment.

        :param execute_run_order: Base runorder. Default: - runOrder + 1
        :param run_order: Base runorder. Default: - Next sequential runorder

        stability
        :stability: experimental
        """
        self._values = {}
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if run_order is not None:
            self._values["run_order"] = run_order

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        """Base runorder.

        default
        :default: - runOrder + 1

        stability
        :stability: experimental
        """
        return self._values.get("execute_run_order")

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """Base runorder.

        default
        :default: - Next sequential runorder

        stability
        :stability: experimental
        """
        return self._values.get("run_order")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddStackOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.AddStageOptions",
    jsii_struct_bases=[],
    name_mapping={"manual_approvals": "manualApprovals"},
)
class AddStageOptions:
    def __init__(self, *, manual_approvals: typing.Optional[bool] = None) -> None:
        """Options for adding an application stage to a pipeline.

        :param manual_approvals: Add manual approvals before executing change sets. This gives humans the opportunity to confirm the change set looks alright before deploying it. Default: false

        stability
        :stability: experimental
        """
        self._values = {}
        if manual_approvals is not None:
            self._values["manual_approvals"] = manual_approvals

    @builtins.property
    def manual_approvals(self) -> typing.Optional[bool]:
        """Add manual approvals before executing change sets.

        This gives humans the opportunity to confirm the change set looks alright
        before deploying it.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("manual_approvals")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddStageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.AdditionalArtifact",
    jsii_struct_bases=[],
    name_mapping={"artifact": "artifact", "directory": "directory"},
)
class AdditionalArtifact:
    def __init__(self, *, artifact: _Artifact_af6d98e9, directory: str) -> None:
        """Specification of an additional artifact to generate.

        :param artifact: Artifact to represent the build directory in the pipeline.
        :param directory: Directory to be packaged.

        stability
        :stability: experimental
        """
        self._values = {
            "artifact": artifact,
            "directory": directory,
        }

    @builtins.property
    def artifact(self) -> _Artifact_af6d98e9:
        """Artifact to represent the build directory in the pipeline.

        stability
        :stability: experimental
        """
        return self._values.get("artifact")

    @builtins.property
    def directory(self) -> str:
        """Directory to be packaged.

        stability
        :stability: experimental
        """
        return self._values.get("directory")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdditionalArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.AssetPublishingCommand",
    jsii_struct_bases=[],
    name_mapping={
        "asset_id": "assetId",
        "asset_manifest_path": "assetManifestPath",
        "asset_selector": "assetSelector",
        "asset_type": "assetType",
    },
)
class AssetPublishingCommand:
    def __init__(
        self,
        *,
        asset_id: str,
        asset_manifest_path: str,
        asset_selector: str,
        asset_type: "AssetType",
    ) -> None:
        """Instructions to publish certain assets.

        :param asset_id: Asset identifier.
        :param asset_manifest_path: Asset manifest path.
        :param asset_selector: Asset selector to pass to ``cdk-assets``.
        :param asset_type: Type of asset to publish.

        stability
        :stability: experimental
        """
        self._values = {
            "asset_id": asset_id,
            "asset_manifest_path": asset_manifest_path,
            "asset_selector": asset_selector,
            "asset_type": asset_type,
        }

    @builtins.property
    def asset_id(self) -> str:
        """Asset identifier.

        stability
        :stability: experimental
        """
        return self._values.get("asset_id")

    @builtins.property
    def asset_manifest_path(self) -> str:
        """Asset manifest path.

        stability
        :stability: experimental
        """
        return self._values.get("asset_manifest_path")

    @builtins.property
    def asset_selector(self) -> str:
        """Asset selector to pass to ``cdk-assets``.

        stability
        :stability: experimental
        """
        return self._values.get("asset_selector")

    @builtins.property
    def asset_type(self) -> "AssetType":
        """Type of asset to publish.

        stability
        :stability: experimental
        """
        return self._values.get("asset_type")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetPublishingCommand(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.pipelines.AssetType")
class AssetType(enum.Enum):
    """Type of the asset that is being published.

    stability
    :stability: experimental
    """

    FILE = "FILE"
    """A file.

    stability
    :stability: experimental
    """
    DOCKER_IMAGE = "DOCKER_IMAGE"
    """A Docker image.

    stability
    :stability: experimental
    """


class CdkPipeline(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.pipelines.CdkPipeline",
):
    """A Pipeline to deploy CDK apps.

    Defines an AWS CodePipeline-based Pipeline to deploy CDK applications.

    Automatically manages the following:

    - Stack dependency order.
    - Asset publishing.
    - Keeping the pipeline up-to-date as the CDK apps change.
    - Using stack outputs later on in the pipeline.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cloud_assembly_artifact: _Artifact_af6d98e9,
        cdk_cli_version: typing.Optional[str] = None,
        code_pipeline: typing.Optional[_Pipeline_0667258b] = None,
        pipeline_name: typing.Optional[str] = None,
        source_action: typing.Optional[_IAction_369e77ae] = None,
        synth_action: typing.Optional[_IAction_369e77ae] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cloud_assembly_artifact: The artifact you have defined to be the artifact to hold the cloudAssemblyArtifact for the synth action.
        :param cdk_cli_version: CDK CLI version to use in pipeline. Some Actions in the pipeline will download and run a version of the CDK CLI. Specify the version here. Default: - Latest version
        :param code_pipeline: Existing CodePipeline to add deployment stages to. Use this if you want more control over the CodePipeline that gets created. You can choose to not pass this value, in which case a new CodePipeline is created with default settings. If you pass an existing CodePipeline, it should should have been created with ``restartExecutionOnUpdate: true``. [disable-awslint:ref-via-interface] Default: - A new CodePipeline is automatically generated
        :param pipeline_name: Name of the pipeline. Can only be set if ``codePipeline`` is not set. Default: - A name is automatically generated
        :param source_action: The CodePipeline action used to retrieve the CDK app's source. Default: - Required unless ``codePipeline`` is given
        :param synth_action: The CodePipeline action build and synthesis step of the CDK app. Default: - Required unless ``codePipeline`` or ``sourceAction`` is given

        stability
        :stability: experimental
        """
        props = CdkPipelineProps(
            cloud_assembly_artifact=cloud_assembly_artifact,
            cdk_cli_version=cdk_cli_version,
            code_pipeline=code_pipeline,
            pipeline_name=pipeline_name,
            source_action=source_action,
            synth_action=synth_action,
        )

        jsii.create(CdkPipeline, self, [scope, id, props])

    @jsii.member(jsii_name="addApplicationStage")
    def add_application_stage(
        self,
        app_stage: _Stage_eb8e262d,
        *,
        manual_approvals: typing.Optional[bool] = None,
    ) -> "CdkStage":
        """Add pipeline stage that will deploy the given application stage.

        The application construct should subclass ``Stage`` and can contain any
        number of ``Stacks`` inside it that may have dependency relationships
        on one another.

        All stacks in the application will be deployed in the appropriate order,
        and all assets found in the application will be added to the asset
        publishing stage.

        :param app_stage: -
        :param manual_approvals: Add manual approvals before executing change sets. This gives humans the opportunity to confirm the change set looks alright before deploying it. Default: false

        stability
        :stability: experimental
        """
        options = AddStageOptions(manual_approvals=manual_approvals)

        return jsii.invoke(self, "addApplicationStage", [app_stage, options])

    @jsii.member(jsii_name="addStage")
    def add_stage(self, stage_name: str) -> "CdkStage":
        """Add a new, empty stage to the pipeline.

        Prefer to use ``addApplicationStage`` if you are intended to deploy a CDK
        application, but you can use this method if you want to add other kinds of
        Actions to a pipeline.

        :param stage_name: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addStage", [stage_name])

    @jsii.member(jsii_name="stackOutput")
    def stack_output(self, cfn_output: _CfnOutput_1185605a) -> "StackOutput":
        """Get the StackOutput object that holds this CfnOutput's value in this pipeline.

        ``StackOutput`` can be used in validation actions later in the pipeline.

        :param cfn_output: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "stackOutput", [cfn_output])

    @jsii.member(jsii_name="stage")
    def stage(self, stage_name: str) -> _IStage_b7c853a7:
        """Access one of the pipeline's stages by stage name.

        You can use this to add more Actions to a stage.

        :param stage_name: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "stage", [stage_name])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate that we don't have any stacks violating dependency order in the pipeline.

        Our own convenience methods will never generate a pipeline that does that (although
        this is a nice verification), but a user can also add the stacks by hand.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "validate", [])

    @builtins.property
    @jsii.member(jsii_name="codePipeline")
    def code_pipeline(self) -> _Pipeline_0667258b:
        """The underlying CodePipeline object.

        You can use this to add more Stages to the pipeline, or Actions
        to Stages.

        stability
        :stability: experimental
        """
        return jsii.get(self, "codePipeline")


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.CdkPipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "cdk_cli_version": "cdkCliVersion",
        "code_pipeline": "codePipeline",
        "pipeline_name": "pipelineName",
        "source_action": "sourceAction",
        "synth_action": "synthAction",
    },
)
class CdkPipelineProps:
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_af6d98e9,
        cdk_cli_version: typing.Optional[str] = None,
        code_pipeline: typing.Optional[_Pipeline_0667258b] = None,
        pipeline_name: typing.Optional[str] = None,
        source_action: typing.Optional[_IAction_369e77ae] = None,
        synth_action: typing.Optional[_IAction_369e77ae] = None,
    ) -> None:
        """Properties for a CdkPipeline.

        :param cloud_assembly_artifact: The artifact you have defined to be the artifact to hold the cloudAssemblyArtifact for the synth action.
        :param cdk_cli_version: CDK CLI version to use in pipeline. Some Actions in the pipeline will download and run a version of the CDK CLI. Specify the version here. Default: - Latest version
        :param code_pipeline: Existing CodePipeline to add deployment stages to. Use this if you want more control over the CodePipeline that gets created. You can choose to not pass this value, in which case a new CodePipeline is created with default settings. If you pass an existing CodePipeline, it should should have been created with ``restartExecutionOnUpdate: true``. [disable-awslint:ref-via-interface] Default: - A new CodePipeline is automatically generated
        :param pipeline_name: Name of the pipeline. Can only be set if ``codePipeline`` is not set. Default: - A name is automatically generated
        :param source_action: The CodePipeline action used to retrieve the CDK app's source. Default: - Required unless ``codePipeline`` is given
        :param synth_action: The CodePipeline action build and synthesis step of the CDK app. Default: - Required unless ``codePipeline`` or ``sourceAction`` is given

        stability
        :stability: experimental
        """
        self._values = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
        }
        if cdk_cli_version is not None:
            self._values["cdk_cli_version"] = cdk_cli_version
        if code_pipeline is not None:
            self._values["code_pipeline"] = code_pipeline
        if pipeline_name is not None:
            self._values["pipeline_name"] = pipeline_name
        if source_action is not None:
            self._values["source_action"] = source_action
        if synth_action is not None:
            self._values["synth_action"] = synth_action

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_af6d98e9:
        """The artifact you have defined to be the artifact to hold the cloudAssemblyArtifact for the synth action.

        stability
        :stability: experimental
        """
        return self._values.get("cloud_assembly_artifact")

    @builtins.property
    def cdk_cli_version(self) -> typing.Optional[str]:
        """CDK CLI version to use in pipeline.

        Some Actions in the pipeline will download and run a version of the CDK
        CLI. Specify the version here.

        default
        :default: - Latest version

        stability
        :stability: experimental
        """
        return self._values.get("cdk_cli_version")

    @builtins.property
    def code_pipeline(self) -> typing.Optional[_Pipeline_0667258b]:
        """Existing CodePipeline to add deployment stages to.

        Use this if you want more control over the CodePipeline that gets created.
        You can choose to not pass this value, in which case a new CodePipeline is
        created with default settings.

        If you pass an existing CodePipeline, it should should have been created
        with ``restartExecutionOnUpdate: true``.

        [disable-awslint:ref-via-interface]

        default
        :default: - A new CodePipeline is automatically generated

        stability
        :stability: experimental
        """
        return self._values.get("code_pipeline")

    @builtins.property
    def pipeline_name(self) -> typing.Optional[str]:
        """Name of the pipeline.

        Can only be set if ``codePipeline`` is not set.

        default
        :default: - A name is automatically generated

        stability
        :stability: experimental
        """
        return self._values.get("pipeline_name")

    @builtins.property
    def source_action(self) -> typing.Optional[_IAction_369e77ae]:
        """The CodePipeline action used to retrieve the CDK app's source.

        default
        :default: - Required unless ``codePipeline`` is given

        stability
        :stability: experimental
        """
        return self._values.get("source_action")

    @builtins.property
    def synth_action(self) -> typing.Optional[_IAction_369e77ae]:
        """The CodePipeline action build and synthesis step of the CDK app.

        default
        :default: - Required unless ``codePipeline`` or ``sourceAction`` is given

        stability
        :stability: experimental
        """
        return self._values.get("synth_action")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkPipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdkStage(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.pipelines.CdkStage",
):
    """Stage in a CdkPipeline.

    You don't need to instantiate this class directly. Use
    ``cdkPipeline.addStage()`` instead.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cloud_assembly_artifact: _Artifact_af6d98e9,
        host: "IStageHost",
        pipeline_stage: _IStage_b7c853a7,
        stage_name: str,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cloud_assembly_artifact: The CodePipeline Artifact with the Cloud Assembly.
        :param host: Features the Stage needs from its environment.
        :param pipeline_stage: The underlying Pipeline Stage associated with thisCdkStage.
        :param stage_name: Name of the stage that should be created.

        stability
        :stability: experimental
        """
        props = CdkStageProps(
            cloud_assembly_artifact=cloud_assembly_artifact,
            host=host,
            pipeline_stage=pipeline_stage,
            stage_name=stage_name,
        )

        jsii.create(CdkStage, self, [scope, id, props])

    @jsii.member(jsii_name="addActions")
    def add_actions(self, *actions: _IAction_369e77ae) -> None:
        """Add one or more CodePipeline Actions.

        You need to make sure it is created with the right runOrder. Call ``nextSequentialRunOrder()``
        for every action to get actions to execute in sequence.

        :param actions: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addActions", [*actions])

    @jsii.member(jsii_name="addApplication")
    def add_application(
        self,
        app_stage: _Stage_eb8e262d,
        *,
        manual_approvals: typing.Optional[bool] = None,
    ) -> None:
        """Add all stacks in the application Stage to this stage.

        The application construct should subclass ``Stage`` and can contain any
        number of ``Stacks`` inside it that may have dependency relationships
        on one another.

        All stacks in the application will be deployed in the appropriate order,
        and all assets found in the application will be added to the asset
        publishing stage.

        :param app_stage: -
        :param manual_approvals: Add manual approvals before executing change sets. This gives humans the opportunity to confirm the change set looks alright before deploying it. Default: false

        stability
        :stability: experimental
        """
        options = AddStageOptions(manual_approvals=manual_approvals)

        return jsii.invoke(self, "addApplication", [app_stage, options])

    @jsii.member(jsii_name="addManualApprovalAction")
    def add_manual_approval_action(
        self,
        *,
        action_name: typing.Optional[str] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Add a manual approval action.

        If you need more flexibility than what this method offers,
        use ``addAction`` with a ``ManualApprovalAction``.

        :param action_name: The name of the manual approval action. Default: 'ManualApproval' with a rolling counter
        :param run_order: The runOrder for this action. Default: - The next sequential runOrder

        stability
        :stability: experimental
        """
        options = AddManualApprovalOptions(
            action_name=action_name, run_order=run_order
        )

        return jsii.invoke(self, "addManualApprovalAction", [options])

    @jsii.member(jsii_name="addStackArtifactDeployment")
    def add_stack_artifact_deployment(
        self,
        stack_artifact: _CloudFormationStackArtifact_64f58f61,
        *,
        execute_run_order: typing.Optional[jsii.Number] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Add a deployment action based on a stack artifact.

        :param stack_artifact: -
        :param execute_run_order: Base runorder. Default: - runOrder + 1
        :param run_order: Base runorder. Default: - Next sequential runorder

        stability
        :stability: experimental
        """
        options = AddStackOptions(
            execute_run_order=execute_run_order, run_order=run_order
        )

        return jsii.invoke(self, "addStackArtifactDeployment", [stack_artifact, options])

    @jsii.member(jsii_name="deploysStack")
    def deploys_stack(self, artifact_id: str) -> bool:
        """Whether this Stage contains an action to deploy the given stack, identified by its artifact ID.

        :param artifact_id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "deploysStack", [artifact_id])

    @jsii.member(jsii_name="nextSequentialRunOrder")
    def next_sequential_run_order(
        self, count: typing.Optional[jsii.Number] = None
    ) -> jsii.Number:
        """Return the runOrder number necessary to run the next Action in sequence with the rest.

        FIXME: This is here because Actions are immutable and can't be reordered
        after creation, nor is there a way to specify relative priorities, which
        is a limitation that we should take away in the base library.

        :param count: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "nextSequentialRunOrder", [count])


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.CdkStageProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "host": "host",
        "pipeline_stage": "pipelineStage",
        "stage_name": "stageName",
    },
)
class CdkStageProps:
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_af6d98e9,
        host: "IStageHost",
        pipeline_stage: _IStage_b7c853a7,
        stage_name: str,
    ) -> None:
        """Construction properties for a CdkStage.

        :param cloud_assembly_artifact: The CodePipeline Artifact with the Cloud Assembly.
        :param host: Features the Stage needs from its environment.
        :param pipeline_stage: The underlying Pipeline Stage associated with thisCdkStage.
        :param stage_name: Name of the stage that should be created.

        stability
        :stability: experimental
        """
        self._values = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "host": host,
            "pipeline_stage": pipeline_stage,
            "stage_name": stage_name,
        }

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_af6d98e9:
        """The CodePipeline Artifact with the Cloud Assembly.

        stability
        :stability: experimental
        """
        return self._values.get("cloud_assembly_artifact")

    @builtins.property
    def host(self) -> "IStageHost":
        """Features the Stage needs from its environment.

        stability
        :stability: experimental
        """
        return self._values.get("host")

    @builtins.property
    def pipeline_stage(self) -> _IStage_b7c853a7:
        """The underlying Pipeline Stage associated with thisCdkStage.

        stability
        :stability: experimental
        """
        return self._values.get("pipeline_stage")

    @builtins.property
    def stage_name(self) -> str:
        """Name of the stage that should be created.

        stability
        :stability: experimental
        """
        return self._values.get("stage_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkStageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_369e77ae)
class DeployCdkStackAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.pipelines.DeployCdkStackAction",
):
    """Action to deploy a CDK Stack.

    Adds two CodePipeline Actions to the pipeline: one to create a ChangeSet
    and one to execute it.

    You do not need to instantiate this action yourself -- it will automatically
    be added by the pipeline when you add stack artifacts or entire stages.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        *,
        action_role: _IRole_e69bbae4,
        stack_name: str,
        template_path: str,
        cloud_formation_execution_role: typing.Optional[_IRole_e69bbae4] = None,
        dependency_stack_artifact_ids: typing.Optional[typing.List[str]] = None,
        region: typing.Optional[str] = None,
        stack_artifact_id: typing.Optional[str] = None,
        cloud_assembly_input: _Artifact_af6d98e9,
        base_action_name: typing.Optional[str] = None,
        change_set_name: typing.Optional[str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_af6d98e9] = None,
        output_file_name: typing.Optional[str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param action_role: Role for the action to assume. This controls the account to deploy into
        :param stack_name: The name of the stack that should be created/updated.
        :param template_path: Relative path of template in the input artifact.
        :param cloud_formation_execution_role: Role to execute CloudFormation under. Default: - Execute CloudFormation using the action role
        :param dependency_stack_artifact_ids: Artifact ID for the stacks this stack depends on. Used for pipeline order checking. Default: - No dependencies
        :param region: Region to deploy into. Default: - Same region as pipeline
        :param stack_artifact_id: Artifact ID for the stack deployed here. Used for pipeline order checking. Default: - Order will not be checked
        :param cloud_assembly_input: The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: Base name of the action. Default: stackName
        :param change_set_name: Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: Run order for the Prepare action. Default: 1

        stability
        :stability: experimental
        """
        props = DeployCdkStackActionProps(
            action_role=action_role,
            stack_name=stack_name,
            template_path=template_path,
            cloud_formation_execution_role=cloud_formation_execution_role,
            dependency_stack_artifact_ids=dependency_stack_artifact_ids,
            region=region,
            stack_artifact_id=stack_artifact_id,
            cloud_assembly_input=cloud_assembly_input,
            base_action_name=base_action_name,
            change_set_name=change_set_name,
            execute_run_order=execute_run_order,
            output=output,
            output_file_name=output_file_name,
            prepare_run_order=prepare_run_order,
        )

        jsii.create(DeployCdkStackAction, self, [props])

    @jsii.member(jsii_name="fromStackArtifact")
    @builtins.classmethod
    def from_stack_artifact(
        cls,
        scope: _Construct_f50a3f53,
        artifact: _CloudFormationStackArtifact_64f58f61,
        *,
        stack_name: typing.Optional[str] = None,
        cloud_assembly_input: _Artifact_af6d98e9,
        base_action_name: typing.Optional[str] = None,
        change_set_name: typing.Optional[str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_af6d98e9] = None,
        output_file_name: typing.Optional[str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
    ) -> "DeployCdkStackAction":
        """Construct a DeployCdkStackAction from a Stack artifact.

        :param scope: -
        :param artifact: -
        :param stack_name: The name of the stack that should be created/updated. Default: - Same as stack artifact
        :param cloud_assembly_input: The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: Base name of the action. Default: stackName
        :param change_set_name: Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: Run order for the Prepare action. Default: 1

        stability
        :stability: experimental
        """
        options = CdkStackActionFromArtifactOptions(
            stack_name=stack_name,
            cloud_assembly_input=cloud_assembly_input,
            base_action_name=base_action_name,
            change_set_name=change_set_name,
            execute_run_order=execute_run_order,
            output=output,
            output_file_name=output_file_name,
            prepare_run_order=prepare_run_order,
        )

        return jsii.sinvoke(cls, "fromStackArtifact", [scope, artifact, options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_f50a3f53,
        stage: _IStage_b7c853a7,
        *,
        bucket: _IBucket_25bad983,
        role: _IRole_e69bbae4,
    ) -> _ActionConfig_c379766c:
        """Exists to implement IAction.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bind", [scope, stage, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: str,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
        *,
        description: typing.Optional[str] = None,
        enabled: typing.Optional[bool] = None,
        event_bus: typing.Optional[_IEventBus_ed4f1700] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        schedule: typing.Optional[_Schedule_11a70620] = None,
        targets: typing.Optional[typing.List[_IRuleTarget_41800a77]] = None,
    ) -> _Rule_c38e0b39:
        """Exists to implement IAction.

        :param name: -
        :param target: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        stability
        :stability: experimental
        """
        options = _RuleProps_d60f0abf(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return jsii.invoke(self, "onStateChange", [name, target, options])

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_8f5d7a9d:
        """Exists to implement IAction.

        stability
        :stability: experimental
        """
        return jsii.get(self, "actionProperties")

    @builtins.property
    @jsii.member(jsii_name="dependencyStackArtifactIds")
    def dependency_stack_artifact_ids(self) -> typing.List[str]:
        """Artifact ids of the artifact this stack artifact depends on.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dependencyStackArtifactIds")

    @builtins.property
    @jsii.member(jsii_name="executeRunOrder")
    def execute_run_order(self) -> jsii.Number:
        """The runorder for the execute action.

        stability
        :stability: experimental
        """
        return jsii.get(self, "executeRunOrder")

    @builtins.property
    @jsii.member(jsii_name="prepareRunOrder")
    def prepare_run_order(self) -> jsii.Number:
        """The runorder for the prepare action.

        stability
        :stability: experimental
        """
        return jsii.get(self, "prepareRunOrder")

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> str:
        """Name of the deployed stack.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stackName")

    @builtins.property
    @jsii.member(jsii_name="stackArtifactId")
    def stack_artifact_id(self) -> typing.Optional[str]:
        """Artifact id of the artifact this action was based on.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stackArtifactId")


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.DeployCdkStackActionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "base_action_name": "baseActionName",
        "change_set_name": "changeSetName",
        "execute_run_order": "executeRunOrder",
        "output": "output",
        "output_file_name": "outputFileName",
        "prepare_run_order": "prepareRunOrder",
    },
)
class DeployCdkStackActionOptions:
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_af6d98e9,
        base_action_name: typing.Optional[str] = None,
        change_set_name: typing.Optional[str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_af6d98e9] = None,
        output_file_name: typing.Optional[str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Customization options for a DeployCdkStackAction.

        :param cloud_assembly_input: The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: Base name of the action. Default: stackName
        :param change_set_name: Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: Run order for the Prepare action. Default: 1

        stability
        :stability: experimental
        """
        self._values = {
            "cloud_assembly_input": cloud_assembly_input,
        }
        if base_action_name is not None:
            self._values["base_action_name"] = base_action_name
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if prepare_run_order is not None:
            self._values["prepare_run_order"] = prepare_run_order

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_af6d98e9:
        """The CodePipeline artifact that holds the Cloud Assembly.

        stability
        :stability: experimental
        """
        return self._values.get("cloud_assembly_input")

    @builtins.property
    def base_action_name(self) -> typing.Optional[str]:
        """Base name of the action.

        default
        :default: stackName

        stability
        :stability: experimental
        """
        return self._values.get("base_action_name")

    @builtins.property
    def change_set_name(self) -> typing.Optional[str]:
        """Name of the change set to create and deploy.

        default
        :default: 'PipelineChange'

        stability
        :stability: experimental
        """
        return self._values.get("change_set_name")

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        """Run order for the Execute action.

        default
        :default: - prepareRunOrder + 1

        stability
        :stability: experimental
        """
        return self._values.get("execute_run_order")

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_af6d98e9]:
        """Artifact to write Stack Outputs to.

        default
        :default: - No outputs

        stability
        :stability: experimental
        """
        return self._values.get("output")

    @builtins.property
    def output_file_name(self) -> typing.Optional[str]:
        """Filename in output to write Stack outputs to.

        default
        :default: - Required when 'output' is set

        stability
        :stability: experimental
        """
        return self._values.get("output_file_name")

    @builtins.property
    def prepare_run_order(self) -> typing.Optional[jsii.Number]:
        """Run order for the Prepare action.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get("prepare_run_order")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeployCdkStackActionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.DeployCdkStackActionProps",
    jsii_struct_bases=[DeployCdkStackActionOptions],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "base_action_name": "baseActionName",
        "change_set_name": "changeSetName",
        "execute_run_order": "executeRunOrder",
        "output": "output",
        "output_file_name": "outputFileName",
        "prepare_run_order": "prepareRunOrder",
        "action_role": "actionRole",
        "stack_name": "stackName",
        "template_path": "templatePath",
        "cloud_formation_execution_role": "cloudFormationExecutionRole",
        "dependency_stack_artifact_ids": "dependencyStackArtifactIds",
        "region": "region",
        "stack_artifact_id": "stackArtifactId",
    },
)
class DeployCdkStackActionProps(DeployCdkStackActionOptions):
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_af6d98e9,
        base_action_name: typing.Optional[str] = None,
        change_set_name: typing.Optional[str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_af6d98e9] = None,
        output_file_name: typing.Optional[str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
        action_role: _IRole_e69bbae4,
        stack_name: str,
        template_path: str,
        cloud_formation_execution_role: typing.Optional[_IRole_e69bbae4] = None,
        dependency_stack_artifact_ids: typing.Optional[typing.List[str]] = None,
        region: typing.Optional[str] = None,
        stack_artifact_id: typing.Optional[str] = None,
    ) -> None:
        """Properties for a DeployCdkStackAction.

        :param cloud_assembly_input: The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: Base name of the action. Default: stackName
        :param change_set_name: Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: Run order for the Prepare action. Default: 1
        :param action_role: Role for the action to assume. This controls the account to deploy into
        :param stack_name: The name of the stack that should be created/updated.
        :param template_path: Relative path of template in the input artifact.
        :param cloud_formation_execution_role: Role to execute CloudFormation under. Default: - Execute CloudFormation using the action role
        :param dependency_stack_artifact_ids: Artifact ID for the stacks this stack depends on. Used for pipeline order checking. Default: - No dependencies
        :param region: Region to deploy into. Default: - Same region as pipeline
        :param stack_artifact_id: Artifact ID for the stack deployed here. Used for pipeline order checking. Default: - Order will not be checked

        stability
        :stability: experimental
        """
        self._values = {
            "cloud_assembly_input": cloud_assembly_input,
            "action_role": action_role,
            "stack_name": stack_name,
            "template_path": template_path,
        }
        if base_action_name is not None:
            self._values["base_action_name"] = base_action_name
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if prepare_run_order is not None:
            self._values["prepare_run_order"] = prepare_run_order
        if cloud_formation_execution_role is not None:
            self._values["cloud_formation_execution_role"] = cloud_formation_execution_role
        if dependency_stack_artifact_ids is not None:
            self._values["dependency_stack_artifact_ids"] = dependency_stack_artifact_ids
        if region is not None:
            self._values["region"] = region
        if stack_artifact_id is not None:
            self._values["stack_artifact_id"] = stack_artifact_id

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_af6d98e9:
        """The CodePipeline artifact that holds the Cloud Assembly.

        stability
        :stability: experimental
        """
        return self._values.get("cloud_assembly_input")

    @builtins.property
    def base_action_name(self) -> typing.Optional[str]:
        """Base name of the action.

        default
        :default: stackName

        stability
        :stability: experimental
        """
        return self._values.get("base_action_name")

    @builtins.property
    def change_set_name(self) -> typing.Optional[str]:
        """Name of the change set to create and deploy.

        default
        :default: 'PipelineChange'

        stability
        :stability: experimental
        """
        return self._values.get("change_set_name")

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        """Run order for the Execute action.

        default
        :default: - prepareRunOrder + 1

        stability
        :stability: experimental
        """
        return self._values.get("execute_run_order")

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_af6d98e9]:
        """Artifact to write Stack Outputs to.

        default
        :default: - No outputs

        stability
        :stability: experimental
        """
        return self._values.get("output")

    @builtins.property
    def output_file_name(self) -> typing.Optional[str]:
        """Filename in output to write Stack outputs to.

        default
        :default: - Required when 'output' is set

        stability
        :stability: experimental
        """
        return self._values.get("output_file_name")

    @builtins.property
    def prepare_run_order(self) -> typing.Optional[jsii.Number]:
        """Run order for the Prepare action.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get("prepare_run_order")

    @builtins.property
    def action_role(self) -> _IRole_e69bbae4:
        """Role for the action to assume.

        This controls the account to deploy into

        stability
        :stability: experimental
        """
        return self._values.get("action_role")

    @builtins.property
    def stack_name(self) -> str:
        """The name of the stack that should be created/updated.

        stability
        :stability: experimental
        """
        return self._values.get("stack_name")

    @builtins.property
    def template_path(self) -> str:
        """Relative path of template in the input artifact.

        stability
        :stability: experimental
        """
        return self._values.get("template_path")

    @builtins.property
    def cloud_formation_execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role to execute CloudFormation under.

        default
        :default: - Execute CloudFormation using the action role

        stability
        :stability: experimental
        """
        return self._values.get("cloud_formation_execution_role")

    @builtins.property
    def dependency_stack_artifact_ids(self) -> typing.Optional[typing.List[str]]:
        """Artifact ID for the stacks this stack depends on.

        Used for pipeline order checking.

        default
        :default: - No dependencies

        stability
        :stability: experimental
        """
        return self._values.get("dependency_stack_artifact_ids")

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """Region to deploy into.

        default
        :default: - Same region as pipeline

        stability
        :stability: experimental
        """
        return self._values.get("region")

    @builtins.property
    def stack_artifact_id(self) -> typing.Optional[str]:
        """Artifact ID for the stack deployed here.

        Used for pipeline order checking.

        default
        :default: - Order will not be checked

        stability
        :stability: experimental
        """
        return self._values.get("stack_artifact_id")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeployCdkStackActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.FromStackArtifactOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "execute_run_order": "executeRunOrder",
        "output": "output",
        "output_file_name": "outputFileName",
        "prepare_run_order": "prepareRunOrder",
    },
)
class FromStackArtifactOptions:
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_af6d98e9,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_af6d98e9] = None,
        output_file_name: typing.Optional[str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        """Options for CdkDeployAction.fromStackArtifact.

        :param cloud_assembly_input: The CodePipeline artifact that holds the Cloud Assembly.
        :param execute_run_order: Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: Run order for the 2 actions that will be created. Default: 1

        stability
        :stability: experimental
        """
        self._values = {
            "cloud_assembly_input": cloud_assembly_input,
        }
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if prepare_run_order is not None:
            self._values["prepare_run_order"] = prepare_run_order

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_af6d98e9:
        """The CodePipeline artifact that holds the Cloud Assembly.

        stability
        :stability: experimental
        """
        return self._values.get("cloud_assembly_input")

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        """Run order for the Execute action.

        default
        :default: - prepareRunOrder + 1

        stability
        :stability: experimental
        """
        return self._values.get("execute_run_order")

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_af6d98e9]:
        """Artifact to write Stack Outputs to.

        default
        :default: - No outputs

        stability
        :stability: experimental
        """
        return self._values.get("output")

    @builtins.property
    def output_file_name(self) -> typing.Optional[str]:
        """Filename in output to write Stack outputs to.

        default
        :default: - Required when 'output' is set

        stability
        :stability: experimental
        """
        return self._values.get("output_file_name")

    @builtins.property
    def prepare_run_order(self) -> typing.Optional[jsii.Number]:
        """Run order for the 2 actions that will be created.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get("prepare_run_order")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FromStackArtifactOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk-experiment.pipelines.IStageHost")
class IStageHost(jsii.compat.Protocol):
    """Features that the Stage needs from its environment.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStageHostProxy

    @jsii.member(jsii_name="publishAsset")
    def publish_asset(
        self,
        *,
        asset_id: str,
        asset_manifest_path: str,
        asset_selector: str,
        asset_type: "AssetType",
    ) -> None:
        """Make sure all the assets from the given manifest are published.

        :param asset_id: Asset identifier.
        :param asset_manifest_path: Asset manifest path.
        :param asset_selector: Asset selector to pass to ``cdk-assets``.
        :param asset_type: Type of asset to publish.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="stackOutputArtifact")
    def stack_output_artifact(
        self, stack_artifact_id: str
    ) -> typing.Optional[_Artifact_af6d98e9]:
        """Return the Artifact the given stack has to emit its outputs into, if any.

        :param stack_artifact_id: -

        stability
        :stability: experimental
        """
        ...


class _IStageHostProxy:
    """Features that the Stage needs from its environment.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.pipelines.IStageHost"

    @jsii.member(jsii_name="publishAsset")
    def publish_asset(
        self,
        *,
        asset_id: str,
        asset_manifest_path: str,
        asset_selector: str,
        asset_type: "AssetType",
    ) -> None:
        """Make sure all the assets from the given manifest are published.

        :param asset_id: Asset identifier.
        :param asset_manifest_path: Asset manifest path.
        :param asset_selector: Asset selector to pass to ``cdk-assets``.
        :param asset_type: Type of asset to publish.

        stability
        :stability: experimental
        """
        command = AssetPublishingCommand(
            asset_id=asset_id,
            asset_manifest_path=asset_manifest_path,
            asset_selector=asset_selector,
            asset_type=asset_type,
        )

        return jsii.invoke(self, "publishAsset", [command])

    @jsii.member(jsii_name="stackOutputArtifact")
    def stack_output_artifact(
        self, stack_artifact_id: str
    ) -> typing.Optional[_Artifact_af6d98e9]:
        """Return the Artifact the given stack has to emit its outputs into, if any.

        :param stack_artifact_id: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "stackOutputArtifact", [stack_artifact_id])


@jsii.implements(_IAction_369e77ae)
class PublishAssetsAction(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.pipelines.PublishAssetsAction",
):
    """Action to publish an asset in the pipeline.

    Creates a CodeBuild project which will use the CDK CLI
    to prepare and publish the asset.

    You do not need to instantiate this action -- it will automatically
    be added by the pipeline when you add stacks that use assets.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        action_name: str,
        asset_type: "AssetType",
        cloud_assembly_input: _Artifact_af6d98e9,
        cdk_cli_version: typing.Optional[str] = None,
        project_name: typing.Optional[str] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param action_name: Name of publishing action.
        :param asset_type: AssetType we're publishing.
        :param cloud_assembly_input: The CodePipeline artifact that holds the Cloud Assembly.
        :param cdk_cli_version: Version of CDK CLI to 'npm install'. Default: - Latest version
        :param project_name: Name of the CodeBuild project. Default: - Automatically generated
        :param role: Role to use for CodePipeline and CodeBuild to build and publish the assets. Default: - Automatically generated

        stability
        :stability: experimental
        """
        props = PublishAssetsActionProps(
            action_name=action_name,
            asset_type=asset_type,
            cloud_assembly_input=cloud_assembly_input,
            cdk_cli_version=cdk_cli_version,
            project_name=project_name,
            role=role,
        )

        jsii.create(PublishAssetsAction, self, [scope, id, props])

    @jsii.member(jsii_name="addPublishCommand")
    def add_publish_command(
        self, relative_manifest_path: str, asset_selector: str
    ) -> None:
        """Add a single publishing command.

        Manifest path should be relative to the root Cloud Assembly.

        :param relative_manifest_path: -
        :param asset_selector: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addPublishCommand", [relative_manifest_path, asset_selector])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_f50a3f53,
        stage: _IStage_b7c853a7,
        *,
        bucket: _IBucket_25bad983,
        role: _IRole_e69bbae4,
    ) -> _ActionConfig_c379766c:
        """Exists to implement IAction.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bind", [scope, stage, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: str,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
        *,
        description: typing.Optional[str] = None,
        enabled: typing.Optional[bool] = None,
        event_bus: typing.Optional[_IEventBus_ed4f1700] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        schedule: typing.Optional[_Schedule_11a70620] = None,
        targets: typing.Optional[typing.List[_IRuleTarget_41800a77]] = None,
    ) -> _Rule_c38e0b39:
        """Exists to implement IAction.

        :param name: -
        :param target: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        stability
        :stability: experimental
        """
        options = _RuleProps_d60f0abf(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return jsii.invoke(self, "onStateChange", [name, target, options])

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_8f5d7a9d:
        """Exists to implement IAction.

        stability
        :stability: experimental
        """
        return jsii.get(self, "actionProperties")


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.PublishAssetsActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_name": "actionName",
        "asset_type": "assetType",
        "cloud_assembly_input": "cloudAssemblyInput",
        "cdk_cli_version": "cdkCliVersion",
        "project_name": "projectName",
        "role": "role",
    },
)
class PublishAssetsActionProps:
    def __init__(
        self,
        *,
        action_name: str,
        asset_type: "AssetType",
        cloud_assembly_input: _Artifact_af6d98e9,
        cdk_cli_version: typing.Optional[str] = None,
        project_name: typing.Optional[str] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
    ) -> None:
        """Props for a PublishAssetsAction.

        :param action_name: Name of publishing action.
        :param asset_type: AssetType we're publishing.
        :param cloud_assembly_input: The CodePipeline artifact that holds the Cloud Assembly.
        :param cdk_cli_version: Version of CDK CLI to 'npm install'. Default: - Latest version
        :param project_name: Name of the CodeBuild project. Default: - Automatically generated
        :param role: Role to use for CodePipeline and CodeBuild to build and publish the assets. Default: - Automatically generated

        stability
        :stability: experimental
        """
        self._values = {
            "action_name": action_name,
            "asset_type": asset_type,
            "cloud_assembly_input": cloud_assembly_input,
        }
        if cdk_cli_version is not None:
            self._values["cdk_cli_version"] = cdk_cli_version
        if project_name is not None:
            self._values["project_name"] = project_name
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def action_name(self) -> str:
        """Name of publishing action.

        stability
        :stability: experimental
        """
        return self._values.get("action_name")

    @builtins.property
    def asset_type(self) -> "AssetType":
        """AssetType we're publishing.

        stability
        :stability: experimental
        """
        return self._values.get("asset_type")

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_af6d98e9:
        """The CodePipeline artifact that holds the Cloud Assembly.

        stability
        :stability: experimental
        """
        return self._values.get("cloud_assembly_input")

    @builtins.property
    def cdk_cli_version(self) -> typing.Optional[str]:
        """Version of CDK CLI to 'npm install'.

        default
        :default: - Latest version

        stability
        :stability: experimental
        """
        return self._values.get("cdk_cli_version")

    @builtins.property
    def project_name(self) -> typing.Optional[str]:
        """Name of the CodeBuild project.

        default
        :default: - Automatically generated

        stability
        :stability: experimental
        """
        return self._values.get("project_name")

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role to use for CodePipeline and CodeBuild to build and publish the assets.

        default
        :default: - Automatically generated

        stability
        :stability: experimental
        """
        return self._values.get("role")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PublishAssetsActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_369e77ae)
class ShellScriptAction(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.pipelines.ShellScriptAction"
):
    """Validate a revision using shell commands.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        *,
        action_name: str,
        commands: typing.List[str],
        additional_artifacts: typing.Optional[typing.List[_Artifact_af6d98e9]] = None,
        bash_options: typing.Optional[str] = None,
        run_order: typing.Optional[jsii.Number] = None,
        use_outputs: typing.Optional[typing.Mapping[str, "StackOutput"]] = None,
    ) -> None:
        """
        :param action_name: Name of the validation action in the pipeline.
        :param commands: Commands to run.
        :param additional_artifacts: Additional artifacts to use as input for the CodeBuild project. You can use these files to load more complex test sets into the shellscript build environment. The files artifact given here will be unpacked into the current working directory, the other ones will be unpacked into directories which are available through the environment variables $CODEBUILD_SRC_DIR_. The CodeBuild job must have at least one input artifact, so you must provide either at least one additional artifact here or one stack output using ``useOutput``. Default: - No additional artifacts
        :param bash_options: Bash options to set at the start of the script. Default: '-eu' (errexit and nounset)
        :param run_order: RunOrder for this action. Use this to sequence the shell script after the deployments. The default value is 100 so you don't have to supply the value if you just want to run this after the application stacks have been deployed, and you don't have more than 100 stacks. Default: 100
        :param use_outputs: Stack outputs to make available as environment variables. Default: - No outputs used

        stability
        :stability: experimental
        """
        props = ShellScriptActionProps(
            action_name=action_name,
            commands=commands,
            additional_artifacts=additional_artifacts,
            bash_options=bash_options,
            run_order=run_order,
            use_outputs=use_outputs,
        )

        jsii.create(ShellScriptAction, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_f50a3f53,
        stage: _IStage_b7c853a7,
        *,
        bucket: _IBucket_25bad983,
        role: _IRole_e69bbae4,
    ) -> _ActionConfig_c379766c:
        """Exists to implement IAction.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bind", [scope, stage, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: str,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
        *,
        description: typing.Optional[str] = None,
        enabled: typing.Optional[bool] = None,
        event_bus: typing.Optional[_IEventBus_ed4f1700] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        schedule: typing.Optional[_Schedule_11a70620] = None,
        targets: typing.Optional[typing.List[_IRuleTarget_41800a77]] = None,
    ) -> _Rule_c38e0b39:
        """Exists to implement IAction.

        :param name: -
        :param target: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        stability
        :stability: experimental
        """
        options = _RuleProps_d60f0abf(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return jsii.invoke(self, "onStateChange", [name, target, options])

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_8f5d7a9d:
        """Exists to implement IAction.

        stability
        :stability: experimental
        """
        return jsii.get(self, "actionProperties")

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> _IProject_2a66e54e:
        """Project generated to run the shell script in.

        stability
        :stability: experimental
        """
        return jsii.get(self, "project")


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.ShellScriptActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_name": "actionName",
        "commands": "commands",
        "additional_artifacts": "additionalArtifacts",
        "bash_options": "bashOptions",
        "run_order": "runOrder",
        "use_outputs": "useOutputs",
    },
)
class ShellScriptActionProps:
    def __init__(
        self,
        *,
        action_name: str,
        commands: typing.List[str],
        additional_artifacts: typing.Optional[typing.List[_Artifact_af6d98e9]] = None,
        bash_options: typing.Optional[str] = None,
        run_order: typing.Optional[jsii.Number] = None,
        use_outputs: typing.Optional[typing.Mapping[str, "StackOutput"]] = None,
    ) -> None:
        """Properties for ShellScriptValidation.

        :param action_name: Name of the validation action in the pipeline.
        :param commands: Commands to run.
        :param additional_artifacts: Additional artifacts to use as input for the CodeBuild project. You can use these files to load more complex test sets into the shellscript build environment. The files artifact given here will be unpacked into the current working directory, the other ones will be unpacked into directories which are available through the environment variables $CODEBUILD_SRC_DIR_. The CodeBuild job must have at least one input artifact, so you must provide either at least one additional artifact here or one stack output using ``useOutput``. Default: - No additional artifacts
        :param bash_options: Bash options to set at the start of the script. Default: '-eu' (errexit and nounset)
        :param run_order: RunOrder for this action. Use this to sequence the shell script after the deployments. The default value is 100 so you don't have to supply the value if you just want to run this after the application stacks have been deployed, and you don't have more than 100 stacks. Default: 100
        :param use_outputs: Stack outputs to make available as environment variables. Default: - No outputs used

        stability
        :stability: experimental
        """
        self._values = {
            "action_name": action_name,
            "commands": commands,
        }
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if bash_options is not None:
            self._values["bash_options"] = bash_options
        if run_order is not None:
            self._values["run_order"] = run_order
        if use_outputs is not None:
            self._values["use_outputs"] = use_outputs

    @builtins.property
    def action_name(self) -> str:
        """Name of the validation action in the pipeline.

        stability
        :stability: experimental
        """
        return self._values.get("action_name")

    @builtins.property
    def commands(self) -> typing.List[str]:
        """Commands to run.

        stability
        :stability: experimental
        """
        return self._values.get("commands")

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[_Artifact_af6d98e9]]:
        """Additional artifacts to use as input for the CodeBuild project.

        You can use these files to load more complex test sets into the
        shellscript build environment.

        The files artifact given here will be unpacked into the current
        working directory, the other ones will be unpacked into directories
        which are available through the environment variables
        $CODEBUILD_SRC_DIR_.

        The CodeBuild job must have at least one input artifact, so you
        must provide either at least one additional artifact here or one
        stack output using ``useOutput``.

        default
        :default: - No additional artifacts

        stability
        :stability: experimental
        """
        return self._values.get("additional_artifacts")

    @builtins.property
    def bash_options(self) -> typing.Optional[str]:
        """Bash options to set at the start of the script.

        default
        :default: '-eu' (errexit and nounset)

        stability
        :stability: experimental
        """
        return self._values.get("bash_options")

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        """RunOrder for this action.

        Use this to sequence the shell script after the deployments.

        The default value is 100 so you don't have to supply the value if you just
        want to run this after the application stacks have been deployed, and you
        don't have more than 100 stacks.

        default
        :default: 100

        stability
        :stability: experimental
        """
        return self._values.get("run_order")

    @builtins.property
    def use_outputs(self) -> typing.Optional[typing.Mapping[str, "StackOutput"]]:
        """Stack outputs to make available as environment variables.

        default
        :default: - No outputs used

        stability
        :stability: experimental
        """
        return self._values.get("use_outputs")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ShellScriptActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_369e77ae)
class SimpleSynthAction(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.pipelines.SimpleSynthAction"
):
    """A standard synth with a generated buildspec.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        *,
        synth_command: str,
        build_command: typing.Optional[str] = None,
        build_commands: typing.Optional[typing.List[str]] = None,
        install_command: typing.Optional[str] = None,
        install_commands: typing.Optional[typing.List[str]] = None,
        test_commands: typing.Optional[typing.List[str]] = None,
        cloud_assembly_artifact: _Artifact_af6d98e9,
        source_artifact: _Artifact_af6d98e9,
        action_name: typing.Optional[str] = None,
        additional_artifacts: typing.Optional[typing.List["AdditionalArtifact"]] = None,
        copy_environment_variables: typing.Optional[typing.List[str]] = None,
        environment: typing.Optional[_BuildEnvironment_3f2fec35] = None,
        environment_variables: typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]] = None,
        project_name: typing.Optional[str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_f75dc775]] = None,
        subdirectory: typing.Optional[str] = None,
    ) -> None:
        """
        :param synth_command: The synth command.
        :param build_command: The build command. If your programming language requires a compilation step, put the compilation command here. Default: - No build required
        :param build_commands: The build commands. If your programming language requires a compilation step, put the compilation command here. Default: - No build required
        :param install_command: The install command. If not provided by the build image or another dependency management tool, at least install the CDK CLI here using ``npm install -g aws-cdk``. Default: - No install required
        :param install_commands: Install commands. If not provided by the build image or another dependency management tool, at least install the CDK CLI here using ``npm install -g aws-cdk``. Default: - No install required
        :param test_commands: Test commands. These commands are run after the build commands but before the synth command. Default: - No test commands
        :param cloud_assembly_artifact: The artifact where the CloudAssembly should be emitted.
        :param source_artifact: The source artifact of the CodePipeline.
        :param action_name: Name of the build action. Default: 'Synth'
        :param additional_artifacts: Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: Environment variables to send into build. Default: - No additional environment variables
        :param project_name: Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: Directory inside the source where package.json and cdk.json are located. Default: - Repository root

        stability
        :stability: experimental
        """
        props = SimpleSynthActionProps(
            synth_command=synth_command,
            build_command=build_command,
            build_commands=build_commands,
            install_command=install_command,
            install_commands=install_commands,
            test_commands=test_commands,
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_artifact=source_artifact,
            action_name=action_name,
            additional_artifacts=additional_artifacts,
            copy_environment_variables=copy_environment_variables,
            environment=environment,
            environment_variables=environment_variables,
            project_name=project_name,
            role_policy_statements=role_policy_statements,
            subdirectory=subdirectory,
        )

        jsii.create(SimpleSynthAction, self, [props])

    @jsii.member(jsii_name="standardNpmSynth")
    @builtins.classmethod
    def standard_npm_synth(
        cls,
        *,
        build_command: typing.Optional[str] = None,
        install_command: typing.Optional[str] = None,
        synth_command: typing.Optional[str] = None,
        cloud_assembly_artifact: _Artifact_af6d98e9,
        source_artifact: _Artifact_af6d98e9,
        action_name: typing.Optional[str] = None,
        additional_artifacts: typing.Optional[typing.List["AdditionalArtifact"]] = None,
        copy_environment_variables: typing.Optional[typing.List[str]] = None,
        environment: typing.Optional[_BuildEnvironment_3f2fec35] = None,
        environment_variables: typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]] = None,
        project_name: typing.Optional[str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_f75dc775]] = None,
        subdirectory: typing.Optional[str] = None,
    ) -> "SimpleSynthAction":
        """Create a standard NPM synth action.

        Uses ``npm ci`` to install dependencies and ``npx cdk synth`` to synthesize.

        If you need a build step, add ``buildCommand: 'npm run build'``.

        :param build_command: The build command. By default, we assume NPM projects are either written in JavaScript or are using ``ts-node``, so don't need a build command. Otherwise, put the build command here, for example ``npm run build``. Default: - No build required
        :param install_command: The install command. Default: 'npm ci'
        :param synth_command: The synth command. Default: 'npx cdk synth'
        :param cloud_assembly_artifact: The artifact where the CloudAssembly should be emitted.
        :param source_artifact: The source artifact of the CodePipeline.
        :param action_name: Name of the build action. Default: 'Synth'
        :param additional_artifacts: Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: Environment variables to send into build. Default: - No additional environment variables
        :param project_name: Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: Directory inside the source where package.json and cdk.json are located. Default: - Repository root

        stability
        :stability: experimental
        """
        options = StandardNpmSynthOptions(
            build_command=build_command,
            install_command=install_command,
            synth_command=synth_command,
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_artifact=source_artifact,
            action_name=action_name,
            additional_artifacts=additional_artifacts,
            copy_environment_variables=copy_environment_variables,
            environment=environment,
            environment_variables=environment_variables,
            project_name=project_name,
            role_policy_statements=role_policy_statements,
            subdirectory=subdirectory,
        )

        return jsii.sinvoke(cls, "standardNpmSynth", [options])

    @jsii.member(jsii_name="standardYarnSynth")
    @builtins.classmethod
    def standard_yarn_synth(
        cls,
        *,
        build_command: typing.Optional[str] = None,
        install_command: typing.Optional[str] = None,
        synth_command: typing.Optional[str] = None,
        cloud_assembly_artifact: _Artifact_af6d98e9,
        source_artifact: _Artifact_af6d98e9,
        action_name: typing.Optional[str] = None,
        additional_artifacts: typing.Optional[typing.List["AdditionalArtifact"]] = None,
        copy_environment_variables: typing.Optional[typing.List[str]] = None,
        environment: typing.Optional[_BuildEnvironment_3f2fec35] = None,
        environment_variables: typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]] = None,
        project_name: typing.Optional[str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_f75dc775]] = None,
        subdirectory: typing.Optional[str] = None,
    ) -> "SimpleSynthAction":
        """Create a standard Yarn synth action.

        Uses ``yarn install --frozen-lockfile`` to install dependencies and ``npx cdk synth`` to synthesize.

        If you need a build step, add ``buildCommand: 'yarn build'``.

        :param build_command: The build command. By default, we assume NPM projects are either written in JavaScript or are using ``ts-node``, so don't need a build command. Otherwise, put the build command here, for example ``npm run build``. Default: - No build required
        :param install_command: The install command. Default: 'yarn install --frozen-lockfile'
        :param synth_command: The synth command. Default: 'npx cdk synth'
        :param cloud_assembly_artifact: The artifact where the CloudAssembly should be emitted.
        :param source_artifact: The source artifact of the CodePipeline.
        :param action_name: Name of the build action. Default: 'Synth'
        :param additional_artifacts: Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: Environment variables to send into build. Default: - No additional environment variables
        :param project_name: Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: Directory inside the source where package.json and cdk.json are located. Default: - Repository root

        stability
        :stability: experimental
        """
        options = StandardYarnSynthOptions(
            build_command=build_command,
            install_command=install_command,
            synth_command=synth_command,
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_artifact=source_artifact,
            action_name=action_name,
            additional_artifacts=additional_artifacts,
            copy_environment_variables=copy_environment_variables,
            environment=environment,
            environment_variables=environment_variables,
            project_name=project_name,
            role_policy_statements=role_policy_statements,
            subdirectory=subdirectory,
        )

        return jsii.sinvoke(cls, "standardYarnSynth", [options])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_f50a3f53,
        stage: _IStage_b7c853a7,
        *,
        bucket: _IBucket_25bad983,
        role: _IRole_e69bbae4,
    ) -> _ActionConfig_c379766c:
        """Exists to implement IAction.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bind", [scope, stage, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: str,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
        *,
        description: typing.Optional[str] = None,
        enabled: typing.Optional[bool] = None,
        event_bus: typing.Optional[_IEventBus_ed4f1700] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        schedule: typing.Optional[_Schedule_11a70620] = None,
        targets: typing.Optional[typing.List[_IRuleTarget_41800a77]] = None,
    ) -> _Rule_c38e0b39:
        """Exists to implement IAction.

        :param name: -
        :param target: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        stability
        :stability: experimental
        """
        options = _RuleProps_d60f0abf(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return jsii.invoke(self, "onStateChange", [name, target, options])

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_8f5d7a9d:
        """Exists to implement IAction.

        stability
        :stability: experimental
        """
        return jsii.get(self, "actionProperties")


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.SimpleSynthOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "source_artifact": "sourceArtifact",
        "action_name": "actionName",
        "additional_artifacts": "additionalArtifacts",
        "copy_environment_variables": "copyEnvironmentVariables",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
        "role_policy_statements": "rolePolicyStatements",
        "subdirectory": "subdirectory",
    },
)
class SimpleSynthOptions:
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_af6d98e9,
        source_artifact: _Artifact_af6d98e9,
        action_name: typing.Optional[str] = None,
        additional_artifacts: typing.Optional[typing.List["AdditionalArtifact"]] = None,
        copy_environment_variables: typing.Optional[typing.List[str]] = None,
        environment: typing.Optional[_BuildEnvironment_3f2fec35] = None,
        environment_variables: typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]] = None,
        project_name: typing.Optional[str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_f75dc775]] = None,
        subdirectory: typing.Optional[str] = None,
    ) -> None:
        """Configuration options for a SimpleSynth.

        :param cloud_assembly_artifact: The artifact where the CloudAssembly should be emitted.
        :param source_artifact: The source artifact of the CodePipeline.
        :param action_name: Name of the build action. Default: 'Synth'
        :param additional_artifacts: Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: Environment variables to send into build. Default: - No additional environment variables
        :param project_name: Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: Directory inside the source where package.json and cdk.json are located. Default: - Repository root

        stability
        :stability: experimental
        """
        if isinstance(environment, dict):
            environment = _BuildEnvironment_3f2fec35(**environment)
        self._values = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "source_artifact": source_artifact,
        }
        if action_name is not None:
            self._values["action_name"] = action_name
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if copy_environment_variables is not None:
            self._values["copy_environment_variables"] = copy_environment_variables
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_af6d98e9:
        """The artifact where the CloudAssembly should be emitted.

        stability
        :stability: experimental
        """
        return self._values.get("cloud_assembly_artifact")

    @builtins.property
    def source_artifact(self) -> _Artifact_af6d98e9:
        """The source artifact of the CodePipeline.

        stability
        :stability: experimental
        """
        return self._values.get("source_artifact")

    @builtins.property
    def action_name(self) -> typing.Optional[str]:
        """Name of the build action.

        default
        :default: 'Synth'

        stability
        :stability: experimental
        """
        return self._values.get("action_name")

    @builtins.property
    def additional_artifacts(
        self,
    ) -> typing.Optional[typing.List["AdditionalArtifact"]]:
        """Produce additional output artifacts after the build based on the given directories.

        Can be used to produce additional artifacts during the build step,
        separate from the cloud assembly, which can be used further on in the
        pipeline.

        Directories are evaluated with respect to ``subdirectory``.

        default
        :default: - No additional artifacts generated

        stability
        :stability: experimental
        """
        return self._values.get("additional_artifacts")

    @builtins.property
    def copy_environment_variables(self) -> typing.Optional[typing.List[str]]:
        """Environment variables to copy over from parent env.

        These are environment variables that are being used by the build.

        default
        :default: - No environment variables copied

        stability
        :stability: experimental
        """
        return self._values.get("copy_environment_variables")

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_3f2fec35]:
        """Build environment to use for CodeBuild job.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0

        stability
        :stability: experimental
        """
        return self._values.get("environment")

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]]:
        """Environment variables to send into build.

        default
        :default: - No additional environment variables

        stability
        :stability: experimental
        """
        return self._values.get("environment_variables")

    @builtins.property
    def project_name(self) -> typing.Optional[str]:
        """Name of the CodeBuild project.

        default
        :default: - Automatically generated

        stability
        :stability: experimental
        """
        return self._values.get("project_name")

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_f75dc775]]:
        """Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        default
        :default: - No policy statements added to CodeBuild Project Role

        stability
        :stability: experimental
        """
        return self._values.get("role_policy_statements")

    @builtins.property
    def subdirectory(self) -> typing.Optional[str]:
        """Directory inside the source where package.json and cdk.json are located.

        default
        :default: - Repository root

        stability
        :stability: experimental
        """
        return self._values.get("subdirectory")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SimpleSynthOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackOutput(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.pipelines.StackOutput"
):
    """A single output of a Stack.

    stability
    :stability: experimental
    """

    def __init__(self, artifact_file: _ArtifactPath_8730c13b, output_name: str) -> None:
        """Build a StackOutput from a known artifact and an output name.

        :param artifact_file: -
        :param output_name: -

        stability
        :stability: experimental
        """
        jsii.create(StackOutput, self, [artifact_file, output_name])

    @builtins.property
    @jsii.member(jsii_name="artifactFile")
    def artifact_file(self) -> _ArtifactPath_8730c13b:
        """The artifact and file the output is stored in.

        stability
        :stability: experimental
        """
        return jsii.get(self, "artifactFile")

    @builtins.property
    @jsii.member(jsii_name="outputName")
    def output_name(self) -> str:
        """The name of the output in the JSON object in the file.

        stability
        :stability: experimental
        """
        return jsii.get(self, "outputName")


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.StandardNpmSynthOptions",
    jsii_struct_bases=[SimpleSynthOptions],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "source_artifact": "sourceArtifact",
        "action_name": "actionName",
        "additional_artifacts": "additionalArtifacts",
        "copy_environment_variables": "copyEnvironmentVariables",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
        "role_policy_statements": "rolePolicyStatements",
        "subdirectory": "subdirectory",
        "build_command": "buildCommand",
        "install_command": "installCommand",
        "synth_command": "synthCommand",
    },
)
class StandardNpmSynthOptions(SimpleSynthOptions):
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_af6d98e9,
        source_artifact: _Artifact_af6d98e9,
        action_name: typing.Optional[str] = None,
        additional_artifacts: typing.Optional[typing.List["AdditionalArtifact"]] = None,
        copy_environment_variables: typing.Optional[typing.List[str]] = None,
        environment: typing.Optional[_BuildEnvironment_3f2fec35] = None,
        environment_variables: typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]] = None,
        project_name: typing.Optional[str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_f75dc775]] = None,
        subdirectory: typing.Optional[str] = None,
        build_command: typing.Optional[str] = None,
        install_command: typing.Optional[str] = None,
        synth_command: typing.Optional[str] = None,
    ) -> None:
        """Options for a convention-based synth using NPM.

        :param cloud_assembly_artifact: The artifact where the CloudAssembly should be emitted.
        :param source_artifact: The source artifact of the CodePipeline.
        :param action_name: Name of the build action. Default: 'Synth'
        :param additional_artifacts: Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: Environment variables to send into build. Default: - No additional environment variables
        :param project_name: Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param build_command: The build command. By default, we assume NPM projects are either written in JavaScript or are using ``ts-node``, so don't need a build command. Otherwise, put the build command here, for example ``npm run build``. Default: - No build required
        :param install_command: The install command. Default: 'npm ci'
        :param synth_command: The synth command. Default: 'npx cdk synth'

        stability
        :stability: experimental
        """
        if isinstance(environment, dict):
            environment = _BuildEnvironment_3f2fec35(**environment)
        self._values = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "source_artifact": source_artifact,
        }
        if action_name is not None:
            self._values["action_name"] = action_name
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if copy_environment_variables is not None:
            self._values["copy_environment_variables"] = copy_environment_variables
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if build_command is not None:
            self._values["build_command"] = build_command
        if install_command is not None:
            self._values["install_command"] = install_command
        if synth_command is not None:
            self._values["synth_command"] = synth_command

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_af6d98e9:
        """The artifact where the CloudAssembly should be emitted.

        stability
        :stability: experimental
        """
        return self._values.get("cloud_assembly_artifact")

    @builtins.property
    def source_artifact(self) -> _Artifact_af6d98e9:
        """The source artifact of the CodePipeline.

        stability
        :stability: experimental
        """
        return self._values.get("source_artifact")

    @builtins.property
    def action_name(self) -> typing.Optional[str]:
        """Name of the build action.

        default
        :default: 'Synth'

        stability
        :stability: experimental
        """
        return self._values.get("action_name")

    @builtins.property
    def additional_artifacts(
        self,
    ) -> typing.Optional[typing.List["AdditionalArtifact"]]:
        """Produce additional output artifacts after the build based on the given directories.

        Can be used to produce additional artifacts during the build step,
        separate from the cloud assembly, which can be used further on in the
        pipeline.

        Directories are evaluated with respect to ``subdirectory``.

        default
        :default: - No additional artifacts generated

        stability
        :stability: experimental
        """
        return self._values.get("additional_artifacts")

    @builtins.property
    def copy_environment_variables(self) -> typing.Optional[typing.List[str]]:
        """Environment variables to copy over from parent env.

        These are environment variables that are being used by the build.

        default
        :default: - No environment variables copied

        stability
        :stability: experimental
        """
        return self._values.get("copy_environment_variables")

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_3f2fec35]:
        """Build environment to use for CodeBuild job.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0

        stability
        :stability: experimental
        """
        return self._values.get("environment")

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]]:
        """Environment variables to send into build.

        default
        :default: - No additional environment variables

        stability
        :stability: experimental
        """
        return self._values.get("environment_variables")

    @builtins.property
    def project_name(self) -> typing.Optional[str]:
        """Name of the CodeBuild project.

        default
        :default: - Automatically generated

        stability
        :stability: experimental
        """
        return self._values.get("project_name")

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_f75dc775]]:
        """Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        default
        :default: - No policy statements added to CodeBuild Project Role

        stability
        :stability: experimental
        """
        return self._values.get("role_policy_statements")

    @builtins.property
    def subdirectory(self) -> typing.Optional[str]:
        """Directory inside the source where package.json and cdk.json are located.

        default
        :default: - Repository root

        stability
        :stability: experimental
        """
        return self._values.get("subdirectory")

    @builtins.property
    def build_command(self) -> typing.Optional[str]:
        """The build command.

        By default, we assume NPM projects are either written in JavaScript or are
        using ``ts-node``, so don't need a build command.

        Otherwise, put the build command here, for example ``npm run build``.

        default
        :default: - No build required

        stability
        :stability: experimental
        """
        return self._values.get("build_command")

    @builtins.property
    def install_command(self) -> typing.Optional[str]:
        """The install command.

        default
        :default: 'npm ci'

        stability
        :stability: experimental
        """
        return self._values.get("install_command")

    @builtins.property
    def synth_command(self) -> typing.Optional[str]:
        """The synth command.

        default
        :default: 'npx cdk synth'

        stability
        :stability: experimental
        """
        return self._values.get("synth_command")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StandardNpmSynthOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.StandardYarnSynthOptions",
    jsii_struct_bases=[SimpleSynthOptions],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "source_artifact": "sourceArtifact",
        "action_name": "actionName",
        "additional_artifacts": "additionalArtifacts",
        "copy_environment_variables": "copyEnvironmentVariables",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
        "role_policy_statements": "rolePolicyStatements",
        "subdirectory": "subdirectory",
        "build_command": "buildCommand",
        "install_command": "installCommand",
        "synth_command": "synthCommand",
    },
)
class StandardYarnSynthOptions(SimpleSynthOptions):
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_af6d98e9,
        source_artifact: _Artifact_af6d98e9,
        action_name: typing.Optional[str] = None,
        additional_artifacts: typing.Optional[typing.List["AdditionalArtifact"]] = None,
        copy_environment_variables: typing.Optional[typing.List[str]] = None,
        environment: typing.Optional[_BuildEnvironment_3f2fec35] = None,
        environment_variables: typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]] = None,
        project_name: typing.Optional[str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_f75dc775]] = None,
        subdirectory: typing.Optional[str] = None,
        build_command: typing.Optional[str] = None,
        install_command: typing.Optional[str] = None,
        synth_command: typing.Optional[str] = None,
    ) -> None:
        """Options for a convention-based synth using Yarn.

        :param cloud_assembly_artifact: The artifact where the CloudAssembly should be emitted.
        :param source_artifact: The source artifact of the CodePipeline.
        :param action_name: Name of the build action. Default: 'Synth'
        :param additional_artifacts: Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: Environment variables to send into build. Default: - No additional environment variables
        :param project_name: Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param build_command: The build command. By default, we assume NPM projects are either written in JavaScript or are using ``ts-node``, so don't need a build command. Otherwise, put the build command here, for example ``npm run build``. Default: - No build required
        :param install_command: The install command. Default: 'yarn install --frozen-lockfile'
        :param synth_command: The synth command. Default: 'npx cdk synth'

        stability
        :stability: experimental
        """
        if isinstance(environment, dict):
            environment = _BuildEnvironment_3f2fec35(**environment)
        self._values = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "source_artifact": source_artifact,
        }
        if action_name is not None:
            self._values["action_name"] = action_name
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if copy_environment_variables is not None:
            self._values["copy_environment_variables"] = copy_environment_variables
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if build_command is not None:
            self._values["build_command"] = build_command
        if install_command is not None:
            self._values["install_command"] = install_command
        if synth_command is not None:
            self._values["synth_command"] = synth_command

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_af6d98e9:
        """The artifact where the CloudAssembly should be emitted.

        stability
        :stability: experimental
        """
        return self._values.get("cloud_assembly_artifact")

    @builtins.property
    def source_artifact(self) -> _Artifact_af6d98e9:
        """The source artifact of the CodePipeline.

        stability
        :stability: experimental
        """
        return self._values.get("source_artifact")

    @builtins.property
    def action_name(self) -> typing.Optional[str]:
        """Name of the build action.

        default
        :default: 'Synth'

        stability
        :stability: experimental
        """
        return self._values.get("action_name")

    @builtins.property
    def additional_artifacts(
        self,
    ) -> typing.Optional[typing.List["AdditionalArtifact"]]:
        """Produce additional output artifacts after the build based on the given directories.

        Can be used to produce additional artifacts during the build step,
        separate from the cloud assembly, which can be used further on in the
        pipeline.

        Directories are evaluated with respect to ``subdirectory``.

        default
        :default: - No additional artifacts generated

        stability
        :stability: experimental
        """
        return self._values.get("additional_artifacts")

    @builtins.property
    def copy_environment_variables(self) -> typing.Optional[typing.List[str]]:
        """Environment variables to copy over from parent env.

        These are environment variables that are being used by the build.

        default
        :default: - No environment variables copied

        stability
        :stability: experimental
        """
        return self._values.get("copy_environment_variables")

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_3f2fec35]:
        """Build environment to use for CodeBuild job.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0

        stability
        :stability: experimental
        """
        return self._values.get("environment")

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]]:
        """Environment variables to send into build.

        default
        :default: - No additional environment variables

        stability
        :stability: experimental
        """
        return self._values.get("environment_variables")

    @builtins.property
    def project_name(self) -> typing.Optional[str]:
        """Name of the CodeBuild project.

        default
        :default: - Automatically generated

        stability
        :stability: experimental
        """
        return self._values.get("project_name")

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_f75dc775]]:
        """Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        default
        :default: - No policy statements added to CodeBuild Project Role

        stability
        :stability: experimental
        """
        return self._values.get("role_policy_statements")

    @builtins.property
    def subdirectory(self) -> typing.Optional[str]:
        """Directory inside the source where package.json and cdk.json are located.

        default
        :default: - Repository root

        stability
        :stability: experimental
        """
        return self._values.get("subdirectory")

    @builtins.property
    def build_command(self) -> typing.Optional[str]:
        """The build command.

        By default, we assume NPM projects are either written in JavaScript or are
        using ``ts-node``, so don't need a build command.

        Otherwise, put the build command here, for example ``npm run build``.

        default
        :default: - No build required

        stability
        :stability: experimental
        """
        return self._values.get("build_command")

    @builtins.property
    def install_command(self) -> typing.Optional[str]:
        """The install command.

        default
        :default: 'yarn install --frozen-lockfile'

        stability
        :stability: experimental
        """
        return self._values.get("install_command")

    @builtins.property
    def synth_command(self) -> typing.Optional[str]:
        """The synth command.

        default
        :default: 'npx cdk synth'

        stability
        :stability: experimental
        """
        return self._values.get("synth_command")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StandardYarnSynthOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_369e77ae)
class UpdatePipelineAction(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.pipelines.UpdatePipelineAction",
):
    """Action to self-mutate the pipeline.

    Creates a CodeBuild project which will use the CDK CLI
    to deploy the pipeline stack.

    You do not need to instantiate this action -- it will automatically
    be added by the pipeline.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cloud_assembly_input: _Artifact_af6d98e9,
        pipeline_stack_name: str,
        cdk_cli_version: typing.Optional[str] = None,
        project_name: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cloud_assembly_input: The CodePipeline artifact that holds the Cloud Assembly.
        :param pipeline_stack_name: Name of the pipeline stack.
        :param cdk_cli_version: Version of CDK CLI to 'npm install'. Default: - Latest version
        :param project_name: Name of the CodeBuild project. Default: - Automatically generated

        stability
        :stability: experimental
        """
        props = UpdatePipelineActionProps(
            cloud_assembly_input=cloud_assembly_input,
            pipeline_stack_name=pipeline_stack_name,
            cdk_cli_version=cdk_cli_version,
            project_name=project_name,
        )

        jsii.create(UpdatePipelineAction, self, [scope, id, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_f50a3f53,
        stage: _IStage_b7c853a7,
        *,
        bucket: _IBucket_25bad983,
        role: _IRole_e69bbae4,
    ) -> _ActionConfig_c379766c:
        """Exists to implement IAction.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        stability
        :stability: experimental
        """
        options = _ActionBindOptions_530c352f(bucket=bucket, role=role)

        return jsii.invoke(self, "bind", [scope, stage, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: str,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
        *,
        description: typing.Optional[str] = None,
        enabled: typing.Optional[bool] = None,
        event_bus: typing.Optional[_IEventBus_ed4f1700] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        schedule: typing.Optional[_Schedule_11a70620] = None,
        targets: typing.Optional[typing.List[_IRuleTarget_41800a77]] = None,
    ) -> _Rule_c38e0b39:
        """Exists to implement IAction.

        :param name: -
        :param target: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        stability
        :stability: experimental
        """
        options = _RuleProps_d60f0abf(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return jsii.invoke(self, "onStateChange", [name, target, options])

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_8f5d7a9d:
        """Exists to implement IAction.

        stability
        :stability: experimental
        """
        return jsii.get(self, "actionProperties")


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.UpdatePipelineActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "pipeline_stack_name": "pipelineStackName",
        "cdk_cli_version": "cdkCliVersion",
        "project_name": "projectName",
    },
)
class UpdatePipelineActionProps:
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_af6d98e9,
        pipeline_stack_name: str,
        cdk_cli_version: typing.Optional[str] = None,
        project_name: typing.Optional[str] = None,
    ) -> None:
        """Props for the UpdatePipelineAction.

        :param cloud_assembly_input: The CodePipeline artifact that holds the Cloud Assembly.
        :param pipeline_stack_name: Name of the pipeline stack.
        :param cdk_cli_version: Version of CDK CLI to 'npm install'. Default: - Latest version
        :param project_name: Name of the CodeBuild project. Default: - Automatically generated

        stability
        :stability: experimental
        """
        self._values = {
            "cloud_assembly_input": cloud_assembly_input,
            "pipeline_stack_name": pipeline_stack_name,
        }
        if cdk_cli_version is not None:
            self._values["cdk_cli_version"] = cdk_cli_version
        if project_name is not None:
            self._values["project_name"] = project_name

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_af6d98e9:
        """The CodePipeline artifact that holds the Cloud Assembly.

        stability
        :stability: experimental
        """
        return self._values.get("cloud_assembly_input")

    @builtins.property
    def pipeline_stack_name(self) -> str:
        """Name of the pipeline stack.

        stability
        :stability: experimental
        """
        return self._values.get("pipeline_stack_name")

    @builtins.property
    def cdk_cli_version(self) -> typing.Optional[str]:
        """Version of CDK CLI to 'npm install'.

        default
        :default: - Latest version

        stability
        :stability: experimental
        """
        return self._values.get("cdk_cli_version")

    @builtins.property
    def project_name(self) -> typing.Optional[str]:
        """Name of the CodeBuild project.

        default
        :default: - Automatically generated

        stability
        :stability: experimental
        """
        return self._values.get("project_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UpdatePipelineActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.CdkStackActionFromArtifactOptions",
    jsii_struct_bases=[DeployCdkStackActionOptions],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "base_action_name": "baseActionName",
        "change_set_name": "changeSetName",
        "execute_run_order": "executeRunOrder",
        "output": "output",
        "output_file_name": "outputFileName",
        "prepare_run_order": "prepareRunOrder",
        "stack_name": "stackName",
    },
)
class CdkStackActionFromArtifactOptions(DeployCdkStackActionOptions):
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_af6d98e9,
        base_action_name: typing.Optional[str] = None,
        change_set_name: typing.Optional[str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_af6d98e9] = None,
        output_file_name: typing.Optional[str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
        stack_name: typing.Optional[str] = None,
    ) -> None:
        """Options for the 'fromStackArtifact' operation.

        :param cloud_assembly_input: The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: Base name of the action. Default: stackName
        :param change_set_name: Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: Run order for the Prepare action. Default: 1
        :param stack_name: The name of the stack that should be created/updated. Default: - Same as stack artifact

        stability
        :stability: experimental
        """
        self._values = {
            "cloud_assembly_input": cloud_assembly_input,
        }
        if base_action_name is not None:
            self._values["base_action_name"] = base_action_name
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if prepare_run_order is not None:
            self._values["prepare_run_order"] = prepare_run_order
        if stack_name is not None:
            self._values["stack_name"] = stack_name

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_af6d98e9:
        """The CodePipeline artifact that holds the Cloud Assembly.

        stability
        :stability: experimental
        """
        return self._values.get("cloud_assembly_input")

    @builtins.property
    def base_action_name(self) -> typing.Optional[str]:
        """Base name of the action.

        default
        :default: stackName

        stability
        :stability: experimental
        """
        return self._values.get("base_action_name")

    @builtins.property
    def change_set_name(self) -> typing.Optional[str]:
        """Name of the change set to create and deploy.

        default
        :default: 'PipelineChange'

        stability
        :stability: experimental
        """
        return self._values.get("change_set_name")

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        """Run order for the Execute action.

        default
        :default: - prepareRunOrder + 1

        stability
        :stability: experimental
        """
        return self._values.get("execute_run_order")

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_af6d98e9]:
        """Artifact to write Stack Outputs to.

        default
        :default: - No outputs

        stability
        :stability: experimental
        """
        return self._values.get("output")

    @builtins.property
    def output_file_name(self) -> typing.Optional[str]:
        """Filename in output to write Stack outputs to.

        default
        :default: - Required when 'output' is set

        stability
        :stability: experimental
        """
        return self._values.get("output_file_name")

    @builtins.property
    def prepare_run_order(self) -> typing.Optional[jsii.Number]:
        """Run order for the Prepare action.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get("prepare_run_order")

    @builtins.property
    def stack_name(self) -> typing.Optional[str]:
        """The name of the stack that should be created/updated.

        default
        :default: - Same as stack artifact

        stability
        :stability: experimental
        """
        return self._values.get("stack_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkStackActionFromArtifactOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.pipelines.SimpleSynthActionProps",
    jsii_struct_bases=[SimpleSynthOptions],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "source_artifact": "sourceArtifact",
        "action_name": "actionName",
        "additional_artifacts": "additionalArtifacts",
        "copy_environment_variables": "copyEnvironmentVariables",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
        "role_policy_statements": "rolePolicyStatements",
        "subdirectory": "subdirectory",
        "synth_command": "synthCommand",
        "build_command": "buildCommand",
        "build_commands": "buildCommands",
        "install_command": "installCommand",
        "install_commands": "installCommands",
        "test_commands": "testCommands",
    },
)
class SimpleSynthActionProps(SimpleSynthOptions):
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_af6d98e9,
        source_artifact: _Artifact_af6d98e9,
        action_name: typing.Optional[str] = None,
        additional_artifacts: typing.Optional[typing.List["AdditionalArtifact"]] = None,
        copy_environment_variables: typing.Optional[typing.List[str]] = None,
        environment: typing.Optional[_BuildEnvironment_3f2fec35] = None,
        environment_variables: typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]] = None,
        project_name: typing.Optional[str] = None,
        role_policy_statements: typing.Optional[typing.List[_PolicyStatement_f75dc775]] = None,
        subdirectory: typing.Optional[str] = None,
        synth_command: str,
        build_command: typing.Optional[str] = None,
        build_commands: typing.Optional[typing.List[str]] = None,
        install_command: typing.Optional[str] = None,
        install_commands: typing.Optional[typing.List[str]] = None,
        test_commands: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Construction props for SimpleSynthAction.

        :param cloud_assembly_artifact: The artifact where the CloudAssembly should be emitted.
        :param source_artifact: The source artifact of the CodePipeline.
        :param action_name: Name of the build action. Default: 'Synth'
        :param additional_artifacts: Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param copy_environment_variables: Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0
        :param environment_variables: Environment variables to send into build. Default: - No additional environment variables
        :param project_name: Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param synth_command: The synth command.
        :param build_command: The build command. If your programming language requires a compilation step, put the compilation command here. Default: - No build required
        :param build_commands: The build commands. If your programming language requires a compilation step, put the compilation command here. Default: - No build required
        :param install_command: The install command. If not provided by the build image or another dependency management tool, at least install the CDK CLI here using ``npm install -g aws-cdk``. Default: - No install required
        :param install_commands: Install commands. If not provided by the build image or another dependency management tool, at least install the CDK CLI here using ``npm install -g aws-cdk``. Default: - No install required
        :param test_commands: Test commands. These commands are run after the build commands but before the synth command. Default: - No test commands

        stability
        :stability: experimental
        """
        if isinstance(environment, dict):
            environment = _BuildEnvironment_3f2fec35(**environment)
        self._values = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "source_artifact": source_artifact,
            "synth_command": synth_command,
        }
        if action_name is not None:
            self._values["action_name"] = action_name
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if copy_environment_variables is not None:
            self._values["copy_environment_variables"] = copy_environment_variables
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if build_command is not None:
            self._values["build_command"] = build_command
        if build_commands is not None:
            self._values["build_commands"] = build_commands
        if install_command is not None:
            self._values["install_command"] = install_command
        if install_commands is not None:
            self._values["install_commands"] = install_commands
        if test_commands is not None:
            self._values["test_commands"] = test_commands

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_af6d98e9:
        """The artifact where the CloudAssembly should be emitted.

        stability
        :stability: experimental
        """
        return self._values.get("cloud_assembly_artifact")

    @builtins.property
    def source_artifact(self) -> _Artifact_af6d98e9:
        """The source artifact of the CodePipeline.

        stability
        :stability: experimental
        """
        return self._values.get("source_artifact")

    @builtins.property
    def action_name(self) -> typing.Optional[str]:
        """Name of the build action.

        default
        :default: 'Synth'

        stability
        :stability: experimental
        """
        return self._values.get("action_name")

    @builtins.property
    def additional_artifacts(
        self,
    ) -> typing.Optional[typing.List["AdditionalArtifact"]]:
        """Produce additional output artifacts after the build based on the given directories.

        Can be used to produce additional artifacts during the build step,
        separate from the cloud assembly, which can be used further on in the
        pipeline.

        Directories are evaluated with respect to ``subdirectory``.

        default
        :default: - No additional artifacts generated

        stability
        :stability: experimental
        """
        return self._values.get("additional_artifacts")

    @builtins.property
    def copy_environment_variables(self) -> typing.Optional[typing.List[str]]:
        """Environment variables to copy over from parent env.

        These are environment variables that are being used by the build.

        default
        :default: - No environment variables copied

        stability
        :stability: experimental
        """
        return self._values.get("copy_environment_variables")

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_3f2fec35]:
        """Build environment to use for CodeBuild job.

        default
        :default: BuildEnvironment.LinuxBuildImage.STANDARD_4_0

        stability
        :stability: experimental
        """
        return self._values.get("environment")

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[str, _BuildEnvironmentVariable_dda665dd]]:
        """Environment variables to send into build.

        default
        :default: - No additional environment variables

        stability
        :stability: experimental
        """
        return self._values.get("environment_variables")

    @builtins.property
    def project_name(self) -> typing.Optional[str]:
        """Name of the CodeBuild project.

        default
        :default: - Automatically generated

        stability
        :stability: experimental
        """
        return self._values.get("project_name")

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_f75dc775]]:
        """Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        default
        :default: - No policy statements added to CodeBuild Project Role

        stability
        :stability: experimental
        """
        return self._values.get("role_policy_statements")

    @builtins.property
    def subdirectory(self) -> typing.Optional[str]:
        """Directory inside the source where package.json and cdk.json are located.

        default
        :default: - Repository root

        stability
        :stability: experimental
        """
        return self._values.get("subdirectory")

    @builtins.property
    def synth_command(self) -> str:
        """The synth command.

        stability
        :stability: experimental
        """
        return self._values.get("synth_command")

    @builtins.property
    def build_command(self) -> typing.Optional[str]:
        """The build command.

        If your programming language requires a compilation step, put the
        compilation command here.

        default
        :default: - No build required

        deprecated
        :deprecated: Use ``buildCommands`` instead

        stability
        :stability: deprecated
        """
        return self._values.get("build_command")

    @builtins.property
    def build_commands(self) -> typing.Optional[typing.List[str]]:
        """The build commands.

        If your programming language requires a compilation step, put the
        compilation command here.

        default
        :default: - No build required

        stability
        :stability: experimental
        """
        return self._values.get("build_commands")

    @builtins.property
    def install_command(self) -> typing.Optional[str]:
        """The install command.

        If not provided by the build image or another dependency
        management tool, at least install the CDK CLI here using
        ``npm install -g aws-cdk``.

        default
        :default: - No install required

        deprecated
        :deprecated: Use ``installCommands`` instead

        stability
        :stability: deprecated
        """
        return self._values.get("install_command")

    @builtins.property
    def install_commands(self) -> typing.Optional[typing.List[str]]:
        """Install commands.

        If not provided by the build image or another dependency
        management tool, at least install the CDK CLI here using
        ``npm install -g aws-cdk``.

        default
        :default: - No install required

        stability
        :stability: experimental
        """
        return self._values.get("install_commands")

    @builtins.property
    def test_commands(self) -> typing.Optional[typing.List[str]]:
        """Test commands.

        These commands are run after the build commands but before the
        synth command.

        default
        :default: - No test commands

        stability
        :stability: experimental
        """
        return self._values.get("test_commands")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SimpleSynthActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddManualApprovalOptions",
    "AddStackOptions",
    "AddStageOptions",
    "AdditionalArtifact",
    "AssetPublishingCommand",
    "AssetType",
    "CdkPipeline",
    "CdkPipelineProps",
    "CdkStackActionFromArtifactOptions",
    "CdkStage",
    "CdkStageProps",
    "DeployCdkStackAction",
    "DeployCdkStackActionOptions",
    "DeployCdkStackActionProps",
    "FromStackArtifactOptions",
    "IStageHost",
    "PublishAssetsAction",
    "PublishAssetsActionProps",
    "ShellScriptAction",
    "ShellScriptActionProps",
    "SimpleSynthAction",
    "SimpleSynthActionProps",
    "SimpleSynthOptions",
    "StackOutput",
    "StandardNpmSynthOptions",
    "StandardYarnSynthOptions",
    "UpdatePipelineAction",
    "UpdatePipelineActionProps",
]

publication.publish()
