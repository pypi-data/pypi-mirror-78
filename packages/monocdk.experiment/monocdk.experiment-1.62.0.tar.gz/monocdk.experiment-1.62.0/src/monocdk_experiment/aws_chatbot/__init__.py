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
    Construct as _Construct_f50a3f53,
    IInspectable as _IInspectable_051e6ed8,
    IResource as _IResource_72f7ee7e,
    Resource as _Resource_884d0774,
    TreeInspector as _TreeInspector_154f5999,
)
from ..aws_iam import (
    IGrantable as _IGrantable_0fcfc53a,
    IPrincipal as _IPrincipal_97126874,
    IRole as _IRole_e69bbae4,
    PolicyStatement as _PolicyStatement_f75dc775,
)
from ..aws_sns import ITopic as _ITopic_ef0ebe0e


@jsii.implements(_IInspectable_051e6ed8)
class CfnSlackChannelConfiguration(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_chatbot.CfnSlackChannelConfiguration",
):
    """A CloudFormation ``AWS::Chatbot::SlackChannelConfiguration``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html
    cloudformationResource:
    :cloudformationResource:: AWS::Chatbot::SlackChannelConfiguration
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        configuration_name: str,
        iam_role_arn: str,
        slack_channel_id: str,
        slack_workspace_id: str,
        logging_level: typing.Optional[str] = None,
        sns_topic_arns: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Create a new ``AWS::Chatbot::SlackChannelConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param configuration_name: ``AWS::Chatbot::SlackChannelConfiguration.ConfigurationName``.
        :param iam_role_arn: ``AWS::Chatbot::SlackChannelConfiguration.IamRoleArn``.
        :param slack_channel_id: ``AWS::Chatbot::SlackChannelConfiguration.SlackChannelId``.
        :param slack_workspace_id: ``AWS::Chatbot::SlackChannelConfiguration.SlackWorkspaceId``.
        :param logging_level: ``AWS::Chatbot::SlackChannelConfiguration.LoggingLevel``.
        :param sns_topic_arns: ``AWS::Chatbot::SlackChannelConfiguration.SnsTopicArns``.
        """
        props = CfnSlackChannelConfigurationProps(
            configuration_name=configuration_name,
            iam_role_arn=iam_role_arn,
            slack_channel_id=slack_channel_id,
            slack_workspace_id=slack_workspace_id,
            logging_level=logging_level,
            sns_topic_arns=sns_topic_arns,
        )

        jsii.create(CfnSlackChannelConfiguration, self, [scope, id, props])

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
    @jsii.member(jsii_name="configurationName")
    def configuration_name(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.ConfigurationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-configurationname
        """
        return jsii.get(self, "configurationName")

    @configuration_name.setter
    def configuration_name(self, value: str) -> None:
        jsii.set(self, "configurationName", value)

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.IamRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-iamrolearn
        """
        return jsii.get(self, "iamRoleArn")

    @iam_role_arn.setter
    def iam_role_arn(self, value: str) -> None:
        jsii.set(self, "iamRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="slackChannelId")
    def slack_channel_id(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.SlackChannelId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackchannelid
        """
        return jsii.get(self, "slackChannelId")

    @slack_channel_id.setter
    def slack_channel_id(self, value: str) -> None:
        jsii.set(self, "slackChannelId", value)

    @builtins.property
    @jsii.member(jsii_name="slackWorkspaceId")
    def slack_workspace_id(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.SlackWorkspaceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackworkspaceid
        """
        return jsii.get(self, "slackWorkspaceId")

    @slack_workspace_id.setter
    def slack_workspace_id(self, value: str) -> None:
        jsii.set(self, "slackWorkspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="loggingLevel")
    def logging_level(self) -> typing.Optional[str]:
        """``AWS::Chatbot::SlackChannelConfiguration.LoggingLevel``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-logginglevel
        """
        return jsii.get(self, "loggingLevel")

    @logging_level.setter
    def logging_level(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "loggingLevel", value)

    @builtins.property
    @jsii.member(jsii_name="snsTopicArns")
    def sns_topic_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Chatbot::SlackChannelConfiguration.SnsTopicArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-snstopicarns
        """
        return jsii.get(self, "snsTopicArns")

    @sns_topic_arns.setter
    def sns_topic_arns(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "snsTopicArns", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_chatbot.CfnSlackChannelConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_name": "configurationName",
        "iam_role_arn": "iamRoleArn",
        "slack_channel_id": "slackChannelId",
        "slack_workspace_id": "slackWorkspaceId",
        "logging_level": "loggingLevel",
        "sns_topic_arns": "snsTopicArns",
    },
)
class CfnSlackChannelConfigurationProps:
    def __init__(
        self,
        *,
        configuration_name: str,
        iam_role_arn: str,
        slack_channel_id: str,
        slack_workspace_id: str,
        logging_level: typing.Optional[str] = None,
        sns_topic_arns: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::Chatbot::SlackChannelConfiguration``.

        :param configuration_name: ``AWS::Chatbot::SlackChannelConfiguration.ConfigurationName``.
        :param iam_role_arn: ``AWS::Chatbot::SlackChannelConfiguration.IamRoleArn``.
        :param slack_channel_id: ``AWS::Chatbot::SlackChannelConfiguration.SlackChannelId``.
        :param slack_workspace_id: ``AWS::Chatbot::SlackChannelConfiguration.SlackWorkspaceId``.
        :param logging_level: ``AWS::Chatbot::SlackChannelConfiguration.LoggingLevel``.
        :param sns_topic_arns: ``AWS::Chatbot::SlackChannelConfiguration.SnsTopicArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html
        """
        self._values = {
            "configuration_name": configuration_name,
            "iam_role_arn": iam_role_arn,
            "slack_channel_id": slack_channel_id,
            "slack_workspace_id": slack_workspace_id,
        }
        if logging_level is not None:
            self._values["logging_level"] = logging_level
        if sns_topic_arns is not None:
            self._values["sns_topic_arns"] = sns_topic_arns

    @builtins.property
    def configuration_name(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.ConfigurationName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-configurationname
        """
        return self._values.get("configuration_name")

    @builtins.property
    def iam_role_arn(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.IamRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-iamrolearn
        """
        return self._values.get("iam_role_arn")

    @builtins.property
    def slack_channel_id(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.SlackChannelId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackchannelid
        """
        return self._values.get("slack_channel_id")

    @builtins.property
    def slack_workspace_id(self) -> str:
        """``AWS::Chatbot::SlackChannelConfiguration.SlackWorkspaceId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackworkspaceid
        """
        return self._values.get("slack_workspace_id")

    @builtins.property
    def logging_level(self) -> typing.Optional[str]:
        """``AWS::Chatbot::SlackChannelConfiguration.LoggingLevel``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-logginglevel
        """
        return self._values.get("logging_level")

    @builtins.property
    def sns_topic_arns(self) -> typing.Optional[typing.List[str]]:
        """``AWS::Chatbot::SlackChannelConfiguration.SnsTopicArns``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-snstopicarns
        """
        return self._values.get("sns_topic_arns")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSlackChannelConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk-experiment.aws_chatbot.ISlackChannelConfiguration")
class ISlackChannelConfiguration(
    _IResource_72f7ee7e, _IGrantable_0fcfc53a, jsii.compat.Protocol
):
    """Represents a Slack channel configuration.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ISlackChannelConfigurationProxy

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationArn")
    def slack_channel_configuration_arn(self) -> str:
        """The ARN of the Slack channel configuration In the form of arn:aws:chatbot:{region}:{account}:chat-configuration/slack-channel/{slackChannelName}.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationName")
    def slack_channel_configuration_name(self) -> str:
        """The name of Slack channel configuration.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The permission role of Slack channel configuration.

        default
        :default: - A role will be created.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: _PolicyStatement_f75dc775) -> None:
        """Adds a statement to the IAM role.

        :param statement: -

        stability
        :stability: experimental
        """
        ...


class _ISlackChannelConfigurationProxy(
    jsii.proxy_for(_IResource_72f7ee7e), jsii.proxy_for(_IGrantable_0fcfc53a)
):
    """Represents a Slack channel configuration.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_chatbot.ISlackChannelConfiguration"

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationArn")
    def slack_channel_configuration_arn(self) -> str:
        """The ARN of the Slack channel configuration In the form of arn:aws:chatbot:{region}:{account}:chat-configuration/slack-channel/{slackChannelName}.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "slackChannelConfigurationArn")

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationName")
    def slack_channel_configuration_name(self) -> str:
        """The name of Slack channel configuration.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "slackChannelConfigurationName")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The permission role of Slack channel configuration.

        default
        :default: - A role will be created.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "role")

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: _PolicyStatement_f75dc775) -> None:
        """Adds a statement to the IAM role.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])


@jsii.enum(jsii_type="monocdk-experiment.aws_chatbot.LoggingLevel")
class LoggingLevel(enum.Enum):
    """Logging levels include ERROR, INFO, or NONE.

    stability
    :stability: experimental
    """

    ERROR = "ERROR"
    """ERROR.

    stability
    :stability: experimental
    """
    INFO = "INFO"
    """INFO.

    stability
    :stability: experimental
    """
    NONE = "NONE"
    """NONE.

    stability
    :stability: experimental
    """


@jsii.implements(ISlackChannelConfiguration)
class SlackChannelConfiguration(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_chatbot.SlackChannelConfiguration",
):
    """A new Slack channel configuration.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        slack_channel_configuration_name: str,
        slack_channel_id: str,
        slack_workspace_id: str,
        logging_level: typing.Optional["LoggingLevel"] = None,
        notification_topics: typing.Optional[typing.List[_ITopic_ef0ebe0e]] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param slack_channel_configuration_name: The name of Slack channel configuration.
        :param slack_channel_id: The ID of the Slack channel. To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ABCBBLZZZ.
        :param slack_workspace_id: The ID of the Slack workspace authorized with AWS Chatbot. To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in Setting Up AWS Chatbot with Slack in the AWS Chatbot User Guide.
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Default: LoggingLevel.NONE
        :param notification_topics: The SNS topics that deliver notifications to AWS Chatbot. Default: None
        :param role: The permission role of Slack channel configuration. Default: - A role will be created.

        stability
        :stability: experimental
        """
        props = SlackChannelConfigurationProps(
            slack_channel_configuration_name=slack_channel_configuration_name,
            slack_channel_id=slack_channel_id,
            slack_workspace_id=slack_workspace_id,
            logging_level=logging_level,
            notification_topics=notification_topics,
            role=role,
        )

        jsii.create(SlackChannelConfiguration, self, [scope, id, props])

    @jsii.member(jsii_name="fromSlackChannelConfigurationArn")
    @builtins.classmethod
    def from_slack_channel_configuration_arn(
        cls, scope: _Construct_f50a3f53, id: str, slack_channel_configuration_arn: str
    ) -> "ISlackChannelConfiguration":
        """Import an existing Slack channel configuration provided an ARN.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param slack_channel_configuration_arn: configuration ARN (i.e. arn:aws:chatbot::1234567890:chat-configuration/slack-channel/my-slack).

        return
        :return: a reference to the existing Slack channel configuration

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromSlackChannelConfigurationArn", [scope, id, slack_channel_configuration_arn])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: _PolicyStatement_f75dc775) -> None:
        """Adds extra permission to iam-role of Slack channel configuration.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_97126874:
        """The principal to grant permissions to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationArn")
    def slack_channel_configuration_arn(self) -> str:
        """The ARN of the Slack channel configuration In the form of arn:aws:chatbot:{region}:{account}:chat-configuration/slack-channel/{slackChannelName}.

        stability
        :stability: experimental
        """
        return jsii.get(self, "slackChannelConfigurationArn")

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationName")
    def slack_channel_configuration_name(self) -> str:
        """The name of Slack channel configuration.

        stability
        :stability: experimental
        """
        return jsii.get(self, "slackChannelConfigurationName")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The permission role of Slack channel configuration.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_chatbot.SlackChannelConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "slack_channel_configuration_name": "slackChannelConfigurationName",
        "slack_channel_id": "slackChannelId",
        "slack_workspace_id": "slackWorkspaceId",
        "logging_level": "loggingLevel",
        "notification_topics": "notificationTopics",
        "role": "role",
    },
)
class SlackChannelConfigurationProps:
    def __init__(
        self,
        *,
        slack_channel_configuration_name: str,
        slack_channel_id: str,
        slack_workspace_id: str,
        logging_level: typing.Optional["LoggingLevel"] = None,
        notification_topics: typing.Optional[typing.List[_ITopic_ef0ebe0e]] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
    ) -> None:
        """Properties for a new Slack channel configuration.

        :param slack_channel_configuration_name: The name of Slack channel configuration.
        :param slack_channel_id: The ID of the Slack channel. To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ABCBBLZZZ.
        :param slack_workspace_id: The ID of the Slack workspace authorized with AWS Chatbot. To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in Setting Up AWS Chatbot with Slack in the AWS Chatbot User Guide.
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Default: LoggingLevel.NONE
        :param notification_topics: The SNS topics that deliver notifications to AWS Chatbot. Default: None
        :param role: The permission role of Slack channel configuration. Default: - A role will be created.

        stability
        :stability: experimental
        """
        self._values = {
            "slack_channel_configuration_name": slack_channel_configuration_name,
            "slack_channel_id": slack_channel_id,
            "slack_workspace_id": slack_workspace_id,
        }
        if logging_level is not None:
            self._values["logging_level"] = logging_level
        if notification_topics is not None:
            self._values["notification_topics"] = notification_topics
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def slack_channel_configuration_name(self) -> str:
        """The name of Slack channel configuration.

        stability
        :stability: experimental
        """
        return self._values.get("slack_channel_configuration_name")

    @builtins.property
    def slack_channel_id(self) -> str:
        """The ID of the Slack channel.

        To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link.
        The channel ID is the 9-character string at the end of the URL. For example, ABCBBLZZZ.

        stability
        :stability: experimental
        """
        return self._values.get("slack_channel_id")

    @builtins.property
    def slack_workspace_id(self) -> str:
        """The ID of the Slack workspace authorized with AWS Chatbot.

        To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console.
        Then you can copy and paste the workspace ID from the console.
        For more details, see steps 1-4 in Setting Up AWS Chatbot with Slack in the AWS Chatbot User Guide.

        see
        :see: https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro
        stability
        :stability: experimental
        """
        return self._values.get("slack_workspace_id")

    @builtins.property
    def logging_level(self) -> typing.Optional["LoggingLevel"]:
        """Specifies the logging level for this configuration.

        This property affects the log entries pushed to Amazon CloudWatch Logs.

        default
        :default: LoggingLevel.NONE

        stability
        :stability: experimental
        """
        return self._values.get("logging_level")

    @builtins.property
    def notification_topics(self) -> typing.Optional[typing.List[_ITopic_ef0ebe0e]]:
        """The SNS topics that deliver notifications to AWS Chatbot.

        default
        :default: None

        stability
        :stability: experimental
        """
        return self._values.get("notification_topics")

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The permission role of Slack channel configuration.

        default
        :default: - A role will be created.

        stability
        :stability: experimental
        """
        return self._values.get("role")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SlackChannelConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnSlackChannelConfiguration",
    "CfnSlackChannelConfigurationProps",
    "ISlackChannelConfiguration",
    "LoggingLevel",
    "SlackChannelConfiguration",
    "SlackChannelConfigurationProps",
]

publication.publish()
