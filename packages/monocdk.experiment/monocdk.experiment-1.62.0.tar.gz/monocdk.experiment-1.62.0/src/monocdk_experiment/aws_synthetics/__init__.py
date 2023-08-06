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
    AssetHashType as _AssetHashType_16f7047a,
    BundlingOptions as _BundlingOptions_0cab5223,
    CfnResource as _CfnResource_7760e8e4,
    CfnTag as _CfnTag_b4661f1a,
    Construct as _Construct_f50a3f53,
    Duration as _Duration_5170c158,
    IInspectable as _IInspectable_051e6ed8,
    IResolvable as _IResolvable_9ceae33e,
    Resource as _Resource_884d0774,
    TagManager as _TagManager_2508893f,
    TreeInspector as _TreeInspector_154f5999,
)
from ..assets import FollowMode as _FollowMode_f74e7125
from ..aws_cloudwatch import (
    Metric as _Metric_53e89548,
    MetricOptions as _MetricOptions_ad2c4d5d,
    Unit as _Unit_e1b74f3c,
)
from ..aws_iam import IGrantable as _IGrantable_0fcfc53a, IRole as _IRole_e69bbae4
from ..aws_s3 import IBucket as _IBucket_25bad983, Location as _Location_2d2ff215
from ..aws_s3_assets import AssetOptions as _AssetOptions_ed6c2956


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_synthetics.ArtifactsBucketLocation",
    jsii_struct_bases=[],
    name_mapping={"bucket": "bucket", "prefix": "prefix"},
)
class ArtifactsBucketLocation:
    def __init__(
        self, *, bucket: _IBucket_25bad983, prefix: typing.Optional[str] = None
    ) -> None:
        """Options for specifying the s3 location that stores the data of each canary run.

        The artifacts bucket location **cannot**
        be updated once the canary is created.

        :param bucket: The s3 location that stores the data of each run.
        :param prefix: The S3 bucket prefix. Specify this if you want a more specific path within the artifacts bucket. Default: - no prefix

        stability
        :stability: experimental
        """
        self._values = {
            "bucket": bucket,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> _IBucket_25bad983:
        """The s3 location that stores the data of each run.

        stability
        :stability: experimental
        """
        return self._values.get("bucket")

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """The S3 bucket prefix.

        Specify this if you want a more specific path within the artifacts bucket.

        default
        :default: - no prefix

        stability
        :stability: experimental
        """
        return self._values.get("prefix")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactsBucketLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Canary(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_synthetics.Canary",
):
    """Define a new Canary.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        test: "Test",
        artifacts_bucket_location: typing.Optional["ArtifactsBucketLocation"] = None,
        canary_name: typing.Optional[str] = None,
        failure_retention_period: typing.Optional[_Duration_5170c158] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        runtime: typing.Optional["Runtime"] = None,
        schedule: typing.Optional["Schedule"] = None,
        start_after_creation: typing.Optional[bool] = None,
        success_retention_period: typing.Optional[_Duration_5170c158] = None,
        time_to_live: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param test: The type of test that you want your canary to run. Use ``Test.custom()`` to specify the test to run.
        :param artifacts_bucket_location: The s3 location that stores the data of the canary runs. Default: - A new s3 bucket will be created without a prefix.
        :param canary_name: The name of the canary. Be sure to give it a descriptive name that distinguishes it from other canaries in your account. Do not include secrets or proprietary information in your canary name. The canary name makes up part of the canary ARN, which is included in outbound calls over the internet. Default: - A unique name will be generated from the construct ID
        :param failure_retention_period: How many days should failed runs be retained. Default: Duration.days(31)
        :param role: Canary execution role. This is the role that will be assumed by the canary upon execution. It controls the permissions that the canary will have. The role must be assumable by the AWS Lambda service principal. If not supplied, a role will be created with all the required permissions. If you provide a Role, you must add the required permissions. Default: - A unique role will be generated for this canary. You can add permissions to roles by calling 'addToRolePolicy'.
        :param runtime: Specify the runtime version to use for the canary. Currently, the only valid value is ``Runtime.SYNTHETICS_1.0``. Default: Runtime.SYNTHETICS_1_0
        :param schedule: Specify the schedule for how often the canary runs. For example, if you set ``schedule`` to ``rate(10 minutes)``, then the canary will run every 10 minutes. You can set the schedule with ``Schedule.rate(Duration)`` (recommended) or you can specify an expression using ``Schedule.expression()``. Default: 'rate(5 minutes)'
        :param start_after_creation: Whether or not the canary should start after creation. Default: true
        :param success_retention_period: How many days should successful runs be retained. Default: Duration.days(31)
        :param time_to_live: How long the canary will be in a 'RUNNING' state. For example, if you set ``timeToLive`` to be 1 hour and ``schedule`` to be ``rate(10 minutes)``, your canary will run at 10 minute intervals for an hour, for a total of 6 times. Default: - no limit

        stability
        :stability: experimental
        """
        props = CanaryProps(
            test=test,
            artifacts_bucket_location=artifacts_bucket_location,
            canary_name=canary_name,
            failure_retention_period=failure_retention_period,
            role=role,
            runtime=runtime,
            schedule=schedule,
            start_after_creation=start_after_creation,
            success_retention_period=success_retention_period,
            time_to_live=time_to_live,
        )

        jsii.create(Canary, self, [scope, id, props])

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measure the Duration of a single canary run, in seconds.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: avg over 5 minutes

        stability
        :stability: experimental
        """
        options = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricDuration", [options])

    @jsii.member(jsii_name="metricFailed")
    def metric_failed(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measure the number of failed canary runs over a given time period.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: avg over 5 minutes

        stability
        :stability: experimental
        """
        options = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricFailed", [options])

    @jsii.member(jsii_name="metricSuccessPercent")
    def metric_success_percent(
        self,
        *,
        account: typing.Optional[str] = None,
        color: typing.Optional[str] = None,
        dimensions: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        label: typing.Optional[str] = None,
        period: typing.Optional[_Duration_5170c158] = None,
        region: typing.Optional[str] = None,
        statistic: typing.Optional[str] = None,
        unit: typing.Optional[_Unit_e1b74f3c] = None,
    ) -> _Metric_53e89548:
        """Measure the percentage of successful canary runs.

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        default
        :default: avg over 5 minutes

        stability
        :stability: experimental
        """
        options = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricSuccessPercent", [options])

    @builtins.property
    @jsii.member(jsii_name="artifactsBucket")
    def artifacts_bucket(self) -> _IBucket_25bad983:
        """Bucket where data from each canary run is stored.

        stability
        :stability: experimental
        """
        return jsii.get(self, "artifactsBucket")

    @builtins.property
    @jsii.member(jsii_name="canaryId")
    def canary_id(self) -> str:
        """The canary ID.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "canaryId")

    @builtins.property
    @jsii.member(jsii_name="canaryName")
    def canary_name(self) -> str:
        """The canary Name.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "canaryName")

    @builtins.property
    @jsii.member(jsii_name="canaryState")
    def canary_state(self) -> str:
        """The state of the canary.

        For example, 'RUNNING', 'STOPPED', 'NOT STARTED', or 'ERROR'.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "canaryState")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _IRole_e69bbae4:
        """Execution role associated with this Canary.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_synthetics.CanaryProps",
    jsii_struct_bases=[],
    name_mapping={
        "test": "test",
        "artifacts_bucket_location": "artifactsBucketLocation",
        "canary_name": "canaryName",
        "failure_retention_period": "failureRetentionPeriod",
        "role": "role",
        "runtime": "runtime",
        "schedule": "schedule",
        "start_after_creation": "startAfterCreation",
        "success_retention_period": "successRetentionPeriod",
        "time_to_live": "timeToLive",
    },
)
class CanaryProps:
    def __init__(
        self,
        *,
        test: "Test",
        artifacts_bucket_location: typing.Optional["ArtifactsBucketLocation"] = None,
        canary_name: typing.Optional[str] = None,
        failure_retention_period: typing.Optional[_Duration_5170c158] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        runtime: typing.Optional["Runtime"] = None,
        schedule: typing.Optional["Schedule"] = None,
        start_after_creation: typing.Optional[bool] = None,
        success_retention_period: typing.Optional[_Duration_5170c158] = None,
        time_to_live: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """Properties for a canary.

        :param test: The type of test that you want your canary to run. Use ``Test.custom()`` to specify the test to run.
        :param artifacts_bucket_location: The s3 location that stores the data of the canary runs. Default: - A new s3 bucket will be created without a prefix.
        :param canary_name: The name of the canary. Be sure to give it a descriptive name that distinguishes it from other canaries in your account. Do not include secrets or proprietary information in your canary name. The canary name makes up part of the canary ARN, which is included in outbound calls over the internet. Default: - A unique name will be generated from the construct ID
        :param failure_retention_period: How many days should failed runs be retained. Default: Duration.days(31)
        :param role: Canary execution role. This is the role that will be assumed by the canary upon execution. It controls the permissions that the canary will have. The role must be assumable by the AWS Lambda service principal. If not supplied, a role will be created with all the required permissions. If you provide a Role, you must add the required permissions. Default: - A unique role will be generated for this canary. You can add permissions to roles by calling 'addToRolePolicy'.
        :param runtime: Specify the runtime version to use for the canary. Currently, the only valid value is ``Runtime.SYNTHETICS_1.0``. Default: Runtime.SYNTHETICS_1_0
        :param schedule: Specify the schedule for how often the canary runs. For example, if you set ``schedule`` to ``rate(10 minutes)``, then the canary will run every 10 minutes. You can set the schedule with ``Schedule.rate(Duration)`` (recommended) or you can specify an expression using ``Schedule.expression()``. Default: 'rate(5 minutes)'
        :param start_after_creation: Whether or not the canary should start after creation. Default: true
        :param success_retention_period: How many days should successful runs be retained. Default: Duration.days(31)
        :param time_to_live: How long the canary will be in a 'RUNNING' state. For example, if you set ``timeToLive`` to be 1 hour and ``schedule`` to be ``rate(10 minutes)``, your canary will run at 10 minute intervals for an hour, for a total of 6 times. Default: - no limit

        stability
        :stability: experimental
        """
        if isinstance(artifacts_bucket_location, dict):
            artifacts_bucket_location = ArtifactsBucketLocation(**artifacts_bucket_location)
        self._values = {
            "test": test,
        }
        if artifacts_bucket_location is not None:
            self._values["artifacts_bucket_location"] = artifacts_bucket_location
        if canary_name is not None:
            self._values["canary_name"] = canary_name
        if failure_retention_period is not None:
            self._values["failure_retention_period"] = failure_retention_period
        if role is not None:
            self._values["role"] = role
        if runtime is not None:
            self._values["runtime"] = runtime
        if schedule is not None:
            self._values["schedule"] = schedule
        if start_after_creation is not None:
            self._values["start_after_creation"] = start_after_creation
        if success_retention_period is not None:
            self._values["success_retention_period"] = success_retention_period
        if time_to_live is not None:
            self._values["time_to_live"] = time_to_live

    @builtins.property
    def test(self) -> "Test":
        """The type of test that you want your canary to run.

        Use ``Test.custom()`` to specify the test to run.

        stability
        :stability: experimental
        """
        return self._values.get("test")

    @builtins.property
    def artifacts_bucket_location(self) -> typing.Optional["ArtifactsBucketLocation"]:
        """The s3 location that stores the data of the canary runs.

        default
        :default: - A new s3 bucket will be created without a prefix.

        stability
        :stability: experimental
        """
        return self._values.get("artifacts_bucket_location")

    @builtins.property
    def canary_name(self) -> typing.Optional[str]:
        """The name of the canary.

        Be sure to give it a descriptive name that distinguishes it from
        other canaries in your account.

        Do not include secrets or proprietary information in your canary name. The canary name
        makes up part of the canary ARN, which is included in outbound calls over the internet.

        default
        :default: - A unique name will be generated from the construct ID

        see
        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/servicelens_canaries_security.html
        stability
        :stability: experimental
        """
        return self._values.get("canary_name")

    @builtins.property
    def failure_retention_period(self) -> typing.Optional[_Duration_5170c158]:
        """How many days should failed runs be retained.

        default
        :default: Duration.days(31)

        stability
        :stability: experimental
        """
        return self._values.get("failure_retention_period")

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Canary execution role.

        This is the role that will be assumed by the canary upon execution.
        It controls the permissions that the canary will have. The role must
        be assumable by the AWS Lambda service principal.

        If not supplied, a role will be created with all the required permissions.
        If you provide a Role, you must add the required permissions.

        default
        :default:

        - A unique role will be generated for this canary.
          You can add permissions to roles by calling 'addToRolePolicy'.

        see
        :see: required permissions: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-executionrolearn
        stability
        :stability: experimental
        """
        return self._values.get("role")

    @builtins.property
    def runtime(self) -> typing.Optional["Runtime"]:
        """Specify the runtime version to use for the canary.

        Currently, the only valid value is ``Runtime.SYNTHETICS_1.0``.

        default
        :default: Runtime.SYNTHETICS_1_0

        stability
        :stability: experimental
        """
        return self._values.get("runtime")

    @builtins.property
    def schedule(self) -> typing.Optional["Schedule"]:
        """Specify the schedule for how often the canary runs.

        For example, if you set ``schedule`` to ``rate(10 minutes)``, then the canary will run every 10 minutes.
        You can set the schedule with ``Schedule.rate(Duration)`` (recommended) or you can specify an expression using ``Schedule.expression()``.

        default
        :default: 'rate(5 minutes)'

        stability
        :stability: experimental
        """
        return self._values.get("schedule")

    @builtins.property
    def start_after_creation(self) -> typing.Optional[bool]:
        """Whether or not the canary should start after creation.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("start_after_creation")

    @builtins.property
    def success_retention_period(self) -> typing.Optional[_Duration_5170c158]:
        """How many days should successful runs be retained.

        default
        :default: Duration.days(31)

        stability
        :stability: experimental
        """
        return self._values.get("success_retention_period")

    @builtins.property
    def time_to_live(self) -> typing.Optional[_Duration_5170c158]:
        """How long the canary will be in a 'RUNNING' state.

        For example, if you set ``timeToLive`` to be 1 hour and ``schedule`` to be ``rate(10 minutes)``,
        your canary will run at 10 minute intervals for an hour, for a total of 6 times.

        default
        :default: - no limit

        stability
        :stability: experimental
        """
        return self._values.get("time_to_live")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CanaryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnCanary(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_synthetics.CfnCanary",
):
    """A CloudFormation ``AWS::Synthetics::Canary``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html
    cloudformationResource:
    :cloudformationResource:: AWS::Synthetics::Canary
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        artifact_s3_location: str,
        code: typing.Union["CodeProperty", _IResolvable_9ceae33e],
        execution_role_arn: str,
        name: str,
        runtime_version: str,
        schedule: typing.Union["ScheduleProperty", _IResolvable_9ceae33e],
        start_canary_after_creation: typing.Union[bool, _IResolvable_9ceae33e],
        failure_retention_period: typing.Optional[jsii.Number] = None,
        run_config: typing.Optional[typing.Union["RunConfigProperty", _IResolvable_9ceae33e]] = None,
        success_retention_period: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        vpc_config: typing.Optional[typing.Union["VPCConfigProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Create a new ``AWS::Synthetics::Canary``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param artifact_s3_location: ``AWS::Synthetics::Canary.ArtifactS3Location``.
        :param code: ``AWS::Synthetics::Canary.Code``.
        :param execution_role_arn: ``AWS::Synthetics::Canary.ExecutionRoleArn``.
        :param name: ``AWS::Synthetics::Canary.Name``.
        :param runtime_version: ``AWS::Synthetics::Canary.RuntimeVersion``.
        :param schedule: ``AWS::Synthetics::Canary.Schedule``.
        :param start_canary_after_creation: ``AWS::Synthetics::Canary.StartCanaryAfterCreation``.
        :param failure_retention_period: ``AWS::Synthetics::Canary.FailureRetentionPeriod``.
        :param run_config: ``AWS::Synthetics::Canary.RunConfig``.
        :param success_retention_period: ``AWS::Synthetics::Canary.SuccessRetentionPeriod``.
        :param tags: ``AWS::Synthetics::Canary.Tags``.
        :param vpc_config: ``AWS::Synthetics::Canary.VPCConfig``.
        """
        props = CfnCanaryProps(
            artifact_s3_location=artifact_s3_location,
            code=code,
            execution_role_arn=execution_role_arn,
            name=name,
            runtime_version=runtime_version,
            schedule=schedule,
            start_canary_after_creation=start_canary_after_creation,
            failure_retention_period=failure_retention_period,
            run_config=run_config,
            success_retention_period=success_retention_period,
            tags=tags,
            vpc_config=vpc_config,
        )

        jsii.create(CfnCanary, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_154f5999) -> None:
        """Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "inspect", [inspector])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self, props: typing.Mapping[str, typing.Any]
    ) -> typing.Mapping[str, typing.Any]:
        """
        :param props: -
        """
        return jsii.invoke(self, "renderProperties", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME")

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Id
        """
        return jsii.get(self, "attrId")

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: State
        """
        return jsii.get(self, "attrState")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::Synthetics::Canary.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="artifactS3Location")
    def artifact_s3_location(self) -> str:
        """``AWS::Synthetics::Canary.ArtifactS3Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-artifacts3location
        """
        return jsii.get(self, "artifactS3Location")

    @artifact_s3_location.setter
    def artifact_s3_location(self, value: str) -> None:
        jsii.set(self, "artifactS3Location", value)

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> typing.Union["CodeProperty", _IResolvable_9ceae33e]:
        """``AWS::Synthetics::Canary.Code``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-code
        """
        return jsii.get(self, "code")

    @code.setter
    def code(self, value: typing.Union["CodeProperty", _IResolvable_9ceae33e]) -> None:
        jsii.set(self, "code", value)

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> str:
        """``AWS::Synthetics::Canary.ExecutionRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-executionrolearn
        """
        return jsii.get(self, "executionRoleArn")

    @execution_role_arn.setter
    def execution_role_arn(self, value: str) -> None:
        jsii.set(self, "executionRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """``AWS::Synthetics::Canary.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> str:
        """``AWS::Synthetics::Canary.RuntimeVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runtimeversion
        """
        return jsii.get(self, "runtimeVersion")

    @runtime_version.setter
    def runtime_version(self, value: str) -> None:
        jsii.set(self, "runtimeVersion", value)

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> typing.Union["ScheduleProperty", _IResolvable_9ceae33e]:
        """``AWS::Synthetics::Canary.Schedule``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-schedule
        """
        return jsii.get(self, "schedule")

    @schedule.setter
    def schedule(
        self, value: typing.Union["ScheduleProperty", _IResolvable_9ceae33e]
    ) -> None:
        jsii.set(self, "schedule", value)

    @builtins.property
    @jsii.member(jsii_name="startCanaryAfterCreation")
    def start_canary_after_creation(self) -> typing.Union[bool, _IResolvable_9ceae33e]:
        """``AWS::Synthetics::Canary.StartCanaryAfterCreation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-startcanaryaftercreation
        """
        return jsii.get(self, "startCanaryAfterCreation")

    @start_canary_after_creation.setter
    def start_canary_after_creation(
        self, value: typing.Union[bool, _IResolvable_9ceae33e]
    ) -> None:
        jsii.set(self, "startCanaryAfterCreation", value)

    @builtins.property
    @jsii.member(jsii_name="failureRetentionPeriod")
    def failure_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Synthetics::Canary.FailureRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-failureretentionperiod
        """
        return jsii.get(self, "failureRetentionPeriod")

    @failure_retention_period.setter
    def failure_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "failureRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="runConfig")
    def run_config(
        self,
    ) -> typing.Optional[typing.Union["RunConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Synthetics::Canary.RunConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runconfig
        """
        return jsii.get(self, "runConfig")

    @run_config.setter
    def run_config(
        self,
        value: typing.Optional[typing.Union["RunConfigProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "runConfig", value)

    @builtins.property
    @jsii.member(jsii_name="successRetentionPeriod")
    def success_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Synthetics::Canary.SuccessRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-successretentionperiod
        """
        return jsii.get(self, "successRetentionPeriod")

    @success_retention_period.setter
    def success_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "successRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="vpcConfig")
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union["VPCConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Synthetics::Canary.VPCConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-vpcconfig
        """
        return jsii.get(self, "vpcConfig")

    @vpc_config.setter
    def vpc_config(
        self,
        value: typing.Optional[typing.Union["VPCConfigProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "vpcConfig", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_synthetics.CfnCanary.CodeProperty",
        jsii_struct_bases=[],
        name_mapping={
            "handler": "handler",
            "s3_bucket": "s3Bucket",
            "s3_key": "s3Key",
            "s3_object_version": "s3ObjectVersion",
            "script": "script",
        },
    )
    class CodeProperty:
        def __init__(
            self,
            *,
            handler: typing.Optional[str] = None,
            s3_bucket: typing.Optional[str] = None,
            s3_key: typing.Optional[str] = None,
            s3_object_version: typing.Optional[str] = None,
            script: typing.Optional[str] = None,
        ) -> None:
            """
            :param handler: ``CfnCanary.CodeProperty.Handler``.
            :param s3_bucket: ``CfnCanary.CodeProperty.S3Bucket``.
            :param s3_key: ``CfnCanary.CodeProperty.S3Key``.
            :param s3_object_version: ``CfnCanary.CodeProperty.S3ObjectVersion``.
            :param script: ``CfnCanary.CodeProperty.Script``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html
            """
            self._values = {}
            if handler is not None:
                self._values["handler"] = handler
            if s3_bucket is not None:
                self._values["s3_bucket"] = s3_bucket
            if s3_key is not None:
                self._values["s3_key"] = s3_key
            if s3_object_version is not None:
                self._values["s3_object_version"] = s3_object_version
            if script is not None:
                self._values["script"] = script

        @builtins.property
        def handler(self) -> typing.Optional[str]:
            """``CfnCanary.CodeProperty.Handler``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-handler
            """
            return self._values.get("handler")

        @builtins.property
        def s3_bucket(self) -> typing.Optional[str]:
            """``CfnCanary.CodeProperty.S3Bucket``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3bucket
            """
            return self._values.get("s3_bucket")

        @builtins.property
        def s3_key(self) -> typing.Optional[str]:
            """``CfnCanary.CodeProperty.S3Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3key
            """
            return self._values.get("s3_key")

        @builtins.property
        def s3_object_version(self) -> typing.Optional[str]:
            """``CfnCanary.CodeProperty.S3ObjectVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-s3objectversion
            """
            return self._values.get("s3_object_version")

        @builtins.property
        def script(self) -> typing.Optional[str]:
            """``CfnCanary.CodeProperty.Script``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-code.html#cfn-synthetics-canary-code-script
            """
            return self._values.get("script")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CodeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_synthetics.CfnCanary.RunConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "timeout_in_seconds": "timeoutInSeconds",
            "memory_in_mb": "memoryInMb",
        },
    )
    class RunConfigProperty:
        def __init__(
            self,
            *,
            timeout_in_seconds: jsii.Number,
            memory_in_mb: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param timeout_in_seconds: ``CfnCanary.RunConfigProperty.TimeoutInSeconds``.
            :param memory_in_mb: ``CfnCanary.RunConfigProperty.MemoryInMB``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html
            """
            self._values = {
                "timeout_in_seconds": timeout_in_seconds,
            }
            if memory_in_mb is not None:
                self._values["memory_in_mb"] = memory_in_mb

        @builtins.property
        def timeout_in_seconds(self) -> jsii.Number:
            """``CfnCanary.RunConfigProperty.TimeoutInSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-timeoutinseconds
            """
            return self._values.get("timeout_in_seconds")

        @builtins.property
        def memory_in_mb(self) -> typing.Optional[jsii.Number]:
            """``CfnCanary.RunConfigProperty.MemoryInMB``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-runconfig.html#cfn-synthetics-canary-runconfig-memoryinmb
            """
            return self._values.get("memory_in_mb")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RunConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_synthetics.CfnCanary.ScheduleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "expression": "expression",
            "duration_in_seconds": "durationInSeconds",
        },
    )
    class ScheduleProperty:
        def __init__(
            self, *, expression: str, duration_in_seconds: typing.Optional[str] = None
        ) -> None:
            """
            :param expression: ``CfnCanary.ScheduleProperty.Expression``.
            :param duration_in_seconds: ``CfnCanary.ScheduleProperty.DurationInSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html
            """
            self._values = {
                "expression": expression,
            }
            if duration_in_seconds is not None:
                self._values["duration_in_seconds"] = duration_in_seconds

        @builtins.property
        def expression(self) -> str:
            """``CfnCanary.ScheduleProperty.Expression``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html#cfn-synthetics-canary-schedule-expression
            """
            return self._values.get("expression")

        @builtins.property
        def duration_in_seconds(self) -> typing.Optional[str]:
            """``CfnCanary.ScheduleProperty.DurationInSeconds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-schedule.html#cfn-synthetics-canary-schedule-durationinseconds
            """
            return self._values.get("duration_in_seconds")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScheduleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_synthetics.CfnCanary.VPCConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
            "vpc_id": "vpcId",
        },
    )
    class VPCConfigProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.List[str],
            subnet_ids: typing.List[str],
            vpc_id: typing.Optional[str] = None,
        ) -> None:
            """
            :param security_group_ids: ``CfnCanary.VPCConfigProperty.SecurityGroupIds``.
            :param subnet_ids: ``CfnCanary.VPCConfigProperty.SubnetIds``.
            :param vpc_id: ``CfnCanary.VPCConfigProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html
            """
            self._values = {
                "security_group_ids": security_group_ids,
                "subnet_ids": subnet_ids,
            }
            if vpc_id is not None:
                self._values["vpc_id"] = vpc_id

        @builtins.property
        def security_group_ids(self) -> typing.List[str]:
            """``CfnCanary.VPCConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-securitygroupids
            """
            return self._values.get("security_group_ids")

        @builtins.property
        def subnet_ids(self) -> typing.List[str]:
            """``CfnCanary.VPCConfigProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-subnetids
            """
            return self._values.get("subnet_ids")

        @builtins.property
        def vpc_id(self) -> typing.Optional[str]:
            """``CfnCanary.VPCConfigProperty.VpcId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-synthetics-canary-vpcconfig.html#cfn-synthetics-canary-vpcconfig-vpcid
            """
            return self._values.get("vpc_id")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VPCConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_synthetics.CfnCanaryProps",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_s3_location": "artifactS3Location",
        "code": "code",
        "execution_role_arn": "executionRoleArn",
        "name": "name",
        "runtime_version": "runtimeVersion",
        "schedule": "schedule",
        "start_canary_after_creation": "startCanaryAfterCreation",
        "failure_retention_period": "failureRetentionPeriod",
        "run_config": "runConfig",
        "success_retention_period": "successRetentionPeriod",
        "tags": "tags",
        "vpc_config": "vpcConfig",
    },
)
class CfnCanaryProps:
    def __init__(
        self,
        *,
        artifact_s3_location: str,
        code: typing.Union["CfnCanary.CodeProperty", _IResolvable_9ceae33e],
        execution_role_arn: str,
        name: str,
        runtime_version: str,
        schedule: typing.Union["CfnCanary.ScheduleProperty", _IResolvable_9ceae33e],
        start_canary_after_creation: typing.Union[bool, _IResolvable_9ceae33e],
        failure_retention_period: typing.Optional[jsii.Number] = None,
        run_config: typing.Optional[typing.Union["CfnCanary.RunConfigProperty", _IResolvable_9ceae33e]] = None,
        success_retention_period: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        vpc_config: typing.Optional[typing.Union["CfnCanary.VPCConfigProperty", _IResolvable_9ceae33e]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Synthetics::Canary``.

        :param artifact_s3_location: ``AWS::Synthetics::Canary.ArtifactS3Location``.
        :param code: ``AWS::Synthetics::Canary.Code``.
        :param execution_role_arn: ``AWS::Synthetics::Canary.ExecutionRoleArn``.
        :param name: ``AWS::Synthetics::Canary.Name``.
        :param runtime_version: ``AWS::Synthetics::Canary.RuntimeVersion``.
        :param schedule: ``AWS::Synthetics::Canary.Schedule``.
        :param start_canary_after_creation: ``AWS::Synthetics::Canary.StartCanaryAfterCreation``.
        :param failure_retention_period: ``AWS::Synthetics::Canary.FailureRetentionPeriod``.
        :param run_config: ``AWS::Synthetics::Canary.RunConfig``.
        :param success_retention_period: ``AWS::Synthetics::Canary.SuccessRetentionPeriod``.
        :param tags: ``AWS::Synthetics::Canary.Tags``.
        :param vpc_config: ``AWS::Synthetics::Canary.VPCConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html
        """
        self._values = {
            "artifact_s3_location": artifact_s3_location,
            "code": code,
            "execution_role_arn": execution_role_arn,
            "name": name,
            "runtime_version": runtime_version,
            "schedule": schedule,
            "start_canary_after_creation": start_canary_after_creation,
        }
        if failure_retention_period is not None:
            self._values["failure_retention_period"] = failure_retention_period
        if run_config is not None:
            self._values["run_config"] = run_config
        if success_retention_period is not None:
            self._values["success_retention_period"] = success_retention_period
        if tags is not None:
            self._values["tags"] = tags
        if vpc_config is not None:
            self._values["vpc_config"] = vpc_config

    @builtins.property
    def artifact_s3_location(self) -> str:
        """``AWS::Synthetics::Canary.ArtifactS3Location``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-artifacts3location
        """
        return self._values.get("artifact_s3_location")

    @builtins.property
    def code(self) -> typing.Union["CfnCanary.CodeProperty", _IResolvable_9ceae33e]:
        """``AWS::Synthetics::Canary.Code``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-code
        """
        return self._values.get("code")

    @builtins.property
    def execution_role_arn(self) -> str:
        """``AWS::Synthetics::Canary.ExecutionRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-executionrolearn
        """
        return self._values.get("execution_role_arn")

    @builtins.property
    def name(self) -> str:
        """``AWS::Synthetics::Canary.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-name
        """
        return self._values.get("name")

    @builtins.property
    def runtime_version(self) -> str:
        """``AWS::Synthetics::Canary.RuntimeVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runtimeversion
        """
        return self._values.get("runtime_version")

    @builtins.property
    def schedule(
        self,
    ) -> typing.Union["CfnCanary.ScheduleProperty", _IResolvable_9ceae33e]:
        """``AWS::Synthetics::Canary.Schedule``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-schedule
        """
        return self._values.get("schedule")

    @builtins.property
    def start_canary_after_creation(self) -> typing.Union[bool, _IResolvable_9ceae33e]:
        """``AWS::Synthetics::Canary.StartCanaryAfterCreation``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-startcanaryaftercreation
        """
        return self._values.get("start_canary_after_creation")

    @builtins.property
    def failure_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Synthetics::Canary.FailureRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-failureretentionperiod
        """
        return self._values.get("failure_retention_period")

    @builtins.property
    def run_config(
        self,
    ) -> typing.Optional[typing.Union["CfnCanary.RunConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Synthetics::Canary.RunConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-runconfig
        """
        return self._values.get("run_config")

    @builtins.property
    def success_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::Synthetics::Canary.SuccessRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-successretentionperiod
        """
        return self._values.get("success_retention_period")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::Synthetics::Canary.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-tags
        """
        return self._values.get("tags")

    @builtins.property
    def vpc_config(
        self,
    ) -> typing.Optional[typing.Union["CfnCanary.VPCConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::Synthetics::Canary.VPCConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-synthetics-canary.html#cfn-synthetics-canary-vpcconfig
        """
        return self._values.get("vpc_config")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCanaryProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Code(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk-experiment.aws_synthetics.Code",
):
    """The code the canary should execute.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _CodeProxy

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(Code, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(
        cls,
        asset_path: str,
        *,
        readers: typing.Optional[typing.List[_IGrantable_0fcfc53a]] = None,
        source_hash: typing.Optional[str] = None,
        exclude: typing.Optional[typing.List[str]] = None,
        follow: typing.Optional[_FollowMode_f74e7125] = None,
        asset_hash: typing.Optional[str] = None,
        asset_hash_type: typing.Optional[_AssetHashType_16f7047a] = None,
        bundling: typing.Optional[_BundlingOptions_0cab5223] = None,
    ) -> "AssetCode":
        """Specify code from a local path.

        Path must include the folder structure ``nodejs/node_modules/myCanaryFilename.js``.

        :param asset_path: Either a directory or a .zip file.
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise

        return
        :return: ``AssetCode`` associated with the specified path.

        see
        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_WritingCanary.html#CloudWatch_Synthetics_Canaries_write_from_scratch
        stability
        :stability: experimental
        """
        options = _AssetOptions_ed6c2956(
            readers=readers,
            source_hash=source_hash,
            exclude=exclude,
            follow=follow,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
        )

        return jsii.sinvoke(cls, "fromAsset", [asset_path, options])

    @jsii.member(jsii_name="fromBucket")
    @builtins.classmethod
    def from_bucket(
        cls,
        bucket: _IBucket_25bad983,
        key: str,
        object_version: typing.Optional[str] = None,
    ) -> "S3Code":
        """Specify code from an s3 bucket.

        The object in the s3 bucket must be a .zip file that contains
        the structure ``nodejs/node_modules/myCanaryFilename.js``.

        :param bucket: The S3 bucket.
        :param key: The object key.
        :param object_version: Optional S3 object version.

        return
        :return: ``S3Code`` associated with the specified S3 object.

        see
        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries_WritingCanary.html#CloudWatch_Synthetics_Canaries_write_from_scratch
        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromBucket", [bucket, key, object_version])

    @jsii.member(jsii_name="fromInline")
    @builtins.classmethod
    def from_inline(cls, code: str) -> "InlineCode":
        """Specify code inline.

        :param code: The actual handler code (limited to 4KiB).

        return
        :return: ``InlineCode`` with inline code.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromInline", [code])

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _Construct_f50a3f53, handler: str) -> "CodeConfig":
        """Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.
        :param handler: -

        return
        :return: a bound ``CodeConfig``.

        stability
        :stability: experimental
        """
        ...


class _CodeProxy(Code):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, handler: str) -> "CodeConfig":
        """Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: The binding scope. Don't be smart about trying to down-cast or assume it's initialized. You may just use it as a construct scope.
        :param handler: -

        return
        :return: a bound ``CodeConfig``.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, handler])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_synthetics.CodeConfig",
    jsii_struct_bases=[],
    name_mapping={"inline_code": "inlineCode", "s3_location": "s3Location"},
)
class CodeConfig:
    def __init__(
        self,
        *,
        inline_code: typing.Optional[str] = None,
        s3_location: typing.Optional[_Location_2d2ff215] = None,
    ) -> None:
        """Configuration of the code class.

        :param inline_code: Inline code (mutually exclusive with ``s3Location``). Default: - none
        :param s3_location: The location of the code in S3 (mutually exclusive with ``inlineCode``). Default: - none

        stability
        :stability: experimental
        """
        if isinstance(s3_location, dict):
            s3_location = _Location_2d2ff215(**s3_location)
        self._values = {}
        if inline_code is not None:
            self._values["inline_code"] = inline_code
        if s3_location is not None:
            self._values["s3_location"] = s3_location

    @builtins.property
    def inline_code(self) -> typing.Optional[str]:
        """Inline code (mutually exclusive with ``s3Location``).

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get("inline_code")

    @builtins.property
    def s3_location(self) -> typing.Optional[_Location_2d2ff215]:
        """The location of the code in S3 (mutually exclusive with ``inlineCode``).

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get("s3_location")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_synthetics.CustomTestOptions",
    jsii_struct_bases=[],
    name_mapping={"code": "code", "handler": "handler"},
)
class CustomTestOptions:
    def __init__(self, *, code: "Code", handler: str) -> None:
        """Properties for specifying a test.

        :param code: The code of the canary script.
        :param handler: The handler for the code. Must end with ``.handler``.

        stability
        :stability: experimental
        """
        self._values = {
            "code": code,
            "handler": handler,
        }

    @builtins.property
    def code(self) -> "Code":
        """The code of the canary script.

        stability
        :stability: experimental
        """
        return self._values.get("code")

    @builtins.property
    def handler(self) -> str:
        """The handler for the code.

        Must end with ``.handler``.

        stability
        :stability: experimental
        """
        return self._values.get("handler")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomTestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InlineCode(
    Code,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_synthetics.InlineCode",
):
    """Canary code from an inline string.

    stability
    :stability: experimental
    """

    def __init__(self, code: str) -> None:
        """
        :param code: -

        stability
        :stability: experimental
        """
        jsii.create(InlineCode, self, [code])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, handler: str) -> "CodeConfig":
        """Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param _scope: -
        :param handler: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, handler])


class Runtime(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_synthetics.Runtime"
):
    """Runtime options for a canary.

    stability
    :stability: experimental
    """

    def __init__(self, name: str) -> None:
        """
        :param name: The name of the runtime version.

        stability
        :stability: experimental
        """
        jsii.create(Runtime, self, [name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="SYNTHETICS_1_0")
    def SYNTHETICS_1_0(cls) -> "Runtime":
        """``syn-1.0`` includes the following:.

        - Synthetics library 1.0
        - Synthetics handler code 1.0
        - Lambda runtime Node.js 10.x
        - Puppeteer-core version 1.14.0
        - The Chromium version that matches Puppeteer-core 1.14.0

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "SYNTHETICS_1_0")

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """The name of the runtime version.

        stability
        :stability: experimental
        """
        return jsii.get(self, "name")


class S3Code(
    Code, metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_synthetics.S3Code"
):
    """S3 bucket path to the code zip file.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        bucket: _IBucket_25bad983,
        key: str,
        object_version: typing.Optional[str] = None,
    ) -> None:
        """
        :param bucket: -
        :param key: -
        :param object_version: -

        stability
        :stability: experimental
        """
        jsii.create(S3Code, self, [bucket, key, object_version])

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _Construct_f50a3f53, _handler: str) -> "CodeConfig":
        """Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param _scope: -
        :param _handler: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_scope, _handler])


class Schedule(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_synthetics.Schedule"
):
    """Schedule for canary runs.

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="expression")
    @builtins.classmethod
    def expression(cls, expression: str) -> "Schedule":
        """Construct a schedule from a literal schedule expression.

        The expression must be in a ``rate(number units)`` format.
        For example, ``Schedule.expression('rate(10 minutes)')``

        :param expression: The expression to use.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "expression", [expression])

    @jsii.member(jsii_name="once")
    @builtins.classmethod
    def once(cls) -> "Schedule":
        """The canary will be executed once.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "once", [])

    @jsii.member(jsii_name="rate")
    @builtins.classmethod
    def rate(cls, interval: _Duration_5170c158) -> "Schedule":
        """Construct a schedule from an interval.

        Allowed values: 0 (for a single run) or between 1 and 60 minutes.
        To specify a single run, you can use ``Schedule.once()``.

        :param interval: The interval at which to run the canary.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "rate", [interval])

    @builtins.property
    @jsii.member(jsii_name="expressionString")
    def expression_string(self) -> str:
        """The Schedule expression.

        stability
        :stability: experimental
        """
        return jsii.get(self, "expressionString")


class Test(metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_synthetics.Test"):
    """Specify a test that the canary should run.

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, *, code: "Code", handler: str) -> "Test":
        """Specify a custom test with your own code.

        :param code: The code of the canary script.
        :param handler: The handler for the code. Must end with ``.handler``.

        return
        :return: ``Test`` associated with the specified Code object

        stability
        :stability: experimental
        """
        options = CustomTestOptions(code=code, handler=handler)

        return jsii.sinvoke(cls, "custom", [options])

    @builtins.property
    @jsii.member(jsii_name="code")
    def code(self) -> "Code":
        """The code that the canary should run.

        stability
        :stability: experimental
        """
        return jsii.get(self, "code")

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> str:
        """The handler of the canary.

        stability
        :stability: experimental
        """
        return jsii.get(self, "handler")


