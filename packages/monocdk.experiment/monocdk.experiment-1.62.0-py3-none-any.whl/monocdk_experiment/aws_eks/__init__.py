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
    Duration as _Duration_5170c158,
    IInspectable as _IInspectable_051e6ed8,
    IResolvable as _IResolvable_9ceae33e,
    IResource as _IResource_72f7ee7e,
    ITaggable as _ITaggable_6ea67ae1,
    Resource as _Resource_884d0774,
    ResourceEnvironment as _ResourceEnvironment_5b040075,
    Stack as _Stack_05f4505a,
    TagManager as _TagManager_2508893f,
    TreeInspector as _TreeInspector_154f5999,
)
from ..aws_autoscaling import (
    AutoScalingGroup as _AutoScalingGroup_003d0b84,
    BlockDevice as _BlockDevice_6b64cf0c,
    CommonAutoScalingGroupProps as _CommonAutoScalingGroupProps_43a23fca,
    GroupMetrics as _GroupMetrics_8f5d7498,
    HealthCheck as _HealthCheck_ed599e14,
    Monitoring as _Monitoring_11cb7f01,
    NotificationConfiguration as _NotificationConfiguration_396b88c6,
    RollingUpdateConfiguration as _RollingUpdateConfiguration_c96dd49e,
    UpdateType as _UpdateType_7a2ac17e,
)
from ..aws_ec2 import (
    Connections as _Connections_231f38b5,
    IConnectable as _IConnectable_a587039f,
    IMachineImage as _IMachineImage_d5cd7b45,
    ISecurityGroup as _ISecurityGroup_d72ab8e8,
    ISubnet as _ISubnet_7f5367e6,
    IVpc as _IVpc_3795853f,
    InstanceType as _InstanceType_85a97b30,
    MachineImageConfig as _MachineImageConfig_815fc1b9,
    SubnetSelection as _SubnetSelection_36a13cd6,
)
from ..aws_iam import (
    AddToPrincipalPolicyResult as _AddToPrincipalPolicyResult_7f6eff3f,
    IPrincipal as _IPrincipal_97126874,
    IRole as _IRole_e69bbae4,
    IUser as _IUser_7e7f2b20,
    OpenIdConnectProvider as _OpenIdConnectProvider_36010b0a,
    PolicyStatement as _PolicyStatement_f75dc775,
    PrincipalPolicyFragment as _PrincipalPolicyFragment_621f702c,
    Role as _Role_6f613128,
)
from ..aws_kms import IKey as _IKey_3336c79d
from ..aws_lambda import (
    ILayerVersion as _ILayerVersion_aa5e0c0c,
    LayerVersionPermission as _LayerVersionPermission_b7d4b3d2,
    Runtime as _Runtime_8b970b80,
)
from ..aws_sns import ITopic as _ITopic_ef0ebe0e


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.AutoScalingGroupOptions",
    jsii_struct_bases=[],
    name_mapping={
        "bootstrap_enabled": "bootstrapEnabled",
        "bootstrap_options": "bootstrapOptions",
        "machine_image_type": "machineImageType",
        "map_role": "mapRole",
    },
)
class AutoScalingGroupOptions:
    def __init__(
        self,
        *,
        bootstrap_enabled: typing.Optional[bool] = None,
        bootstrap_options: typing.Optional["BootstrapOptions"] = None,
        machine_image_type: typing.Optional["MachineImageType"] = None,
        map_role: typing.Optional[bool] = None,
    ) -> None:
        """Options for adding an AutoScalingGroup as capacity.

        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: Allows options for node bootstrapping through EC2 user data. Default: - default options
        :param machine_image_type: Allow options to specify different machine image type. Default: MachineImageType.AMAZON_LINUX_2
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).

        stability
        :stability: experimental
        """
        if isinstance(bootstrap_options, dict):
            bootstrap_options = BootstrapOptions(**bootstrap_options)
        self._values = {}
        if bootstrap_enabled is not None:
            self._values["bootstrap_enabled"] = bootstrap_enabled
        if bootstrap_options is not None:
            self._values["bootstrap_options"] = bootstrap_options
        if machine_image_type is not None:
            self._values["machine_image_type"] = machine_image_type
        if map_role is not None:
            self._values["map_role"] = map_role

    @builtins.property
    def bootstrap_enabled(self) -> typing.Optional[bool]:
        """Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster.

        If you wish to provide a custom user data script, set this to ``false`` and
        manually invoke ``autoscalingGroup.addUserData()``.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("bootstrap_enabled")

    @builtins.property
    def bootstrap_options(self) -> typing.Optional["BootstrapOptions"]:
        """Allows options for node bootstrapping through EC2 user data.

        default
        :default: - default options

        stability
        :stability: experimental
        """
        return self._values.get("bootstrap_options")

    @builtins.property
    def machine_image_type(self) -> typing.Optional["MachineImageType"]:
        """Allow options to specify different machine image type.

        default
        :default: MachineImageType.AMAZON_LINUX_2

        stability
        :stability: experimental
        """
        return self._values.get("machine_image_type")

    @builtins.property
    def map_role(self) -> typing.Optional[bool]:
        """Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC.

        This cannot be explicitly set to ``true`` if the cluster has kubectl disabled.

        default
        :default: - true if the cluster has kubectl enabled (which is the default).

        stability
        :stability: experimental
        """
        return self._values.get("map_role")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoScalingGroupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsAuth(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.AwsAuth",
):
    """Manages mapping between IAM users and roles to Kubernetes RBAC configuration.

    see
    :see: https://docs.aws.amazon.com/en_us/eks/latest/userguide/add-user-role.html
    stability
    :stability: experimental
    """

    def __init__(
        self, scope: _Construct_f50a3f53, id: str, *, cluster: "Cluster"
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        props = AwsAuthProps(cluster=cluster)

        jsii.create(AwsAuth, self, [scope, id, props])

    @jsii.member(jsii_name="addAccount")
    def add_account(self, account_id: str) -> None:
        """Additional AWS account to add to the aws-auth configmap.

        :param account_id: account number.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addAccount", [account_id])

    @jsii.member(jsii_name="addMastersRole")
    def add_masters_role(
        self, role: _IRole_e69bbae4, username: typing.Optional[str] = None
    ) -> None:
        """Adds the specified IAM role to the ``system:masters`` RBAC group, which means that anyone that can assume it will be able to administer this Kubernetes system.

        :param role: The IAM role to add.
        :param username: Optional user (defaults to the role ARN).

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addMastersRole", [role, username])

    @jsii.member(jsii_name="addRoleMapping")
    def add_role_mapping(
        self,
        role: _IRole_e69bbae4,
        *,
        groups: typing.List[str],
        username: typing.Optional[str] = None,
    ) -> None:
        """Adds a mapping between an IAM role to a Kubernetes user and groups.

        :param role: The IAM role to map.
        :param groups: A list of groups within Kubernetes to which the role is mapped.
        :param username: The user name within Kubernetes to map to the IAM role. Default: - By default, the user name is the ARN of the IAM role.

        stability
        :stability: experimental
        """
        mapping = AwsAuthMapping(groups=groups, username=username)

        return jsii.invoke(self, "addRoleMapping", [role, mapping])

    @jsii.member(jsii_name="addUserMapping")
    def add_user_mapping(
        self,
        user: _IUser_7e7f2b20,
        *,
        groups: typing.List[str],
        username: typing.Optional[str] = None,
    ) -> None:
        """Adds a mapping between an IAM user to a Kubernetes user and groups.

        :param user: The IAM user to map.
        :param groups: A list of groups within Kubernetes to which the role is mapped.
        :param username: The user name within Kubernetes to map to the IAM role. Default: - By default, the user name is the ARN of the IAM role.

        stability
        :stability: experimental
        """
        mapping = AwsAuthMapping(groups=groups, username=username)

        return jsii.invoke(self, "addUserMapping", [user, mapping])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.AwsAuthMapping",
    jsii_struct_bases=[],
    name_mapping={"groups": "groups", "username": "username"},
)
class AwsAuthMapping:
    def __init__(
        self, *, groups: typing.List[str], username: typing.Optional[str] = None
    ) -> None:
        """AwsAuth mapping.

        :param groups: A list of groups within Kubernetes to which the role is mapped.
        :param username: The user name within Kubernetes to map to the IAM role. Default: - By default, the user name is the ARN of the IAM role.

        stability
        :stability: experimental
        """
        self._values = {
            "groups": groups,
        }
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def groups(self) -> typing.List[str]:
        """A list of groups within Kubernetes to which the role is mapped.

        see
        :see: https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings
        stability
        :stability: experimental
        """
        return self._values.get("groups")

    @builtins.property
    def username(self) -> typing.Optional[str]:
        """The user name within Kubernetes to map to the IAM role.

        default
        :default: - By default, the user name is the ARN of the IAM role.

        stability
        :stability: experimental
        """
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsAuthMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.AwsAuthProps",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster"},
)
class AwsAuthProps:
    def __init__(self, *, cluster: "Cluster") -> None:
        """Configuration props for the AwsAuth construct.

        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        self._values = {
            "cluster": cluster,
        }

    @builtins.property
    def cluster(self) -> "Cluster":
        """The EKS cluster to apply this configuration to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get("cluster")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsAuthProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.BootstrapOptions",
    jsii_struct_bases=[],
    name_mapping={
        "additional_args": "additionalArgs",
        "aws_api_retry_attempts": "awsApiRetryAttempts",
        "docker_config_json": "dockerConfigJson",
        "enable_docker_bridge": "enableDockerBridge",
        "kubelet_extra_args": "kubeletExtraArgs",
        "use_max_pods": "useMaxPods",
    },
)
class BootstrapOptions:
    def __init__(
        self,
        *,
        additional_args: typing.Optional[str] = None,
        aws_api_retry_attempts: typing.Optional[jsii.Number] = None,
        docker_config_json: typing.Optional[str] = None,
        enable_docker_bridge: typing.Optional[bool] = None,
        kubelet_extra_args: typing.Optional[str] = None,
        use_max_pods: typing.Optional[bool] = None,
    ) -> None:
        """EKS node bootstrapping options.

        :param additional_args: Additional command line arguments to pass to the ``/etc/eks/bootstrap.sh`` command. Default: - none
        :param aws_api_retry_attempts: Number of retry attempts for AWS API call (DescribeCluster). Default: 3
        :param docker_config_json: The contents of the ``/etc/docker/daemon.json`` file. Useful if you want a custom config differing from the default one in the EKS AMI. Default: - none
        :param enable_docker_bridge: Restores the docker default bridge network. Default: false
        :param kubelet_extra_args: Extra arguments to add to the kubelet. Useful for adding labels or taints. Default: - none
        :param use_max_pods: Sets ``--max-pods`` for the kubelet based on the capacity of the EC2 instance. Default: true

        stability
        :stability: experimental
        """
        self._values = {}
        if additional_args is not None:
            self._values["additional_args"] = additional_args
        if aws_api_retry_attempts is not None:
            self._values["aws_api_retry_attempts"] = aws_api_retry_attempts
        if docker_config_json is not None:
            self._values["docker_config_json"] = docker_config_json
        if enable_docker_bridge is not None:
            self._values["enable_docker_bridge"] = enable_docker_bridge
        if kubelet_extra_args is not None:
            self._values["kubelet_extra_args"] = kubelet_extra_args
        if use_max_pods is not None:
            self._values["use_max_pods"] = use_max_pods

    @builtins.property
    def additional_args(self) -> typing.Optional[str]:
        """Additional command line arguments to pass to the ``/etc/eks/bootstrap.sh`` command.

        default
        :default: - none

        see
        :see: https://github.com/awslabs/amazon-eks-ami/blob/master/files/bootstrap.sh
        stability
        :stability: experimental
        """
        return self._values.get("additional_args")

    @builtins.property
    def aws_api_retry_attempts(self) -> typing.Optional[jsii.Number]:
        """Number of retry attempts for AWS API call (DescribeCluster).

        default
        :default: 3

        stability
        :stability: experimental
        """
        return self._values.get("aws_api_retry_attempts")

    @builtins.property
    def docker_config_json(self) -> typing.Optional[str]:
        """The contents of the ``/etc/docker/daemon.json`` file. Useful if you want a custom config differing from the default one in the EKS AMI.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get("docker_config_json")

    @builtins.property
    def enable_docker_bridge(self) -> typing.Optional[bool]:
        """Restores the docker default bridge network.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("enable_docker_bridge")

    @builtins.property
    def kubelet_extra_args(self) -> typing.Optional[str]:
        """Extra arguments to add to the kubelet.

        Useful for adding labels or taints.

        default
        :default: - none

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            --node - labelsfoo = bar , goo = far
        """
        return self._values.get("kubelet_extra_args")

    @builtins.property
    def use_max_pods(self) -> typing.Optional[bool]:
        """Sets ``--max-pods`` for the kubelet based on the capacity of the EC2 instance.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("use_max_pods")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BootstrapOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.CapacityOptions",
    jsii_struct_bases=[_CommonAutoScalingGroupProps_43a23fca],
    name_mapping={
        "allow_all_outbound": "allowAllOutbound",
        "associate_public_ip_address": "associatePublicIpAddress",
        "auto_scaling_group_name": "autoScalingGroupName",
        "block_devices": "blockDevices",
        "cooldown": "cooldown",
        "desired_capacity": "desiredCapacity",
        "group_metrics": "groupMetrics",
        "health_check": "healthCheck",
        "ignore_unmodified_size_properties": "ignoreUnmodifiedSizeProperties",
        "instance_monitoring": "instanceMonitoring",
        "key_name": "keyName",
        "max_capacity": "maxCapacity",
        "max_instance_lifetime": "maxInstanceLifetime",
        "min_capacity": "minCapacity",
        "notifications": "notifications",
        "notifications_topic": "notificationsTopic",
        "replacing_update_min_successful_instances_percent": "replacingUpdateMinSuccessfulInstancesPercent",
        "resource_signal_count": "resourceSignalCount",
        "resource_signal_timeout": "resourceSignalTimeout",
        "rolling_update_configuration": "rollingUpdateConfiguration",
        "spot_price": "spotPrice",
        "update_type": "updateType",
        "vpc_subnets": "vpcSubnets",
        "instance_type": "instanceType",
        "bootstrap_enabled": "bootstrapEnabled",
        "bootstrap_options": "bootstrapOptions",
        "machine_image_type": "machineImageType",
        "map_role": "mapRole",
    },
)
class CapacityOptions(_CommonAutoScalingGroupProps_43a23fca):
    def __init__(
        self,
        *,
        allow_all_outbound: typing.Optional[bool] = None,
        associate_public_ip_address: typing.Optional[bool] = None,
        auto_scaling_group_name: typing.Optional[str] = None,
        block_devices: typing.Optional[typing.List[_BlockDevice_6b64cf0c]] = None,
        cooldown: typing.Optional[_Duration_5170c158] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        group_metrics: typing.Optional[typing.List[_GroupMetrics_8f5d7498]] = None,
        health_check: typing.Optional[_HealthCheck_ed599e14] = None,
        ignore_unmodified_size_properties: typing.Optional[bool] = None,
        instance_monitoring: typing.Optional[_Monitoring_11cb7f01] = None,
        key_name: typing.Optional[str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_instance_lifetime: typing.Optional[_Duration_5170c158] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        notifications: typing.Optional[typing.List[_NotificationConfiguration_396b88c6]] = None,
        notifications_topic: typing.Optional[_ITopic_ef0ebe0e] = None,
        replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number] = None,
        resource_signal_count: typing.Optional[jsii.Number] = None,
        resource_signal_timeout: typing.Optional[_Duration_5170c158] = None,
        rolling_update_configuration: typing.Optional[_RollingUpdateConfiguration_c96dd49e] = None,
        spot_price: typing.Optional[str] = None,
        update_type: typing.Optional[_UpdateType_7a2ac17e] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        instance_type: _InstanceType_85a97b30,
        bootstrap_enabled: typing.Optional[bool] = None,
        bootstrap_options: typing.Optional["BootstrapOptions"] = None,
        machine_image_type: typing.Optional["MachineImageType"] = None,
        map_role: typing.Optional[bool] = None,
    ) -> None:
        """Options for adding worker nodes.

        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param auto_scaling_group_name: The name of the Auto Scaling group. This name must be unique per Region per account. Default: - Auto generated by CloudFormation
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. If this is set to a number, every deployment will reset the amount of instances to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param group_metrics: Enable monitoring for group metrics, these metrics describe the group rather than any of its instances. To report all group metrics use ``GroupMetrics.all()`` Group metrics are reported in a granularity of 1 minute at no additional charge. Default: - no group metrics will be reported
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param instance_monitoring: Controls whether instances in this group are launched with detailed or basic monitoring. When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes. Default: - Monitoring.DETAILED
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param max_instance_lifetime: The maximum amount of time that an instance can be in service. The maximum duration applies to all current and future instances in the group. As an instance approaches its maximum duration, it is terminated and replaced, and cannot be used again. You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value, leave this property undefined. Default: none
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications: Configure autoscaling group to send notifications about fleet changes to an SNS topic(s). Default: - No fleet change notifications will be sent.
        :param notifications_topic: SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1
        :param resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
        :param rolling_update_configuration: Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_type: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.
        :param instance_type: Instance type of the instances to start.
        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: EKS node bootstrapping options. Default: - none
        :param machine_image_type: Machine image type. Default: MachineImageType.AMAZON_LINUX_2
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).

        stability
        :stability: experimental
        """
        if isinstance(rolling_update_configuration, dict):
            rolling_update_configuration = _RollingUpdateConfiguration_c96dd49e(**rolling_update_configuration)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        if isinstance(bootstrap_options, dict):
            bootstrap_options = BootstrapOptions(**bootstrap_options)
        self._values = {
            "instance_type": instance_type,
        }
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if associate_public_ip_address is not None:
            self._values["associate_public_ip_address"] = associate_public_ip_address
        if auto_scaling_group_name is not None:
            self._values["auto_scaling_group_name"] = auto_scaling_group_name
        if block_devices is not None:
            self._values["block_devices"] = block_devices
        if cooldown is not None:
            self._values["cooldown"] = cooldown
        if desired_capacity is not None:
            self._values["desired_capacity"] = desired_capacity
        if group_metrics is not None:
            self._values["group_metrics"] = group_metrics
        if health_check is not None:
            self._values["health_check"] = health_check
        if ignore_unmodified_size_properties is not None:
            self._values["ignore_unmodified_size_properties"] = ignore_unmodified_size_properties
        if instance_monitoring is not None:
            self._values["instance_monitoring"] = instance_monitoring
        if key_name is not None:
            self._values["key_name"] = key_name
        if max_capacity is not None:
            self._values["max_capacity"] = max_capacity
        if max_instance_lifetime is not None:
            self._values["max_instance_lifetime"] = max_instance_lifetime
        if min_capacity is not None:
            self._values["min_capacity"] = min_capacity
        if notifications is not None:
            self._values["notifications"] = notifications
        if notifications_topic is not None:
            self._values["notifications_topic"] = notifications_topic
        if replacing_update_min_successful_instances_percent is not None:
            self._values["replacing_update_min_successful_instances_percent"] = replacing_update_min_successful_instances_percent
        if resource_signal_count is not None:
            self._values["resource_signal_count"] = resource_signal_count
        if resource_signal_timeout is not None:
            self._values["resource_signal_timeout"] = resource_signal_timeout
        if rolling_update_configuration is not None:
            self._values["rolling_update_configuration"] = rolling_update_configuration
        if spot_price is not None:
            self._values["spot_price"] = spot_price
        if update_type is not None:
            self._values["update_type"] = update_type
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if bootstrap_enabled is not None:
            self._values["bootstrap_enabled"] = bootstrap_enabled
        if bootstrap_options is not None:
            self._values["bootstrap_options"] = bootstrap_options
        if machine_image_type is not None:
            self._values["machine_image_type"] = machine_image_type
        if map_role is not None:
            self._values["map_role"] = map_role

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether the instances can initiate connections to anywhere by default.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("allow_all_outbound")

    @builtins.property
    def associate_public_ip_address(self) -> typing.Optional[bool]:
        """Whether instances in the Auto Scaling Group should have public IP addresses associated with them.

        default
        :default: - Use subnet setting.

        stability
        :stability: experimental
        """
        return self._values.get("associate_public_ip_address")

    @builtins.property
    def auto_scaling_group_name(self) -> typing.Optional[str]:
        """The name of the Auto Scaling group.

        This name must be unique per Region per account.

        default
        :default: - Auto generated by CloudFormation

        stability
        :stability: experimental
        """
        return self._values.get("auto_scaling_group_name")

    @builtins.property
    def block_devices(self) -> typing.Optional[typing.List[_BlockDevice_6b64cf0c]]:
        """Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes.

        Each instance that is launched has an associated root device volume,
        either an Amazon EBS volume or an instance store volume.
        You can use block device mappings to specify additional EBS volumes or
        instance store volumes to attach to an instance when it is launched.

        default
        :default: - Uses the block device mapping of the AMI

        see
        :see: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/block-device-mapping-concepts.html
        stability
        :stability: experimental
        """
        return self._values.get("block_devices")

    @builtins.property
    def cooldown(self) -> typing.Optional[_Duration_5170c158]:
        """Default scaling cooldown for this AutoScalingGroup.

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get("cooldown")

    @builtins.property
    def desired_capacity(self) -> typing.Optional[jsii.Number]:
        """Initial amount of instances in the fleet.

        If this is set to a number, every deployment will reset the amount of
        instances to this number. It is recommended to leave this value blank.

        default
        :default: minCapacity, and leave unchanged during deployment

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-desiredcapacity
        stability
        :stability: experimental
        """
        return self._values.get("desired_capacity")

    @builtins.property
    def group_metrics(self) -> typing.Optional[typing.List[_GroupMetrics_8f5d7498]]:
        """Enable monitoring for group metrics, these metrics describe the group rather than any of its instances.

        To report all group metrics use ``GroupMetrics.all()``
        Group metrics are reported in a granularity of 1 minute at no additional charge.

        default
        :default: - no group metrics will be reported

        stability
        :stability: experimental
        """
        return self._values.get("group_metrics")

    @builtins.property
    def health_check(self) -> typing.Optional[_HealthCheck_ed599e14]:
        """Configuration for health checks.

        default
        :default: - HealthCheck.ec2 with no grace period

        stability
        :stability: experimental
        """
        return self._values.get("health_check")

    @builtins.property
    def ignore_unmodified_size_properties(self) -> typing.Optional[bool]:
        """If the ASG has scheduled actions, don't reset unchanged group sizes.

        Only used if the ASG has scheduled actions (which may scale your ASG up
        or down regardless of cdk deployments). If true, the size of the group
        will only be reset if it has been changed in the CDK app. If false, the
        sizes will always be changed back to what they were in the CDK app
        on deployment.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("ignore_unmodified_size_properties")

    @builtins.property
    def instance_monitoring(self) -> typing.Optional[_Monitoring_11cb7f01]:
        """Controls whether instances in this group are launched with detailed or basic monitoring.

        When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account
        is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes.

        default
        :default: - Monitoring.DETAILED

        see
        :see: https://docs.aws.amazon.com/autoscaling/latest/userguide/as-instance-monitoring.html#enable-as-instance-metrics
        stability
        :stability: experimental
        """
        return self._values.get("instance_monitoring")

    @builtins.property
    def key_name(self) -> typing.Optional[str]:
        """Name of SSH keypair to grant access to instances.

        default
        :default: - No SSH access will be possible.

        stability
        :stability: experimental
        """
        return self._values.get("key_name")

    @builtins.property
    def max_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum number of instances in the fleet.

        default
        :default: desiredCapacity

        stability
        :stability: experimental
        """
        return self._values.get("max_capacity")

    @builtins.property
    def max_instance_lifetime(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum amount of time that an instance can be in service.

        The maximum duration applies
        to all current and future instances in the group. As an instance approaches its maximum duration,
        it is terminated and replaced, and cannot be used again.

        You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value,
        leave this property undefined.

        default
        :default: none

        see
        :see: https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-max-instance-lifetime.html
        stability
        :stability: experimental
        """
        return self._values.get("max_instance_lifetime")

    @builtins.property
    def min_capacity(self) -> typing.Optional[jsii.Number]:
        """Minimum number of instances in the fleet.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get("min_capacity")

    @builtins.property
    def notifications(
        self,
    ) -> typing.Optional[typing.List[_NotificationConfiguration_396b88c6]]:
        """Configure autoscaling group to send notifications about fleet changes to an SNS topic(s).

        default
        :default: - No fleet change notifications will be sent.

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-notificationconfigurations
        stability
        :stability: experimental
        """
        return self._values.get("notifications")

    @builtins.property
    def notifications_topic(self) -> typing.Optional[_ITopic_ef0ebe0e]:
        """SNS topic to send notifications about fleet changes.

        default
        :default: - No fleet change notifications will be sent.

        deprecated
        :deprecated: use ``notifications``

        stability
        :stability: deprecated
        """
        return self._values.get("notifications_topic")

    @builtins.property
    def replacing_update_min_successful_instances_percent(
        self,
    ) -> typing.Optional[jsii.Number]:
        """Configuration for replacing updates.

        Only used if updateType == UpdateType.ReplacingUpdate. Specifies how
        many instances must signal success for the update to succeed.

        default
        :default: minSuccessfulInstancesPercent

        stability
        :stability: experimental
        """
        return self._values.get("replacing_update_min_successful_instances_percent")

    @builtins.property
    def resource_signal_count(self) -> typing.Optional[jsii.Number]:
        """How many ResourceSignal calls CloudFormation expects before the resource is considered created.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get("resource_signal_count")

    @builtins.property
    def resource_signal_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The length of time to wait for the resourceSignalCount.

        The maximum value is 43200 (12 hours).

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get("resource_signal_timeout")

    @builtins.property
    def rolling_update_configuration(
        self,
    ) -> typing.Optional[_RollingUpdateConfiguration_c96dd49e]:
        """Configuration for rolling updates.

        Only used if updateType == UpdateType.RollingUpdate.

        default
        :default: - RollingUpdateConfiguration with defaults.

        stability
        :stability: experimental
        """
        return self._values.get("rolling_update_configuration")

    @builtins.property
    def spot_price(self) -> typing.Optional[str]:
        """The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request.

        Spot Instances are
        launched when the price you specify exceeds the current Spot market price.

        default
        :default: none

        stability
        :stability: experimental
        """
        return self._values.get("spot_price")

    @builtins.property
    def update_type(self) -> typing.Optional[_UpdateType_7a2ac17e]:
        """What to do when an AutoScalingGroup's instance configuration is changed.

        This is applied when any of the settings on the ASG are changed that
        affect how the instances should be created (VPC, instance type, startup
        scripts, etc.). It indicates how the existing instances should be
        replaced with new instances matching the new config. By default, nothing
        is done and only new instances are launched with the new config.

        default
        :default: UpdateType.None

        stability
        :stability: experimental
        """
        return self._values.get("update_type")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Where to place instances within the VPC.

        default
        :default: - All Private subnets.

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    @builtins.property
    def instance_type(self) -> _InstanceType_85a97b30:
        """Instance type of the instances to start.

        stability
        :stability: experimental
        """
        return self._values.get("instance_type")

    @builtins.property
    def bootstrap_enabled(self) -> typing.Optional[bool]:
        """Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster.

        If you wish to provide a custom user data script, set this to ``false`` and
        manually invoke ``autoscalingGroup.addUserData()``.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("bootstrap_enabled")

    @builtins.property
    def bootstrap_options(self) -> typing.Optional["BootstrapOptions"]:
        """EKS node bootstrapping options.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get("bootstrap_options")

    @builtins.property
    def machine_image_type(self) -> typing.Optional["MachineImageType"]:
        """Machine image type.

        default
        :default: MachineImageType.AMAZON_LINUX_2

        stability
        :stability: experimental
        """
        return self._values.get("machine_image_type")

    @builtins.property
    def map_role(self) -> typing.Optional[bool]:
        """Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC.

        This cannot be explicitly set to ``true`` if the cluster has kubectl disabled.

        default
        :default: - true if the cluster has kubectl enabled (which is the default).

        stability
        :stability: experimental
        """
        return self._values.get("map_role")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CapacityOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnCluster(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.CfnCluster",
):
    """A CloudFormation ``AWS::EKS::Cluster``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html
    cloudformationResource:
    :cloudformationResource:: AWS::EKS::Cluster
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        resources_vpc_config: typing.Union["ResourcesVpcConfigProperty", _IResolvable_9ceae33e],
        role_arn: str,
        encryption_config: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EncryptionConfigProperty", _IResolvable_9ceae33e]]]] = None,
        name: typing.Optional[str] = None,
        version: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::EKS::Cluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resources_vpc_config: ``AWS::EKS::Cluster.ResourcesVpcConfig``.
        :param role_arn: ``AWS::EKS::Cluster.RoleArn``.
        :param encryption_config: ``AWS::EKS::Cluster.EncryptionConfig``.
        :param name: ``AWS::EKS::Cluster.Name``.
        :param version: ``AWS::EKS::Cluster.Version``.
        """
        props = CfnClusterProps(
            resources_vpc_config=resources_vpc_config,
            role_arn=role_arn,
            encryption_config=encryption_config,
            name=name,
            version=version,
        )

        jsii.create(CfnCluster, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrCertificateAuthorityData")
    def attr_certificate_authority_data(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: CertificateAuthorityData
        """
        return jsii.get(self, "attrCertificateAuthorityData")

    @builtins.property
    @jsii.member(jsii_name="attrClusterSecurityGroupId")
    def attr_cluster_security_group_id(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ClusterSecurityGroupId
        """
        return jsii.get(self, "attrClusterSecurityGroupId")

    @builtins.property
    @jsii.member(jsii_name="attrEncryptionConfigKeyArn")
    def attr_encryption_config_key_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: EncryptionConfigKeyArn
        """
        return jsii.get(self, "attrEncryptionConfigKeyArn")

    @builtins.property
    @jsii.member(jsii_name="attrEndpoint")
    def attr_endpoint(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint
        """
        return jsii.get(self, "attrEndpoint")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="resourcesVpcConfig")
    def resources_vpc_config(
        self,
    ) -> typing.Union["ResourcesVpcConfigProperty", _IResolvable_9ceae33e]:
        """``AWS::EKS::Cluster.ResourcesVpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-resourcesvpcconfig
        """
        return jsii.get(self, "resourcesVpcConfig")

    @resources_vpc_config.setter
    def resources_vpc_config(
        self, value: typing.Union["ResourcesVpcConfigProperty", _IResolvable_9ceae33e]
    ) -> None:
        jsii.set(self, "resourcesVpcConfig", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """``AWS::EKS::Cluster.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="encryptionConfig")
    def encryption_config(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EncryptionConfigProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::EKS::Cluster.EncryptionConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-encryptionconfig
        """
        return jsii.get(self, "encryptionConfig")

    @encryption_config.setter
    def encryption_config(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["EncryptionConfigProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "encryptionConfig", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[str]:
        """``AWS::EKS::Cluster.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-name
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[str]:
        """``AWS::EKS::Cluster.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-version
        """
        return jsii.get(self, "version")

    @version.setter
    def version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "version", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_eks.CfnCluster.EncryptionConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"provider": "provider", "resources": "resources"},
    )
    class EncryptionConfigProperty:
        def __init__(
            self,
            *,
            provider: typing.Optional[typing.Union["CfnCluster.ProviderProperty", _IResolvable_9ceae33e]] = None,
            resources: typing.Optional[typing.List[str]] = None,
        ) -> None:
            """
            :param provider: ``CfnCluster.EncryptionConfigProperty.Provider``.
            :param resources: ``CfnCluster.EncryptionConfigProperty.Resources``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-encryptionconfig.html
            """
            self._values = {}
            if provider is not None:
                self._values["provider"] = provider
            if resources is not None:
                self._values["resources"] = resources

        @builtins.property
        def provider(
            self,
        ) -> typing.Optional[typing.Union["CfnCluster.ProviderProperty", _IResolvable_9ceae33e]]:
            """``CfnCluster.EncryptionConfigProperty.Provider``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-encryptionconfig.html#cfn-eks-cluster-encryptionconfig-provider
            """
            return self._values.get("provider")

        @builtins.property
        def resources(self) -> typing.Optional[typing.List[str]]:
            """``CfnCluster.EncryptionConfigProperty.Resources``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-encryptionconfig.html#cfn-eks-cluster-encryptionconfig-resources
            """
            return self._values.get("resources")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_eks.CfnCluster.ProviderProperty",
        jsii_struct_bases=[],
        name_mapping={"key_arn": "keyArn"},
    )
    class ProviderProperty:
        def __init__(self, *, key_arn: typing.Optional[str] = None) -> None:
            """
            :param key_arn: ``CfnCluster.ProviderProperty.KeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-provider.html
            """
            self._values = {}
            if key_arn is not None:
                self._values["key_arn"] = key_arn

        @builtins.property
        def key_arn(self) -> typing.Optional[str]:
            """``CfnCluster.ProviderProperty.KeyArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-provider.html#cfn-eks-cluster-provider-keyarn
            """
            return self._values.get("key_arn")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_eks.CfnCluster.ResourcesVpcConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "subnet_ids": "subnetIds",
            "security_group_ids": "securityGroupIds",
        },
    )
    class ResourcesVpcConfigProperty:
        def __init__(
            self,
            *,
            subnet_ids: typing.List[str],
            security_group_ids: typing.Optional[typing.List[str]] = None,
        ) -> None:
            """
            :param subnet_ids: ``CfnCluster.ResourcesVpcConfigProperty.SubnetIds``.
            :param security_group_ids: ``CfnCluster.ResourcesVpcConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html
            """
            self._values = {
                "subnet_ids": subnet_ids,
            }
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids

        @builtins.property
        def subnet_ids(self) -> typing.List[str]:
            """``CfnCluster.ResourcesVpcConfigProperty.SubnetIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html#cfn-eks-cluster-resourcesvpcconfig-subnetids
            """
            return self._values.get("subnet_ids")

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[str]]:
            """``CfnCluster.ResourcesVpcConfigProperty.SecurityGroupIds``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-cluster-resourcesvpcconfig.html#cfn-eks-cluster-resourcesvpcconfig-securitygroupids
            """
            return self._values.get("security_group_ids")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourcesVpcConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.CfnClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "resources_vpc_config": "resourcesVpcConfig",
        "role_arn": "roleArn",
        "encryption_config": "encryptionConfig",
        "name": "name",
        "version": "version",
    },
)
class CfnClusterProps:
    def __init__(
        self,
        *,
        resources_vpc_config: typing.Union["CfnCluster.ResourcesVpcConfigProperty", _IResolvable_9ceae33e],
        role_arn: str,
        encryption_config: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnCluster.EncryptionConfigProperty", _IResolvable_9ceae33e]]]] = None,
        name: typing.Optional[str] = None,
        version: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::EKS::Cluster``.

        :param resources_vpc_config: ``AWS::EKS::Cluster.ResourcesVpcConfig``.
        :param role_arn: ``AWS::EKS::Cluster.RoleArn``.
        :param encryption_config: ``AWS::EKS::Cluster.EncryptionConfig``.
        :param name: ``AWS::EKS::Cluster.Name``.
        :param version: ``AWS::EKS::Cluster.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html
        """
        self._values = {
            "resources_vpc_config": resources_vpc_config,
            "role_arn": role_arn,
        }
        if encryption_config is not None:
            self._values["encryption_config"] = encryption_config
        if name is not None:
            self._values["name"] = name
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def resources_vpc_config(
        self,
    ) -> typing.Union["CfnCluster.ResourcesVpcConfigProperty", _IResolvable_9ceae33e]:
        """``AWS::EKS::Cluster.ResourcesVpcConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-resourcesvpcconfig
        """
        return self._values.get("resources_vpc_config")

    @builtins.property
    def role_arn(self) -> str:
        """``AWS::EKS::Cluster.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-rolearn
        """
        return self._values.get("role_arn")

    @builtins.property
    def encryption_config(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnCluster.EncryptionConfigProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::EKS::Cluster.EncryptionConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-encryptionconfig
        """
        return self._values.get("encryption_config")

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """``AWS::EKS::Cluster.Name``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-name
        """
        return self._values.get("name")

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """``AWS::EKS::Cluster.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-cluster.html#cfn-eks-cluster-version
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnNodegroup(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.CfnNodegroup",
):
    """A CloudFormation ``AWS::EKS::Nodegroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::EKS::Nodegroup
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cluster_name: str,
        node_role: str,
        subnets: typing.List[str],
        ami_type: typing.Optional[str] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        instance_types: typing.Optional[typing.List[str]] = None,
        labels: typing.Any = None,
        nodegroup_name: typing.Optional[str] = None,
        release_version: typing.Optional[str] = None,
        remote_access: typing.Optional[typing.Union["RemoteAccessProperty", _IResolvable_9ceae33e]] = None,
        scaling_config: typing.Optional[typing.Union["ScalingConfigProperty", _IResolvable_9ceae33e]] = None,
        tags: typing.Any = None,
        version: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::EKS::Nodegroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param cluster_name: ``AWS::EKS::Nodegroup.ClusterName``.
        :param node_role: ``AWS::EKS::Nodegroup.NodeRole``.
        :param subnets: ``AWS::EKS::Nodegroup.Subnets``.
        :param ami_type: ``AWS::EKS::Nodegroup.AmiType``.
        :param disk_size: ``AWS::EKS::Nodegroup.DiskSize``.
        :param force_update_enabled: ``AWS::EKS::Nodegroup.ForceUpdateEnabled``.
        :param instance_types: ``AWS::EKS::Nodegroup.InstanceTypes``.
        :param labels: ``AWS::EKS::Nodegroup.Labels``.
        :param nodegroup_name: ``AWS::EKS::Nodegroup.NodegroupName``.
        :param release_version: ``AWS::EKS::Nodegroup.ReleaseVersion``.
        :param remote_access: ``AWS::EKS::Nodegroup.RemoteAccess``.
        :param scaling_config: ``AWS::EKS::Nodegroup.ScalingConfig``.
        :param tags: ``AWS::EKS::Nodegroup.Tags``.
        :param version: ``AWS::EKS::Nodegroup.Version``.
        """
        props = CfnNodegroupProps(
            cluster_name=cluster_name,
            node_role=node_role,
            subnets=subnets,
            ami_type=ami_type,
            disk_size=disk_size,
            force_update_enabled=force_update_enabled,
            instance_types=instance_types,
            labels=labels,
            nodegroup_name=nodegroup_name,
            release_version=release_version,
            remote_access=remote_access,
            scaling_config=scaling_config,
            tags=tags,
            version=version,
        )

        jsii.create(CfnNodegroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrClusterName")
    def attr_cluster_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ClusterName
        """
        return jsii.get(self, "attrClusterName")

    @builtins.property
    @jsii.member(jsii_name="attrNodegroupName")
    def attr_nodegroup_name(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: NodegroupName
        """
        return jsii.get(self, "attrNodegroupName")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::EKS::Nodegroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """``AWS::EKS::Nodegroup.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-clustername
        """
        return jsii.get(self, "clusterName")

    @cluster_name.setter
    def cluster_name(self, value: str) -> None:
        jsii.set(self, "clusterName", value)

    @builtins.property
    @jsii.member(jsii_name="labels")
    def labels(self) -> typing.Any:
        """``AWS::EKS::Nodegroup.Labels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-labels
        """
        return jsii.get(self, "labels")

    @labels.setter
    def labels(self, value: typing.Any) -> None:
        jsii.set(self, "labels", value)

    @builtins.property
    @jsii.member(jsii_name="nodeRole")
    def node_role(self) -> str:
        """``AWS::EKS::Nodegroup.NodeRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-noderole
        """
        return jsii.get(self, "nodeRole")

    @node_role.setter
    def node_role(self, value: str) -> None:
        jsii.set(self, "nodeRole", value)

    @builtins.property
    @jsii.member(jsii_name="subnets")
    def subnets(self) -> typing.List[str]:
        """``AWS::EKS::Nodegroup.Subnets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-subnets
        """
        return jsii.get(self, "subnets")

    @subnets.setter
    def subnets(self, value: typing.List[str]) -> None:
        jsii.set(self, "subnets", value)

    @builtins.property
    @jsii.member(jsii_name="amiType")
    def ami_type(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.AmiType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-amitype
        """
        return jsii.get(self, "amiType")

    @ami_type.setter
    def ami_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "amiType", value)

    @builtins.property
    @jsii.member(jsii_name="diskSize")
    def disk_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::EKS::Nodegroup.DiskSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-disksize
        """
        return jsii.get(self, "diskSize")

    @disk_size.setter
    def disk_size(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "diskSize", value)

    @builtins.property
    @jsii.member(jsii_name="forceUpdateEnabled")
    def force_update_enabled(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::EKS::Nodegroup.ForceUpdateEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-forceupdateenabled
        """
        return jsii.get(self, "forceUpdateEnabled")

    @force_update_enabled.setter
    def force_update_enabled(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "forceUpdateEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="instanceTypes")
    def instance_types(self) -> typing.Optional[typing.List[str]]:
        """``AWS::EKS::Nodegroup.InstanceTypes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-instancetypes
        """
        return jsii.get(self, "instanceTypes")

    @instance_types.setter
    def instance_types(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "instanceTypes", value)

    @builtins.property
    @jsii.member(jsii_name="nodegroupName")
    def nodegroup_name(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.NodegroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-nodegroupname
        """
        return jsii.get(self, "nodegroupName")

    @nodegroup_name.setter
    def nodegroup_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "nodegroupName", value)

    @builtins.property
    @jsii.member(jsii_name="releaseVersion")
    def release_version(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.ReleaseVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-releaseversion
        """
        return jsii.get(self, "releaseVersion")

    @release_version.setter
    def release_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "releaseVersion", value)

    @builtins.property
    @jsii.member(jsii_name="remoteAccess")
    def remote_access(
        self,
    ) -> typing.Optional[typing.Union["RemoteAccessProperty", _IResolvable_9ceae33e]]:
        """``AWS::EKS::Nodegroup.RemoteAccess``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-remoteaccess
        """
        return jsii.get(self, "remoteAccess")

    @remote_access.setter
    def remote_access(
        self,
        value: typing.Optional[typing.Union["RemoteAccessProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "remoteAccess", value)

    @builtins.property
    @jsii.member(jsii_name="scalingConfig")
    def scaling_config(
        self,
    ) -> typing.Optional[typing.Union["ScalingConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::EKS::Nodegroup.ScalingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-scalingconfig
        """
        return jsii.get(self, "scalingConfig")

    @scaling_config.setter
    def scaling_config(
        self,
        value: typing.Optional[typing.Union["ScalingConfigProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "scalingConfig", value)

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-version
        """
        return jsii.get(self, "version")

    @version.setter
    def version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "version", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_eks.CfnNodegroup.RemoteAccessProperty",
        jsii_struct_bases=[],
        name_mapping={
            "ec2_ssh_key": "ec2SshKey",
            "source_security_groups": "sourceSecurityGroups",
        },
    )
    class RemoteAccessProperty:
        def __init__(
            self,
            *,
            ec2_ssh_key: str,
            source_security_groups: typing.Optional[typing.List[str]] = None,
        ) -> None:
            """
            :param ec2_ssh_key: ``CfnNodegroup.RemoteAccessProperty.Ec2SshKey``.
            :param source_security_groups: ``CfnNodegroup.RemoteAccessProperty.SourceSecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html
            """
            self._values = {
                "ec2_ssh_key": ec2_ssh_key,
            }
            if source_security_groups is not None:
                self._values["source_security_groups"] = source_security_groups

        @builtins.property
        def ec2_ssh_key(self) -> str:
            """``CfnNodegroup.RemoteAccessProperty.Ec2SshKey``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html#cfn-eks-nodegroup-remoteaccess-ec2sshkey
            """
            return self._values.get("ec2_ssh_key")

        @builtins.property
        def source_security_groups(self) -> typing.Optional[typing.List[str]]:
            """``CfnNodegroup.RemoteAccessProperty.SourceSecurityGroups``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html#cfn-eks-nodegroup-remoteaccess-sourcesecuritygroups
            """
            return self._values.get("source_security_groups")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RemoteAccessProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_eks.CfnNodegroup.ScalingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "desired_size": "desiredSize",
            "max_size": "maxSize",
            "min_size": "minSize",
        },
    )
    class ScalingConfigProperty:
        def __init__(
            self,
            *,
            desired_size: typing.Optional[jsii.Number] = None,
            max_size: typing.Optional[jsii.Number] = None,
            min_size: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param desired_size: ``CfnNodegroup.ScalingConfigProperty.DesiredSize``.
            :param max_size: ``CfnNodegroup.ScalingConfigProperty.MaxSize``.
            :param min_size: ``CfnNodegroup.ScalingConfigProperty.MinSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html
            """
            self._values = {}
            if desired_size is not None:
                self._values["desired_size"] = desired_size
            if max_size is not None:
                self._values["max_size"] = max_size
            if min_size is not None:
                self._values["min_size"] = min_size

        @builtins.property
        def desired_size(self) -> typing.Optional[jsii.Number]:
            """``CfnNodegroup.ScalingConfigProperty.DesiredSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html#cfn-eks-nodegroup-scalingconfig-desiredsize
            """
            return self._values.get("desired_size")

        @builtins.property
        def max_size(self) -> typing.Optional[jsii.Number]:
            """``CfnNodegroup.ScalingConfigProperty.MaxSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html#cfn-eks-nodegroup-scalingconfig-maxsize
            """
            return self._values.get("max_size")

        @builtins.property
        def min_size(self) -> typing.Optional[jsii.Number]:
            """``CfnNodegroup.ScalingConfigProperty.MinSize``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-scalingconfig.html#cfn-eks-nodegroup-scalingconfig-minsize
            """
            return self._values.get("min_size")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.CfnNodegroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_name": "clusterName",
        "node_role": "nodeRole",
        "subnets": "subnets",
        "ami_type": "amiType",
        "disk_size": "diskSize",
        "force_update_enabled": "forceUpdateEnabled",
        "instance_types": "instanceTypes",
        "labels": "labels",
        "nodegroup_name": "nodegroupName",
        "release_version": "releaseVersion",
        "remote_access": "remoteAccess",
        "scaling_config": "scalingConfig",
        "tags": "tags",
        "version": "version",
    },
)
class CfnNodegroupProps:
    def __init__(
        self,
        *,
        cluster_name: str,
        node_role: str,
        subnets: typing.List[str],
        ami_type: typing.Optional[str] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update_enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        instance_types: typing.Optional[typing.List[str]] = None,
        labels: typing.Any = None,
        nodegroup_name: typing.Optional[str] = None,
        release_version: typing.Optional[str] = None,
        remote_access: typing.Optional[typing.Union["CfnNodegroup.RemoteAccessProperty", _IResolvable_9ceae33e]] = None,
        scaling_config: typing.Optional[typing.Union["CfnNodegroup.ScalingConfigProperty", _IResolvable_9ceae33e]] = None,
        tags: typing.Any = None,
        version: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::EKS::Nodegroup``.

        :param cluster_name: ``AWS::EKS::Nodegroup.ClusterName``.
        :param node_role: ``AWS::EKS::Nodegroup.NodeRole``.
        :param subnets: ``AWS::EKS::Nodegroup.Subnets``.
        :param ami_type: ``AWS::EKS::Nodegroup.AmiType``.
        :param disk_size: ``AWS::EKS::Nodegroup.DiskSize``.
        :param force_update_enabled: ``AWS::EKS::Nodegroup.ForceUpdateEnabled``.
        :param instance_types: ``AWS::EKS::Nodegroup.InstanceTypes``.
        :param labels: ``AWS::EKS::Nodegroup.Labels``.
        :param nodegroup_name: ``AWS::EKS::Nodegroup.NodegroupName``.
        :param release_version: ``AWS::EKS::Nodegroup.ReleaseVersion``.
        :param remote_access: ``AWS::EKS::Nodegroup.RemoteAccess``.
        :param scaling_config: ``AWS::EKS::Nodegroup.ScalingConfig``.
        :param tags: ``AWS::EKS::Nodegroup.Tags``.
        :param version: ``AWS::EKS::Nodegroup.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html
        """
        self._values = {
            "cluster_name": cluster_name,
            "node_role": node_role,
            "subnets": subnets,
        }
        if ami_type is not None:
            self._values["ami_type"] = ami_type
        if disk_size is not None:
            self._values["disk_size"] = disk_size
        if force_update_enabled is not None:
            self._values["force_update_enabled"] = force_update_enabled
        if instance_types is not None:
            self._values["instance_types"] = instance_types
        if labels is not None:
            self._values["labels"] = labels
        if nodegroup_name is not None:
            self._values["nodegroup_name"] = nodegroup_name
        if release_version is not None:
            self._values["release_version"] = release_version
        if remote_access is not None:
            self._values["remote_access"] = remote_access
        if scaling_config is not None:
            self._values["scaling_config"] = scaling_config
        if tags is not None:
            self._values["tags"] = tags
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def cluster_name(self) -> str:
        """``AWS::EKS::Nodegroup.ClusterName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-clustername
        """
        return self._values.get("cluster_name")

    @builtins.property
    def node_role(self) -> str:
        """``AWS::EKS::Nodegroup.NodeRole``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-noderole
        """
        return self._values.get("node_role")

    @builtins.property
    def subnets(self) -> typing.List[str]:
        """``AWS::EKS::Nodegroup.Subnets``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-subnets
        """
        return self._values.get("subnets")

    @builtins.property
    def ami_type(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.AmiType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-amitype
        """
        return self._values.get("ami_type")

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        """``AWS::EKS::Nodegroup.DiskSize``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-disksize
        """
        return self._values.get("disk_size")

    @builtins.property
    def force_update_enabled(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::EKS::Nodegroup.ForceUpdateEnabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-forceupdateenabled
        """
        return self._values.get("force_update_enabled")

    @builtins.property
    def instance_types(self) -> typing.Optional[typing.List[str]]:
        """``AWS::EKS::Nodegroup.InstanceTypes``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-instancetypes
        """
        return self._values.get("instance_types")

    @builtins.property
    def labels(self) -> typing.Any:
        """``AWS::EKS::Nodegroup.Labels``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-labels
        """
        return self._values.get("labels")

    @builtins.property
    def nodegroup_name(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.NodegroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-nodegroupname
        """
        return self._values.get("nodegroup_name")

    @builtins.property
    def release_version(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.ReleaseVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-releaseversion
        """
        return self._values.get("release_version")

    @builtins.property
    def remote_access(
        self,
    ) -> typing.Optional[typing.Union["CfnNodegroup.RemoteAccessProperty", _IResolvable_9ceae33e]]:
        """``AWS::EKS::Nodegroup.RemoteAccess``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-remoteaccess
        """
        return self._values.get("remote_access")

    @builtins.property
    def scaling_config(
        self,
    ) -> typing.Optional[typing.Union["CfnNodegroup.ScalingConfigProperty", _IResolvable_9ceae33e]]:
        """``AWS::EKS::Nodegroup.ScalingConfig``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-scalingconfig
        """
        return self._values.get("scaling_config")

    @builtins.property
    def tags(self) -> typing.Any:
        """``AWS::EKS::Nodegroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-tags
        """
        return self._values.get("tags")

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """``AWS::EKS::Nodegroup.Version``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-eks-nodegroup.html#cfn-eks-nodegroup-version
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNodegroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.ClusterAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_name": "clusterName",
        "cluster_certificate_authority_data": "clusterCertificateAuthorityData",
        "cluster_encryption_config_key_arn": "clusterEncryptionConfigKeyArn",
        "cluster_endpoint": "clusterEndpoint",
        "cluster_security_group_id": "clusterSecurityGroupId",
        "kubectl_environment": "kubectlEnvironment",
        "kubectl_layer": "kubectlLayer",
        "kubectl_private_subnet_ids": "kubectlPrivateSubnetIds",
        "kubectl_role_arn": "kubectlRoleArn",
        "kubectl_security_group_id": "kubectlSecurityGroupId",
        "security_group_ids": "securityGroupIds",
        "vpc": "vpc",
    },
)
class ClusterAttributes:
    def __init__(
        self,
        *,
        cluster_name: str,
        cluster_certificate_authority_data: typing.Optional[str] = None,
        cluster_encryption_config_key_arn: typing.Optional[str] = None,
        cluster_endpoint: typing.Optional[str] = None,
        cluster_security_group_id: typing.Optional[str] = None,
        kubectl_environment: typing.Optional[typing.Mapping[str, str]] = None,
        kubectl_layer: typing.Optional[_ILayerVersion_aa5e0c0c] = None,
        kubectl_private_subnet_ids: typing.Optional[typing.List[str]] = None,
        kubectl_role_arn: typing.Optional[str] = None,
        kubectl_security_group_id: typing.Optional[str] = None,
        security_group_ids: typing.Optional[typing.List[str]] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
    ) -> None:
        """Attributes for EKS clusters.

        :param cluster_name: The physical name of the Cluster.
        :param cluster_certificate_authority_data: The certificate-authority-data for your cluster. Default: - if not specified ``cluster.clusterCertificateAuthorityData`` will throw an error
        :param cluster_encryption_config_key_arn: Amazon Resource Name (ARN) or alias of the customer master key (CMK). Default: - if not specified ``cluster.clusterEncryptionConfigKeyArn`` will throw an error
        :param cluster_endpoint: The API Server endpoint URL. Default: - if not specified ``cluster.clusterEndpoint`` will throw an error.
        :param cluster_security_group_id: The cluster security group that was created by Amazon EKS for the cluster. Default: - if not specified ``cluster.clusterSecurityGroupId`` will throw an error
        :param kubectl_environment: Environment variables to use when running ``kubectl`` against this cluster. Default: - no additional variables
        :param kubectl_layer: An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI. By default, the provider will use the layer included in the "aws-lambda-layer-kubectl" SAR application which is available in all commercial regions. To deploy the layer locally, visit https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md for instructions on how to prepare the .zip file and then define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'kubectl-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`)), compatibleRuntimes: [lambda.Runtime.PROVIDED] }); Or you can use the standard layer like this (with options to customize the version and SAR application ID): ```ts const layer = new eks.KubectlLayer(this, 'KubectlLayer'); Default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.
        :param kubectl_private_subnet_ids: Subnets to host the ``kubectl`` compute resources. If not specified, the k8s endpoint is expected to be accessible publicly. Default: - k8s endpoint is expected to be accessible publicly
        :param kubectl_role_arn: An IAM role with cluster administrator and "system:masters" permissions. Default: - if not specified, it not be possible to issue ``kubectl`` commands against an imported cluster.
        :param kubectl_security_group_id: A security group to use for ``kubectl`` execution. If not specified, the k8s endpoint is expected to be accessible publicly. Default: - k8s endpoint is expected to be accessible publicly
        :param security_group_ids: Additional security groups associated with this cluster. Default: - if not specified, no additional security groups will be considered in ``cluster.connections``.
        :param vpc: The VPC in which this Cluster was created. Default: - if not specified ``cluster.vpc`` will throw an error

        stability
        :stability: experimental
        """
        self._values = {
            "cluster_name": cluster_name,
        }
        if cluster_certificate_authority_data is not None:
            self._values["cluster_certificate_authority_data"] = cluster_certificate_authority_data
        if cluster_encryption_config_key_arn is not None:
            self._values["cluster_encryption_config_key_arn"] = cluster_encryption_config_key_arn
        if cluster_endpoint is not None:
            self._values["cluster_endpoint"] = cluster_endpoint
        if cluster_security_group_id is not None:
            self._values["cluster_security_group_id"] = cluster_security_group_id
        if kubectl_environment is not None:
            self._values["kubectl_environment"] = kubectl_environment
        if kubectl_layer is not None:
            self._values["kubectl_layer"] = kubectl_layer
        if kubectl_private_subnet_ids is not None:
            self._values["kubectl_private_subnet_ids"] = kubectl_private_subnet_ids
        if kubectl_role_arn is not None:
            self._values["kubectl_role_arn"] = kubectl_role_arn
        if kubectl_security_group_id is not None:
            self._values["kubectl_security_group_id"] = kubectl_security_group_id
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def cluster_name(self) -> str:
        """The physical name of the Cluster.

        stability
        :stability: experimental
        """
        return self._values.get("cluster_name")

    @builtins.property
    def cluster_certificate_authority_data(self) -> typing.Optional[str]:
        """The certificate-authority-data for your cluster.

        default
        :default:

        - if not specified ``cluster.clusterCertificateAuthorityData`` will
          throw an error

        stability
        :stability: experimental
        """
        return self._values.get("cluster_certificate_authority_data")

    @builtins.property
    def cluster_encryption_config_key_arn(self) -> typing.Optional[str]:
        """Amazon Resource Name (ARN) or alias of the customer master key (CMK).

        default
        :default:

        - if not specified ``cluster.clusterEncryptionConfigKeyArn`` will
          throw an error

        stability
        :stability: experimental
        """
        return self._values.get("cluster_encryption_config_key_arn")

    @builtins.property
    def cluster_endpoint(self) -> typing.Optional[str]:
        """The API Server endpoint URL.

        default
        :default: - if not specified ``cluster.clusterEndpoint`` will throw an error.

        stability
        :stability: experimental
        """
        return self._values.get("cluster_endpoint")

    @builtins.property
    def cluster_security_group_id(self) -> typing.Optional[str]:
        """The cluster security group that was created by Amazon EKS for the cluster.

        default
        :default:

        - if not specified ``cluster.clusterSecurityGroupId`` will throw an
          error

        stability
        :stability: experimental
        """
        return self._values.get("cluster_security_group_id")

    @builtins.property
    def kubectl_environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Environment variables to use when running ``kubectl`` against this cluster.

        default
        :default: - no additional variables

        stability
        :stability: experimental
        """
        return self._values.get("kubectl_environment")

    @builtins.property
    def kubectl_layer(self) -> typing.Optional[_ILayerVersion_aa5e0c0c]:
        """An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI.

        By default, the provider will use the layer included in the
        "aws-lambda-layer-kubectl" SAR application which is available in all
        commercial regions.

        To deploy the layer locally, visit
        https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md
        for instructions on how to prepare the .zip file and then define it in your
        app as follows::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           layer = lambda_.LayerVersion(self, "kubectl-layer",
               code=lambda_.Code.from_asset(f"{__dirname}/layer.zip")
           )
           compatible_runtimes =

           Oryoucanusethestandardlayerlikeself()with options
           tocustomizetheversionandSARapplicationID

           ```ts
           const layer = new eks.KubectlLayer(this, 'KubectlLayer');

        default
        :default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.

        see
        :see: https://github.com/aws-samples/aws-lambda-layer-kubectl
        stability
        :stability: experimental
        """
        return self._values.get("kubectl_layer")

    @builtins.property
    def kubectl_private_subnet_ids(self) -> typing.Optional[typing.List[str]]:
        """Subnets to host the ``kubectl`` compute resources.

        If not specified, the k8s
        endpoint is expected to be accessible publicly.

        default
        :default: - k8s endpoint is expected to be accessible publicly

        stability
        :stability: experimental
        """
        return self._values.get("kubectl_private_subnet_ids")

    @builtins.property
    def kubectl_role_arn(self) -> typing.Optional[str]:
        """An IAM role with cluster administrator and "system:masters" permissions.

        default
        :default:

        - if not specified, it not be possible to issue ``kubectl`` commands
          against an imported cluster.

        stability
        :stability: experimental
        """
        return self._values.get("kubectl_role_arn")

    @builtins.property
    def kubectl_security_group_id(self) -> typing.Optional[str]:
        """A security group to use for ``kubectl`` execution.

        If not specified, the k8s
        endpoint is expected to be accessible publicly.

        default
        :default: - k8s endpoint is expected to be accessible publicly

        stability
        :stability: experimental
        """
        return self._values.get("kubectl_security_group_id")

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """Additional security groups associated with this cluster.

        default
        :default:

        - if not specified, no additional security groups will be
          considered in ``cluster.connections``.

        stability
        :stability: experimental
        """
        return self._values.get("security_group_ids")

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC in which this Cluster was created.

        default
        :default: - if not specified ``cluster.vpc`` will throw an error

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.CommonClusterOptions",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "cluster_name": "clusterName",
        "output_cluster_name": "outputClusterName",
        "output_config_command": "outputConfigCommand",
        "role": "role",
        "security_group": "securityGroup",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
    },
)
class CommonClusterOptions:
    def __init__(
        self,
        *,
        version: "KubernetesVersion",
        cluster_name: typing.Optional[str] = None,
        output_cluster_name: typing.Optional[bool] = None,
        output_config_command: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_group: typing.Optional[_ISecurityGroup_d72ab8e8] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
        vpc_subnets: typing.Optional[typing.List[_SubnetSelection_36a13cd6]] = None,
    ) -> None:
        """Options for configuring an EKS cluster.

        :param version: The Kubernetes version to run in the cluster.
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if output_cluster_name is not None:
            self._values["output_cluster_name"] = output_cluster_name
        if output_config_command is not None:
            self._values["output_config_command"] = output_config_command
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def version(self) -> "KubernetesVersion":
        """The Kubernetes version to run in the cluster.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """Name for the cluster.

        default
        :default: - Automatically generated name

        stability
        :stability: experimental
        """
        return self._values.get("cluster_name")

    @builtins.property
    def output_cluster_name(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the name of the cluster will be synthesized.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("output_cluster_name")

    @builtins.property
    def output_config_command(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized.

        This command will include
        the cluster name and, if applicable, the ARN of the masters IAM role.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("output_config_command")

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get("role")

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """Security Group to use for Control Plane ENIs.

        default
        :default: - A security group is automatically created

        stability
        :stability: experimental
        """
        return self._values.get("security_group")

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC in which to create the Cluster.

        default
        :default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[typing.List[_SubnetSelection_36a13cd6]]:
        """Where to place EKS Control Plane ENIs.

        If you want to create public load balancers, this must include public subnets.

        For example, to only select private subnets, supply the following::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           vpcSubnets: [
              { subnetType: ec2.SubnetType.Private }
           ]

        default
        :default: - All public and private subnets

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonClusterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.aws_eks.CoreDnsComputeType")
class CoreDnsComputeType(enum.Enum):
    """The type of compute resources to use for CoreDNS.

    stability
    :stability: experimental
    """

    EC2 = "EC2"
    """Deploy CoreDNS on EC2 instances.

    stability
    :stability: experimental
    """
    FARGATE = "FARGATE"
    """Deploy CoreDNS on Fargate-managed instances.

    stability
    :stability: experimental
    """


@jsii.enum(jsii_type="monocdk-experiment.aws_eks.DefaultCapacityType")
class DefaultCapacityType(enum.Enum):
    """The default capacity type for the cluster.

    stability
    :stability: experimental
    """

    NODEGROUP = "NODEGROUP"
    """managed node group.

    stability
    :stability: experimental
    """
    EC2 = "EC2"
    """EC2 autoscaling group.

    stability
    :stability: experimental
    """


@jsii.implements(_IMachineImage_d5cd7b45)
class EksOptimizedImage(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eks.EksOptimizedImage"
):
    """Construct an Amazon Linux 2 image from the latest EKS Optimized AMI published in SSM.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        *,
        kubernetes_version: typing.Optional[str] = None,
        node_type: typing.Optional["NodeType"] = None,
    ) -> None:
        """Constructs a new instance of the EcsOptimizedAmi class.

        :param kubernetes_version: The Kubernetes version to use. Default: - The latest version
        :param node_type: What instance type to retrieve the image for (standard or GPU-optimized). Default: NodeType.STANDARD

        stability
        :stability: experimental
        """
        props = EksOptimizedImageProps(
            kubernetes_version=kubernetes_version, node_type=node_type
        )

        jsii.create(EksOptimizedImage, self, [props])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: _Construct_f50a3f53) -> _MachineImageConfig_815fc1b9:
        """Return the correct image.

        :param scope: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getImage", [scope])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.EksOptimizedImageProps",
    jsii_struct_bases=[],
    name_mapping={"kubernetes_version": "kubernetesVersion", "node_type": "nodeType"},
)
class EksOptimizedImageProps:
    def __init__(
        self,
        *,
        kubernetes_version: typing.Optional[str] = None,
        node_type: typing.Optional["NodeType"] = None,
    ) -> None:
        """Properties for EksOptimizedImage.

        :param kubernetes_version: The Kubernetes version to use. Default: - The latest version
        :param node_type: What instance type to retrieve the image for (standard or GPU-optimized). Default: NodeType.STANDARD

        stability
        :stability: experimental
        """
        self._values = {}
        if kubernetes_version is not None:
            self._values["kubernetes_version"] = kubernetes_version
        if node_type is not None:
            self._values["node_type"] = node_type

    @builtins.property
    def kubernetes_version(self) -> typing.Optional[str]:
        """The Kubernetes version to use.

        default
        :default: - The latest version

        stability
        :stability: experimental
        """
        return self._values.get("kubernetes_version")

    @builtins.property
    def node_type(self) -> typing.Optional["NodeType"]:
        """What instance type to retrieve the image for (standard or GPU-optimized).

        default
        :default: NodeType.STANDARD

        stability
        :stability: experimental
        """
        return self._values.get("node_type")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EksOptimizedImageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EndpointAccess(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eks.EndpointAccess"
):
    """Endpoint access characteristics.

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="onlyFrom")
    def only_from(self, *cidr: str) -> "EndpointAccess":
        """Restrict public access to specific CIDR blocks.

        If public access is disabled, this method will result in an error.

        :param cidr: CIDR blocks.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "onlyFrom", [*cidr])

    @jsii.python.classproperty
    @jsii.member(jsii_name="PRIVATE")
    def PRIVATE(cls) -> "EndpointAccess":
        """The cluster endpoint is only accessible through your VPC.

        Worker node traffic to the endpoint will stay within your VPC.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PRIVATE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PUBLIC")
    def PUBLIC(cls) -> "EndpointAccess":
        """The cluster endpoint is accessible from outside of your VPC.

        Worker node traffic will leave your VPC to connect to the endpoint.

        By default, the endpoint is exposed to all adresses. You can optionally limit the CIDR blocks that can access the public endpoint using the ``PUBLIC.onlyFrom`` method.
        If you limit access to specific CIDR blocks, you must ensure that the CIDR blocks that you
        specify include the addresses that worker nodes and Fargate pods (if you use them)
        access the public endpoint from.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PUBLIC")

    @jsii.python.classproperty
    @jsii.member(jsii_name="PUBLIC_AND_PRIVATE")
    def PUBLIC_AND_PRIVATE(cls) -> "EndpointAccess":
        """The cluster endpoint is accessible from outside of your VPC.

        Worker node traffic to the endpoint will stay within your VPC.

        By default, the endpoint is exposed to all adresses. You can optionally limit the CIDR blocks that can access the public endpoint using the ``PUBLIC_AND_PRIVATE.onlyFrom`` method.
        If you limit access to specific CIDR blocks, you must ensure that the CIDR blocks that you
        specify include the addresses that worker nodes and Fargate pods (if you use them)
        access the public endpoint from.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "PUBLIC_AND_PRIVATE")


@jsii.implements(_ITaggable_6ea67ae1)
class FargateProfile(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.FargateProfile",
):
    """Fargate profiles allows an administrator to declare which pods run on Fargate.

    This declaration is done through the profile’s selectors. Each
    profile can have up to five selectors that contain a namespace and optional
    labels. You must define a namespace for every selector. The label field
    consists of multiple optional key-value pairs. Pods that match a selector (by
    matching a namespace for the selector and all of the labels specified in the
    selector) are scheduled on Fargate. If a namespace selector is defined
    without any labels, Amazon EKS will attempt to schedule all pods that run in
    that namespace onto Fargate using the profile. If a to-be-scheduled pod
    matches any of the selectors in the Fargate profile, then that pod is
    scheduled on Fargate.

    If a pod matches multiple Fargate profiles, Amazon EKS picks one of the
    matches at random. In this case, you can specify which profile a pod should
    use by adding the following Kubernetes label to the pod specification:
    eks.amazonaws.com/fargate-profile: profile_name. However, the pod must still
    match a selector in that profile in order to be scheduled onto Fargate.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cluster: "Cluster",
        selectors: typing.List["Selector"],
        fargate_profile_name: typing.Optional[str] = None,
        pod_execution_role: typing.Optional[_IRole_e69bbae4] = None,
        subnet_selection: typing.Optional[_SubnetSelection_36a13cd6] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The EKS cluster to apply the Fargate profile to. [disable-awslint:ref-via-interface]
        :param selectors: The selectors to match for pods to use this Fargate profile. Each selector must have an associated namespace. Optionally, you can also specify labels for a namespace. At least one selector is required and you may specify up to five selectors.
        :param fargate_profile_name: The name of the Fargate profile. Default: - generated
        :param pod_execution_role: The pod execution role to use for pods that match the selectors in the Fargate profile. The pod execution role allows Fargate infrastructure to register with your cluster as a node, and it provides read access to Amazon ECR image repositories. Default: - a role will be automatically created
        :param subnet_selection: Select which subnets to launch your pods into. At this time, pods running on Fargate are not assigned public IP addresses, so only private subnets (with no direct route to an Internet Gateway) are allowed. Default: - all private subnets of the VPC are selected.
        :param vpc: The VPC from which to select subnets to launch your pods into. By default, all private subnets are selected. You can customize this using ``subnetSelection``. Default: - all private subnets used by theEKS cluster

        stability
        :stability: experimental
        """
        props = FargateProfileProps(
            cluster=cluster,
            selectors=selectors,
            fargate_profile_name=fargate_profile_name,
            pod_execution_role=pod_execution_role,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(FargateProfile, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="fargateProfileArn")
    def fargate_profile_arn(self) -> str:
        """The full Amazon Resource Name (ARN) of the Fargate profile.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "fargateProfileArn")

    @builtins.property
    @jsii.member(jsii_name="fargateProfileName")
    def fargate_profile_name(self) -> str:
        """The name of the Fargate profile.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "fargateProfileName")

    @builtins.property
    @jsii.member(jsii_name="podExecutionRole")
    def pod_execution_role(self) -> _IRole_e69bbae4:
        """The pod execution role to use for pods that match the selectors in the Fargate profile.

        The pod execution role allows Fargate infrastructure to
        register with your cluster as a node, and it provides read access to Amazon
        ECR image repositories.

        stability
        :stability: experimental
        """
        return jsii.get(self, "podExecutionRole")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """Resource tags.

        stability
        :stability: experimental
        """
        return jsii.get(self, "tags")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.FargateProfileOptions",
    jsii_struct_bases=[],
    name_mapping={
        "selectors": "selectors",
        "fargate_profile_name": "fargateProfileName",
        "pod_execution_role": "podExecutionRole",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class FargateProfileOptions:
    def __init__(
        self,
        *,
        selectors: typing.List["Selector"],
        fargate_profile_name: typing.Optional[str] = None,
        pod_execution_role: typing.Optional[_IRole_e69bbae4] = None,
        subnet_selection: typing.Optional[_SubnetSelection_36a13cd6] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
    ) -> None:
        """Options for defining EKS Fargate Profiles.

        :param selectors: The selectors to match for pods to use this Fargate profile. Each selector must have an associated namespace. Optionally, you can also specify labels for a namespace. At least one selector is required and you may specify up to five selectors.
        :param fargate_profile_name: The name of the Fargate profile. Default: - generated
        :param pod_execution_role: The pod execution role to use for pods that match the selectors in the Fargate profile. The pod execution role allows Fargate infrastructure to register with your cluster as a node, and it provides read access to Amazon ECR image repositories. Default: - a role will be automatically created
        :param subnet_selection: Select which subnets to launch your pods into. At this time, pods running on Fargate are not assigned public IP addresses, so only private subnets (with no direct route to an Internet Gateway) are allowed. Default: - all private subnets of the VPC are selected.
        :param vpc: The VPC from which to select subnets to launch your pods into. By default, all private subnets are selected. You can customize this using ``subnetSelection``. Default: - all private subnets used by theEKS cluster

        stability
        :stability: experimental
        """
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_36a13cd6(**subnet_selection)
        self._values = {
            "selectors": selectors,
        }
        if fargate_profile_name is not None:
            self._values["fargate_profile_name"] = fargate_profile_name
        if pod_execution_role is not None:
            self._values["pod_execution_role"] = pod_execution_role
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def selectors(self) -> typing.List["Selector"]:
        """The selectors to match for pods to use this Fargate profile.

        Each selector
        must have an associated namespace. Optionally, you can also specify labels
        for a namespace.

        At least one selector is required and you may specify up to five selectors.

        stability
        :stability: experimental
        """
        return self._values.get("selectors")

    @builtins.property
    def fargate_profile_name(self) -> typing.Optional[str]:
        """The name of the Fargate profile.

        default
        :default: - generated

        stability
        :stability: experimental
        """
        return self._values.get("fargate_profile_name")

    @builtins.property
    def pod_execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The pod execution role to use for pods that match the selectors in the Fargate profile.

        The pod execution role allows Fargate infrastructure to
        register with your cluster as a node, and it provides read access to Amazon
        ECR image repositories.

        default
        :default: - a role will be automatically created

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/pod-execution-role.html
        stability
        :stability: experimental
        """
        return self._values.get("pod_execution_role")

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Select which subnets to launch your pods into.

        At this time, pods running
        on Fargate are not assigned public IP addresses, so only private subnets
        (with no direct route to an Internet Gateway) are allowed.

        default
        :default: - all private subnets of the VPC are selected.

        stability
        :stability: experimental
        """
        return self._values.get("subnet_selection")

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC from which to select subnets to launch your pods into.

        By default, all private subnets are selected. You can customize this using
        ``subnetSelection``.

        default
        :default: - all private subnets used by theEKS cluster

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateProfileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.FargateProfileProps",
    jsii_struct_bases=[FargateProfileOptions],
    name_mapping={
        "selectors": "selectors",
        "fargate_profile_name": "fargateProfileName",
        "pod_execution_role": "podExecutionRole",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "cluster": "cluster",
    },
)
class FargateProfileProps(FargateProfileOptions):
    def __init__(
        self,
        *,
        selectors: typing.List["Selector"],
        fargate_profile_name: typing.Optional[str] = None,
        pod_execution_role: typing.Optional[_IRole_e69bbae4] = None,
        subnet_selection: typing.Optional[_SubnetSelection_36a13cd6] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
        cluster: "Cluster",
    ) -> None:
        """Configuration props for EKS Fargate Profiles.

        :param selectors: The selectors to match for pods to use this Fargate profile. Each selector must have an associated namespace. Optionally, you can also specify labels for a namespace. At least one selector is required and you may specify up to five selectors.
        :param fargate_profile_name: The name of the Fargate profile. Default: - generated
        :param pod_execution_role: The pod execution role to use for pods that match the selectors in the Fargate profile. The pod execution role allows Fargate infrastructure to register with your cluster as a node, and it provides read access to Amazon ECR image repositories. Default: - a role will be automatically created
        :param subnet_selection: Select which subnets to launch your pods into. At this time, pods running on Fargate are not assigned public IP addresses, so only private subnets (with no direct route to an Internet Gateway) are allowed. Default: - all private subnets of the VPC are selected.
        :param vpc: The VPC from which to select subnets to launch your pods into. By default, all private subnets are selected. You can customize this using ``subnetSelection``. Default: - all private subnets used by theEKS cluster
        :param cluster: The EKS cluster to apply the Fargate profile to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_36a13cd6(**subnet_selection)
        self._values = {
            "selectors": selectors,
            "cluster": cluster,
        }
        if fargate_profile_name is not None:
            self._values["fargate_profile_name"] = fargate_profile_name
        if pod_execution_role is not None:
            self._values["pod_execution_role"] = pod_execution_role
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def selectors(self) -> typing.List["Selector"]:
        """The selectors to match for pods to use this Fargate profile.

        Each selector
        must have an associated namespace. Optionally, you can also specify labels
        for a namespace.

        At least one selector is required and you may specify up to five selectors.

        stability
        :stability: experimental
        """
        return self._values.get("selectors")

    @builtins.property
    def fargate_profile_name(self) -> typing.Optional[str]:
        """The name of the Fargate profile.

        default
        :default: - generated

        stability
        :stability: experimental
        """
        return self._values.get("fargate_profile_name")

    @builtins.property
    def pod_execution_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The pod execution role to use for pods that match the selectors in the Fargate profile.

        The pod execution role allows Fargate infrastructure to
        register with your cluster as a node, and it provides read access to Amazon
        ECR image repositories.

        default
        :default: - a role will be automatically created

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/pod-execution-role.html
        stability
        :stability: experimental
        """
        return self._values.get("pod_execution_role")

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Select which subnets to launch your pods into.

        At this time, pods running
        on Fargate are not assigned public IP addresses, so only private subnets
        (with no direct route to an Internet Gateway) are allowed.

        default
        :default: - all private subnets of the VPC are selected.

        stability
        :stability: experimental
        """
        return self._values.get("subnet_selection")

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC from which to select subnets to launch your pods into.

        By default, all private subnets are selected. You can customize this using
        ``subnetSelection``.

        default
        :default: - all private subnets used by theEKS cluster

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def cluster(self) -> "Cluster":
        """The EKS cluster to apply the Fargate profile to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get("cluster")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HelmChart(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.HelmChart",
):
    """Represents a helm chart within the Kubernetes system.

    Applies/deletes the resources using ``kubectl`` in sync with the resource.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cluster: "ICluster",
        chart: str,
        create_namespace: typing.Optional[bool] = None,
        namespace: typing.Optional[str] = None,
        release: typing.Optional[str] = None,
        repository: typing.Optional[str] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        values: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        version: typing.Optional[str] = None,
        wait: typing.Optional[bool] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]
        :param chart: The name of the chart.
        :param create_namespace: create namespace if not exist. Default: true
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 53 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Default: Duration.minutes(5)
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. Default: - Helm will not wait before marking release as successful

        stability
        :stability: experimental
        """
        props = HelmChartProps(
            cluster=cluster,
            chart=chart,
            create_namespace=create_namespace,
            namespace=namespace,
            release=release,
            repository=repository,
            timeout=timeout,
            values=values,
            version=version,
            wait=wait,
        )

        jsii.create(HelmChart, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="RESOURCE_TYPE")
    def RESOURCE_TYPE(cls) -> str:
        """The CloudFormation resource type.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "RESOURCE_TYPE")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.HelmChartOptions",
    jsii_struct_bases=[],
    name_mapping={
        "chart": "chart",
        "create_namespace": "createNamespace",
        "namespace": "namespace",
        "release": "release",
        "repository": "repository",
        "timeout": "timeout",
        "values": "values",
        "version": "version",
        "wait": "wait",
    },
)
class HelmChartOptions:
    def __init__(
        self,
        *,
        chart: str,
        create_namespace: typing.Optional[bool] = None,
        namespace: typing.Optional[str] = None,
        release: typing.Optional[str] = None,
        repository: typing.Optional[str] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        values: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        version: typing.Optional[str] = None,
        wait: typing.Optional[bool] = None,
    ) -> None:
        """Helm Chart options.

        :param chart: The name of the chart.
        :param create_namespace: create namespace if not exist. Default: true
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 53 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Default: Duration.minutes(5)
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. Default: - Helm will not wait before marking release as successful

        stability
        :stability: experimental
        """
        self._values = {
            "chart": chart,
        }
        if create_namespace is not None:
            self._values["create_namespace"] = create_namespace
        if namespace is not None:
            self._values["namespace"] = namespace
        if release is not None:
            self._values["release"] = release
        if repository is not None:
            self._values["repository"] = repository
        if timeout is not None:
            self._values["timeout"] = timeout
        if values is not None:
            self._values["values"] = values
        if version is not None:
            self._values["version"] = version
        if wait is not None:
            self._values["wait"] = wait

    @builtins.property
    def chart(self) -> str:
        """The name of the chart.

        stability
        :stability: experimental
        """
        return self._values.get("chart")

    @builtins.property
    def create_namespace(self) -> typing.Optional[bool]:
        """create namespace if not exist.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("create_namespace")

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """The Kubernetes namespace scope of the requests.

        default
        :default: default

        stability
        :stability: experimental
        """
        return self._values.get("namespace")

    @builtins.property
    def release(self) -> typing.Optional[str]:
        """The name of the release.

        default
        :default: - If no release name is given, it will use the last 53 characters of the node's unique id.

        stability
        :stability: experimental
        """
        return self._values.get("release")

    @builtins.property
    def repository(self) -> typing.Optional[str]:
        """The repository which contains the chart.

        For example: https://kubernetes-charts.storage.googleapis.com/

        default
        :default: - No repository will be used, which means that the chart needs to be an absolute URL.

        stability
        :stability: experimental
        """
        return self._values.get("repository")

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Amount of time to wait for any individual Kubernetes operation.

        Maximum 15 minutes.

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get("timeout")

    @builtins.property
    def values(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """The values to be used by the chart.

        default
        :default: - No values are provided to the chart.

        stability
        :stability: experimental
        """
        return self._values.get("values")

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The chart version to install.

        default
        :default: - If this is not specified, the latest version is installed

        stability
        :stability: experimental
        """
        return self._values.get("version")

    @builtins.property
    def wait(self) -> typing.Optional[bool]:
        """Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful.

        default
        :default: - Helm will not wait before marking release as successful

        stability
        :stability: experimental
        """
        return self._values.get("wait")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HelmChartOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.HelmChartProps",
    jsii_struct_bases=[HelmChartOptions],
    name_mapping={
        "chart": "chart",
        "create_namespace": "createNamespace",
        "namespace": "namespace",
        "release": "release",
        "repository": "repository",
        "timeout": "timeout",
        "values": "values",
        "version": "version",
        "wait": "wait",
        "cluster": "cluster",
    },
)
class HelmChartProps(HelmChartOptions):
    def __init__(
        self,
        *,
        chart: str,
        create_namespace: typing.Optional[bool] = None,
        namespace: typing.Optional[str] = None,
        release: typing.Optional[str] = None,
        repository: typing.Optional[str] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        values: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        version: typing.Optional[str] = None,
        wait: typing.Optional[bool] = None,
        cluster: "ICluster",
    ) -> None:
        """Helm Chart properties.

        :param chart: The name of the chart.
        :param create_namespace: create namespace if not exist. Default: true
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 53 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Default: Duration.minutes(5)
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. Default: - Helm will not wait before marking release as successful
        :param cluster: The EKS cluster to apply this configuration to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        self._values = {
            "chart": chart,
            "cluster": cluster,
        }
        if create_namespace is not None:
            self._values["create_namespace"] = create_namespace
        if namespace is not None:
            self._values["namespace"] = namespace
        if release is not None:
            self._values["release"] = release
        if repository is not None:
            self._values["repository"] = repository
        if timeout is not None:
            self._values["timeout"] = timeout
        if values is not None:
            self._values["values"] = values
        if version is not None:
            self._values["version"] = version
        if wait is not None:
            self._values["wait"] = wait

    @builtins.property
    def chart(self) -> str:
        """The name of the chart.

        stability
        :stability: experimental
        """
        return self._values.get("chart")

    @builtins.property
    def create_namespace(self) -> typing.Optional[bool]:
        """create namespace if not exist.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("create_namespace")

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """The Kubernetes namespace scope of the requests.

        default
        :default: default

        stability
        :stability: experimental
        """
        return self._values.get("namespace")

    @builtins.property
    def release(self) -> typing.Optional[str]:
        """The name of the release.

        default
        :default: - If no release name is given, it will use the last 53 characters of the node's unique id.

        stability
        :stability: experimental
        """
        return self._values.get("release")

    @builtins.property
    def repository(self) -> typing.Optional[str]:
        """The repository which contains the chart.

        For example: https://kubernetes-charts.storage.googleapis.com/

        default
        :default: - No repository will be used, which means that the chart needs to be an absolute URL.

        stability
        :stability: experimental
        """
        return self._values.get("repository")

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Amount of time to wait for any individual Kubernetes operation.

        Maximum 15 minutes.

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get("timeout")

    @builtins.property
    def values(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """The values to be used by the chart.

        default
        :default: - No values are provided to the chart.

        stability
        :stability: experimental
        """
        return self._values.get("values")

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The chart version to install.

        default
        :default: - If this is not specified, the latest version is installed

        stability
        :stability: experimental
        """
        return self._values.get("version")

    @builtins.property
    def wait(self) -> typing.Optional[bool]:
        """Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful.

        default
        :default: - Helm will not wait before marking release as successful

        stability
        :stability: experimental
        """
        return self._values.get("wait")

    @builtins.property
    def cluster(self) -> "ICluster":
        """The EKS cluster to apply this configuration to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get("cluster")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HelmChartProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk-experiment.aws_eks.ICluster")
class ICluster(_IResource_72f7ee7e, _IConnectable_a587039f, jsii.compat.Protocol):
    """An EKS cluster.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IClusterProxy

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The unique ARN assigned to the service by AWS in the form of arn:aws:eks:.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        """The certificate-authority-data for your cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterEncryptionConfigKeyArn")
    def cluster_encryption_config_key_arn(self) -> str:
        """Amazon Resource Name (ARN) or alias of the customer master key (CMK).

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        """The API Server endpoint URL.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The physical name of the Cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterSecurityGroupId")
    def cluster_security_group_id(self) -> str:
        """The cluster security group that was created by Amazon EKS for the cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="kubectlEnvironment")
    def kubectl_environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Custom environment variables when running ``kubectl`` against this cluster.

        default
        :default: - no additional environment variables

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="kubectlLayer")
    def kubectl_layer(self) -> typing.Optional[_ILayerVersion_aa5e0c0c]:
        """An AWS Lambda layer that includes ``kubectl``, ``helm`` and the ``aws`` CLI.

        If not defined, a default layer will be used.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="kubectlPrivateSubnets")
    def kubectl_private_subnets(
        self,
    ) -> typing.Optional[typing.List[_ISubnet_7f5367e6]]:
        """Subnets to host the ``kubectl`` compute resources.

        default
        :default:

        - If not specified, the k8s endpoint is expected to be accessible
          publicly.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="kubectlRole")
    def kubectl_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """An IAM role that can perform kubectl operations against this cluster.

        The role should be mapped to the ``system:masters`` Kubernetes RBAC role.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="kubectlSecurityGroup")
    def kubectl_security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """A security group to use for ``kubectl`` execution.

        default
        :default:

        - If not specified, the k8s endpoint is expected to be accessible
          publicly.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addChart")
    def add_chart(
        self,
        id: str,
        *,
        chart: str,
        create_namespace: typing.Optional[bool] = None,
        namespace: typing.Optional[str] = None,
        release: typing.Optional[str] = None,
        repository: typing.Optional[str] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        values: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        version: typing.Optional[str] = None,
        wait: typing.Optional[bool] = None,
    ) -> "HelmChart":
        """Defines a Helm chart in this cluster.

        :param id: logical id of this chart.
        :param chart: The name of the chart.
        :param create_namespace: create namespace if not exist. Default: true
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 53 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Default: Duration.minutes(5)
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. Default: - Helm will not wait before marking release as successful

        return
        :return: a ``HelmChart`` construct

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addManifest")
    def add_manifest(self, id: str, *manifest: typing.Any) -> "KubernetesManifest":
        """Defines a Kubernetes resource in this cluster.

        The manifest will be applied/deleted using kubectl as needed.

        :param id: logical id of this manifest.
        :param manifest: a list of Kubernetes resource specifications.

        return
        :return: a ``KubernetesManifest`` object.

        stability
        :stability: experimental
        """
        ...


class _IClusterProxy(
    jsii.proxy_for(_IResource_72f7ee7e), jsii.proxy_for(_IConnectable_a587039f)
):
    """An EKS cluster.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_eks.ICluster"

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The unique ARN assigned to the service by AWS in the form of arn:aws:eks:.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterArn")

    @builtins.property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        """The certificate-authority-data for your cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterCertificateAuthorityData")

    @builtins.property
    @jsii.member(jsii_name="clusterEncryptionConfigKeyArn")
    def cluster_encryption_config_key_arn(self) -> str:
        """Amazon Resource Name (ARN) or alias of the customer master key (CMK).

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterEncryptionConfigKeyArn")

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        """The API Server endpoint URL.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The physical name of the Cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterName")

    @builtins.property
    @jsii.member(jsii_name="clusterSecurityGroupId")
    def cluster_security_group_id(self) -> str:
        """The cluster security group that was created by Amazon EKS for the cluster.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterSecurityGroupId")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")

    @builtins.property
    @jsii.member(jsii_name="kubectlEnvironment")
    def kubectl_environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Custom environment variables when running ``kubectl`` against this cluster.

        default
        :default: - no additional environment variables

        stability
        :stability: experimental
        """
        return jsii.get(self, "kubectlEnvironment")

    @builtins.property
    @jsii.member(jsii_name="kubectlLayer")
    def kubectl_layer(self) -> typing.Optional[_ILayerVersion_aa5e0c0c]:
        """An AWS Lambda layer that includes ``kubectl``, ``helm`` and the ``aws`` CLI.

        If not defined, a default layer will be used.

        stability
        :stability: experimental
        """
        return jsii.get(self, "kubectlLayer")

    @builtins.property
    @jsii.member(jsii_name="kubectlPrivateSubnets")
    def kubectl_private_subnets(
        self,
    ) -> typing.Optional[typing.List[_ISubnet_7f5367e6]]:
        """Subnets to host the ``kubectl`` compute resources.

        default
        :default:

        - If not specified, the k8s endpoint is expected to be accessible
          publicly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "kubectlPrivateSubnets")

    @builtins.property
    @jsii.member(jsii_name="kubectlRole")
    def kubectl_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """An IAM role that can perform kubectl operations against this cluster.

        The role should be mapped to the ``system:masters`` Kubernetes RBAC role.

        stability
        :stability: experimental
        """
        return jsii.get(self, "kubectlRole")

    @builtins.property
    @jsii.member(jsii_name="kubectlSecurityGroup")
    def kubectl_security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """A security group to use for ``kubectl`` execution.

        default
        :default:

        - If not specified, the k8s endpoint is expected to be accessible
          publicly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "kubectlSecurityGroup")

    @jsii.member(jsii_name="addChart")
    def add_chart(
        self,
        id: str,
        *,
        chart: str,
        create_namespace: typing.Optional[bool] = None,
        namespace: typing.Optional[str] = None,
        release: typing.Optional[str] = None,
        repository: typing.Optional[str] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        values: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        version: typing.Optional[str] = None,
        wait: typing.Optional[bool] = None,
    ) -> "HelmChart":
        """Defines a Helm chart in this cluster.

        :param id: logical id of this chart.
        :param chart: The name of the chart.
        :param create_namespace: create namespace if not exist. Default: true
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 53 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Default: Duration.minutes(5)
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. Default: - Helm will not wait before marking release as successful

        return
        :return: a ``HelmChart`` construct

        stability
        :stability: experimental
        """
        options = HelmChartOptions(
            chart=chart,
            create_namespace=create_namespace,
            namespace=namespace,
            release=release,
            repository=repository,
            timeout=timeout,
            values=values,
            version=version,
            wait=wait,
        )

        return jsii.invoke(self, "addChart", [id, options])

    @jsii.member(jsii_name="addManifest")
    def add_manifest(self, id: str, *manifest: typing.Any) -> "KubernetesManifest":
        """Defines a Kubernetes resource in this cluster.

        The manifest will be applied/deleted using kubectl as needed.

        :param id: logical id of this manifest.
        :param manifest: a list of Kubernetes resource specifications.

        return
        :return: a ``KubernetesManifest`` object.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addManifest", [id, *manifest])


@jsii.interface(jsii_type="monocdk-experiment.aws_eks.INodegroup")
class INodegroup(_IResource_72f7ee7e, jsii.compat.Protocol):
    """NodeGroup interface.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INodegroupProxy

    @builtins.property
    @jsii.member(jsii_name="nodegroupName")
    def nodegroup_name(self) -> str:
        """Name of the nodegroup.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _INodegroupProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """NodeGroup interface.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_eks.INodegroup"

    @builtins.property
    @jsii.member(jsii_name="nodegroupName")
    def nodegroup_name(self) -> str:
        """Name of the nodegroup.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "nodegroupName")


@jsii.implements(_ILayerVersion_aa5e0c0c)
class KubectlLayer(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.KubectlLayer",
):
    """An AWS Lambda layer that includes kubectl and the AWS CLI.

    see
    :see: https://github.com/aws-samples/aws-lambda-layer-kubectl
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        application_id: typing.Optional[str] = None,
        version: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param application_id: The Serverless Application Repository application ID which contains the kubectl layer. Default: - The ARN for the ``lambda-layer-kubectl`` SAR app.
        :param version: The semantic version of the kubectl AWS Lambda Layer SAR app to use. Default: '2.0.0'

        stability
        :stability: experimental
        """
        props = KubectlLayerProps(application_id=application_id, version=version)

        jsii.create(KubectlLayer, self, [scope, id, props])

    @jsii.member(jsii_name="addPermission")
    def add_permission(
        self,
        _id: str,
        *,
        account_id: str,
        organization_id: typing.Optional[str] = None,
    ) -> None:
        """Add permission for this layer version to specific entities.

        Usage within
        the same account where the layer is defined is always allowed and does not
        require calling this method. Note that the principal that creates the
        Lambda function using the layer (for example, a CloudFormation changeset
        execution role) also needs to have the ``lambda:GetLayerVersion``
        permission on the layer version.

        :param _id: -
        :param account_id: The AWS Account id of the account that is authorized to use a Lambda Layer Version. The wild-card ``'*'`` can be used to grant access to "any" account (or any account in an organization when ``organizationId`` is specified).
        :param organization_id: The ID of the AWS Organization to hwich the grant is restricted. Can only be specified if ``accountId`` is ``'*'``

        stability
        :stability: experimental
        """
        _permission = _LayerVersionPermission_b7d4b3d2(
            account_id=account_id, organization_id=organization_id
        )

        return jsii.invoke(self, "addPermission", [_id, _permission])

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> _ResourceEnvironment_5b040075:
        """The environment this resource belongs to.

        For resources that are created and managed by the CDK
        (generally, those created by creating new class instances like Role, Bucket, etc.),
        this is always the same as the environment of the stack they belong to;
        however, for imported resources
        (those obtained from static methods like fromRoleArn, fromBucketName, etc.),
        that might be different than the stack they were imported into.

        stability
        :stability: experimental
        """
        return jsii.get(self, "env")

    @builtins.property
    @jsii.member(jsii_name="layerVersionArn")
    def layer_version_arn(self) -> str:
        """The ARN of the AWS Lambda layer version.

        stability
        :stability: experimental
        """
        return jsii.get(self, "layerVersionArn")

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> _Stack_05f4505a:
        """The stack in which this resource is defined.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stack")

    @builtins.property
    @jsii.member(jsii_name="compatibleRuntimes")
    def compatible_runtimes(self) -> typing.Optional[typing.List[_Runtime_8b970b80]]:
        """All runtimes are compatible.

        stability
        :stability: experimental
        """
        return jsii.get(self, "compatibleRuntimes")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.KubectlLayerProps",
    jsii_struct_bases=[],
    name_mapping={"application_id": "applicationId", "version": "version"},
)
class KubectlLayerProps:
    def __init__(
        self,
        *,
        application_id: typing.Optional[str] = None,
        version: typing.Optional[str] = None,
    ) -> None:
        """Properties for KubectlLayer.

        :param application_id: The Serverless Application Repository application ID which contains the kubectl layer. Default: - The ARN for the ``lambda-layer-kubectl`` SAR app.
        :param version: The semantic version of the kubectl AWS Lambda Layer SAR app to use. Default: '2.0.0'

        stability
        :stability: experimental
        """
        self._values = {}
        if application_id is not None:
            self._values["application_id"] = application_id
        if version is not None:
            self._values["version"] = version

    @builtins.property
    def application_id(self) -> typing.Optional[str]:
        """The Serverless Application Repository application ID which contains the kubectl layer.

        default
        :default: - The ARN for the ``lambda-layer-kubectl`` SAR app.

        see
        :see: https://github.com/aws-samples/aws-lambda-layer-kubectl
        stability
        :stability: experimental
        """
        return self._values.get("application_id")

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The semantic version of the kubectl AWS Lambda Layer SAR app to use.

        default
        :default: '2.0.0'

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubectlLayerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesManifest(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.KubernetesManifest",
):
    """Represents a manifest within the Kubernetes system.

    Alternatively, you can use ``cluster.addManifest(resource[, resource, ...])``
    to define resources on this cluster.

    Applies/deletes the manifest using ``kubectl``.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cluster: "ICluster",
        manifest: typing.List[typing.Any],
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The EKS cluster to apply this manifest to. [disable-awslint:ref-via-interface]
        :param manifest: The manifest to apply. Consists of any number of child resources. When the resources are created/updated, this manifest will be applied to the cluster through ``kubectl apply`` and when the resources or the stack is deleted, the resources in the manifest will be deleted through ``kubectl delete``.

        stability
        :stability: experimental
        """
        props = KubernetesManifestProps(cluster=cluster, manifest=manifest)

        jsii.create(KubernetesManifest, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="RESOURCE_TYPE")
    def RESOURCE_TYPE(cls) -> str:
        """The CloudFormation reosurce type.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "RESOURCE_TYPE")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.KubernetesManifestProps",
    jsii_struct_bases=[],
    name_mapping={"cluster": "cluster", "manifest": "manifest"},
)
class KubernetesManifestProps:
    def __init__(
        self, *, cluster: "ICluster", manifest: typing.List[typing.Any]
    ) -> None:
        """Properties for KubernetesManifest.

        :param cluster: The EKS cluster to apply this manifest to. [disable-awslint:ref-via-interface]
        :param manifest: The manifest to apply. Consists of any number of child resources. When the resources are created/updated, this manifest will be applied to the cluster through ``kubectl apply`` and when the resources or the stack is deleted, the resources in the manifest will be deleted through ``kubectl delete``.

        stability
        :stability: experimental
        """
        self._values = {
            "cluster": cluster,
            "manifest": manifest,
        }

    @builtins.property
    def cluster(self) -> "ICluster":
        """The EKS cluster to apply this manifest to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get("cluster")

    @builtins.property
    def manifest(self) -> typing.List[typing.Any]:
        """The manifest to apply.

        Consists of any number of child resources.

        When the resources are created/updated, this manifest will be applied to the
        cluster through ``kubectl apply`` and when the resources or the stack is
        deleted, the resources in the manifest will be deleted through ``kubectl delete``.

        stability
        :stability: experimental

        Example::

            # Example automatically generated. See https://github.com/aws/jsii/issues/826
            [{
                "api_version": "v1",
                "kind": "Pod",
                "metadata": {"name": "mypod"},
                "spec": {
                    "containers": [{"name": "hello", "image": "paulbouwer/hello-kubernetes:1.5", "ports": [{"container_port": 8080}]}]
                }
            }]
        """
        return self._values.get("manifest")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesManifestProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesObjectValue(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.KubernetesObjectValue",
):
    """Represents a value of a specific object deployed in the cluster.

    Use this to fetch any information available by the ``kubectl get`` command.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cluster: "ICluster",
        json_path: str,
        object_name: str,
        object_type: str,
        object_namespace: typing.Optional[str] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The EKS cluster to fetch attributes from. [disable-awslint:ref-via-interface]
        :param json_path: JSONPath to the specific value.
        :param object_name: The name of the object to query.
        :param object_type: The object type to query. (e.g 'service', 'pod'...)
        :param object_namespace: The namespace the object belongs to. Default: 'default'
        :param timeout: Timeout for waiting on a value. Default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        props = KubernetesObjectValueProps(
            cluster=cluster,
            json_path=json_path,
            object_name=object_name,
            object_type=object_type,
            object_namespace=object_namespace,
            timeout=timeout,
        )

        jsii.create(KubernetesObjectValue, self, [scope, id, props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="RESOURCE_TYPE")
    def RESOURCE_TYPE(cls) -> str:
        """The CloudFormation reosurce type.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "RESOURCE_TYPE")

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> str:
        """The value as a string token.

        stability
        :stability: experimental
        """
        return jsii.get(self, "value")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.KubernetesObjectValueProps",
    jsii_struct_bases=[],
    name_mapping={
        "cluster": "cluster",
        "json_path": "jsonPath",
        "object_name": "objectName",
        "object_type": "objectType",
        "object_namespace": "objectNamespace",
        "timeout": "timeout",
    },
)
class KubernetesObjectValueProps:
    def __init__(
        self,
        *,
        cluster: "ICluster",
        json_path: str,
        object_name: str,
        object_type: str,
        object_namespace: typing.Optional[str] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """Properties for KubernetesObjectValue.

        :param cluster: The EKS cluster to fetch attributes from. [disable-awslint:ref-via-interface]
        :param json_path: JSONPath to the specific value.
        :param object_name: The name of the object to query.
        :param object_type: The object type to query. (e.g 'service', 'pod'...)
        :param object_namespace: The namespace the object belongs to. Default: 'default'
        :param timeout: Timeout for waiting on a value. Default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        self._values = {
            "cluster": cluster,
            "json_path": json_path,
            "object_name": object_name,
            "object_type": object_type,
        }
        if object_namespace is not None:
            self._values["object_namespace"] = object_namespace
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def cluster(self) -> "ICluster":
        """The EKS cluster to fetch attributes from.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get("cluster")

    @builtins.property
    def json_path(self) -> str:
        """JSONPath to the specific value.

        see
        :see: https://kubernetes.io/docs/reference/kubectl/jsonpath/
        stability
        :stability: experimental
        """
        return self._values.get("json_path")

    @builtins.property
    def object_name(self) -> str:
        """The name of the object to query.

        stability
        :stability: experimental
        """
        return self._values.get("object_name")

    @builtins.property
    def object_type(self) -> str:
        """The object type to query.

        (e.g 'service', 'pod'...)

        stability
        :stability: experimental
        """
        return self._values.get("object_type")

    @builtins.property
    def object_namespace(self) -> typing.Optional[str]:
        """The namespace the object belongs to.

        default
        :default: 'default'

        stability
        :stability: experimental
        """
        return self._values.get("object_namespace")

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Timeout for waiting on a value.

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get("timeout")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesObjectValueProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesPatch(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.KubernetesPatch",
):
    """A CloudFormation resource which applies/restores a JSON patch into a Kubernetes resource.

    see
    :see: https://kubernetes.io/docs/tasks/run-application/update-api-object-kubectl-patch/
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        apply_patch: typing.Mapping[str, typing.Any],
        cluster: "ICluster",
        resource_name: str,
        restore_patch: typing.Mapping[str, typing.Any],
        patch_type: typing.Optional["PatchType"] = None,
        resource_namespace: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param apply_patch: The JSON object to pass to ``kubectl patch`` when the resource is created/updated.
        :param cluster: The cluster to apply the patch to. [disable-awslint:ref-via-interface]
        :param resource_name: The full name of the resource to patch (e.g. ``deployment/coredns``).
        :param restore_patch: The JSON object to pass to ``kubectl patch`` when the resource is removed.
        :param patch_type: The patch type to pass to ``kubectl patch``. The default type used by ``kubectl patch`` is "strategic". Default: PatchType.STRATEGIC
        :param resource_namespace: The kubernetes API namespace. Default: "default"

        stability
        :stability: experimental
        """
        props = KubernetesPatchProps(
            apply_patch=apply_patch,
            cluster=cluster,
            resource_name=resource_name,
            restore_patch=restore_patch,
            patch_type=patch_type,
            resource_namespace=resource_namespace,
        )

        jsii.create(KubernetesPatch, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.KubernetesPatchProps",
    jsii_struct_bases=[],
    name_mapping={
        "apply_patch": "applyPatch",
        "cluster": "cluster",
        "resource_name": "resourceName",
        "restore_patch": "restorePatch",
        "patch_type": "patchType",
        "resource_namespace": "resourceNamespace",
    },
)
class KubernetesPatchProps:
    def __init__(
        self,
        *,
        apply_patch: typing.Mapping[str, typing.Any],
        cluster: "ICluster",
        resource_name: str,
        restore_patch: typing.Mapping[str, typing.Any],
        patch_type: typing.Optional["PatchType"] = None,
        resource_namespace: typing.Optional[str] = None,
    ) -> None:
        """Properties for KubernetesPatch.

        :param apply_patch: The JSON object to pass to ``kubectl patch`` when the resource is created/updated.
        :param cluster: The cluster to apply the patch to. [disable-awslint:ref-via-interface]
        :param resource_name: The full name of the resource to patch (e.g. ``deployment/coredns``).
        :param restore_patch: The JSON object to pass to ``kubectl patch`` when the resource is removed.
        :param patch_type: The patch type to pass to ``kubectl patch``. The default type used by ``kubectl patch`` is "strategic". Default: PatchType.STRATEGIC
        :param resource_namespace: The kubernetes API namespace. Default: "default"

        stability
        :stability: experimental
        """
        self._values = {
            "apply_patch": apply_patch,
            "cluster": cluster,
            "resource_name": resource_name,
            "restore_patch": restore_patch,
        }
        if patch_type is not None:
            self._values["patch_type"] = patch_type
        if resource_namespace is not None:
            self._values["resource_namespace"] = resource_namespace

    @builtins.property
    def apply_patch(self) -> typing.Mapping[str, typing.Any]:
        """The JSON object to pass to ``kubectl patch`` when the resource is created/updated.

        stability
        :stability: experimental
        """
        return self._values.get("apply_patch")

    @builtins.property
    def cluster(self) -> "ICluster":
        """The cluster to apply the patch to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get("cluster")

    @builtins.property
    def resource_name(self) -> str:
        """The full name of the resource to patch (e.g. ``deployment/coredns``).

        stability
        :stability: experimental
        """
        return self._values.get("resource_name")

    @builtins.property
    def restore_patch(self) -> typing.Mapping[str, typing.Any]:
        """The JSON object to pass to ``kubectl patch`` when the resource is removed.

        stability
        :stability: experimental
        """
        return self._values.get("restore_patch")

    @builtins.property
    def patch_type(self) -> typing.Optional["PatchType"]:
        """The patch type to pass to ``kubectl patch``.

        The default type used by ``kubectl patch`` is "strategic".

        default
        :default: PatchType.STRATEGIC

        stability
        :stability: experimental
        """
        return self._values.get("patch_type")

    @builtins.property
    def resource_namespace(self) -> typing.Optional[str]:
        """The kubernetes API namespace.

        default
        :default: "default"

        stability
        :stability: experimental
        """
        return self._values.get("resource_namespace")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KubernetesPatchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class KubernetesVersion(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_eks.KubernetesVersion"
):
    """Kubernetes cluster version.

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, version: str) -> "KubernetesVersion":
        """Custom cluster version.

        :param version: custom version number.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [version])

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_14")
    def V1_14(cls) -> "KubernetesVersion":
        """Kubernetes version 1.14.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "V1_14")

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_15")
    def V1_15(cls) -> "KubernetesVersion":
        """Kubernetes version 1.15.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "V1_15")

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_16")
    def V1_16(cls) -> "KubernetesVersion":
        """Kubernetes version 1.16.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "V1_16")

    @jsii.python.classproperty
    @jsii.member(jsii_name="V1_17")
    def V1_17(cls) -> "KubernetesVersion":
        """Kubernetes version 1.17.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "V1_17")

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """cluster version number.

        stability
        :stability: experimental
        """
        return jsii.get(self, "version")


@jsii.implements(ICluster)
class LegacyCluster(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.LegacyCluster",
):
    """A Cluster represents a managed Kubernetes Service (EKS).

    This is a fully managed cluster of API Servers (control-plane)
    The user is still required to create the worker nodes.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::EKS::Cluster
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        default_capacity: typing.Optional[jsii.Number] = None,
        default_capacity_instance: typing.Optional[_InstanceType_85a97b30] = None,
        default_capacity_type: typing.Optional["DefaultCapacityType"] = None,
        secrets_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        version: "KubernetesVersion",
        cluster_name: typing.Optional[str] = None,
        output_cluster_name: typing.Optional[bool] = None,
        output_config_command: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_group: typing.Optional[_ISecurityGroup_d72ab8e8] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
        vpc_subnets: typing.Optional[typing.List[_SubnetSelection_36a13cd6]] = None,
    ) -> None:
        """Initiates an EKS Cluster with the supplied arguments.

        :param scope: a Construct, most likely a cdk.Stack created.
        :param id: -
        :param default_capacity: Number of instances to allocate as an initial capacity for this cluster. Instance type can be configured through ``defaultCapacityInstanceType``, which defaults to ``m5.large``. Use ``cluster.addCapacity`` to add additional customized capacity. Set this to ``0`` is you wish to avoid the initial capacity allocation. Default: 2
        :param default_capacity_instance: The instance type to use for the default capacity. This will only be taken into account if ``defaultCapacity`` is > 0. Default: m5.large
        :param default_capacity_type: The default capacity type for the cluster. Default: NODEGROUP
        :param secrets_encryption_key: KMS secret for envelope encryption for Kubernetes secrets. Default: - By default, Kubernetes stores all secret object data within etcd and all etcd volumes used by Amazon EKS are encrypted at the disk-level using AWS-Managed encryption keys.
        :param version: The Kubernetes version to run in the cluster.
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets

        stability
        :stability: experimental
        """
        props = LegacyClusterProps(
            default_capacity=default_capacity,
            default_capacity_instance=default_capacity_instance,
            default_capacity_type=default_capacity_type,
            secrets_encryption_key=secrets_encryption_key,
            version=version,
            cluster_name=cluster_name,
            output_cluster_name=output_cluster_name,
            output_config_command=output_config_command,
            role=role,
            security_group=security_group,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(LegacyCluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterAttributes")
    @builtins.classmethod
    def from_cluster_attributes(
        cls,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cluster_name: str,
        cluster_certificate_authority_data: typing.Optional[str] = None,
        cluster_encryption_config_key_arn: typing.Optional[str] = None,
        cluster_endpoint: typing.Optional[str] = None,
        cluster_security_group_id: typing.Optional[str] = None,
        kubectl_environment: typing.Optional[typing.Mapping[str, str]] = None,
        kubectl_layer: typing.Optional[_ILayerVersion_aa5e0c0c] = None,
        kubectl_private_subnet_ids: typing.Optional[typing.List[str]] = None,
        kubectl_role_arn: typing.Optional[str] = None,
        kubectl_security_group_id: typing.Optional[str] = None,
        security_group_ids: typing.Optional[typing.List[str]] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
    ) -> "ICluster":
        """Import an existing cluster.

        :param scope: the construct scope, in most cases 'this'.
        :param id: the id or name to import as.
        :param cluster_name: The physical name of the Cluster.
        :param cluster_certificate_authority_data: The certificate-authority-data for your cluster. Default: - if not specified ``cluster.clusterCertificateAuthorityData`` will throw an error
        :param cluster_encryption_config_key_arn: Amazon Resource Name (ARN) or alias of the customer master key (CMK). Default: - if not specified ``cluster.clusterEncryptionConfigKeyArn`` will throw an error
        :param cluster_endpoint: The API Server endpoint URL. Default: - if not specified ``cluster.clusterEndpoint`` will throw an error.
        :param cluster_security_group_id: The cluster security group that was created by Amazon EKS for the cluster. Default: - if not specified ``cluster.clusterSecurityGroupId`` will throw an error
        :param kubectl_environment: Environment variables to use when running ``kubectl`` against this cluster. Default: - no additional variables
        :param kubectl_layer: An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI. By default, the provider will use the layer included in the "aws-lambda-layer-kubectl" SAR application which is available in all commercial regions. To deploy the layer locally, visit https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md for instructions on how to prepare the .zip file and then define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'kubectl-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`)), compatibleRuntimes: [lambda.Runtime.PROVIDED] }); Or you can use the standard layer like this (with options to customize the version and SAR application ID): ```ts const layer = new eks.KubectlLayer(this, 'KubectlLayer'); Default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.
        :param kubectl_private_subnet_ids: Subnets to host the ``kubectl`` compute resources. If not specified, the k8s endpoint is expected to be accessible publicly. Default: - k8s endpoint is expected to be accessible publicly
        :param kubectl_role_arn: An IAM role with cluster administrator and "system:masters" permissions. Default: - if not specified, it not be possible to issue ``kubectl`` commands against an imported cluster.
        :param kubectl_security_group_id: A security group to use for ``kubectl`` execution. If not specified, the k8s endpoint is expected to be accessible publicly. Default: - k8s endpoint is expected to be accessible publicly
        :param security_group_ids: Additional security groups associated with this cluster. Default: - if not specified, no additional security groups will be considered in ``cluster.connections``.
        :param vpc: The VPC in which this Cluster was created. Default: - if not specified ``cluster.vpc`` will throw an error

        stability
        :stability: experimental
        """
        attrs = ClusterAttributes(
            cluster_name=cluster_name,
            cluster_certificate_authority_data=cluster_certificate_authority_data,
            cluster_encryption_config_key_arn=cluster_encryption_config_key_arn,
            cluster_endpoint=cluster_endpoint,
            cluster_security_group_id=cluster_security_group_id,
            kubectl_environment=kubectl_environment,
            kubectl_layer=kubectl_layer,
            kubectl_private_subnet_ids=kubectl_private_subnet_ids,
            kubectl_role_arn=kubectl_role_arn,
            kubectl_security_group_id=kubectl_security_group_id,
            security_group_ids=security_group_ids,
            vpc=vpc,
        )

        return jsii.sinvoke(cls, "fromClusterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(
        self,
        auto_scaling_group: _AutoScalingGroup_003d0b84,
        *,
        bootstrap_enabled: typing.Optional[bool] = None,
        bootstrap_options: typing.Optional["BootstrapOptions"] = None,
        machine_image_type: typing.Optional["MachineImageType"] = None,
        map_role: typing.Optional[bool] = None,
    ) -> None:
        """Add compute capacity to this EKS cluster in the form of an AutoScalingGroup.

        The AutoScalingGroup must be running an EKS-optimized AMI containing the
        /etc/eks/bootstrap.sh script. This method will configure Security Groups,
        add the right policies to the instance role, apply the right tags, and add
        the required user data to the instance's launch configuration.

        Spot instances will be labeled ``lifecycle=Ec2Spot`` and tainted with ``PreferNoSchedule``.
        If kubectl is enabled, the
        `spot interrupt handler <https://github.com/awslabs/ec2-spot-labs/tree/master/ec2-spot-eks-solution/spot-termination-handler>`_
        daemon will be installed on all spot instances to handle
        `EC2 Spot Instance Termination Notices <https://aws.amazon.com/blogs/aws/new-ec2-spot-instance-termination-notices/>`_.

        Prefer to use ``addCapacity`` if possible.

        :param auto_scaling_group: [disable-awslint:ref-via-interface].
        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: Allows options for node bootstrapping through EC2 user data. Default: - default options
        :param machine_image_type: Allow options to specify different machine image type. Default: MachineImageType.AMAZON_LINUX_2
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html
        stability
        :stability: experimental
        """
        options = AutoScalingGroupOptions(
            bootstrap_enabled=bootstrap_enabled,
            bootstrap_options=bootstrap_options,
            machine_image_type=machine_image_type,
            map_role=map_role,
        )

        return jsii.invoke(self, "addAutoScalingGroup", [auto_scaling_group, options])

    @jsii.member(jsii_name="addCapacity")
    def add_capacity(
        self,
        id: str,
        *,
        instance_type: _InstanceType_85a97b30,
        bootstrap_enabled: typing.Optional[bool] = None,
        bootstrap_options: typing.Optional["BootstrapOptions"] = None,
        machine_image_type: typing.Optional["MachineImageType"] = None,
        map_role: typing.Optional[bool] = None,
        allow_all_outbound: typing.Optional[bool] = None,
        associate_public_ip_address: typing.Optional[bool] = None,
        auto_scaling_group_name: typing.Optional[str] = None,
        block_devices: typing.Optional[typing.List[_BlockDevice_6b64cf0c]] = None,
        cooldown: typing.Optional[_Duration_5170c158] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        group_metrics: typing.Optional[typing.List[_GroupMetrics_8f5d7498]] = None,
        health_check: typing.Optional[_HealthCheck_ed599e14] = None,
        ignore_unmodified_size_properties: typing.Optional[bool] = None,
        instance_monitoring: typing.Optional[_Monitoring_11cb7f01] = None,
        key_name: typing.Optional[str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_instance_lifetime: typing.Optional[_Duration_5170c158] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        notifications: typing.Optional[typing.List[_NotificationConfiguration_396b88c6]] = None,
        notifications_topic: typing.Optional[_ITopic_ef0ebe0e] = None,
        replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number] = None,
        resource_signal_count: typing.Optional[jsii.Number] = None,
        resource_signal_timeout: typing.Optional[_Duration_5170c158] = None,
        rolling_update_configuration: typing.Optional[_RollingUpdateConfiguration_c96dd49e] = None,
        spot_price: typing.Optional[str] = None,
        update_type: typing.Optional[_UpdateType_7a2ac17e] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> _AutoScalingGroup_003d0b84:
        """Add nodes to this EKS cluster.

        The nodes will automatically be configured with the right VPC and AMI
        for the instance type and Kubernetes version.

        Spot instances will be labeled ``lifecycle=Ec2Spot`` and tainted with ``PreferNoSchedule``.

        :param id: -
        :param instance_type: Instance type of the instances to start.
        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: EKS node bootstrapping options. Default: - none
        :param machine_image_type: Machine image type. Default: MachineImageType.AMAZON_LINUX_2
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).
        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param auto_scaling_group_name: The name of the Auto Scaling group. This name must be unique per Region per account. Default: - Auto generated by CloudFormation
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. If this is set to a number, every deployment will reset the amount of instances to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param group_metrics: Enable monitoring for group metrics, these metrics describe the group rather than any of its instances. To report all group metrics use ``GroupMetrics.all()`` Group metrics are reported in a granularity of 1 minute at no additional charge. Default: - no group metrics will be reported
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param instance_monitoring: Controls whether instances in this group are launched with detailed or basic monitoring. When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes. Default: - Monitoring.DETAILED
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param max_instance_lifetime: The maximum amount of time that an instance can be in service. The maximum duration applies to all current and future instances in the group. As an instance approaches its maximum duration, it is terminated and replaced, and cannot be used again. You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value, leave this property undefined. Default: none
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications: Configure autoscaling group to send notifications about fleet changes to an SNS topic(s). Default: - No fleet change notifications will be sent.
        :param notifications_topic: SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1
        :param resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
        :param rolling_update_configuration: Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_type: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.

        stability
        :stability: experimental
        """
        options = CapacityOptions(
            instance_type=instance_type,
            bootstrap_enabled=bootstrap_enabled,
            bootstrap_options=bootstrap_options,
            machine_image_type=machine_image_type,
            map_role=map_role,
            allow_all_outbound=allow_all_outbound,
            associate_public_ip_address=associate_public_ip_address,
            auto_scaling_group_name=auto_scaling_group_name,
            block_devices=block_devices,
            cooldown=cooldown,
            desired_capacity=desired_capacity,
            group_metrics=group_metrics,
            health_check=health_check,
            ignore_unmodified_size_properties=ignore_unmodified_size_properties,
            instance_monitoring=instance_monitoring,
            key_name=key_name,
            max_capacity=max_capacity,
            max_instance_lifetime=max_instance_lifetime,
            min_capacity=min_capacity,
            notifications=notifications,
            notifications_topic=notifications_topic,
            replacing_update_min_successful_instances_percent=replacing_update_min_successful_instances_percent,
            resource_signal_count=resource_signal_count,
            resource_signal_timeout=resource_signal_timeout,
            rolling_update_configuration=rolling_update_configuration,
            spot_price=spot_price,
            update_type=update_type,
            vpc_subnets=vpc_subnets,
        )

        return jsii.invoke(self, "addCapacity", [id, options])

    @jsii.member(jsii_name="addChart")
    def add_chart(
        self,
        _id: str,
        *,
        chart: str,
        create_namespace: typing.Optional[bool] = None,
        namespace: typing.Optional[str] = None,
        release: typing.Optional[str] = None,
        repository: typing.Optional[str] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        values: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        version: typing.Optional[str] = None,
        wait: typing.Optional[bool] = None,
    ) -> "HelmChart":
        """Defines a Helm chart in this cluster.

        :param _id: -
        :param chart: The name of the chart.
        :param create_namespace: create namespace if not exist. Default: true
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 53 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Default: Duration.minutes(5)
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. Default: - Helm will not wait before marking release as successful

        stability
        :stability: experimental
        """
        _options = HelmChartOptions(
            chart=chart,
            create_namespace=create_namespace,
            namespace=namespace,
            release=release,
            repository=repository,
            timeout=timeout,
            values=values,
            version=version,
            wait=wait,
        )

        return jsii.invoke(self, "addChart", [_id, _options])

    @jsii.member(jsii_name="addManifest")
    def add_manifest(self, _id: str, *_manifest: typing.Any) -> "KubernetesManifest":
        """Defines a Kubernetes resource in this cluster.

        The manifest will be applied/deleted using kubectl as needed.

        :param _id: -
        :param _manifest: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addManifest", [_id, *_manifest])

    @jsii.member(jsii_name="addNodegroup")
    def add_nodegroup(
        self,
        id: str,
        *,
        ami_type: typing.Optional["NodegroupAmiType"] = None,
        desired_size: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update: typing.Optional[bool] = None,
        instance_type: typing.Optional[_InstanceType_85a97b30] = None,
        labels: typing.Optional[typing.Mapping[str, str]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        nodegroup_name: typing.Optional[str] = None,
        node_role: typing.Optional[_IRole_e69bbae4] = None,
        release_version: typing.Optional[str] = None,
        remote_access: typing.Optional["NodegroupRemoteAccess"] = None,
        subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        tags: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> "Nodegroup":
        """Add managed nodegroup to this Amazon EKS cluster.

        This method will create a new managed nodegroup and add into the capacity.

        :param id: The ID of the nodegroup.
        :param ami_type: The AMI type for your node group. Default: AL2_x86_64
        :param desired_size: The current number of worker nodes that the managed node group should maintain. If not specified, the nodewgroup will initially create ``minSize`` instances. Default: 2
        :param disk_size: The root device disk size (in GiB) for your node group instances. Default: 20
        :param force_update: Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue. If an update fails because pods could not be drained, you can force the update after it fails to terminate the old node whether or not any pods are running on the node. Default: true
        :param instance_type: The instance type to use for your node group. Currently, you can specify a single instance type for a node group. The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the ``AL2_x86_64_GPU`` with the amiType parameter. Default: t3.medium
        :param labels: The Kubernetes labels to be applied to the nodes in the node group when they are created. Default: - None
        :param max_size: The maximum number of worker nodes that the managed node group can scale out to. Managed node groups can support up to 100 nodes by default. Default: - desiredSize
        :param min_size: The minimum number of worker nodes that the managed node group can scale in to. This number must be greater than zero. Default: 1
        :param nodegroup_name: Name of the Nodegroup. Default: - resource ID
        :param node_role: The IAM role to associate with your node group. The Amazon EKS worker node kubelet daemon makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched. Default: - None. Auto-generated if not specified.
        :param release_version: The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``). Default: - The latest available AMI version for the node group's current Kubernetes version is used.
        :param remote_access: The remote access (SSH) configuration to use with your node group. Disabled by default, however, if you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0) Default: - disabled
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. By specifying the SubnetSelection, the selected subnets will automatically apply required tags i.e. ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with the name of your cluster. Default: - private subnets
        :param tags: The metadata to apply to the node group to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Node group tags do not propagate to any other resources associated with the node group, such as the Amazon EC2 instances or subnets. Default: - None

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html
        stability
        :stability: experimental
        """
        options = NodegroupOptions(
            ami_type=ami_type,
            desired_size=desired_size,
            disk_size=disk_size,
            force_update=force_update,
            instance_type=instance_type,
            labels=labels,
            max_size=max_size,
            min_size=min_size,
            nodegroup_name=nodegroup_name,
            node_role=node_role,
            release_version=release_version,
            remote_access=remote_access,
            subnets=subnets,
            tags=tags,
        )

        return jsii.invoke(self, "addNodegroup", [id, options])

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The AWS generated ARN for the Cluster resource.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            arn:aws:eks:us-west-2666666666666cluster / prod
        """
        return jsii.get(self, "clusterArn")

    @builtins.property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        """The certificate-authority-data for your cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterCertificateAuthorityData")

    @builtins.property
    @jsii.member(jsii_name="clusterEncryptionConfigKeyArn")
    def cluster_encryption_config_key_arn(self) -> str:
        """Amazon Resource Name (ARN) or alias of the customer master key (CMK).

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterEncryptionConfigKeyArn")

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        """The endpoint URL for the Cluster.

        This is the URL inside the kubeconfig file to use with kubectl

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The Name of the created EKS Cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterName")

    @builtins.property
    @jsii.member(jsii_name="clusterSecurityGroupId")
    def cluster_security_group_id(self) -> str:
        """The cluster security group that was created by Amazon EKS for the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterSecurityGroupId")

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Manages connection rules (Security Group Rules) for the cluster.

        stability
        :stability: experimental
        memberof:
        :memberof:: Cluster
        type:
        :type:: {ec2.Connections}
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _IRole_e69bbae4:
        """IAM role assumed by the EKS Control Plane.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")

    @builtins.property
    @jsii.member(jsii_name="defaultCapacity")
    def default_capacity(self) -> typing.Optional[_AutoScalingGroup_003d0b84]:
        """The auto scaling group that hosts the default capacity for this cluster.

        This will be ``undefined`` if the ``defaultCapacityType`` is not ``EC2`` or
        ``defaultCapacityType`` is ``EC2`` but default capacity is set to 0.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultCapacity")

    @builtins.property
    @jsii.member(jsii_name="defaultNodegroup")
    def default_nodegroup(self) -> typing.Optional["Nodegroup"]:
        """The node group that hosts the default capacity for this cluster.

        This will be ``undefined`` if the ``defaultCapacityType`` is ``EC2`` or
        ``defaultCapacityType`` is ``NODEGROUP`` but default capacity is set to 0.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultNodegroup")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.LegacyClusterProps",
    jsii_struct_bases=[CommonClusterOptions],
    name_mapping={
        "version": "version",
        "cluster_name": "clusterName",
        "output_cluster_name": "outputClusterName",
        "output_config_command": "outputConfigCommand",
        "role": "role",
        "security_group": "securityGroup",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "default_capacity": "defaultCapacity",
        "default_capacity_instance": "defaultCapacityInstance",
        "default_capacity_type": "defaultCapacityType",
        "secrets_encryption_key": "secretsEncryptionKey",
    },
)
class LegacyClusterProps(CommonClusterOptions):
    def __init__(
        self,
        *,
        version: "KubernetesVersion",
        cluster_name: typing.Optional[str] = None,
        output_cluster_name: typing.Optional[bool] = None,
        output_config_command: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_group: typing.Optional[_ISecurityGroup_d72ab8e8] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
        vpc_subnets: typing.Optional[typing.List[_SubnetSelection_36a13cd6]] = None,
        default_capacity: typing.Optional[jsii.Number] = None,
        default_capacity_instance: typing.Optional[_InstanceType_85a97b30] = None,
        default_capacity_type: typing.Optional["DefaultCapacityType"] = None,
        secrets_encryption_key: typing.Optional[_IKey_3336c79d] = None,
    ) -> None:
        """Common configuration props for EKS clusters.

        :param version: The Kubernetes version to run in the cluster.
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets
        :param default_capacity: Number of instances to allocate as an initial capacity for this cluster. Instance type can be configured through ``defaultCapacityInstanceType``, which defaults to ``m5.large``. Use ``cluster.addCapacity`` to add additional customized capacity. Set this to ``0`` is you wish to avoid the initial capacity allocation. Default: 2
        :param default_capacity_instance: The instance type to use for the default capacity. This will only be taken into account if ``defaultCapacity`` is > 0. Default: m5.large
        :param default_capacity_type: The default capacity type for the cluster. Default: NODEGROUP
        :param secrets_encryption_key: KMS secret for envelope encryption for Kubernetes secrets. Default: - By default, Kubernetes stores all secret object data within etcd and all etcd volumes used by Amazon EKS are encrypted at the disk-level using AWS-Managed encryption keys.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if output_cluster_name is not None:
            self._values["output_cluster_name"] = output_cluster_name
        if output_config_command is not None:
            self._values["output_config_command"] = output_config_command
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if default_capacity is not None:
            self._values["default_capacity"] = default_capacity
        if default_capacity_instance is not None:
            self._values["default_capacity_instance"] = default_capacity_instance
        if default_capacity_type is not None:
            self._values["default_capacity_type"] = default_capacity_type
        if secrets_encryption_key is not None:
            self._values["secrets_encryption_key"] = secrets_encryption_key

    @builtins.property
    def version(self) -> "KubernetesVersion":
        """The Kubernetes version to run in the cluster.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """Name for the cluster.

        default
        :default: - Automatically generated name

        stability
        :stability: experimental
        """
        return self._values.get("cluster_name")

    @builtins.property
    def output_cluster_name(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the name of the cluster will be synthesized.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("output_cluster_name")

    @builtins.property
    def output_config_command(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized.

        This command will include
        the cluster name and, if applicable, the ARN of the masters IAM role.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("output_config_command")

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get("role")

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """Security Group to use for Control Plane ENIs.

        default
        :default: - A security group is automatically created

        stability
        :stability: experimental
        """
        return self._values.get("security_group")

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC in which to create the Cluster.

        default
        :default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[typing.List[_SubnetSelection_36a13cd6]]:
        """Where to place EKS Control Plane ENIs.

        If you want to create public load balancers, this must include public subnets.

        For example, to only select private subnets, supply the following::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           vpcSubnets: [
              { subnetType: ec2.SubnetType.Private }
           ]

        default
        :default: - All public and private subnets

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    @builtins.property
    def default_capacity(self) -> typing.Optional[jsii.Number]:
        """Number of instances to allocate as an initial capacity for this cluster.

        Instance type can be configured through ``defaultCapacityInstanceType``,
        which defaults to ``m5.large``.

        Use ``cluster.addCapacity`` to add additional customized capacity. Set this
        to ``0`` is you wish to avoid the initial capacity allocation.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get("default_capacity")

    @builtins.property
    def default_capacity_instance(self) -> typing.Optional[_InstanceType_85a97b30]:
        """The instance type to use for the default capacity.

        This will only be taken
        into account if ``defaultCapacity`` is > 0.

        default
        :default: m5.large

        stability
        :stability: experimental
        """
        return self._values.get("default_capacity_instance")

    @builtins.property
    def default_capacity_type(self) -> typing.Optional["DefaultCapacityType"]:
        """The default capacity type for the cluster.

        default
        :default: NODEGROUP

        stability
        :stability: experimental
        """
        return self._values.get("default_capacity_type")

    @builtins.property
    def secrets_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """KMS secret for envelope encryption for Kubernetes secrets.

        default
        :default:

        - By default, Kubernetes stores all secret object data within etcd and
          all etcd volumes used by Amazon EKS are encrypted at the disk-level
          using AWS-Managed encryption keys.

        stability
        :stability: experimental
        """
        return self._values.get("secrets_encryption_key")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LegacyClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.aws_eks.MachineImageType")
class MachineImageType(enum.Enum):
    """The machine image type.

    stability
    :stability: experimental
    """

    AMAZON_LINUX_2 = "AMAZON_LINUX_2"
    """Amazon EKS-optimized Linux AMI.

    stability
    :stability: experimental
    """
    BOTTLEROCKET = "BOTTLEROCKET"
    """Bottlerocket AMI.

    stability
    :stability: experimental
    """


@jsii.enum(jsii_type="monocdk-experiment.aws_eks.NodeType")
class NodeType(enum.Enum):
    """Whether the worker nodes should support GPU or just standard instances.

    stability
    :stability: experimental
    """

    STANDARD = "STANDARD"
    """Standard instances.

    stability
    :stability: experimental
    """
    GPU = "GPU"
    """GPU instances.

    stability
    :stability: experimental
    """
    INFERENTIA = "INFERENTIA"
    """Inferentia instances.

    stability
    :stability: experimental
    """


@jsii.implements(INodegroup)
class Nodegroup(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.Nodegroup",
):
    """The Nodegroup resource class.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cluster: "ICluster",
        ami_type: typing.Optional["NodegroupAmiType"] = None,
        desired_size: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update: typing.Optional[bool] = None,
        instance_type: typing.Optional[_InstanceType_85a97b30] = None,
        labels: typing.Optional[typing.Mapping[str, str]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        nodegroup_name: typing.Optional[str] = None,
        node_role: typing.Optional[_IRole_e69bbae4] = None,
        release_version: typing.Optional[str] = None,
        remote_access: typing.Optional["NodegroupRemoteAccess"] = None,
        subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        tags: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: Cluster resource.
        :param ami_type: The AMI type for your node group. Default: AL2_x86_64
        :param desired_size: The current number of worker nodes that the managed node group should maintain. If not specified, the nodewgroup will initially create ``minSize`` instances. Default: 2
        :param disk_size: The root device disk size (in GiB) for your node group instances. Default: 20
        :param force_update: Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue. If an update fails because pods could not be drained, you can force the update after it fails to terminate the old node whether or not any pods are running on the node. Default: true
        :param instance_type: The instance type to use for your node group. Currently, you can specify a single instance type for a node group. The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the ``AL2_x86_64_GPU`` with the amiType parameter. Default: t3.medium
        :param labels: The Kubernetes labels to be applied to the nodes in the node group when they are created. Default: - None
        :param max_size: The maximum number of worker nodes that the managed node group can scale out to. Managed node groups can support up to 100 nodes by default. Default: - desiredSize
        :param min_size: The minimum number of worker nodes that the managed node group can scale in to. This number must be greater than zero. Default: 1
        :param nodegroup_name: Name of the Nodegroup. Default: - resource ID
        :param node_role: The IAM role to associate with your node group. The Amazon EKS worker node kubelet daemon makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched. Default: - None. Auto-generated if not specified.
        :param release_version: The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``). Default: - The latest available AMI version for the node group's current Kubernetes version is used.
        :param remote_access: The remote access (SSH) configuration to use with your node group. Disabled by default, however, if you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0) Default: - disabled
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. By specifying the SubnetSelection, the selected subnets will automatically apply required tags i.e. ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with the name of your cluster. Default: - private subnets
        :param tags: The metadata to apply to the node group to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Node group tags do not propagate to any other resources associated with the node group, such as the Amazon EC2 instances or subnets. Default: - None

        stability
        :stability: experimental
        """
        props = NodegroupProps(
            cluster=cluster,
            ami_type=ami_type,
            desired_size=desired_size,
            disk_size=disk_size,
            force_update=force_update,
            instance_type=instance_type,
            labels=labels,
            max_size=max_size,
            min_size=min_size,
            nodegroup_name=nodegroup_name,
            node_role=node_role,
            release_version=release_version,
            remote_access=remote_access,
            subnets=subnets,
            tags=tags,
        )

        jsii.create(Nodegroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromNodegroupName")
    @builtins.classmethod
    def from_nodegroup_name(
        cls, scope: _Construct_f50a3f53, id: str, nodegroup_name: str
    ) -> "INodegroup":
        """Import the Nodegroup from attributes.

        :param scope: -
        :param id: -
        :param nodegroup_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromNodegroupName", [scope, id, nodegroup_name])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> "ICluster":
        """the Amazon EKS cluster resource.

        stability
        :stability: experimental
        attribute:
        :attribute:: ClusterName
        """
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="nodegroupArn")
    def nodegroup_arn(self) -> str:
        """ARN of the nodegroup.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "nodegroupArn")

    @builtins.property
    @jsii.member(jsii_name="nodegroupName")
    def nodegroup_name(self) -> str:
        """Nodegroup name.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "nodegroupName")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _IRole_e69bbae4:
        """IAM role of the instance profile for the nodegroup.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")


@jsii.enum(jsii_type="monocdk-experiment.aws_eks.NodegroupAmiType")
class NodegroupAmiType(enum.Enum):
    """The AMI type for your node group.

    GPU instance types should use the ``AL2_x86_64_GPU`` AMI type, which uses the
    Amazon EKS-optimized Linux AMI with GPU support. Non-GPU instances should use the ``AL2_x86_64`` AMI type, which
    uses the Amazon EKS-optimized Linux AMI.

    stability
    :stability: experimental
    """

    AL2_X86_64 = "AL2_X86_64"
    """Amazon Linux 2.

    stability
    :stability: experimental
    """
    AL2_X86_64_GPU = "AL2_X86_64_GPU"
    """Amazon Linux 2 with GPU support.

    stability
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.NodegroupOptions",
    jsii_struct_bases=[],
    name_mapping={
        "ami_type": "amiType",
        "desired_size": "desiredSize",
        "disk_size": "diskSize",
        "force_update": "forceUpdate",
        "instance_type": "instanceType",
        "labels": "labels",
        "max_size": "maxSize",
        "min_size": "minSize",
        "nodegroup_name": "nodegroupName",
        "node_role": "nodeRole",
        "release_version": "releaseVersion",
        "remote_access": "remoteAccess",
        "subnets": "subnets",
        "tags": "tags",
    },
)
class NodegroupOptions:
    def __init__(
        self,
        *,
        ami_type: typing.Optional["NodegroupAmiType"] = None,
        desired_size: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update: typing.Optional[bool] = None,
        instance_type: typing.Optional[_InstanceType_85a97b30] = None,
        labels: typing.Optional[typing.Mapping[str, str]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        nodegroup_name: typing.Optional[str] = None,
        node_role: typing.Optional[_IRole_e69bbae4] = None,
        release_version: typing.Optional[str] = None,
        remote_access: typing.Optional["NodegroupRemoteAccess"] = None,
        subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        tags: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> None:
        """The Nodegroup Options for addNodeGroup() method.

        :param ami_type: The AMI type for your node group. Default: AL2_x86_64
        :param desired_size: The current number of worker nodes that the managed node group should maintain. If not specified, the nodewgroup will initially create ``minSize`` instances. Default: 2
        :param disk_size: The root device disk size (in GiB) for your node group instances. Default: 20
        :param force_update: Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue. If an update fails because pods could not be drained, you can force the update after it fails to terminate the old node whether or not any pods are running on the node. Default: true
        :param instance_type: The instance type to use for your node group. Currently, you can specify a single instance type for a node group. The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the ``AL2_x86_64_GPU`` with the amiType parameter. Default: t3.medium
        :param labels: The Kubernetes labels to be applied to the nodes in the node group when they are created. Default: - None
        :param max_size: The maximum number of worker nodes that the managed node group can scale out to. Managed node groups can support up to 100 nodes by default. Default: - desiredSize
        :param min_size: The minimum number of worker nodes that the managed node group can scale in to. This number must be greater than zero. Default: 1
        :param nodegroup_name: Name of the Nodegroup. Default: - resource ID
        :param node_role: The IAM role to associate with your node group. The Amazon EKS worker node kubelet daemon makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched. Default: - None. Auto-generated if not specified.
        :param release_version: The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``). Default: - The latest available AMI version for the node group's current Kubernetes version is used.
        :param remote_access: The remote access (SSH) configuration to use with your node group. Disabled by default, however, if you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0) Default: - disabled
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. By specifying the SubnetSelection, the selected subnets will automatically apply required tags i.e. ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with the name of your cluster. Default: - private subnets
        :param tags: The metadata to apply to the node group to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Node group tags do not propagate to any other resources associated with the node group, such as the Amazon EC2 instances or subnets. Default: - None

        stability
        :stability: experimental
        """
        if isinstance(remote_access, dict):
            remote_access = NodegroupRemoteAccess(**remote_access)
        if isinstance(subnets, dict):
            subnets = _SubnetSelection_36a13cd6(**subnets)
        self._values = {}
        if ami_type is not None:
            self._values["ami_type"] = ami_type
        if desired_size is not None:
            self._values["desired_size"] = desired_size
        if disk_size is not None:
            self._values["disk_size"] = disk_size
        if force_update is not None:
            self._values["force_update"] = force_update
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if labels is not None:
            self._values["labels"] = labels
        if max_size is not None:
            self._values["max_size"] = max_size
        if min_size is not None:
            self._values["min_size"] = min_size
        if nodegroup_name is not None:
            self._values["nodegroup_name"] = nodegroup_name
        if node_role is not None:
            self._values["node_role"] = node_role
        if release_version is not None:
            self._values["release_version"] = release_version
        if remote_access is not None:
            self._values["remote_access"] = remote_access
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def ami_type(self) -> typing.Optional["NodegroupAmiType"]:
        """The AMI type for your node group.

        default
        :default: AL2_x86_64

        stability
        :stability: experimental
        """
        return self._values.get("ami_type")

    @builtins.property
    def desired_size(self) -> typing.Optional[jsii.Number]:
        """The current number of worker nodes that the managed node group should maintain.

        If not specified,
        the nodewgroup will initially create ``minSize`` instances.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get("desired_size")

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        """The root device disk size (in GiB) for your node group instances.

        default
        :default: 20

        stability
        :stability: experimental
        """
        return self._values.get("disk_size")

    @builtins.property
    def force_update(self) -> typing.Optional[bool]:
        """Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue.

        If an update fails because pods could not be drained, you can force the update after it fails to terminate the old
        node whether or not any pods are
        running on the node.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("force_update")

    @builtins.property
    def instance_type(self) -> typing.Optional[_InstanceType_85a97b30]:
        """The instance type to use for your node group.

        Currently, you can specify a single instance type for a node group.
        The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the
        ``AL2_x86_64_GPU`` with the amiType parameter.

        default
        :default: t3.medium

        stability
        :stability: experimental
        """
        return self._values.get("instance_type")

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The Kubernetes labels to be applied to the nodes in the node group when they are created.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get("labels")

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        """The maximum number of worker nodes that the managed node group can scale out to.

        Managed node groups can support up to 100 nodes by default.

        default
        :default: - desiredSize

        stability
        :stability: experimental
        """
        return self._values.get("max_size")

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        """The minimum number of worker nodes that the managed node group can scale in to.

        This number must be greater than zero.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get("min_size")

    @builtins.property
    def nodegroup_name(self) -> typing.Optional[str]:
        """Name of the Nodegroup.

        default
        :default: - resource ID

        stability
        :stability: experimental
        """
        return self._values.get("nodegroup_name")

    @builtins.property
    def node_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role to associate with your node group.

        The Amazon EKS worker node kubelet daemon
        makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through
        an IAM instance profile and associated policies. Before you can launch worker nodes and register them
        into a cluster, you must create an IAM role for those worker nodes to use when they are launched.

        default
        :default: - None. Auto-generated if not specified.

        stability
        :stability: experimental
        """
        return self._values.get("node_role")

    @builtins.property
    def release_version(self) -> typing.Optional[str]:
        """The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``).

        default
        :default: - The latest available AMI version for the node group's current Kubernetes version is used.

        stability
        :stability: experimental
        """
        return self._values.get("release_version")

    @builtins.property
    def remote_access(self) -> typing.Optional["NodegroupRemoteAccess"]:
        """The remote access (SSH) configuration to use with your node group.

        Disabled by default, however, if you
        specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group,
        then port 22 on the worker nodes is opened to the internet (0.0.0.0/0)

        default
        :default: - disabled

        stability
        :stability: experimental
        """
        return self._values.get("remote_access")

    @builtins.property
    def subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The subnets to use for the Auto Scaling group that is created for your node group.

        By specifying the
        SubnetSelection, the selected subnets will automatically apply required tags i.e.
        ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with
        the name of your cluster.

        default
        :default: - private subnets

        stability
        :stability: experimental
        """
        return self._values.get("subnets")

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The metadata to apply to the node group to assist with categorization and organization.

        Each tag consists of
        a key and an optional value, both of which you define. Node group tags do not propagate to any other resources
        associated with the node group, such as the Amazon EC2 instances or subnets.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodegroupOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.NodegroupProps",
    jsii_struct_bases=[NodegroupOptions],
    name_mapping={
        "ami_type": "amiType",
        "desired_size": "desiredSize",
        "disk_size": "diskSize",
        "force_update": "forceUpdate",
        "instance_type": "instanceType",
        "labels": "labels",
        "max_size": "maxSize",
        "min_size": "minSize",
        "nodegroup_name": "nodegroupName",
        "node_role": "nodeRole",
        "release_version": "releaseVersion",
        "remote_access": "remoteAccess",
        "subnets": "subnets",
        "tags": "tags",
        "cluster": "cluster",
    },
)
class NodegroupProps(NodegroupOptions):
    def __init__(
        self,
        *,
        ami_type: typing.Optional["NodegroupAmiType"] = None,
        desired_size: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update: typing.Optional[bool] = None,
        instance_type: typing.Optional[_InstanceType_85a97b30] = None,
        labels: typing.Optional[typing.Mapping[str, str]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        nodegroup_name: typing.Optional[str] = None,
        node_role: typing.Optional[_IRole_e69bbae4] = None,
        release_version: typing.Optional[str] = None,
        remote_access: typing.Optional["NodegroupRemoteAccess"] = None,
        subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        tags: typing.Optional[typing.Mapping[str, str]] = None,
        cluster: "ICluster",
    ) -> None:
        """NodeGroup properties interface.

        :param ami_type: The AMI type for your node group. Default: AL2_x86_64
        :param desired_size: The current number of worker nodes that the managed node group should maintain. If not specified, the nodewgroup will initially create ``minSize`` instances. Default: 2
        :param disk_size: The root device disk size (in GiB) for your node group instances. Default: 20
        :param force_update: Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue. If an update fails because pods could not be drained, you can force the update after it fails to terminate the old node whether or not any pods are running on the node. Default: true
        :param instance_type: The instance type to use for your node group. Currently, you can specify a single instance type for a node group. The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the ``AL2_x86_64_GPU`` with the amiType parameter. Default: t3.medium
        :param labels: The Kubernetes labels to be applied to the nodes in the node group when they are created. Default: - None
        :param max_size: The maximum number of worker nodes that the managed node group can scale out to. Managed node groups can support up to 100 nodes by default. Default: - desiredSize
        :param min_size: The minimum number of worker nodes that the managed node group can scale in to. This number must be greater than zero. Default: 1
        :param nodegroup_name: Name of the Nodegroup. Default: - resource ID
        :param node_role: The IAM role to associate with your node group. The Amazon EKS worker node kubelet daemon makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched. Default: - None. Auto-generated if not specified.
        :param release_version: The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``). Default: - The latest available AMI version for the node group's current Kubernetes version is used.
        :param remote_access: The remote access (SSH) configuration to use with your node group. Disabled by default, however, if you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0) Default: - disabled
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. By specifying the SubnetSelection, the selected subnets will automatically apply required tags i.e. ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with the name of your cluster. Default: - private subnets
        :param tags: The metadata to apply to the node group to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Node group tags do not propagate to any other resources associated with the node group, such as the Amazon EC2 instances or subnets. Default: - None
        :param cluster: Cluster resource.

        stability
        :stability: experimental
        """
        if isinstance(remote_access, dict):
            remote_access = NodegroupRemoteAccess(**remote_access)
        if isinstance(subnets, dict):
            subnets = _SubnetSelection_36a13cd6(**subnets)
        self._values = {
            "cluster": cluster,
        }
        if ami_type is not None:
            self._values["ami_type"] = ami_type
        if desired_size is not None:
            self._values["desired_size"] = desired_size
        if disk_size is not None:
            self._values["disk_size"] = disk_size
        if force_update is not None:
            self._values["force_update"] = force_update
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if labels is not None:
            self._values["labels"] = labels
        if max_size is not None:
            self._values["max_size"] = max_size
        if min_size is not None:
            self._values["min_size"] = min_size
        if nodegroup_name is not None:
            self._values["nodegroup_name"] = nodegroup_name
        if node_role is not None:
            self._values["node_role"] = node_role
        if release_version is not None:
            self._values["release_version"] = release_version
        if remote_access is not None:
            self._values["remote_access"] = remote_access
        if subnets is not None:
            self._values["subnets"] = subnets
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def ami_type(self) -> typing.Optional["NodegroupAmiType"]:
        """The AMI type for your node group.

        default
        :default: AL2_x86_64

        stability
        :stability: experimental
        """
        return self._values.get("ami_type")

    @builtins.property
    def desired_size(self) -> typing.Optional[jsii.Number]:
        """The current number of worker nodes that the managed node group should maintain.

        If not specified,
        the nodewgroup will initially create ``minSize`` instances.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get("desired_size")

    @builtins.property
    def disk_size(self) -> typing.Optional[jsii.Number]:
        """The root device disk size (in GiB) for your node group instances.

        default
        :default: 20

        stability
        :stability: experimental
        """
        return self._values.get("disk_size")

    @builtins.property
    def force_update(self) -> typing.Optional[bool]:
        """Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue.

        If an update fails because pods could not be drained, you can force the update after it fails to terminate the old
        node whether or not any pods are
        running on the node.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("force_update")

    @builtins.property
    def instance_type(self) -> typing.Optional[_InstanceType_85a97b30]:
        """The instance type to use for your node group.

        Currently, you can specify a single instance type for a node group.
        The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the
        ``AL2_x86_64_GPU`` with the amiType parameter.

        default
        :default: t3.medium

        stability
        :stability: experimental
        """
        return self._values.get("instance_type")

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The Kubernetes labels to be applied to the nodes in the node group when they are created.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get("labels")

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        """The maximum number of worker nodes that the managed node group can scale out to.

        Managed node groups can support up to 100 nodes by default.

        default
        :default: - desiredSize

        stability
        :stability: experimental
        """
        return self._values.get("max_size")

    @builtins.property
    def min_size(self) -> typing.Optional[jsii.Number]:
        """The minimum number of worker nodes that the managed node group can scale in to.

        This number must be greater than zero.

        default
        :default: 1

        stability
        :stability: experimental
        """
        return self._values.get("min_size")

    @builtins.property
    def nodegroup_name(self) -> typing.Optional[str]:
        """Name of the Nodegroup.

        default
        :default: - resource ID

        stability
        :stability: experimental
        """
        return self._values.get("nodegroup_name")

    @builtins.property
    def node_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role to associate with your node group.

        The Amazon EKS worker node kubelet daemon
        makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through
        an IAM instance profile and associated policies. Before you can launch worker nodes and register them
        into a cluster, you must create an IAM role for those worker nodes to use when they are launched.

        default
        :default: - None. Auto-generated if not specified.

        stability
        :stability: experimental
        """
        return self._values.get("node_role")

    @builtins.property
    def release_version(self) -> typing.Optional[str]:
        """The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``).

        default
        :default: - The latest available AMI version for the node group's current Kubernetes version is used.

        stability
        :stability: experimental
        """
        return self._values.get("release_version")

    @builtins.property
    def remote_access(self) -> typing.Optional["NodegroupRemoteAccess"]:
        """The remote access (SSH) configuration to use with your node group.

        Disabled by default, however, if you
        specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group,
        then port 22 on the worker nodes is opened to the internet (0.0.0.0/0)

        default
        :default: - disabled

        stability
        :stability: experimental
        """
        return self._values.get("remote_access")

    @builtins.property
    def subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The subnets to use for the Auto Scaling group that is created for your node group.

        By specifying the
        SubnetSelection, the selected subnets will automatically apply required tags i.e.
        ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with
        the name of your cluster.

        default
        :default: - private subnets

        stability
        :stability: experimental
        """
        return self._values.get("subnets")

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The metadata to apply to the node group to assist with categorization and organization.

        Each tag consists of
        a key and an optional value, both of which you define. Node group tags do not propagate to any other resources
        associated with the node group, such as the Amazon EC2 instances or subnets.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get("tags")

    @builtins.property
    def cluster(self) -> "ICluster":
        """Cluster resource.

        stability
        :stability: experimental
        """
        return self._values.get("cluster")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodegroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.NodegroupRemoteAccess",
    jsii_struct_bases=[],
    name_mapping={
        "ssh_key_name": "sshKeyName",
        "source_security_groups": "sourceSecurityGroups",
    },
)
class NodegroupRemoteAccess:
    def __init__(
        self,
        *,
        ssh_key_name: str,
        source_security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
    ) -> None:
        """The remote access (SSH) configuration to use with your node group.

        :param ssh_key_name: The Amazon EC2 SSH key that provides access for SSH communication with the worker nodes in the managed node group.
        :param source_security_groups: The security groups that are allowed SSH access (port 22) to the worker nodes. If you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0). Default: - port 22 on the worker nodes is opened to the internet (0.0.0.0/0)

        see
        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-eks-nodegroup-remoteaccess.html
        stability
        :stability: experimental
        """
        self._values = {
            "ssh_key_name": ssh_key_name,
        }
        if source_security_groups is not None:
            self._values["source_security_groups"] = source_security_groups

    @builtins.property
    def ssh_key_name(self) -> str:
        """The Amazon EC2 SSH key that provides access for SSH communication with the worker nodes in the managed node group.

        stability
        :stability: experimental
        """
        return self._values.get("ssh_key_name")

    @builtins.property
    def source_security_groups(
        self,
    ) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The security groups that are allowed SSH access (port 22) to the worker nodes.

        If you specify an Amazon EC2 SSH
        key but do not specify a source security group when you create a managed node group, then port 22 on the worker
        nodes is opened to the internet (0.0.0.0/0).

        default
        :default: - port 22 on the worker nodes is opened to the internet (0.0.0.0/0)

        stability
        :stability: experimental
        """
        return self._values.get("source_security_groups")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodegroupRemoteAccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.aws_eks.PatchType")
class PatchType(enum.Enum):
    """Values for ``kubectl patch`` --type argument.

    stability
    :stability: experimental
    """

    JSON = "JSON"
    """JSON Patch, RFC 6902.

    stability
    :stability: experimental
    """
    MERGE = "MERGE"
    """JSON Merge patch.

    stability
    :stability: experimental
    """
    STRATEGIC = "STRATEGIC"
    """Strategic merge patch.

    stability
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.Selector",
    jsii_struct_bases=[],
    name_mapping={"namespace": "namespace", "labels": "labels"},
)
class Selector:
    def __init__(
        self,
        *,
        namespace: str,
        labels: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> None:
        """Fargate profile selector.

        :param namespace: The Kubernetes namespace that the selector should match. You must specify a namespace for a selector. The selector only matches pods that are created in this namespace, but you can create multiple selectors to target multiple namespaces.
        :param labels: The Kubernetes labels that the selector should match. A pod must contain all of the labels that are specified in the selector for it to be considered a match. Default: - all pods within the namespace will be selected.

        stability
        :stability: experimental
        """
        self._values = {
            "namespace": namespace,
        }
        if labels is not None:
            self._values["labels"] = labels

    @builtins.property
    def namespace(self) -> str:
        """The Kubernetes namespace that the selector should match.

        You must specify a namespace for a selector. The selector only matches pods
        that are created in this namespace, but you can create multiple selectors
        to target multiple namespaces.

        stability
        :stability: experimental
        """
        return self._values.get("namespace")

    @builtins.property
    def labels(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The Kubernetes labels that the selector should match.

        A pod must contain
        all of the labels that are specified in the selector for it to be
        considered a match.

        default
        :default: - all pods within the namespace will be selected.

        stability
        :stability: experimental
        """
        return self._values.get("labels")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Selector(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IPrincipal_97126874)
class ServiceAccount(
    _Construct_f50a3f53,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.ServiceAccount",
):
    """Service Account.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cluster: "Cluster",
        name: typing.Optional[str] = None,
        namespace: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param cluster: The cluster to apply the patch to. [disable-awslint:ref-via-interface]
        :param name: The name of the service account. Default: - If no name is given, it will use the id of the resource.
        :param namespace: The namespace of the service account. Default: "default"

        stability
        :stability: experimental
        """
        props = ServiceAccountProps(cluster=cluster, name=name, namespace=namespace)

        jsii.create(ServiceAccount, self, [scope, id, props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: _PolicyStatement_f75dc775) -> bool:
        """Add to the policy of this principal.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToPolicy", [statement])

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self, statement: _PolicyStatement_f75dc775
    ) -> _AddToPrincipalPolicyResult_7f6eff3f:
        """Add to the policy of this principal.

        :param statement: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToPrincipalPolicy", [statement])

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> str:
        """When this Principal is used in an AssumeRole policy, the action to use.

        stability
        :stability: experimental
        """
        return jsii.get(self, "assumeRoleAction")

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_97126874:
        """The principal to grant permissions to.

        stability
        :stability: experimental
        """
        return jsii.get(self, "grantPrincipal")

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> _PrincipalPolicyFragment_621f702c:
        """Return the policy fragment that identifies this principal in a Policy.

        stability
        :stability: experimental
        """
        return jsii.get(self, "policyFragment")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _IRole_e69bbae4:
        """The role which is linked to the service account.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")

    @builtins.property
    @jsii.member(jsii_name="serviceAccountName")
    def service_account_name(self) -> str:
        """The name of the service account.

        stability
        :stability: experimental
        """
        return jsii.get(self, "serviceAccountName")

    @builtins.property
    @jsii.member(jsii_name="serviceAccountNamespace")
    def service_account_namespace(self) -> str:
        """The namespace where the service account is located in.

        stability
        :stability: experimental
        """
        return jsii.get(self, "serviceAccountNamespace")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.ServiceAccountOptions",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "namespace": "namespace"},
)
class ServiceAccountOptions:
    def __init__(
        self,
        *,
        name: typing.Optional[str] = None,
        namespace: typing.Optional[str] = None,
    ) -> None:
        """Options for ``ServiceAccount``.

        :param name: The name of the service account. Default: - If no name is given, it will use the id of the resource.
        :param namespace: The namespace of the service account. Default: "default"

        stability
        :stability: experimental
        """
        self._values = {}
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """The name of the service account.

        default
        :default: - If no name is given, it will use the id of the resource.

        stability
        :stability: experimental
        """
        return self._values.get("name")

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """The namespace of the service account.

        default
        :default: "default"

        stability
        :stability: experimental
        """
        return self._values.get("namespace")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAccountOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.ServiceAccountProps",
    jsii_struct_bases=[ServiceAccountOptions],
    name_mapping={"name": "name", "namespace": "namespace", "cluster": "cluster"},
)
class ServiceAccountProps(ServiceAccountOptions):
    def __init__(
        self,
        *,
        name: typing.Optional[str] = None,
        namespace: typing.Optional[str] = None,
        cluster: "Cluster",
    ) -> None:
        """Properties for defining service accounts.

        :param name: The name of the service account. Default: - If no name is given, it will use the id of the resource.
        :param namespace: The namespace of the service account. Default: "default"
        :param cluster: The cluster to apply the patch to. [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        self._values = {
            "cluster": cluster,
        }
        if name is not None:
            self._values["name"] = name
        if namespace is not None:
            self._values["namespace"] = namespace

    @builtins.property
    def name(self) -> typing.Optional[str]:
        """The name of the service account.

        default
        :default: - If no name is given, it will use the id of the resource.

        stability
        :stability: experimental
        """
        return self._values.get("name")

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """The namespace of the service account.

        default
        :default: "default"

        stability
        :stability: experimental
        """
        return self._values.get("namespace")

    @builtins.property
    def cluster(self) -> "Cluster":
        """The cluster to apply the patch to.

        [disable-awslint:ref-via-interface]

        stability
        :stability: experimental
        """
        return self._values.get("cluster")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceAccountProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.ServiceLoadBalancerAddressOptions",
    jsii_struct_bases=[],
    name_mapping={"namespace": "namespace", "timeout": "timeout"},
)
class ServiceLoadBalancerAddressOptions:
    def __init__(
        self,
        *,
        namespace: typing.Optional[str] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """Options for fetching a ServiceLoadBalancerAddress.

        :param namespace: The namespace the service belongs to. Default: 'default'
        :param timeout: Timeout for waiting on the load balancer address. Default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        self._values = {}
        if namespace is not None:
            self._values["namespace"] = namespace
        if timeout is not None:
            self._values["timeout"] = timeout

    @builtins.property
    def namespace(self) -> typing.Optional[str]:
        """The namespace the service belongs to.

        default
        :default: 'default'

        stability
        :stability: experimental
        """
        return self._values.get("namespace")

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """Timeout for waiting on the load balancer address.

        default
        :default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        return self._values.get("timeout")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceLoadBalancerAddressOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ICluster)
class Cluster(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.Cluster",
):
    """A Cluster represents a managed Kubernetes Service (EKS).

    This is a fully managed cluster of API Servers (control-plane)
    The user is still required to create the worker nodes.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        default_capacity: typing.Optional[jsii.Number] = None,
        default_capacity_instance: typing.Optional[_InstanceType_85a97b30] = None,
        default_capacity_type: typing.Optional["DefaultCapacityType"] = None,
        kubectl_enabled: typing.Optional[bool] = None,
        secrets_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        core_dns_compute_type: typing.Optional["CoreDnsComputeType"] = None,
        endpoint_access: typing.Optional["EndpointAccess"] = None,
        kubectl_environment: typing.Optional[typing.Mapping[str, str]] = None,
        kubectl_layer: typing.Optional[_ILayerVersion_aa5e0c0c] = None,
        masters_role: typing.Optional[_IRole_e69bbae4] = None,
        output_masters_role_arn: typing.Optional[bool] = None,
        version: "KubernetesVersion",
        cluster_name: typing.Optional[str] = None,
        output_cluster_name: typing.Optional[bool] = None,
        output_config_command: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_group: typing.Optional[_ISecurityGroup_d72ab8e8] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
        vpc_subnets: typing.Optional[typing.List[_SubnetSelection_36a13cd6]] = None,
    ) -> None:
        """Initiates an EKS Cluster with the supplied arguments.

        :param scope: a Construct, most likely a cdk.Stack created.
        :param id: -
        :param default_capacity: Number of instances to allocate as an initial capacity for this cluster. Instance type can be configured through ``defaultCapacityInstanceType``, which defaults to ``m5.large``. Use ``cluster.addCapacity`` to add additional customized capacity. Set this to ``0`` is you wish to avoid the initial capacity allocation. Default: 2
        :param default_capacity_instance: The instance type to use for the default capacity. This will only be taken into account if ``defaultCapacity`` is > 0. Default: m5.large
        :param default_capacity_type: The default capacity type for the cluster. Default: NODEGROUP
        :param kubectl_enabled: NOT SUPPORTED: We no longer allow disabling kubectl-support. Setting this option to ``false`` will throw an error. To temporary allow you to retain existing clusters created with ``kubectlEnabled: false``, you can use ``eks.LegacyCluster`` class, which is a drop-in replacement for ``eks.Cluster`` with ``kubectlEnabled: false``. Bear in mind that this is a temporary workaround. We have plans to remove ``eks.LegacyCluster``. If you have a use case for using ``eks.LegacyCluster``, please add a comment here https://github.com/aws/aws-cdk/issues/9332 and let us know so we can make sure to continue to support your use case with ``eks.Cluster``. This issue also includes additional context into why this class is being removed. Default: true
        :param secrets_encryption_key: KMS secret for envelope encryption for Kubernetes secrets. Default: - By default, Kubernetes stores all secret object data within etcd and all etcd volumes used by Amazon EKS are encrypted at the disk-level using AWS-Managed encryption keys.
        :param core_dns_compute_type: Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param endpoint_access: Configure access to the Kubernetes API server endpoint.. Default: EndpointAccess.PUBLIC_AND_PRIVATE
        :param kubectl_environment: Environment variables for the kubectl execution. Only relevant for kubectl enabled clusters. Default: - No environment variables.
        :param kubectl_layer: An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI. By default, the provider will use the layer included in the "aws-lambda-layer-kubectl" SAR application which is available in all commercial regions. To deploy the layer locally, visit https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md for instructions on how to prepare the .zip file and then define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'kubectl-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`)), compatibleRuntimes: [lambda.Runtime.PROVIDED] }) Default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - a role that assumable by anyone with permissions in the same account will automatically be defined
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param version: The Kubernetes version to run in the cluster.
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets

        stability
        :stability: experimental
        """
        props = ClusterProps(
            default_capacity=default_capacity,
            default_capacity_instance=default_capacity_instance,
            default_capacity_type=default_capacity_type,
            kubectl_enabled=kubectl_enabled,
            secrets_encryption_key=secrets_encryption_key,
            core_dns_compute_type=core_dns_compute_type,
            endpoint_access=endpoint_access,
            kubectl_environment=kubectl_environment,
            kubectl_layer=kubectl_layer,
            masters_role=masters_role,
            output_masters_role_arn=output_masters_role_arn,
            version=version,
            cluster_name=cluster_name,
            output_cluster_name=output_cluster_name,
            output_config_command=output_config_command,
            role=role,
            security_group=security_group,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(Cluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromClusterAttributes")
    @builtins.classmethod
    def from_cluster_attributes(
        cls,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cluster_name: str,
        cluster_certificate_authority_data: typing.Optional[str] = None,
        cluster_encryption_config_key_arn: typing.Optional[str] = None,
        cluster_endpoint: typing.Optional[str] = None,
        cluster_security_group_id: typing.Optional[str] = None,
        kubectl_environment: typing.Optional[typing.Mapping[str, str]] = None,
        kubectl_layer: typing.Optional[_ILayerVersion_aa5e0c0c] = None,
        kubectl_private_subnet_ids: typing.Optional[typing.List[str]] = None,
        kubectl_role_arn: typing.Optional[str] = None,
        kubectl_security_group_id: typing.Optional[str] = None,
        security_group_ids: typing.Optional[typing.List[str]] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
    ) -> "ICluster":
        """Import an existing cluster.

        :param scope: the construct scope, in most cases 'this'.
        :param id: the id or name to import as.
        :param cluster_name: The physical name of the Cluster.
        :param cluster_certificate_authority_data: The certificate-authority-data for your cluster. Default: - if not specified ``cluster.clusterCertificateAuthorityData`` will throw an error
        :param cluster_encryption_config_key_arn: Amazon Resource Name (ARN) or alias of the customer master key (CMK). Default: - if not specified ``cluster.clusterEncryptionConfigKeyArn`` will throw an error
        :param cluster_endpoint: The API Server endpoint URL. Default: - if not specified ``cluster.clusterEndpoint`` will throw an error.
        :param cluster_security_group_id: The cluster security group that was created by Amazon EKS for the cluster. Default: - if not specified ``cluster.clusterSecurityGroupId`` will throw an error
        :param kubectl_environment: Environment variables to use when running ``kubectl`` against this cluster. Default: - no additional variables
        :param kubectl_layer: An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI. By default, the provider will use the layer included in the "aws-lambda-layer-kubectl" SAR application which is available in all commercial regions. To deploy the layer locally, visit https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md for instructions on how to prepare the .zip file and then define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'kubectl-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`)), compatibleRuntimes: [lambda.Runtime.PROVIDED] }); Or you can use the standard layer like this (with options to customize the version and SAR application ID): ```ts const layer = new eks.KubectlLayer(this, 'KubectlLayer'); Default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.
        :param kubectl_private_subnet_ids: Subnets to host the ``kubectl`` compute resources. If not specified, the k8s endpoint is expected to be accessible publicly. Default: - k8s endpoint is expected to be accessible publicly
        :param kubectl_role_arn: An IAM role with cluster administrator and "system:masters" permissions. Default: - if not specified, it not be possible to issue ``kubectl`` commands against an imported cluster.
        :param kubectl_security_group_id: A security group to use for ``kubectl`` execution. If not specified, the k8s endpoint is expected to be accessible publicly. Default: - k8s endpoint is expected to be accessible publicly
        :param security_group_ids: Additional security groups associated with this cluster. Default: - if not specified, no additional security groups will be considered in ``cluster.connections``.
        :param vpc: The VPC in which this Cluster was created. Default: - if not specified ``cluster.vpc`` will throw an error

        stability
        :stability: experimental
        """
        attrs = ClusterAttributes(
            cluster_name=cluster_name,
            cluster_certificate_authority_data=cluster_certificate_authority_data,
            cluster_encryption_config_key_arn=cluster_encryption_config_key_arn,
            cluster_endpoint=cluster_endpoint,
            cluster_security_group_id=cluster_security_group_id,
            kubectl_environment=kubectl_environment,
            kubectl_layer=kubectl_layer,
            kubectl_private_subnet_ids=kubectl_private_subnet_ids,
            kubectl_role_arn=kubectl_role_arn,
            kubectl_security_group_id=kubectl_security_group_id,
            security_group_ids=security_group_ids,
            vpc=vpc,
        )

        return jsii.sinvoke(cls, "fromClusterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addAutoScalingGroup")
    def add_auto_scaling_group(
        self,
        auto_scaling_group: _AutoScalingGroup_003d0b84,
        *,
        bootstrap_enabled: typing.Optional[bool] = None,
        bootstrap_options: typing.Optional["BootstrapOptions"] = None,
        machine_image_type: typing.Optional["MachineImageType"] = None,
        map_role: typing.Optional[bool] = None,
    ) -> None:
        """Add compute capacity to this EKS cluster in the form of an AutoScalingGroup.

        The AutoScalingGroup must be running an EKS-optimized AMI containing the
        /etc/eks/bootstrap.sh script. This method will configure Security Groups,
        add the right policies to the instance role, apply the right tags, and add
        the required user data to the instance's launch configuration.

        Spot instances will be labeled ``lifecycle=Ec2Spot`` and tainted with ``PreferNoSchedule``.
        If kubectl is enabled, the
        `spot interrupt handler <https://github.com/awslabs/ec2-spot-labs/tree/master/ec2-spot-eks-solution/spot-termination-handler>`_
        daemon will be installed on all spot instances to handle
        `EC2 Spot Instance Termination Notices <https://aws.amazon.com/blogs/aws/new-ec2-spot-instance-termination-notices/>`_.

        Prefer to use ``addCapacity`` if possible.

        :param auto_scaling_group: [disable-awslint:ref-via-interface].
        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: Allows options for node bootstrapping through EC2 user data. Default: - default options
        :param machine_image_type: Allow options to specify different machine image type. Default: MachineImageType.AMAZON_LINUX_2
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/launch-workers.html
        stability
        :stability: experimental
        """
        options = AutoScalingGroupOptions(
            bootstrap_enabled=bootstrap_enabled,
            bootstrap_options=bootstrap_options,
            machine_image_type=machine_image_type,
            map_role=map_role,
        )

        return jsii.invoke(self, "addAutoScalingGroup", [auto_scaling_group, options])

    @jsii.member(jsii_name="addCapacity")
    def add_capacity(
        self,
        id: str,
        *,
        instance_type: _InstanceType_85a97b30,
        bootstrap_enabled: typing.Optional[bool] = None,
        bootstrap_options: typing.Optional["BootstrapOptions"] = None,
        machine_image_type: typing.Optional["MachineImageType"] = None,
        map_role: typing.Optional[bool] = None,
        allow_all_outbound: typing.Optional[bool] = None,
        associate_public_ip_address: typing.Optional[bool] = None,
        auto_scaling_group_name: typing.Optional[str] = None,
        block_devices: typing.Optional[typing.List[_BlockDevice_6b64cf0c]] = None,
        cooldown: typing.Optional[_Duration_5170c158] = None,
        desired_capacity: typing.Optional[jsii.Number] = None,
        group_metrics: typing.Optional[typing.List[_GroupMetrics_8f5d7498]] = None,
        health_check: typing.Optional[_HealthCheck_ed599e14] = None,
        ignore_unmodified_size_properties: typing.Optional[bool] = None,
        instance_monitoring: typing.Optional[_Monitoring_11cb7f01] = None,
        key_name: typing.Optional[str] = None,
        max_capacity: typing.Optional[jsii.Number] = None,
        max_instance_lifetime: typing.Optional[_Duration_5170c158] = None,
        min_capacity: typing.Optional[jsii.Number] = None,
        notifications: typing.Optional[typing.List[_NotificationConfiguration_396b88c6]] = None,
        notifications_topic: typing.Optional[_ITopic_ef0ebe0e] = None,
        replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number] = None,
        resource_signal_count: typing.Optional[jsii.Number] = None,
        resource_signal_timeout: typing.Optional[_Duration_5170c158] = None,
        rolling_update_configuration: typing.Optional[_RollingUpdateConfiguration_c96dd49e] = None,
        spot_price: typing.Optional[str] = None,
        update_type: typing.Optional[_UpdateType_7a2ac17e] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> _AutoScalingGroup_003d0b84:
        """Add nodes to this EKS cluster.

        The nodes will automatically be configured with the right VPC and AMI
        for the instance type and Kubernetes version.

        Note that if you specify ``updateType: RollingUpdate`` or ``updateType: ReplacingUpdate``, your nodes might be replaced at deploy
        time without notice in case the recommended AMI for your machine image type has been updated by AWS.
        The default behavior for ``updateType`` is ``None``, which means only new instances will be launched using the new AMI.

        Spot instances will be labeled ``lifecycle=Ec2Spot`` and tainted with ``PreferNoSchedule``.
        In addition, the `spot interrupt handler <https://github.com/awslabs/ec2-spot-labs/tree/master/ec2-spot-eks-solution/spot-termination-handler>`_
        daemon will be installed on all spot instances to handle
        `EC2 Spot Instance Termination Notices <https://aws.amazon.com/blogs/aws/new-ec2-spot-instance-termination-notices/>`_.

        :param id: -
        :param instance_type: Instance type of the instances to start.
        :param bootstrap_enabled: Configures the EC2 user-data script for instances in this autoscaling group to bootstrap the node (invoke ``/etc/eks/bootstrap.sh``) and associate it with the EKS cluster. If you wish to provide a custom user data script, set this to ``false`` and manually invoke ``autoscalingGroup.addUserData()``. Default: true
        :param bootstrap_options: EKS node bootstrapping options. Default: - none
        :param machine_image_type: Machine image type. Default: MachineImageType.AMAZON_LINUX_2
        :param map_role: Will automatically update the aws-auth ConfigMap to map the IAM instance role to RBAC. This cannot be explicitly set to ``true`` if the cluster has kubectl disabled. Default: - true if the cluster has kubectl enabled (which is the default).
        :param allow_all_outbound: Whether the instances can initiate connections to anywhere by default. Default: true
        :param associate_public_ip_address: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
        :param auto_scaling_group_name: The name of the Auto Scaling group. This name must be unique per Region per account. Default: - Auto generated by CloudFormation
        :param block_devices: Specifies how block devices are exposed to the instance. You can specify virtual devices and EBS volumes. Each instance that is launched has an associated root device volume, either an Amazon EBS volume or an instance store volume. You can use block device mappings to specify additional EBS volumes or instance store volumes to attach to an instance when it is launched. Default: - Uses the block device mapping of the AMI
        :param cooldown: Default scaling cooldown for this AutoScalingGroup. Default: Duration.minutes(5)
        :param desired_capacity: Initial amount of instances in the fleet. If this is set to a number, every deployment will reset the amount of instances to this number. It is recommended to leave this value blank. Default: minCapacity, and leave unchanged during deployment
        :param group_metrics: Enable monitoring for group metrics, these metrics describe the group rather than any of its instances. To report all group metrics use ``GroupMetrics.all()`` Group metrics are reported in a granularity of 1 minute at no additional charge. Default: - no group metrics will be reported
        :param health_check: Configuration for health checks. Default: - HealthCheck.ec2 with no grace period
        :param ignore_unmodified_size_properties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
        :param instance_monitoring: Controls whether instances in this group are launched with detailed or basic monitoring. When detailed monitoring is enabled, Amazon CloudWatch generates metrics every minute and your account is charged a fee. When you disable detailed monitoring, CloudWatch generates metrics every 5 minutes. Default: - Monitoring.DETAILED
        :param key_name: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
        :param max_capacity: Maximum number of instances in the fleet. Default: desiredCapacity
        :param max_instance_lifetime: The maximum amount of time that an instance can be in service. The maximum duration applies to all current and future instances in the group. As an instance approaches its maximum duration, it is terminated and replaced, and cannot be used again. You must specify a value of at least 604,800 seconds (7 days). To clear a previously set value, leave this property undefined. Default: none
        :param min_capacity: Minimum number of instances in the fleet. Default: 1
        :param notifications: Configure autoscaling group to send notifications about fleet changes to an SNS topic(s). Default: - No fleet change notifications will be sent.
        :param notifications_topic: SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
        :param replacing_update_min_successful_instances_percent: Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
        :param resource_signal_count: How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1
        :param resource_signal_timeout: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: Duration.minutes(5)
        :param rolling_update_configuration: Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
        :param spot_price: The maximum hourly price (in USD) to be paid for any Spot Instance launched to fulfill the request. Spot Instances are launched when the price you specify exceeds the current Spot market price. Default: none
        :param update_type: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
        :param vpc_subnets: Where to place instances within the VPC. Default: - All Private subnets.

        stability
        :stability: experimental
        """
        options = CapacityOptions(
            instance_type=instance_type,
            bootstrap_enabled=bootstrap_enabled,
            bootstrap_options=bootstrap_options,
            machine_image_type=machine_image_type,
            map_role=map_role,
            allow_all_outbound=allow_all_outbound,
            associate_public_ip_address=associate_public_ip_address,
            auto_scaling_group_name=auto_scaling_group_name,
            block_devices=block_devices,
            cooldown=cooldown,
            desired_capacity=desired_capacity,
            group_metrics=group_metrics,
            health_check=health_check,
            ignore_unmodified_size_properties=ignore_unmodified_size_properties,
            instance_monitoring=instance_monitoring,
            key_name=key_name,
            max_capacity=max_capacity,
            max_instance_lifetime=max_instance_lifetime,
            min_capacity=min_capacity,
            notifications=notifications,
            notifications_topic=notifications_topic,
            replacing_update_min_successful_instances_percent=replacing_update_min_successful_instances_percent,
            resource_signal_count=resource_signal_count,
            resource_signal_timeout=resource_signal_timeout,
            rolling_update_configuration=rolling_update_configuration,
            spot_price=spot_price,
            update_type=update_type,
            vpc_subnets=vpc_subnets,
        )

        return jsii.invoke(self, "addCapacity", [id, options])

    @jsii.member(jsii_name="addChart")
    def add_chart(
        self,
        id: str,
        *,
        chart: str,
        create_namespace: typing.Optional[bool] = None,
        namespace: typing.Optional[str] = None,
        release: typing.Optional[str] = None,
        repository: typing.Optional[str] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        values: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        version: typing.Optional[str] = None,
        wait: typing.Optional[bool] = None,
    ) -> "HelmChart":
        """Defines a Helm chart in this cluster.

        :param id: logical id of this chart.
        :param chart: The name of the chart.
        :param create_namespace: create namespace if not exist. Default: true
        :param namespace: The Kubernetes namespace scope of the requests. Default: default
        :param release: The name of the release. Default: - If no release name is given, it will use the last 53 characters of the node's unique id.
        :param repository: The repository which contains the chart. For example: https://kubernetes-charts.storage.googleapis.com/ Default: - No repository will be used, which means that the chart needs to be an absolute URL.
        :param timeout: Amount of time to wait for any individual Kubernetes operation. Maximum 15 minutes. Default: Duration.minutes(5)
        :param values: The values to be used by the chart. Default: - No values are provided to the chart.
        :param version: The chart version to install. Default: - If this is not specified, the latest version is installed
        :param wait: Whether or not Helm should wait until all Pods, PVCs, Services, and minimum number of Pods of a Deployment, StatefulSet, or ReplicaSet are in a ready state before marking the release as successful. Default: - Helm will not wait before marking release as successful

        return
        :return: a ``HelmChart`` construct

        stability
        :stability: experimental
        """
        options = HelmChartOptions(
            chart=chart,
            create_namespace=create_namespace,
            namespace=namespace,
            release=release,
            repository=repository,
            timeout=timeout,
            values=values,
            version=version,
            wait=wait,
        )

        return jsii.invoke(self, "addChart", [id, options])

    @jsii.member(jsii_name="addFargateProfile")
    def add_fargate_profile(
        self,
        id: str,
        *,
        selectors: typing.List["Selector"],
        fargate_profile_name: typing.Optional[str] = None,
        pod_execution_role: typing.Optional[_IRole_e69bbae4] = None,
        subnet_selection: typing.Optional[_SubnetSelection_36a13cd6] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
    ) -> "FargateProfile":
        """Adds a Fargate profile to this cluster.

        :param id: the id of this profile.
        :param selectors: The selectors to match for pods to use this Fargate profile. Each selector must have an associated namespace. Optionally, you can also specify labels for a namespace. At least one selector is required and you may specify up to five selectors.
        :param fargate_profile_name: The name of the Fargate profile. Default: - generated
        :param pod_execution_role: The pod execution role to use for pods that match the selectors in the Fargate profile. The pod execution role allows Fargate infrastructure to register with your cluster as a node, and it provides read access to Amazon ECR image repositories. Default: - a role will be automatically created
        :param subnet_selection: Select which subnets to launch your pods into. At this time, pods running on Fargate are not assigned public IP addresses, so only private subnets (with no direct route to an Internet Gateway) are allowed. Default: - all private subnets of the VPC are selected.
        :param vpc: The VPC from which to select subnets to launch your pods into. By default, all private subnets are selected. You can customize this using ``subnetSelection``. Default: - all private subnets used by theEKS cluster

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/fargate-profile.html
        stability
        :stability: experimental
        """
        options = FargateProfileOptions(
            selectors=selectors,
            fargate_profile_name=fargate_profile_name,
            pod_execution_role=pod_execution_role,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        return jsii.invoke(self, "addFargateProfile", [id, options])

    @jsii.member(jsii_name="addManifest")
    def add_manifest(self, id: str, *manifest: typing.Any) -> "KubernetesManifest":
        """Defines a Kubernetes resource in this cluster.

        The manifest will be applied/deleted using kubectl as needed.

        :param id: logical id of this manifest.
        :param manifest: a list of Kubernetes resource specifications.

        return
        :return: a ``KubernetesResource`` object.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addManifest", [id, *manifest])

    @jsii.member(jsii_name="addNodegroup")
    def add_nodegroup(
        self,
        id: str,
        *,
        ami_type: typing.Optional["NodegroupAmiType"] = None,
        desired_size: typing.Optional[jsii.Number] = None,
        disk_size: typing.Optional[jsii.Number] = None,
        force_update: typing.Optional[bool] = None,
        instance_type: typing.Optional[_InstanceType_85a97b30] = None,
        labels: typing.Optional[typing.Mapping[str, str]] = None,
        max_size: typing.Optional[jsii.Number] = None,
        min_size: typing.Optional[jsii.Number] = None,
        nodegroup_name: typing.Optional[str] = None,
        node_role: typing.Optional[_IRole_e69bbae4] = None,
        release_version: typing.Optional[str] = None,
        remote_access: typing.Optional["NodegroupRemoteAccess"] = None,
        subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        tags: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> "Nodegroup":
        """Add managed nodegroup to this Amazon EKS cluster.

        This method will create a new managed nodegroup and add into the capacity.

        :param id: The ID of the nodegroup.
        :param ami_type: The AMI type for your node group. Default: AL2_x86_64
        :param desired_size: The current number of worker nodes that the managed node group should maintain. If not specified, the nodewgroup will initially create ``minSize`` instances. Default: 2
        :param disk_size: The root device disk size (in GiB) for your node group instances. Default: 20
        :param force_update: Force the update if the existing node group's pods are unable to be drained due to a pod disruption budget issue. If an update fails because pods could not be drained, you can force the update after it fails to terminate the old node whether or not any pods are running on the node. Default: true
        :param instance_type: The instance type to use for your node group. Currently, you can specify a single instance type for a node group. The default value for this parameter is ``t3.medium``. If you choose a GPU instance type, be sure to specify the ``AL2_x86_64_GPU`` with the amiType parameter. Default: t3.medium
        :param labels: The Kubernetes labels to be applied to the nodes in the node group when they are created. Default: - None
        :param max_size: The maximum number of worker nodes that the managed node group can scale out to. Managed node groups can support up to 100 nodes by default. Default: - desiredSize
        :param min_size: The minimum number of worker nodes that the managed node group can scale in to. This number must be greater than zero. Default: 1
        :param nodegroup_name: Name of the Nodegroup. Default: - resource ID
        :param node_role: The IAM role to associate with your node group. The Amazon EKS worker node kubelet daemon makes calls to AWS APIs on your behalf. Worker nodes receive permissions for these API calls through an IAM instance profile and associated policies. Before you can launch worker nodes and register them into a cluster, you must create an IAM role for those worker nodes to use when they are launched. Default: - None. Auto-generated if not specified.
        :param release_version: The AMI version of the Amazon EKS-optimized AMI to use with your node group (for example, ``1.14.7-YYYYMMDD``). Default: - The latest available AMI version for the node group's current Kubernetes version is used.
        :param remote_access: The remote access (SSH) configuration to use with your node group. Disabled by default, however, if you specify an Amazon EC2 SSH key but do not specify a source security group when you create a managed node group, then port 22 on the worker nodes is opened to the internet (0.0.0.0/0) Default: - disabled
        :param subnets: The subnets to use for the Auto Scaling group that is created for your node group. By specifying the SubnetSelection, the selected subnets will automatically apply required tags i.e. ``kubernetes.io/cluster/CLUSTER_NAME`` with a value of ``shared``, where ``CLUSTER_NAME`` is replaced with the name of your cluster. Default: - private subnets
        :param tags: The metadata to apply to the node group to assist with categorization and organization. Each tag consists of a key and an optional value, both of which you define. Node group tags do not propagate to any other resources associated with the node group, such as the Amazon EC2 instances or subnets. Default: - None

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/managed-node-groups.html
        stability
        :stability: experimental
        """
        options = NodegroupOptions(
            ami_type=ami_type,
            desired_size=desired_size,
            disk_size=disk_size,
            force_update=force_update,
            instance_type=instance_type,
            labels=labels,
            max_size=max_size,
            min_size=min_size,
            nodegroup_name=nodegroup_name,
            node_role=node_role,
            release_version=release_version,
            remote_access=remote_access,
            subnets=subnets,
            tags=tags,
        )

        return jsii.invoke(self, "addNodegroup", [id, options])

    @jsii.member(jsii_name="addServiceAccount")
    def add_service_account(
        self,
        id: str,
        *,
        name: typing.Optional[str] = None,
        namespace: typing.Optional[str] = None,
    ) -> "ServiceAccount":
        """Adds a service account to this cluster.

        :param id: the id of this service account.
        :param name: The name of the service account. Default: - If no name is given, it will use the id of the resource.
        :param namespace: The namespace of the service account. Default: "default"

        stability
        :stability: experimental
        """
        options = ServiceAccountOptions(name=name, namespace=namespace)

        return jsii.invoke(self, "addServiceAccount", [id, options])

    @jsii.member(jsii_name="getServiceLoadBalancerAddress")
    def get_service_load_balancer_address(
        self,
        service_name: str,
        *,
        namespace: typing.Optional[str] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
    ) -> str:
        """Fetch the load balancer address of a service of type 'LoadBalancer'.

        :param service_name: The name of the service.
        :param namespace: The namespace the service belongs to. Default: 'default'
        :param timeout: Timeout for waiting on the load balancer address. Default: Duration.minutes(5)

        stability
        :stability: experimental
        """
        options = ServiceLoadBalancerAddressOptions(
            namespace=namespace, timeout=timeout
        )

        return jsii.invoke(self, "getServiceLoadBalancerAddress", [service_name, options])

    @builtins.property
    @jsii.member(jsii_name="adminRole")
    def admin_role(self) -> _Role_6f613128:
        """An IAM role with administrative permissions to create or update the cluster.

        This role also has ``systems:master`` permissions.

        stability
        :stability: experimental
        """
        return jsii.get(self, "adminRole")

    @builtins.property
    @jsii.member(jsii_name="awsAuth")
    def aws_auth(self) -> "AwsAuth":
        """Lazily creates the AwsAuth resource, which manages AWS authentication mapping.

        stability
        :stability: experimental
        """
        return jsii.get(self, "awsAuth")

    @builtins.property
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """The AWS generated ARN for the Cluster resource.

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            arn:aws:eks:us-west-2666666666666cluster / prod
        """
        return jsii.get(self, "clusterArn")

    @builtins.property
    @jsii.member(jsii_name="clusterCertificateAuthorityData")
    def cluster_certificate_authority_data(self) -> str:
        """The certificate-authority-data for your cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterCertificateAuthorityData")

    @builtins.property
    @jsii.member(jsii_name="clusterEncryptionConfigKeyArn")
    def cluster_encryption_config_key_arn(self) -> str:
        """Amazon Resource Name (ARN) or alias of the customer master key (CMK).

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterEncryptionConfigKeyArn")

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> str:
        """The endpoint URL for the Cluster.

        This is the URL inside the kubeconfig file to use with kubectl

        stability
        :stability: experimental

        Example::

            # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
            https:
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        """The Name of the created EKS Cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterName")

    @builtins.property
    @jsii.member(jsii_name="clusterOpenIdConnectIssuer")
    def cluster_open_id_connect_issuer(self) -> str:
        """If this cluster is kubectl-enabled, returns the OpenID Connect issuer.

        This is because the values is only be retrieved by the API and not exposed
        by CloudFormation. If this cluster is not kubectl-enabled (i.e. uses the
        stock ``CfnCluster``), this is ``undefined``.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterOpenIdConnectIssuer")

    @builtins.property
    @jsii.member(jsii_name="clusterOpenIdConnectIssuerUrl")
    def cluster_open_id_connect_issuer_url(self) -> str:
        """If this cluster is kubectl-enabled, returns the OpenID Connect issuer url.

        This is because the values is only be retrieved by the API and not exposed
        by CloudFormation. If this cluster is not kubectl-enabled (i.e. uses the
        stock ``CfnCluster``), this is ``undefined``.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "clusterOpenIdConnectIssuerUrl")

    @builtins.property
    @jsii.member(jsii_name="clusterSecurityGroupId")
    def cluster_security_group_id(self) -> str:
        """The cluster security group that was created by Amazon EKS for the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterSecurityGroupId")

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Manages connection rules (Security Group Rules) for the cluster.

        stability
        :stability: experimental
        memberof:
        :memberof:: Cluster
        type:
        :type:: {ec2.Connections}
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProvider")
    def open_id_connect_provider(self) -> _OpenIdConnectProvider_36010b0a:
        """An ``OpenIdConnectProvider`` resource associated with this cluster, and which can be used to link this cluster to AWS IAM.

        A provider will only be defined if this property is accessed (lazy initialization).

        stability
        :stability: experimental
        """
        return jsii.get(self, "openIdConnectProvider")

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> _IRole_e69bbae4:
        """IAM role assumed by the EKS Control Plane.

        stability
        :stability: experimental
        """
        return jsii.get(self, "role")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC in which this Cluster was created.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")

    @builtins.property
    @jsii.member(jsii_name="defaultCapacity")
    def default_capacity(self) -> typing.Optional[_AutoScalingGroup_003d0b84]:
        """The auto scaling group that hosts the default capacity for this cluster.

        This will be ``undefined`` if the ``defaultCapacityType`` is not ``EC2`` or
        ``defaultCapacityType`` is ``EC2`` but default capacity is set to 0.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultCapacity")

    @builtins.property
    @jsii.member(jsii_name="defaultNodegroup")
    def default_nodegroup(self) -> typing.Optional["Nodegroup"]:
        """The node group that hosts the default capacity for this cluster.

        This will be ``undefined`` if the ``defaultCapacityType`` is ``EC2`` or
        ``defaultCapacityType`` is ``NODEGROUP`` but default capacity is set to 0.

        stability
        :stability: experimental
        """
        return jsii.get(self, "defaultNodegroup")

    @builtins.property
    @jsii.member(jsii_name="kubectlEnvironment")
    def kubectl_environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Custom environment variables when running ``kubectl`` against this cluster.

        default
        :default: - no additional environment variables

        stability
        :stability: experimental
        """
        return jsii.get(self, "kubectlEnvironment")

    @builtins.property
    @jsii.member(jsii_name="kubectlLayer")
    def kubectl_layer(self) -> typing.Optional[_ILayerVersion_aa5e0c0c]:
        """The AWS Lambda layer that contains ``kubectl``, ``helm`` and the AWS CLI.

        If
        undefined, a SAR app that contains this layer will be used.

        stability
        :stability: experimental
        """
        return jsii.get(self, "kubectlLayer")

    @builtins.property
    @jsii.member(jsii_name="kubectlPrivateSubnets")
    def kubectl_private_subnets(
        self,
    ) -> typing.Optional[typing.List[_ISubnet_7f5367e6]]:
        """Subnets to host the ``kubectl`` compute resources.

        default
        :default:

        - If not specified, the k8s endpoint is expected to be accessible
          publicly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "kubectlPrivateSubnets")

    @builtins.property
    @jsii.member(jsii_name="kubectlRole")
    def kubectl_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """An IAM role that can perform kubectl operations against this cluster.

        The role should be mapped to the ``system:masters`` Kubernetes RBAC role.

        stability
        :stability: experimental
        """
        return jsii.get(self, "kubectlRole")

    @builtins.property
    @jsii.member(jsii_name="kubectlSecurityGroup")
    def kubectl_security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """A security group to use for ``kubectl`` execution.

        default
        :default:

        - If not specified, the k8s endpoint is expected to be accessible
          publicly.

        stability
        :stability: experimental
        """
        return jsii.get(self, "kubectlSecurityGroup")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.ClusterOptions",
    jsii_struct_bases=[CommonClusterOptions],
    name_mapping={
        "version": "version",
        "cluster_name": "clusterName",
        "output_cluster_name": "outputClusterName",
        "output_config_command": "outputConfigCommand",
        "role": "role",
        "security_group": "securityGroup",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "core_dns_compute_type": "coreDnsComputeType",
        "endpoint_access": "endpointAccess",
        "kubectl_environment": "kubectlEnvironment",
        "kubectl_layer": "kubectlLayer",
        "masters_role": "mastersRole",
        "output_masters_role_arn": "outputMastersRoleArn",
    },
)
class ClusterOptions(CommonClusterOptions):
    def __init__(
        self,
        *,
        version: "KubernetesVersion",
        cluster_name: typing.Optional[str] = None,
        output_cluster_name: typing.Optional[bool] = None,
        output_config_command: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_group: typing.Optional[_ISecurityGroup_d72ab8e8] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
        vpc_subnets: typing.Optional[typing.List[_SubnetSelection_36a13cd6]] = None,
        core_dns_compute_type: typing.Optional["CoreDnsComputeType"] = None,
        endpoint_access: typing.Optional["EndpointAccess"] = None,
        kubectl_environment: typing.Optional[typing.Mapping[str, str]] = None,
        kubectl_layer: typing.Optional[_ILayerVersion_aa5e0c0c] = None,
        masters_role: typing.Optional[_IRole_e69bbae4] = None,
        output_masters_role_arn: typing.Optional[bool] = None,
    ) -> None:
        """Options for EKS clusters.

        :param version: The Kubernetes version to run in the cluster.
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets
        :param core_dns_compute_type: Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param endpoint_access: Configure access to the Kubernetes API server endpoint.. Default: EndpointAccess.PUBLIC_AND_PRIVATE
        :param kubectl_environment: Environment variables for the kubectl execution. Only relevant for kubectl enabled clusters. Default: - No environment variables.
        :param kubectl_layer: An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI. By default, the provider will use the layer included in the "aws-lambda-layer-kubectl" SAR application which is available in all commercial regions. To deploy the layer locally, visit https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md for instructions on how to prepare the .zip file and then define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'kubectl-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`)), compatibleRuntimes: [lambda.Runtime.PROVIDED] }) Default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - a role that assumable by anyone with permissions in the same account will automatically be defined
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if output_cluster_name is not None:
            self._values["output_cluster_name"] = output_cluster_name
        if output_config_command is not None:
            self._values["output_config_command"] = output_config_command
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if core_dns_compute_type is not None:
            self._values["core_dns_compute_type"] = core_dns_compute_type
        if endpoint_access is not None:
            self._values["endpoint_access"] = endpoint_access
        if kubectl_environment is not None:
            self._values["kubectl_environment"] = kubectl_environment
        if kubectl_layer is not None:
            self._values["kubectl_layer"] = kubectl_layer
        if masters_role is not None:
            self._values["masters_role"] = masters_role
        if output_masters_role_arn is not None:
            self._values["output_masters_role_arn"] = output_masters_role_arn

    @builtins.property
    def version(self) -> "KubernetesVersion":
        """The Kubernetes version to run in the cluster.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """Name for the cluster.

        default
        :default: - Automatically generated name

        stability
        :stability: experimental
        """
        return self._values.get("cluster_name")

    @builtins.property
    def output_cluster_name(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the name of the cluster will be synthesized.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("output_cluster_name")

    @builtins.property
    def output_config_command(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized.

        This command will include
        the cluster name and, if applicable, the ARN of the masters IAM role.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("output_config_command")

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get("role")

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """Security Group to use for Control Plane ENIs.

        default
        :default: - A security group is automatically created

        stability
        :stability: experimental
        """
        return self._values.get("security_group")

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC in which to create the Cluster.

        default
        :default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[typing.List[_SubnetSelection_36a13cd6]]:
        """Where to place EKS Control Plane ENIs.

        If you want to create public load balancers, this must include public subnets.

        For example, to only select private subnets, supply the following::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           vpcSubnets: [
              { subnetType: ec2.SubnetType.Private }
           ]

        default
        :default: - All public and private subnets

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    @builtins.property
    def core_dns_compute_type(self) -> typing.Optional["CoreDnsComputeType"]:
        """Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS.

        default
        :default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)

        stability
        :stability: experimental
        """
        return self._values.get("core_dns_compute_type")

    @builtins.property
    def endpoint_access(self) -> typing.Optional["EndpointAccess"]:
        """Configure access to the Kubernetes API server endpoint..

        default
        :default: EndpointAccess.PUBLIC_AND_PRIVATE

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html
        stability
        :stability: experimental
        """
        return self._values.get("endpoint_access")

    @builtins.property
    def kubectl_environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Environment variables for the kubectl execution.

        Only relevant for kubectl enabled clusters.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get("kubectl_environment")

    @builtins.property
    def kubectl_layer(self) -> typing.Optional[_ILayerVersion_aa5e0c0c]:
        """An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI.

        By default, the provider will use the layer included in the
        "aws-lambda-layer-kubectl" SAR application which is available in all
        commercial regions.

        To deploy the layer locally, visit
        https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md
        for instructions on how to prepare the .zip file and then define it in your
        app as follows::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           layer = lambda_.LayerVersion(self, "kubectl-layer",
               code=lambda_.Code.from_asset(f"{__dirname}/layer.zip")
           )
           compatible_runtimes =

        default
        :default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.

        see
        :see: https://github.com/aws-samples/aws-lambda-layer-kubectl
        stability
        :stability: experimental
        """
        return self._values.get("kubectl_layer")

    @builtins.property
    def masters_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group.

        default
        :default:

        - a role that assumable by anyone with permissions in the same
          account will automatically be defined

        see
        :see: https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings
        stability
        :stability: experimental
        """
        return self._values.get("masters_role")

    @builtins.property
    def output_masters_role_arn(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified).

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("output_masters_role_arn")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.ClusterProps",
    jsii_struct_bases=[ClusterOptions],
    name_mapping={
        "version": "version",
        "cluster_name": "clusterName",
        "output_cluster_name": "outputClusterName",
        "output_config_command": "outputConfigCommand",
        "role": "role",
        "security_group": "securityGroup",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "core_dns_compute_type": "coreDnsComputeType",
        "endpoint_access": "endpointAccess",
        "kubectl_environment": "kubectlEnvironment",
        "kubectl_layer": "kubectlLayer",
        "masters_role": "mastersRole",
        "output_masters_role_arn": "outputMastersRoleArn",
        "default_capacity": "defaultCapacity",
        "default_capacity_instance": "defaultCapacityInstance",
        "default_capacity_type": "defaultCapacityType",
        "kubectl_enabled": "kubectlEnabled",
        "secrets_encryption_key": "secretsEncryptionKey",
    },
)
class ClusterProps(ClusterOptions):
    def __init__(
        self,
        *,
        version: "KubernetesVersion",
        cluster_name: typing.Optional[str] = None,
        output_cluster_name: typing.Optional[bool] = None,
        output_config_command: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_group: typing.Optional[_ISecurityGroup_d72ab8e8] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
        vpc_subnets: typing.Optional[typing.List[_SubnetSelection_36a13cd6]] = None,
        core_dns_compute_type: typing.Optional["CoreDnsComputeType"] = None,
        endpoint_access: typing.Optional["EndpointAccess"] = None,
        kubectl_environment: typing.Optional[typing.Mapping[str, str]] = None,
        kubectl_layer: typing.Optional[_ILayerVersion_aa5e0c0c] = None,
        masters_role: typing.Optional[_IRole_e69bbae4] = None,
        output_masters_role_arn: typing.Optional[bool] = None,
        default_capacity: typing.Optional[jsii.Number] = None,
        default_capacity_instance: typing.Optional[_InstanceType_85a97b30] = None,
        default_capacity_type: typing.Optional["DefaultCapacityType"] = None,
        kubectl_enabled: typing.Optional[bool] = None,
        secrets_encryption_key: typing.Optional[_IKey_3336c79d] = None,
    ) -> None:
        """Common configuration props for EKS clusters.

        :param version: The Kubernetes version to run in the cluster.
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets
        :param core_dns_compute_type: Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param endpoint_access: Configure access to the Kubernetes API server endpoint.. Default: EndpointAccess.PUBLIC_AND_PRIVATE
        :param kubectl_environment: Environment variables for the kubectl execution. Only relevant for kubectl enabled clusters. Default: - No environment variables.
        :param kubectl_layer: An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI. By default, the provider will use the layer included in the "aws-lambda-layer-kubectl" SAR application which is available in all commercial regions. To deploy the layer locally, visit https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md for instructions on how to prepare the .zip file and then define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'kubectl-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`)), compatibleRuntimes: [lambda.Runtime.PROVIDED] }) Default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - a role that assumable by anyone with permissions in the same account will automatically be defined
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param default_capacity: Number of instances to allocate as an initial capacity for this cluster. Instance type can be configured through ``defaultCapacityInstanceType``, which defaults to ``m5.large``. Use ``cluster.addCapacity`` to add additional customized capacity. Set this to ``0`` is you wish to avoid the initial capacity allocation. Default: 2
        :param default_capacity_instance: The instance type to use for the default capacity. This will only be taken into account if ``defaultCapacity`` is > 0. Default: m5.large
        :param default_capacity_type: The default capacity type for the cluster. Default: NODEGROUP
        :param kubectl_enabled: NOT SUPPORTED: We no longer allow disabling kubectl-support. Setting this option to ``false`` will throw an error. To temporary allow you to retain existing clusters created with ``kubectlEnabled: false``, you can use ``eks.LegacyCluster`` class, which is a drop-in replacement for ``eks.Cluster`` with ``kubectlEnabled: false``. Bear in mind that this is a temporary workaround. We have plans to remove ``eks.LegacyCluster``. If you have a use case for using ``eks.LegacyCluster``, please add a comment here https://github.com/aws/aws-cdk/issues/9332 and let us know so we can make sure to continue to support your use case with ``eks.Cluster``. This issue also includes additional context into why this class is being removed. Default: true
        :param secrets_encryption_key: KMS secret for envelope encryption for Kubernetes secrets. Default: - By default, Kubernetes stores all secret object data within etcd and all etcd volumes used by Amazon EKS are encrypted at the disk-level using AWS-Managed encryption keys.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if output_cluster_name is not None:
            self._values["output_cluster_name"] = output_cluster_name
        if output_config_command is not None:
            self._values["output_config_command"] = output_config_command
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if core_dns_compute_type is not None:
            self._values["core_dns_compute_type"] = core_dns_compute_type
        if endpoint_access is not None:
            self._values["endpoint_access"] = endpoint_access
        if kubectl_environment is not None:
            self._values["kubectl_environment"] = kubectl_environment
        if kubectl_layer is not None:
            self._values["kubectl_layer"] = kubectl_layer
        if masters_role is not None:
            self._values["masters_role"] = masters_role
        if output_masters_role_arn is not None:
            self._values["output_masters_role_arn"] = output_masters_role_arn
        if default_capacity is not None:
            self._values["default_capacity"] = default_capacity
        if default_capacity_instance is not None:
            self._values["default_capacity_instance"] = default_capacity_instance
        if default_capacity_type is not None:
            self._values["default_capacity_type"] = default_capacity_type
        if kubectl_enabled is not None:
            self._values["kubectl_enabled"] = kubectl_enabled
        if secrets_encryption_key is not None:
            self._values["secrets_encryption_key"] = secrets_encryption_key

    @builtins.property
    def version(self) -> "KubernetesVersion":
        """The Kubernetes version to run in the cluster.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """Name for the cluster.

        default
        :default: - Automatically generated name

        stability
        :stability: experimental
        """
        return self._values.get("cluster_name")

    @builtins.property
    def output_cluster_name(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the name of the cluster will be synthesized.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("output_cluster_name")

    @builtins.property
    def output_config_command(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized.

        This command will include
        the cluster name and, if applicable, the ARN of the masters IAM role.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("output_config_command")

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get("role")

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """Security Group to use for Control Plane ENIs.

        default
        :default: - A security group is automatically created

        stability
        :stability: experimental
        """
        return self._values.get("security_group")

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC in which to create the Cluster.

        default
        :default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[typing.List[_SubnetSelection_36a13cd6]]:
        """Where to place EKS Control Plane ENIs.

        If you want to create public load balancers, this must include public subnets.

        For example, to only select private subnets, supply the following::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           vpcSubnets: [
              { subnetType: ec2.SubnetType.Private }
           ]

        default
        :default: - All public and private subnets

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    @builtins.property
    def core_dns_compute_type(self) -> typing.Optional["CoreDnsComputeType"]:
        """Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS.

        default
        :default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)

        stability
        :stability: experimental
        """
        return self._values.get("core_dns_compute_type")

    @builtins.property
    def endpoint_access(self) -> typing.Optional["EndpointAccess"]:
        """Configure access to the Kubernetes API server endpoint..

        default
        :default: EndpointAccess.PUBLIC_AND_PRIVATE

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html
        stability
        :stability: experimental
        """
        return self._values.get("endpoint_access")

    @builtins.property
    def kubectl_environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Environment variables for the kubectl execution.

        Only relevant for kubectl enabled clusters.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get("kubectl_environment")

    @builtins.property
    def kubectl_layer(self) -> typing.Optional[_ILayerVersion_aa5e0c0c]:
        """An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI.

        By default, the provider will use the layer included in the
        "aws-lambda-layer-kubectl" SAR application which is available in all
        commercial regions.

        To deploy the layer locally, visit
        https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md
        for instructions on how to prepare the .zip file and then define it in your
        app as follows::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           layer = lambda_.LayerVersion(self, "kubectl-layer",
               code=lambda_.Code.from_asset(f"{__dirname}/layer.zip")
           )
           compatible_runtimes =

        default
        :default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.

        see
        :see: https://github.com/aws-samples/aws-lambda-layer-kubectl
        stability
        :stability: experimental
        """
        return self._values.get("kubectl_layer")

    @builtins.property
    def masters_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group.

        default
        :default:

        - a role that assumable by anyone with permissions in the same
          account will automatically be defined

        see
        :see: https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings
        stability
        :stability: experimental
        """
        return self._values.get("masters_role")

    @builtins.property
    def output_masters_role_arn(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified).

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("output_masters_role_arn")

    @builtins.property
    def default_capacity(self) -> typing.Optional[jsii.Number]:
        """Number of instances to allocate as an initial capacity for this cluster.

        Instance type can be configured through ``defaultCapacityInstanceType``,
        which defaults to ``m5.large``.

        Use ``cluster.addCapacity`` to add additional customized capacity. Set this
        to ``0`` is you wish to avoid the initial capacity allocation.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get("default_capacity")

    @builtins.property
    def default_capacity_instance(self) -> typing.Optional[_InstanceType_85a97b30]:
        """The instance type to use for the default capacity.

        This will only be taken
        into account if ``defaultCapacity`` is > 0.

        default
        :default: m5.large

        stability
        :stability: experimental
        """
        return self._values.get("default_capacity_instance")

    @builtins.property
    def default_capacity_type(self) -> typing.Optional["DefaultCapacityType"]:
        """The default capacity type for the cluster.

        default
        :default: NODEGROUP

        stability
        :stability: experimental
        """
        return self._values.get("default_capacity_type")

    @builtins.property
    def kubectl_enabled(self) -> typing.Optional[bool]:
        """NOT SUPPORTED: We no longer allow disabling kubectl-support. Setting this option to ``false`` will throw an error.

        To temporary allow you to retain existing clusters created with
        ``kubectlEnabled: false``, you can use ``eks.LegacyCluster`` class, which is a
        drop-in replacement for ``eks.Cluster`` with ``kubectlEnabled: false``.

        Bear in mind that this is a temporary workaround. We have plans to remove
        ``eks.LegacyCluster``. If you have a use case for using ``eks.LegacyCluster``,
        please add a comment here https://github.com/aws/aws-cdk/issues/9332 and
        let us know so we can make sure to continue to support your use case with
        ``eks.Cluster``. This issue also includes additional context into why this
        class is being removed.

        default
        :default: true

        deprecated
        :deprecated:

        ``eks.LegacyCluster`` is **temporarily** provided as a drop-in
        replacement until you are able to migrate to ``eks.Cluster``.

        see
        :see: https://github.com/aws/aws-cdk/issues/9332
        stability
        :stability: deprecated
        """
        return self._values.get("kubectl_enabled")

    @builtins.property
    def secrets_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """KMS secret for envelope encryption for Kubernetes secrets.

        default
        :default:

        - By default, Kubernetes stores all secret object data within etcd and
          all etcd volumes used by Amazon EKS are encrypted at the disk-level
          using AWS-Managed encryption keys.

        stability
        :stability: experimental
        """
        return self._values.get("secrets_encryption_key")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FargateCluster(
    Cluster,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_eks.FargateCluster",
):
    """Defines an EKS cluster that runs entirely on AWS Fargate.

    The cluster is created with a default Fargate Profile that matches the
    "default" and "kube-system" namespaces. You can add additional profiles using
    ``addFargateProfile``.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        default_profile: typing.Optional["FargateProfileOptions"] = None,
        core_dns_compute_type: typing.Optional["CoreDnsComputeType"] = None,
        endpoint_access: typing.Optional["EndpointAccess"] = None,
        kubectl_environment: typing.Optional[typing.Mapping[str, str]] = None,
        kubectl_layer: typing.Optional[_ILayerVersion_aa5e0c0c] = None,
        masters_role: typing.Optional[_IRole_e69bbae4] = None,
        output_masters_role_arn: typing.Optional[bool] = None,
        version: "KubernetesVersion",
        cluster_name: typing.Optional[str] = None,
        output_cluster_name: typing.Optional[bool] = None,
        output_config_command: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_group: typing.Optional[_ISecurityGroup_d72ab8e8] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
        vpc_subnets: typing.Optional[typing.List[_SubnetSelection_36a13cd6]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param default_profile: Fargate Profile to create along with the cluster. Default: - A profile called "default" with 'default' and 'kube-system' selectors will be created if this is left undefined.
        :param core_dns_compute_type: Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param endpoint_access: Configure access to the Kubernetes API server endpoint.. Default: EndpointAccess.PUBLIC_AND_PRIVATE
        :param kubectl_environment: Environment variables for the kubectl execution. Only relevant for kubectl enabled clusters. Default: - No environment variables.
        :param kubectl_layer: An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI. By default, the provider will use the layer included in the "aws-lambda-layer-kubectl" SAR application which is available in all commercial regions. To deploy the layer locally, visit https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md for instructions on how to prepare the .zip file and then define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'kubectl-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`)), compatibleRuntimes: [lambda.Runtime.PROVIDED] }) Default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - a role that assumable by anyone with permissions in the same account will automatically be defined
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param version: The Kubernetes version to run in the cluster.
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets

        stability
        :stability: experimental
        """
        props = FargateClusterProps(
            default_profile=default_profile,
            core_dns_compute_type=core_dns_compute_type,
            endpoint_access=endpoint_access,
            kubectl_environment=kubectl_environment,
            kubectl_layer=kubectl_layer,
            masters_role=masters_role,
            output_masters_role_arn=output_masters_role_arn,
            version=version,
            cluster_name=cluster_name,
            output_cluster_name=output_cluster_name,
            output_config_command=output_config_command,
            role=role,
            security_group=security_group,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(FargateCluster, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_eks.FargateClusterProps",
    jsii_struct_bases=[ClusterOptions],
    name_mapping={
        "version": "version",
        "cluster_name": "clusterName",
        "output_cluster_name": "outputClusterName",
        "output_config_command": "outputConfigCommand",
        "role": "role",
        "security_group": "securityGroup",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "core_dns_compute_type": "coreDnsComputeType",
        "endpoint_access": "endpointAccess",
        "kubectl_environment": "kubectlEnvironment",
        "kubectl_layer": "kubectlLayer",
        "masters_role": "mastersRole",
        "output_masters_role_arn": "outputMastersRoleArn",
        "default_profile": "defaultProfile",
    },
)
class FargateClusterProps(ClusterOptions):
    def __init__(
        self,
        *,
        version: "KubernetesVersion",
        cluster_name: typing.Optional[str] = None,
        output_cluster_name: typing.Optional[bool] = None,
        output_config_command: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_group: typing.Optional[_ISecurityGroup_d72ab8e8] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
        vpc_subnets: typing.Optional[typing.List[_SubnetSelection_36a13cd6]] = None,
        core_dns_compute_type: typing.Optional["CoreDnsComputeType"] = None,
        endpoint_access: typing.Optional["EndpointAccess"] = None,
        kubectl_environment: typing.Optional[typing.Mapping[str, str]] = None,
        kubectl_layer: typing.Optional[_ILayerVersion_aa5e0c0c] = None,
        masters_role: typing.Optional[_IRole_e69bbae4] = None,
        output_masters_role_arn: typing.Optional[bool] = None,
        default_profile: typing.Optional["FargateProfileOptions"] = None,
    ) -> None:
        """Configuration props for EKS Fargate.

        :param version: The Kubernetes version to run in the cluster.
        :param cluster_name: Name for the cluster. Default: - Automatically generated name
        :param output_cluster_name: Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param role: Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param vpc: The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets
        :param core_dns_compute_type: Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param endpoint_access: Configure access to the Kubernetes API server endpoint.. Default: EndpointAccess.PUBLIC_AND_PRIVATE
        :param kubectl_environment: Environment variables for the kubectl execution. Only relevant for kubectl enabled clusters. Default: - No environment variables.
        :param kubectl_layer: An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI. By default, the provider will use the layer included in the "aws-lambda-layer-kubectl" SAR application which is available in all commercial regions. To deploy the layer locally, visit https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md for instructions on how to prepare the .zip file and then define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'kubectl-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`)), compatibleRuntimes: [lambda.Runtime.PROVIDED] }) Default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.
        :param masters_role: An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - a role that assumable by anyone with permissions in the same account will automatically be defined
        :param output_masters_role_arn: Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param default_profile: Fargate Profile to create along with the cluster. Default: - A profile called "default" with 'default' and 'kube-system' selectors will be created if this is left undefined.

        stability
        :stability: experimental
        """
        if isinstance(default_profile, dict):
            default_profile = FargateProfileOptions(**default_profile)
        self._values = {
            "version": version,
        }
        if cluster_name is not None:
            self._values["cluster_name"] = cluster_name
        if output_cluster_name is not None:
            self._values["output_cluster_name"] = output_cluster_name
        if output_config_command is not None:
            self._values["output_config_command"] = output_config_command
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if core_dns_compute_type is not None:
            self._values["core_dns_compute_type"] = core_dns_compute_type
        if endpoint_access is not None:
            self._values["endpoint_access"] = endpoint_access
        if kubectl_environment is not None:
            self._values["kubectl_environment"] = kubectl_environment
        if kubectl_layer is not None:
            self._values["kubectl_layer"] = kubectl_layer
        if masters_role is not None:
            self._values["masters_role"] = masters_role
        if output_masters_role_arn is not None:
            self._values["output_masters_role_arn"] = output_masters_role_arn
        if default_profile is not None:
            self._values["default_profile"] = default_profile

    @builtins.property
    def version(self) -> "KubernetesVersion":
        """The Kubernetes version to run in the cluster.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    @builtins.property
    def cluster_name(self) -> typing.Optional[str]:
        """Name for the cluster.

        default
        :default: - Automatically generated name

        stability
        :stability: experimental
        """
        return self._values.get("cluster_name")

    @builtins.property
    def output_cluster_name(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the name of the cluster will be synthesized.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("output_cluster_name")

    @builtins.property
    def output_config_command(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized.

        This command will include
        the cluster name and, if applicable, the ARN of the masters IAM role.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("output_config_command")

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get("role")

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """Security Group to use for Control Plane ENIs.

        default
        :default: - A security group is automatically created

        stability
        :stability: experimental
        """
        return self._values.get("security_group")

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC in which to create the Cluster.

        default
        :default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[typing.List[_SubnetSelection_36a13cd6]]:
        """Where to place EKS Control Plane ENIs.

        If you want to create public load balancers, this must include public subnets.

        For example, to only select private subnets, supply the following::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           vpcSubnets: [
              { subnetType: ec2.SubnetType.Private }
           ]

        default
        :default: - All public and private subnets

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    @builtins.property
    def core_dns_compute_type(self) -> typing.Optional["CoreDnsComputeType"]:
        """Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS.

        default
        :default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)

        stability
        :stability: experimental
        """
        return self._values.get("core_dns_compute_type")

    @builtins.property
    def endpoint_access(self) -> typing.Optional["EndpointAccess"]:
        """Configure access to the Kubernetes API server endpoint..

        default
        :default: EndpointAccess.PUBLIC_AND_PRIVATE

        see
        :see: https://docs.aws.amazon.com/eks/latest/userguide/cluster-endpoint.html
        stability
        :stability: experimental
        """
        return self._values.get("endpoint_access")

    @builtins.property
    def kubectl_environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Environment variables for the kubectl execution.

        Only relevant for kubectl enabled clusters.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get("kubectl_environment")

    @builtins.property
    def kubectl_layer(self) -> typing.Optional[_ILayerVersion_aa5e0c0c]:
        """An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI.

        By default, the provider will use the layer included in the
        "aws-lambda-layer-kubectl" SAR application which is available in all
        commercial regions.

        To deploy the layer locally, visit
        https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md
        for instructions on how to prepare the .zip file and then define it in your
        app as follows::

           # Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
           layer = lambda_.LayerVersion(self, "kubectl-layer",
               code=lambda_.Code.from_asset(f"{__dirname}/layer.zip")
           )
           compatible_runtimes =

        default
        :default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.

        see
        :see: https://github.com/aws-samples/aws-lambda-layer-kubectl
        stability
        :stability: experimental
        """
        return self._values.get("kubectl_layer")

    @builtins.property
    def masters_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group.

        default
        :default:

        - a role that assumable by anyone with permissions in the same
          account will automatically be defined

        see
        :see: https://kubernetes.io/docs/reference/access-authn-authz/rbac/#default-roles-and-role-bindings
        stability
        :stability: experimental
        """
        return self._values.get("masters_role")

    @builtins.property
    def output_masters_role_arn(self) -> typing.Optional[bool]:
        """Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified).

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("output_masters_role_arn")

    @builtins.property
    def default_profile(self) -> typing.Optional["FargateProfileOptions"]:
        """Fargate Profile to create along with the cluster.

        default
        :default:

        - A profile called "default" with 'default' and 'kube-system'
          selectors will be created if this is left undefined.

        stability
        :stability: experimental
        """
        return self._values.get("default_profile")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FargateClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AutoScalingGroupOptions",
    "AwsAuth",
    "AwsAuthMapping",
    "AwsAuthProps",
    "BootstrapOptions",
    "CapacityOptions",
    "CfnCluster",
    "CfnClusterProps",
    "CfnNodegroup",
    "CfnNodegroupProps",
    "Cluster",
    "ClusterAttributes",
    "ClusterOptions",
    "ClusterProps",
    "CommonClusterOptions",
    "CoreDnsComputeType",
    "DefaultCapacityType",
    "EksOptimizedImage",
    "EksOptimizedImageProps",
    "EndpointAccess",
    "FargateCluster",
    "FargateClusterProps",
    "FargateProfile",
    "FargateProfileOptions",
    "FargateProfileProps",
    "HelmChart",
    "HelmChartOptions",
    "HelmChartProps",
    "ICluster",
    "INodegroup",
    "KubectlLayer",
    "KubectlLayerProps",
    "KubernetesManifest",
    "KubernetesManifestProps",
    "KubernetesObjectValue",
    "KubernetesObjectValueProps",
    "KubernetesPatch",
    "KubernetesPatchProps",
    "KubernetesVersion",
    "LegacyCluster",
    "LegacyClusterProps",
    "MachineImageType",
    "NodeType",
    "Nodegroup",
    "NodegroupAmiType",
    "NodegroupOptions",
    "NodegroupProps",
    "NodegroupRemoteAccess",
    "PatchType",
    "Selector",
    "ServiceAccount",
    "ServiceAccountOptions",
    "ServiceAccountProps",
    "ServiceLoadBalancerAddressOptions",
]

publication.publish()
