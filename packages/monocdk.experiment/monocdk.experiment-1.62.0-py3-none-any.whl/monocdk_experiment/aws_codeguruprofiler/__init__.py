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
    CfnResource as _CfnResource_7760e8e4,
    CfnTag as _CfnTag_b4661f1a,
    Construct as _Construct_f50a3f53,
    IInspectable as _IInspectable_051e6ed8,
    IResolvable as _IResolvable_9ceae33e,
    IResource as _IResource_72f7ee7e,
    Resource as _Resource_884d0774,
    TagManager as _TagManager_2508893f,
    TreeInspector as _TreeInspector_154f5999,
)
from ..aws_iam import Grant as _Grant_96af6d2d, IGrantable as _IGrantable_0fcfc53a


@jsii.implements(_IInspectable_051e6ed8)
class CfnProfilingGroup(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codeguruprofiler.CfnProfilingGroup",
):
    """A CloudFormation ``AWS::CodeGuruProfiler::ProfilingGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::CodeGuruProfiler::ProfilingGroup
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        profiling_group_name: str,
        agent_permissions: typing.Any = None,
        anomaly_detection_notification_configuration: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ChannelProperty", _IResolvable_9ceae33e]]]] = None,
        compute_platform: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::CodeGuruProfiler::ProfilingGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param profiling_group_name: ``AWS::CodeGuruProfiler::ProfilingGroup.ProfilingGroupName``.
        :param agent_permissions: ``AWS::CodeGuruProfiler::ProfilingGroup.AgentPermissions``.
        :param anomaly_detection_notification_configuration: ``AWS::CodeGuruProfiler::ProfilingGroup.AnomalyDetectionNotificationConfiguration``.
        :param compute_platform: ``AWS::CodeGuruProfiler::ProfilingGroup.ComputePlatform``.
        :param tags: ``AWS::CodeGuruProfiler::ProfilingGroup.Tags``.
        """
        props = CfnProfilingGroupProps(
            profiling_group_name=profiling_group_name,
            agent_permissions=agent_permissions,
            anomaly_detection_notification_configuration=anomaly_detection_notification_configuration,
            compute_platform=compute_platform,
            tags=tags,
        )

        jsii.create(CfnProfilingGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Arn
        """
        return jsii.get(self, "attrArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::CodeGuruProfiler::ProfilingGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="agentPermissions")
    def agent_permissions(self) -> typing.Any:
        """``AWS::CodeGuruProfiler::ProfilingGroup.AgentPermissions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-agentpermissions
        """
        return jsii.get(self, "agentPermissions")

    @agent_permissions.setter
    def agent_permissions(self, value: typing.Any) -> None:
        jsii.set(self, "agentPermissions", value)

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> str:
        """``AWS::CodeGuruProfiler::ProfilingGroup.ProfilingGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-profilinggroupname
        """
        return jsii.get(self, "profilingGroupName")

    @profiling_group_name.setter
    def profiling_group_name(self, value: str) -> None:
        jsii.set(self, "profilingGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="anomalyDetectionNotificationConfiguration")
    def anomaly_detection_notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ChannelProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeGuruProfiler::ProfilingGroup.AnomalyDetectionNotificationConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-anomalydetectionnotificationconfiguration
        """
        return jsii.get(self, "anomalyDetectionNotificationConfiguration")

    @anomaly_detection_notification_configuration.setter
    def anomaly_detection_notification_configuration(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ChannelProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "anomalyDetectionNotificationConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="computePlatform")
    def compute_platform(self) -> typing.Optional[str]:
        """``AWS::CodeGuruProfiler::ProfilingGroup.ComputePlatform``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-computeplatform
        """
        return jsii.get(self, "computePlatform")

    @compute_platform.setter
    def compute_platform(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "computePlatform", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_codeguruprofiler.CfnProfilingGroup.ChannelProperty",
        jsii_struct_bases=[],
        name_mapping={"channel_uri": "channelUri", "channel_id": "channelId"},
    )
    class ChannelProperty:
        def __init__(
            self, *, channel_uri: str, channel_id: typing.Optional[str] = None
        ) -> None:
            """
            :param channel_uri: ``CfnProfilingGroup.ChannelProperty.channelUri``.
            :param channel_id: ``CfnProfilingGroup.ChannelProperty.channelId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-channel.html
            """
            self._values = {
                "channel_uri": channel_uri,
            }
            if channel_id is not None:
                self._values["channel_id"] = channel_id

        @builtins.property
        def channel_uri(self) -> str:
            """``CfnProfilingGroup.ChannelProperty.channelUri``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-channel.html#cfn-codeguruprofiler-profilinggroup-channel-channeluri
            """
            return self._values.get("channel_uri")

        @builtins.property
        def channel_id(self) -> typing.Optional[str]:
            """``CfnProfilingGroup.ChannelProperty.channelId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-channel.html#cfn-codeguruprofiler-profilinggroup-channel-channelid
            """
            return self._values.get("channel_id")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codeguruprofiler.CfnProfilingGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "profiling_group_name": "profilingGroupName",
        "agent_permissions": "agentPermissions",
        "anomaly_detection_notification_configuration": "anomalyDetectionNotificationConfiguration",
        "compute_platform": "computePlatform",
        "tags": "tags",
    },
)
class CfnProfilingGroupProps:
    def __init__(
        self,
        *,
        profiling_group_name: str,
        agent_permissions: typing.Any = None,
        anomaly_detection_notification_configuration: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProfilingGroup.ChannelProperty", _IResolvable_9ceae33e]]]] = None,
        compute_platform: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::CodeGuruProfiler::ProfilingGroup``.

        :param profiling_group_name: ``AWS::CodeGuruProfiler::ProfilingGroup.ProfilingGroupName``.
        :param agent_permissions: ``AWS::CodeGuruProfiler::ProfilingGroup.AgentPermissions``.
        :param anomaly_detection_notification_configuration: ``AWS::CodeGuruProfiler::ProfilingGroup.AnomalyDetectionNotificationConfiguration``.
        :param compute_platform: ``AWS::CodeGuruProfiler::ProfilingGroup.ComputePlatform``.
        :param tags: ``AWS::CodeGuruProfiler::ProfilingGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html
        """
        self._values = {
            "profiling_group_name": profiling_group_name,
        }
        if agent_permissions is not None:
            self._values["agent_permissions"] = agent_permissions
        if anomaly_detection_notification_configuration is not None:
            self._values["anomaly_detection_notification_configuration"] = anomaly_detection_notification_configuration
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def profiling_group_name(self) -> str:
        """``AWS::CodeGuruProfiler::ProfilingGroup.ProfilingGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-profilinggroupname
        """
        return self._values.get("profiling_group_name")

    @builtins.property
    def agent_permissions(self) -> typing.Any:
        """``AWS::CodeGuruProfiler::ProfilingGroup.AgentPermissions``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-agentpermissions
        """
        return self._values.get("agent_permissions")

    @builtins.property
    def anomaly_detection_notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnProfilingGroup.ChannelProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::CodeGuruProfiler::ProfilingGroup.AnomalyDetectionNotificationConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-anomalydetectionnotificationconfiguration
        """
        return self._values.get("anomaly_detection_notification_configuration")

    @builtins.property
    def compute_platform(self) -> typing.Optional[str]:
        """``AWS::CodeGuruProfiler::ProfilingGroup.ComputePlatform``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-computeplatform
        """
        return self._values.get("compute_platform")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::CodeGuruProfiler::ProfilingGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfilingGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.aws_codeguruprofiler.ComputePlatform")
class ComputePlatform(enum.Enum):
    """The compute platform of the profiling group.

    stability
    :stability: experimental
    """

    AWS_LAMBDA = "AWS_LAMBDA"
    """Use AWS_LAMBDA if your application runs on AWS Lambda.

    stability
    :stability: experimental
    """
    DEFAULT = "DEFAULT"
    """Use Default if your application runs on a compute platform that is not AWS Lambda, such an Amazon EC2 instance, an on-premises server, or a different platform.

    stability
    :stability: experimental
    """


@jsii.interface(jsii_type="monocdk-experiment.aws_codeguruprofiler.IProfilingGroup")
class IProfilingGroup(_IResource_72f7ee7e, jsii.compat.Protocol):
    """IResource represents a Profiling Group.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IProfilingGroupProxy

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> str:
        """A name for the profiling group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.

        stability
        :stability: experimental
        """
        ...


class _IProfilingGroupProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """IResource represents a Profiling Group.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_codeguruprofiler.IProfilingGroup"

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> str:
        """A name for the profiling group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "profilingGroupName")

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantPublish", [grantee])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee])


@jsii.implements(IProfilingGroup)
class ProfilingGroup(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_codeguruprofiler.ProfilingGroup",
):
    """A new Profiling Group.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        compute_platform: typing.Optional["ComputePlatform"] = None,
        profiling_group_name: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param compute_platform: The compute platform of the profiling group. Default: ComputePlatform.DEFAULT
        :param profiling_group_name: A name for the profiling group. Default: - automatically generated name.

        stability
        :stability: experimental
        """
        props = ProfilingGroupProps(
            compute_platform=compute_platform,
            profiling_group_name=profiling_group_name,
        )

        jsii.create(ProfilingGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromProfilingGroupArn")
    @builtins.classmethod
    def from_profiling_group_arn(
        cls, scope: _Construct_f50a3f53, id: str, profiling_group_arn: str
    ) -> "IProfilingGroup":
        """Import an existing Profiling Group provided an ARN.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param profiling_group_arn: Profiling Group ARN.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromProfilingGroupArn", [scope, id, profiling_group_arn])

    @jsii.member(jsii_name="fromProfilingGroupName")
    @builtins.classmethod
    def from_profiling_group_name(
        cls, scope: _Construct_f50a3f53, id: str, profiling_group_name: str
    ) -> "IProfilingGroup":
        """Import an existing Profiling Group provided a Profiling Group Name.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param profiling_group_name: Profiling Group Name.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromProfilingGroupName", [scope, id, profiling_group_name])

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantPublish", [grantee])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @builtins.property
    @jsii.member(jsii_name="profilingGroupArn")
    def profiling_group_arn(self) -> str:
        """The ARN of the Profiling Group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "profilingGroupArn")

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> str:
        """The name of the Profiling Group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "profilingGroupName")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_codeguruprofiler.ProfilingGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_platform": "computePlatform",
        "profiling_group_name": "profilingGroupName",
    },
)
class ProfilingGroupProps:
    def __init__(
        self,
        *,
        compute_platform: typing.Optional["ComputePlatform"] = None,
        profiling_group_name: typing.Optional[str] = None,
    ) -> None:
        """Properties for creating a new Profiling Group.

        :param compute_platform: The compute platform of the profiling group. Default: ComputePlatform.DEFAULT
        :param profiling_group_name: A name for the profiling group. Default: - automatically generated name.

        stability
        :stability: experimental
        """
        self._values = {}
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if profiling_group_name is not None:
            self._values["profiling_group_name"] = profiling_group_name

    @builtins.property
    def compute_platform(self) -> typing.Optional["ComputePlatform"]:
        """The compute platform of the profiling group.

        default
        :default: ComputePlatform.DEFAULT

        stability
        :stability: experimental
        """
        return self._values.get("compute_platform")

    @builtins.property
    def profiling_group_name(self) -> typing.Optional[str]:
        """A name for the profiling group.

        default
        :default: - automatically generated name.

        stability
        :stability: experimental
        """
        return self._values.get("profiling_group_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProfilingGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnProfilingGroup",
    "CfnProfilingGroupProps",
    "ComputePlatform",
    "IProfilingGroup",
    "ProfilingGroup",
    "ProfilingGroupProps",
]

publication.publish()