class AssetCode(
    Code,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_synthetics.AssetCode",
):
    """Canary code from an Asset.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        asset_path: str,
        *,
        readers: typing.Optional[typing.List[_IGrantable_0fcfc53a]] = None,
        source_hash: typing.Optional[str] = None,
        exclude: typing.Optional[typing.List[str]] = None,
        follow: typing.Optional[_FollowMode_f74e7125] = None,
        asset_hash: typing.Optional[str] = None,
        asset_hash_type: typing.Optional[_AssetHashType_16f7047a] = None,
        bundling: typing.Optional[_BundlingOptions_0cab5223] = None,
    ) -> None:
        """
        :param asset_path: The path to the asset file or directory.
        :param readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later. Default: - No principals that can read file asset.
        :param source_hash: Custom hash to use when identifying the specific version of the asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the source hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the source hash, you will need to make sure it is updated every time the source changes, or otherwise it is possible that some deployments will not be invalidated. Default: - automatically calculate source hash based on the contents of the source file or directory.
        :param exclude: Glob patterns to exclude from the copy. Default: nothing is excluded
        :param follow: A strategy for how to handle symlinks. Default: Never
        :param asset_hash: Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - based on ``assetHashType``
        :param asset_hash_type: Specifies the type of hash to calculate for this asset. If ``assetHash`` is configured, this option must be ``undefined`` or ``AssetHashType.CUSTOM``. Default: - the default is ``AssetHashType.SOURCE``, but if ``assetHash`` is explicitly specified this value defaults to ``AssetHashType.CUSTOM``.
        :param bundling: Bundle the asset by executing a command in a Docker container. The asset path will be mounted at ``/asset-input``. The Docker container is responsible for putting content at ``/asset-output``. The content at ``/asset-output`` will be zipped and used as the final asset. Default: - uploaded as-is to S3 if the asset is a regular file or a .zip file, archived into a .zip file and uploaded to S3 otherwise

        stability
        :stability: experimental
        """
        options = _AssetOptions_ed6c2956(
            readers=readers,
            source_hash=source_hash,
            exclude=exclude,
            follow=follow,
            asset_hash=asset_hash,
            asset_hash_type=asset_hash_type,
            bundling=bundling,
        )

        jsii.create(AssetCode, self, [asset_path, options])

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_f50a3f53, handler: str) -> "CodeConfig":
        """Called when the canary is initialized to allow this object to bind to the stack, add resources and have fun.

        :param scope: -
        :param handler: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [scope, handler])


__all__ = [
    "ArtifactsBucketLocation",
    "AssetCode",
    "Canary",
    "CanaryProps",
    "CfnCanary",
    "CfnCanaryProps",
    "Code",
    "CodeConfig",
    "CustomTestOptions",
    "InlineCode",
    "Runtime",
    "S3Code",
    "Schedule",
    "Test",
]

publication.publish()
