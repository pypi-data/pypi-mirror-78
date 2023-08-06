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
    Duration as _Duration_5170c158,
    IInspectable as _IInspectable_051e6ed8,
    IResolvable as _IResolvable_9ceae33e,
    IResource as _IResource_72f7ee7e,
    RemovalPolicy as _RemovalPolicy_5986e9f3,
    Resource as _Resource_884d0774,
    ResourceProps as _ResourceProps_92be6f66,
    SecretValue as _SecretValue_99478b8b,
    TagManager as _TagManager_2508893f,
    TreeInspector as _TreeInspector_154f5999,
)
from ..aws_cloudwatch import (
    Metric as _Metric_53e89548,
    MetricOptions as _MetricOptions_ad2c4d5d,
    Unit as _Unit_e1b74f3c,
)
from ..aws_ec2 import (
    Connections as _Connections_231f38b5,
    IConnectable as _IConnectable_a587039f,
    ISecurityGroup as _ISecurityGroup_d72ab8e8,
    IVpc as _IVpc_3795853f,
    InstanceType as _InstanceType_85a97b30,
    SubnetSelection as _SubnetSelection_36a13cd6,
)
from ..aws_events import (
    EventPattern as _EventPattern_8aa7b781,
    IRuleTarget as _IRuleTarget_41800a77,
    OnEventOptions as _OnEventOptions_926fbcf9,
    Rule as _Rule_c38e0b39,
)
from ..aws_iam import (
    Grant as _Grant_96af6d2d,
    IGrantable as _IGrantable_0fcfc53a,
    IRole as _IRole_e69bbae4,
)
from ..aws_kms import IKey as _IKey_3336c79d
from ..aws_logs import RetentionDays as _RetentionDays_bdc7ad1f
from ..aws_s3 import IBucket as _IBucket_25bad983
from ..aws_secretsmanager import (
    ISecret as _ISecret_75279d36,
    ISecretAttachmentTarget as _ISecretAttachmentTarget_0a569782,
    Secret as _Secret_01d21232,
    SecretAttachmentTargetProps as _SecretAttachmentTargetProps_b948cd13,
    SecretRotation as _SecretRotation_312fb992,
    SecretRotationApplication as _SecretRotationApplication_5d71a263,
)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.AuroraClusterEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class AuroraClusterEngineProps:
    def __init__(self, *, version: "AuroraEngineVersion") -> None:
        """Creation properties of the plain Aurora database cluster engine.

        Used in {@link DatabaseClusterEngine.aurora}.

        :param version: The version of the Aurora cluster engine.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "AuroraEngineVersion":
        """The version of the Aurora cluster engine.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuroraClusterEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AuroraEngineVersion(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_rds.AuroraEngineVersion"
):
    """The versions for the Aurora cluster engine (those returned by {@link DatabaseClusterEngine.aurora}).

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        aurora_full_version: str,
        aurora_major_version: typing.Optional[str] = None,
    ) -> "AuroraEngineVersion":
        """Create a new AuroraEngineVersion with an arbitrary version.

        :param aurora_full_version: the full version string, for example "5.6.mysql_aurora.1.78.3.6".
        :param aurora_major_version: the major version of the engine, defaults to "5.6".

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [aurora_full_version, aurora_major_version])

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_17_9")
    def VER_1_17_9(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.17.9".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_17_9")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_19_0")
    def VER_1_19_0(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.19.0".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_19_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_19_1")
    def VER_1_19_1(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.19.1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_19_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_19_2")
    def VER_1_19_2(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.19.2".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_19_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_19_5")
    def VER_1_19_5(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.19.5".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_19_5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_19_6")
    def VER_1_19_6(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.19.6".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_19_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_20_0")
    def VER_1_20_0(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.20.0".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_20_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_20_1")
    def VER_1_20_1(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.20.1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_20_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_21_0")
    def VER_1_21_0(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.21.0".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_21_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_22_0")
    def VER_1_22_0(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.22.0".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_22_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_22_1")
    def VER_1_22_1(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.22.1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_22_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_22_1_3")
    def VER_1_22_1_3(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.22.1.3".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_22_1_3")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_1_22_2")
    def VER_1_22_2(cls) -> "AuroraEngineVersion":
        """Version "5.6.mysql_aurora.1.22.2".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_1_22_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10A")
    def VER_10_A(cls) -> "AuroraEngineVersion":
        """Version "5.6.10a".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10A")

    @builtins.property
    @jsii.member(jsii_name="auroraFullVersion")
    def aurora_full_version(self) -> str:
        """The full version string, for example, "5.6.mysql_aurora.1.78.3.6".

        stability
        :stability: experimental
        """
        return jsii.get(self, "auroraFullVersion")

    @builtins.property
    @jsii.member(jsii_name="auroraMajorVersion")
    def aurora_major_version(self) -> str:
        """The major version of the engine.

        Currently, it's always "5.6".

        stability
        :stability: experimental
        """
        return jsii.get(self, "auroraMajorVersion")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.AuroraMysqlClusterEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class AuroraMysqlClusterEngineProps:
    def __init__(self, *, version: "AuroraMysqlEngineVersion") -> None:
        """Creation properties of the Aurora MySQL database cluster engine.

        Used in {@link DatabaseClusterEngine.auroraMysql}.

        :param version: The version of the Aurora MySQL cluster engine.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "AuroraMysqlEngineVersion":
        """The version of the Aurora MySQL cluster engine.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuroraMysqlClusterEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AuroraMysqlEngineVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.AuroraMysqlEngineVersion",
):
    """The versions for the Aurora MySQL cluster engine (those returned by {@link DatabaseClusterEngine.auroraMysql}).

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        aurora_mysql_full_version: str,
        aurora_mysql_major_version: typing.Optional[str] = None,
    ) -> "AuroraMysqlEngineVersion":
        """Create a new AuroraMysqlEngineVersion with an arbitrary version.

        :param aurora_mysql_full_version: the full version string, for example "5.7.mysql_aurora.2.78.3.6".
        :param aurora_mysql_major_version: the major version of the engine, defaults to "5.7".

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [aurora_mysql_full_version, aurora_mysql_major_version])

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_03_2")
    def VER_2_03_2(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.03.2".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_03_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_03_3")
    def VER_2_03_3(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.03.3".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_03_3")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_03_4")
    def VER_2_03_4(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.03.4".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_03_4")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_04_0")
    def VER_2_04_0(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.04.0".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_04_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_04_1")
    def VER_2_04_1(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.04.1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_04_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_04_2")
    def VER_2_04_2(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.04.2".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_04_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_04_3")
    def VER_2_04_3(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.04.3".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_04_3")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_04_4")
    def VER_2_04_4(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.04.4".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_04_4")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_04_5")
    def VER_2_04_5(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.04.5".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_04_5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_04_6")
    def VER_2_04_6(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.04.6".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_04_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_04_7")
    def VER_2_04_7(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.04.7".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_04_7")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_04_8")
    def VER_2_04_8(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.04.8".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_04_8")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_05_0")
    def VER_2_05_0(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.05.0".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_05_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_06_0")
    def VER_2_06_0(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.06.0".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_06_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_07_0")
    def VER_2_07_0(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.07.0".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_07_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_07_1")
    def VER_2_07_1(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.07.1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_07_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_07_2")
    def VER_2_07_2(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.07.2".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_07_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_08_0")
    def VER_2_08_0(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.08.0".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_08_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_2_08_1")
    def VER_2_08_1(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.mysql_aurora.2.08.1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_2_08_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7_12")
    def VER_5_7_12(cls) -> "AuroraMysqlEngineVersion":
        """Version "5.7.12".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7_12")

    @builtins.property
    @jsii.member(jsii_name="auroraMysqlFullVersion")
    def aurora_mysql_full_version(self) -> str:
        """The full version string, for example, "5.7.mysql_aurora.1.78.3.6".

        stability
        :stability: experimental
        """
        return jsii.get(self, "auroraMysqlFullVersion")

    @builtins.property
    @jsii.member(jsii_name="auroraMysqlMajorVersion")
    def aurora_mysql_major_version(self) -> str:
        """The major version of the engine.

        Currently, it's always "5.7".

        stability
        :stability: experimental
        """
        return jsii.get(self, "auroraMysqlMajorVersion")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.AuroraPostgresClusterEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class AuroraPostgresClusterEngineProps:
    def __init__(self, *, version: "AuroraPostgresEngineVersion") -> None:
        """Creation properties of the Aurora PostgreSQL database cluster engine.

        Used in {@link DatabaseClusterEngine.auroraPostgres}.

        :param version: The version of the Aurora PostgreSQL cluster engine.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "AuroraPostgresEngineVersion":
        """The version of the Aurora PostgreSQL cluster engine.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AuroraPostgresClusterEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AuroraPostgresEngineVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.AuroraPostgresEngineVersion",
):
    """The versions for the Aurora PostgreSQL cluster engine (those returned by {@link DatabaseClusterEngine.auroraPostgres}).

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls, aurora_postgres_full_version: str, aurora_postgres_major_version: str
    ) -> "AuroraPostgresEngineVersion":
        """Create a new AuroraPostgresEngineVersion with an arbitrary version.

        :param aurora_postgres_full_version: the full version string, for example "9.6.25.1".
        :param aurora_postgres_major_version: the major version of the engine, for example "9.6".

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [aurora_postgres_full_version, aurora_postgres_major_version])

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_11")
    def VER_10_11(cls) -> "AuroraPostgresEngineVersion":
        """Version "10.11".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_12")
    def VER_10_12(cls) -> "AuroraPostgresEngineVersion":
        """Version "10.12".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_12")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_4")
    def VER_10_4(cls) -> "AuroraPostgresEngineVersion":
        """Version "10.4".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_4")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_5")
    def VER_10_5(cls) -> "AuroraPostgresEngineVersion":
        """Version "10.5".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_6")
    def VER_10_6(cls) -> "AuroraPostgresEngineVersion":
        """Version "10.6".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_7")
    def VER_10_7(cls) -> "AuroraPostgresEngineVersion":
        """Version "10.7".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_7")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_4")
    def VER_11_4(cls) -> "AuroraPostgresEngineVersion":
        """Version "11.4".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_4")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_6")
    def VER_11_6(cls) -> "AuroraPostgresEngineVersion":
        """Version "11.6".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_7")
    def VER_11_7(cls) -> "AuroraPostgresEngineVersion":
        """Version "11.7".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_7")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_11")
    def VER_9_6_11(cls) -> "AuroraPostgresEngineVersion":
        """Version "9.6.11".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_12")
    def VER_9_6_12(cls) -> "AuroraPostgresEngineVersion":
        """Version "9.6.12".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_12")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_16")
    def VER_9_6_16(cls) -> "AuroraPostgresEngineVersion":
        """Version "9.6.16".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_16")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_17")
    def VER_9_6_17(cls) -> "AuroraPostgresEngineVersion":
        """Version "9.6.17".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_17")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_8")
    def VER_9_6_8(cls) -> "AuroraPostgresEngineVersion":
        """Version "9.6.8".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_8")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_9")
    def VER_9_6_9(cls) -> "AuroraPostgresEngineVersion":
        """Version "9.6.9".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_9")

    @builtins.property
    @jsii.member(jsii_name="auroraPostgresFullVersion")
    def aurora_postgres_full_version(self) -> str:
        """The full version string, for example, "9.6.25.1".

        stability
        :stability: experimental
        """
        return jsii.get(self, "auroraPostgresFullVersion")

    @builtins.property
    @jsii.member(jsii_name="auroraPostgresMajorVersion")
    def aurora_postgres_major_version(self) -> str:
        """The major version of the engine, for example, "9.6".

        stability
        :stability: experimental
        """
        return jsii.get(self, "auroraPostgresMajorVersion")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.BackupProps",
    jsii_struct_bases=[],
    name_mapping={"retention": "retention", "preferred_window": "preferredWindow"},
)
class BackupProps:
    def __init__(
        self,
        *,
        retention: _Duration_5170c158,
        preferred_window: typing.Optional[str] = None,
    ) -> None:
        """Backup configuration for RDS databases.

        :param retention: How many days to retain the backup.
        :param preferred_window: A daily time range in 24-hours UTC format in which backups preferably execute. Must be at least 30 minutes long. Example: '01:00-02:00' Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow

        default
        :default:

        - The retention period for automated backups is 1 day.
          The preferred backup window will be a 30-minute window selected at random
          from an 8-hour block of time for each AWS Region.

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        stability
        :stability: experimental
        """
        self._values = {
            "retention": retention,
        }
        if preferred_window is not None:
            self._values["preferred_window"] = preferred_window

    @builtins.property
    def retention(self) -> _Duration_5170c158:
        """How many days to retain the backup.

        stability
        :stability: experimental
        """
        return self._values.get("retention")

    @builtins.property
    def preferred_window(self) -> typing.Optional[str]:
        """A daily time range in 24-hours UTC format in which backups preferably execute.

        Must be at least 30 minutes long.

        Example: '01:00-02:00'

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region. To see the time blocks available, see
          https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow

        stability
        :stability: experimental
        """
        return self._values.get("preferred_window")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBCluster(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.CfnDBCluster",
):
    """A CloudFormation ``AWS::RDS::DBCluster``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html
    cloudformationResource:
    :cloudformationResource:: AWS::RDS::DBCluster
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        engine: str,
        associated_roles: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DBClusterRoleProperty", _IResolvable_9ceae33e]]]] = None,
        availability_zones: typing.Optional[typing.List[str]] = None,
        backtrack_window: typing.Optional[jsii.Number] = None,
        backup_retention_period: typing.Optional[jsii.Number] = None,
        database_name: typing.Optional[str] = None,
        db_cluster_identifier: typing.Optional[str] = None,
        db_cluster_parameter_group_name: typing.Optional[str] = None,
        db_subnet_group_name: typing.Optional[str] = None,
        deletion_protection: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        enable_cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        enable_http_endpoint: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        enable_iam_database_authentication: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        engine_mode: typing.Optional[str] = None,
        engine_version: typing.Optional[str] = None,
        kms_key_id: typing.Optional[str] = None,
        master_username: typing.Optional[str] = None,
        master_user_password: typing.Optional[str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[str] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        replication_source_identifier: typing.Optional[str] = None,
        restore_type: typing.Optional[str] = None,
        scaling_configuration: typing.Optional[typing.Union["ScalingConfigurationProperty", _IResolvable_9ceae33e]] = None,
        snapshot_identifier: typing.Optional[str] = None,
        source_db_cluster_identifier: typing.Optional[str] = None,
        source_region: typing.Optional[str] = None,
        storage_encrypted: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        use_latest_restorable_time: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Create a new ``AWS::RDS::DBCluster``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param engine: ``AWS::RDS::DBCluster.Engine``.
        :param associated_roles: ``AWS::RDS::DBCluster.AssociatedRoles``.
        :param availability_zones: ``AWS::RDS::DBCluster.AvailabilityZones``.
        :param backtrack_window: ``AWS::RDS::DBCluster.BacktrackWindow``.
        :param backup_retention_period: ``AWS::RDS::DBCluster.BackupRetentionPeriod``.
        :param database_name: ``AWS::RDS::DBCluster.DatabaseName``.
        :param db_cluster_identifier: ``AWS::RDS::DBCluster.DBClusterIdentifier``.
        :param db_cluster_parameter_group_name: ``AWS::RDS::DBCluster.DBClusterParameterGroupName``.
        :param db_subnet_group_name: ``AWS::RDS::DBCluster.DBSubnetGroupName``.
        :param deletion_protection: ``AWS::RDS::DBCluster.DeletionProtection``.
        :param enable_cloudwatch_logs_exports: ``AWS::RDS::DBCluster.EnableCloudwatchLogsExports``.
        :param enable_http_endpoint: ``AWS::RDS::DBCluster.EnableHttpEndpoint``.
        :param enable_iam_database_authentication: ``AWS::RDS::DBCluster.EnableIAMDatabaseAuthentication``.
        :param engine_mode: ``AWS::RDS::DBCluster.EngineMode``.
        :param engine_version: ``AWS::RDS::DBCluster.EngineVersion``.
        :param kms_key_id: ``AWS::RDS::DBCluster.KmsKeyId``.
        :param master_username: ``AWS::RDS::DBCluster.MasterUsername``.
        :param master_user_password: ``AWS::RDS::DBCluster.MasterUserPassword``.
        :param port: ``AWS::RDS::DBCluster.Port``.
        :param preferred_backup_window: ``AWS::RDS::DBCluster.PreferredBackupWindow``.
        :param preferred_maintenance_window: ``AWS::RDS::DBCluster.PreferredMaintenanceWindow``.
        :param replication_source_identifier: ``AWS::RDS::DBCluster.ReplicationSourceIdentifier``.
        :param restore_type: ``AWS::RDS::DBCluster.RestoreType``.
        :param scaling_configuration: ``AWS::RDS::DBCluster.ScalingConfiguration``.
        :param snapshot_identifier: ``AWS::RDS::DBCluster.SnapshotIdentifier``.
        :param source_db_cluster_identifier: ``AWS::RDS::DBCluster.SourceDBClusterIdentifier``.
        :param source_region: ``AWS::RDS::DBCluster.SourceRegion``.
        :param storage_encrypted: ``AWS::RDS::DBCluster.StorageEncrypted``.
        :param tags: ``AWS::RDS::DBCluster.Tags``.
        :param use_latest_restorable_time: ``AWS::RDS::DBCluster.UseLatestRestorableTime``.
        :param vpc_security_group_ids: ``AWS::RDS::DBCluster.VpcSecurityGroupIds``.
        """
        props = CfnDBClusterProps(
            engine=engine,
            associated_roles=associated_roles,
            availability_zones=availability_zones,
            backtrack_window=backtrack_window,
            backup_retention_period=backup_retention_period,
            database_name=database_name,
            db_cluster_identifier=db_cluster_identifier,
            db_cluster_parameter_group_name=db_cluster_parameter_group_name,
            db_subnet_group_name=db_subnet_group_name,
            deletion_protection=deletion_protection,
            enable_cloudwatch_logs_exports=enable_cloudwatch_logs_exports,
            enable_http_endpoint=enable_http_endpoint,
            enable_iam_database_authentication=enable_iam_database_authentication,
            engine_mode=engine_mode,
            engine_version=engine_version,
            kms_key_id=kms_key_id,
            master_username=master_username,
            master_user_password=master_user_password,
            port=port,
            preferred_backup_window=preferred_backup_window,
            preferred_maintenance_window=preferred_maintenance_window,
            replication_source_identifier=replication_source_identifier,
            restore_type=restore_type,
            scaling_configuration=scaling_configuration,
            snapshot_identifier=snapshot_identifier,
            source_db_cluster_identifier=source_db_cluster_identifier,
            source_region=source_region,
            storage_encrypted=storage_encrypted,
            tags=tags,
            use_latest_restorable_time=use_latest_restorable_time,
            vpc_security_group_ids=vpc_security_group_ids,
        )

        jsii.create(CfnDBCluster, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrEndpointAddress")
    def attr_endpoint_address(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint.Address
        """
        return jsii.get(self, "attrEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="attrEndpointPort")
    def attr_endpoint_port(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint.Port
        """
        return jsii.get(self, "attrEndpointPort")

    @builtins.property
    @jsii.member(jsii_name="attrReadEndpointAddress")
    def attr_read_endpoint_address(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: ReadEndpoint.Address
        """
        return jsii.get(self, "attrReadEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::RDS::DBCluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> str:
        """``AWS::RDS::DBCluster.Engine``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-engine
        """
        return jsii.get(self, "engine")

    @engine.setter
    def engine(self, value: str) -> None:
        jsii.set(self, "engine", value)

    @builtins.property
    @jsii.member(jsii_name="associatedRoles")
    def associated_roles(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DBClusterRoleProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::RDS::DBCluster.AssociatedRoles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-associatedroles
        """
        return jsii.get(self, "associatedRoles")

    @associated_roles.setter
    def associated_roles(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DBClusterRoleProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "associatedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBCluster.AvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-availabilityzones
        """
        return jsii.get(self, "availabilityZones")

    @availability_zones.setter
    def availability_zones(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "availabilityZones", value)

    @builtins.property
    @jsii.member(jsii_name="backtrackWindow")
    def backtrack_window(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBCluster.BacktrackWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-backtrackwindow
        """
        return jsii.get(self, "backtrackWindow")

    @backtrack_window.setter
    def backtrack_window(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "backtrackWindow", value)

    @builtins.property
    @jsii.member(jsii_name="backupRetentionPeriod")
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBCluster.BackupRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-backuprententionperiod
        """
        return jsii.get(self, "backupRetentionPeriod")

    @backup_retention_period.setter
    def backup_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "backupRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="databaseName")
    def database_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.DatabaseName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-databasename
        """
        return jsii.get(self, "databaseName")

    @database_name.setter
    def database_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "databaseName", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.DBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbclusteridentifier
        """
        return jsii.get(self, "dbClusterIdentifier")

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbClusterIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterParameterGroupName")
    def db_cluster_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.DBClusterParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbclusterparametergroupname
        """
        return jsii.get(self, "dbClusterParameterGroupName")

    @db_cluster_parameter_group_name.setter
    def db_cluster_parameter_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbClusterParameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbsubnetgroupname
        """
        return jsii.get(self, "dbSubnetGroupName")

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbSubnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBCluster.DeletionProtection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-deletionprotection
        """
        return jsii.get(self, "deletionProtection")

    @deletion_protection.setter
    def deletion_protection(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "deletionProtection", value)

    @builtins.property
    @jsii.member(jsii_name="enableCloudwatchLogsExports")
    def enable_cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBCluster.EnableCloudwatchLogsExports``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enablecloudwatchlogsexports
        """
        return jsii.get(self, "enableCloudwatchLogsExports")

    @enable_cloudwatch_logs_exports.setter
    def enable_cloudwatch_logs_exports(
        self, value: typing.Optional[typing.List[str]]
    ) -> None:
        jsii.set(self, "enableCloudwatchLogsExports", value)

    @builtins.property
    @jsii.member(jsii_name="enableHttpEndpoint")
    def enable_http_endpoint(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBCluster.EnableHttpEndpoint``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enablehttpendpoint
        """
        return jsii.get(self, "enableHttpEndpoint")

    @enable_http_endpoint.setter
    def enable_http_endpoint(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "enableHttpEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="enableIamDatabaseAuthentication")
    def enable_iam_database_authentication(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBCluster.EnableIAMDatabaseAuthentication``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enableiamdatabaseauthentication
        """
        return jsii.get(self, "enableIamDatabaseAuthentication")

    @enable_iam_database_authentication.setter
    def enable_iam_database_authentication(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "enableIamDatabaseAuthentication", value)

    @builtins.property
    @jsii.member(jsii_name="engineMode")
    def engine_mode(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.EngineMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enginemode
        """
        return jsii.get(self, "engineMode")

    @engine_mode.setter
    def engine_mode(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "engineMode", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.EngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-engineversion
        """
        return jsii.get(self, "engineVersion")

    @engine_version.setter
    def engine_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="masterUsername")
    def master_username(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.MasterUsername``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-masterusername
        """
        return jsii.get(self, "masterUsername")

    @master_username.setter
    def master_username(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "masterUsername", value)

    @builtins.property
    @jsii.member(jsii_name="masterUserPassword")
    def master_user_password(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.MasterUserPassword``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-masteruserpassword
        """
        return jsii.get(self, "masterUserPassword")

    @master_user_password.setter
    def master_user_password(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "masterUserPassword", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBCluster.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-port
        """
        return jsii.get(self, "port")

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="preferredBackupWindow")
    def preferred_backup_window(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.PreferredBackupWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-preferredbackupwindow
        """
        return jsii.get(self, "preferredBackupWindow")

    @preferred_backup_window.setter
    def preferred_backup_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "preferredBackupWindow", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="replicationSourceIdentifier")
    def replication_source_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.ReplicationSourceIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-replicationsourceidentifier
        """
        return jsii.get(self, "replicationSourceIdentifier")

    @replication_source_identifier.setter
    def replication_source_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "replicationSourceIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="restoreType")
    def restore_type(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.RestoreType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-restoretype
        """
        return jsii.get(self, "restoreType")

    @restore_type.setter
    def restore_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "restoreType", value)

    @builtins.property
    @jsii.member(jsii_name="scalingConfiguration")
    def scaling_configuration(
        self,
    ) -> typing.Optional[typing.Union["ScalingConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBCluster.ScalingConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-scalingconfiguration
        """
        return jsii.get(self, "scalingConfiguration")

    @scaling_configuration.setter
    def scaling_configuration(
        self,
        value: typing.Optional[typing.Union["ScalingConfigurationProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "scalingConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="snapshotIdentifier")
    def snapshot_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.SnapshotIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-snapshotidentifier
        """
        return jsii.get(self, "snapshotIdentifier")

    @snapshot_identifier.setter
    def snapshot_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "snapshotIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="sourceDbClusterIdentifier")
    def source_db_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.SourceDBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-sourcedbclusteridentifier
        """
        return jsii.get(self, "sourceDbClusterIdentifier")

    @source_db_cluster_identifier.setter
    def source_db_cluster_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "sourceDbClusterIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="sourceRegion")
    def source_region(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.SourceRegion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-sourceregion
        """
        return jsii.get(self, "sourceRegion")

    @source_region.setter
    def source_region(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "sourceRegion", value)

    @builtins.property
    @jsii.member(jsii_name="storageEncrypted")
    def storage_encrypted(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBCluster.StorageEncrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-storageencrypted
        """
        return jsii.get(self, "storageEncrypted")

    @storage_encrypted.setter
    def storage_encrypted(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "storageEncrypted", value)

    @builtins.property
    @jsii.member(jsii_name="useLatestRestorableTime")
    def use_latest_restorable_time(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBCluster.UseLatestRestorableTime``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-uselatestrestorabletime
        """
        return jsii.get(self, "useLatestRestorableTime")

    @use_latest_restorable_time.setter
    def use_latest_restorable_time(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "useLatestRestorableTime", value)

    @builtins.property
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBCluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-vpcsecuritygroupids
        """
        return jsii.get(self, "vpcSecurityGroupIds")

    @vpc_security_group_ids.setter
    def vpc_security_group_ids(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "vpcSecurityGroupIds", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_rds.CfnDBCluster.DBClusterRoleProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "feature_name": "featureName"},
    )
    class DBClusterRoleProperty:
        def __init__(
            self, *, role_arn: str, feature_name: typing.Optional[str] = None
        ) -> None:
            """
            :param role_arn: ``CfnDBCluster.DBClusterRoleProperty.RoleArn``.
            :param feature_name: ``CfnDBCluster.DBClusterRoleProperty.FeatureName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-dbclusterrole.html
            """
            self._values = {
                "role_arn": role_arn,
            }
            if feature_name is not None:
                self._values["feature_name"] = feature_name

        @builtins.property
        def role_arn(self) -> str:
            """``CfnDBCluster.DBClusterRoleProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-dbclusterrole.html#cfn-rds-dbcluster-dbclusterrole-rolearn
            """
            return self._values.get("role_arn")

        @builtins.property
        def feature_name(self) -> typing.Optional[str]:
            """``CfnDBCluster.DBClusterRoleProperty.FeatureName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-dbclusterrole.html#cfn-rds-dbcluster-dbclusterrole-featurename
            """
            return self._values.get("feature_name")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DBClusterRoleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_rds.CfnDBCluster.ScalingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_pause": "autoPause",
            "max_capacity": "maxCapacity",
            "min_capacity": "minCapacity",
            "seconds_until_auto_pause": "secondsUntilAutoPause",
        },
    )
    class ScalingConfigurationProperty:
        def __init__(
            self,
            *,
            auto_pause: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
            max_capacity: typing.Optional[jsii.Number] = None,
            min_capacity: typing.Optional[jsii.Number] = None,
            seconds_until_auto_pause: typing.Optional[jsii.Number] = None,
        ) -> None:
            """
            :param auto_pause: ``CfnDBCluster.ScalingConfigurationProperty.AutoPause``.
            :param max_capacity: ``CfnDBCluster.ScalingConfigurationProperty.MaxCapacity``.
            :param min_capacity: ``CfnDBCluster.ScalingConfigurationProperty.MinCapacity``.
            :param seconds_until_auto_pause: ``CfnDBCluster.ScalingConfigurationProperty.SecondsUntilAutoPause``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html
            """
            self._values = {}
            if auto_pause is not None:
                self._values["auto_pause"] = auto_pause
            if max_capacity is not None:
                self._values["max_capacity"] = max_capacity
            if min_capacity is not None:
                self._values["min_capacity"] = min_capacity
            if seconds_until_auto_pause is not None:
                self._values["seconds_until_auto_pause"] = seconds_until_auto_pause

        @builtins.property
        def auto_pause(
            self,
        ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
            """``CfnDBCluster.ScalingConfigurationProperty.AutoPause``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-autopause
            """
            return self._values.get("auto_pause")

        @builtins.property
        def max_capacity(self) -> typing.Optional[jsii.Number]:
            """``CfnDBCluster.ScalingConfigurationProperty.MaxCapacity``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-maxcapacity
            """
            return self._values.get("max_capacity")

        @builtins.property
        def min_capacity(self) -> typing.Optional[jsii.Number]:
            """``CfnDBCluster.ScalingConfigurationProperty.MinCapacity``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-mincapacity
            """
            return self._values.get("min_capacity")

        @builtins.property
        def seconds_until_auto_pause(self) -> typing.Optional[jsii.Number]:
            """``CfnDBCluster.ScalingConfigurationProperty.SecondsUntilAutoPause``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-secondsuntilautopause
            """
            return self._values.get("seconds_until_auto_pause")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScalingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBClusterParameterGroup(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.CfnDBClusterParameterGroup",
):
    """A CloudFormation ``AWS::RDS::DBClusterParameterGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::RDS::DBClusterParameterGroup
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        description: str,
        family: str,
        parameters: typing.Any,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::RDS::DBClusterParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::RDS::DBClusterParameterGroup.Description``.
        :param family: ``AWS::RDS::DBClusterParameterGroup.Family``.
        :param parameters: ``AWS::RDS::DBClusterParameterGroup.Parameters``.
        :param tags: ``AWS::RDS::DBClusterParameterGroup.Tags``.
        """
        props = CfnDBClusterParameterGroupProps(
            description=description, family=family, parameters=parameters, tags=tags
        )

        jsii.create(CfnDBClusterParameterGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::RDS::DBClusterParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        """``AWS::RDS::DBClusterParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: str) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> str:
        """``AWS::RDS::DBClusterParameterGroup.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-family
        """
        return jsii.get(self, "family")

    @family.setter
    def family(self, value: str) -> None:
        jsii.set(self, "family", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> typing.Any:
        """``AWS::RDS::DBClusterParameterGroup.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: typing.Any) -> None:
        jsii.set(self, "parameters", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.CfnDBClusterParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "family": "family",
        "parameters": "parameters",
        "tags": "tags",
    },
)
class CfnDBClusterParameterGroupProps:
    def __init__(
        self,
        *,
        description: str,
        family: str,
        parameters: typing.Any,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::RDS::DBClusterParameterGroup``.

        :param description: ``AWS::RDS::DBClusterParameterGroup.Description``.
        :param family: ``AWS::RDS::DBClusterParameterGroup.Family``.
        :param parameters: ``AWS::RDS::DBClusterParameterGroup.Parameters``.
        :param tags: ``AWS::RDS::DBClusterParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html
        """
        self._values = {
            "description": description,
            "family": family,
            "parameters": parameters,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> str:
        """``AWS::RDS::DBClusterParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-description
        """
        return self._values.get("description")

    @builtins.property
    def family(self) -> str:
        """``AWS::RDS::DBClusterParameterGroup.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-family
        """
        return self._values.get("family")

    @builtins.property
    def parameters(self) -> typing.Any:
        """``AWS::RDS::DBClusterParameterGroup.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-parameters
        """
        return self._values.get("parameters")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::RDS::DBClusterParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBClusterParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.CfnDBClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "engine": "engine",
        "associated_roles": "associatedRoles",
        "availability_zones": "availabilityZones",
        "backtrack_window": "backtrackWindow",
        "backup_retention_period": "backupRetentionPeriod",
        "database_name": "databaseName",
        "db_cluster_identifier": "dbClusterIdentifier",
        "db_cluster_parameter_group_name": "dbClusterParameterGroupName",
        "db_subnet_group_name": "dbSubnetGroupName",
        "deletion_protection": "deletionProtection",
        "enable_cloudwatch_logs_exports": "enableCloudwatchLogsExports",
        "enable_http_endpoint": "enableHttpEndpoint",
        "enable_iam_database_authentication": "enableIamDatabaseAuthentication",
        "engine_mode": "engineMode",
        "engine_version": "engineVersion",
        "kms_key_id": "kmsKeyId",
        "master_username": "masterUsername",
        "master_user_password": "masterUserPassword",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "replication_source_identifier": "replicationSourceIdentifier",
        "restore_type": "restoreType",
        "scaling_configuration": "scalingConfiguration",
        "snapshot_identifier": "snapshotIdentifier",
        "source_db_cluster_identifier": "sourceDbClusterIdentifier",
        "source_region": "sourceRegion",
        "storage_encrypted": "storageEncrypted",
        "tags": "tags",
        "use_latest_restorable_time": "useLatestRestorableTime",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnDBClusterProps:
    def __init__(
        self,
        *,
        engine: str,
        associated_roles: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDBCluster.DBClusterRoleProperty", _IResolvable_9ceae33e]]]] = None,
        availability_zones: typing.Optional[typing.List[str]] = None,
        backtrack_window: typing.Optional[jsii.Number] = None,
        backup_retention_period: typing.Optional[jsii.Number] = None,
        database_name: typing.Optional[str] = None,
        db_cluster_identifier: typing.Optional[str] = None,
        db_cluster_parameter_group_name: typing.Optional[str] = None,
        db_subnet_group_name: typing.Optional[str] = None,
        deletion_protection: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        enable_cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        enable_http_endpoint: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        enable_iam_database_authentication: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        engine_mode: typing.Optional[str] = None,
        engine_version: typing.Optional[str] = None,
        kms_key_id: typing.Optional[str] = None,
        master_username: typing.Optional[str] = None,
        master_user_password: typing.Optional[str] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[str] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        replication_source_identifier: typing.Optional[str] = None,
        restore_type: typing.Optional[str] = None,
        scaling_configuration: typing.Optional[typing.Union["CfnDBCluster.ScalingConfigurationProperty", _IResolvable_9ceae33e]] = None,
        snapshot_identifier: typing.Optional[str] = None,
        source_db_cluster_identifier: typing.Optional[str] = None,
        source_region: typing.Optional[str] = None,
        storage_encrypted: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        use_latest_restorable_time: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::RDS::DBCluster``.

        :param engine: ``AWS::RDS::DBCluster.Engine``.
        :param associated_roles: ``AWS::RDS::DBCluster.AssociatedRoles``.
        :param availability_zones: ``AWS::RDS::DBCluster.AvailabilityZones``.
        :param backtrack_window: ``AWS::RDS::DBCluster.BacktrackWindow``.
        :param backup_retention_period: ``AWS::RDS::DBCluster.BackupRetentionPeriod``.
        :param database_name: ``AWS::RDS::DBCluster.DatabaseName``.
        :param db_cluster_identifier: ``AWS::RDS::DBCluster.DBClusterIdentifier``.
        :param db_cluster_parameter_group_name: ``AWS::RDS::DBCluster.DBClusterParameterGroupName``.
        :param db_subnet_group_name: ``AWS::RDS::DBCluster.DBSubnetGroupName``.
        :param deletion_protection: ``AWS::RDS::DBCluster.DeletionProtection``.
        :param enable_cloudwatch_logs_exports: ``AWS::RDS::DBCluster.EnableCloudwatchLogsExports``.
        :param enable_http_endpoint: ``AWS::RDS::DBCluster.EnableHttpEndpoint``.
        :param enable_iam_database_authentication: ``AWS::RDS::DBCluster.EnableIAMDatabaseAuthentication``.
        :param engine_mode: ``AWS::RDS::DBCluster.EngineMode``.
        :param engine_version: ``AWS::RDS::DBCluster.EngineVersion``.
        :param kms_key_id: ``AWS::RDS::DBCluster.KmsKeyId``.
        :param master_username: ``AWS::RDS::DBCluster.MasterUsername``.
        :param master_user_password: ``AWS::RDS::DBCluster.MasterUserPassword``.
        :param port: ``AWS::RDS::DBCluster.Port``.
        :param preferred_backup_window: ``AWS::RDS::DBCluster.PreferredBackupWindow``.
        :param preferred_maintenance_window: ``AWS::RDS::DBCluster.PreferredMaintenanceWindow``.
        :param replication_source_identifier: ``AWS::RDS::DBCluster.ReplicationSourceIdentifier``.
        :param restore_type: ``AWS::RDS::DBCluster.RestoreType``.
        :param scaling_configuration: ``AWS::RDS::DBCluster.ScalingConfiguration``.
        :param snapshot_identifier: ``AWS::RDS::DBCluster.SnapshotIdentifier``.
        :param source_db_cluster_identifier: ``AWS::RDS::DBCluster.SourceDBClusterIdentifier``.
        :param source_region: ``AWS::RDS::DBCluster.SourceRegion``.
        :param storage_encrypted: ``AWS::RDS::DBCluster.StorageEncrypted``.
        :param tags: ``AWS::RDS::DBCluster.Tags``.
        :param use_latest_restorable_time: ``AWS::RDS::DBCluster.UseLatestRestorableTime``.
        :param vpc_security_group_ids: ``AWS::RDS::DBCluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html
        """
        self._values = {
            "engine": engine,
        }
        if associated_roles is not None:
            self._values["associated_roles"] = associated_roles
        if availability_zones is not None:
            self._values["availability_zones"] = availability_zones
        if backtrack_window is not None:
            self._values["backtrack_window"] = backtrack_window
        if backup_retention_period is not None:
            self._values["backup_retention_period"] = backup_retention_period
        if database_name is not None:
            self._values["database_name"] = database_name
        if db_cluster_identifier is not None:
            self._values["db_cluster_identifier"] = db_cluster_identifier
        if db_cluster_parameter_group_name is not None:
            self._values["db_cluster_parameter_group_name"] = db_cluster_parameter_group_name
        if db_subnet_group_name is not None:
            self._values["db_subnet_group_name"] = db_subnet_group_name
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if enable_cloudwatch_logs_exports is not None:
            self._values["enable_cloudwatch_logs_exports"] = enable_cloudwatch_logs_exports
        if enable_http_endpoint is not None:
            self._values["enable_http_endpoint"] = enable_http_endpoint
        if enable_iam_database_authentication is not None:
            self._values["enable_iam_database_authentication"] = enable_iam_database_authentication
        if engine_mode is not None:
            self._values["engine_mode"] = engine_mode
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if master_username is not None:
            self._values["master_username"] = master_username
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if replication_source_identifier is not None:
            self._values["replication_source_identifier"] = replication_source_identifier
        if restore_type is not None:
            self._values["restore_type"] = restore_type
        if scaling_configuration is not None:
            self._values["scaling_configuration"] = scaling_configuration
        if snapshot_identifier is not None:
            self._values["snapshot_identifier"] = snapshot_identifier
        if source_db_cluster_identifier is not None:
            self._values["source_db_cluster_identifier"] = source_db_cluster_identifier
        if source_region is not None:
            self._values["source_region"] = source_region
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if tags is not None:
            self._values["tags"] = tags
        if use_latest_restorable_time is not None:
            self._values["use_latest_restorable_time"] = use_latest_restorable_time
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def engine(self) -> str:
        """``AWS::RDS::DBCluster.Engine``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-engine
        """
        return self._values.get("engine")

    @builtins.property
    def associated_roles(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDBCluster.DBClusterRoleProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::RDS::DBCluster.AssociatedRoles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-associatedroles
        """
        return self._values.get("associated_roles")

    @builtins.property
    def availability_zones(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBCluster.AvailabilityZones``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-availabilityzones
        """
        return self._values.get("availability_zones")

    @builtins.property
    def backtrack_window(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBCluster.BacktrackWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-backtrackwindow
        """
        return self._values.get("backtrack_window")

    @builtins.property
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBCluster.BackupRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-backuprententionperiod
        """
        return self._values.get("backup_retention_period")

    @builtins.property
    def database_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.DatabaseName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-databasename
        """
        return self._values.get("database_name")

    @builtins.property
    def db_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.DBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbclusteridentifier
        """
        return self._values.get("db_cluster_identifier")

    @builtins.property
    def db_cluster_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.DBClusterParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbclusterparametergroupname
        """
        return self._values.get("db_cluster_parameter_group_name")

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbsubnetgroupname
        """
        return self._values.get("db_subnet_group_name")

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBCluster.DeletionProtection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-deletionprotection
        """
        return self._values.get("deletion_protection")

    @builtins.property
    def enable_cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBCluster.EnableCloudwatchLogsExports``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enablecloudwatchlogsexports
        """
        return self._values.get("enable_cloudwatch_logs_exports")

    @builtins.property
    def enable_http_endpoint(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBCluster.EnableHttpEndpoint``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enablehttpendpoint
        """
        return self._values.get("enable_http_endpoint")

    @builtins.property
    def enable_iam_database_authentication(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBCluster.EnableIAMDatabaseAuthentication``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enableiamdatabaseauthentication
        """
        return self._values.get("enable_iam_database_authentication")

    @builtins.property
    def engine_mode(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.EngineMode``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enginemode
        """
        return self._values.get("engine_mode")

    @builtins.property
    def engine_version(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.EngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-engineversion
        """
        return self._values.get("engine_version")

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-kmskeyid
        """
        return self._values.get("kms_key_id")

    @builtins.property
    def master_username(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.MasterUsername``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-masterusername
        """
        return self._values.get("master_username")

    @builtins.property
    def master_user_password(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.MasterUserPassword``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-masteruserpassword
        """
        return self._values.get("master_user_password")

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBCluster.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-port
        """
        return self._values.get("port")

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.PreferredBackupWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-preferredbackupwindow
        """
        return self._values.get("preferred_backup_window")

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-preferredmaintenancewindow
        """
        return self._values.get("preferred_maintenance_window")

    @builtins.property
    def replication_source_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.ReplicationSourceIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-replicationsourceidentifier
        """
        return self._values.get("replication_source_identifier")

    @builtins.property
    def restore_type(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.RestoreType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-restoretype
        """
        return self._values.get("restore_type")

    @builtins.property
    def scaling_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnDBCluster.ScalingConfigurationProperty", _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBCluster.ScalingConfiguration``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-scalingconfiguration
        """
        return self._values.get("scaling_configuration")

    @builtins.property
    def snapshot_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.SnapshotIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-snapshotidentifier
        """
        return self._values.get("snapshot_identifier")

    @builtins.property
    def source_db_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.SourceDBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-sourcedbclusteridentifier
        """
        return self._values.get("source_db_cluster_identifier")

    @builtins.property
    def source_region(self) -> typing.Optional[str]:
        """``AWS::RDS::DBCluster.SourceRegion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-sourceregion
        """
        return self._values.get("source_region")

    @builtins.property
    def storage_encrypted(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBCluster.StorageEncrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-storageencrypted
        """
        return self._values.get("storage_encrypted")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::RDS::DBCluster.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-tags
        """
        return self._values.get("tags")

    @builtins.property
    def use_latest_restorable_time(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBCluster.UseLatestRestorableTime``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-uselatestrestorabletime
        """
        return self._values.get("use_latest_restorable_time")

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBCluster.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-vpcsecuritygroupids
        """
        return self._values.get("vpc_security_group_ids")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBInstance(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.CfnDBInstance",
):
    """A CloudFormation ``AWS::RDS::DBInstance``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html
    cloudformationResource:
    :cloudformationResource:: AWS::RDS::DBInstance
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        db_instance_class: str,
        allocated_storage: typing.Optional[str] = None,
        allow_major_version_upgrade: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        associated_roles: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DBInstanceRoleProperty", _IResolvable_9ceae33e]]]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        availability_zone: typing.Optional[str] = None,
        backup_retention_period: typing.Optional[jsii.Number] = None,
        ca_certificate_identifier: typing.Optional[str] = None,
        character_set_name: typing.Optional[str] = None,
        copy_tags_to_snapshot: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        db_cluster_identifier: typing.Optional[str] = None,
        db_instance_identifier: typing.Optional[str] = None,
        db_name: typing.Optional[str] = None,
        db_parameter_group_name: typing.Optional[str] = None,
        db_security_groups: typing.Optional[typing.List[str]] = None,
        db_snapshot_identifier: typing.Optional[str] = None,
        db_subnet_group_name: typing.Optional[str] = None,
        delete_automated_backups: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        deletion_protection: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        domain: typing.Optional[str] = None,
        domain_iam_role_name: typing.Optional[str] = None,
        enable_cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        enable_iam_database_authentication: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        enable_performance_insights: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        engine: typing.Optional[str] = None,
        engine_version: typing.Optional[str] = None,
        iops: typing.Optional[jsii.Number] = None,
        kms_key_id: typing.Optional[str] = None,
        license_model: typing.Optional[str] = None,
        master_username: typing.Optional[str] = None,
        master_user_password: typing.Optional[str] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[jsii.Number] = None,
        monitoring_role_arn: typing.Optional[str] = None,
        multi_az: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        option_group_name: typing.Optional[str] = None,
        performance_insights_kms_key_id: typing.Optional[str] = None,
        performance_insights_retention_period: typing.Optional[jsii.Number] = None,
        port: typing.Optional[str] = None,
        preferred_backup_window: typing.Optional[str] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        processor_features: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ProcessorFeatureProperty", _IResolvable_9ceae33e]]]] = None,
        promotion_tier: typing.Optional[jsii.Number] = None,
        publicly_accessible: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        source_db_instance_identifier: typing.Optional[str] = None,
        source_region: typing.Optional[str] = None,
        storage_encrypted: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        storage_type: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        timezone: typing.Optional[str] = None,
        use_default_processor_features: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        vpc_security_groups: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Create a new ``AWS::RDS::DBInstance``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_instance_class: ``AWS::RDS::DBInstance.DBInstanceClass``.
        :param allocated_storage: ``AWS::RDS::DBInstance.AllocatedStorage``.
        :param allow_major_version_upgrade: ``AWS::RDS::DBInstance.AllowMajorVersionUpgrade``.
        :param associated_roles: ``AWS::RDS::DBInstance.AssociatedRoles``.
        :param auto_minor_version_upgrade: ``AWS::RDS::DBInstance.AutoMinorVersionUpgrade``.
        :param availability_zone: ``AWS::RDS::DBInstance.AvailabilityZone``.
        :param backup_retention_period: ``AWS::RDS::DBInstance.BackupRetentionPeriod``.
        :param ca_certificate_identifier: ``AWS::RDS::DBInstance.CACertificateIdentifier``.
        :param character_set_name: ``AWS::RDS::DBInstance.CharacterSetName``.
        :param copy_tags_to_snapshot: ``AWS::RDS::DBInstance.CopyTagsToSnapshot``.
        :param db_cluster_identifier: ``AWS::RDS::DBInstance.DBClusterIdentifier``.
        :param db_instance_identifier: ``AWS::RDS::DBInstance.DBInstanceIdentifier``.
        :param db_name: ``AWS::RDS::DBInstance.DBName``.
        :param db_parameter_group_name: ``AWS::RDS::DBInstance.DBParameterGroupName``.
        :param db_security_groups: ``AWS::RDS::DBInstance.DBSecurityGroups``.
        :param db_snapshot_identifier: ``AWS::RDS::DBInstance.DBSnapshotIdentifier``.
        :param db_subnet_group_name: ``AWS::RDS::DBInstance.DBSubnetGroupName``.
        :param delete_automated_backups: ``AWS::RDS::DBInstance.DeleteAutomatedBackups``.
        :param deletion_protection: ``AWS::RDS::DBInstance.DeletionProtection``.
        :param domain: ``AWS::RDS::DBInstance.Domain``.
        :param domain_iam_role_name: ``AWS::RDS::DBInstance.DomainIAMRoleName``.
        :param enable_cloudwatch_logs_exports: ``AWS::RDS::DBInstance.EnableCloudwatchLogsExports``.
        :param enable_iam_database_authentication: ``AWS::RDS::DBInstance.EnableIAMDatabaseAuthentication``.
        :param enable_performance_insights: ``AWS::RDS::DBInstance.EnablePerformanceInsights``.
        :param engine: ``AWS::RDS::DBInstance.Engine``.
        :param engine_version: ``AWS::RDS::DBInstance.EngineVersion``.
        :param iops: ``AWS::RDS::DBInstance.Iops``.
        :param kms_key_id: ``AWS::RDS::DBInstance.KmsKeyId``.
        :param license_model: ``AWS::RDS::DBInstance.LicenseModel``.
        :param master_username: ``AWS::RDS::DBInstance.MasterUsername``.
        :param master_user_password: ``AWS::RDS::DBInstance.MasterUserPassword``.
        :param max_allocated_storage: ``AWS::RDS::DBInstance.MaxAllocatedStorage``.
        :param monitoring_interval: ``AWS::RDS::DBInstance.MonitoringInterval``.
        :param monitoring_role_arn: ``AWS::RDS::DBInstance.MonitoringRoleArn``.
        :param multi_az: ``AWS::RDS::DBInstance.MultiAZ``.
        :param option_group_name: ``AWS::RDS::DBInstance.OptionGroupName``.
        :param performance_insights_kms_key_id: ``AWS::RDS::DBInstance.PerformanceInsightsKMSKeyId``.
        :param performance_insights_retention_period: ``AWS::RDS::DBInstance.PerformanceInsightsRetentionPeriod``.
        :param port: ``AWS::RDS::DBInstance.Port``.
        :param preferred_backup_window: ``AWS::RDS::DBInstance.PreferredBackupWindow``.
        :param preferred_maintenance_window: ``AWS::RDS::DBInstance.PreferredMaintenanceWindow``.
        :param processor_features: ``AWS::RDS::DBInstance.ProcessorFeatures``.
        :param promotion_tier: ``AWS::RDS::DBInstance.PromotionTier``.
        :param publicly_accessible: ``AWS::RDS::DBInstance.PubliclyAccessible``.
        :param source_db_instance_identifier: ``AWS::RDS::DBInstance.SourceDBInstanceIdentifier``.
        :param source_region: ``AWS::RDS::DBInstance.SourceRegion``.
        :param storage_encrypted: ``AWS::RDS::DBInstance.StorageEncrypted``.
        :param storage_type: ``AWS::RDS::DBInstance.StorageType``.
        :param tags: ``AWS::RDS::DBInstance.Tags``.
        :param timezone: ``AWS::RDS::DBInstance.Timezone``.
        :param use_default_processor_features: ``AWS::RDS::DBInstance.UseDefaultProcessorFeatures``.
        :param vpc_security_groups: ``AWS::RDS::DBInstance.VPCSecurityGroups``.
        """
        props = CfnDBInstanceProps(
            db_instance_class=db_instance_class,
            allocated_storage=allocated_storage,
            allow_major_version_upgrade=allow_major_version_upgrade,
            associated_roles=associated_roles,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            availability_zone=availability_zone,
            backup_retention_period=backup_retention_period,
            ca_certificate_identifier=ca_certificate_identifier,
            character_set_name=character_set_name,
            copy_tags_to_snapshot=copy_tags_to_snapshot,
            db_cluster_identifier=db_cluster_identifier,
            db_instance_identifier=db_instance_identifier,
            db_name=db_name,
            db_parameter_group_name=db_parameter_group_name,
            db_security_groups=db_security_groups,
            db_snapshot_identifier=db_snapshot_identifier,
            db_subnet_group_name=db_subnet_group_name,
            delete_automated_backups=delete_automated_backups,
            deletion_protection=deletion_protection,
            domain=domain,
            domain_iam_role_name=domain_iam_role_name,
            enable_cloudwatch_logs_exports=enable_cloudwatch_logs_exports,
            enable_iam_database_authentication=enable_iam_database_authentication,
            enable_performance_insights=enable_performance_insights,
            engine=engine,
            engine_version=engine_version,
            iops=iops,
            kms_key_id=kms_key_id,
            license_model=license_model,
            master_username=master_username,
            master_user_password=master_user_password,
            max_allocated_storage=max_allocated_storage,
            monitoring_interval=monitoring_interval,
            monitoring_role_arn=monitoring_role_arn,
            multi_az=multi_az,
            option_group_name=option_group_name,
            performance_insights_kms_key_id=performance_insights_kms_key_id,
            performance_insights_retention_period=performance_insights_retention_period,
            port=port,
            preferred_backup_window=preferred_backup_window,
            preferred_maintenance_window=preferred_maintenance_window,
            processor_features=processor_features,
            promotion_tier=promotion_tier,
            publicly_accessible=publicly_accessible,
            source_db_instance_identifier=source_db_instance_identifier,
            source_region=source_region,
            storage_encrypted=storage_encrypted,
            storage_type=storage_type,
            tags=tags,
            timezone=timezone,
            use_default_processor_features=use_default_processor_features,
            vpc_security_groups=vpc_security_groups,
        )

        jsii.create(CfnDBInstance, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrEndpointAddress")
    def attr_endpoint_address(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint.Address
        """
        return jsii.get(self, "attrEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="attrEndpointPort")
    def attr_endpoint_port(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: Endpoint.Port
        """
        return jsii.get(self, "attrEndpointPort")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::RDS::DBInstance.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceClass")
    def db_instance_class(self) -> str:
        """``AWS::RDS::DBInstance.DBInstanceClass``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbinstanceclass
        """
        return jsii.get(self, "dbInstanceClass")

    @db_instance_class.setter
    def db_instance_class(self, value: str) -> None:
        jsii.set(self, "dbInstanceClass", value)

    @builtins.property
    @jsii.member(jsii_name="allocatedStorage")
    def allocated_storage(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.AllocatedStorage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-allocatedstorage
        """
        return jsii.get(self, "allocatedStorage")

    @allocated_storage.setter
    def allocated_storage(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "allocatedStorage", value)

    @builtins.property
    @jsii.member(jsii_name="allowMajorVersionUpgrade")
    def allow_major_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.AllowMajorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-allowmajorversionupgrade
        """
        return jsii.get(self, "allowMajorVersionUpgrade")

    @allow_major_version_upgrade.setter
    def allow_major_version_upgrade(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "allowMajorVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="associatedRoles")
    def associated_roles(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DBInstanceRoleProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::RDS::DBInstance.AssociatedRoles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-associatedroles
        """
        return jsii.get(self, "associatedRoles")

    @associated_roles.setter
    def associated_roles(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["DBInstanceRoleProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "associatedRoles", value)

    @builtins.property
    @jsii.member(jsii_name="autoMinorVersionUpgrade")
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.AutoMinorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-autominorversionupgrade
        """
        return jsii.get(self, "autoMinorVersionUpgrade")

    @auto_minor_version_upgrade.setter
    def auto_minor_version_upgrade(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "autoMinorVersionUpgrade", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.AvailabilityZone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-availabilityzone
        """
        return jsii.get(self, "availabilityZone")

    @availability_zone.setter
    def availability_zone(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="backupRetentionPeriod")
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBInstance.BackupRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-backupretentionperiod
        """
        return jsii.get(self, "backupRetentionPeriod")

    @backup_retention_period.setter
    def backup_retention_period(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "backupRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="caCertificateIdentifier")
    def ca_certificate_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.CACertificateIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-cacertificateidentifier
        """
        return jsii.get(self, "caCertificateIdentifier")

    @ca_certificate_identifier.setter
    def ca_certificate_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "caCertificateIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="characterSetName")
    def character_set_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.CharacterSetName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-charactersetname
        """
        return jsii.get(self, "characterSetName")

    @character_set_name.setter
    def character_set_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "characterSetName", value)

    @builtins.property
    @jsii.member(jsii_name="copyTagsToSnapshot")
    def copy_tags_to_snapshot(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.CopyTagsToSnapshot``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-copytagstosnapshot
        """
        return jsii.get(self, "copyTagsToSnapshot")

    @copy_tags_to_snapshot.setter
    def copy_tags_to_snapshot(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "copyTagsToSnapshot", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterIdentifier")
    def db_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbclusteridentifier
        """
        return jsii.get(self, "dbClusterIdentifier")

    @db_cluster_identifier.setter
    def db_cluster_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbClusterIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="dbInstanceIdentifier")
    def db_instance_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DBInstanceIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbinstanceidentifier
        """
        return jsii.get(self, "dbInstanceIdentifier")

    @db_instance_identifier.setter
    def db_instance_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbInstanceIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="dbName")
    def db_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DBName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbname
        """
        return jsii.get(self, "dbName")

    @db_name.setter
    def db_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbName", value)

    @builtins.property
    @jsii.member(jsii_name="dbParameterGroupName")
    def db_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DBParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbparametergroupname
        """
        return jsii.get(self, "dbParameterGroupName")

    @db_parameter_group_name.setter
    def db_parameter_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbParameterGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="dbSecurityGroups")
    def db_security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBInstance.DBSecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsecuritygroups
        """
        return jsii.get(self, "dbSecurityGroups")

    @db_security_groups.setter
    def db_security_groups(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "dbSecurityGroups", value)

    @builtins.property
    @jsii.member(jsii_name="dbSnapshotIdentifier")
    def db_snapshot_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DBSnapshotIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsnapshotidentifier
        """
        return jsii.get(self, "dbSnapshotIdentifier")

    @db_snapshot_identifier.setter
    def db_snapshot_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbSnapshotIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsubnetgroupname
        """
        return jsii.get(self, "dbSubnetGroupName")

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbSubnetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="deleteAutomatedBackups")
    def delete_automated_backups(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.DeleteAutomatedBackups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-deleteautomatedbackups
        """
        return jsii.get(self, "deleteAutomatedBackups")

    @delete_automated_backups.setter
    def delete_automated_backups(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "deleteAutomatedBackups", value)

    @builtins.property
    @jsii.member(jsii_name="deletionProtection")
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.DeletionProtection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-deletionprotection
        """
        return jsii.get(self, "deletionProtection")

    @deletion_protection.setter
    def deletion_protection(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "deletionProtection", value)

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.Domain``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-domain
        """
        return jsii.get(self, "domain")

    @domain.setter
    def domain(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "domain", value)

    @builtins.property
    @jsii.member(jsii_name="domainIamRoleName")
    def domain_iam_role_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DomainIAMRoleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-domainiamrolename
        """
        return jsii.get(self, "domainIamRoleName")

    @domain_iam_role_name.setter
    def domain_iam_role_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "domainIamRoleName", value)

    @builtins.property
    @jsii.member(jsii_name="enableCloudwatchLogsExports")
    def enable_cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBInstance.EnableCloudwatchLogsExports``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-enablecloudwatchlogsexports
        """
        return jsii.get(self, "enableCloudwatchLogsExports")

    @enable_cloudwatch_logs_exports.setter
    def enable_cloudwatch_logs_exports(
        self, value: typing.Optional[typing.List[str]]
    ) -> None:
        jsii.set(self, "enableCloudwatchLogsExports", value)

    @builtins.property
    @jsii.member(jsii_name="enableIamDatabaseAuthentication")
    def enable_iam_database_authentication(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.EnableIAMDatabaseAuthentication``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-enableiamdatabaseauthentication
        """
        return jsii.get(self, "enableIamDatabaseAuthentication")

    @enable_iam_database_authentication.setter
    def enable_iam_database_authentication(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "enableIamDatabaseAuthentication", value)

    @builtins.property
    @jsii.member(jsii_name="enablePerformanceInsights")
    def enable_performance_insights(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.EnablePerformanceInsights``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-enableperformanceinsights
        """
        return jsii.get(self, "enablePerformanceInsights")

    @enable_performance_insights.setter
    def enable_performance_insights(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "enablePerformanceInsights", value)

    @builtins.property
    @jsii.member(jsii_name="engine")
    def engine(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.Engine``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-engine
        """
        return jsii.get(self, "engine")

    @engine.setter
    def engine(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "engine", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.EngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-engineversion
        """
        return jsii.get(self, "engineVersion")

    @engine_version.setter
    def engine_version(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="iops")
    def iops(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBInstance.Iops``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-iops
        """
        return jsii.get(self, "iops")

    @iops.setter
    def iops(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "iops", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-kmskeyid
        """
        return jsii.get(self, "kmsKeyId")

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="licenseModel")
    def license_model(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.LicenseModel``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-licensemodel
        """
        return jsii.get(self, "licenseModel")

    @license_model.setter
    def license_model(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "licenseModel", value)

    @builtins.property
    @jsii.member(jsii_name="masterUsername")
    def master_username(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.MasterUsername``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-masterusername
        """
        return jsii.get(self, "masterUsername")

    @master_username.setter
    def master_username(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "masterUsername", value)

    @builtins.property
    @jsii.member(jsii_name="masterUserPassword")
    def master_user_password(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.MasterUserPassword``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-masteruserpassword
        """
        return jsii.get(self, "masterUserPassword")

    @master_user_password.setter
    def master_user_password(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "masterUserPassword", value)

    @builtins.property
    @jsii.member(jsii_name="maxAllocatedStorage")
    def max_allocated_storage(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBInstance.MaxAllocatedStorage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-maxallocatedstorage
        """
        return jsii.get(self, "maxAllocatedStorage")

    @max_allocated_storage.setter
    def max_allocated_storage(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "maxAllocatedStorage", value)

    @builtins.property
    @jsii.member(jsii_name="monitoringInterval")
    def monitoring_interval(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBInstance.MonitoringInterval``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-monitoringinterval
        """
        return jsii.get(self, "monitoringInterval")

    @monitoring_interval.setter
    def monitoring_interval(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "monitoringInterval", value)

    @builtins.property
    @jsii.member(jsii_name="monitoringRoleArn")
    def monitoring_role_arn(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.MonitoringRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-monitoringrolearn
        """
        return jsii.get(self, "monitoringRoleArn")

    @monitoring_role_arn.setter
    def monitoring_role_arn(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "monitoringRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="multiAz")
    def multi_az(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.MultiAZ``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-multiaz
        """
        return jsii.get(self, "multiAz")

    @multi_az.setter
    def multi_az(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "multiAz", value)

    @builtins.property
    @jsii.member(jsii_name="optionGroupName")
    def option_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.OptionGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-optiongroupname
        """
        return jsii.get(self, "optionGroupName")

    @option_group_name.setter
    def option_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "optionGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="performanceInsightsKmsKeyId")
    def performance_insights_kms_key_id(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.PerformanceInsightsKMSKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-performanceinsightskmskeyid
        """
        return jsii.get(self, "performanceInsightsKmsKeyId")

    @performance_insights_kms_key_id.setter
    def performance_insights_kms_key_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "performanceInsightsKmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="performanceInsightsRetentionPeriod")
    def performance_insights_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBInstance.PerformanceInsightsRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-performanceinsightsretentionperiod
        """
        return jsii.get(self, "performanceInsightsRetentionPeriod")

    @performance_insights_retention_period.setter
    def performance_insights_retention_period(
        self, value: typing.Optional[jsii.Number]
    ) -> None:
        jsii.set(self, "performanceInsightsRetentionPeriod", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-port
        """
        return jsii.get(self, "port")

    @port.setter
    def port(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="preferredBackupWindow")
    def preferred_backup_window(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.PreferredBackupWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-preferredbackupwindow
        """
        return jsii.get(self, "preferredBackupWindow")

    @preferred_backup_window.setter
    def preferred_backup_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "preferredBackupWindow", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-preferredmaintenancewindow
        """
        return jsii.get(self, "preferredMaintenanceWindow")

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="processorFeatures")
    def processor_features(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ProcessorFeatureProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::RDS::DBInstance.ProcessorFeatures``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-processorfeatures
        """
        return jsii.get(self, "processorFeatures")

    @processor_features.setter
    def processor_features(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["ProcessorFeatureProperty", _IResolvable_9ceae33e]]]],
    ) -> None:
        jsii.set(self, "processorFeatures", value)

    @builtins.property
    @jsii.member(jsii_name="promotionTier")
    def promotion_tier(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBInstance.PromotionTier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-promotiontier
        """
        return jsii.get(self, "promotionTier")

    @promotion_tier.setter
    def promotion_tier(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "promotionTier", value)

    @builtins.property
    @jsii.member(jsii_name="publiclyAccessible")
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.PubliclyAccessible``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-publiclyaccessible
        """
        return jsii.get(self, "publiclyAccessible")

    @publicly_accessible.setter
    def publicly_accessible(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "publiclyAccessible", value)

    @builtins.property
    @jsii.member(jsii_name="sourceDbInstanceIdentifier")
    def source_db_instance_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.SourceDBInstanceIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-sourcedbinstanceidentifier
        """
        return jsii.get(self, "sourceDbInstanceIdentifier")

    @source_db_instance_identifier.setter
    def source_db_instance_identifier(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "sourceDbInstanceIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="sourceRegion")
    def source_region(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.SourceRegion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-sourceregion
        """
        return jsii.get(self, "sourceRegion")

    @source_region.setter
    def source_region(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "sourceRegion", value)

    @builtins.property
    @jsii.member(jsii_name="storageEncrypted")
    def storage_encrypted(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.StorageEncrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-storageencrypted
        """
        return jsii.get(self, "storageEncrypted")

    @storage_encrypted.setter
    def storage_encrypted(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "storageEncrypted", value)

    @builtins.property
    @jsii.member(jsii_name="storageType")
    def storage_type(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.StorageType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-storagetype
        """
        return jsii.get(self, "storageType")

    @storage_type.setter
    def storage_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "storageType", value)

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.Timezone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-timezone
        """
        return jsii.get(self, "timezone")

    @timezone.setter
    def timezone(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "timezone", value)

    @builtins.property
    @jsii.member(jsii_name="useDefaultProcessorFeatures")
    def use_default_processor_features(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.UseDefaultProcessorFeatures``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-usedefaultprocessorfeatures
        """
        return jsii.get(self, "useDefaultProcessorFeatures")

    @use_default_processor_features.setter
    def use_default_processor_features(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "useDefaultProcessorFeatures", value)

    @builtins.property
    @jsii.member(jsii_name="vpcSecurityGroups")
    def vpc_security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBInstance.VPCSecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-vpcsecuritygroups
        """
        return jsii.get(self, "vpcSecurityGroups")

    @vpc_security_groups.setter
    def vpc_security_groups(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "vpcSecurityGroups", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_rds.CfnDBInstance.DBInstanceRoleProperty",
        jsii_struct_bases=[],
        name_mapping={"feature_name": "featureName", "role_arn": "roleArn"},
    )
    class DBInstanceRoleProperty:
        def __init__(self, *, feature_name: str, role_arn: str) -> None:
            """
            :param feature_name: ``CfnDBInstance.DBInstanceRoleProperty.FeatureName``.
            :param role_arn: ``CfnDBInstance.DBInstanceRoleProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-dbinstancerole.html
            """
            self._values = {
                "feature_name": feature_name,
                "role_arn": role_arn,
            }

        @builtins.property
        def feature_name(self) -> str:
            """``CfnDBInstance.DBInstanceRoleProperty.FeatureName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-dbinstancerole.html#cfn-rds-dbinstance-dbinstancerole-featurename
            """
            return self._values.get("feature_name")

        @builtins.property
        def role_arn(self) -> str:
            """``CfnDBInstance.DBInstanceRoleProperty.RoleArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-dbinstancerole.html#cfn-rds-dbinstance-dbinstancerole-rolearn
            """
            return self._values.get("role_arn")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DBInstanceRoleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_rds.CfnDBInstance.ProcessorFeatureProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class ProcessorFeatureProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[str] = None,
            value: typing.Optional[str] = None,
        ) -> None:
            """
            :param name: ``CfnDBInstance.ProcessorFeatureProperty.Name``.
            :param value: ``CfnDBInstance.ProcessorFeatureProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-processorfeature.html
            """
            self._values = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnDBInstance.ProcessorFeatureProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-processorfeature.html#cfn-rds-dbinstance-processorfeature-name
            """
            return self._values.get("name")

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnDBInstance.ProcessorFeatureProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-processorfeature.html#cfn-rds-dbinstance-processorfeature-value
            """
            return self._values.get("value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProcessorFeatureProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.CfnDBInstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_instance_class": "dbInstanceClass",
        "allocated_storage": "allocatedStorage",
        "allow_major_version_upgrade": "allowMajorVersionUpgrade",
        "associated_roles": "associatedRoles",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "backup_retention_period": "backupRetentionPeriod",
        "ca_certificate_identifier": "caCertificateIdentifier",
        "character_set_name": "characterSetName",
        "copy_tags_to_snapshot": "copyTagsToSnapshot",
        "db_cluster_identifier": "dbClusterIdentifier",
        "db_instance_identifier": "dbInstanceIdentifier",
        "db_name": "dbName",
        "db_parameter_group_name": "dbParameterGroupName",
        "db_security_groups": "dbSecurityGroups",
        "db_snapshot_identifier": "dbSnapshotIdentifier",
        "db_subnet_group_name": "dbSubnetGroupName",
        "delete_automated_backups": "deleteAutomatedBackups",
        "deletion_protection": "deletionProtection",
        "domain": "domain",
        "domain_iam_role_name": "domainIamRoleName",
        "enable_cloudwatch_logs_exports": "enableCloudwatchLogsExports",
        "enable_iam_database_authentication": "enableIamDatabaseAuthentication",
        "enable_performance_insights": "enablePerformanceInsights",
        "engine": "engine",
        "engine_version": "engineVersion",
        "iops": "iops",
        "kms_key_id": "kmsKeyId",
        "license_model": "licenseModel",
        "master_username": "masterUsername",
        "master_user_password": "masterUserPassword",
        "max_allocated_storage": "maxAllocatedStorage",
        "monitoring_interval": "monitoringInterval",
        "monitoring_role_arn": "monitoringRoleArn",
        "multi_az": "multiAz",
        "option_group_name": "optionGroupName",
        "performance_insights_kms_key_id": "performanceInsightsKmsKeyId",
        "performance_insights_retention_period": "performanceInsightsRetentionPeriod",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "processor_features": "processorFeatures",
        "promotion_tier": "promotionTier",
        "publicly_accessible": "publiclyAccessible",
        "source_db_instance_identifier": "sourceDbInstanceIdentifier",
        "source_region": "sourceRegion",
        "storage_encrypted": "storageEncrypted",
        "storage_type": "storageType",
        "tags": "tags",
        "timezone": "timezone",
        "use_default_processor_features": "useDefaultProcessorFeatures",
        "vpc_security_groups": "vpcSecurityGroups",
    },
)
class CfnDBInstanceProps:
    def __init__(
        self,
        *,
        db_instance_class: str,
        allocated_storage: typing.Optional[str] = None,
        allow_major_version_upgrade: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        associated_roles: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDBInstance.DBInstanceRoleProperty", _IResolvable_9ceae33e]]]] = None,
        auto_minor_version_upgrade: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        availability_zone: typing.Optional[str] = None,
        backup_retention_period: typing.Optional[jsii.Number] = None,
        ca_certificate_identifier: typing.Optional[str] = None,
        character_set_name: typing.Optional[str] = None,
        copy_tags_to_snapshot: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        db_cluster_identifier: typing.Optional[str] = None,
        db_instance_identifier: typing.Optional[str] = None,
        db_name: typing.Optional[str] = None,
        db_parameter_group_name: typing.Optional[str] = None,
        db_security_groups: typing.Optional[typing.List[str]] = None,
        db_snapshot_identifier: typing.Optional[str] = None,
        db_subnet_group_name: typing.Optional[str] = None,
        delete_automated_backups: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        deletion_protection: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        domain: typing.Optional[str] = None,
        domain_iam_role_name: typing.Optional[str] = None,
        enable_cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        enable_iam_database_authentication: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        enable_performance_insights: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        engine: typing.Optional[str] = None,
        engine_version: typing.Optional[str] = None,
        iops: typing.Optional[jsii.Number] = None,
        kms_key_id: typing.Optional[str] = None,
        license_model: typing.Optional[str] = None,
        master_username: typing.Optional[str] = None,
        master_user_password: typing.Optional[str] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[jsii.Number] = None,
        monitoring_role_arn: typing.Optional[str] = None,
        multi_az: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        option_group_name: typing.Optional[str] = None,
        performance_insights_kms_key_id: typing.Optional[str] = None,
        performance_insights_retention_period: typing.Optional[jsii.Number] = None,
        port: typing.Optional[str] = None,
        preferred_backup_window: typing.Optional[str] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        processor_features: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDBInstance.ProcessorFeatureProperty", _IResolvable_9ceae33e]]]] = None,
        promotion_tier: typing.Optional[jsii.Number] = None,
        publicly_accessible: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        source_db_instance_identifier: typing.Optional[str] = None,
        source_region: typing.Optional[str] = None,
        storage_encrypted: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        storage_type: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
        timezone: typing.Optional[str] = None,
        use_default_processor_features: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        vpc_security_groups: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::RDS::DBInstance``.

        :param db_instance_class: ``AWS::RDS::DBInstance.DBInstanceClass``.
        :param allocated_storage: ``AWS::RDS::DBInstance.AllocatedStorage``.
        :param allow_major_version_upgrade: ``AWS::RDS::DBInstance.AllowMajorVersionUpgrade``.
        :param associated_roles: ``AWS::RDS::DBInstance.AssociatedRoles``.
        :param auto_minor_version_upgrade: ``AWS::RDS::DBInstance.AutoMinorVersionUpgrade``.
        :param availability_zone: ``AWS::RDS::DBInstance.AvailabilityZone``.
        :param backup_retention_period: ``AWS::RDS::DBInstance.BackupRetentionPeriod``.
        :param ca_certificate_identifier: ``AWS::RDS::DBInstance.CACertificateIdentifier``.
        :param character_set_name: ``AWS::RDS::DBInstance.CharacterSetName``.
        :param copy_tags_to_snapshot: ``AWS::RDS::DBInstance.CopyTagsToSnapshot``.
        :param db_cluster_identifier: ``AWS::RDS::DBInstance.DBClusterIdentifier``.
        :param db_instance_identifier: ``AWS::RDS::DBInstance.DBInstanceIdentifier``.
        :param db_name: ``AWS::RDS::DBInstance.DBName``.
        :param db_parameter_group_name: ``AWS::RDS::DBInstance.DBParameterGroupName``.
        :param db_security_groups: ``AWS::RDS::DBInstance.DBSecurityGroups``.
        :param db_snapshot_identifier: ``AWS::RDS::DBInstance.DBSnapshotIdentifier``.
        :param db_subnet_group_name: ``AWS::RDS::DBInstance.DBSubnetGroupName``.
        :param delete_automated_backups: ``AWS::RDS::DBInstance.DeleteAutomatedBackups``.
        :param deletion_protection: ``AWS::RDS::DBInstance.DeletionProtection``.
        :param domain: ``AWS::RDS::DBInstance.Domain``.
        :param domain_iam_role_name: ``AWS::RDS::DBInstance.DomainIAMRoleName``.
        :param enable_cloudwatch_logs_exports: ``AWS::RDS::DBInstance.EnableCloudwatchLogsExports``.
        :param enable_iam_database_authentication: ``AWS::RDS::DBInstance.EnableIAMDatabaseAuthentication``.
        :param enable_performance_insights: ``AWS::RDS::DBInstance.EnablePerformanceInsights``.
        :param engine: ``AWS::RDS::DBInstance.Engine``.
        :param engine_version: ``AWS::RDS::DBInstance.EngineVersion``.
        :param iops: ``AWS::RDS::DBInstance.Iops``.
        :param kms_key_id: ``AWS::RDS::DBInstance.KmsKeyId``.
        :param license_model: ``AWS::RDS::DBInstance.LicenseModel``.
        :param master_username: ``AWS::RDS::DBInstance.MasterUsername``.
        :param master_user_password: ``AWS::RDS::DBInstance.MasterUserPassword``.
        :param max_allocated_storage: ``AWS::RDS::DBInstance.MaxAllocatedStorage``.
        :param monitoring_interval: ``AWS::RDS::DBInstance.MonitoringInterval``.
        :param monitoring_role_arn: ``AWS::RDS::DBInstance.MonitoringRoleArn``.
        :param multi_az: ``AWS::RDS::DBInstance.MultiAZ``.
        :param option_group_name: ``AWS::RDS::DBInstance.OptionGroupName``.
        :param performance_insights_kms_key_id: ``AWS::RDS::DBInstance.PerformanceInsightsKMSKeyId``.
        :param performance_insights_retention_period: ``AWS::RDS::DBInstance.PerformanceInsightsRetentionPeriod``.
        :param port: ``AWS::RDS::DBInstance.Port``.
        :param preferred_backup_window: ``AWS::RDS::DBInstance.PreferredBackupWindow``.
        :param preferred_maintenance_window: ``AWS::RDS::DBInstance.PreferredMaintenanceWindow``.
        :param processor_features: ``AWS::RDS::DBInstance.ProcessorFeatures``.
        :param promotion_tier: ``AWS::RDS::DBInstance.PromotionTier``.
        :param publicly_accessible: ``AWS::RDS::DBInstance.PubliclyAccessible``.
        :param source_db_instance_identifier: ``AWS::RDS::DBInstance.SourceDBInstanceIdentifier``.
        :param source_region: ``AWS::RDS::DBInstance.SourceRegion``.
        :param storage_encrypted: ``AWS::RDS::DBInstance.StorageEncrypted``.
        :param storage_type: ``AWS::RDS::DBInstance.StorageType``.
        :param tags: ``AWS::RDS::DBInstance.Tags``.
        :param timezone: ``AWS::RDS::DBInstance.Timezone``.
        :param use_default_processor_features: ``AWS::RDS::DBInstance.UseDefaultProcessorFeatures``.
        :param vpc_security_groups: ``AWS::RDS::DBInstance.VPCSecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html
        """
        self._values = {
            "db_instance_class": db_instance_class,
        }
        if allocated_storage is not None:
            self._values["allocated_storage"] = allocated_storage
        if allow_major_version_upgrade is not None:
            self._values["allow_major_version_upgrade"] = allow_major_version_upgrade
        if associated_roles is not None:
            self._values["associated_roles"] = associated_roles
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if backup_retention_period is not None:
            self._values["backup_retention_period"] = backup_retention_period
        if ca_certificate_identifier is not None:
            self._values["ca_certificate_identifier"] = ca_certificate_identifier
        if character_set_name is not None:
            self._values["character_set_name"] = character_set_name
        if copy_tags_to_snapshot is not None:
            self._values["copy_tags_to_snapshot"] = copy_tags_to_snapshot
        if db_cluster_identifier is not None:
            self._values["db_cluster_identifier"] = db_cluster_identifier
        if db_instance_identifier is not None:
            self._values["db_instance_identifier"] = db_instance_identifier
        if db_name is not None:
            self._values["db_name"] = db_name
        if db_parameter_group_name is not None:
            self._values["db_parameter_group_name"] = db_parameter_group_name
        if db_security_groups is not None:
            self._values["db_security_groups"] = db_security_groups
        if db_snapshot_identifier is not None:
            self._values["db_snapshot_identifier"] = db_snapshot_identifier
        if db_subnet_group_name is not None:
            self._values["db_subnet_group_name"] = db_subnet_group_name
        if delete_automated_backups is not None:
            self._values["delete_automated_backups"] = delete_automated_backups
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if domain is not None:
            self._values["domain"] = domain
        if domain_iam_role_name is not None:
            self._values["domain_iam_role_name"] = domain_iam_role_name
        if enable_cloudwatch_logs_exports is not None:
            self._values["enable_cloudwatch_logs_exports"] = enable_cloudwatch_logs_exports
        if enable_iam_database_authentication is not None:
            self._values["enable_iam_database_authentication"] = enable_iam_database_authentication
        if enable_performance_insights is not None:
            self._values["enable_performance_insights"] = enable_performance_insights
        if engine is not None:
            self._values["engine"] = engine
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if iops is not None:
            self._values["iops"] = iops
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if license_model is not None:
            self._values["license_model"] = license_model
        if master_username is not None:
            self._values["master_username"] = master_username
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password
        if max_allocated_storage is not None:
            self._values["max_allocated_storage"] = max_allocated_storage
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_role_arn is not None:
            self._values["monitoring_role_arn"] = monitoring_role_arn
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if option_group_name is not None:
            self._values["option_group_name"] = option_group_name
        if performance_insights_kms_key_id is not None:
            self._values["performance_insights_kms_key_id"] = performance_insights_kms_key_id
        if performance_insights_retention_period is not None:
            self._values["performance_insights_retention_period"] = performance_insights_retention_period
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if processor_features is not None:
            self._values["processor_features"] = processor_features
        if promotion_tier is not None:
            self._values["promotion_tier"] = promotion_tier
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if source_db_instance_identifier is not None:
            self._values["source_db_instance_identifier"] = source_db_instance_identifier
        if source_region is not None:
            self._values["source_region"] = source_region
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if tags is not None:
            self._values["tags"] = tags
        if timezone is not None:
            self._values["timezone"] = timezone
        if use_default_processor_features is not None:
            self._values["use_default_processor_features"] = use_default_processor_features
        if vpc_security_groups is not None:
            self._values["vpc_security_groups"] = vpc_security_groups

    @builtins.property
    def db_instance_class(self) -> str:
        """``AWS::RDS::DBInstance.DBInstanceClass``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbinstanceclass
        """
        return self._values.get("db_instance_class")

    @builtins.property
    def allocated_storage(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.AllocatedStorage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-allocatedstorage
        """
        return self._values.get("allocated_storage")

    @builtins.property
    def allow_major_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.AllowMajorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-allowmajorversionupgrade
        """
        return self._values.get("allow_major_version_upgrade")

    @builtins.property
    def associated_roles(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDBInstance.DBInstanceRoleProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::RDS::DBInstance.AssociatedRoles``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-associatedroles
        """
        return self._values.get("associated_roles")

    @builtins.property
    def auto_minor_version_upgrade(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.AutoMinorVersionUpgrade``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-autominorversionupgrade
        """
        return self._values.get("auto_minor_version_upgrade")

    @builtins.property
    def availability_zone(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.AvailabilityZone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-availabilityzone
        """
        return self._values.get("availability_zone")

    @builtins.property
    def backup_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBInstance.BackupRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-backupretentionperiod
        """
        return self._values.get("backup_retention_period")

    @builtins.property
    def ca_certificate_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.CACertificateIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-cacertificateidentifier
        """
        return self._values.get("ca_certificate_identifier")

    @builtins.property
    def character_set_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.CharacterSetName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-charactersetname
        """
        return self._values.get("character_set_name")

    @builtins.property
    def copy_tags_to_snapshot(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.CopyTagsToSnapshot``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-copytagstosnapshot
        """
        return self._values.get("copy_tags_to_snapshot")

    @builtins.property
    def db_cluster_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DBClusterIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbclusteridentifier
        """
        return self._values.get("db_cluster_identifier")

    @builtins.property
    def db_instance_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DBInstanceIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbinstanceidentifier
        """
        return self._values.get("db_instance_identifier")

    @builtins.property
    def db_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DBName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbname
        """
        return self._values.get("db_name")

    @builtins.property
    def db_parameter_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DBParameterGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbparametergroupname
        """
        return self._values.get("db_parameter_group_name")

    @builtins.property
    def db_security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBInstance.DBSecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsecuritygroups
        """
        return self._values.get("db_security_groups")

    @builtins.property
    def db_snapshot_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DBSnapshotIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsnapshotidentifier
        """
        return self._values.get("db_snapshot_identifier")

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsubnetgroupname
        """
        return self._values.get("db_subnet_group_name")

    @builtins.property
    def delete_automated_backups(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.DeleteAutomatedBackups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-deleteautomatedbackups
        """
        return self._values.get("delete_automated_backups")

    @builtins.property
    def deletion_protection(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.DeletionProtection``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-deletionprotection
        """
        return self._values.get("deletion_protection")

    @builtins.property
    def domain(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.Domain``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-domain
        """
        return self._values.get("domain")

    @builtins.property
    def domain_iam_role_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.DomainIAMRoleName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-domainiamrolename
        """
        return self._values.get("domain_iam_role_name")

    @builtins.property
    def enable_cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBInstance.EnableCloudwatchLogsExports``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-enablecloudwatchlogsexports
        """
        return self._values.get("enable_cloudwatch_logs_exports")

    @builtins.property
    def enable_iam_database_authentication(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.EnableIAMDatabaseAuthentication``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-enableiamdatabaseauthentication
        """
        return self._values.get("enable_iam_database_authentication")

    @builtins.property
    def enable_performance_insights(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.EnablePerformanceInsights``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-enableperformanceinsights
        """
        return self._values.get("enable_performance_insights")

    @builtins.property
    def engine(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.Engine``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-engine
        """
        return self._values.get("engine")

    @builtins.property
    def engine_version(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.EngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-engineversion
        """
        return self._values.get("engine_version")

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBInstance.Iops``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-iops
        """
        return self._values.get("iops")

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.KmsKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-kmskeyid
        """
        return self._values.get("kms_key_id")

    @builtins.property
    def license_model(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.LicenseModel``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-licensemodel
        """
        return self._values.get("license_model")

    @builtins.property
    def master_username(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.MasterUsername``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-masterusername
        """
        return self._values.get("master_username")

    @builtins.property
    def master_user_password(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.MasterUserPassword``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-masteruserpassword
        """
        return self._values.get("master_user_password")

    @builtins.property
    def max_allocated_storage(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBInstance.MaxAllocatedStorage``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-maxallocatedstorage
        """
        return self._values.get("max_allocated_storage")

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBInstance.MonitoringInterval``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-monitoringinterval
        """
        return self._values.get("monitoring_interval")

    @builtins.property
    def monitoring_role_arn(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.MonitoringRoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-monitoringrolearn
        """
        return self._values.get("monitoring_role_arn")

    @builtins.property
    def multi_az(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.MultiAZ``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-multiaz
        """
        return self._values.get("multi_az")

    @builtins.property
    def option_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.OptionGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-optiongroupname
        """
        return self._values.get("option_group_name")

    @builtins.property
    def performance_insights_kms_key_id(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.PerformanceInsightsKMSKeyId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-performanceinsightskmskeyid
        """
        return self._values.get("performance_insights_kms_key_id")

    @builtins.property
    def performance_insights_retention_period(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBInstance.PerformanceInsightsRetentionPeriod``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-performanceinsightsretentionperiod
        """
        return self._values.get("performance_insights_retention_period")

    @builtins.property
    def port(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.Port``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-port
        """
        return self._values.get("port")

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.PreferredBackupWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-preferredbackupwindow
        """
        return self._values.get("preferred_backup_window")

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.PreferredMaintenanceWindow``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-preferredmaintenancewindow
        """
        return self._values.get("preferred_maintenance_window")

    @builtins.property
    def processor_features(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDBInstance.ProcessorFeatureProperty", _IResolvable_9ceae33e]]]]:
        """``AWS::RDS::DBInstance.ProcessorFeatures``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-processorfeatures
        """
        return self._values.get("processor_features")

    @builtins.property
    def promotion_tier(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBInstance.PromotionTier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-promotiontier
        """
        return self._values.get("promotion_tier")

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.PubliclyAccessible``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-publiclyaccessible
        """
        return self._values.get("publicly_accessible")

    @builtins.property
    def source_db_instance_identifier(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.SourceDBInstanceIdentifier``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-sourcedbinstanceidentifier
        """
        return self._values.get("source_db_instance_identifier")

    @builtins.property
    def source_region(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.SourceRegion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-sourceregion
        """
        return self._values.get("source_region")

    @builtins.property
    def storage_encrypted(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.StorageEncrypted``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-storageencrypted
        """
        return self._values.get("storage_encrypted")

    @builtins.property
    def storage_type(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.StorageType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-storagetype
        """
        return self._values.get("storage_type")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::RDS::DBInstance.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-tags
        """
        return self._values.get("tags")

    @builtins.property
    def timezone(self) -> typing.Optional[str]:
        """``AWS::RDS::DBInstance.Timezone``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-timezone
        """
        return self._values.get("timezone")

    @builtins.property
    def use_default_processor_features(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBInstance.UseDefaultProcessorFeatures``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-usedefaultprocessorfeatures
        """
        return self._values.get("use_default_processor_features")

    @builtins.property
    def vpc_security_groups(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBInstance.VPCSecurityGroups``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-vpcsecuritygroups
        """
        return self._values.get("vpc_security_groups")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBParameterGroup(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.CfnDBParameterGroup",
):
    """A CloudFormation ``AWS::RDS::DBParameterGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::RDS::DBParameterGroup
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        description: str,
        family: str,
        parameters: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::RDS::DBParameterGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: ``AWS::RDS::DBParameterGroup.Description``.
        :param family: ``AWS::RDS::DBParameterGroup.Family``.
        :param parameters: ``AWS::RDS::DBParameterGroup.Parameters``.
        :param tags: ``AWS::RDS::DBParameterGroup.Tags``.
        """
        props = CfnDBParameterGroupProps(
            description=description, family=family, parameters=parameters, tags=tags
        )

        jsii.create(CfnDBParameterGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::RDS::DBParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html#cfn-rds-dbparametergroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> str:
        """``AWS::RDS::DBParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html#cfn-rds-dbparametergroup-description
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: str) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="family")
    def family(self) -> str:
        """``AWS::RDS::DBParameterGroup.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html#cfn-rds-dbparametergroup-family
        """
        return jsii.get(self, "family")

    @family.setter
    def family(self, value: str) -> None:
        jsii.set(self, "family", value)

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]:
        """``AWS::RDS::DBParameterGroup.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html#cfn-rds-dbparametergroup-parameters
        """
        return jsii.get(self, "parameters")

    @parameters.setter
    def parameters(
        self,
        value: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]],
    ) -> None:
        jsii.set(self, "parameters", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.CfnDBParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "family": "family",
        "parameters": "parameters",
        "tags": "tags",
    },
)
class CfnDBParameterGroupProps:
    def __init__(
        self,
        *,
        description: str,
        family: str,
        parameters: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::RDS::DBParameterGroup``.

        :param description: ``AWS::RDS::DBParameterGroup.Description``.
        :param family: ``AWS::RDS::DBParameterGroup.Family``.
        :param parameters: ``AWS::RDS::DBParameterGroup.Parameters``.
        :param tags: ``AWS::RDS::DBParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html
        """
        self._values = {
            "description": description,
            "family": family,
        }
        if parameters is not None:
            self._values["parameters"] = parameters
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def description(self) -> str:
        """``AWS::RDS::DBParameterGroup.Description``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html#cfn-rds-dbparametergroup-description
        """
        return self._values.get("description")

    @builtins.property
    def family(self) -> str:
        """``AWS::RDS::DBParameterGroup.Family``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html#cfn-rds-dbparametergroup-family
        """
        return self._values.get("family")

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.Mapping[str, str]]]:
        """``AWS::RDS::DBParameterGroup.Parameters``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html#cfn-rds-dbparametergroup-parameters
        """
        return self._values.get("parameters")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::RDS::DBParameterGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html#cfn-rds-dbparametergroup-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBProxy(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.CfnDBProxy",
):
    """A CloudFormation ``AWS::RDS::DBProxy``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html
    cloudformationResource:
    :cloudformationResource:: AWS::RDS::DBProxy
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        auth: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["AuthFormatProperty", _IResolvable_9ceae33e]]],
        db_proxy_name: str,
        engine_family: str,
        role_arn: str,
        vpc_subnet_ids: typing.List[str],
        debug_logging: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        idle_client_timeout: typing.Optional[jsii.Number] = None,
        require_tls: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List["TagFormatProperty"]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Create a new ``AWS::RDS::DBProxy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auth: ``AWS::RDS::DBProxy.Auth``.
        :param db_proxy_name: ``AWS::RDS::DBProxy.DBProxyName``.
        :param engine_family: ``AWS::RDS::DBProxy.EngineFamily``.
        :param role_arn: ``AWS::RDS::DBProxy.RoleArn``.
        :param vpc_subnet_ids: ``AWS::RDS::DBProxy.VpcSubnetIds``.
        :param debug_logging: ``AWS::RDS::DBProxy.DebugLogging``.
        :param idle_client_timeout: ``AWS::RDS::DBProxy.IdleClientTimeout``.
        :param require_tls: ``AWS::RDS::DBProxy.RequireTLS``.
        :param tags: ``AWS::RDS::DBProxy.Tags``.
        :param vpc_security_group_ids: ``AWS::RDS::DBProxy.VpcSecurityGroupIds``.
        """
        props = CfnDBProxyProps(
            auth=auth,
            db_proxy_name=db_proxy_name,
            engine_family=engine_family,
            role_arn=role_arn,
            vpc_subnet_ids=vpc_subnet_ids,
            debug_logging=debug_logging,
            idle_client_timeout=idle_client_timeout,
            require_tls=require_tls,
            tags=tags,
            vpc_security_group_ids=vpc_security_group_ids,
        )

        jsii.create(CfnDBProxy, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrDbProxyArn")
    def attr_db_proxy_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: DBProxyArn
        """
        return jsii.get(self, "attrDbProxyArn")

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
    @jsii.member(jsii_name="auth")
    def auth(
        self,
    ) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["AuthFormatProperty", _IResolvable_9ceae33e]]]:
        """``AWS::RDS::DBProxy.Auth``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-auth
        """
        return jsii.get(self, "auth")

    @auth.setter
    def auth(
        self,
        value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["AuthFormatProperty", _IResolvable_9ceae33e]]],
    ) -> None:
        jsii.set(self, "auth", value)

    @builtins.property
    @jsii.member(jsii_name="dbProxyName")
    def db_proxy_name(self) -> str:
        """``AWS::RDS::DBProxy.DBProxyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-dbproxyname
        """
        return jsii.get(self, "dbProxyName")

    @db_proxy_name.setter
    def db_proxy_name(self, value: str) -> None:
        jsii.set(self, "dbProxyName", value)

    @builtins.property
    @jsii.member(jsii_name="engineFamily")
    def engine_family(self) -> str:
        """``AWS::RDS::DBProxy.EngineFamily``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-enginefamily
        """
        return jsii.get(self, "engineFamily")

    @engine_family.setter
    def engine_family(self, value: str) -> None:
        jsii.set(self, "engineFamily", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> str:
        """``AWS::RDS::DBProxy.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-rolearn
        """
        return jsii.get(self, "roleArn")

    @role_arn.setter
    def role_arn(self, value: str) -> None:
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="vpcSubnetIds")
    def vpc_subnet_ids(self) -> typing.List[str]:
        """``AWS::RDS::DBProxy.VpcSubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-vpcsubnetids
        """
        return jsii.get(self, "vpcSubnetIds")

    @vpc_subnet_ids.setter
    def vpc_subnet_ids(self, value: typing.List[str]) -> None:
        jsii.set(self, "vpcSubnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="debugLogging")
    def debug_logging(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBProxy.DebugLogging``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-debuglogging
        """
        return jsii.get(self, "debugLogging")

    @debug_logging.setter
    def debug_logging(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "debugLogging", value)

    @builtins.property
    @jsii.member(jsii_name="idleClientTimeout")
    def idle_client_timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBProxy.IdleClientTimeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-idleclienttimeout
        """
        return jsii.get(self, "idleClientTimeout")

    @idle_client_timeout.setter
    def idle_client_timeout(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "idleClientTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="requireTls")
    def require_tls(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBProxy.RequireTLS``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-requiretls
        """
        return jsii.get(self, "requireTls")

    @require_tls.setter
    def require_tls(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "requireTls", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["TagFormatProperty"]]:
        """``AWS::RDS::DBProxy.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-tags
        """
        return jsii.get(self, "tags")

    @tags.setter
    def tags(self, value: typing.Optional[typing.List["TagFormatProperty"]]) -> None:
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="vpcSecurityGroupIds")
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBProxy.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-vpcsecuritygroupids
        """
        return jsii.get(self, "vpcSecurityGroupIds")

    @vpc_security_group_ids.setter
    def vpc_security_group_ids(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "vpcSecurityGroupIds", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_rds.CfnDBProxy.AuthFormatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auth_scheme": "authScheme",
            "description": "description",
            "iam_auth": "iamAuth",
            "secret_arn": "secretArn",
            "user_name": "userName",
        },
    )
    class AuthFormatProperty:
        def __init__(
            self,
            *,
            auth_scheme: typing.Optional[str] = None,
            description: typing.Optional[str] = None,
            iam_auth: typing.Optional[str] = None,
            secret_arn: typing.Optional[str] = None,
            user_name: typing.Optional[str] = None,
        ) -> None:
            """
            :param auth_scheme: ``CfnDBProxy.AuthFormatProperty.AuthScheme``.
            :param description: ``CfnDBProxy.AuthFormatProperty.Description``.
            :param iam_auth: ``CfnDBProxy.AuthFormatProperty.IAMAuth``.
            :param secret_arn: ``CfnDBProxy.AuthFormatProperty.SecretArn``.
            :param user_name: ``CfnDBProxy.AuthFormatProperty.UserName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-authformat.html
            """
            self._values = {}
            if auth_scheme is not None:
                self._values["auth_scheme"] = auth_scheme
            if description is not None:
                self._values["description"] = description
            if iam_auth is not None:
                self._values["iam_auth"] = iam_auth
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if user_name is not None:
                self._values["user_name"] = user_name

        @builtins.property
        def auth_scheme(self) -> typing.Optional[str]:
            """``CfnDBProxy.AuthFormatProperty.AuthScheme``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-authformat.html#cfn-rds-dbproxy-authformat-authscheme
            """
            return self._values.get("auth_scheme")

        @builtins.property
        def description(self) -> typing.Optional[str]:
            """``CfnDBProxy.AuthFormatProperty.Description``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-authformat.html#cfn-rds-dbproxy-authformat-description
            """
            return self._values.get("description")

        @builtins.property
        def iam_auth(self) -> typing.Optional[str]:
            """``CfnDBProxy.AuthFormatProperty.IAMAuth``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-authformat.html#cfn-rds-dbproxy-authformat-iamauth
            """
            return self._values.get("iam_auth")

        @builtins.property
        def secret_arn(self) -> typing.Optional[str]:
            """``CfnDBProxy.AuthFormatProperty.SecretArn``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-authformat.html#cfn-rds-dbproxy-authformat-secretarn
            """
            return self._values.get("secret_arn")

        @builtins.property
        def user_name(self) -> typing.Optional[str]:
            """``CfnDBProxy.AuthFormatProperty.UserName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-authformat.html#cfn-rds-dbproxy-authformat-username
            """
            return self._values.get("user_name")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AuthFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_rds.CfnDBProxy.TagFormatProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagFormatProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[str] = None,
            value: typing.Optional[str] = None,
        ) -> None:
            """
            :param key: ``CfnDBProxy.TagFormatProperty.Key``.
            :param value: ``CfnDBProxy.TagFormatProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-tagformat.html
            """
            self._values = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[str]:
            """``CfnDBProxy.TagFormatProperty.Key``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-tagformat.html#cfn-rds-dbproxy-tagformat-key
            """
            return self._values.get("key")

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnDBProxy.TagFormatProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxy-tagformat.html#cfn-rds-dbproxy-tagformat-value
            """
            return self._values.get("value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.CfnDBProxyProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth": "auth",
        "db_proxy_name": "dbProxyName",
        "engine_family": "engineFamily",
        "role_arn": "roleArn",
        "vpc_subnet_ids": "vpcSubnetIds",
        "debug_logging": "debugLogging",
        "idle_client_timeout": "idleClientTimeout",
        "require_tls": "requireTls",
        "tags": "tags",
        "vpc_security_group_ids": "vpcSecurityGroupIds",
    },
)
class CfnDBProxyProps:
    def __init__(
        self,
        *,
        auth: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDBProxy.AuthFormatProperty", _IResolvable_9ceae33e]]],
        db_proxy_name: str,
        engine_family: str,
        role_arn: str,
        vpc_subnet_ids: typing.List[str],
        debug_logging: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        idle_client_timeout: typing.Optional[jsii.Number] = None,
        require_tls: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        tags: typing.Optional[typing.List["CfnDBProxy.TagFormatProperty"]] = None,
        vpc_security_group_ids: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::RDS::DBProxy``.

        :param auth: ``AWS::RDS::DBProxy.Auth``.
        :param db_proxy_name: ``AWS::RDS::DBProxy.DBProxyName``.
        :param engine_family: ``AWS::RDS::DBProxy.EngineFamily``.
        :param role_arn: ``AWS::RDS::DBProxy.RoleArn``.
        :param vpc_subnet_ids: ``AWS::RDS::DBProxy.VpcSubnetIds``.
        :param debug_logging: ``AWS::RDS::DBProxy.DebugLogging``.
        :param idle_client_timeout: ``AWS::RDS::DBProxy.IdleClientTimeout``.
        :param require_tls: ``AWS::RDS::DBProxy.RequireTLS``.
        :param tags: ``AWS::RDS::DBProxy.Tags``.
        :param vpc_security_group_ids: ``AWS::RDS::DBProxy.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html
        """
        self._values = {
            "auth": auth,
            "db_proxy_name": db_proxy_name,
            "engine_family": engine_family,
            "role_arn": role_arn,
            "vpc_subnet_ids": vpc_subnet_ids,
        }
        if debug_logging is not None:
            self._values["debug_logging"] = debug_logging
        if idle_client_timeout is not None:
            self._values["idle_client_timeout"] = idle_client_timeout
        if require_tls is not None:
            self._values["require_tls"] = require_tls
        if tags is not None:
            self._values["tags"] = tags
        if vpc_security_group_ids is not None:
            self._values["vpc_security_group_ids"] = vpc_security_group_ids

    @builtins.property
    def auth(
        self,
    ) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDBProxy.AuthFormatProperty", _IResolvable_9ceae33e]]]:
        """``AWS::RDS::DBProxy.Auth``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-auth
        """
        return self._values.get("auth")

    @builtins.property
    def db_proxy_name(self) -> str:
        """``AWS::RDS::DBProxy.DBProxyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-dbproxyname
        """
        return self._values.get("db_proxy_name")

    @builtins.property
    def engine_family(self) -> str:
        """``AWS::RDS::DBProxy.EngineFamily``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-enginefamily
        """
        return self._values.get("engine_family")

    @builtins.property
    def role_arn(self) -> str:
        """``AWS::RDS::DBProxy.RoleArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-rolearn
        """
        return self._values.get("role_arn")

    @builtins.property
    def vpc_subnet_ids(self) -> typing.List[str]:
        """``AWS::RDS::DBProxy.VpcSubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-vpcsubnetids
        """
        return self._values.get("vpc_subnet_ids")

    @builtins.property
    def debug_logging(
        self,
    ) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBProxy.DebugLogging``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-debuglogging
        """
        return self._values.get("debug_logging")

    @builtins.property
    def idle_client_timeout(self) -> typing.Optional[jsii.Number]:
        """``AWS::RDS::DBProxy.IdleClientTimeout``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-idleclienttimeout
        """
        return self._values.get("idle_client_timeout")

    @builtins.property
    def require_tls(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBProxy.RequireTLS``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-requiretls
        """
        return self._values.get("require_tls")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["CfnDBProxy.TagFormatProperty"]]:
        """``AWS::RDS::DBProxy.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-tags
        """
        return self._values.get("tags")

    @builtins.property
    def vpc_security_group_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBProxy.VpcSecurityGroupIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxy.html#cfn-rds-dbproxy-vpcsecuritygroupids
        """
        return self._values.get("vpc_security_group_ids")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBProxyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBProxyTargetGroup(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.CfnDBProxyTargetGroup",
):
    """A CloudFormation ``AWS::RDS::DBProxyTargetGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::RDS::DBProxyTargetGroup
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        db_proxy_name: str,
        target_group_name: str,
        connection_pool_configuration_info: typing.Optional[typing.Union["ConnectionPoolConfigurationInfoFormatProperty", _IResolvable_9ceae33e]] = None,
        db_cluster_identifiers: typing.Optional[typing.List[str]] = None,
        db_instance_identifiers: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Create a new ``AWS::RDS::DBProxyTargetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_proxy_name: ``AWS::RDS::DBProxyTargetGroup.DBProxyName``.
        :param target_group_name: ``AWS::RDS::DBProxyTargetGroup.TargetGroupName``.
        :param connection_pool_configuration_info: ``AWS::RDS::DBProxyTargetGroup.ConnectionPoolConfigurationInfo``.
        :param db_cluster_identifiers: ``AWS::RDS::DBProxyTargetGroup.DBClusterIdentifiers``.
        :param db_instance_identifiers: ``AWS::RDS::DBProxyTargetGroup.DBInstanceIdentifiers``.
        """
        props = CfnDBProxyTargetGroupProps(
            db_proxy_name=db_proxy_name,
            target_group_name=target_group_name,
            connection_pool_configuration_info=connection_pool_configuration_info,
            db_cluster_identifiers=db_cluster_identifiers,
            db_instance_identifiers=db_instance_identifiers,
        )

        jsii.create(CfnDBProxyTargetGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="attrTargetGroupArn")
    def attr_target_group_arn(self) -> str:
        """
        cloudformationAttribute:
        :cloudformationAttribute:: TargetGroupArn
        """
        return jsii.get(self, "attrTargetGroupArn")

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="dbProxyName")
    def db_proxy_name(self) -> str:
        """``AWS::RDS::DBProxyTargetGroup.DBProxyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-dbproxyname
        """
        return jsii.get(self, "dbProxyName")

    @db_proxy_name.setter
    def db_proxy_name(self, value: str) -> None:
        jsii.set(self, "dbProxyName", value)

    @builtins.property
    @jsii.member(jsii_name="targetGroupName")
    def target_group_name(self) -> str:
        """``AWS::RDS::DBProxyTargetGroup.TargetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-targetgroupname
        """
        return jsii.get(self, "targetGroupName")

    @target_group_name.setter
    def target_group_name(self, value: str) -> None:
        jsii.set(self, "targetGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="connectionPoolConfigurationInfo")
    def connection_pool_configuration_info(
        self,
    ) -> typing.Optional[typing.Union["ConnectionPoolConfigurationInfoFormatProperty", _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBProxyTargetGroup.ConnectionPoolConfigurationInfo``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfo
        """
        return jsii.get(self, "connectionPoolConfigurationInfo")

    @connection_pool_configuration_info.setter
    def connection_pool_configuration_info(
        self,
        value: typing.Optional[typing.Union["ConnectionPoolConfigurationInfoFormatProperty", _IResolvable_9ceae33e]],
    ) -> None:
        jsii.set(self, "connectionPoolConfigurationInfo", value)

    @builtins.property
    @jsii.member(jsii_name="dbClusterIdentifiers")
    def db_cluster_identifiers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBProxyTargetGroup.DBClusterIdentifiers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-dbclusteridentifiers
        """
        return jsii.get(self, "dbClusterIdentifiers")

    @db_cluster_identifiers.setter
    def db_cluster_identifiers(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "dbClusterIdentifiers", value)

    @builtins.property
    @jsii.member(jsii_name="dbInstanceIdentifiers")
    def db_instance_identifiers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBProxyTargetGroup.DBInstanceIdentifiers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-dbinstanceidentifiers
        """
        return jsii.get(self, "dbInstanceIdentifiers")

    @db_instance_identifiers.setter
    def db_instance_identifiers(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "dbInstanceIdentifiers", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_rds.CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connection_borrow_timeout": "connectionBorrowTimeout",
            "init_query": "initQuery",
            "max_connections_percent": "maxConnectionsPercent",
            "max_idle_connections_percent": "maxIdleConnectionsPercent",
            "session_pinning_filters": "sessionPinningFilters",
        },
    )
    class ConnectionPoolConfigurationInfoFormatProperty:
        def __init__(
            self,
            *,
            connection_borrow_timeout: typing.Optional[jsii.Number] = None,
            init_query: typing.Optional[str] = None,
            max_connections_percent: typing.Optional[jsii.Number] = None,
            max_idle_connections_percent: typing.Optional[jsii.Number] = None,
            session_pinning_filters: typing.Optional[typing.List[str]] = None,
        ) -> None:
            """
            :param connection_borrow_timeout: ``CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty.ConnectionBorrowTimeout``.
            :param init_query: ``CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty.InitQuery``.
            :param max_connections_percent: ``CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty.MaxConnectionsPercent``.
            :param max_idle_connections_percent: ``CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty.MaxIdleConnectionsPercent``.
            :param session_pinning_filters: ``CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty.SessionPinningFilters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat.html
            """
            self._values = {}
            if connection_borrow_timeout is not None:
                self._values["connection_borrow_timeout"] = connection_borrow_timeout
            if init_query is not None:
                self._values["init_query"] = init_query
            if max_connections_percent is not None:
                self._values["max_connections_percent"] = max_connections_percent
            if max_idle_connections_percent is not None:
                self._values["max_idle_connections_percent"] = max_idle_connections_percent
            if session_pinning_filters is not None:
                self._values["session_pinning_filters"] = session_pinning_filters

        @builtins.property
        def connection_borrow_timeout(self) -> typing.Optional[jsii.Number]:
            """``CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty.ConnectionBorrowTimeout``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat-connectionborrowtimeout
            """
            return self._values.get("connection_borrow_timeout")

        @builtins.property
        def init_query(self) -> typing.Optional[str]:
            """``CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty.InitQuery``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat-initquery
            """
            return self._values.get("init_query")

        @builtins.property
        def max_connections_percent(self) -> typing.Optional[jsii.Number]:
            """``CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty.MaxConnectionsPercent``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat-maxconnectionspercent
            """
            return self._values.get("max_connections_percent")

        @builtins.property
        def max_idle_connections_percent(self) -> typing.Optional[jsii.Number]:
            """``CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty.MaxIdleConnectionsPercent``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat-maxidleconnectionspercent
            """
            return self._values.get("max_idle_connections_percent")

        @builtins.property
        def session_pinning_filters(self) -> typing.Optional[typing.List[str]]:
            """``CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty.SessionPinningFilters``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfoformat-sessionpinningfilters
            """
            return self._values.get("session_pinning_filters")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConnectionPoolConfigurationInfoFormatProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.CfnDBProxyTargetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_proxy_name": "dbProxyName",
        "target_group_name": "targetGroupName",
        "connection_pool_configuration_info": "connectionPoolConfigurationInfo",
        "db_cluster_identifiers": "dbClusterIdentifiers",
        "db_instance_identifiers": "dbInstanceIdentifiers",
    },
)
class CfnDBProxyTargetGroupProps:
    def __init__(
        self,
        *,
        db_proxy_name: str,
        target_group_name: str,
        connection_pool_configuration_info: typing.Optional[typing.Union["CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty", _IResolvable_9ceae33e]] = None,
        db_cluster_identifiers: typing.Optional[typing.List[str]] = None,
        db_instance_identifiers: typing.Optional[typing.List[str]] = None,
    ) -> None:
        """Properties for defining a ``AWS::RDS::DBProxyTargetGroup``.

        :param db_proxy_name: ``AWS::RDS::DBProxyTargetGroup.DBProxyName``.
        :param target_group_name: ``AWS::RDS::DBProxyTargetGroup.TargetGroupName``.
        :param connection_pool_configuration_info: ``AWS::RDS::DBProxyTargetGroup.ConnectionPoolConfigurationInfo``.
        :param db_cluster_identifiers: ``AWS::RDS::DBProxyTargetGroup.DBClusterIdentifiers``.
        :param db_instance_identifiers: ``AWS::RDS::DBProxyTargetGroup.DBInstanceIdentifiers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html
        """
        self._values = {
            "db_proxy_name": db_proxy_name,
            "target_group_name": target_group_name,
        }
        if connection_pool_configuration_info is not None:
            self._values["connection_pool_configuration_info"] = connection_pool_configuration_info
        if db_cluster_identifiers is not None:
            self._values["db_cluster_identifiers"] = db_cluster_identifiers
        if db_instance_identifiers is not None:
            self._values["db_instance_identifiers"] = db_instance_identifiers

    @builtins.property
    def db_proxy_name(self) -> str:
        """``AWS::RDS::DBProxyTargetGroup.DBProxyName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-dbproxyname
        """
        return self._values.get("db_proxy_name")

    @builtins.property
    def target_group_name(self) -> str:
        """``AWS::RDS::DBProxyTargetGroup.TargetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-targetgroupname
        """
        return self._values.get("target_group_name")

    @builtins.property
    def connection_pool_configuration_info(
        self,
    ) -> typing.Optional[typing.Union["CfnDBProxyTargetGroup.ConnectionPoolConfigurationInfoFormatProperty", _IResolvable_9ceae33e]]:
        """``AWS::RDS::DBProxyTargetGroup.ConnectionPoolConfigurationInfo``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-connectionpoolconfigurationinfo
        """
        return self._values.get("connection_pool_configuration_info")

    @builtins.property
    def db_cluster_identifiers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBProxyTargetGroup.DBClusterIdentifiers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-dbclusteridentifiers
        """
        return self._values.get("db_cluster_identifiers")

    @builtins.property
    def db_instance_identifiers(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::DBProxyTargetGroup.DBInstanceIdentifiers``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbproxytargetgroup.html#cfn-rds-dbproxytargetgroup-dbinstanceidentifiers
        """
        return self._values.get("db_instance_identifiers")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBProxyTargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBSecurityGroup(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.CfnDBSecurityGroup",
):
    """A CloudFormation ``AWS::RDS::DBSecurityGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html
    cloudformationResource:
    :cloudformationResource:: AWS::RDS::DBSecurityGroup
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        db_security_group_ingress: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["IngressProperty", _IResolvable_9ceae33e]]],
        group_description: str,
        ec2_vpc_id: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::RDS::DBSecurityGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_security_group_ingress: ``AWS::RDS::DBSecurityGroup.DBSecurityGroupIngress``.
        :param group_description: ``AWS::RDS::DBSecurityGroup.GroupDescription``.
        :param ec2_vpc_id: ``AWS::RDS::DBSecurityGroup.EC2VpcId``.
        :param tags: ``AWS::RDS::DBSecurityGroup.Tags``.
        """
        props = CfnDBSecurityGroupProps(
            db_security_group_ingress=db_security_group_ingress,
            group_description=group_description,
            ec2_vpc_id=ec2_vpc_id,
            tags=tags,
        )

        jsii.create(CfnDBSecurityGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::RDS::DBSecurityGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html#cfn-rds-dbsecuritygroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="dbSecurityGroupIngress")
    def db_security_group_ingress(
        self,
    ) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["IngressProperty", _IResolvable_9ceae33e]]]:
        """``AWS::RDS::DBSecurityGroup.DBSecurityGroupIngress``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html#cfn-rds-dbsecuritygroup-dbsecuritygroupingress
        """
        return jsii.get(self, "dbSecurityGroupIngress")

    @db_security_group_ingress.setter
    def db_security_group_ingress(
        self,
        value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["IngressProperty", _IResolvable_9ceae33e]]],
    ) -> None:
        jsii.set(self, "dbSecurityGroupIngress", value)

    @builtins.property
    @jsii.member(jsii_name="groupDescription")
    def group_description(self) -> str:
        """``AWS::RDS::DBSecurityGroup.GroupDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html#cfn-rds-dbsecuritygroup-groupdescription
        """
        return jsii.get(self, "groupDescription")

    @group_description.setter
    def group_description(self, value: str) -> None:
        jsii.set(self, "groupDescription", value)

    @builtins.property
    @jsii.member(jsii_name="ec2VpcId")
    def ec2_vpc_id(self) -> typing.Optional[str]:
        """``AWS::RDS::DBSecurityGroup.EC2VpcId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html#cfn-rds-dbsecuritygroup-ec2vpcid
        """
        return jsii.get(self, "ec2VpcId")

    @ec2_vpc_id.setter
    def ec2_vpc_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ec2VpcId", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_rds.CfnDBSecurityGroup.IngressProperty",
        jsii_struct_bases=[],
        name_mapping={
            "cidrip": "cidrip",
            "ec2_security_group_id": "ec2SecurityGroupId",
            "ec2_security_group_name": "ec2SecurityGroupName",
            "ec2_security_group_owner_id": "ec2SecurityGroupOwnerId",
        },
    )
    class IngressProperty:
        def __init__(
            self,
            *,
            cidrip: typing.Optional[str] = None,
            ec2_security_group_id: typing.Optional[str] = None,
            ec2_security_group_name: typing.Optional[str] = None,
            ec2_security_group_owner_id: typing.Optional[str] = None,
        ) -> None:
            """
            :param cidrip: ``CfnDBSecurityGroup.IngressProperty.CIDRIP``.
            :param ec2_security_group_id: ``CfnDBSecurityGroup.IngressProperty.EC2SecurityGroupId``.
            :param ec2_security_group_name: ``CfnDBSecurityGroup.IngressProperty.EC2SecurityGroupName``.
            :param ec2_security_group_owner_id: ``CfnDBSecurityGroup.IngressProperty.EC2SecurityGroupOwnerId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group-rule.html
            """
            self._values = {}
            if cidrip is not None:
                self._values["cidrip"] = cidrip
            if ec2_security_group_id is not None:
                self._values["ec2_security_group_id"] = ec2_security_group_id
            if ec2_security_group_name is not None:
                self._values["ec2_security_group_name"] = ec2_security_group_name
            if ec2_security_group_owner_id is not None:
                self._values["ec2_security_group_owner_id"] = ec2_security_group_owner_id

        @builtins.property
        def cidrip(self) -> typing.Optional[str]:
            """``CfnDBSecurityGroup.IngressProperty.CIDRIP``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group-rule.html#cfn-rds-securitygroup-cidrip
            """
            return self._values.get("cidrip")

        @builtins.property
        def ec2_security_group_id(self) -> typing.Optional[str]:
            """``CfnDBSecurityGroup.IngressProperty.EC2SecurityGroupId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group-rule.html#cfn-rds-securitygroup-ec2securitygroupid
            """
            return self._values.get("ec2_security_group_id")

        @builtins.property
        def ec2_security_group_name(self) -> typing.Optional[str]:
            """``CfnDBSecurityGroup.IngressProperty.EC2SecurityGroupName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group-rule.html#cfn-rds-securitygroup-ec2securitygroupname
            """
            return self._values.get("ec2_security_group_name")

        @builtins.property
        def ec2_security_group_owner_id(self) -> typing.Optional[str]:
            """``CfnDBSecurityGroup.IngressProperty.EC2SecurityGroupOwnerId``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group-rule.html#cfn-rds-securitygroup-ec2securitygroupownerid
            """
            return self._values.get("ec2_security_group_owner_id")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IngressProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBSecurityGroupIngress(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.CfnDBSecurityGroupIngress",
):
    """A CloudFormation ``AWS::RDS::DBSecurityGroupIngress``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html
    cloudformationResource:
    :cloudformationResource:: AWS::RDS::DBSecurityGroupIngress
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        db_security_group_name: str,
        cidrip: typing.Optional[str] = None,
        ec2_security_group_id: typing.Optional[str] = None,
        ec2_security_group_name: typing.Optional[str] = None,
        ec2_security_group_owner_id: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::RDS::DBSecurityGroupIngress``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_security_group_name: ``AWS::RDS::DBSecurityGroupIngress.DBSecurityGroupName``.
        :param cidrip: ``AWS::RDS::DBSecurityGroupIngress.CIDRIP``.
        :param ec2_security_group_id: ``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupId``.
        :param ec2_security_group_name: ``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupName``.
        :param ec2_security_group_owner_id: ``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupOwnerId``.
        """
        props = CfnDBSecurityGroupIngressProps(
            db_security_group_name=db_security_group_name,
            cidrip=cidrip,
            ec2_security_group_id=ec2_security_group_id,
            ec2_security_group_name=ec2_security_group_name,
            ec2_security_group_owner_id=ec2_security_group_owner_id,
        )

        jsii.create(CfnDBSecurityGroupIngress, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="dbSecurityGroupName")
    def db_security_group_name(self) -> str:
        """``AWS::RDS::DBSecurityGroupIngress.DBSecurityGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-dbsecuritygroupname
        """
        return jsii.get(self, "dbSecurityGroupName")

    @db_security_group_name.setter
    def db_security_group_name(self, value: str) -> None:
        jsii.set(self, "dbSecurityGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="cidrip")
    def cidrip(self) -> typing.Optional[str]:
        """``AWS::RDS::DBSecurityGroupIngress.CIDRIP``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-cidrip
        """
        return jsii.get(self, "cidrip")

    @cidrip.setter
    def cidrip(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "cidrip", value)

    @builtins.property
    @jsii.member(jsii_name="ec2SecurityGroupId")
    def ec2_security_group_id(self) -> typing.Optional[str]:
        """``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-ec2securitygroupid
        """
        return jsii.get(self, "ec2SecurityGroupId")

    @ec2_security_group_id.setter
    def ec2_security_group_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ec2SecurityGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="ec2SecurityGroupName")
    def ec2_security_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-ec2securitygroupname
        """
        return jsii.get(self, "ec2SecurityGroupName")

    @ec2_security_group_name.setter
    def ec2_security_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ec2SecurityGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="ec2SecurityGroupOwnerId")
    def ec2_security_group_owner_id(self) -> typing.Optional[str]:
        """``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupOwnerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-ec2securitygroupownerid
        """
        return jsii.get(self, "ec2SecurityGroupOwnerId")

    @ec2_security_group_owner_id.setter
    def ec2_security_group_owner_id(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "ec2SecurityGroupOwnerId", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.CfnDBSecurityGroupIngressProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_security_group_name": "dbSecurityGroupName",
        "cidrip": "cidrip",
        "ec2_security_group_id": "ec2SecurityGroupId",
        "ec2_security_group_name": "ec2SecurityGroupName",
        "ec2_security_group_owner_id": "ec2SecurityGroupOwnerId",
    },
)
class CfnDBSecurityGroupIngressProps:
    def __init__(
        self,
        *,
        db_security_group_name: str,
        cidrip: typing.Optional[str] = None,
        ec2_security_group_id: typing.Optional[str] = None,
        ec2_security_group_name: typing.Optional[str] = None,
        ec2_security_group_owner_id: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::RDS::DBSecurityGroupIngress``.

        :param db_security_group_name: ``AWS::RDS::DBSecurityGroupIngress.DBSecurityGroupName``.
        :param cidrip: ``AWS::RDS::DBSecurityGroupIngress.CIDRIP``.
        :param ec2_security_group_id: ``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupId``.
        :param ec2_security_group_name: ``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupName``.
        :param ec2_security_group_owner_id: ``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupOwnerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html
        """
        self._values = {
            "db_security_group_name": db_security_group_name,
        }
        if cidrip is not None:
            self._values["cidrip"] = cidrip
        if ec2_security_group_id is not None:
            self._values["ec2_security_group_id"] = ec2_security_group_id
        if ec2_security_group_name is not None:
            self._values["ec2_security_group_name"] = ec2_security_group_name
        if ec2_security_group_owner_id is not None:
            self._values["ec2_security_group_owner_id"] = ec2_security_group_owner_id

    @builtins.property
    def db_security_group_name(self) -> str:
        """``AWS::RDS::DBSecurityGroupIngress.DBSecurityGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-dbsecuritygroupname
        """
        return self._values.get("db_security_group_name")

    @builtins.property
    def cidrip(self) -> typing.Optional[str]:
        """``AWS::RDS::DBSecurityGroupIngress.CIDRIP``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-cidrip
        """
        return self._values.get("cidrip")

    @builtins.property
    def ec2_security_group_id(self) -> typing.Optional[str]:
        """``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-ec2securitygroupid
        """
        return self._values.get("ec2_security_group_id")

    @builtins.property
    def ec2_security_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-ec2securitygroupname
        """
        return self._values.get("ec2_security_group_name")

    @builtins.property
    def ec2_security_group_owner_id(self) -> typing.Optional[str]:
        """``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupOwnerId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-ec2securitygroupownerid
        """
        return self._values.get("ec2_security_group_owner_id")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBSecurityGroupIngressProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.CfnDBSecurityGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_security_group_ingress": "dbSecurityGroupIngress",
        "group_description": "groupDescription",
        "ec2_vpc_id": "ec2VpcId",
        "tags": "tags",
    },
)
class CfnDBSecurityGroupProps:
    def __init__(
        self,
        *,
        db_security_group_ingress: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDBSecurityGroup.IngressProperty", _IResolvable_9ceae33e]]],
        group_description: str,
        ec2_vpc_id: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::RDS::DBSecurityGroup``.

        :param db_security_group_ingress: ``AWS::RDS::DBSecurityGroup.DBSecurityGroupIngress``.
        :param group_description: ``AWS::RDS::DBSecurityGroup.GroupDescription``.
        :param ec2_vpc_id: ``AWS::RDS::DBSecurityGroup.EC2VpcId``.
        :param tags: ``AWS::RDS::DBSecurityGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html
        """
        self._values = {
            "db_security_group_ingress": db_security_group_ingress,
            "group_description": group_description,
        }
        if ec2_vpc_id is not None:
            self._values["ec2_vpc_id"] = ec2_vpc_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def db_security_group_ingress(
        self,
    ) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnDBSecurityGroup.IngressProperty", _IResolvable_9ceae33e]]]:
        """``AWS::RDS::DBSecurityGroup.DBSecurityGroupIngress``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html#cfn-rds-dbsecuritygroup-dbsecuritygroupingress
        """
        return self._values.get("db_security_group_ingress")

    @builtins.property
    def group_description(self) -> str:
        """``AWS::RDS::DBSecurityGroup.GroupDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html#cfn-rds-dbsecuritygroup-groupdescription
        """
        return self._values.get("group_description")

    @builtins.property
    def ec2_vpc_id(self) -> typing.Optional[str]:
        """``AWS::RDS::DBSecurityGroup.EC2VpcId``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html#cfn-rds-dbsecuritygroup-ec2vpcid
        """
        return self._values.get("ec2_vpc_id")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::RDS::DBSecurityGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html#cfn-rds-dbsecuritygroup-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBSecurityGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnDBSubnetGroup(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.CfnDBSubnetGroup",
):
    """A CloudFormation ``AWS::RDS::DBSubnetGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html
    cloudformationResource:
    :cloudformationResource:: AWS::RDS::DBSubnetGroup
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        db_subnet_group_description: str,
        subnet_ids: typing.List[str],
        db_subnet_group_name: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::RDS::DBSubnetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param db_subnet_group_description: ``AWS::RDS::DBSubnetGroup.DBSubnetGroupDescription``.
        :param subnet_ids: ``AWS::RDS::DBSubnetGroup.SubnetIds``.
        :param db_subnet_group_name: ``AWS::RDS::DBSubnetGroup.DBSubnetGroupName``.
        :param tags: ``AWS::RDS::DBSubnetGroup.Tags``.
        """
        props = CfnDBSubnetGroupProps(
            db_subnet_group_description=db_subnet_group_description,
            subnet_ids=subnet_ids,
            db_subnet_group_name=db_subnet_group_name,
            tags=tags,
        )

        jsii.create(CfnDBSubnetGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::RDS::DBSubnetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html#cfn-rds-dbsubnetgroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupDescription")
    def db_subnet_group_description(self) -> str:
        """``AWS::RDS::DBSubnetGroup.DBSubnetGroupDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html#cfn-rds-dbsubnetgroup-dbsubnetgroupdescription
        """
        return jsii.get(self, "dbSubnetGroupDescription")

    @db_subnet_group_description.setter
    def db_subnet_group_description(self, value: str) -> None:
        jsii.set(self, "dbSubnetGroupDescription", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::RDS::DBSubnetGroup.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html#cfn-rds-dbsubnetgroup-subnetids
        """
        return jsii.get(self, "subnetIds")

    @subnet_ids.setter
    def subnet_ids(self, value: typing.List[str]) -> None:
        jsii.set(self, "subnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBSubnetGroup.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html#cfn-rds-dbsubnetgroup-dbsubnetgroupname
        """
        return jsii.get(self, "dbSubnetGroupName")

    @db_subnet_group_name.setter
    def db_subnet_group_name(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "dbSubnetGroupName", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.CfnDBSubnetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "db_subnet_group_description": "dbSubnetGroupDescription",
        "subnet_ids": "subnetIds",
        "db_subnet_group_name": "dbSubnetGroupName",
        "tags": "tags",
    },
)
class CfnDBSubnetGroupProps:
    def __init__(
        self,
        *,
        db_subnet_group_description: str,
        subnet_ids: typing.List[str],
        db_subnet_group_name: typing.Optional[str] = None,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::RDS::DBSubnetGroup``.

        :param db_subnet_group_description: ``AWS::RDS::DBSubnetGroup.DBSubnetGroupDescription``.
        :param subnet_ids: ``AWS::RDS::DBSubnetGroup.SubnetIds``.
        :param db_subnet_group_name: ``AWS::RDS::DBSubnetGroup.DBSubnetGroupName``.
        :param tags: ``AWS::RDS::DBSubnetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html
        """
        self._values = {
            "db_subnet_group_description": db_subnet_group_description,
            "subnet_ids": subnet_ids,
        }
        if db_subnet_group_name is not None:
            self._values["db_subnet_group_name"] = db_subnet_group_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def db_subnet_group_description(self) -> str:
        """``AWS::RDS::DBSubnetGroup.DBSubnetGroupDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html#cfn-rds-dbsubnetgroup-dbsubnetgroupdescription
        """
        return self._values.get("db_subnet_group_description")

    @builtins.property
    def subnet_ids(self) -> typing.List[str]:
        """``AWS::RDS::DBSubnetGroup.SubnetIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html#cfn-rds-dbsubnetgroup-subnetids
        """
        return self._values.get("subnet_ids")

    @builtins.property
    def db_subnet_group_name(self) -> typing.Optional[str]:
        """``AWS::RDS::DBSubnetGroup.DBSubnetGroupName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html#cfn-rds-dbsubnetgroup-dbsubnetgroupname
        """
        return self._values.get("db_subnet_group_name")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::RDS::DBSubnetGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html#cfn-rds-dbsubnetgroup-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDBSubnetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnEventSubscription(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.CfnEventSubscription",
):
    """A CloudFormation ``AWS::RDS::EventSubscription``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html
    cloudformationResource:
    :cloudformationResource:: AWS::RDS::EventSubscription
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        sns_topic_arn: str,
        enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        event_categories: typing.Optional[typing.List[str]] = None,
        source_ids: typing.Optional[typing.List[str]] = None,
        source_type: typing.Optional[str] = None,
    ) -> None:
        """Create a new ``AWS::RDS::EventSubscription``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param sns_topic_arn: ``AWS::RDS::EventSubscription.SnsTopicArn``.
        :param enabled: ``AWS::RDS::EventSubscription.Enabled``.
        :param event_categories: ``AWS::RDS::EventSubscription.EventCategories``.
        :param source_ids: ``AWS::RDS::EventSubscription.SourceIds``.
        :param source_type: ``AWS::RDS::EventSubscription.SourceType``.
        """
        props = CfnEventSubscriptionProps(
            sns_topic_arn=sns_topic_arn,
            enabled=enabled,
            event_categories=event_categories,
            source_ids=source_ids,
            source_type=source_type,
        )

        jsii.create(CfnEventSubscription, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="snsTopicArn")
    def sns_topic_arn(self) -> str:
        """``AWS::RDS::EventSubscription.SnsTopicArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-snstopicarn
        """
        return jsii.get(self, "snsTopicArn")

    @sns_topic_arn.setter
    def sns_topic_arn(self, value: str) -> None:
        jsii.set(self, "snsTopicArn", value)

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::EventSubscription.Enabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-enabled
        """
        return jsii.get(self, "enabled")

    @enabled.setter
    def enabled(
        self, value: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]
    ) -> None:
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="eventCategories")
    def event_categories(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::EventSubscription.EventCategories``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-eventcategories
        """
        return jsii.get(self, "eventCategories")

    @event_categories.setter
    def event_categories(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "eventCategories", value)

    @builtins.property
    @jsii.member(jsii_name="sourceIds")
    def source_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::EventSubscription.SourceIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-sourceids
        """
        return jsii.get(self, "sourceIds")

    @source_ids.setter
    def source_ids(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "sourceIds", value)

    @builtins.property
    @jsii.member(jsii_name="sourceType")
    def source_type(self) -> typing.Optional[str]:
        """``AWS::RDS::EventSubscription.SourceType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-sourcetype
        """
        return jsii.get(self, "sourceType")

    @source_type.setter
    def source_type(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "sourceType", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.CfnEventSubscriptionProps",
    jsii_struct_bases=[],
    name_mapping={
        "sns_topic_arn": "snsTopicArn",
        "enabled": "enabled",
        "event_categories": "eventCategories",
        "source_ids": "sourceIds",
        "source_type": "sourceType",
    },
)
class CfnEventSubscriptionProps:
    def __init__(
        self,
        *,
        sns_topic_arn: str,
        enabled: typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]] = None,
        event_categories: typing.Optional[typing.List[str]] = None,
        source_ids: typing.Optional[typing.List[str]] = None,
        source_type: typing.Optional[str] = None,
    ) -> None:
        """Properties for defining a ``AWS::RDS::EventSubscription``.

        :param sns_topic_arn: ``AWS::RDS::EventSubscription.SnsTopicArn``.
        :param enabled: ``AWS::RDS::EventSubscription.Enabled``.
        :param event_categories: ``AWS::RDS::EventSubscription.EventCategories``.
        :param source_ids: ``AWS::RDS::EventSubscription.SourceIds``.
        :param source_type: ``AWS::RDS::EventSubscription.SourceType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html
        """
        self._values = {
            "sns_topic_arn": sns_topic_arn,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if event_categories is not None:
            self._values["event_categories"] = event_categories
        if source_ids is not None:
            self._values["source_ids"] = source_ids
        if source_type is not None:
            self._values["source_type"] = source_type

    @builtins.property
    def sns_topic_arn(self) -> str:
        """``AWS::RDS::EventSubscription.SnsTopicArn``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-snstopicarn
        """
        return self._values.get("sns_topic_arn")

    @builtins.property
    def enabled(self) -> typing.Optional[typing.Union[bool, _IResolvable_9ceae33e]]:
        """``AWS::RDS::EventSubscription.Enabled``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-enabled
        """
        return self._values.get("enabled")

    @builtins.property
    def event_categories(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::EventSubscription.EventCategories``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-eventcategories
        """
        return self._values.get("event_categories")

    @builtins.property
    def source_ids(self) -> typing.Optional[typing.List[str]]:
        """``AWS::RDS::EventSubscription.SourceIds``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-sourceids
        """
        return self._values.get("source_ids")

    @builtins.property
    def source_type(self) -> typing.Optional[str]:
        """``AWS::RDS::EventSubscription.SourceType``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-sourcetype
        """
        return self._values.get("source_type")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEventSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_051e6ed8)
class CfnOptionGroup(
    _CfnResource_7760e8e4,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.CfnOptionGroup",
):
    """A CloudFormation ``AWS::RDS::OptionGroup``.

    see
    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html
    cloudformationResource:
    :cloudformationResource:: AWS::RDS::OptionGroup
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        engine_name: str,
        major_engine_version: str,
        option_configurations: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["OptionConfigurationProperty", _IResolvable_9ceae33e]]],
        option_group_description: str,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Create a new ``AWS::RDS::OptionGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param engine_name: ``AWS::RDS::OptionGroup.EngineName``.
        :param major_engine_version: ``AWS::RDS::OptionGroup.MajorEngineVersion``.
        :param option_configurations: ``AWS::RDS::OptionGroup.OptionConfigurations``.
        :param option_group_description: ``AWS::RDS::OptionGroup.OptionGroupDescription``.
        :param tags: ``AWS::RDS::OptionGroup.Tags``.
        """
        props = CfnOptionGroupProps(
            engine_name=engine_name,
            major_engine_version=major_engine_version,
            option_configurations=option_configurations,
            option_group_description=option_group_description,
            tags=tags,
        )

        jsii.create(CfnOptionGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[str, typing.Any]:
        return jsii.get(self, "cfnProperties")

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_2508893f:
        """``AWS::RDS::OptionGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-tags
        """
        return jsii.get(self, "tags")

    @builtins.property
    @jsii.member(jsii_name="engineName")
    def engine_name(self) -> str:
        """``AWS::RDS::OptionGroup.EngineName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-enginename
        """
        return jsii.get(self, "engineName")

    @engine_name.setter
    def engine_name(self, value: str) -> None:
        jsii.set(self, "engineName", value)

    @builtins.property
    @jsii.member(jsii_name="majorEngineVersion")
    def major_engine_version(self) -> str:
        """``AWS::RDS::OptionGroup.MajorEngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-majorengineversion
        """
        return jsii.get(self, "majorEngineVersion")

    @major_engine_version.setter
    def major_engine_version(self, value: str) -> None:
        jsii.set(self, "majorEngineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="optionConfigurations")
    def option_configurations(
        self,
    ) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["OptionConfigurationProperty", _IResolvable_9ceae33e]]]:
        """``AWS::RDS::OptionGroup.OptionConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-optionconfigurations
        """
        return jsii.get(self, "optionConfigurations")

    @option_configurations.setter
    def option_configurations(
        self,
        value: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["OptionConfigurationProperty", _IResolvable_9ceae33e]]],
    ) -> None:
        jsii.set(self, "optionConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="optionGroupDescription")
    def option_group_description(self) -> str:
        """``AWS::RDS::OptionGroup.OptionGroupDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-optiongroupdescription
        """
        return jsii.get(self, "optionGroupDescription")

    @option_group_description.setter
    def option_group_description(self, value: str) -> None:
        jsii.set(self, "optionGroupDescription", value)

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_rds.CfnOptionGroup.OptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "option_name": "optionName",
            "db_security_group_memberships": "dbSecurityGroupMemberships",
            "option_settings": "optionSettings",
            "option_version": "optionVersion",
            "port": "port",
            "vpc_security_group_memberships": "vpcSecurityGroupMemberships",
        },
    )
    class OptionConfigurationProperty:
        def __init__(
            self,
            *,
            option_name: str,
            db_security_group_memberships: typing.Optional[typing.List[str]] = None,
            option_settings: typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnOptionGroup.OptionSettingProperty", _IResolvable_9ceae33e]]]] = None,
            option_version: typing.Optional[str] = None,
            port: typing.Optional[jsii.Number] = None,
            vpc_security_group_memberships: typing.Optional[typing.List[str]] = None,
        ) -> None:
            """
            :param option_name: ``CfnOptionGroup.OptionConfigurationProperty.OptionName``.
            :param db_security_group_memberships: ``CfnOptionGroup.OptionConfigurationProperty.DBSecurityGroupMemberships``.
            :param option_settings: ``CfnOptionGroup.OptionConfigurationProperty.OptionSettings``.
            :param option_version: ``CfnOptionGroup.OptionConfigurationProperty.OptionVersion``.
            :param port: ``CfnOptionGroup.OptionConfigurationProperty.Port``.
            :param vpc_security_group_memberships: ``CfnOptionGroup.OptionConfigurationProperty.VpcSecurityGroupMemberships``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html
            """
            self._values = {
                "option_name": option_name,
            }
            if db_security_group_memberships is not None:
                self._values["db_security_group_memberships"] = db_security_group_memberships
            if option_settings is not None:
                self._values["option_settings"] = option_settings
            if option_version is not None:
                self._values["option_version"] = option_version
            if port is not None:
                self._values["port"] = port
            if vpc_security_group_memberships is not None:
                self._values["vpc_security_group_memberships"] = vpc_security_group_memberships

        @builtins.property
        def option_name(self) -> str:
            """``CfnOptionGroup.OptionConfigurationProperty.OptionName``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html#cfn-rds-optiongroup-optionconfigurations-optionname
            """
            return self._values.get("option_name")

        @builtins.property
        def db_security_group_memberships(self) -> typing.Optional[typing.List[str]]:
            """``CfnOptionGroup.OptionConfigurationProperty.DBSecurityGroupMemberships``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html#cfn-rds-optiongroup-optionconfigurations-dbsecuritygroupmemberships
            """
            return self._values.get("db_security_group_memberships")

        @builtins.property
        def option_settings(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnOptionGroup.OptionSettingProperty", _IResolvable_9ceae33e]]]]:
            """``CfnOptionGroup.OptionConfigurationProperty.OptionSettings``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html#cfn-rds-optiongroup-optionconfigurations-optionsettings
            """
            return self._values.get("option_settings")

        @builtins.property
        def option_version(self) -> typing.Optional[str]:
            """``CfnOptionGroup.OptionConfigurationProperty.OptionVersion``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html#cfn-rds-optiongroup-optionconfiguration-optionversion
            """
            return self._values.get("option_version")

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            """``CfnOptionGroup.OptionConfigurationProperty.Port``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html#cfn-rds-optiongroup-optionconfigurations-port
            """
            return self._values.get("port")

        @builtins.property
        def vpc_security_group_memberships(self) -> typing.Optional[typing.List[str]]:
            """``CfnOptionGroup.OptionConfigurationProperty.VpcSecurityGroupMemberships``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html#cfn-rds-optiongroup-optionconfigurations-vpcsecuritygroupmemberships
            """
            return self._values.get("vpc_security_group_memberships")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk-experiment.aws_rds.CfnOptionGroup.OptionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class OptionSettingProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[str] = None,
            value: typing.Optional[str] = None,
        ) -> None:
            """
            :param name: ``CfnOptionGroup.OptionSettingProperty.Name``.
            :param value: ``CfnOptionGroup.OptionSettingProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations-optionsettings.html
            """
            self._values = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[str]:
            """``CfnOptionGroup.OptionSettingProperty.Name``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations-optionsettings.html#cfn-rds-optiongroup-optionconfigurations-optionsettings-name
            """
            return self._values.get("name")

        @builtins.property
        def value(self) -> typing.Optional[str]:
            """``CfnOptionGroup.OptionSettingProperty.Value``.

            see
            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations-optionsettings.html#cfn-rds-optiongroup-optionconfigurations-optionsettings-value
            """
            return self._values.get("value")

        def __eq__(self, rhs) -> bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs) -> bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.CfnOptionGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "engine_name": "engineName",
        "major_engine_version": "majorEngineVersion",
        "option_configurations": "optionConfigurations",
        "option_group_description": "optionGroupDescription",
        "tags": "tags",
    },
)
class CfnOptionGroupProps:
    def __init__(
        self,
        *,
        engine_name: str,
        major_engine_version: str,
        option_configurations: typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnOptionGroup.OptionConfigurationProperty", _IResolvable_9ceae33e]]],
        option_group_description: str,
        tags: typing.Optional[typing.List[_CfnTag_b4661f1a]] = None,
    ) -> None:
        """Properties for defining a ``AWS::RDS::OptionGroup``.

        :param engine_name: ``AWS::RDS::OptionGroup.EngineName``.
        :param major_engine_version: ``AWS::RDS::OptionGroup.MajorEngineVersion``.
        :param option_configurations: ``AWS::RDS::OptionGroup.OptionConfigurations``.
        :param option_group_description: ``AWS::RDS::OptionGroup.OptionGroupDescription``.
        :param tags: ``AWS::RDS::OptionGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html
        """
        self._values = {
            "engine_name": engine_name,
            "major_engine_version": major_engine_version,
            "option_configurations": option_configurations,
            "option_group_description": option_group_description,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def engine_name(self) -> str:
        """``AWS::RDS::OptionGroup.EngineName``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-enginename
        """
        return self._values.get("engine_name")

    @builtins.property
    def major_engine_version(self) -> str:
        """``AWS::RDS::OptionGroup.MajorEngineVersion``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-majorengineversion
        """
        return self._values.get("major_engine_version")

    @builtins.property
    def option_configurations(
        self,
    ) -> typing.Union[_IResolvable_9ceae33e, typing.List[typing.Union["CfnOptionGroup.OptionConfigurationProperty", _IResolvable_9ceae33e]]]:
        """``AWS::RDS::OptionGroup.OptionConfigurations``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-optionconfigurations
        """
        return self._values.get("option_configurations")

    @builtins.property
    def option_group_description(self) -> str:
        """``AWS::RDS::OptionGroup.OptionGroupDescription``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-optiongroupdescription
        """
        return self._values.get("option_group_description")

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_b4661f1a]]:
        """``AWS::RDS::OptionGroup.Tags``.

        see
        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-tags
        """
        return self._values.get("tags")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOptionGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.ClusterEngineBindOptions",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_group": "parameterGroup",
        "s3_export_role": "s3ExportRole",
        "s3_import_role": "s3ImportRole",
    },
)
class ClusterEngineBindOptions:
    def __init__(
        self,
        *,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        s3_export_role: typing.Optional[_IRole_e69bbae4] = None,
        s3_import_role: typing.Optional[_IRole_e69bbae4] = None,
    ) -> None:
        """The extra options passed to the {@link IClusterEngine.bindToCluster} method.

        :param parameter_group: The customer-provided ParameterGroup. Default: - none
        :param s3_export_role: The role used for S3 exporting. Default: - none
        :param s3_import_role: The role used for S3 importing. Default: - none

        stability
        :stability: experimental
        """
        self._values = {}
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if s3_export_role is not None:
            self._values["s3_export_role"] = s3_export_role
        if s3_import_role is not None:
            self._values["s3_import_role"] = s3_import_role

    @builtins.property
    def parameter_group(self) -> typing.Optional["IParameterGroup"]:
        """The customer-provided ParameterGroup.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get("parameter_group")

    @builtins.property
    def s3_export_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The role used for S3 exporting.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get("s3_export_role")

    @builtins.property
    def s3_import_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The role used for S3 importing.

        default
        :default: - none

        stability
        :stability: experimental
        """
        return self._values.get("s3_import_role")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterEngineBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.ClusterEngineConfig",
    jsii_struct_bases=[],
    name_mapping={"parameter_group": "parameterGroup", "port": "port"},
)
class ClusterEngineConfig:
    def __init__(
        self,
        *,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        port: typing.Optional[jsii.Number] = None,
    ) -> None:
        """The type returned from the {@link IClusterEngine.bindToCluster} method.

        :param parameter_group: The ParameterGroup to use for the cluster. Default: - no ParameterGroup will be used
        :param port: The port to use for this cluster, unless the customer specified the port directly. Default: - use the default port for clusters (3306)

        stability
        :stability: experimental
        """
        self._values = {}
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if port is not None:
            self._values["port"] = port

    @builtins.property
    def parameter_group(self) -> typing.Optional["IParameterGroup"]:
        """The ParameterGroup to use for the cluster.

        default
        :default: - no ParameterGroup will be used

        stability
        :stability: experimental
        """
        return self._values.get("parameter_group")

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port to use for this cluster, unless the customer specified the port directly.

        default
        :default: - use the default port for clusters (3306)

        stability
        :stability: experimental
        """
        return self._values.get("port")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ClusterEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.DatabaseClusterAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "cluster_endpoint_address": "clusterEndpointAddress",
        "cluster_identifier": "clusterIdentifier",
        "instance_endpoint_addresses": "instanceEndpointAddresses",
        "instance_identifiers": "instanceIdentifiers",
        "port": "port",
        "reader_endpoint_address": "readerEndpointAddress",
        "security_groups": "securityGroups",
    },
)
class DatabaseClusterAttributes:
    def __init__(
        self,
        *,
        cluster_endpoint_address: str,
        cluster_identifier: str,
        instance_endpoint_addresses: typing.List[str],
        instance_identifiers: typing.List[str],
        port: jsii.Number,
        reader_endpoint_address: str,
        security_groups: typing.List[_ISecurityGroup_d72ab8e8],
    ) -> None:
        """Properties that describe an existing cluster instance.

        :param cluster_endpoint_address: Cluster endpoint address.
        :param cluster_identifier: Identifier for the cluster.
        :param instance_endpoint_addresses: Endpoint addresses of individual instances.
        :param instance_identifiers: Identifier for the instances.
        :param port: The database port.
        :param reader_endpoint_address: Reader endpoint address.
        :param security_groups: The security groups of the database cluster.

        stability
        :stability: experimental
        """
        self._values = {
            "cluster_endpoint_address": cluster_endpoint_address,
            "cluster_identifier": cluster_identifier,
            "instance_endpoint_addresses": instance_endpoint_addresses,
            "instance_identifiers": instance_identifiers,
            "port": port,
            "reader_endpoint_address": reader_endpoint_address,
            "security_groups": security_groups,
        }

    @builtins.property
    def cluster_endpoint_address(self) -> str:
        """Cluster endpoint address.

        stability
        :stability: experimental
        """
        return self._values.get("cluster_endpoint_address")

    @builtins.property
    def cluster_identifier(self) -> str:
        """Identifier for the cluster.

        stability
        :stability: experimental
        """
        return self._values.get("cluster_identifier")

    @builtins.property
    def instance_endpoint_addresses(self) -> typing.List[str]:
        """Endpoint addresses of individual instances.

        stability
        :stability: experimental
        """
        return self._values.get("instance_endpoint_addresses")

    @builtins.property
    def instance_identifiers(self) -> typing.List[str]:
        """Identifier for the instances.

        stability
        :stability: experimental
        """
        return self._values.get("instance_identifiers")

    @builtins.property
    def port(self) -> jsii.Number:
        """The database port.

        stability
        :stability: experimental
        """
        return self._values.get("port")

    @builtins.property
    def reader_endpoint_address(self) -> str:
        """Reader endpoint address.

        stability
        :stability: experimental
        """
        return self._values.get("reader_endpoint_address")

    @builtins.property
    def security_groups(self) -> typing.List[_ISecurityGroup_d72ab8e8]:
        """The security groups of the database cluster.

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseClusterAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseClusterEngine(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.DatabaseClusterEngine",
):
    """A database cluster engine.

    Provides mapping to the serverless application
    used for secret rotation.

    stability
    :stability: experimental
    """

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(DatabaseClusterEngine, self, [])

    @jsii.member(jsii_name="aurora")
    @builtins.classmethod
    def aurora(cls, *, version: "AuroraEngineVersion") -> "IClusterEngine":
        """Creates a new plain Aurora database cluster engine.

        :param version: The version of the Aurora cluster engine.

        stability
        :stability: experimental
        """
        props = AuroraClusterEngineProps(version=version)

        return jsii.sinvoke(cls, "aurora", [props])

    @jsii.member(jsii_name="auroraMysql")
    @builtins.classmethod
    def aurora_mysql(cls, *, version: "AuroraMysqlEngineVersion") -> "IClusterEngine":
        """Creates a new Aurora MySQL database cluster engine.

        :param version: The version of the Aurora MySQL cluster engine.

        stability
        :stability: experimental
        """
        props = AuroraMysqlClusterEngineProps(version=version)

        return jsii.sinvoke(cls, "auroraMysql", [props])

    @jsii.member(jsii_name="auroraPostgres")
    @builtins.classmethod
    def aurora_postgres(
        cls, *, version: "AuroraPostgresEngineVersion"
    ) -> "IClusterEngine":
        """Creates a new Aurora PostgreSQL database cluster engine.

        :param version: The version of the Aurora PostgreSQL cluster engine.

        stability
        :stability: experimental
        """
        props = AuroraPostgresClusterEngineProps(version=version)

        return jsii.sinvoke(cls, "auroraPostgres", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="AURORA")
    def AURORA(cls) -> "IClusterEngine":
        """The unversioned 'aurora' cluster engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link aurora()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "AURORA")

    @jsii.python.classproperty
    @jsii.member(jsii_name="AURORA_MYSQL")
    def AURORA_MYSQL(cls) -> "IClusterEngine":
        """The unversioned 'aurora-msql' cluster engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link auroraMysql()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "AURORA_MYSQL")

    @jsii.python.classproperty
    @jsii.member(jsii_name="AURORA_POSTGRESQL")
    def AURORA_POSTGRESQL(cls) -> "IClusterEngine":
        """The unversioned 'aurora-postgresql' cluster engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link auroraPostgres()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "AURORA_POSTGRESQL")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.DatabaseClusterProps",
    jsii_struct_bases=[],
    name_mapping={
        "engine": "engine",
        "instance_props": "instanceProps",
        "master_user": "masterUser",
        "backup": "backup",
        "cloudwatch_logs_exports": "cloudwatchLogsExports",
        "cloudwatch_logs_retention": "cloudwatchLogsRetention",
        "cloudwatch_logs_retention_role": "cloudwatchLogsRetentionRole",
        "cluster_identifier": "clusterIdentifier",
        "default_database_name": "defaultDatabaseName",
        "deletion_protection": "deletionProtection",
        "instance_identifier_base": "instanceIdentifierBase",
        "instances": "instances",
        "monitoring_interval": "monitoringInterval",
        "monitoring_role": "monitoringRole",
        "parameter_group": "parameterGroup",
        "port": "port",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "removal_policy": "removalPolicy",
        "s3_export_buckets": "s3ExportBuckets",
        "s3_export_role": "s3ExportRole",
        "s3_import_buckets": "s3ImportBuckets",
        "s3_import_role": "s3ImportRole",
        "storage_encrypted": "storageEncrypted",
        "storage_encryption_key": "storageEncryptionKey",
    },
)
class DatabaseClusterProps:
    def __init__(
        self,
        *,
        engine: "IClusterEngine",
        instance_props: "InstanceProps",
        master_user: "Login",
        backup: typing.Optional["BackupProps"] = None,
        cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        cloudwatch_logs_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        cloudwatch_logs_retention_role: typing.Optional[_IRole_e69bbae4] = None,
        cluster_identifier: typing.Optional[str] = None,
        default_database_name: typing.Optional[str] = None,
        deletion_protection: typing.Optional[bool] = None,
        instance_identifier_base: typing.Optional[str] = None,
        instances: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[_Duration_5170c158] = None,
        monitoring_role: typing.Optional[_IRole_e69bbae4] = None,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        s3_export_buckets: typing.Optional[typing.List[_IBucket_25bad983]] = None,
        s3_export_role: typing.Optional[_IRole_e69bbae4] = None,
        s3_import_buckets: typing.Optional[typing.List[_IBucket_25bad983]] = None,
        s3_import_role: typing.Optional[_IRole_e69bbae4] = None,
        storage_encrypted: typing.Optional[bool] = None,
        storage_encryption_key: typing.Optional[_IKey_3336c79d] = None,
    ) -> None:
        """Properties for a new database cluster.

        :param engine: What kind of database to start.
        :param instance_props: Settings for the individual instances that are launched.
        :param master_user: Username and password for the administrative user.
        :param backup: Backup settings. Default: - Backup retention period for automated backups is 1 day. Backup preferred window is set to a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param cluster_identifier: An optional identifier for the cluster. Default: - A name is automatically generated.
        :param default_database_name: Name of a database which is automatically created inside the cluster. Default: - Database is not created in cluster.
        :param deletion_protection: Indicates whether the DB cluster should have deletion protection enabled. Default: false
        :param instance_identifier_base: Base identifier for instances. Every replica is named by appending the replica number to this string, 1-based. Default: - clusterIdentifier is used with the word "Instance" appended. If clusterIdentifier is not provided, the identifier is automatically generated.
        :param instances: How many replicas/instances to create. Has to be at least 1. Default: 2
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instances. Default: no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instances monitoring. Default: - A role is automatically created for you
        :param parameter_group: Additional parameters to pass to the database engine. Default: - No parameter group.
        :param port: What port to listen on. Default: - The default for the engine is used.
        :param preferred_maintenance_window: A preferred maintenance window day/time range. Should be specified as a range ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). Example: 'Sun:23:45-Mon:00:15' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param removal_policy: The removal policy to apply when the cluster and its instances are removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the cluster and instances, but retain a snapshot of the data)
        :param s3_export_buckets: S3 buckets that you want to load data into. This feature is only supported by the Aurora database engine. This property must not be used if ``s3ExportRole`` is used. For MySQL: Default: - None
        :param s3_export_role: Role that will be associated with this DB cluster to enable S3 export. This feature is only supported by the Aurora database engine. This property must not be used if ``s3ExportBuckets`` is used. For MySQL: Default: - New role is created if ``s3ExportBuckets`` is set, no role is defined otherwise
        :param s3_import_buckets: S3 buckets that you want to load data from. This feature is only supported by the Aurora database engine. This property must not be used if ``s3ImportRole`` is used. For MySQL: Default: - None
        :param s3_import_role: Role that will be associated with this DB cluster to enable S3 import. This feature is only supported by the Aurora database engine. This property must not be used if ``s3ImportBuckets`` is used. For MySQL: Default: - New role is created if ``s3ImportBuckets`` is set, no role is defined otherwise
        :param storage_encrypted: Whether to enable storage encryption. Default: - true if storageEncryptionKey is provided, false otherwise
        :param storage_encryption_key: The KMS key for storage encryption. If specified, {@link storageEncrypted} will be set to ``true``. Default: - if storageEncrypted is true then the default master key, no key otherwise

        stability
        :stability: experimental
        """
        if isinstance(instance_props, dict):
            instance_props = InstanceProps(**instance_props)
        if isinstance(master_user, dict):
            master_user = Login(**master_user)
        if isinstance(backup, dict):
            backup = BackupProps(**backup)
        self._values = {
            "engine": engine,
            "instance_props": instance_props,
            "master_user": master_user,
        }
        if backup is not None:
            self._values["backup"] = backup
        if cloudwatch_logs_exports is not None:
            self._values["cloudwatch_logs_exports"] = cloudwatch_logs_exports
        if cloudwatch_logs_retention is not None:
            self._values["cloudwatch_logs_retention"] = cloudwatch_logs_retention
        if cloudwatch_logs_retention_role is not None:
            self._values["cloudwatch_logs_retention_role"] = cloudwatch_logs_retention_role
        if cluster_identifier is not None:
            self._values["cluster_identifier"] = cluster_identifier
        if default_database_name is not None:
            self._values["default_database_name"] = default_database_name
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if instance_identifier_base is not None:
            self._values["instance_identifier_base"] = instance_identifier_base
        if instances is not None:
            self._values["instances"] = instances
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_role is not None:
            self._values["monitoring_role"] = monitoring_role
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if port is not None:
            self._values["port"] = port
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if s3_export_buckets is not None:
            self._values["s3_export_buckets"] = s3_export_buckets
        if s3_export_role is not None:
            self._values["s3_export_role"] = s3_export_role
        if s3_import_buckets is not None:
            self._values["s3_import_buckets"] = s3_import_buckets
        if s3_import_role is not None:
            self._values["s3_import_role"] = s3_import_role
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if storage_encryption_key is not None:
            self._values["storage_encryption_key"] = storage_encryption_key

    @builtins.property
    def engine(self) -> "IClusterEngine":
        """What kind of database to start.

        stability
        :stability: experimental
        """
        return self._values.get("engine")

    @builtins.property
    def instance_props(self) -> "InstanceProps":
        """Settings for the individual instances that are launched.

        stability
        :stability: experimental
        """
        return self._values.get("instance_props")

    @builtins.property
    def master_user(self) -> "Login":
        """Username and password for the administrative user.

        stability
        :stability: experimental
        """
        return self._values.get("master_user")

    @builtins.property
    def backup(self) -> typing.Optional["BackupProps"]:
        """Backup settings.

        default
        :default:

        - Backup retention period for automated backups is 1 day.
          Backup preferred window is set to a 30-minute window selected at random from an
          8-hour block of time for each AWS Region, occurring on a random day of the week.

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        stability
        :stability: experimental
        """
        return self._values.get("backup")

    @builtins.property
    def cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """The list of log types that need to be enabled for exporting to CloudWatch Logs.

        default
        :default: - no log exports

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_exports")

    @builtins.property
    def cloudwatch_logs_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``Infinity``.

        default
        :default: - logs never expire

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_retention")

    @builtins.property
    def cloudwatch_logs_retention_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        default
        :default: - a new role is created.

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_retention_role")

    @builtins.property
    def cluster_identifier(self) -> typing.Optional[str]:
        """An optional identifier for the cluster.

        default
        :default: - A name is automatically generated.

        stability
        :stability: experimental
        """
        return self._values.get("cluster_identifier")

    @builtins.property
    def default_database_name(self) -> typing.Optional[str]:
        """Name of a database which is automatically created inside the cluster.

        default
        :default: - Database is not created in cluster.

        stability
        :stability: experimental
        """
        return self._values.get("default_database_name")

    @builtins.property
    def deletion_protection(self) -> typing.Optional[bool]:
        """Indicates whether the DB cluster should have deletion protection enabled.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("deletion_protection")

    @builtins.property
    def instance_identifier_base(self) -> typing.Optional[str]:
        """Base identifier for instances.

        Every replica is named by appending the replica number to this string, 1-based.

        default
        :default:

        - clusterIdentifier is used with the word "Instance" appended.
          If clusterIdentifier is not provided, the identifier is automatically generated.

        stability
        :stability: experimental
        """
        return self._values.get("instance_identifier_base")

    @builtins.property
    def instances(self) -> typing.Optional[jsii.Number]:
        """How many replicas/instances to create.

        Has to be at least 1.

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get("instances")

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[_Duration_5170c158]:
        """The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instances.

        default
        :default: no enhanced monitoring

        stability
        :stability: experimental
        """
        return self._values.get("monitoring_interval")

    @builtins.property
    def monitoring_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that will be used to manage DB instances monitoring.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get("monitoring_role")

    @builtins.property
    def parameter_group(self) -> typing.Optional["IParameterGroup"]:
        """Additional parameters to pass to the database engine.

        default
        :default: - No parameter group.

        stability
        :stability: experimental
        """
        return self._values.get("parameter_group")

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """What port to listen on.

        default
        :default: - The default for the engine is used.

        stability
        :stability: experimental
        """
        return self._values.get("port")

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """A preferred maintenance window day/time range. Should be specified as a range ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC).

        Example: 'Sun:23:45-Mon:00:15'

        default
        :default:

        - 30-minute window selected at random from an 8-hour block of time for
          each AWS Region, occurring on a random day of the week.

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        stability
        :stability: experimental
        """
        return self._values.get("preferred_maintenance_window")

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """The removal policy to apply when the cluster and its instances are removed from the stack or replaced during an update.

        default
        :default: - RemovalPolicy.SNAPSHOT (remove the cluster and instances, but retain a snapshot of the data)

        stability
        :stability: experimental
        """
        return self._values.get("removal_policy")

    @builtins.property
    def s3_export_buckets(self) -> typing.Optional[typing.List[_IBucket_25bad983]]:
        """S3 buckets that you want to load data into. This feature is only supported by the Aurora database engine.

        This property must not be used if ``s3ExportRole`` is used.

        For MySQL:

        default
        :default: - None

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/postgresql-s3-export.html
        stability
        :stability: experimental
        """
        return self._values.get("s3_export_buckets")

    @builtins.property
    def s3_export_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that will be associated with this DB cluster to enable S3 export.

        This feature is only supported by the Aurora database engine.

        This property must not be used if ``s3ExportBuckets`` is used.

        For MySQL:

        default
        :default: - New role is created if ``s3ExportBuckets`` is set, no role is defined otherwise

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/postgresql-s3-export.html
        stability
        :stability: experimental
        """
        return self._values.get("s3_export_role")

    @builtins.property
    def s3_import_buckets(self) -> typing.Optional[typing.List[_IBucket_25bad983]]:
        """S3 buckets that you want to load data from. This feature is only supported by the Aurora database engine.

        This property must not be used if ``s3ImportRole`` is used.

        For MySQL:

        default
        :default: - None

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Migrating.html
        stability
        :stability: experimental
        """
        return self._values.get("s3_import_buckets")

    @builtins.property
    def s3_import_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that will be associated with this DB cluster to enable S3 import.

        This feature is only supported by the Aurora database engine.

        This property must not be used if ``s3ImportBuckets`` is used.

        For MySQL:

        default
        :default: - New role is created if ``s3ImportBuckets`` is set, no role is defined otherwise

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraPostgreSQL.Migrating.html
        stability
        :stability: experimental
        """
        return self._values.get("s3_import_role")

    @builtins.property
    def storage_encrypted(self) -> typing.Optional[bool]:
        """Whether to enable storage encryption.

        default
        :default: - true if storageEncryptionKey is provided, false otherwise

        stability
        :stability: experimental
        """
        return self._values.get("storage_encrypted")

    @builtins.property
    def storage_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The KMS key for storage encryption.

        If specified, {@link storageEncrypted} will be set to ``true``.

        default
        :default: - if storageEncrypted is true then the default master key, no key otherwise

        stability
        :stability: experimental
        """
        return self._values.get("storage_encryption_key")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseClusterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.DatabaseInstanceAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "instance_endpoint_address": "instanceEndpointAddress",
        "instance_identifier": "instanceIdentifier",
        "port": "port",
        "security_groups": "securityGroups",
    },
)
class DatabaseInstanceAttributes:
    def __init__(
        self,
        *,
        instance_endpoint_address: str,
        instance_identifier: str,
        port: jsii.Number,
        security_groups: typing.List[_ISecurityGroup_d72ab8e8],
    ) -> None:
        """Properties that describe an existing instance.

        :param instance_endpoint_address: The endpoint address.
        :param instance_identifier: The instance identifier.
        :param port: The database port.
        :param security_groups: The security groups of the instance.

        stability
        :stability: experimental
        """
        self._values = {
            "instance_endpoint_address": instance_endpoint_address,
            "instance_identifier": instance_identifier,
            "port": port,
            "security_groups": security_groups,
        }

    @builtins.property
    def instance_endpoint_address(self) -> str:
        """The endpoint address.

        stability
        :stability: experimental
        """
        return self._values.get("instance_endpoint_address")

    @builtins.property
    def instance_identifier(self) -> str:
        """The instance identifier.

        stability
        :stability: experimental
        """
        return self._values.get("instance_identifier")

    @builtins.property
    def port(self) -> jsii.Number:
        """The database port.

        stability
        :stability: experimental
        """
        return self._values.get("port")

    @builtins.property
    def security_groups(self) -> typing.List[_ISecurityGroup_d72ab8e8]:
        """The security groups of the instance.

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseInstanceAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseInstanceEngine(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.DatabaseInstanceEngine",
):
    """A database instance engine.

    Provides mapping to DatabaseEngine used for
    secret rotation.

    stability
    :stability: experimental
    """

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(DatabaseInstanceEngine, self, [])

    @jsii.member(jsii_name="mariaDb")
    @builtins.classmethod
    def maria_db(cls, *, version: "MariaDbEngineVersion") -> "IInstanceEngine":
        """Creates a new MariaDB instance engine.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        props = MariaDbInstanceEngineProps(version=version)

        return jsii.sinvoke(cls, "mariaDb", [props])

    @jsii.member(jsii_name="mysql")
    @builtins.classmethod
    def mysql(cls, *, version: "MysqlEngineVersion") -> "IInstanceEngine":
        """Creates a new MySQL instance engine.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        props = MySqlInstanceEngineProps(version=version)

        return jsii.sinvoke(cls, "mysql", [props])

    @jsii.member(jsii_name="oracleEe")
    @builtins.classmethod
    def oracle_ee(cls, *, version: "OracleEngineVersion") -> "IInstanceEngine":
        """Creates a new Oracle Enterprise Edition instance engine.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        props = OracleEeInstanceEngineProps(version=version)

        return jsii.sinvoke(cls, "oracleEe", [props])

    @jsii.member(jsii_name="oracleSe")
    @builtins.classmethod
    def oracle_se(cls, *, version: "OracleLegacyEngineVersion") -> "IInstanceEngine":
        """Creates a new Oracle Standard Edition instance engine.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        props = OracleSeInstanceEngineProps(version=version)

        return jsii.sinvoke(cls, "oracleSe", [props])

    @jsii.member(jsii_name="oracleSe1")
    @builtins.classmethod
    def oracle_se1(cls, *, version: "OracleLegacyEngineVersion") -> "IInstanceEngine":
        """Creates a new Oracle Standard Edition 1 instance engine.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        props = OracleSe1InstanceEngineProps(version=version)

        return jsii.sinvoke(cls, "oracleSe1", [props])

    @jsii.member(jsii_name="oracleSe2")
    @builtins.classmethod
    def oracle_se2(cls, *, version: "OracleEngineVersion") -> "IInstanceEngine":
        """Creates a new Oracle Standard Edition 1 instance engine.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        props = OracleSe2InstanceEngineProps(version=version)

        return jsii.sinvoke(cls, "oracleSe2", [props])

    @jsii.member(jsii_name="postgres")
    @builtins.classmethod
    def postgres(cls, *, version: "PostgresEngineVersion") -> "IInstanceEngine":
        """Creates a new PostgreSQL instance engine.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        props = PostgresInstanceEngineProps(version=version)

        return jsii.sinvoke(cls, "postgres", [props])

    @jsii.member(jsii_name="sqlServerEe")
    @builtins.classmethod
    def sql_server_ee(cls, *, version: "SqlServerEngineVersion") -> "IInstanceEngine":
        """Creates a new SQL Server Enterprise Edition instance engine.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        props = SqlServerEeInstanceEngineProps(version=version)

        return jsii.sinvoke(cls, "sqlServerEe", [props])

    @jsii.member(jsii_name="sqlServerEx")
    @builtins.classmethod
    def sql_server_ex(cls, *, version: "SqlServerEngineVersion") -> "IInstanceEngine":
        """Creates a new SQL Server Express Edition instance engine.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        props = SqlServerExInstanceEngineProps(version=version)

        return jsii.sinvoke(cls, "sqlServerEx", [props])

    @jsii.member(jsii_name="sqlServerSe")
    @builtins.classmethod
    def sql_server_se(cls, *, version: "SqlServerEngineVersion") -> "IInstanceEngine":
        """Creates a new SQL Server Standard Edition instance engine.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        props = SqlServerSeInstanceEngineProps(version=version)

        return jsii.sinvoke(cls, "sqlServerSe", [props])

    @jsii.member(jsii_name="sqlServerWeb")
    @builtins.classmethod
    def sql_server_web(cls, *, version: "SqlServerEngineVersion") -> "IInstanceEngine":
        """Creates a new SQL Server Web Edition instance engine.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        props = SqlServerWebInstanceEngineProps(version=version)

        return jsii.sinvoke(cls, "sqlServerWeb", [props])

    @jsii.python.classproperty
    @jsii.member(jsii_name="MARIADB")
    def MARIADB(cls) -> "IInstanceEngine":
        """The unversioned 'mariadb' instance engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link mariaDb()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "MARIADB")

    @jsii.python.classproperty
    @jsii.member(jsii_name="MYSQL")
    def MYSQL(cls) -> "IInstanceEngine":
        """The unversioned 'mysql' instance engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link mysql()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "MYSQL")

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORACLE_EE")
    def ORACLE_EE(cls) -> "IInstanceEngine":
        """The unversioned 'oracle-ee' instance engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link oracleEe()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "ORACLE_EE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORACLE_SE")
    def ORACLE_SE(cls) -> "IInstanceEngine":
        """The unversioned 'oracle-se' instance engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link oracleSe()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "ORACLE_SE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORACLE_SE1")
    def ORACLE_SE1(cls) -> "IInstanceEngine":
        """The unversioned 'oracle-se1' instance engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link oracleSe1()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "ORACLE_SE1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="ORACLE_SE2")
    def ORACLE_SE2(cls) -> "IInstanceEngine":
        """The unversioned 'oracle-se2' instance engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link oracleSe2()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "ORACLE_SE2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="POSTGRES")
    def POSTGRES(cls) -> "IInstanceEngine":
        """The unversioned 'postgres' instance engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link postgres()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "POSTGRES")

    @jsii.python.classproperty
    @jsii.member(jsii_name="SQL_SERVER_EE")
    def SQL_SERVER_EE(cls) -> "IInstanceEngine":
        """The unversioned 'sqlserver-ee' instance engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link sqlServerEe()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "SQL_SERVER_EE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="SQL_SERVER_EX")
    def SQL_SERVER_EX(cls) -> "IInstanceEngine":
        """The unversioned 'sqlserver-ex' instance engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link sqlServerEx()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "SQL_SERVER_EX")

    @jsii.python.classproperty
    @jsii.member(jsii_name="SQL_SERVER_SE")
    def SQL_SERVER_SE(cls) -> "IInstanceEngine":
        """The unversioned 'sqlserver-se' instance engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link sqlServerSe()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "SQL_SERVER_SE")

    @jsii.python.classproperty
    @jsii.member(jsii_name="SQL_SERVER_WEB")
    def SQL_SERVER_WEB(cls) -> "IInstanceEngine":
        """The unversioned 'sqlserver-web' instance engine.

        deprecated
        :deprecated:

        using unversioned engines is an availability risk.
        We recommend using versioned engines created using the {@link sqlServerWeb()} method

        stability
        :stability: deprecated
        """
        return jsii.sget(cls, "SQL_SERVER_WEB")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.DatabaseInstanceNewProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "backup_retention": "backupRetention",
        "cloudwatch_logs_exports": "cloudwatchLogsExports",
        "cloudwatch_logs_retention": "cloudwatchLogsRetention",
        "cloudwatch_logs_retention_role": "cloudwatchLogsRetentionRole",
        "copy_tags_to_snapshot": "copyTagsToSnapshot",
        "delete_automated_backups": "deleteAutomatedBackups",
        "deletion_protection": "deletionProtection",
        "domain": "domain",
        "domain_role": "domainRole",
        "enable_performance_insights": "enablePerformanceInsights",
        "iam_authentication": "iamAuthentication",
        "instance_identifier": "instanceIdentifier",
        "iops": "iops",
        "max_allocated_storage": "maxAllocatedStorage",
        "monitoring_interval": "monitoringInterval",
        "monitoring_role": "monitoringRole",
        "multi_az": "multiAz",
        "option_group": "optionGroup",
        "performance_insight_encryption_key": "performanceInsightEncryptionKey",
        "performance_insight_retention": "performanceInsightRetention",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "processor_features": "processorFeatures",
        "removal_policy": "removalPolicy",
        "security_groups": "securityGroups",
        "storage_type": "storageType",
        "vpc_placement": "vpcPlacement",
        "vpc_subnets": "vpcSubnets",
    },
)
class DatabaseInstanceNewProps:
    def __init__(
        self,
        *,
        vpc: _IVpc_3795853f,
        auto_minor_version_upgrade: typing.Optional[bool] = None,
        availability_zone: typing.Optional[str] = None,
        backup_retention: typing.Optional[_Duration_5170c158] = None,
        cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        cloudwatch_logs_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        cloudwatch_logs_retention_role: typing.Optional[_IRole_e69bbae4] = None,
        copy_tags_to_snapshot: typing.Optional[bool] = None,
        delete_automated_backups: typing.Optional[bool] = None,
        deletion_protection: typing.Optional[bool] = None,
        domain: typing.Optional[str] = None,
        domain_role: typing.Optional[_IRole_e69bbae4] = None,
        enable_performance_insights: typing.Optional[bool] = None,
        iam_authentication: typing.Optional[bool] = None,
        instance_identifier: typing.Optional[str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[_Duration_5170c158] = None,
        monitoring_role: typing.Optional[_IRole_e69bbae4] = None,
        multi_az: typing.Optional[bool] = None,
        option_group: typing.Optional["IOptionGroup"] = None,
        performance_insight_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        performance_insight_retention: typing.Optional["PerformanceInsightRetention"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[str] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        processor_features: typing.Optional["ProcessorFeatures"] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        storage_type: typing.Optional["StorageType"] = None,
        vpc_placement: typing.Optional[_SubnetSelection_36a13cd6] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> None:
        """Construction properties for a DatabaseInstanceNew.

        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. Default: Duration.days(1)
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: false
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: true
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_type: The storage type. Default: GP2
        :param vpc_placement: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets

        stability
        :stability: experimental
        """
        if isinstance(processor_features, dict):
            processor_features = ProcessorFeatures(**processor_features)
        if isinstance(vpc_placement, dict):
            vpc_placement = _SubnetSelection_36a13cd6(**vpc_placement)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            "vpc": vpc,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if backup_retention is not None:
            self._values["backup_retention"] = backup_retention
        if cloudwatch_logs_exports is not None:
            self._values["cloudwatch_logs_exports"] = cloudwatch_logs_exports
        if cloudwatch_logs_retention is not None:
            self._values["cloudwatch_logs_retention"] = cloudwatch_logs_retention
        if cloudwatch_logs_retention_role is not None:
            self._values["cloudwatch_logs_retention_role"] = cloudwatch_logs_retention_role
        if copy_tags_to_snapshot is not None:
            self._values["copy_tags_to_snapshot"] = copy_tags_to_snapshot
        if delete_automated_backups is not None:
            self._values["delete_automated_backups"] = delete_automated_backups
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if domain is not None:
            self._values["domain"] = domain
        if domain_role is not None:
            self._values["domain_role"] = domain_role
        if enable_performance_insights is not None:
            self._values["enable_performance_insights"] = enable_performance_insights
        if iam_authentication is not None:
            self._values["iam_authentication"] = iam_authentication
        if instance_identifier is not None:
            self._values["instance_identifier"] = instance_identifier
        if iops is not None:
            self._values["iops"] = iops
        if max_allocated_storage is not None:
            self._values["max_allocated_storage"] = max_allocated_storage
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_role is not None:
            self._values["monitoring_role"] = monitoring_role
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if option_group is not None:
            self._values["option_group"] = option_group
        if performance_insight_encryption_key is not None:
            self._values["performance_insight_encryption_key"] = performance_insight_encryption_key
        if performance_insight_retention is not None:
            self._values["performance_insight_retention"] = performance_insight_retention
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if processor_features is not None:
            self._values["processor_features"] = processor_features
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if vpc_placement is not None:
            self._values["vpc_placement"] = vpc_placement
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _IVpc_3795853f:
        """The VPC network where the DB subnet group should be created.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def auto_minor_version_upgrade(self) -> typing.Optional[bool]:
        """Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("auto_minor_version_upgrade")

    @builtins.property
    def availability_zone(self) -> typing.Optional[str]:
        """The name of the Availability Zone where the DB instance will be located.

        default
        :default: - no preference

        stability
        :stability: experimental
        """
        return self._values.get("availability_zone")

    @builtins.property
    def backup_retention(self) -> typing.Optional[_Duration_5170c158]:
        """The number of days during which automatic DB snapshots are retained.

        Set
        to zero to disable backups.

        default
        :default: Duration.days(1)

        stability
        :stability: experimental
        """
        return self._values.get("backup_retention")

    @builtins.property
    def cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """The list of log types that need to be enabled for exporting to CloudWatch Logs.

        default
        :default: - no log exports

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_exports")

    @builtins.property
    def cloudwatch_logs_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``Infinity``.

        default
        :default: - logs never expire

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_retention")

    @builtins.property
    def cloudwatch_logs_retention_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        default
        :default: - a new role is created.

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_retention_role")

    @builtins.property
    def copy_tags_to_snapshot(self) -> typing.Optional[bool]:
        """Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("copy_tags_to_snapshot")

    @builtins.property
    def delete_automated_backups(self) -> typing.Optional[bool]:
        """Indicates whether automated backups should be deleted or retained when you delete a DB instance.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("delete_automated_backups")

    @builtins.property
    def deletion_protection(self) -> typing.Optional[bool]:
        """Indicates whether the DB instance should have deletion protection enabled.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("deletion_protection")

    @builtins.property
    def domain(self) -> typing.Optional[str]:
        """The Active Directory directory ID to create the DB instance in.

        default
        :default: - Do not join domain

        stability
        :stability: experimental
        """
        return self._values.get("domain")

    @builtins.property
    def domain_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role to be used when making API calls to the Directory Service.

        The role needs the AWS-managed policy
        AmazonRDSDirectoryServiceAccess or equivalent.

        default
        :default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified

        stability
        :stability: experimental
        """
        return self._values.get("domain_role")

    @builtins.property
    def enable_performance_insights(self) -> typing.Optional[bool]:
        """Whether to enable Performance Insights for the DB instance.

        default
        :default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.

        stability
        :stability: experimental
        """
        return self._values.get("enable_performance_insights")

    @builtins.property
    def iam_authentication(self) -> typing.Optional[bool]:
        """Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("iam_authentication")

    @builtins.property
    def instance_identifier(self) -> typing.Optional[str]:
        """A name for the DB instance.

        If you specify a name, AWS CloudFormation
        converts it to lowercase.

        default
        :default: - a CloudFormation generated name

        stability
        :stability: experimental
        """
        return self._values.get("instance_identifier")

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) that the database provisions.

        The value must be equal to or greater than 1000.

        default
        :default: - no provisioned iops

        stability
        :stability: experimental
        """
        return self._values.get("iops")

    @builtins.property
    def max_allocated_storage(self) -> typing.Optional[jsii.Number]:
        """Upper limit to which RDS can scale the storage in GiB(Gibibyte).

        default
        :default: - No autoscaling of RDS instance

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling
        stability
        :stability: experimental
        """
        return self._values.get("max_allocated_storage")

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[_Duration_5170c158]:
        """The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance.

        default
        :default: - no enhanced monitoring

        stability
        :stability: experimental
        """
        return self._values.get("monitoring_interval")

    @builtins.property
    def monitoring_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that will be used to manage DB instance monitoring.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get("monitoring_role")

    @builtins.property
    def multi_az(self) -> typing.Optional[bool]:
        """Specifies if the database instance is a multiple Availability Zone deployment.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("multi_az")

    @builtins.property
    def option_group(self) -> typing.Optional["IOptionGroup"]:
        """The option group to associate with the instance.

        default
        :default: - no option group

        stability
        :stability: experimental
        """
        return self._values.get("option_group")

    @builtins.property
    def performance_insight_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The AWS KMS key for encryption of Performance Insights data.

        default
        :default: - default master key

        stability
        :stability: experimental
        """
        return self._values.get("performance_insight_encryption_key")

    @builtins.property
    def performance_insight_retention(
        self,
    ) -> typing.Optional["PerformanceInsightRetention"]:
        """The amount of time, in days, to retain Performance Insights data.

        default
        :default: 7

        stability
        :stability: experimental
        """
        return self._values.get("performance_insight_retention")

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port for the instance.

        default
        :default: - the default port for the chosen engine.

        stability
        :stability: experimental
        """
        return self._values.get("port")

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[str]:
        """The daily time range during which automated backups are performed.

        Constraints:

        - Must be in the format ``hh24:mi-hh24:mi``.
        - Must be in Universal Coordinated Time (UTC).
        - Must not conflict with the preferred maintenance window.
        - Must be at least 30 minutes.

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region. To see the time blocks available, see
          https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow

        stability
        :stability: experimental
        """
        return self._values.get("preferred_backup_window")

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """The weekly time range (in UTC) during which system maintenance can occur.

        Format: ``ddd:hh24:mi-ddd:hh24:mi``
        Constraint: Minimum 30-minute window

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region, occurring on a random day of the week. To see
          the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance

        stability
        :stability: experimental
        """
        return self._values.get("preferred_maintenance_window")

    @builtins.property
    def processor_features(self) -> typing.Optional["ProcessorFeatures"]:
        """The number of CPU cores and the number of threads per core.

        default
        :default:

        - the default number of CPU cores and threads per core for the
          chosen instance class.

        See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor

        stability
        :stability: experimental
        """
        return self._values.get("processor_features")

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update.

        default
        :default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)

        stability
        :stability: experimental
        """
        return self._values.get("removal_policy")

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The security groups to assign to the DB instance.

        default
        :default: - a new security group is created

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    @builtins.property
    def storage_type(self) -> typing.Optional["StorageType"]:
        """The storage type.

        default
        :default: GP2

        stability
        :stability: experimental
        """
        return self._values.get("storage_type")

    @builtins.property
    def vpc_placement(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The type of subnets to add to the created DB subnet group.

        default
        :default: - private subnets

        deprecated
        :deprecated: use ``vpcSubnets``

        stability
        :stability: deprecated
        """
        return self._values.get("vpc_placement")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The type of subnets to add to the created DB subnet group.

        default
        :default: - private subnets

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseInstanceNewProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.DatabaseInstanceReadReplicaProps",
    jsii_struct_bases=[DatabaseInstanceNewProps],
    name_mapping={
        "vpc": "vpc",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "backup_retention": "backupRetention",
        "cloudwatch_logs_exports": "cloudwatchLogsExports",
        "cloudwatch_logs_retention": "cloudwatchLogsRetention",
        "cloudwatch_logs_retention_role": "cloudwatchLogsRetentionRole",
        "copy_tags_to_snapshot": "copyTagsToSnapshot",
        "delete_automated_backups": "deleteAutomatedBackups",
        "deletion_protection": "deletionProtection",
        "domain": "domain",
        "domain_role": "domainRole",
        "enable_performance_insights": "enablePerformanceInsights",
        "iam_authentication": "iamAuthentication",
        "instance_identifier": "instanceIdentifier",
        "iops": "iops",
        "max_allocated_storage": "maxAllocatedStorage",
        "monitoring_interval": "monitoringInterval",
        "monitoring_role": "monitoringRole",
        "multi_az": "multiAz",
        "option_group": "optionGroup",
        "performance_insight_encryption_key": "performanceInsightEncryptionKey",
        "performance_insight_retention": "performanceInsightRetention",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "processor_features": "processorFeatures",
        "removal_policy": "removalPolicy",
        "security_groups": "securityGroups",
        "storage_type": "storageType",
        "vpc_placement": "vpcPlacement",
        "vpc_subnets": "vpcSubnets",
        "instance_type": "instanceType",
        "source_database_instance": "sourceDatabaseInstance",
        "storage_encrypted": "storageEncrypted",
        "storage_encryption_key": "storageEncryptionKey",
    },
)
class DatabaseInstanceReadReplicaProps(DatabaseInstanceNewProps):
    def __init__(
        self,
        *,
        vpc: _IVpc_3795853f,
        auto_minor_version_upgrade: typing.Optional[bool] = None,
        availability_zone: typing.Optional[str] = None,
        backup_retention: typing.Optional[_Duration_5170c158] = None,
        cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        cloudwatch_logs_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        cloudwatch_logs_retention_role: typing.Optional[_IRole_e69bbae4] = None,
        copy_tags_to_snapshot: typing.Optional[bool] = None,
        delete_automated_backups: typing.Optional[bool] = None,
        deletion_protection: typing.Optional[bool] = None,
        domain: typing.Optional[str] = None,
        domain_role: typing.Optional[_IRole_e69bbae4] = None,
        enable_performance_insights: typing.Optional[bool] = None,
        iam_authentication: typing.Optional[bool] = None,
        instance_identifier: typing.Optional[str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[_Duration_5170c158] = None,
        monitoring_role: typing.Optional[_IRole_e69bbae4] = None,
        multi_az: typing.Optional[bool] = None,
        option_group: typing.Optional["IOptionGroup"] = None,
        performance_insight_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        performance_insight_retention: typing.Optional["PerformanceInsightRetention"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[str] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        processor_features: typing.Optional["ProcessorFeatures"] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        storage_type: typing.Optional["StorageType"] = None,
        vpc_placement: typing.Optional[_SubnetSelection_36a13cd6] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        instance_type: _InstanceType_85a97b30,
        source_database_instance: "IDatabaseInstance",
        storage_encrypted: typing.Optional[bool] = None,
        storage_encryption_key: typing.Optional[_IKey_3336c79d] = None,
    ) -> None:
        """Construction properties for a DatabaseInstanceReadReplica.

        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. Default: Duration.days(1)
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: false
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: true
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_type: The storage type. Default: GP2
        :param vpc_placement: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param instance_type: The name of the compute and memory capacity classes.
        :param source_database_instance: The source database instance. Each DB instance can have a limited number of read replicas. For more information, see https://docs.aws.amazon.com/AmazonRDS/latest/DeveloperGuide/USER_ReadRepl.html.
        :param storage_encrypted: Indicates whether the DB instance is encrypted. Default: - true if storageEncryptionKey has been provided, false otherwise
        :param storage_encryption_key: The KMS key that's used to encrypt the DB instance. Default: - default master key if storageEncrypted is true, no key otherwise

        stability
        :stability: experimental
        """
        if isinstance(processor_features, dict):
            processor_features = ProcessorFeatures(**processor_features)
        if isinstance(vpc_placement, dict):
            vpc_placement = _SubnetSelection_36a13cd6(**vpc_placement)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            "vpc": vpc,
            "instance_type": instance_type,
            "source_database_instance": source_database_instance,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if backup_retention is not None:
            self._values["backup_retention"] = backup_retention
        if cloudwatch_logs_exports is not None:
            self._values["cloudwatch_logs_exports"] = cloudwatch_logs_exports
        if cloudwatch_logs_retention is not None:
            self._values["cloudwatch_logs_retention"] = cloudwatch_logs_retention
        if cloudwatch_logs_retention_role is not None:
            self._values["cloudwatch_logs_retention_role"] = cloudwatch_logs_retention_role
        if copy_tags_to_snapshot is not None:
            self._values["copy_tags_to_snapshot"] = copy_tags_to_snapshot
        if delete_automated_backups is not None:
            self._values["delete_automated_backups"] = delete_automated_backups
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if domain is not None:
            self._values["domain"] = domain
        if domain_role is not None:
            self._values["domain_role"] = domain_role
        if enable_performance_insights is not None:
            self._values["enable_performance_insights"] = enable_performance_insights
        if iam_authentication is not None:
            self._values["iam_authentication"] = iam_authentication
        if instance_identifier is not None:
            self._values["instance_identifier"] = instance_identifier
        if iops is not None:
            self._values["iops"] = iops
        if max_allocated_storage is not None:
            self._values["max_allocated_storage"] = max_allocated_storage
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_role is not None:
            self._values["monitoring_role"] = monitoring_role
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if option_group is not None:
            self._values["option_group"] = option_group
        if performance_insight_encryption_key is not None:
            self._values["performance_insight_encryption_key"] = performance_insight_encryption_key
        if performance_insight_retention is not None:
            self._values["performance_insight_retention"] = performance_insight_retention
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if processor_features is not None:
            self._values["processor_features"] = processor_features
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if vpc_placement is not None:
            self._values["vpc_placement"] = vpc_placement
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if storage_encryption_key is not None:
            self._values["storage_encryption_key"] = storage_encryption_key

    @builtins.property
    def vpc(self) -> _IVpc_3795853f:
        """The VPC network where the DB subnet group should be created.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def auto_minor_version_upgrade(self) -> typing.Optional[bool]:
        """Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("auto_minor_version_upgrade")

    @builtins.property
    def availability_zone(self) -> typing.Optional[str]:
        """The name of the Availability Zone where the DB instance will be located.

        default
        :default: - no preference

        stability
        :stability: experimental
        """
        return self._values.get("availability_zone")

    @builtins.property
    def backup_retention(self) -> typing.Optional[_Duration_5170c158]:
        """The number of days during which automatic DB snapshots are retained.

        Set
        to zero to disable backups.

        default
        :default: Duration.days(1)

        stability
        :stability: experimental
        """
        return self._values.get("backup_retention")

    @builtins.property
    def cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """The list of log types that need to be enabled for exporting to CloudWatch Logs.

        default
        :default: - no log exports

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_exports")

    @builtins.property
    def cloudwatch_logs_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``Infinity``.

        default
        :default: - logs never expire

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_retention")

    @builtins.property
    def cloudwatch_logs_retention_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        default
        :default: - a new role is created.

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_retention_role")

    @builtins.property
    def copy_tags_to_snapshot(self) -> typing.Optional[bool]:
        """Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("copy_tags_to_snapshot")

    @builtins.property
    def delete_automated_backups(self) -> typing.Optional[bool]:
        """Indicates whether automated backups should be deleted or retained when you delete a DB instance.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("delete_automated_backups")

    @builtins.property
    def deletion_protection(self) -> typing.Optional[bool]:
        """Indicates whether the DB instance should have deletion protection enabled.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("deletion_protection")

    @builtins.property
    def domain(self) -> typing.Optional[str]:
        """The Active Directory directory ID to create the DB instance in.

        default
        :default: - Do not join domain

        stability
        :stability: experimental
        """
        return self._values.get("domain")

    @builtins.property
    def domain_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role to be used when making API calls to the Directory Service.

        The role needs the AWS-managed policy
        AmazonRDSDirectoryServiceAccess or equivalent.

        default
        :default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified

        stability
        :stability: experimental
        """
        return self._values.get("domain_role")

    @builtins.property
    def enable_performance_insights(self) -> typing.Optional[bool]:
        """Whether to enable Performance Insights for the DB instance.

        default
        :default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.

        stability
        :stability: experimental
        """
        return self._values.get("enable_performance_insights")

    @builtins.property
    def iam_authentication(self) -> typing.Optional[bool]:
        """Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("iam_authentication")

    @builtins.property
    def instance_identifier(self) -> typing.Optional[str]:
        """A name for the DB instance.

        If you specify a name, AWS CloudFormation
        converts it to lowercase.

        default
        :default: - a CloudFormation generated name

        stability
        :stability: experimental
        """
        return self._values.get("instance_identifier")

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) that the database provisions.

        The value must be equal to or greater than 1000.

        default
        :default: - no provisioned iops

        stability
        :stability: experimental
        """
        return self._values.get("iops")

    @builtins.property
    def max_allocated_storage(self) -> typing.Optional[jsii.Number]:
        """Upper limit to which RDS can scale the storage in GiB(Gibibyte).

        default
        :default: - No autoscaling of RDS instance

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling
        stability
        :stability: experimental
        """
        return self._values.get("max_allocated_storage")

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[_Duration_5170c158]:
        """The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance.

        default
        :default: - no enhanced monitoring

        stability
        :stability: experimental
        """
        return self._values.get("monitoring_interval")

    @builtins.property
    def monitoring_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that will be used to manage DB instance monitoring.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get("monitoring_role")

    @builtins.property
    def multi_az(self) -> typing.Optional[bool]:
        """Specifies if the database instance is a multiple Availability Zone deployment.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("multi_az")

    @builtins.property
    def option_group(self) -> typing.Optional["IOptionGroup"]:
        """The option group to associate with the instance.

        default
        :default: - no option group

        stability
        :stability: experimental
        """
        return self._values.get("option_group")

    @builtins.property
    def performance_insight_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The AWS KMS key for encryption of Performance Insights data.

        default
        :default: - default master key

        stability
        :stability: experimental
        """
        return self._values.get("performance_insight_encryption_key")

    @builtins.property
    def performance_insight_retention(
        self,
    ) -> typing.Optional["PerformanceInsightRetention"]:
        """The amount of time, in days, to retain Performance Insights data.

        default
        :default: 7

        stability
        :stability: experimental
        """
        return self._values.get("performance_insight_retention")

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port for the instance.

        default
        :default: - the default port for the chosen engine.

        stability
        :stability: experimental
        """
        return self._values.get("port")

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[str]:
        """The daily time range during which automated backups are performed.

        Constraints:

        - Must be in the format ``hh24:mi-hh24:mi``.
        - Must be in Universal Coordinated Time (UTC).
        - Must not conflict with the preferred maintenance window.
        - Must be at least 30 minutes.

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region. To see the time blocks available, see
          https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow

        stability
        :stability: experimental
        """
        return self._values.get("preferred_backup_window")

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """The weekly time range (in UTC) during which system maintenance can occur.

        Format: ``ddd:hh24:mi-ddd:hh24:mi``
        Constraint: Minimum 30-minute window

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region, occurring on a random day of the week. To see
          the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance

        stability
        :stability: experimental
        """
        return self._values.get("preferred_maintenance_window")

    @builtins.property
    def processor_features(self) -> typing.Optional["ProcessorFeatures"]:
        """The number of CPU cores and the number of threads per core.

        default
        :default:

        - the default number of CPU cores and threads per core for the
          chosen instance class.

        See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor

        stability
        :stability: experimental
        """
        return self._values.get("processor_features")

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update.

        default
        :default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)

        stability
        :stability: experimental
        """
        return self._values.get("removal_policy")

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The security groups to assign to the DB instance.

        default
        :default: - a new security group is created

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    @builtins.property
    def storage_type(self) -> typing.Optional["StorageType"]:
        """The storage type.

        default
        :default: GP2

        stability
        :stability: experimental
        """
        return self._values.get("storage_type")

    @builtins.property
    def vpc_placement(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The type of subnets to add to the created DB subnet group.

        default
        :default: - private subnets

        deprecated
        :deprecated: use ``vpcSubnets``

        stability
        :stability: deprecated
        """
        return self._values.get("vpc_placement")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The type of subnets to add to the created DB subnet group.

        default
        :default: - private subnets

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    @builtins.property
    def instance_type(self) -> _InstanceType_85a97b30:
        """The name of the compute and memory capacity classes.

        stability
        :stability: experimental
        """
        return self._values.get("instance_type")

    @builtins.property
    def source_database_instance(self) -> "IDatabaseInstance":
        """The source database instance.

        Each DB instance can have a limited number of read replicas. For more
        information, see https://docs.aws.amazon.com/AmazonRDS/latest/DeveloperGuide/USER_ReadRepl.html.

        stability
        :stability: experimental
        """
        return self._values.get("source_database_instance")

    @builtins.property
    def storage_encrypted(self) -> typing.Optional[bool]:
        """Indicates whether the DB instance is encrypted.

        default
        :default: - true if storageEncryptionKey has been provided, false otherwise

        stability
        :stability: experimental
        """
        return self._values.get("storage_encrypted")

    @builtins.property
    def storage_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The KMS key that's used to encrypt the DB instance.

        default
        :default: - default master key if storageEncrypted is true, no key otherwise

        stability
        :stability: experimental
        """
        return self._values.get("storage_encryption_key")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseInstanceReadReplicaProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.DatabaseInstanceSourceProps",
    jsii_struct_bases=[DatabaseInstanceNewProps],
    name_mapping={
        "vpc": "vpc",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "backup_retention": "backupRetention",
        "cloudwatch_logs_exports": "cloudwatchLogsExports",
        "cloudwatch_logs_retention": "cloudwatchLogsRetention",
        "cloudwatch_logs_retention_role": "cloudwatchLogsRetentionRole",
        "copy_tags_to_snapshot": "copyTagsToSnapshot",
        "delete_automated_backups": "deleteAutomatedBackups",
        "deletion_protection": "deletionProtection",
        "domain": "domain",
        "domain_role": "domainRole",
        "enable_performance_insights": "enablePerformanceInsights",
        "iam_authentication": "iamAuthentication",
        "instance_identifier": "instanceIdentifier",
        "iops": "iops",
        "max_allocated_storage": "maxAllocatedStorage",
        "monitoring_interval": "monitoringInterval",
        "monitoring_role": "monitoringRole",
        "multi_az": "multiAz",
        "option_group": "optionGroup",
        "performance_insight_encryption_key": "performanceInsightEncryptionKey",
        "performance_insight_retention": "performanceInsightRetention",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "processor_features": "processorFeatures",
        "removal_policy": "removalPolicy",
        "security_groups": "securityGroups",
        "storage_type": "storageType",
        "vpc_placement": "vpcPlacement",
        "vpc_subnets": "vpcSubnets",
        "engine": "engine",
        "allocated_storage": "allocatedStorage",
        "allow_major_version_upgrade": "allowMajorVersionUpgrade",
        "database_name": "databaseName",
        "instance_type": "instanceType",
        "license_model": "licenseModel",
        "master_user_password": "masterUserPassword",
        "master_user_password_encryption_key": "masterUserPasswordEncryptionKey",
        "parameter_group": "parameterGroup",
        "timezone": "timezone",
    },
)
class DatabaseInstanceSourceProps(DatabaseInstanceNewProps):
    def __init__(
        self,
        *,
        vpc: _IVpc_3795853f,
        auto_minor_version_upgrade: typing.Optional[bool] = None,
        availability_zone: typing.Optional[str] = None,
        backup_retention: typing.Optional[_Duration_5170c158] = None,
        cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        cloudwatch_logs_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        cloudwatch_logs_retention_role: typing.Optional[_IRole_e69bbae4] = None,
        copy_tags_to_snapshot: typing.Optional[bool] = None,
        delete_automated_backups: typing.Optional[bool] = None,
        deletion_protection: typing.Optional[bool] = None,
        domain: typing.Optional[str] = None,
        domain_role: typing.Optional[_IRole_e69bbae4] = None,
        enable_performance_insights: typing.Optional[bool] = None,
        iam_authentication: typing.Optional[bool] = None,
        instance_identifier: typing.Optional[str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[_Duration_5170c158] = None,
        monitoring_role: typing.Optional[_IRole_e69bbae4] = None,
        multi_az: typing.Optional[bool] = None,
        option_group: typing.Optional["IOptionGroup"] = None,
        performance_insight_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        performance_insight_retention: typing.Optional["PerformanceInsightRetention"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[str] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        processor_features: typing.Optional["ProcessorFeatures"] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        storage_type: typing.Optional["StorageType"] = None,
        vpc_placement: typing.Optional[_SubnetSelection_36a13cd6] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        engine: "IInstanceEngine",
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[bool] = None,
        database_name: typing.Optional[str] = None,
        instance_type: typing.Optional[_InstanceType_85a97b30] = None,
        license_model: typing.Optional["LicenseModel"] = None,
        master_user_password: typing.Optional[_SecretValue_99478b8b] = None,
        master_user_password_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        timezone: typing.Optional[str] = None,
    ) -> None:
        """Construction properties for a DatabaseInstanceSource.

        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. Default: Duration.days(1)
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: false
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: true
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_type: The storage type. Default: GP2
        :param vpc_placement: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param engine: The database engine.
        :param allocated_storage: The allocated storage size, specified in gigabytes (GB). Default: 100
        :param allow_major_version_upgrade: Whether to allow major version upgrades. Default: false
        :param database_name: The name of the database. Default: - no name
        :param instance_type: The name of the compute and memory capacity for the instance. Default: - m5.large (or, more specifically, db.m5.large)
        :param license_model: The license model. Default: - RDS default license model
        :param master_user_password: The master user password. Default: - a Secrets Manager generated password
        :param master_user_password_encryption_key: The KMS key used to encrypt the secret for the master user password. Default: - default master key
        :param parameter_group: The DB parameter group to associate with the instance. Default: - no parameter group
        :param timezone: The time zone of the instance. This is currently supported only by Microsoft Sql Server. Default: - RDS default timezone

        stability
        :stability: experimental
        """
        if isinstance(processor_features, dict):
            processor_features = ProcessorFeatures(**processor_features)
        if isinstance(vpc_placement, dict):
            vpc_placement = _SubnetSelection_36a13cd6(**vpc_placement)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            "vpc": vpc,
            "engine": engine,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if backup_retention is not None:
            self._values["backup_retention"] = backup_retention
        if cloudwatch_logs_exports is not None:
            self._values["cloudwatch_logs_exports"] = cloudwatch_logs_exports
        if cloudwatch_logs_retention is not None:
            self._values["cloudwatch_logs_retention"] = cloudwatch_logs_retention
        if cloudwatch_logs_retention_role is not None:
            self._values["cloudwatch_logs_retention_role"] = cloudwatch_logs_retention_role
        if copy_tags_to_snapshot is not None:
            self._values["copy_tags_to_snapshot"] = copy_tags_to_snapshot
        if delete_automated_backups is not None:
            self._values["delete_automated_backups"] = delete_automated_backups
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if domain is not None:
            self._values["domain"] = domain
        if domain_role is not None:
            self._values["domain_role"] = domain_role
        if enable_performance_insights is not None:
            self._values["enable_performance_insights"] = enable_performance_insights
        if iam_authentication is not None:
            self._values["iam_authentication"] = iam_authentication
        if instance_identifier is not None:
            self._values["instance_identifier"] = instance_identifier
        if iops is not None:
            self._values["iops"] = iops
        if max_allocated_storage is not None:
            self._values["max_allocated_storage"] = max_allocated_storage
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_role is not None:
            self._values["monitoring_role"] = monitoring_role
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if option_group is not None:
            self._values["option_group"] = option_group
        if performance_insight_encryption_key is not None:
            self._values["performance_insight_encryption_key"] = performance_insight_encryption_key
        if performance_insight_retention is not None:
            self._values["performance_insight_retention"] = performance_insight_retention
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if processor_features is not None:
            self._values["processor_features"] = processor_features
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if vpc_placement is not None:
            self._values["vpc_placement"] = vpc_placement
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if allocated_storage is not None:
            self._values["allocated_storage"] = allocated_storage
        if allow_major_version_upgrade is not None:
            self._values["allow_major_version_upgrade"] = allow_major_version_upgrade
        if database_name is not None:
            self._values["database_name"] = database_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if license_model is not None:
            self._values["license_model"] = license_model
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password
        if master_user_password_encryption_key is not None:
            self._values["master_user_password_encryption_key"] = master_user_password_encryption_key
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if timezone is not None:
            self._values["timezone"] = timezone

    @builtins.property
    def vpc(self) -> _IVpc_3795853f:
        """The VPC network where the DB subnet group should be created.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def auto_minor_version_upgrade(self) -> typing.Optional[bool]:
        """Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("auto_minor_version_upgrade")

    @builtins.property
    def availability_zone(self) -> typing.Optional[str]:
        """The name of the Availability Zone where the DB instance will be located.

        default
        :default: - no preference

        stability
        :stability: experimental
        """
        return self._values.get("availability_zone")

    @builtins.property
    def backup_retention(self) -> typing.Optional[_Duration_5170c158]:
        """The number of days during which automatic DB snapshots are retained.

        Set
        to zero to disable backups.

        default
        :default: Duration.days(1)

        stability
        :stability: experimental
        """
        return self._values.get("backup_retention")

    @builtins.property
    def cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """The list of log types that need to be enabled for exporting to CloudWatch Logs.

        default
        :default: - no log exports

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_exports")

    @builtins.property
    def cloudwatch_logs_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``Infinity``.

        default
        :default: - logs never expire

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_retention")

    @builtins.property
    def cloudwatch_logs_retention_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        default
        :default: - a new role is created.

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_retention_role")

    @builtins.property
    def copy_tags_to_snapshot(self) -> typing.Optional[bool]:
        """Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("copy_tags_to_snapshot")

    @builtins.property
    def delete_automated_backups(self) -> typing.Optional[bool]:
        """Indicates whether automated backups should be deleted or retained when you delete a DB instance.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("delete_automated_backups")

    @builtins.property
    def deletion_protection(self) -> typing.Optional[bool]:
        """Indicates whether the DB instance should have deletion protection enabled.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("deletion_protection")

    @builtins.property
    def domain(self) -> typing.Optional[str]:
        """The Active Directory directory ID to create the DB instance in.

        default
        :default: - Do not join domain

        stability
        :stability: experimental
        """
        return self._values.get("domain")

    @builtins.property
    def domain_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role to be used when making API calls to the Directory Service.

        The role needs the AWS-managed policy
        AmazonRDSDirectoryServiceAccess or equivalent.

        default
        :default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified

        stability
        :stability: experimental
        """
        return self._values.get("domain_role")

    @builtins.property
    def enable_performance_insights(self) -> typing.Optional[bool]:
        """Whether to enable Performance Insights for the DB instance.

        default
        :default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.

        stability
        :stability: experimental
        """
        return self._values.get("enable_performance_insights")

    @builtins.property
    def iam_authentication(self) -> typing.Optional[bool]:
        """Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("iam_authentication")

    @builtins.property
    def instance_identifier(self) -> typing.Optional[str]:
        """A name for the DB instance.

        If you specify a name, AWS CloudFormation
        converts it to lowercase.

        default
        :default: - a CloudFormation generated name

        stability
        :stability: experimental
        """
        return self._values.get("instance_identifier")

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) that the database provisions.

        The value must be equal to or greater than 1000.

        default
        :default: - no provisioned iops

        stability
        :stability: experimental
        """
        return self._values.get("iops")

    @builtins.property
    def max_allocated_storage(self) -> typing.Optional[jsii.Number]:
        """Upper limit to which RDS can scale the storage in GiB(Gibibyte).

        default
        :default: - No autoscaling of RDS instance

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling
        stability
        :stability: experimental
        """
        return self._values.get("max_allocated_storage")

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[_Duration_5170c158]:
        """The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance.

        default
        :default: - no enhanced monitoring

        stability
        :stability: experimental
        """
        return self._values.get("monitoring_interval")

    @builtins.property
    def monitoring_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that will be used to manage DB instance monitoring.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get("monitoring_role")

    @builtins.property
    def multi_az(self) -> typing.Optional[bool]:
        """Specifies if the database instance is a multiple Availability Zone deployment.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("multi_az")

    @builtins.property
    def option_group(self) -> typing.Optional["IOptionGroup"]:
        """The option group to associate with the instance.

        default
        :default: - no option group

        stability
        :stability: experimental
        """
        return self._values.get("option_group")

    @builtins.property
    def performance_insight_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The AWS KMS key for encryption of Performance Insights data.

        default
        :default: - default master key

        stability
        :stability: experimental
        """
        return self._values.get("performance_insight_encryption_key")

    @builtins.property
    def performance_insight_retention(
        self,
    ) -> typing.Optional["PerformanceInsightRetention"]:
        """The amount of time, in days, to retain Performance Insights data.

        default
        :default: 7

        stability
        :stability: experimental
        """
        return self._values.get("performance_insight_retention")

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port for the instance.

        default
        :default: - the default port for the chosen engine.

        stability
        :stability: experimental
        """
        return self._values.get("port")

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[str]:
        """The daily time range during which automated backups are performed.

        Constraints:

        - Must be in the format ``hh24:mi-hh24:mi``.
        - Must be in Universal Coordinated Time (UTC).
        - Must not conflict with the preferred maintenance window.
        - Must be at least 30 minutes.

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region. To see the time blocks available, see
          https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow

        stability
        :stability: experimental
        """
        return self._values.get("preferred_backup_window")

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """The weekly time range (in UTC) during which system maintenance can occur.

        Format: ``ddd:hh24:mi-ddd:hh24:mi``
        Constraint: Minimum 30-minute window

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region, occurring on a random day of the week. To see
          the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance

        stability
        :stability: experimental
        """
        return self._values.get("preferred_maintenance_window")

    @builtins.property
    def processor_features(self) -> typing.Optional["ProcessorFeatures"]:
        """The number of CPU cores and the number of threads per core.

        default
        :default:

        - the default number of CPU cores and threads per core for the
          chosen instance class.

        See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor

        stability
        :stability: experimental
        """
        return self._values.get("processor_features")

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update.

        default
        :default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)

        stability
        :stability: experimental
        """
        return self._values.get("removal_policy")

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The security groups to assign to the DB instance.

        default
        :default: - a new security group is created

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    @builtins.property
    def storage_type(self) -> typing.Optional["StorageType"]:
        """The storage type.

        default
        :default: GP2

        stability
        :stability: experimental
        """
        return self._values.get("storage_type")

    @builtins.property
    def vpc_placement(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The type of subnets to add to the created DB subnet group.

        default
        :default: - private subnets

        deprecated
        :deprecated: use ``vpcSubnets``

        stability
        :stability: deprecated
        """
        return self._values.get("vpc_placement")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The type of subnets to add to the created DB subnet group.

        default
        :default: - private subnets

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    @builtins.property
    def engine(self) -> "IInstanceEngine":
        """The database engine.

        stability
        :stability: experimental
        """
        return self._values.get("engine")

    @builtins.property
    def allocated_storage(self) -> typing.Optional[jsii.Number]:
        """The allocated storage size, specified in gigabytes (GB).

        default
        :default: 100

        stability
        :stability: experimental
        """
        return self._values.get("allocated_storage")

    @builtins.property
    def allow_major_version_upgrade(self) -> typing.Optional[bool]:
        """Whether to allow major version upgrades.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("allow_major_version_upgrade")

    @builtins.property
    def database_name(self) -> typing.Optional[str]:
        """The name of the database.

        default
        :default: - no name

        stability
        :stability: experimental
        """
        return self._values.get("database_name")

    @builtins.property
    def instance_type(self) -> typing.Optional[_InstanceType_85a97b30]:
        """The name of the compute and memory capacity for the instance.

        default
        :default: - m5.large (or, more specifically, db.m5.large)

        stability
        :stability: experimental
        """
        return self._values.get("instance_type")

    @builtins.property
    def license_model(self) -> typing.Optional["LicenseModel"]:
        """The license model.

        default
        :default: - RDS default license model

        stability
        :stability: experimental
        """
        return self._values.get("license_model")

    @builtins.property
    def master_user_password(self) -> typing.Optional[_SecretValue_99478b8b]:
        """The master user password.

        default
        :default: - a Secrets Manager generated password

        stability
        :stability: experimental
        """
        return self._values.get("master_user_password")

    @builtins.property
    def master_user_password_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The KMS key used to encrypt the secret for the master user password.

        default
        :default: - default master key

        stability
        :stability: experimental
        """
        return self._values.get("master_user_password_encryption_key")

    @builtins.property
    def parameter_group(self) -> typing.Optional["IParameterGroup"]:
        """The DB parameter group to associate with the instance.

        default
        :default: - no parameter group

        stability
        :stability: experimental
        """
        return self._values.get("parameter_group")

    @builtins.property
    def timezone(self) -> typing.Optional[str]:
        """The time zone of the instance.

        This is currently supported only by Microsoft Sql Server.

        default
        :default: - RDS default timezone

        stability
        :stability: experimental
        """
        return self._values.get("timezone")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseInstanceSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.DatabaseProxyAttributes",
    jsii_struct_bases=[],
    name_mapping={
        "db_proxy_arn": "dbProxyArn",
        "db_proxy_name": "dbProxyName",
        "endpoint": "endpoint",
        "security_groups": "securityGroups",
    },
)
class DatabaseProxyAttributes:
    def __init__(
        self,
        *,
        db_proxy_arn: str,
        db_proxy_name: str,
        endpoint: str,
        security_groups: typing.List[_ISecurityGroup_d72ab8e8],
    ) -> None:
        """Properties that describe an existing DB Proxy.

        :param db_proxy_arn: DB Proxy ARN.
        :param db_proxy_name: DB Proxy Name.
        :param endpoint: Endpoint.
        :param security_groups: The security groups of the instance.

        stability
        :stability: experimental
        """
        self._values = {
            "db_proxy_arn": db_proxy_arn,
            "db_proxy_name": db_proxy_name,
            "endpoint": endpoint,
            "security_groups": security_groups,
        }

    @builtins.property
    def db_proxy_arn(self) -> str:
        """DB Proxy ARN.

        stability
        :stability: experimental
        """
        return self._values.get("db_proxy_arn")

    @builtins.property
    def db_proxy_name(self) -> str:
        """DB Proxy Name.

        stability
        :stability: experimental
        """
        return self._values.get("db_proxy_name")

    @builtins.property
    def endpoint(self) -> str:
        """Endpoint.

        stability
        :stability: experimental
        """
        return self._values.get("endpoint")

    @builtins.property
    def security_groups(self) -> typing.List[_ISecurityGroup_d72ab8e8]:
        """The security groups of the instance.

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseProxyAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.DatabaseProxyOptions",
    jsii_struct_bases=[],
    name_mapping={
        "secrets": "secrets",
        "vpc": "vpc",
        "borrow_timeout": "borrowTimeout",
        "db_proxy_name": "dbProxyName",
        "debug_logging": "debugLogging",
        "iam_auth": "iamAuth",
        "idle_client_timeout": "idleClientTimeout",
        "init_query": "initQuery",
        "max_connections_percent": "maxConnectionsPercent",
        "max_idle_connections_percent": "maxIdleConnectionsPercent",
        "require_tls": "requireTLS",
        "role": "role",
        "security_groups": "securityGroups",
        "session_pinning_filters": "sessionPinningFilters",
        "vpc_subnets": "vpcSubnets",
    },
)
class DatabaseProxyOptions:
    def __init__(
        self,
        *,
        secrets: typing.List[_ISecret_75279d36],
        vpc: _IVpc_3795853f,
        borrow_timeout: typing.Optional[_Duration_5170c158] = None,
        db_proxy_name: typing.Optional[str] = None,
        debug_logging: typing.Optional[bool] = None,
        iam_auth: typing.Optional[bool] = None,
        idle_client_timeout: typing.Optional[_Duration_5170c158] = None,
        init_query: typing.Optional[str] = None,
        max_connections_percent: typing.Optional[jsii.Number] = None,
        max_idle_connections_percent: typing.Optional[jsii.Number] = None,
        require_tls: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        session_pinning_filters: typing.Optional[typing.List["SessionPinningFilter"]] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> None:
        """Options for a new DatabaseProxy.

        :param secrets: The secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster. These secrets are stored within Amazon Secrets Manager. One or more secrets are required.
        :param vpc: The VPC to associate with the new proxy.
        :param borrow_timeout: The duration for a proxy to wait for a connection to become available in the connection pool. Only applies when the proxy has opened its maximum number of connections and all connections are busy with client sessions. Value must be between 1 second and 1 hour, or ``Duration.seconds(0)`` to represent unlimited. Default: cdk.Duration.seconds(120)
        :param db_proxy_name: The identifier for the proxy. This name must be unique for all proxies owned by your AWS account in the specified AWS Region. An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two consecutive hyphens. Default: - Generated by CloudFormation (recommended)
        :param debug_logging: Whether the proxy includes detailed information about SQL statements in its logs. This information helps you to debug issues involving SQL behavior or the performance and scalability of the proxy connections. The debug information includes the text of SQL statements that you submit through the proxy. Thus, only enable this setting when needed for debugging, and only when you have security measures in place to safeguard any sensitive information that appears in the logs. Default: false
        :param iam_auth: Whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy. Default: false
        :param idle_client_timeout: The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it. You can set this value higher or lower than the connection timeout limit for the associated database. Default: cdk.Duration.minutes(30)
        :param init_query: One or more SQL statements for the proxy to run when opening each new database connection. Typically used with SET statements to make sure that each connection has identical settings such as time zone and character set. For multiple statements, use semicolons as the separator. You can also include multiple variables in a single SET statement, such as SET x=1, y=2. not currently supported for PostgreSQL. Default: - no initialization query
        :param max_connections_percent: The maximum size of the connection pool for each target in a target group. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. 1-100 Default: 100
        :param max_idle_connections_percent: Controls how actively the proxy closes idle database connections in the connection pool. A high value enables the proxy to leave a high percentage of idle connections open. A low value causes the proxy to close idle client connections and return the underlying database connections to the connection pool. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. between 0 and MaxConnectionsPercent Default: 50
        :param require_tls: A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy. By enabling this setting, you can enforce encrypted TLS connections to the proxy. Default: true
        :param role: IAM role that the proxy uses to access secrets in AWS Secrets Manager. Default: - A role will automatically be created
        :param security_groups: One or more VPC security groups to associate with the new proxy. Default: - No security groups
        :param session_pinning_filters: Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection. Including an item in the list exempts that class of SQL operations from the pinning behavior. Default: - no session pinning filters
        :param vpc_subnets: The subnets used by the proxy. Default: - the VPC default strategy if not specified.

        stability
        :stability: experimental
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            "secrets": secrets,
            "vpc": vpc,
        }
        if borrow_timeout is not None:
            self._values["borrow_timeout"] = borrow_timeout
        if db_proxy_name is not None:
            self._values["db_proxy_name"] = db_proxy_name
        if debug_logging is not None:
            self._values["debug_logging"] = debug_logging
        if iam_auth is not None:
            self._values["iam_auth"] = iam_auth
        if idle_client_timeout is not None:
            self._values["idle_client_timeout"] = idle_client_timeout
        if init_query is not None:
            self._values["init_query"] = init_query
        if max_connections_percent is not None:
            self._values["max_connections_percent"] = max_connections_percent
        if max_idle_connections_percent is not None:
            self._values["max_idle_connections_percent"] = max_idle_connections_percent
        if require_tls is not None:
            self._values["require_tls"] = require_tls
        if role is not None:
            self._values["role"] = role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if session_pinning_filters is not None:
            self._values["session_pinning_filters"] = session_pinning_filters
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def secrets(self) -> typing.List[_ISecret_75279d36]:
        """The secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster.

        These secrets are stored within Amazon Secrets Manager.
        One or more secrets are required.

        stability
        :stability: experimental
        """
        return self._values.get("secrets")

    @builtins.property
    def vpc(self) -> _IVpc_3795853f:
        """The VPC to associate with the new proxy.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def borrow_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The duration for a proxy to wait for a connection to become available in the connection pool.

        Only applies when the proxy has opened its maximum number of connections and all connections are busy with client
        sessions.

        Value must be between 1 second and 1 hour, or ``Duration.seconds(0)`` to represent unlimited.

        default
        :default: cdk.Duration.seconds(120)

        stability
        :stability: experimental
        """
        return self._values.get("borrow_timeout")

    @builtins.property
    def db_proxy_name(self) -> typing.Optional[str]:
        """The identifier for the proxy.

        This name must be unique for all proxies owned by your AWS account in the specified AWS Region.
        An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens;
        it can't end with a hyphen or contain two consecutive hyphens.

        default
        :default: - Generated by CloudFormation (recommended)

        stability
        :stability: experimental
        """
        return self._values.get("db_proxy_name")

    @builtins.property
    def debug_logging(self) -> typing.Optional[bool]:
        """Whether the proxy includes detailed information about SQL statements in its logs.

        This information helps you to debug issues involving SQL behavior or the performance and scalability of the proxy connections.
        The debug information includes the text of SQL statements that you submit through the proxy.
        Thus, only enable this setting when needed for debugging, and only when you have security measures in place to safeguard any sensitive
        information that appears in the logs.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("debug_logging")

    @builtins.property
    def iam_auth(self) -> typing.Optional[bool]:
        """Whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("iam_auth")

    @builtins.property
    def idle_client_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it.

        You can set this value higher or lower than the connection timeout limit for the associated database.

        default
        :default: cdk.Duration.minutes(30)

        stability
        :stability: experimental
        """
        return self._values.get("idle_client_timeout")

    @builtins.property
    def init_query(self) -> typing.Optional[str]:
        """One or more SQL statements for the proxy to run when opening each new database connection.

        Typically used with SET statements to make sure that each connection has identical settings such as time zone
        and character set.
        For multiple statements, use semicolons as the separator.
        You can also include multiple variables in a single SET statement, such as SET x=1, y=2.

        not currently supported for PostgreSQL.

        default
        :default: - no initialization query

        stability
        :stability: experimental
        """
        return self._values.get("init_query")

    @builtins.property
    def max_connections_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum size of the connection pool for each target in a target group.

        For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB
        cluster used by the target group.

        1-100

        default
        :default: 100

        stability
        :stability: experimental
        """
        return self._values.get("max_connections_percent")

    @builtins.property
    def max_idle_connections_percent(self) -> typing.Optional[jsii.Number]:
        """Controls how actively the proxy closes idle database connections in the connection pool.

        A high value enables the proxy to leave a high percentage of idle connections open.
        A low value causes the proxy to close idle client connections and return the underlying database connections
        to the connection pool.
        For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance
        or Aurora DB cluster used by the target group.

        between 0 and MaxConnectionsPercent

        default
        :default: 50

        stability
        :stability: experimental
        """
        return self._values.get("max_idle_connections_percent")

    @builtins.property
    def require_tls(self) -> typing.Optional[bool]:
        """A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy.

        By enabling this setting, you can enforce encrypted TLS connections to the proxy.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("require_tls")

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """IAM role that the proxy uses to access secrets in AWS Secrets Manager.

        default
        :default: - A role will automatically be created

        stability
        :stability: experimental
        """
        return self._values.get("role")

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """One or more VPC security groups to associate with the new proxy.

        default
        :default: - No security groups

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    @builtins.property
    def session_pinning_filters(
        self,
    ) -> typing.Optional[typing.List["SessionPinningFilter"]]:
        """Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection.

        Including an item in the list exempts that class of SQL operations from the pinning behavior.

        default
        :default: - no session pinning filters

        stability
        :stability: experimental
        """
        return self._values.get("session_pinning_filters")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The subnets used by the proxy.

        default
        :default: - the VPC default strategy if not specified.

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseProxyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.DatabaseProxyProps",
    jsii_struct_bases=[DatabaseProxyOptions],
    name_mapping={
        "secrets": "secrets",
        "vpc": "vpc",
        "borrow_timeout": "borrowTimeout",
        "db_proxy_name": "dbProxyName",
        "debug_logging": "debugLogging",
        "iam_auth": "iamAuth",
        "idle_client_timeout": "idleClientTimeout",
        "init_query": "initQuery",
        "max_connections_percent": "maxConnectionsPercent",
        "max_idle_connections_percent": "maxIdleConnectionsPercent",
        "require_tls": "requireTLS",
        "role": "role",
        "security_groups": "securityGroups",
        "session_pinning_filters": "sessionPinningFilters",
        "vpc_subnets": "vpcSubnets",
        "proxy_target": "proxyTarget",
    },
)
class DatabaseProxyProps(DatabaseProxyOptions):
    def __init__(
        self,
        *,
        secrets: typing.List[_ISecret_75279d36],
        vpc: _IVpc_3795853f,
        borrow_timeout: typing.Optional[_Duration_5170c158] = None,
        db_proxy_name: typing.Optional[str] = None,
        debug_logging: typing.Optional[bool] = None,
        iam_auth: typing.Optional[bool] = None,
        idle_client_timeout: typing.Optional[_Duration_5170c158] = None,
        init_query: typing.Optional[str] = None,
        max_connections_percent: typing.Optional[jsii.Number] = None,
        max_idle_connections_percent: typing.Optional[jsii.Number] = None,
        require_tls: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        session_pinning_filters: typing.Optional[typing.List["SessionPinningFilter"]] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        proxy_target: "ProxyTarget",
    ) -> None:
        """Construction properties for a DatabaseProxy.

        :param secrets: The secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster. These secrets are stored within Amazon Secrets Manager. One or more secrets are required.
        :param vpc: The VPC to associate with the new proxy.
        :param borrow_timeout: The duration for a proxy to wait for a connection to become available in the connection pool. Only applies when the proxy has opened its maximum number of connections and all connections are busy with client sessions. Value must be between 1 second and 1 hour, or ``Duration.seconds(0)`` to represent unlimited. Default: cdk.Duration.seconds(120)
        :param db_proxy_name: The identifier for the proxy. This name must be unique for all proxies owned by your AWS account in the specified AWS Region. An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two consecutive hyphens. Default: - Generated by CloudFormation (recommended)
        :param debug_logging: Whether the proxy includes detailed information about SQL statements in its logs. This information helps you to debug issues involving SQL behavior or the performance and scalability of the proxy connections. The debug information includes the text of SQL statements that you submit through the proxy. Thus, only enable this setting when needed for debugging, and only when you have security measures in place to safeguard any sensitive information that appears in the logs. Default: false
        :param iam_auth: Whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy. Default: false
        :param idle_client_timeout: The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it. You can set this value higher or lower than the connection timeout limit for the associated database. Default: cdk.Duration.minutes(30)
        :param init_query: One or more SQL statements for the proxy to run when opening each new database connection. Typically used with SET statements to make sure that each connection has identical settings such as time zone and character set. For multiple statements, use semicolons as the separator. You can also include multiple variables in a single SET statement, such as SET x=1, y=2. not currently supported for PostgreSQL. Default: - no initialization query
        :param max_connections_percent: The maximum size of the connection pool for each target in a target group. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. 1-100 Default: 100
        :param max_idle_connections_percent: Controls how actively the proxy closes idle database connections in the connection pool. A high value enables the proxy to leave a high percentage of idle connections open. A low value causes the proxy to close idle client connections and return the underlying database connections to the connection pool. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. between 0 and MaxConnectionsPercent Default: 50
        :param require_tls: A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy. By enabling this setting, you can enforce encrypted TLS connections to the proxy. Default: true
        :param role: IAM role that the proxy uses to access secrets in AWS Secrets Manager. Default: - A role will automatically be created
        :param security_groups: One or more VPC security groups to associate with the new proxy. Default: - No security groups
        :param session_pinning_filters: Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection. Including an item in the list exempts that class of SQL operations from the pinning behavior. Default: - no session pinning filters
        :param vpc_subnets: The subnets used by the proxy. Default: - the VPC default strategy if not specified.
        :param proxy_target: DB proxy target: Instance or Cluster.

        stability
        :stability: experimental
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            "secrets": secrets,
            "vpc": vpc,
            "proxy_target": proxy_target,
        }
        if borrow_timeout is not None:
            self._values["borrow_timeout"] = borrow_timeout
        if db_proxy_name is not None:
            self._values["db_proxy_name"] = db_proxy_name
        if debug_logging is not None:
            self._values["debug_logging"] = debug_logging
        if iam_auth is not None:
            self._values["iam_auth"] = iam_auth
        if idle_client_timeout is not None:
            self._values["idle_client_timeout"] = idle_client_timeout
        if init_query is not None:
            self._values["init_query"] = init_query
        if max_connections_percent is not None:
            self._values["max_connections_percent"] = max_connections_percent
        if max_idle_connections_percent is not None:
            self._values["max_idle_connections_percent"] = max_idle_connections_percent
        if require_tls is not None:
            self._values["require_tls"] = require_tls
        if role is not None:
            self._values["role"] = role
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if session_pinning_filters is not None:
            self._values["session_pinning_filters"] = session_pinning_filters
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def secrets(self) -> typing.List[_ISecret_75279d36]:
        """The secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster.

        These secrets are stored within Amazon Secrets Manager.
        One or more secrets are required.

        stability
        :stability: experimental
        """
        return self._values.get("secrets")

    @builtins.property
    def vpc(self) -> _IVpc_3795853f:
        """The VPC to associate with the new proxy.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def borrow_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The duration for a proxy to wait for a connection to become available in the connection pool.

        Only applies when the proxy has opened its maximum number of connections and all connections are busy with client
        sessions.

        Value must be between 1 second and 1 hour, or ``Duration.seconds(0)`` to represent unlimited.

        default
        :default: cdk.Duration.seconds(120)

        stability
        :stability: experimental
        """
        return self._values.get("borrow_timeout")

    @builtins.property
    def db_proxy_name(self) -> typing.Optional[str]:
        """The identifier for the proxy.

        This name must be unique for all proxies owned by your AWS account in the specified AWS Region.
        An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens;
        it can't end with a hyphen or contain two consecutive hyphens.

        default
        :default: - Generated by CloudFormation (recommended)

        stability
        :stability: experimental
        """
        return self._values.get("db_proxy_name")

    @builtins.property
    def debug_logging(self) -> typing.Optional[bool]:
        """Whether the proxy includes detailed information about SQL statements in its logs.

        This information helps you to debug issues involving SQL behavior or the performance and scalability of the proxy connections.
        The debug information includes the text of SQL statements that you submit through the proxy.
        Thus, only enable this setting when needed for debugging, and only when you have security measures in place to safeguard any sensitive
        information that appears in the logs.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("debug_logging")

    @builtins.property
    def iam_auth(self) -> typing.Optional[bool]:
        """Whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("iam_auth")

    @builtins.property
    def idle_client_timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it.

        You can set this value higher or lower than the connection timeout limit for the associated database.

        default
        :default: cdk.Duration.minutes(30)

        stability
        :stability: experimental
        """
        return self._values.get("idle_client_timeout")

    @builtins.property
    def init_query(self) -> typing.Optional[str]:
        """One or more SQL statements for the proxy to run when opening each new database connection.

        Typically used with SET statements to make sure that each connection has identical settings such as time zone
        and character set.
        For multiple statements, use semicolons as the separator.
        You can also include multiple variables in a single SET statement, such as SET x=1, y=2.

        not currently supported for PostgreSQL.

        default
        :default: - no initialization query

        stability
        :stability: experimental
        """
        return self._values.get("init_query")

    @builtins.property
    def max_connections_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum size of the connection pool for each target in a target group.

        For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB
        cluster used by the target group.

        1-100

        default
        :default: 100

        stability
        :stability: experimental
        """
        return self._values.get("max_connections_percent")

    @builtins.property
    def max_idle_connections_percent(self) -> typing.Optional[jsii.Number]:
        """Controls how actively the proxy closes idle database connections in the connection pool.

        A high value enables the proxy to leave a high percentage of idle connections open.
        A low value causes the proxy to close idle client connections and return the underlying database connections
        to the connection pool.
        For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance
        or Aurora DB cluster used by the target group.

        between 0 and MaxConnectionsPercent

        default
        :default: 50

        stability
        :stability: experimental
        """
        return self._values.get("max_idle_connections_percent")

    @builtins.property
    def require_tls(self) -> typing.Optional[bool]:
        """A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy.

        By enabling this setting, you can enforce encrypted TLS connections to the proxy.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("require_tls")

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """IAM role that the proxy uses to access secrets in AWS Secrets Manager.

        default
        :default: - A role will automatically be created

        stability
        :stability: experimental
        """
        return self._values.get("role")

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """One or more VPC security groups to associate with the new proxy.

        default
        :default: - No security groups

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    @builtins.property
    def session_pinning_filters(
        self,
    ) -> typing.Optional[typing.List["SessionPinningFilter"]]:
        """Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection.

        Including an item in the list exempts that class of SQL operations from the pinning behavior.

        default
        :default: - no session pinning filters

        stability
        :stability: experimental
        """
        return self._values.get("session_pinning_filters")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The subnets used by the proxy.

        default
        :default: - the VPC default strategy if not specified.

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    @builtins.property
    def proxy_target(self) -> "ProxyTarget":
        """DB proxy target: Instance or Cluster.

        stability
        :stability: experimental
        """
        return self._values.get("proxy_target")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseProxyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DatabaseSecret(
    _Secret_01d21232,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.DatabaseSecret",
):
    """A database secret.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::SecretsManager::Secret
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        username: str,
        encryption_key: typing.Optional[_IKey_3336c79d] = None,
        master_secret: typing.Optional[_ISecret_75279d36] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param username: The username.
        :param encryption_key: The KMS key to use to encrypt the secret. Default: default master key
        :param master_secret: The master secret which will be used to rotate this secret. Default: - no master secret information will be included

        stability
        :stability: experimental
        """
        props = DatabaseSecretProps(
            username=username,
            encryption_key=encryption_key,
            master_secret=master_secret,
        )

        jsii.create(DatabaseSecret, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.DatabaseSecretProps",
    jsii_struct_bases=[],
    name_mapping={
        "username": "username",
        "encryption_key": "encryptionKey",
        "master_secret": "masterSecret",
    },
)
class DatabaseSecretProps:
    def __init__(
        self,
        *,
        username: str,
        encryption_key: typing.Optional[_IKey_3336c79d] = None,
        master_secret: typing.Optional[_ISecret_75279d36] = None,
    ) -> None:
        """Construction properties for a DatabaseSecret.

        :param username: The username.
        :param encryption_key: The KMS key to use to encrypt the secret. Default: default master key
        :param master_secret: The master secret which will be used to rotate this secret. Default: - no master secret information will be included

        stability
        :stability: experimental
        """
        self._values = {
            "username": username,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if master_secret is not None:
            self._values["master_secret"] = master_secret

    @builtins.property
    def username(self) -> str:
        """The username.

        stability
        :stability: experimental
        """
        return self._values.get("username")

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The KMS key to use to encrypt the secret.

        default
        :default: default master key

        stability
        :stability: experimental
        """
        return self._values.get("encryption_key")

    @builtins.property
    def master_secret(self) -> typing.Optional[_ISecret_75279d36]:
        """The master secret which will be used to rotate this secret.

        default
        :default: - no master secret information will be included

        stability
        :stability: experimental
        """
        return self._values.get("master_secret")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseSecretProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Endpoint(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_rds.Endpoint"
):
    """Connection endpoint of a database cluster or instance.

    Consists of a combination of hostname and port.

    stability
    :stability: experimental
    """

    def __init__(self, address: str, port: jsii.Number) -> None:
        """
        :param address: -
        :param port: -

        stability
        :stability: experimental
        """
        jsii.create(Endpoint, self, [address, port])

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> str:
        """The hostname of the endpoint.

        stability
        :stability: experimental
        """
        return jsii.get(self, "hostname")

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        """The port of the endpoint.

        stability
        :stability: experimental
        """
        return jsii.get(self, "port")

    @builtins.property
    @jsii.member(jsii_name="socketAddress")
    def socket_address(self) -> str:
        """The combination of "HOSTNAME:PORT" for this endpoint.

        stability
        :stability: experimental
        """
        return jsii.get(self, "socketAddress")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.EngineVersion",
    jsii_struct_bases=[],
    name_mapping={"major_version": "majorVersion", "full_version": "fullVersion"},
)
class EngineVersion:
    def __init__(
        self, *, major_version: str, full_version: typing.Optional[str] = None
    ) -> None:
        """A version of an engine - for either a cluster, or instance.

        :param major_version: The major version of the engine, for example, "5.6". Used in specifying the ParameterGroup family and OptionGroup version for this engine.
        :param full_version: The full version string of the engine, for example, "5.6.mysql_aurora.1.22.1". It can be undefined, which means RDS should use whatever version it deems appropriate for the given engine type. Default: - no version specified

        stability
        :stability: experimental
        """
        self._values = {
            "major_version": major_version,
        }
        if full_version is not None:
            self._values["full_version"] = full_version

    @builtins.property
    def major_version(self) -> str:
        """The major version of the engine, for example, "5.6". Used in specifying the ParameterGroup family and OptionGroup version for this engine.

        stability
        :stability: experimental
        """
        return self._values.get("major_version")

    @builtins.property
    def full_version(self) -> typing.Optional[str]:
        """The full version string of the engine, for example, "5.6.mysql_aurora.1.22.1". It can be undefined, which means RDS should use whatever version it deems appropriate for the given engine type.

        default
        :default: - no version specified

        stability
        :stability: experimental
        """
        return self._values.get("full_version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EngineVersion(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk-experiment.aws_rds.IDatabaseCluster")
class IDatabaseCluster(
    _IResource_72f7ee7e,
    _IConnectable_a587039f,
    _ISecretAttachmentTarget_0a569782,
    jsii.compat.Protocol,
):
    """Create a clustered database with a given number of instances.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IDatabaseClusterProxy

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        """The endpoint to use for read/write operations.

        stability
        :stability: experimental
        attribute:
        :attribute:: EndpointAddress,EndpointPort
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """Identifier of the cluster.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> "Endpoint":
        """Endpoint to use for load-balanced read-only operations.

        stability
        :stability: experimental
        attribute:
        :attribute:: ReadEndpointAddress
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        """Endpoints which address each individual replica.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        """Identifiers of the replicas.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addProxy")
    def add_proxy(
        self,
        id: str,
        *,
        secrets: typing.List[_ISecret_75279d36],
        vpc: _IVpc_3795853f,
        borrow_timeout: typing.Optional[_Duration_5170c158] = None,
        db_proxy_name: typing.Optional[str] = None,
        debug_logging: typing.Optional[bool] = None,
        iam_auth: typing.Optional[bool] = None,
        idle_client_timeout: typing.Optional[_Duration_5170c158] = None,
        init_query: typing.Optional[str] = None,
        max_connections_percent: typing.Optional[jsii.Number] = None,
        max_idle_connections_percent: typing.Optional[jsii.Number] = None,
        require_tls: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        session_pinning_filters: typing.Optional[typing.List["SessionPinningFilter"]] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> "DatabaseProxy":
        """Add a new db proxy to this cluster.

        :param id: -
        :param secrets: The secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster. These secrets are stored within Amazon Secrets Manager. One or more secrets are required.
        :param vpc: The VPC to associate with the new proxy.
        :param borrow_timeout: The duration for a proxy to wait for a connection to become available in the connection pool. Only applies when the proxy has opened its maximum number of connections and all connections are busy with client sessions. Value must be between 1 second and 1 hour, or ``Duration.seconds(0)`` to represent unlimited. Default: cdk.Duration.seconds(120)
        :param db_proxy_name: The identifier for the proxy. This name must be unique for all proxies owned by your AWS account in the specified AWS Region. An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two consecutive hyphens. Default: - Generated by CloudFormation (recommended)
        :param debug_logging: Whether the proxy includes detailed information about SQL statements in its logs. This information helps you to debug issues involving SQL behavior or the performance and scalability of the proxy connections. The debug information includes the text of SQL statements that you submit through the proxy. Thus, only enable this setting when needed for debugging, and only when you have security measures in place to safeguard any sensitive information that appears in the logs. Default: false
        :param iam_auth: Whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy. Default: false
        :param idle_client_timeout: The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it. You can set this value higher or lower than the connection timeout limit for the associated database. Default: cdk.Duration.minutes(30)
        :param init_query: One or more SQL statements for the proxy to run when opening each new database connection. Typically used with SET statements to make sure that each connection has identical settings such as time zone and character set. For multiple statements, use semicolons as the separator. You can also include multiple variables in a single SET statement, such as SET x=1, y=2. not currently supported for PostgreSQL. Default: - no initialization query
        :param max_connections_percent: The maximum size of the connection pool for each target in a target group. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. 1-100 Default: 100
        :param max_idle_connections_percent: Controls how actively the proxy closes idle database connections in the connection pool. A high value enables the proxy to leave a high percentage of idle connections open. A low value causes the proxy to close idle client connections and return the underlying database connections to the connection pool. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. between 0 and MaxConnectionsPercent Default: 50
        :param require_tls: A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy. By enabling this setting, you can enforce encrypted TLS connections to the proxy. Default: true
        :param role: IAM role that the proxy uses to access secrets in AWS Secrets Manager. Default: - A role will automatically be created
        :param security_groups: One or more VPC security groups to associate with the new proxy. Default: - No security groups
        :param session_pinning_filters: Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection. Including an item in the list exempts that class of SQL operations from the pinning behavior. Default: - no session pinning filters
        :param vpc_subnets: The subnets used by the proxy. Default: - the VPC default strategy if not specified.

        stability
        :stability: experimental
        """
        ...


class _IDatabaseClusterProxy(
    jsii.proxy_for(_IResource_72f7ee7e),
    jsii.proxy_for(_IConnectable_a587039f),
    jsii.proxy_for(_ISecretAttachmentTarget_0a569782),
):
    """Create a clustered database with a given number of instances.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_rds.IDatabaseCluster"

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        """The endpoint to use for read/write operations.

        stability
        :stability: experimental
        attribute:
        :attribute:: EndpointAddress,EndpointPort
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """Identifier of the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterIdentifier")

    @builtins.property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> "Endpoint":
        """Endpoint to use for load-balanced read-only operations.

        stability
        :stability: experimental
        attribute:
        :attribute:: ReadEndpointAddress
        """
        return jsii.get(self, "clusterReadEndpoint")

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        """Endpoints which address each individual replica.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceEndpoints")

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        """Identifiers of the replicas.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceIdentifiers")

    @jsii.member(jsii_name="addProxy")
    def add_proxy(
        self,
        id: str,
        *,
        secrets: typing.List[_ISecret_75279d36],
        vpc: _IVpc_3795853f,
        borrow_timeout: typing.Optional[_Duration_5170c158] = None,
        db_proxy_name: typing.Optional[str] = None,
        debug_logging: typing.Optional[bool] = None,
        iam_auth: typing.Optional[bool] = None,
        idle_client_timeout: typing.Optional[_Duration_5170c158] = None,
        init_query: typing.Optional[str] = None,
        max_connections_percent: typing.Optional[jsii.Number] = None,
        max_idle_connections_percent: typing.Optional[jsii.Number] = None,
        require_tls: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        session_pinning_filters: typing.Optional[typing.List["SessionPinningFilter"]] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> "DatabaseProxy":
        """Add a new db proxy to this cluster.

        :param id: -
        :param secrets: The secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster. These secrets are stored within Amazon Secrets Manager. One or more secrets are required.
        :param vpc: The VPC to associate with the new proxy.
        :param borrow_timeout: The duration for a proxy to wait for a connection to become available in the connection pool. Only applies when the proxy has opened its maximum number of connections and all connections are busy with client sessions. Value must be between 1 second and 1 hour, or ``Duration.seconds(0)`` to represent unlimited. Default: cdk.Duration.seconds(120)
        :param db_proxy_name: The identifier for the proxy. This name must be unique for all proxies owned by your AWS account in the specified AWS Region. An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two consecutive hyphens. Default: - Generated by CloudFormation (recommended)
        :param debug_logging: Whether the proxy includes detailed information about SQL statements in its logs. This information helps you to debug issues involving SQL behavior or the performance and scalability of the proxy connections. The debug information includes the text of SQL statements that you submit through the proxy. Thus, only enable this setting when needed for debugging, and only when you have security measures in place to safeguard any sensitive information that appears in the logs. Default: false
        :param iam_auth: Whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy. Default: false
        :param idle_client_timeout: The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it. You can set this value higher or lower than the connection timeout limit for the associated database. Default: cdk.Duration.minutes(30)
        :param init_query: One or more SQL statements for the proxy to run when opening each new database connection. Typically used with SET statements to make sure that each connection has identical settings such as time zone and character set. For multiple statements, use semicolons as the separator. You can also include multiple variables in a single SET statement, such as SET x=1, y=2. not currently supported for PostgreSQL. Default: - no initialization query
        :param max_connections_percent: The maximum size of the connection pool for each target in a target group. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. 1-100 Default: 100
        :param max_idle_connections_percent: Controls how actively the proxy closes idle database connections in the connection pool. A high value enables the proxy to leave a high percentage of idle connections open. A low value causes the proxy to close idle client connections and return the underlying database connections to the connection pool. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. between 0 and MaxConnectionsPercent Default: 50
        :param require_tls: A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy. By enabling this setting, you can enforce encrypted TLS connections to the proxy. Default: true
        :param role: IAM role that the proxy uses to access secrets in AWS Secrets Manager. Default: - A role will automatically be created
        :param security_groups: One or more VPC security groups to associate with the new proxy. Default: - No security groups
        :param session_pinning_filters: Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection. Including an item in the list exempts that class of SQL operations from the pinning behavior. Default: - no session pinning filters
        :param vpc_subnets: The subnets used by the proxy. Default: - the VPC default strategy if not specified.

        stability
        :stability: experimental
        """
        options = DatabaseProxyOptions(
            secrets=secrets,
            vpc=vpc,
            borrow_timeout=borrow_timeout,
            db_proxy_name=db_proxy_name,
            debug_logging=debug_logging,
            iam_auth=iam_auth,
            idle_client_timeout=idle_client_timeout,
            init_query=init_query,
            max_connections_percent=max_connections_percent,
            max_idle_connections_percent=max_idle_connections_percent,
            require_tls=require_tls,
            role=role,
            security_groups=security_groups,
            session_pinning_filters=session_pinning_filters,
            vpc_subnets=vpc_subnets,
        )

        return jsii.invoke(self, "addProxy", [id, options])


@jsii.interface(jsii_type="monocdk-experiment.aws_rds.IDatabaseInstance")
class IDatabaseInstance(
    _IResource_72f7ee7e,
    _IConnectable_a587039f,
    _ISecretAttachmentTarget_0a569782,
    jsii.compat.Protocol,
):
    """A database instance.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IDatabaseInstanceProxy

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> str:
        """The instance endpoint address.

        stability
        :stability: experimental
        attribute:
        :attribute:: EndpointAddress
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> str:
        """The instance endpoint port.

        stability
        :stability: experimental
        attribute:
        :attribute:: EndpointPort
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> str:
        """The instance arn.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> "Endpoint":
        """The instance endpoint.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> str:
        """The instance identifier.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="addProxy")
    def add_proxy(
        self,
        id: str,
        *,
        secrets: typing.List[_ISecret_75279d36],
        vpc: _IVpc_3795853f,
        borrow_timeout: typing.Optional[_Duration_5170c158] = None,
        db_proxy_name: typing.Optional[str] = None,
        debug_logging: typing.Optional[bool] = None,
        iam_auth: typing.Optional[bool] = None,
        idle_client_timeout: typing.Optional[_Duration_5170c158] = None,
        init_query: typing.Optional[str] = None,
        max_connections_percent: typing.Optional[jsii.Number] = None,
        max_idle_connections_percent: typing.Optional[jsii.Number] = None,
        require_tls: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        session_pinning_filters: typing.Optional[typing.List["SessionPinningFilter"]] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> "DatabaseProxy":
        """Add a new db proxy to this instance.

        :param id: -
        :param secrets: The secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster. These secrets are stored within Amazon Secrets Manager. One or more secrets are required.
        :param vpc: The VPC to associate with the new proxy.
        :param borrow_timeout: The duration for a proxy to wait for a connection to become available in the connection pool. Only applies when the proxy has opened its maximum number of connections and all connections are busy with client sessions. Value must be between 1 second and 1 hour, or ``Duration.seconds(0)`` to represent unlimited. Default: cdk.Duration.seconds(120)
        :param db_proxy_name: The identifier for the proxy. This name must be unique for all proxies owned by your AWS account in the specified AWS Region. An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two consecutive hyphens. Default: - Generated by CloudFormation (recommended)
        :param debug_logging: Whether the proxy includes detailed information about SQL statements in its logs. This information helps you to debug issues involving SQL behavior or the performance and scalability of the proxy connections. The debug information includes the text of SQL statements that you submit through the proxy. Thus, only enable this setting when needed for debugging, and only when you have security measures in place to safeguard any sensitive information that appears in the logs. Default: false
        :param iam_auth: Whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy. Default: false
        :param idle_client_timeout: The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it. You can set this value higher or lower than the connection timeout limit for the associated database. Default: cdk.Duration.minutes(30)
        :param init_query: One or more SQL statements for the proxy to run when opening each new database connection. Typically used with SET statements to make sure that each connection has identical settings such as time zone and character set. For multiple statements, use semicolons as the separator. You can also include multiple variables in a single SET statement, such as SET x=1, y=2. not currently supported for PostgreSQL. Default: - no initialization query
        :param max_connections_percent: The maximum size of the connection pool for each target in a target group. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. 1-100 Default: 100
        :param max_idle_connections_percent: Controls how actively the proxy closes idle database connections in the connection pool. A high value enables the proxy to leave a high percentage of idle connections open. A low value causes the proxy to close idle client connections and return the underlying database connections to the connection pool. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. between 0 and MaxConnectionsPercent Default: 50
        :param require_tls: A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy. By enabling this setting, you can enforce encrypted TLS connections to the proxy. Default: true
        :param role: IAM role that the proxy uses to access secrets in AWS Secrets Manager. Default: - A role will automatically be created
        :param security_groups: One or more VPC security groups to associate with the new proxy. Default: - No security groups
        :param session_pinning_filters: Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection. Including an item in the list exempts that class of SQL operations from the pinning behavior. Default: - no session pinning filters
        :param vpc_subnets: The subnets used by the proxy. Default: - the VPC default strategy if not specified.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="grantConnect")
    def grant_connect(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity connection access to the database.

        :param grantee: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: str,
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
        """Return the given named metric for this DBInstance.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricCPUUtilization")
    def metric_cpu_utilization(
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
        """The percentage of CPU utilization.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricDatabaseConnections")
    def metric_database_connections(
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
        """The number of database connections in use.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricFreeableMemory")
    def metric_freeable_memory(
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
        """The amount of available random access memory.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricFreeStorageSpace")
    def metric_free_storage_space(
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
        """The amount of available storage space.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricReadIOPS")
    def metric_read_iops(
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
        """The average number of disk write I/O operations per second.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="metricWriteIOPS")
    def metric_write_iops(
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
        """The average number of disk read I/O operations per second.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for instance events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        ...


class _IDatabaseInstanceProxy(
    jsii.proxy_for(_IResource_72f7ee7e),
    jsii.proxy_for(_IConnectable_a587039f),
    jsii.proxy_for(_ISecretAttachmentTarget_0a569782),
):
    """A database instance.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_rds.IDatabaseInstance"

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> str:
        """The instance endpoint address.

        stability
        :stability: experimental
        attribute:
        :attribute:: EndpointAddress
        """
        return jsii.get(self, "dbInstanceEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> str:
        """The instance endpoint port.

        stability
        :stability: experimental
        attribute:
        :attribute:: EndpointPort
        """
        return jsii.get(self, "dbInstanceEndpointPort")

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> str:
        """The instance arn.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceArn")

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> "Endpoint":
        """The instance endpoint.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceEndpoint")

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> str:
        """The instance identifier.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceIdentifier")

    @jsii.member(jsii_name="addProxy")
    def add_proxy(
        self,
        id: str,
        *,
        secrets: typing.List[_ISecret_75279d36],
        vpc: _IVpc_3795853f,
        borrow_timeout: typing.Optional[_Duration_5170c158] = None,
        db_proxy_name: typing.Optional[str] = None,
        debug_logging: typing.Optional[bool] = None,
        iam_auth: typing.Optional[bool] = None,
        idle_client_timeout: typing.Optional[_Duration_5170c158] = None,
        init_query: typing.Optional[str] = None,
        max_connections_percent: typing.Optional[jsii.Number] = None,
        max_idle_connections_percent: typing.Optional[jsii.Number] = None,
        require_tls: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        session_pinning_filters: typing.Optional[typing.List["SessionPinningFilter"]] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> "DatabaseProxy":
        """Add a new db proxy to this instance.

        :param id: -
        :param secrets: The secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster. These secrets are stored within Amazon Secrets Manager. One or more secrets are required.
        :param vpc: The VPC to associate with the new proxy.
        :param borrow_timeout: The duration for a proxy to wait for a connection to become available in the connection pool. Only applies when the proxy has opened its maximum number of connections and all connections are busy with client sessions. Value must be between 1 second and 1 hour, or ``Duration.seconds(0)`` to represent unlimited. Default: cdk.Duration.seconds(120)
        :param db_proxy_name: The identifier for the proxy. This name must be unique for all proxies owned by your AWS account in the specified AWS Region. An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two consecutive hyphens. Default: - Generated by CloudFormation (recommended)
        :param debug_logging: Whether the proxy includes detailed information about SQL statements in its logs. This information helps you to debug issues involving SQL behavior or the performance and scalability of the proxy connections. The debug information includes the text of SQL statements that you submit through the proxy. Thus, only enable this setting when needed for debugging, and only when you have security measures in place to safeguard any sensitive information that appears in the logs. Default: false
        :param iam_auth: Whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy. Default: false
        :param idle_client_timeout: The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it. You can set this value higher or lower than the connection timeout limit for the associated database. Default: cdk.Duration.minutes(30)
        :param init_query: One or more SQL statements for the proxy to run when opening each new database connection. Typically used with SET statements to make sure that each connection has identical settings such as time zone and character set. For multiple statements, use semicolons as the separator. You can also include multiple variables in a single SET statement, such as SET x=1, y=2. not currently supported for PostgreSQL. Default: - no initialization query
        :param max_connections_percent: The maximum size of the connection pool for each target in a target group. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. 1-100 Default: 100
        :param max_idle_connections_percent: Controls how actively the proxy closes idle database connections in the connection pool. A high value enables the proxy to leave a high percentage of idle connections open. A low value causes the proxy to close idle client connections and return the underlying database connections to the connection pool. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. between 0 and MaxConnectionsPercent Default: 50
        :param require_tls: A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy. By enabling this setting, you can enforce encrypted TLS connections to the proxy. Default: true
        :param role: IAM role that the proxy uses to access secrets in AWS Secrets Manager. Default: - A role will automatically be created
        :param security_groups: One or more VPC security groups to associate with the new proxy. Default: - No security groups
        :param session_pinning_filters: Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection. Including an item in the list exempts that class of SQL operations from the pinning behavior. Default: - no session pinning filters
        :param vpc_subnets: The subnets used by the proxy. Default: - the VPC default strategy if not specified.

        stability
        :stability: experimental
        """
        options = DatabaseProxyOptions(
            secrets=secrets,
            vpc=vpc,
            borrow_timeout=borrow_timeout,
            db_proxy_name=db_proxy_name,
            debug_logging=debug_logging,
            iam_auth=iam_auth,
            idle_client_timeout=idle_client_timeout,
            init_query=init_query,
            max_connections_percent=max_connections_percent,
            max_idle_connections_percent=max_idle_connections_percent,
            require_tls=require_tls,
            role=role,
            security_groups=security_groups,
            session_pinning_filters=session_pinning_filters,
            vpc_subnets=vpc_subnets,
        )

        return jsii.invoke(self, "addProxy", [id, options])

    @jsii.member(jsii_name="grantConnect")
    def grant_connect(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity connection access to the database.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantConnect", [grantee])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: str,
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
        """Return the given named metric for this DBInstance.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricCPUUtilization")
    def metric_cpu_utilization(
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
        """The percentage of CPU utilization.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricCPUUtilization", [props])

    @jsii.member(jsii_name="metricDatabaseConnections")
    def metric_database_connections(
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
        """The number of database connections in use.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricDatabaseConnections", [props])

    @jsii.member(jsii_name="metricFreeableMemory")
    def metric_freeable_memory(
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
        """The amount of available random access memory.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricFreeableMemory", [props])

    @jsii.member(jsii_name="metricFreeStorageSpace")
    def metric_free_storage_space(
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
        """The amount of available storage space.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricFreeStorageSpace", [props])

    @jsii.member(jsii_name="metricReadIOPS")
    def metric_read_iops(
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
        """The average number of disk write I/O operations per second.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricReadIOPS", [props])

    @jsii.member(jsii_name="metricWriteIOPS")
    def metric_write_iops(
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
        """The average number of disk read I/O operations per second.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricWriteIOPS", [props])

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for instance events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])


@jsii.interface(jsii_type="monocdk-experiment.aws_rds.IDatabaseProxy")
class IDatabaseProxy(_IResource_72f7ee7e, jsii.compat.Protocol):
    """DB Proxy.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IDatabaseProxyProxy

    @builtins.property
    @jsii.member(jsii_name="dbProxyArn")
    def db_proxy_arn(self) -> str:
        """DB Proxy ARN.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="dbProxyName")
    def db_proxy_name(self) -> str:
        """DB Proxy Name.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> str:
        """Endpoint.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IDatabaseProxyProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """DB Proxy.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_rds.IDatabaseProxy"

    @builtins.property
    @jsii.member(jsii_name="dbProxyArn")
    def db_proxy_arn(self) -> str:
        """DB Proxy ARN.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "dbProxyArn")

    @builtins.property
    @jsii.member(jsii_name="dbProxyName")
    def db_proxy_name(self) -> str:
        """DB Proxy Name.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "dbProxyName")

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> str:
        """Endpoint.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "endpoint")


@jsii.interface(jsii_type="monocdk-experiment.aws_rds.IEngine")
class IEngine(jsii.compat.Protocol):
    """A common interface for database engines.

    Don't implement this interface directly,
    instead implement one of the known sub-interfaces,
    like IClusterEngine and IInstanceEngine.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IEngineProxy

    @builtins.property
    @jsii.member(jsii_name="engineType")
    def engine_type(self) -> str:
        """The type of the engine, for example "mysql".

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional["EngineVersion"]:
        """The exact version of the engine that is used, for example "5.1.42".

        default
        :default: - use the default version for this engine type

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="parameterGroupFamily")
    def parameter_group_family(self) -> typing.Optional[str]:
        """The family to use for ParameterGroups using this engine.

        This is usually equal to "",
        but can sometimes be a variation of that.
        You can pass this property when creating new ParameterGroup.

        default
        :default:

        - the ParameterGroup family is not known
          (which means the major version of the engine is also not known)

        stability
        :stability: experimental
        """
        ...


class _IEngineProxy:
    """A common interface for database engines.

    Don't implement this interface directly,
    instead implement one of the known sub-interfaces,
    like IClusterEngine and IInstanceEngine.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_rds.IEngine"

    @builtins.property
    @jsii.member(jsii_name="engineType")
    def engine_type(self) -> str:
        """The type of the engine, for example "mysql".

        stability
        :stability: experimental
        """
        return jsii.get(self, "engineType")

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional["EngineVersion"]:
        """The exact version of the engine that is used, for example "5.1.42".

        default
        :default: - use the default version for this engine type

        stability
        :stability: experimental
        """
        return jsii.get(self, "engineVersion")

    @builtins.property
    @jsii.member(jsii_name="parameterGroupFamily")
    def parameter_group_family(self) -> typing.Optional[str]:
        """The family to use for ParameterGroups using this engine.

        This is usually equal to "",
        but can sometimes be a variation of that.
        You can pass this property when creating new ParameterGroup.

        default
        :default:

        - the ParameterGroup family is not known
          (which means the major version of the engine is also not known)

        stability
        :stability: experimental
        """
        return jsii.get(self, "parameterGroupFamily")


@jsii.interface(jsii_type="monocdk-experiment.aws_rds.IInstanceEngine")
class IInstanceEngine(IEngine, jsii.compat.Protocol):
    """Interface representing a database instance (as opposed to cluster) engine.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IInstanceEngineProxy

    @builtins.property
    @jsii.member(jsii_name="multiUserRotationApplication")
    def multi_user_rotation_application(self) -> _SecretRotationApplication_5d71a263:
        """The application used by this engine to perform rotation for a multi-user scenario.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="singleUserRotationApplication")
    def single_user_rotation_application(self) -> _SecretRotationApplication_5d71a263:
        """The application used by this engine to perform rotation for a single-user scenario.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="bindToInstance")
    def bind_to_instance(
        self,
        scope: _Construct_f50a3f53,
        *,
        domain: typing.Optional[str] = None,
        timezone: typing.Optional[str] = None,
    ) -> "InstanceEngineConfig":
        """Method called when the engine is used to create a new instance.

        :param scope: -
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - none (it's an optional field)
        :param timezone: The timezone of the database, set by the customer. Default: - none (it's an optional field)

        stability
        :stability: experimental
        """
        ...


class _IInstanceEngineProxy(jsii.proxy_for(IEngine)):
    """Interface representing a database instance (as opposed to cluster) engine.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_rds.IInstanceEngine"

    @builtins.property
    @jsii.member(jsii_name="multiUserRotationApplication")
    def multi_user_rotation_application(self) -> _SecretRotationApplication_5d71a263:
        """The application used by this engine to perform rotation for a multi-user scenario.

        stability
        :stability: experimental
        """
        return jsii.get(self, "multiUserRotationApplication")

    @builtins.property
    @jsii.member(jsii_name="singleUserRotationApplication")
    def single_user_rotation_application(self) -> _SecretRotationApplication_5d71a263:
        """The application used by this engine to perform rotation for a single-user scenario.

        stability
        :stability: experimental
        """
        return jsii.get(self, "singleUserRotationApplication")

    @jsii.member(jsii_name="bindToInstance")
    def bind_to_instance(
        self,
        scope: _Construct_f50a3f53,
        *,
        domain: typing.Optional[str] = None,
        timezone: typing.Optional[str] = None,
    ) -> "InstanceEngineConfig":
        """Method called when the engine is used to create a new instance.

        :param scope: -
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - none (it's an optional field)
        :param timezone: The timezone of the database, set by the customer. Default: - none (it's an optional field)

        stability
        :stability: experimental
        """
        options = InstanceEngineBindOptions(domain=domain, timezone=timezone)

        return jsii.invoke(self, "bindToInstance", [scope, options])


@jsii.interface(jsii_type="monocdk-experiment.aws_rds.IOptionGroup")
class IOptionGroup(_IResource_72f7ee7e, jsii.compat.Protocol):
    """An option group.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IOptionGroupProxy

    @builtins.property
    @jsii.member(jsii_name="optionGroupName")
    def option_group_name(self) -> str:
        """The name of the option group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        ...


class _IOptionGroupProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """An option group.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_rds.IOptionGroup"

    @builtins.property
    @jsii.member(jsii_name="optionGroupName")
    def option_group_name(self) -> str:
        """The name of the option group.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "optionGroupName")


@jsii.interface(jsii_type="monocdk-experiment.aws_rds.IParameterGroup")
class IParameterGroup(_IResource_72f7ee7e, jsii.compat.Protocol):
    """A parameter group.

    Represents both a cluster parameter group,
    and an instance parameter group.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IParameterGroupProxy

    @jsii.member(jsii_name="addParameter")
    def add_parameter(self, key: str, value: str) -> bool:
        """Adds a parameter to this group.

        If this is an imported parameter group,
        this method does nothing.

        :param key: -
        :param value: -

        return
        :return:

        true if the parameter was actually added
        (i.e., this ParameterGroup is not imported),
        false otherwise

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="bindToCluster")
    def bind_to_cluster(self) -> "ParameterGroupClusterConfig":
        """Method called when this Parameter Group is used when defining a database cluster.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="bindToInstance")
    def bind_to_instance(self) -> "ParameterGroupInstanceConfig":
        """Method called when this Parameter Group is used when defining a database instance.

        stability
        :stability: experimental
        """
        ...


class _IParameterGroupProxy(jsii.proxy_for(_IResource_72f7ee7e)):
    """A parameter group.

    Represents both a cluster parameter group,
    and an instance parameter group.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_rds.IParameterGroup"

    @jsii.member(jsii_name="addParameter")
    def add_parameter(self, key: str, value: str) -> bool:
        """Adds a parameter to this group.

        If this is an imported parameter group,
        this method does nothing.

        :param key: -
        :param value: -

        return
        :return:

        true if the parameter was actually added
        (i.e., this ParameterGroup is not imported),
        false otherwise

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addParameter", [key, value])

    @jsii.member(jsii_name="bindToCluster")
    def bind_to_cluster(self) -> "ParameterGroupClusterConfig":
        """Method called when this Parameter Group is used when defining a database cluster.

        stability
        :stability: experimental
        """
        options = ParameterGroupClusterBindOptions()

        return jsii.invoke(self, "bindToCluster", [options])

    @jsii.member(jsii_name="bindToInstance")
    def bind_to_instance(self) -> "ParameterGroupInstanceConfig":
        """Method called when this Parameter Group is used when defining a database instance.

        stability
        :stability: experimental
        """
        options = ParameterGroupInstanceBindOptions()

        return jsii.invoke(self, "bindToInstance", [options])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.InstanceEngineBindOptions",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "timezone": "timezone"},
)
class InstanceEngineBindOptions:
    def __init__(
        self,
        *,
        domain: typing.Optional[str] = None,
        timezone: typing.Optional[str] = None,
    ) -> None:
        """The options passed to {@link IInstanceEngine.bind}.

        :param domain: The Active Directory directory ID to create the DB instance in. Default: - none (it's an optional field)
        :param timezone: The timezone of the database, set by the customer. Default: - none (it's an optional field)

        stability
        :stability: experimental
        """
        self._values = {}
        if domain is not None:
            self._values["domain"] = domain
        if timezone is not None:
            self._values["timezone"] = timezone

    @builtins.property
    def domain(self) -> typing.Optional[str]:
        """The Active Directory directory ID to create the DB instance in.

        default
        :default: - none (it's an optional field)

        stability
        :stability: experimental
        """
        return self._values.get("domain")

    @builtins.property
    def timezone(self) -> typing.Optional[str]:
        """The timezone of the database, set by the customer.

        default
        :default: - none (it's an optional field)

        stability
        :stability: experimental
        """
        return self._values.get("timezone")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceEngineBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.InstanceEngineConfig",
    jsii_struct_bases=[],
    name_mapping={},
)
class InstanceEngineConfig:
    def __init__(self) -> None:
        """The type returned from the {@link IInstanceEngine.bind} method. Empty for now, but there might be fields added to it in the future.

        stability
        :stability: experimental
        """
        self._values = {}

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceEngineConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.InstanceProps",
    jsii_struct_bases=[],
    name_mapping={
        "vpc": "vpc",
        "enable_performance_insights": "enablePerformanceInsights",
        "instance_type": "instanceType",
        "parameter_group": "parameterGroup",
        "performance_insight_encryption_key": "performanceInsightEncryptionKey",
        "performance_insight_retention": "performanceInsightRetention",
        "security_groups": "securityGroups",
        "vpc_subnets": "vpcSubnets",
    },
)
class InstanceProps:
    def __init__(
        self,
        *,
        vpc: _IVpc_3795853f,
        enable_performance_insights: typing.Optional[bool] = None,
        instance_type: typing.Optional[_InstanceType_85a97b30] = None,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        performance_insight_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        performance_insight_retention: typing.Optional["PerformanceInsightRetention"] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> None:
        """Instance properties for database instances.

        :param vpc: What subnets to run the RDS instances in. Must be at least 2 subnets in two different AZs.
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        :param instance_type: What type of instance to start for the replicas. Default: - t3.medium (or, more precisely, db.t3.medium)
        :param parameter_group: The DB parameter group to associate with the instance. Default: no parameter group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7
        :param security_groups: Security group. Default: a new security group is created.
        :param vpc_subnets: Where to place the instances within the VPC. Default: - the Vpc default strategy if not specified.

        stability
        :stability: experimental
        """
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            "vpc": vpc,
        }
        if enable_performance_insights is not None:
            self._values["enable_performance_insights"] = enable_performance_insights
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if performance_insight_encryption_key is not None:
            self._values["performance_insight_encryption_key"] = performance_insight_encryption_key
        if performance_insight_retention is not None:
            self._values["performance_insight_retention"] = performance_insight_retention
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets

    @builtins.property
    def vpc(self) -> _IVpc_3795853f:
        """What subnets to run the RDS instances in.

        Must be at least 2 subnets in two different AZs.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def enable_performance_insights(self) -> typing.Optional[bool]:
        """Whether to enable Performance Insights for the DB instance.

        default
        :default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.

        stability
        :stability: experimental
        """
        return self._values.get("enable_performance_insights")

    @builtins.property
    def instance_type(self) -> typing.Optional[_InstanceType_85a97b30]:
        """What type of instance to start for the replicas.

        default
        :default: - t3.medium (or, more precisely, db.t3.medium)

        stability
        :stability: experimental
        """
        return self._values.get("instance_type")

    @builtins.property
    def parameter_group(self) -> typing.Optional["IParameterGroup"]:
        """The DB parameter group to associate with the instance.

        default
        :default: no parameter group

        stability
        :stability: experimental
        """
        return self._values.get("parameter_group")

    @builtins.property
    def performance_insight_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The AWS KMS key for encryption of Performance Insights data.

        default
        :default: - default master key

        stability
        :stability: experimental
        """
        return self._values.get("performance_insight_encryption_key")

    @builtins.property
    def performance_insight_retention(
        self,
    ) -> typing.Optional["PerformanceInsightRetention"]:
        """The amount of time, in days, to retain Performance Insights data.

        default
        :default: 7

        stability
        :stability: experimental
        """
        return self._values.get("performance_insight_retention")

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """Security group.

        default
        :default: a new security group is created.

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Where to place the instances within the VPC.

        default
        :default: - the Vpc default strategy if not specified.

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.aws_rds.LicenseModel")
class LicenseModel(enum.Enum):
    """The license model.

    stability
    :stability: experimental
    """

    LICENSE_INCLUDED = "LICENSE_INCLUDED"
    """License included.

    stability
    :stability: experimental
    """
    BRING_YOUR_OWN_LICENSE = "BRING_YOUR_OWN_LICENSE"
    """Bring your own licencse.

    stability
    :stability: experimental
    """
    GENERAL_PUBLIC_LICENSE = "GENERAL_PUBLIC_LICENSE"
    """General public license.

    stability
    :stability: experimental
    """


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.Login",
    jsii_struct_bases=[],
    name_mapping={
        "username": "username",
        "encryption_key": "encryptionKey",
        "password": "password",
    },
)
class Login:
    def __init__(
        self,
        *,
        username: str,
        encryption_key: typing.Optional[_IKey_3336c79d] = None,
        password: typing.Optional[_SecretValue_99478b8b] = None,
    ) -> None:
        """Username and password combination.

        :param username: Username.
        :param encryption_key: KMS encryption key to encrypt the generated secret. Default: default master key
        :param password: Password. Do not put passwords in your CDK code directly. Default: a Secrets Manager generated password

        stability
        :stability: experimental
        """
        self._values = {
            "username": username,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def username(self) -> str:
        """Username.

        stability
        :stability: experimental
        """
        return self._values.get("username")

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """KMS encryption key to encrypt the generated secret.

        default
        :default: default master key

        stability
        :stability: experimental
        """
        return self._values.get("encryption_key")

    @builtins.property
    def password(self) -> typing.Optional[_SecretValue_99478b8b]:
        """Password.

        Do not put passwords in your CDK code directly.

        default
        :default: a Secrets Manager generated password

        stability
        :stability: experimental
        """
        return self._values.get("password")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Login(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MariaDbEngineVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.MariaDbEngineVersion",
):
    """The versions for the MariaDB instance engines (those returned by {@link DatabaseInstanceEngine.mariaDb}).

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls, maria_db_full_version: str, maria_db_major_version: str
    ) -> "MariaDbEngineVersion":
        """Create a new MariaDbEngineVersion with an arbitrary version.

        :param maria_db_full_version: the full version string, for example "10.5.28".
        :param maria_db_major_version: the major version of the engine, for example "10.5".

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [maria_db_full_version, maria_db_major_version])

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_0")
    def VER_10_0(cls) -> "MariaDbEngineVersion":
        """Version "10.0" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_0_17")
    def VER_10_0_17(cls) -> "MariaDbEngineVersion":
        """Version "10.0.17".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_0_17")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_0_24")
    def VER_10_0_24(cls) -> "MariaDbEngineVersion":
        """Version "10.0.24".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_0_24")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_0_28")
    def VER_10_0_28(cls) -> "MariaDbEngineVersion":
        """Version "10.0.28".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_0_28")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_0_31")
    def VER_10_0_31(cls) -> "MariaDbEngineVersion":
        """Version "10.0.31".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_0_31")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_0_32")
    def VER_10_0_32(cls) -> "MariaDbEngineVersion":
        """Version "10.0.32".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_0_32")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_0_34")
    def VER_10_0_34(cls) -> "MariaDbEngineVersion":
        """Version "10.0.34".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_0_34")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_0_35")
    def VER_10_0_35(cls) -> "MariaDbEngineVersion":
        """Version "10.0.35".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_0_35")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_1")
    def VER_10_1(cls) -> "MariaDbEngineVersion":
        """Version "10.1" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_1_14")
    def VER_10_1_14(cls) -> "MariaDbEngineVersion":
        """Version "10.1.14".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_1_14")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_1_19")
    def VER_10_1_19(cls) -> "MariaDbEngineVersion":
        """Version "10.1.19".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_1_19")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_1_23")
    def VER_10_1_23(cls) -> "MariaDbEngineVersion":
        """Version "10.1.23".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_1_23")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_1_26")
    def VER_10_1_26(cls) -> "MariaDbEngineVersion":
        """Version "10.1.26".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_1_26")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_1_31")
    def VER_10_1_31(cls) -> "MariaDbEngineVersion":
        """Version "10.1.31".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_1_31")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_1_34")
    def VER_10_1_34(cls) -> "MariaDbEngineVersion":
        """Version "10.1.34".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_1_34")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_2")
    def VER_10_2(cls) -> "MariaDbEngineVersion":
        """Version "10.2" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_2_11")
    def VER_10_2_11(cls) -> "MariaDbEngineVersion":
        """Version "10.2.11".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_2_11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_2_12")
    def VER_10_2_12(cls) -> "MariaDbEngineVersion":
        """Version "10.2.12".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_2_12")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_2_15")
    def VER_10_2_15(cls) -> "MariaDbEngineVersion":
        """Version "10.2.15".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_2_15")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_2_21")
    def VER_10_2_21(cls) -> "MariaDbEngineVersion":
        """Version "10.2.21".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_2_21")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_3")
    def VER_10_3(cls) -> "MariaDbEngineVersion":
        """Version "10.3" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_3")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_3_13")
    def VER_10_3_13(cls) -> "MariaDbEngineVersion":
        """Version "10.3.13".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_3_13")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_3_20")
    def VER_10_3_20(cls) -> "MariaDbEngineVersion":
        """Version "10.3.20".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_3_20")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_3_23")
    def VER_10_3_23(cls) -> "MariaDbEngineVersion":
        """Version "10.3.23".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_3_23")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_3_8")
    def VER_10_3_8(cls) -> "MariaDbEngineVersion":
        """Version "10.3.8".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_3_8")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_4")
    def VER_10_4(cls) -> "MariaDbEngineVersion":
        """Version "10.4" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_4")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_4_13")
    def VER_10_4_13(cls) -> "MariaDbEngineVersion":
        """Version "10.4.13".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_4_13")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_4_8")
    def VER_10_4_8(cls) -> "MariaDbEngineVersion":
        """Version "10.4.8".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_4_8")

    @builtins.property
    @jsii.member(jsii_name="mariaDbFullVersion")
    def maria_db_full_version(self) -> str:
        """The full version string, for example, "10.5.28".

        stability
        :stability: experimental
        """
        return jsii.get(self, "mariaDbFullVersion")

    @builtins.property
    @jsii.member(jsii_name="mariaDbMajorVersion")
    def maria_db_major_version(self) -> str:
        """The major version of the engine, for example, "10.5".

        stability
        :stability: experimental
        """
        return jsii.get(self, "mariaDbMajorVersion")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.MariaDbInstanceEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class MariaDbInstanceEngineProps:
    def __init__(self, *, version: "MariaDbEngineVersion") -> None:
        """Properties for MariaDB instance engines.

        Used in {@link DatabaseInstanceEngine.mariaDb}.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "MariaDbEngineVersion":
        """The exact version of the engine to use.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MariaDbInstanceEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.MySqlInstanceEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class MySqlInstanceEngineProps:
    def __init__(self, *, version: "MysqlEngineVersion") -> None:
        """Properties for MySQL instance engines.

        Used in {@link DatabaseInstanceEngine.mysql}.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "MysqlEngineVersion":
        """The exact version of the engine to use.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MySqlInstanceEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MysqlEngineVersion(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_rds.MysqlEngineVersion"
):
    """The versions for the MySQL instance engines (those returned by {@link DatabaseInstanceEngine.mysql}).

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls, mysql_full_version: str, mysql_major_version: str
    ) -> "MysqlEngineVersion":
        """Create a new MysqlEngineVersion with an arbitrary version.

        :param mysql_full_version: the full version string, for example "8.1.43".
        :param mysql_major_version: the major version of the engine, for example "8.1".

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [mysql_full_version, mysql_major_version])

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_5")
    def VER_5_5(cls) -> "MysqlEngineVersion":
        """Version "5.5" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_5_46")
    def VER_5_5_46(cls) -> "MysqlEngineVersion":
        """Version "5.5.46".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_5_46")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_5_53")
    def VER_5_5_53(cls) -> "MysqlEngineVersion":
        """Version "5.5.53".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_5_53")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_5_57")
    def VER_5_5_57(cls) -> "MysqlEngineVersion":
        """Version "5.5.57".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_5_57")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_5_59")
    def VER_5_5_59(cls) -> "MysqlEngineVersion":
        """Version "5.5.59".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_5_59")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_5_61")
    def VER_5_5_61(cls) -> "MysqlEngineVersion":
        """Version "5.5.61".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_5_61")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_6")
    def VER_5_6(cls) -> "MysqlEngineVersion":
        """Version "5.6" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_6_34")
    def VER_5_6_34(cls) -> "MysqlEngineVersion":
        """Version "5.6.34".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_6_34")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_6_35")
    def VER_5_6_35(cls) -> "MysqlEngineVersion":
        """Version "5.6.35".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_6_35")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_6_37")
    def VER_5_6_37(cls) -> "MysqlEngineVersion":
        """Version "5.6.37".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_6_37")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_6_39")
    def VER_5_6_39(cls) -> "MysqlEngineVersion":
        """Version "5.6.39".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_6_39")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_6_40")
    def VER_5_6_40(cls) -> "MysqlEngineVersion":
        """Version "5.6.40".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_6_40")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_6_41")
    def VER_5_6_41(cls) -> "MysqlEngineVersion":
        """Version "5.6.41".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_6_41")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_6_43")
    def VER_5_6_43(cls) -> "MysqlEngineVersion":
        """Version "5.6.43".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_6_43")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_6_44")
    def VER_5_6_44(cls) -> "MysqlEngineVersion":
        """Version "5.6.44".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_6_44")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_6_46")
    def VER_5_6_46(cls) -> "MysqlEngineVersion":
        """Version "5.6.46".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_6_46")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_6_48")
    def VER_5_6_48(cls) -> "MysqlEngineVersion":
        """Version "5.6.48".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_6_48")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7")
    def VER_5_7(cls) -> "MysqlEngineVersion":
        """Version "5.7" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7_16")
    def VER_5_7_16(cls) -> "MysqlEngineVersion":
        """Version "5.7.16".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7_16")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7_17")
    def VER_5_7_17(cls) -> "MysqlEngineVersion":
        """Version "5.7.17".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7_17")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7_19")
    def VER_5_7_19(cls) -> "MysqlEngineVersion":
        """Version "5.7.19".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7_19")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7_21")
    def VER_5_7_21(cls) -> "MysqlEngineVersion":
        """Version "5.7.21".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7_21")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7_22")
    def VER_5_7_22(cls) -> "MysqlEngineVersion":
        """Version "5.7.22".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7_22")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7_23")
    def VER_5_7_23(cls) -> "MysqlEngineVersion":
        """Version "5.7.23".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7_23")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7_24")
    def VER_5_7_24(cls) -> "MysqlEngineVersion":
        """Version "5.7.24".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7_24")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7_25")
    def VER_5_7_25(cls) -> "MysqlEngineVersion":
        """Version "5.7.25".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7_25")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7_26")
    def VER_5_7_26(cls) -> "MysqlEngineVersion":
        """Version "5.7.26".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7_26")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7_28")
    def VER_5_7_28(cls) -> "MysqlEngineVersion":
        """Version "5.7.28".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7_28")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_5_7_30")
    def VER_5_7_30(cls) -> "MysqlEngineVersion":
        """Version "5.7.30".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_5_7_30")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_8_0")
    def VER_8_0(cls) -> "MysqlEngineVersion":
        """Version "8.0" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_8_0")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_8_0_11")
    def VER_8_0_11(cls) -> "MysqlEngineVersion":
        """Version "8.0.11".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_8_0_11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_8_0_13")
    def VER_8_0_13(cls) -> "MysqlEngineVersion":
        """Version "8.0.13".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_8_0_13")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_8_0_15")
    def VER_8_0_15(cls) -> "MysqlEngineVersion":
        """Version "8.0.15".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_8_0_15")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_8_0_16")
    def VER_8_0_16(cls) -> "MysqlEngineVersion":
        """Version "8.0.16".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_8_0_16")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_8_0_17")
    def VER_8_0_17(cls) -> "MysqlEngineVersion":
        """Version "8.0.17".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_8_0_17")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_8_0_19")
    def VER_8_0_19(cls) -> "MysqlEngineVersion":
        """Version "8.0.19".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_8_0_19")

    @builtins.property
    @jsii.member(jsii_name="mysqlFullVersion")
    def mysql_full_version(self) -> str:
        """The full version string, for example, "10.5.28".

        stability
        :stability: experimental
        """
        return jsii.get(self, "mysqlFullVersion")

    @builtins.property
    @jsii.member(jsii_name="mysqlMajorVersion")
    def mysql_major_version(self) -> str:
        """The major version of the engine, for example, "10.5".

        stability
        :stability: experimental
        """
        return jsii.get(self, "mysqlMajorVersion")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.OptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "port": "port",
        "security_groups": "securityGroups",
        "settings": "settings",
        "version": "version",
        "vpc": "vpc",
    },
)
class OptionConfiguration:
    def __init__(
        self,
        *,
        name: str,
        port: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        settings: typing.Optional[typing.Mapping[str, str]] = None,
        version: typing.Optional[str] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
    ) -> None:
        """Configuration properties for an option.

        :param name: The name of the option.
        :param port: The port number that this option uses. If ``port`` is specified then ``vpc`` must also be specified. Default: - no port
        :param security_groups: Optional list of security groups to use for this option, if ``vpc`` is specified. If no groups are provided, a default one will be created. Default: - a default group will be created if ``port`` or ``vpc`` are specified.
        :param settings: The settings for the option. Default: - no settings
        :param version: The version for the option. Default: - no version
        :param vpc: The VPC where a security group should be created for this option. If ``vpc`` is specified then ``port`` must also be specified. Default: - no VPC

        stability
        :stability: experimental
        """
        self._values = {
            "name": name,
        }
        if port is not None:
            self._values["port"] = port
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if settings is not None:
            self._values["settings"] = settings
        if version is not None:
            self._values["version"] = version
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def name(self) -> str:
        """The name of the option.

        stability
        :stability: experimental
        """
        return self._values.get("name")

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port number that this option uses.

        If ``port`` is specified then ``vpc``
        must also be specified.

        default
        :default: - no port

        stability
        :stability: experimental
        """
        return self._values.get("port")

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """Optional list of security groups to use for this option, if ``vpc`` is specified.

        If no groups are provided, a default one will be created.

        default
        :default: - a default group will be created if ``port`` or ``vpc`` are specified.

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    @builtins.property
    def settings(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The settings for the option.

        default
        :default: - no settings

        stability
        :stability: experimental
        """
        return self._values.get("settings")

    @builtins.property
    def version(self) -> typing.Optional[str]:
        """The version for the option.

        default
        :default: - no version

        stability
        :stability: experimental
        """
        return self._values.get("version")

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """The VPC where a security group should be created for this option.

        If ``vpc``
        is specified then ``port`` must also be specified.

        default
        :default: - no VPC

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IOptionGroup)
class OptionGroup(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.OptionGroup",
):
    """An option group.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        configurations: typing.List["OptionConfiguration"],
        engine: "IInstanceEngine",
        description: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param configurations: The configurations for this option group.
        :param engine: The database engine that this option group is associated with.
        :param description: A description of the option group. Default: a CDK generated description

        stability
        :stability: experimental
        """
        props = OptionGroupProps(
            configurations=configurations, engine=engine, description=description
        )

        jsii.create(OptionGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromOptionGroupName")
    @builtins.classmethod
    def from_option_group_name(
        cls, scope: _Construct_f50a3f53, id: str, option_group_name: str
    ) -> "IOptionGroup":
        """Import an existing option group.

        :param scope: -
        :param id: -
        :param option_group_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromOptionGroupName", [scope, id, option_group_name])

    @builtins.property
    @jsii.member(jsii_name="optionConnections")
    def option_connections(self) -> typing.Mapping[str, _Connections_231f38b5]:
        """The connections object for the options.

        stability
        :stability: experimental
        """
        return jsii.get(self, "optionConnections")

    @builtins.property
    @jsii.member(jsii_name="optionGroupName")
    def option_group_name(self) -> str:
        """The name of the option group.

        stability
        :stability: experimental
        """
        return jsii.get(self, "optionGroupName")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.OptionGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "configurations": "configurations",
        "engine": "engine",
        "description": "description",
    },
)
class OptionGroupProps:
    def __init__(
        self,
        *,
        configurations: typing.List["OptionConfiguration"],
        engine: "IInstanceEngine",
        description: typing.Optional[str] = None,
    ) -> None:
        """Construction properties for an OptionGroup.

        :param configurations: The configurations for this option group.
        :param engine: The database engine that this option group is associated with.
        :param description: A description of the option group. Default: a CDK generated description

        stability
        :stability: experimental
        """
        self._values = {
            "configurations": configurations,
            "engine": engine,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def configurations(self) -> typing.List["OptionConfiguration"]:
        """The configurations for this option group.

        stability
        :stability: experimental
        """
        return self._values.get("configurations")

    @builtins.property
    def engine(self) -> "IInstanceEngine":
        """The database engine that this option group is associated with.

        stability
        :stability: experimental
        """
        return self._values.get("engine")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the option group.

        default
        :default: a CDK generated description

        stability
        :stability: experimental
        """
        return self._values.get("description")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OptionGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.OracleEeInstanceEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class OracleEeInstanceEngineProps:
    def __init__(self, *, version: "OracleEngineVersion") -> None:
        """Properties for Oracle Enterprise Edition instance engines.

        Used in {@link DatabaseInstanceEngine.oracleEe}.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "OracleEngineVersion":
        """The exact version of the engine to use.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleEeInstanceEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OracleEngineVersion(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_rds.OracleEngineVersion"
):
    """The versions for the Oracle instance engines (those returned by {@link DatabaseInstanceEngine.oracleSe2} and {@link DatabaseInstanceEngine.oracleEe}).

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls, oracle_full_version: str, oracle_major_version: str
    ) -> "OracleEngineVersion":
        """Creates a new OracleEngineVersion with an arbitrary version.

        :param oracle_full_version: the full version string, for example "19.0.0.0.ru-2019-10.rur-2019-10.r1".
        :param oracle_major_version: the major version of the engine, for example "19".

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [oracle_full_version, oracle_major_version])

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1")
    def VER_12_1(cls) -> "OracleEngineVersion":
        """Version "12.1" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V1")
    def VER_12_1_0_2_V1(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V10")
    def VER_12_1_0_2_V10(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v10".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V10")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V11")
    def VER_12_1_0_2_V11(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v11".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V12")
    def VER_12_1_0_2_V12(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v12".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V12")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V13")
    def VER_12_1_0_2_V13(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v13".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V13")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V14")
    def VER_12_1_0_2_V14(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v14".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V14")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V15")
    def VER_12_1_0_2_V15(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v15".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V15")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V16")
    def VER_12_1_0_2_V16(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v16".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V16")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V17")
    def VER_12_1_0_2_V17(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v17".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V17")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V18")
    def VER_12_1_0_2_V18(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v18".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V18")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V19")
    def VER_12_1_0_2_V19(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v19".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V19")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V2")
    def VER_12_1_0_2_V2(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v2".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V20")
    def VER_12_1_0_2_V20(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v20".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V20")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V3")
    def VER_12_1_0_2_V3(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v3".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V3")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V4")
    def VER_12_1_0_2_V4(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v4".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V4")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V5")
    def VER_12_1_0_2_V5(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v5".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V6")
    def VER_12_1_0_2_V6(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v6".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V7")
    def VER_12_1_0_2_V7(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v7".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V7")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V8")
    def VER_12_1_0_2_V8(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v8".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V8")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_1_0_2_V9")
    def VER_12_1_0_2_V9(cls) -> "OracleEngineVersion":
        """Version "12.1.0.2.v9".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_1_0_2_V9")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_2")
    def VER_12_2(cls) -> "OracleEngineVersion":
        """Version "12.2" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_2_0_1_2018_10_R1")
    def VER_12_2_0_1_2018_10_R1(cls) -> "OracleEngineVersion":
        """Version "12.2.0.1.ru-2018-10.rur-2018-10.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_2_0_1_2018_10_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_2_0_1_2019_01_R1")
    def VER_12_2_0_1_2019_01_R1(cls) -> "OracleEngineVersion":
        """Version "12.2.0.1.ru-2019-01.rur-2019-01.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_2_0_1_2019_01_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_2_0_1_2019_04_R1")
    def VER_12_2_0_1_2019_04_R1(cls) -> "OracleEngineVersion":
        """Version "12.2.0.1.ru-2019-04.rur-2019-04.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_2_0_1_2019_04_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_2_0_1_2019_07_R1")
    def VER_12_2_0_1_2019_07_R1(cls) -> "OracleEngineVersion":
        """Version "12.2.0.1.ru-2019-07.rur-2019-07.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_2_0_1_2019_07_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_2_0_1_2019_10_R1")
    def VER_12_2_0_1_2019_10_R1(cls) -> "OracleEngineVersion":
        """Version "12.2.0.1.ru-2019-10.rur-2019-10.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_2_0_1_2019_10_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_2_0_1_2020_01_R1")
    def VER_12_2_0_1_2020_01_R1(cls) -> "OracleEngineVersion":
        """Version "12.2.0.1.ru-2020-01.rur-2020-01.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_2_0_1_2020_01_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_2_0_1_2020_04_R1")
    def VER_12_2_0_1_2020_04_R1(cls) -> "OracleEngineVersion":
        """Version "12.2.0.1.ru-2020-04.rur-2020-04.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_2_0_1_2020_04_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_18")
    def VER_18(cls) -> "OracleEngineVersion":
        """Version "18" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_18")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_18_0_0_0_2019_07_R1")
    def VER_18_0_0_0_2019_07_R1(cls) -> "OracleEngineVersion":
        """Version "18.0.0.0.ru-2019-07.rur-2019-07.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_18_0_0_0_2019_07_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_18_0_0_0_2019_10_R1")
    def VER_18_0_0_0_2019_10_R1(cls) -> "OracleEngineVersion":
        """Version "18.0.0.0.ru-2019-10.rur-2019-10.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_18_0_0_0_2019_10_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_18_0_0_0_2020_01_R1")
    def VER_18_0_0_0_2020_01_R1(cls) -> "OracleEngineVersion":
        """Version "18.0.0.0.ru-2020-01.rur-2020-01.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_18_0_0_0_2020_01_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_18_0_0_0_2020_04_R1")
    def VER_18_0_0_0_2020_04_R1(cls) -> "OracleEngineVersion":
        """Version "18.0.0.0.ru-2020-04.rur-2020-04.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_18_0_0_0_2020_04_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_19")
    def VER_19(cls) -> "OracleEngineVersion":
        """Version "19" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_19")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_19_0_0_0_2019_07_R1")
    def VER_19_0_0_0_2019_07_R1(cls) -> "OracleEngineVersion":
        """Version "19.0.0.0.ru-2019-07.rur-2019-07.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_19_0_0_0_2019_07_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_19_0_0_0_2019_10_R1")
    def VER_19_0_0_0_2019_10_R1(cls) -> "OracleEngineVersion":
        """Version "19.0.0.0.ru-2019-10.rur-2019-10.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_19_0_0_0_2019_10_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_19_0_0_0_2020_01_R1")
    def VER_19_0_0_0_2020_01_R1(cls) -> "OracleEngineVersion":
        """Version "19.0.0.0.ru-2020-01.rur-2020-01.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_19_0_0_0_2020_01_R1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_19_0_0_0_2020_04_R1")
    def VER_19_0_0_0_2020_04_R1(cls) -> "OracleEngineVersion":
        """Version "19.0.0.0.ru-2020-04.rur-2020-04.r1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_19_0_0_0_2020_04_R1")

    @builtins.property
    @jsii.member(jsii_name="oracleFullVersion")
    def oracle_full_version(self) -> str:
        """The full version string, for example, "19.0.0.0.ru-2019-10.rur-2019-10.r1".

        stability
        :stability: experimental
        """
        return jsii.get(self, "oracleFullVersion")

    @builtins.property
    @jsii.member(jsii_name="oracleMajorVersion")
    def oracle_major_version(self) -> str:
        """The major version of the engine, for example, "19".

        stability
        :stability: experimental
        """
        return jsii.get(self, "oracleMajorVersion")


class OracleLegacyEngineVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.OracleLegacyEngineVersion",
):
    """The versions for the legacy Oracle instance engines (those returned by {@link DatabaseInstanceEngine.oracleSe} and {@link DatabaseInstanceEngine.oracleSe1}). Note: RDS will stop allowing creating new databases with this version in August 2020.

    stability
    :stability: experimental
    """

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2")
    def VER_11_2(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_2_V2")
    def VER_11_2_0_2_V2(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.2.v2".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_2_V2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V1")
    def VER_11_2_0_4_V1(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V10")
    def VER_11_2_0_4_V10(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v10".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V10")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V11")
    def VER_11_2_0_4_V11(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v11".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V12")
    def VER_11_2_0_4_V12(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v12".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V12")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V13")
    def VER_11_2_0_4_V13(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v13".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V13")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V14")
    def VER_11_2_0_4_V14(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v14".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V14")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V15")
    def VER_11_2_0_4_V15(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v15".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V15")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V16")
    def VER_11_2_0_4_V16(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v16".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V16")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V17")
    def VER_11_2_0_4_V17(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v17".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V17")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V18")
    def VER_11_2_0_4_V18(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v18".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V18")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V19")
    def VER_11_2_0_4_V19(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v19".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V19")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V20")
    def VER_11_2_0_4_V20(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v20".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V20")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V21")
    def VER_11_2_0_4_V21(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v21".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V21")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V22")
    def VER_11_2_0_4_V22(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v22".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V22")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V23")
    def VER_11_2_0_4_V23(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v23".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V23")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V24")
    def VER_11_2_0_4_V24(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v24".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V24")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V3")
    def VER_11_2_0_4_V3(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v3".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V3")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V4")
    def VER_11_2_0_4_V4(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v4".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V4")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V5")
    def VER_11_2_0_4_V5(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v5".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V6")
    def VER_11_2_0_4_V6(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v6".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V7")
    def VER_11_2_0_4_V7(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v7".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V7")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V8")
    def VER_11_2_0_4_V8(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v8".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V8")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2_0_4_V9")
    def VER_11_2_0_4_V9(cls) -> "OracleLegacyEngineVersion":
        """Version "11.2.0.4.v9".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2_0_4_V9")

    @builtins.property
    @jsii.member(jsii_name="oracleLegacyFullVersion")
    def oracle_legacy_full_version(self) -> str:
        """The full version string, for example, "11.2.0.4.v24".

        stability
        :stability: experimental
        """
        return jsii.get(self, "oracleLegacyFullVersion")

    @builtins.property
    @jsii.member(jsii_name="oracleLegacyMajorVersion")
    def oracle_legacy_major_version(self) -> str:
        """The major version of the engine, for example, "11.2".

        stability
        :stability: experimental
        """
        return jsii.get(self, "oracleLegacyMajorVersion")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.OracleSe1InstanceEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class OracleSe1InstanceEngineProps:
    def __init__(self, *, version: "OracleLegacyEngineVersion") -> None:
        """Properties for Oracle Standard Edition 1 instance engines.

        Used in {@link DatabaseInstanceEngine.oracleSe1}.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "OracleLegacyEngineVersion":
        """The exact version of the engine to use.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleSe1InstanceEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.OracleSe2InstanceEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class OracleSe2InstanceEngineProps:
    def __init__(self, *, version: "OracleEngineVersion") -> None:
        """Properties for Oracle Standard Edition 2 instance engines.

        Used in {@link DatabaseInstanceEngine.oracleSe2}.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "OracleEngineVersion":
        """The exact version of the engine to use.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleSe2InstanceEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.OracleSeInstanceEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class OracleSeInstanceEngineProps:
    def __init__(self, *, version: "OracleLegacyEngineVersion") -> None:
        """Properties for Oracle Standard Edition instance engines.

        Used in {@link DatabaseInstanceEngine.oracleSe}.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "OracleLegacyEngineVersion":
        """The exact version of the engine to use.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OracleSeInstanceEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IParameterGroup)
class ParameterGroup(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.ParameterGroup",
):
    """A parameter group.

    Represents both a cluster parameter group,
    and an instance parameter group.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::RDS::DBParameterGroup
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        engine: "IEngine",
        description: typing.Optional[str] = None,
        parameters: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param engine: The database engine for this parameter group.
        :param description: Description for this parameter group. Default: a CDK generated description
        :param parameters: The parameters in this parameter group. Default: - None

        stability
        :stability: experimental
        """
        props = ParameterGroupProps(
            engine=engine, description=description, parameters=parameters
        )

        jsii.create(ParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromParameterGroupName")
    @builtins.classmethod
    def from_parameter_group_name(
        cls, scope: _Construct_f50a3f53, id: str, parameter_group_name: str
    ) -> "IParameterGroup":
        """Imports a parameter group.

        :param scope: -
        :param id: -
        :param parameter_group_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromParameterGroupName", [scope, id, parameter_group_name])

    @jsii.member(jsii_name="addParameter")
    def add_parameter(self, key: str, value: str) -> bool:
        """Add a parameter to this parameter group.

        :param key: The key of the parameter to be added.
        :param value: The value of the parameter to be added.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addParameter", [key, value])

    @jsii.member(jsii_name="bindToCluster")
    def bind_to_cluster(self) -> "ParameterGroupClusterConfig":
        """Method called when this Parameter Group is used when defining a database cluster.

        stability
        :stability: experimental
        """
        _options = ParameterGroupClusterBindOptions()

        return jsii.invoke(self, "bindToCluster", [_options])

    @jsii.member(jsii_name="bindToInstance")
    def bind_to_instance(self) -> "ParameterGroupInstanceConfig":
        """Method called when this Parameter Group is used when defining a database instance.

        stability
        :stability: experimental
        """
        _options = ParameterGroupInstanceBindOptions()

        return jsii.invoke(self, "bindToInstance", [_options])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.ParameterGroupClusterBindOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class ParameterGroupClusterBindOptions:
    def __init__(self) -> None:
        """Options for {@link IParameterGroup.bindToCluster}. Empty for now, but can be extended later.

        stability
        :stability: experimental
        """
        self._values = {}

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParameterGroupClusterBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.ParameterGroupClusterConfig",
    jsii_struct_bases=[],
    name_mapping={"parameter_group_name": "parameterGroupName"},
)
class ParameterGroupClusterConfig:
    def __init__(self, *, parameter_group_name: str) -> None:
        """The type returned from {@link IParameterGroup.bindToCluster}.

        :param parameter_group_name: The name of this parameter group.

        stability
        :stability: experimental
        """
        self._values = {
            "parameter_group_name": parameter_group_name,
        }

    @builtins.property
    def parameter_group_name(self) -> str:
        """The name of this parameter group.

        stability
        :stability: experimental
        """
        return self._values.get("parameter_group_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParameterGroupClusterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.ParameterGroupInstanceBindOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class ParameterGroupInstanceBindOptions:
    def __init__(self) -> None:
        """Options for {@link IParameterGroup.bindToInstance}. Empty for now, but can be extended later.

        stability
        :stability: experimental
        """
        self._values = {}

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParameterGroupInstanceBindOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.ParameterGroupInstanceConfig",
    jsii_struct_bases=[],
    name_mapping={"parameter_group_name": "parameterGroupName"},
)
class ParameterGroupInstanceConfig:
    def __init__(self, *, parameter_group_name: str) -> None:
        """The type returned from {@link IParameterGroup.bindToInstance}.

        :param parameter_group_name: The name of this parameter group.

        stability
        :stability: experimental
        """
        self._values = {
            "parameter_group_name": parameter_group_name,
        }

    @builtins.property
    def parameter_group_name(self) -> str:
        """The name of this parameter group.

        stability
        :stability: experimental
        """
        return self._values.get("parameter_group_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParameterGroupInstanceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.ParameterGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "engine": "engine",
        "description": "description",
        "parameters": "parameters",
    },
)
class ParameterGroupProps:
    def __init__(
        self,
        *,
        engine: "IEngine",
        description: typing.Optional[str] = None,
        parameters: typing.Optional[typing.Mapping[str, str]] = None,
    ) -> None:
        """Properties for a parameter group.

        :param engine: The database engine for this parameter group.
        :param description: Description for this parameter group. Default: a CDK generated description
        :param parameters: The parameters in this parameter group. Default: - None

        stability
        :stability: experimental
        """
        self._values = {
            "engine": engine,
        }
        if description is not None:
            self._values["description"] = description
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def engine(self) -> "IEngine":
        """The database engine for this parameter group.

        stability
        :stability: experimental
        """
        return self._values.get("engine")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """Description for this parameter group.

        default
        :default: a CDK generated description

        stability
        :stability: experimental
        """
        return self._values.get("description")

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, str]]:
        """The parameters in this parameter group.

        default
        :default: - None

        stability
        :stability: experimental
        """
        return self._values.get("parameters")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParameterGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.aws_rds.PerformanceInsightRetention")
class PerformanceInsightRetention(enum.Enum):
    """The retention period for Performance Insight.

    stability
    :stability: experimental
    """

    DEFAULT = "DEFAULT"
    """Default retention period of 7 days.

    stability
    :stability: experimental
    """
    LONG_TERM = "LONG_TERM"
    """Long term retention period of 2 years.

    stability
    :stability: experimental
    """


class PostgresEngineVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.PostgresEngineVersion",
):
    """The versions for the PostgreSQL instance engines (those returned by {@link DatabaseInstanceEngine.postgres}).

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls, postgres_full_version: str, postgres_major_version: str
    ) -> "PostgresEngineVersion":
        """Create a new PostgresEngineVersion with an arbitrary version.

        :param postgres_full_version: the full version string, for example "13.11".
        :param postgres_major_version: the major version of the engine, for example "13".

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [postgres_full_version, postgres_major_version])

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10")
    def VER_10(cls) -> "PostgresEngineVersion":
        """Version "10" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_1")
    def VER_10_1(cls) -> "PostgresEngineVersion":
        """Version "10.1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_10")
    def VER_10_10(cls) -> "PostgresEngineVersion":
        """Version "10.10".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_10")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_11")
    def VER_10_11(cls) -> "PostgresEngineVersion":
        """Version "10.11".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_12")
    def VER_10_12(cls) -> "PostgresEngineVersion":
        """Version "10.12".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_12")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_13")
    def VER_10_13(cls) -> "PostgresEngineVersion":
        """Version "10.13".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_13")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_3")
    def VER_10_3(cls) -> "PostgresEngineVersion":
        """Version "10.3".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_3")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_4")
    def VER_10_4(cls) -> "PostgresEngineVersion":
        """Version "10.4".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_4")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_5")
    def VER_10_5(cls) -> "PostgresEngineVersion":
        """Version "10.5".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_6")
    def VER_10_6(cls) -> "PostgresEngineVersion":
        """Version "10.6".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_7")
    def VER_10_7(cls) -> "PostgresEngineVersion":
        """Version "10.7".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_7")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_10_9")
    def VER_10_9(cls) -> "PostgresEngineVersion":
        """Version "10.9".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_10_9")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11")
    def VER_11(cls) -> "PostgresEngineVersion":
        """Version "11" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_1")
    def VER_11_1(cls) -> "PostgresEngineVersion":
        """Version "11.1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_2")
    def VER_11_2(cls) -> "PostgresEngineVersion":
        """Version "11.2".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_4")
    def VER_11_4(cls) -> "PostgresEngineVersion":
        """Version "11.4".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_4")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_5")
    def VER_11_5(cls) -> "PostgresEngineVersion":
        """Version "11.5".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_6")
    def VER_11_6(cls) -> "PostgresEngineVersion":
        """Version "11.6".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_7")
    def VER_11_7(cls) -> "PostgresEngineVersion":
        """Version "11.7".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_7")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_8")
    def VER_11_8(cls) -> "PostgresEngineVersion":
        """Version "11.8".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_8")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12")
    def VER_12(cls) -> "PostgresEngineVersion":
        """Version "12" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_2")
    def VER_12_2(cls) -> "PostgresEngineVersion":
        """Version "12.2".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_3")
    def VER_12_3(cls) -> "PostgresEngineVersion":
        """Version "12.3".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_3")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5")
    def VER_9_5(cls) -> "PostgresEngineVersion":
        """Version "9.5" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_10")
    def VER_9_5_10(cls) -> "PostgresEngineVersion":
        """Version "9.5.10".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_10")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_12")
    def VER_9_5_12(cls) -> "PostgresEngineVersion":
        """Version "9.5.12".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_12")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_13")
    def VER_9_5_13(cls) -> "PostgresEngineVersion":
        """Version "9.5.13".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_13")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_14")
    def VER_9_5_14(cls) -> "PostgresEngineVersion":
        """Version "9.5.14".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_14")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_15")
    def VER_9_5_15(cls) -> "PostgresEngineVersion":
        """Version "9.5.15".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_15")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_16")
    def VER_9_5_16(cls) -> "PostgresEngineVersion":
        """Version "9.5.16".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_16")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_18")
    def VER_9_5_18(cls) -> "PostgresEngineVersion":
        """Version "9.5.18".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_18")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_19")
    def VER_9_5_19(cls) -> "PostgresEngineVersion":
        """Version "9.5.19".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_19")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_2")
    def VER_9_5_2(cls) -> "PostgresEngineVersion":
        """Version "9.5.2".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_20")
    def VER_9_5_20(cls) -> "PostgresEngineVersion":
        """Version "9.5.20".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_20")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_21")
    def VER_9_5_21(cls) -> "PostgresEngineVersion":
        """Version "9.5.21".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_21")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_22")
    def VER_9_5_22(cls) -> "PostgresEngineVersion":
        """Version "9.5.22".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_22")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_4")
    def VER_9_5_4(cls) -> "PostgresEngineVersion":
        """Version "9.5.4".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_4")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_6")
    def VER_9_5_6(cls) -> "PostgresEngineVersion":
        """Version "9.5.6".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_7")
    def VER_9_5_7(cls) -> "PostgresEngineVersion":
        """Version "9.5.7".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_7")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_5_9")
    def VER_9_5_9(cls) -> "PostgresEngineVersion":
        """Version "9.5.9".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_5_9")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6")
    def VER_9_6(cls) -> "PostgresEngineVersion":
        """Version "9.6" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_1")
    def VER_9_6_1(cls) -> "PostgresEngineVersion":
        """Version "9.6.1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_10")
    def VER_9_6_10(cls) -> "PostgresEngineVersion":
        """Version "9.6.10".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_10")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_11")
    def VER_9_6_11(cls) -> "PostgresEngineVersion":
        """Version "9.6.11".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_12")
    def VER_9_6_12(cls) -> "PostgresEngineVersion":
        """Version "9.6.12".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_12")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_14")
    def VER_9_6_14(cls) -> "PostgresEngineVersion":
        """Version "9.6.14".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_14")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_15")
    def VER_9_6_15(cls) -> "PostgresEngineVersion":
        """Version "9.6.15".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_15")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_16")
    def VER_9_6_16(cls) -> "PostgresEngineVersion":
        """Version "9.6.16".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_16")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_17")
    def VER_9_6_17(cls) -> "PostgresEngineVersion":
        """Version "9.6.17".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_17")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_18")
    def VER_9_6_18(cls) -> "PostgresEngineVersion":
        """Version "9.6.18".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_18")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_2")
    def VER_9_6_2(cls) -> "PostgresEngineVersion":
        """Version "9.6.2".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_2")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_3")
    def VER_9_6_3(cls) -> "PostgresEngineVersion":
        """Version "9.6.3".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_3")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_5")
    def VER_9_6_5(cls) -> "PostgresEngineVersion":
        """Version "9.6.5".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_5")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_6")
    def VER_9_6_6(cls) -> "PostgresEngineVersion":
        """Version "9.6.6".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_6")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_8")
    def VER_9_6_8(cls) -> "PostgresEngineVersion":
        """Version "9.6.8".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_8")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_9_6_9")
    def VER_9_6_9(cls) -> "PostgresEngineVersion":
        """Version "9.6.9".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_9_6_9")

    @builtins.property
    @jsii.member(jsii_name="postgresFullVersion")
    def postgres_full_version(self) -> str:
        """The full version string, for example, "13.11".

        stability
        :stability: experimental
        """
        return jsii.get(self, "postgresFullVersion")

    @builtins.property
    @jsii.member(jsii_name="postgresMajorVersion")
    def postgres_major_version(self) -> str:
        """The major version of the engine, for example, "13".

        stability
        :stability: experimental
        """
        return jsii.get(self, "postgresMajorVersion")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.PostgresInstanceEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class PostgresInstanceEngineProps:
    def __init__(self, *, version: "PostgresEngineVersion") -> None:
        """Properties for PostgreSQL instance engines.

        Used in {@link DatabaseInstanceEngine.postgres}.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "PostgresEngineVersion":
        """The exact version of the engine to use.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PostgresInstanceEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.ProcessorFeatures",
    jsii_struct_bases=[],
    name_mapping={"core_count": "coreCount", "threads_per_core": "threadsPerCore"},
)
class ProcessorFeatures:
    def __init__(
        self,
        *,
        core_count: typing.Optional[jsii.Number] = None,
        threads_per_core: typing.Optional[jsii.Number] = None,
    ) -> None:
        """The processor features.

        :param core_count: The number of CPU core. Default: - the default number of CPU cores for the chosen instance class.
        :param threads_per_core: The number of threads per core. Default: - the default number of threads per core for the chosen instance class.

        stability
        :stability: experimental
        """
        self._values = {}
        if core_count is not None:
            self._values["core_count"] = core_count
        if threads_per_core is not None:
            self._values["threads_per_core"] = threads_per_core

    @builtins.property
    def core_count(self) -> typing.Optional[jsii.Number]:
        """The number of CPU core.

        default
        :default: - the default number of CPU cores for the chosen instance class.

        stability
        :stability: experimental
        """
        return self._values.get("core_count")

    @builtins.property
    def threads_per_core(self) -> typing.Optional[jsii.Number]:
        """The number of threads per core.

        default
        :default: - the default number of threads per core for the chosen instance class.

        stability
        :stability: experimental
        """
        return self._values.get("threads_per_core")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProcessorFeatures(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ProxyTarget(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_rds.ProxyTarget"
):
    """Proxy target: Instance or Cluster.

    A target group is a collection of databases that the proxy can connect to.
    Currently, you can specify only one RDS DB instance or Aurora DB cluster.

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="fromCluster")
    @builtins.classmethod
    def from_cluster(cls, cluster: "IDatabaseCluster") -> "ProxyTarget":
        """From cluster.

        :param cluster: RDS database cluster.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromCluster", [cluster])

    @jsii.member(jsii_name="fromInstance")
    @builtins.classmethod
    def from_instance(cls, instance: "IDatabaseInstance") -> "ProxyTarget":
        """From instance.

        :param instance: RDS database instance.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "fromInstance", [instance])

    @jsii.member(jsii_name="bind")
    def bind(self, _: "DatabaseProxy") -> "ProxyTargetConfig":
        """Bind this target to the specified database proxy.

        :param _: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "bind", [_])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.ProxyTargetConfig",
    jsii_struct_bases=[],
    name_mapping={
        "engine_family": "engineFamily",
        "db_clusters": "dbClusters",
        "db_instances": "dbInstances",
    },
)
class ProxyTargetConfig:
    def __init__(
        self,
        *,
        engine_family: str,
        db_clusters: typing.Optional[typing.List["IDatabaseCluster"]] = None,
        db_instances: typing.Optional[typing.List["IDatabaseInstance"]] = None,
    ) -> None:
        """The result of binding a ``ProxyTarget`` to a ``DatabaseProxy``.

        :param engine_family: The engine family of the database instance or cluster this proxy connects with.
        :param db_clusters: The database clusters to which this proxy connects. Either this or ``dbInstances`` will be set and the other ``undefined``. Default: - ``undefined`` if ``dbInstances`` is set.
        :param db_instances: The database instances to which this proxy connects. Either this or ``dbClusters`` will be set and the other ``undefined``. Default: - ``undefined`` if ``dbClusters`` is set.

        stability
        :stability: experimental
        """
        self._values = {
            "engine_family": engine_family,
        }
        if db_clusters is not None:
            self._values["db_clusters"] = db_clusters
        if db_instances is not None:
            self._values["db_instances"] = db_instances

    @builtins.property
    def engine_family(self) -> str:
        """The engine family of the database instance or cluster this proxy connects with.

        stability
        :stability: experimental
        """
        return self._values.get("engine_family")

    @builtins.property
    def db_clusters(self) -> typing.Optional[typing.List["IDatabaseCluster"]]:
        """The database clusters to which this proxy connects.

        Either this or ``dbInstances`` will be set and the other ``undefined``.

        default
        :default: - ``undefined`` if ``dbInstances`` is set.

        stability
        :stability: experimental
        """
        return self._values.get("db_clusters")

    @builtins.property
    def db_instances(self) -> typing.Optional[typing.List["IDatabaseInstance"]]:
        """The database instances to which this proxy connects.

        Either this or ``dbClusters`` will be set and the other ``undefined``.

        default
        :default: - ``undefined`` if ``dbClusters`` is set.

        stability
        :stability: experimental
        """
        return self._values.get("db_instances")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProxyTargetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.RotationMultiUserOptions",
    jsii_struct_bases=[],
    name_mapping={"secret": "secret", "automatically_after": "automaticallyAfter"},
)
class RotationMultiUserOptions:
    def __init__(
        self,
        *,
        secret: _ISecret_75279d36,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
    ) -> None:
        """Options to add the multi user rotation.

        :param secret: The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> }
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        self._values = {
            "secret": secret,
        }
        if automatically_after is not None:
            self._values["automatically_after"] = automatically_after

    @builtins.property
    def secret(self) -> _ISecret_75279d36:
        """The secret to rotate.

        It must be a JSON string with the following format::

           {
              "engine": <required: database engine>,
              "host": <required: instance host name>,
              "username": <required: username>,
              "password": <required: password>,
              "dbname": <optional: database name>,
              "port": <optional: if not specified, default port will be used>,
              "masterarn": <required: the arn of the master secret which will be used to create users/change passwords>
           }

        stability
        :stability: experimental
        """
        return self._values.get("secret")

    @builtins.property
    def automatically_after(self) -> typing.Optional[_Duration_5170c158]:
        """Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        default
        :default: Duration.days(30)

        stability
        :stability: experimental
        """
        return self._values.get("automatically_after")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RotationMultiUserOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SessionPinningFilter(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.SessionPinningFilter",
):
    """SessionPinningFilter.

    see
    :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html#rds-proxy-pinning
    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, filter_name: str) -> "SessionPinningFilter":
        """custom filter.

        :param filter_name: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [filter_name])

    @jsii.python.classproperty
    @jsii.member(jsii_name="EXCLUDE_VARIABLE_SETS")
    def EXCLUDE_VARIABLE_SETS(cls) -> "SessionPinningFilter":
        """You can opt out of session pinning for the following kinds of application statements:.

        - Setting session variables and configuration settings.

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "EXCLUDE_VARIABLE_SETS")

    @builtins.property
    @jsii.member(jsii_name="filterName")
    def filter_name(self) -> str:
        """Filter name.

        stability
        :stability: experimental
        """
        return jsii.get(self, "filterName")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.SqlServerEeInstanceEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class SqlServerEeInstanceEngineProps:
    def __init__(self, *, version: "SqlServerEngineVersion") -> None:
        """Properties for SQL Server Enterprise Edition instance engines.

        Used in {@link DatabaseInstanceEngine.sqlServerEe}.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "SqlServerEngineVersion":
        """The exact version of the engine to use.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlServerEeInstanceEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlServerEngineVersion(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.SqlServerEngineVersion",
):
    """The versions for the SQL Server instance engines (those returned by {@link DatabaseInstanceEngine.sqlServerSe}, {@link DatabaseInstanceEngine.sqlServerEx}, {@link DatabaseInstanceEngine.sqlServerWeb} and {@link DatabaseInstanceEngine.sqlServerEe}).

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls, sql_server_full_version: str, sql_server_major_version: str
    ) -> "SqlServerEngineVersion":
        """Create a new SqlServerEngineVersion with an arbitrary version.

        :param sql_server_full_version: the full version string, for example "15.00.3049.1.v1".
        :param sql_server_major_version: the major version of the engine, for example "15.00".

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [sql_server_full_version, sql_server_major_version])

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11")
    def VER_11(cls) -> "SqlServerEngineVersion":
        """Version "11.00" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_00_5058_0_V1")
    def VER_11_00_5058_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "11.00.5058.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_00_5058_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_00_6020_0_V1")
    def VER_11_00_6020_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "11.00.6020.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_00_6020_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_00_6594_0_V1")
    def VER_11_00_6594_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "11.00.6594.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_00_6594_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_00_7462_6_V1")
    def VER_11_00_7462_6_V1(cls) -> "SqlServerEngineVersion":
        """Version "11.00.7462.6.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_00_7462_6_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_11_00_7493_4_V1")
    def VER_11_00_7493_4_V1(cls) -> "SqlServerEngineVersion":
        """Version "11.00.7493.4.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_11_00_7493_4_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12")
    def VER_12(cls) -> "SqlServerEngineVersion":
        """Version "12.00" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_00_5000_0_V1")
    def VER_12_00_5000_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "12.00.5000.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_00_5000_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_00_5546_0_V1")
    def VER_12_00_5546_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "12.00.5546.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_00_5546_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_00_5571_0_V1")
    def VER_12_00_5571_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "12.00.5571.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_00_5571_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_00_6293_0_V1")
    def VER_12_00_6293_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "12.00.6293.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_00_6293_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_12_00_6329_1_V1")
    def VER_12_00_6329_1_V1(cls) -> "SqlServerEngineVersion":
        """Version "12.00.6329.1.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_12_00_6329_1_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_13")
    def VER_13(cls) -> "SqlServerEngineVersion":
        """Version "13.00" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_13")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_13_00_2164_0_V1")
    def VER_13_00_2164_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "13.00.2164.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_13_00_2164_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_13_00_4422_0_V1")
    def VER_13_00_4422_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "13.00.4422.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_13_00_4422_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_13_00_4451_0_V1")
    def VER_13_00_4451_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "13.00.4451.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_13_00_4451_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_13_00_4466_4_V1")
    def VER_13_00_4466_4_V1(cls) -> "SqlServerEngineVersion":
        """Version "13.00.4466.4.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_13_00_4466_4_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_13_00_4522_0_V1")
    def VER_13_00_4522_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "13.00.4522.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_13_00_4522_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_13_00_5216_0_V1")
    def VER_13_00_5216_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "13.00.5216.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_13_00_5216_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_13_00_5292_0_V1")
    def VER_13_00_5292_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "13.00.5292.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_13_00_5292_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_13_00_5366_0_V1")
    def VER_13_00_5366_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "13.00.5366.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_13_00_5366_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_13_00_5426_0_V1")
    def VER_13_00_5426_0_V1(cls) -> "SqlServerEngineVersion":
        """Version "13.00.5426.0.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_13_00_5426_0_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_13_00_5598_27_V1")
    def VER_13_00_5598_27_V1(cls) -> "SqlServerEngineVersion":
        """Version "13.00.5598.27.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_13_00_5598_27_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_14")
    def VER_14(cls) -> "SqlServerEngineVersion":
        """Version "14.00" (only a major version, without a specific minor version).

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_14")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_14_00_1000_169_V1")
    def VER_14_00_1000_169_V1(cls) -> "SqlServerEngineVersion":
        """Version "14.00.1000.169.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_14_00_1000_169_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_14_00_3015_40_V1")
    def VER_14_00_3015_40_V1(cls) -> "SqlServerEngineVersion":
        """Version "14.00.3015.40.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_14_00_3015_40_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_14_00_3035_2_V1")
    def VER_14_00_3035_2_V1(cls) -> "SqlServerEngineVersion":
        """Version "14.00.3035.2.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_14_00_3035_2_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_14_00_3049_1_V1")
    def VER_14_00_3049_1_V1(cls) -> "SqlServerEngineVersion":
        """Version "14.00.3049.1.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_14_00_3049_1_V1")

    @jsii.python.classproperty
    @jsii.member(jsii_name="VER_14_00_3192_2_V1")
    def VER_14_00_3192_2_V1(cls) -> "SqlServerEngineVersion":
        """Version "14.00.3192.2.v1".

        stability
        :stability: experimental
        """
        return jsii.sget(cls, "VER_14_00_3192_2_V1")

    @builtins.property
    @jsii.member(jsii_name="sqlServerFullVersion")
    def sql_server_full_version(self) -> str:
        """The full version string, for example, "15.00.3049.1.v1".

        stability
        :stability: experimental
        """
        return jsii.get(self, "sqlServerFullVersion")

    @builtins.property
    @jsii.member(jsii_name="sqlServerMajorVersion")
    def sql_server_major_version(self) -> str:
        """The major version of the engine, for example, "15.00".

        stability
        :stability: experimental
        """
        return jsii.get(self, "sqlServerMajorVersion")


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.SqlServerExInstanceEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class SqlServerExInstanceEngineProps:
    def __init__(self, *, version: "SqlServerEngineVersion") -> None:
        """Properties for SQL Server Express Edition instance engines.

        Used in {@link DatabaseInstanceEngine.sqlServerEx}.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "SqlServerEngineVersion":
        """The exact version of the engine to use.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlServerExInstanceEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.SqlServerSeInstanceEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class SqlServerSeInstanceEngineProps:
    def __init__(self, *, version: "SqlServerEngineVersion") -> None:
        """Properties for SQL Server Standard Edition instance engines.

        Used in {@link DatabaseInstanceEngine.sqlServerSe}.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "SqlServerEngineVersion":
        """The exact version of the engine to use.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlServerSeInstanceEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.SqlServerWebInstanceEngineProps",
    jsii_struct_bases=[],
    name_mapping={"version": "version"},
)
class SqlServerWebInstanceEngineProps:
    def __init__(self, *, version: "SqlServerEngineVersion") -> None:
        """Properties for SQL Server Web Edition instance engines.

        Used in {@link DatabaseInstanceEngine.sqlServerWeb}.

        :param version: The exact version of the engine to use.

        stability
        :stability: experimental
        """
        self._values = {
            "version": version,
        }

    @builtins.property
    def version(self) -> "SqlServerEngineVersion":
        """The exact version of the engine to use.

        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlServerWebInstanceEngineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk-experiment.aws_rds.StorageType")
class StorageType(enum.Enum):
    """The type of storage.

    stability
    :stability: experimental
    """

    STANDARD = "STANDARD"
    """Standard.

    stability
    :stability: experimental
    """
    GP2 = "GP2"
    """General purpose (SSD).

    stability
    :stability: experimental
    """
    IO1 = "IO1"
    """Provisioned IOPS (SSD).

    stability
    :stability: experimental
    """


@jsii.implements(IDatabaseCluster)
class DatabaseCluster(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.DatabaseCluster",
):
    """Create a clustered database with a given number of instances.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::RDS::DBCluster
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        engine: "IClusterEngine",
        instance_props: "InstanceProps",
        master_user: "Login",
        backup: typing.Optional["BackupProps"] = None,
        cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        cloudwatch_logs_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        cloudwatch_logs_retention_role: typing.Optional[_IRole_e69bbae4] = None,
        cluster_identifier: typing.Optional[str] = None,
        default_database_name: typing.Optional[str] = None,
        deletion_protection: typing.Optional[bool] = None,
        instance_identifier_base: typing.Optional[str] = None,
        instances: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[_Duration_5170c158] = None,
        monitoring_role: typing.Optional[_IRole_e69bbae4] = None,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        s3_export_buckets: typing.Optional[typing.List[_IBucket_25bad983]] = None,
        s3_export_role: typing.Optional[_IRole_e69bbae4] = None,
        s3_import_buckets: typing.Optional[typing.List[_IBucket_25bad983]] = None,
        s3_import_role: typing.Optional[_IRole_e69bbae4] = None,
        storage_encrypted: typing.Optional[bool] = None,
        storage_encryption_key: typing.Optional[_IKey_3336c79d] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param engine: What kind of database to start.
        :param instance_props: Settings for the individual instances that are launched.
        :param master_user: Username and password for the administrative user.
        :param backup: Backup settings. Default: - Backup retention period for automated backups is 1 day. Backup preferred window is set to a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param cluster_identifier: An optional identifier for the cluster. Default: - A name is automatically generated.
        :param default_database_name: Name of a database which is automatically created inside the cluster. Default: - Database is not created in cluster.
        :param deletion_protection: Indicates whether the DB cluster should have deletion protection enabled. Default: false
        :param instance_identifier_base: Base identifier for instances. Every replica is named by appending the replica number to this string, 1-based. Default: - clusterIdentifier is used with the word "Instance" appended. If clusterIdentifier is not provided, the identifier is automatically generated.
        :param instances: How many replicas/instances to create. Has to be at least 1. Default: 2
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instances. Default: no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instances monitoring. Default: - A role is automatically created for you
        :param parameter_group: Additional parameters to pass to the database engine. Default: - No parameter group.
        :param port: What port to listen on. Default: - The default for the engine is used.
        :param preferred_maintenance_window: A preferred maintenance window day/time range. Should be specified as a range ddd:hh24:mi-ddd:hh24:mi (24H Clock UTC). Example: 'Sun:23:45-Mon:00:15' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
        :param removal_policy: The removal policy to apply when the cluster and its instances are removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the cluster and instances, but retain a snapshot of the data)
        :param s3_export_buckets: S3 buckets that you want to load data into. This feature is only supported by the Aurora database engine. This property must not be used if ``s3ExportRole`` is used. For MySQL: Default: - None
        :param s3_export_role: Role that will be associated with this DB cluster to enable S3 export. This feature is only supported by the Aurora database engine. This property must not be used if ``s3ExportBuckets`` is used. For MySQL: Default: - New role is created if ``s3ExportBuckets`` is set, no role is defined otherwise
        :param s3_import_buckets: S3 buckets that you want to load data from. This feature is only supported by the Aurora database engine. This property must not be used if ``s3ImportRole`` is used. For MySQL: Default: - None
        :param s3_import_role: Role that will be associated with this DB cluster to enable S3 import. This feature is only supported by the Aurora database engine. This property must not be used if ``s3ImportBuckets`` is used. For MySQL: Default: - New role is created if ``s3ImportBuckets`` is set, no role is defined otherwise
        :param storage_encrypted: Whether to enable storage encryption. Default: - true if storageEncryptionKey is provided, false otherwise
        :param storage_encryption_key: The KMS key for storage encryption. If specified, {@link storageEncrypted} will be set to ``true``. Default: - if storageEncrypted is true then the default master key, no key otherwise

        stability
        :stability: experimental
        """
        props = DatabaseClusterProps(
            engine=engine,
            instance_props=instance_props,
            master_user=master_user,
            backup=backup,
            cloudwatch_logs_exports=cloudwatch_logs_exports,
            cloudwatch_logs_retention=cloudwatch_logs_retention,
            cloudwatch_logs_retention_role=cloudwatch_logs_retention_role,
            cluster_identifier=cluster_identifier,
            default_database_name=default_database_name,
            deletion_protection=deletion_protection,
            instance_identifier_base=instance_identifier_base,
            instances=instances,
            monitoring_interval=monitoring_interval,
            monitoring_role=monitoring_role,
            parameter_group=parameter_group,
            port=port,
            preferred_maintenance_window=preferred_maintenance_window,
            removal_policy=removal_policy,
            s3_export_buckets=s3_export_buckets,
            s3_export_role=s3_export_role,
            s3_import_buckets=s3_import_buckets,
            s3_import_role=s3_import_role,
            storage_encrypted=storage_encrypted,
            storage_encryption_key=storage_encryption_key,
        )

        jsii.create(DatabaseCluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromDatabaseClusterAttributes")
    @builtins.classmethod
    def from_database_cluster_attributes(
        cls,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        cluster_endpoint_address: str,
        cluster_identifier: str,
        instance_endpoint_addresses: typing.List[str],
        instance_identifiers: typing.List[str],
        port: jsii.Number,
        reader_endpoint_address: str,
        security_groups: typing.List[_ISecurityGroup_d72ab8e8],
    ) -> "IDatabaseCluster":
        """Import an existing DatabaseCluster from properties.

        :param scope: -
        :param id: -
        :param cluster_endpoint_address: Cluster endpoint address.
        :param cluster_identifier: Identifier for the cluster.
        :param instance_endpoint_addresses: Endpoint addresses of individual instances.
        :param instance_identifiers: Identifier for the instances.
        :param port: The database port.
        :param reader_endpoint_address: Reader endpoint address.
        :param security_groups: The security groups of the database cluster.

        stability
        :stability: experimental
        """
        attrs = DatabaseClusterAttributes(
            cluster_endpoint_address=cluster_endpoint_address,
            cluster_identifier=cluster_identifier,
            instance_endpoint_addresses=instance_endpoint_addresses,
            instance_identifiers=instance_identifiers,
            port=port,
            reader_endpoint_address=reader_endpoint_address,
            security_groups=security_groups,
        )

        return jsii.sinvoke(cls, "fromDatabaseClusterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addProxy")
    def add_proxy(
        self,
        id: str,
        *,
        secrets: typing.List[_ISecret_75279d36],
        vpc: _IVpc_3795853f,
        borrow_timeout: typing.Optional[_Duration_5170c158] = None,
        db_proxy_name: typing.Optional[str] = None,
        debug_logging: typing.Optional[bool] = None,
        iam_auth: typing.Optional[bool] = None,
        idle_client_timeout: typing.Optional[_Duration_5170c158] = None,
        init_query: typing.Optional[str] = None,
        max_connections_percent: typing.Optional[jsii.Number] = None,
        max_idle_connections_percent: typing.Optional[jsii.Number] = None,
        require_tls: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        session_pinning_filters: typing.Optional[typing.List["SessionPinningFilter"]] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> "DatabaseProxy":
        """Add a new db proxy to this cluster.

        :param id: -
        :param secrets: The secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster. These secrets are stored within Amazon Secrets Manager. One or more secrets are required.
        :param vpc: The VPC to associate with the new proxy.
        :param borrow_timeout: The duration for a proxy to wait for a connection to become available in the connection pool. Only applies when the proxy has opened its maximum number of connections and all connections are busy with client sessions. Value must be between 1 second and 1 hour, or ``Duration.seconds(0)`` to represent unlimited. Default: cdk.Duration.seconds(120)
        :param db_proxy_name: The identifier for the proxy. This name must be unique for all proxies owned by your AWS account in the specified AWS Region. An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two consecutive hyphens. Default: - Generated by CloudFormation (recommended)
        :param debug_logging: Whether the proxy includes detailed information about SQL statements in its logs. This information helps you to debug issues involving SQL behavior or the performance and scalability of the proxy connections. The debug information includes the text of SQL statements that you submit through the proxy. Thus, only enable this setting when needed for debugging, and only when you have security measures in place to safeguard any sensitive information that appears in the logs. Default: false
        :param iam_auth: Whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy. Default: false
        :param idle_client_timeout: The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it. You can set this value higher or lower than the connection timeout limit for the associated database. Default: cdk.Duration.minutes(30)
        :param init_query: One or more SQL statements for the proxy to run when opening each new database connection. Typically used with SET statements to make sure that each connection has identical settings such as time zone and character set. For multiple statements, use semicolons as the separator. You can also include multiple variables in a single SET statement, such as SET x=1, y=2. not currently supported for PostgreSQL. Default: - no initialization query
        :param max_connections_percent: The maximum size of the connection pool for each target in a target group. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. 1-100 Default: 100
        :param max_idle_connections_percent: Controls how actively the proxy closes idle database connections in the connection pool. A high value enables the proxy to leave a high percentage of idle connections open. A low value causes the proxy to close idle client connections and return the underlying database connections to the connection pool. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. between 0 and MaxConnectionsPercent Default: 50
        :param require_tls: A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy. By enabling this setting, you can enforce encrypted TLS connections to the proxy. Default: true
        :param role: IAM role that the proxy uses to access secrets in AWS Secrets Manager. Default: - A role will automatically be created
        :param security_groups: One or more VPC security groups to associate with the new proxy. Default: - No security groups
        :param session_pinning_filters: Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection. Including an item in the list exempts that class of SQL operations from the pinning behavior. Default: - no session pinning filters
        :param vpc_subnets: The subnets used by the proxy. Default: - the VPC default strategy if not specified.

        stability
        :stability: experimental
        """
        options = DatabaseProxyOptions(
            secrets=secrets,
            vpc=vpc,
            borrow_timeout=borrow_timeout,
            db_proxy_name=db_proxy_name,
            debug_logging=debug_logging,
            iam_auth=iam_auth,
            idle_client_timeout=idle_client_timeout,
            init_query=init_query,
            max_connections_percent=max_connections_percent,
            max_idle_connections_percent=max_idle_connections_percent,
            require_tls=require_tls,
            role=role,
            security_groups=security_groups,
            session_pinning_filters=session_pinning_filters,
            vpc_subnets=vpc_subnets,
        )

        return jsii.invoke(self, "addProxy", [id, options])

    @jsii.member(jsii_name="addRotationMultiUser")
    def add_rotation_multi_user(
        self,
        id: str,
        *,
        secret: _ISecret_75279d36,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
    ) -> _SecretRotation_312fb992:
        """Adds the multi user rotation to this cluster.

        :param id: -
        :param secret: The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> }
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        options = RotationMultiUserOptions(
            secret=secret, automatically_after=automatically_after
        )

        return jsii.invoke(self, "addRotationMultiUser", [id, options])

    @jsii.member(jsii_name="addRotationSingleUser")
    def add_rotation_single_user(
        self, automatically_after: typing.Optional[_Duration_5170c158] = None
    ) -> _SecretRotation_312fb992:
        """Adds the single user rotation of the master password to this cluster.

        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addRotationSingleUser", [automatically_after])

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> _SecretAttachmentTargetProps_b948cd13:
        """Renders the secret attachment target specifications.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "asSecretAttachmentTarget", [])

    @builtins.property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        """The endpoint to use for read/write operations.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterEndpoint")

    @builtins.property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """Identifier of the cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterIdentifier")

    @builtins.property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> "Endpoint":
        """Endpoint to use for load-balanced read-only operations.

        stability
        :stability: experimental
        """
        return jsii.get(self, "clusterReadEndpoint")

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Access to the network connections.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        """Endpoints which address each individual replica.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceEndpoints")

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        """Identifiers of the replicas.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceIdentifiers")

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Optional[_ISecret_75279d36]:
        """The secret attached to this cluster.

        stability
        :stability: experimental
        """
        return jsii.get(self, "secret")


@jsii.implements(IDatabaseInstance)
class DatabaseInstanceBase(
    _Resource_884d0774,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk-experiment.aws_rds.DatabaseInstanceBase",
):
    """A new or imported database instance.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _DatabaseInstanceBaseProxy

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        account: typing.Optional[str] = None,
        physical_name: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to

        stability
        :stability: experimental
        """
        props = _ResourceProps_92be6f66(
            account=account, physical_name=physical_name, region=region
        )

        jsii.create(DatabaseInstanceBase, self, [scope, id, props])

    @jsii.member(jsii_name="fromDatabaseInstanceAttributes")
    @builtins.classmethod
    def from_database_instance_attributes(
        cls,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        instance_endpoint_address: str,
        instance_identifier: str,
        port: jsii.Number,
        security_groups: typing.List[_ISecurityGroup_d72ab8e8],
    ) -> "IDatabaseInstance":
        """Import an existing database instance.

        :param scope: -
        :param id: -
        :param instance_endpoint_address: The endpoint address.
        :param instance_identifier: The instance identifier.
        :param port: The database port.
        :param security_groups: The security groups of the instance.

        stability
        :stability: experimental
        """
        attrs = DatabaseInstanceAttributes(
            instance_endpoint_address=instance_endpoint_address,
            instance_identifier=instance_identifier,
            port=port,
            security_groups=security_groups,
        )

        return jsii.sinvoke(cls, "fromDatabaseInstanceAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addProxy")
    def add_proxy(
        self,
        id: str,
        *,
        secrets: typing.List[_ISecret_75279d36],
        vpc: _IVpc_3795853f,
        borrow_timeout: typing.Optional[_Duration_5170c158] = None,
        db_proxy_name: typing.Optional[str] = None,
        debug_logging: typing.Optional[bool] = None,
        iam_auth: typing.Optional[bool] = None,
        idle_client_timeout: typing.Optional[_Duration_5170c158] = None,
        init_query: typing.Optional[str] = None,
        max_connections_percent: typing.Optional[jsii.Number] = None,
        max_idle_connections_percent: typing.Optional[jsii.Number] = None,
        require_tls: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        session_pinning_filters: typing.Optional[typing.List["SessionPinningFilter"]] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> "DatabaseProxy":
        """Add a new db proxy to this instance.

        :param id: -
        :param secrets: The secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster. These secrets are stored within Amazon Secrets Manager. One or more secrets are required.
        :param vpc: The VPC to associate with the new proxy.
        :param borrow_timeout: The duration for a proxy to wait for a connection to become available in the connection pool. Only applies when the proxy has opened its maximum number of connections and all connections are busy with client sessions. Value must be between 1 second and 1 hour, or ``Duration.seconds(0)`` to represent unlimited. Default: cdk.Duration.seconds(120)
        :param db_proxy_name: The identifier for the proxy. This name must be unique for all proxies owned by your AWS account in the specified AWS Region. An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two consecutive hyphens. Default: - Generated by CloudFormation (recommended)
        :param debug_logging: Whether the proxy includes detailed information about SQL statements in its logs. This information helps you to debug issues involving SQL behavior or the performance and scalability of the proxy connections. The debug information includes the text of SQL statements that you submit through the proxy. Thus, only enable this setting when needed for debugging, and only when you have security measures in place to safeguard any sensitive information that appears in the logs. Default: false
        :param iam_auth: Whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy. Default: false
        :param idle_client_timeout: The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it. You can set this value higher or lower than the connection timeout limit for the associated database. Default: cdk.Duration.minutes(30)
        :param init_query: One or more SQL statements for the proxy to run when opening each new database connection. Typically used with SET statements to make sure that each connection has identical settings such as time zone and character set. For multiple statements, use semicolons as the separator. You can also include multiple variables in a single SET statement, such as SET x=1, y=2. not currently supported for PostgreSQL. Default: - no initialization query
        :param max_connections_percent: The maximum size of the connection pool for each target in a target group. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. 1-100 Default: 100
        :param max_idle_connections_percent: Controls how actively the proxy closes idle database connections in the connection pool. A high value enables the proxy to leave a high percentage of idle connections open. A low value causes the proxy to close idle client connections and return the underlying database connections to the connection pool. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. between 0 and MaxConnectionsPercent Default: 50
        :param require_tls: A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy. By enabling this setting, you can enforce encrypted TLS connections to the proxy. Default: true
        :param role: IAM role that the proxy uses to access secrets in AWS Secrets Manager. Default: - A role will automatically be created
        :param security_groups: One or more VPC security groups to associate with the new proxy. Default: - No security groups
        :param session_pinning_filters: Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection. Including an item in the list exempts that class of SQL operations from the pinning behavior. Default: - no session pinning filters
        :param vpc_subnets: The subnets used by the proxy. Default: - the VPC default strategy if not specified.

        stability
        :stability: experimental
        """
        options = DatabaseProxyOptions(
            secrets=secrets,
            vpc=vpc,
            borrow_timeout=borrow_timeout,
            db_proxy_name=db_proxy_name,
            debug_logging=debug_logging,
            iam_auth=iam_auth,
            idle_client_timeout=idle_client_timeout,
            init_query=init_query,
            max_connections_percent=max_connections_percent,
            max_idle_connections_percent=max_idle_connections_percent,
            require_tls=require_tls,
            role=role,
            security_groups=security_groups,
            session_pinning_filters=session_pinning_filters,
            vpc_subnets=vpc_subnets,
        )

        return jsii.invoke(self, "addProxy", [id, options])

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> _SecretAttachmentTargetProps_b948cd13:
        """Renders the secret attachment target specifications.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "asSecretAttachmentTarget", [])

    @jsii.member(jsii_name="grantConnect")
    def grant_connect(self, grantee: _IGrantable_0fcfc53a) -> _Grant_96af6d2d:
        """Grant the given identity connection access to the database.

        :param grantee: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "grantConnect", [grantee])

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: str,
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
        """Return the given named metric for this DBInstance.

        :param metric_name: -
        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricCPUUtilization")
    def metric_cpu_utilization(
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
        """The percentage of CPU utilization.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricCPUUtilization", [props])

    @jsii.member(jsii_name="metricDatabaseConnections")
    def metric_database_connections(
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
        """The number of database connections in use.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricDatabaseConnections", [props])

    @jsii.member(jsii_name="metricFreeableMemory")
    def metric_freeable_memory(
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
        """The amount of available random access memory.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricFreeableMemory", [props])

    @jsii.member(jsii_name="metricFreeStorageSpace")
    def metric_free_storage_space(
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
        """The amount of available storage space.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricFreeStorageSpace", [props])

    @jsii.member(jsii_name="metricReadIOPS")
    def metric_read_iops(
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
        """The average number of disk write I/O operations per second.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricReadIOPS", [props])

    @jsii.member(jsii_name="metricWriteIOPS")
    def metric_write_iops(
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
        """The average number of disk read I/O operations per second.

        Average over 5 minutes

        :param account: Account which this metric comes from. Default: - Deployment account.
        :param color: The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: Dimensions of the metric. Default: - No dimensions.
        :param label: Label for this metric when added to a Graph in a Dashboard. Default: - No label
        :param period: The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: Region which this metric comes from. Default: - Deployment region.
        :param statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        stability
        :stability: experimental
        """
        props = _MetricOptions_ad2c4d5d(
            account=account,
            color=color,
            dimensions=dimensions,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return jsii.invoke(self, "metricWriteIOPS", [props])

    @jsii.member(jsii_name="onEvent")
    def on_event(
        self,
        id: str,
        *,
        description: typing.Optional[str] = None,
        event_pattern: typing.Optional[_EventPattern_8aa7b781] = None,
        rule_name: typing.Optional[str] = None,
        target: typing.Optional[_IRuleTarget_41800a77] = None,
    ) -> _Rule_c38e0b39:
        """Defines a CloudWatch event rule which triggers for instance events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        :param id: -
        :param description: A description of the rule's purpose. Default: - No description
        :param event_pattern: Additional restrictions for the event to route to the specified target. The method that generates the rule probably imposes some type of event filtering. The filtering implied by what you pass here is added on top of that filtering. Default: - No additional filtering based on an event pattern.
        :param rule_name: A name for the rule. Default: AWS CloudFormation generates a unique physical ID.
        :param target: The target to register for the event. Default: - No target is added to the rule. Use ``addTarget()`` to add a target.

        stability
        :stability: experimental
        """
        options = _OnEventOptions_926fbcf9(
            description=description,
            event_pattern=event_pattern,
            rule_name=rule_name,
            target=target,
        )

        return jsii.invoke(self, "onEvent", [id, options])

    @builtins.property
    @jsii.member(jsii_name="connections")
    @abc.abstractmethod
    def connections(self) -> _Connections_231f38b5:
        """Access to network connections.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    @abc.abstractmethod
    def db_instance_endpoint_address(self) -> str:
        """The instance endpoint address.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    @abc.abstractmethod
    def db_instance_endpoint_port(self) -> str:
        """The instance endpoint port.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> str:
        """The instance arn.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceArn")

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    @abc.abstractmethod
    def instance_endpoint(self) -> "Endpoint":
        """The instance endpoint.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    @abc.abstractmethod
    def instance_identifier(self) -> str:
        """The instance identifier.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="enableIamAuthentication")
    @abc.abstractmethod
    def _enable_iam_authentication(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        ...

    @_enable_iam_authentication.setter
    @abc.abstractmethod
    def _enable_iam_authentication(self, value: typing.Optional[bool]) -> None:
        ...


class _DatabaseInstanceBaseProxy(
    DatabaseInstanceBase, jsii.proxy_for(_Resource_884d0774)
):
    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Access to network connections.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> str:
        """The instance endpoint address.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dbInstanceEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> str:
        """The instance endpoint port.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dbInstanceEndpointPort")

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> "Endpoint":
        """The instance endpoint.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceEndpoint")

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> str:
        """The instance identifier.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceIdentifier")

    @builtins.property
    @jsii.member(jsii_name="enableIamAuthentication")
    def _enable_iam_authentication(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "enableIamAuthentication")

    @_enable_iam_authentication.setter
    def _enable_iam_authentication(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "enableIamAuthentication", value)


@jsii.implements(IDatabaseInstance)
class DatabaseInstanceFromSnapshot(
    DatabaseInstanceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.DatabaseInstanceFromSnapshot",
):
    """A database instance restored from a snapshot.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::RDS::DBInstance
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        snapshot_identifier: str,
        generate_master_user_password: typing.Optional[bool] = None,
        master_username: typing.Optional[str] = None,
        engine: "IInstanceEngine",
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[bool] = None,
        database_name: typing.Optional[str] = None,
        instance_type: typing.Optional[_InstanceType_85a97b30] = None,
        license_model: typing.Optional["LicenseModel"] = None,
        master_user_password: typing.Optional[_SecretValue_99478b8b] = None,
        master_user_password_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        timezone: typing.Optional[str] = None,
        vpc: _IVpc_3795853f,
        auto_minor_version_upgrade: typing.Optional[bool] = None,
        availability_zone: typing.Optional[str] = None,
        backup_retention: typing.Optional[_Duration_5170c158] = None,
        cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        cloudwatch_logs_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        cloudwatch_logs_retention_role: typing.Optional[_IRole_e69bbae4] = None,
        copy_tags_to_snapshot: typing.Optional[bool] = None,
        delete_automated_backups: typing.Optional[bool] = None,
        deletion_protection: typing.Optional[bool] = None,
        domain: typing.Optional[str] = None,
        domain_role: typing.Optional[_IRole_e69bbae4] = None,
        enable_performance_insights: typing.Optional[bool] = None,
        iam_authentication: typing.Optional[bool] = None,
        instance_identifier: typing.Optional[str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[_Duration_5170c158] = None,
        monitoring_role: typing.Optional[_IRole_e69bbae4] = None,
        multi_az: typing.Optional[bool] = None,
        option_group: typing.Optional["IOptionGroup"] = None,
        performance_insight_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        performance_insight_retention: typing.Optional["PerformanceInsightRetention"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[str] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        processor_features: typing.Optional["ProcessorFeatures"] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        storage_type: typing.Optional["StorageType"] = None,
        vpc_placement: typing.Optional[_SubnetSelection_36a13cd6] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param snapshot_identifier: The name or Amazon Resource Name (ARN) of the DB snapshot that's used to restore the DB instance. If you're restoring from a shared manual DB snapshot, you must specify the ARN of the snapshot.
        :param generate_master_user_password: Whether to generate a new master user password and store it in Secrets Manager. ``masterUsername`` must be specified with the **current** master user name of the snapshot when this property is set to true. Default: false
        :param master_username: The master user name. Specify this prop with the **current** master user name of the snapshot only when generating a new master user password with ``generateMasterUserPassword``. The value will be set in the generated secret attached to the instance. It is not possible to change the master user name of a RDS instance. Default: - inherited from the snapshot
        :param engine: The database engine.
        :param allocated_storage: The allocated storage size, specified in gigabytes (GB). Default: 100
        :param allow_major_version_upgrade: Whether to allow major version upgrades. Default: false
        :param database_name: The name of the database. Default: - no name
        :param instance_type: The name of the compute and memory capacity for the instance. Default: - m5.large (or, more specifically, db.m5.large)
        :param license_model: The license model. Default: - RDS default license model
        :param master_user_password: The master user password. Default: - a Secrets Manager generated password
        :param master_user_password_encryption_key: The KMS key used to encrypt the secret for the master user password. Default: - default master key
        :param parameter_group: The DB parameter group to associate with the instance. Default: - no parameter group
        :param timezone: The time zone of the instance. This is currently supported only by Microsoft Sql Server. Default: - RDS default timezone
        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. Default: Duration.days(1)
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: false
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: true
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_type: The storage type. Default: GP2
        :param vpc_placement: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets

        stability
        :stability: experimental
        """
        props = DatabaseInstanceFromSnapshotProps(
            snapshot_identifier=snapshot_identifier,
            generate_master_user_password=generate_master_user_password,
            master_username=master_username,
            engine=engine,
            allocated_storage=allocated_storage,
            allow_major_version_upgrade=allow_major_version_upgrade,
            database_name=database_name,
            instance_type=instance_type,
            license_model=license_model,
            master_user_password=master_user_password,
            master_user_password_encryption_key=master_user_password_encryption_key,
            parameter_group=parameter_group,
            timezone=timezone,
            vpc=vpc,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            availability_zone=availability_zone,
            backup_retention=backup_retention,
            cloudwatch_logs_exports=cloudwatch_logs_exports,
            cloudwatch_logs_retention=cloudwatch_logs_retention,
            cloudwatch_logs_retention_role=cloudwatch_logs_retention_role,
            copy_tags_to_snapshot=copy_tags_to_snapshot,
            delete_automated_backups=delete_automated_backups,
            deletion_protection=deletion_protection,
            domain=domain,
            domain_role=domain_role,
            enable_performance_insights=enable_performance_insights,
            iam_authentication=iam_authentication,
            instance_identifier=instance_identifier,
            iops=iops,
            max_allocated_storage=max_allocated_storage,
            monitoring_interval=monitoring_interval,
            monitoring_role=monitoring_role,
            multi_az=multi_az,
            option_group=option_group,
            performance_insight_encryption_key=performance_insight_encryption_key,
            performance_insight_retention=performance_insight_retention,
            port=port,
            preferred_backup_window=preferred_backup_window,
            preferred_maintenance_window=preferred_maintenance_window,
            processor_features=processor_features,
            removal_policy=removal_policy,
            security_groups=security_groups,
            storage_type=storage_type,
            vpc_placement=vpc_placement,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(DatabaseInstanceFromSnapshot, self, [scope, id, props])

    @jsii.member(jsii_name="addRotationMultiUser")
    def add_rotation_multi_user(
        self,
        id: str,
        *,
        secret: _ISecret_75279d36,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
    ) -> _SecretRotation_312fb992:
        """Adds the multi user rotation to this instance.

        :param id: -
        :param secret: The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> }
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        options = RotationMultiUserOptions(
            secret=secret, automatically_after=automatically_after
        )

        return jsii.invoke(self, "addRotationMultiUser", [id, options])

    @jsii.member(jsii_name="addRotationSingleUser")
    def add_rotation_single_user(
        self, automatically_after: typing.Optional[_Duration_5170c158] = None
    ) -> _SecretRotation_312fb992:
        """Adds the single user rotation of the master password to this instance.

        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addRotationSingleUser", [automatically_after])

    @jsii.member(jsii_name="setLogRetention")
    def _set_log_retention(self) -> None:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "setLogRetention", [])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Access to network connections.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> str:
        """The instance endpoint address.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dbInstanceEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> str:
        """The instance endpoint port.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dbInstanceEndpointPort")

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> "Endpoint":
        """The instance endpoint.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceEndpoint")

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> str:
        """The instance identifier.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceIdentifier")

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def _instance_type(self) -> _InstanceType_85a97b30:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceType")

    @builtins.property
    @jsii.member(jsii_name="newCfnProps")
    def _new_cfn_props(self) -> "CfnDBInstanceProps":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "newCfnProps")

    @builtins.property
    @jsii.member(jsii_name="sourceCfnProps")
    def _source_cfn_props(self) -> "CfnDBInstanceProps":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "sourceCfnProps")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC where this database instance is deployed.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Optional[_ISecret_75279d36]:
        """The AWS Secrets Manager secret attached to the instance.

        stability
        :stability: experimental
        """
        return jsii.get(self, "secret")

    @builtins.property
    @jsii.member(jsii_name="vpcPlacement")
    def _vpc_placement(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "vpcPlacement")

    @builtins.property
    @jsii.member(jsii_name="enableIamAuthentication")
    def _enable_iam_authentication(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "enableIamAuthentication")

    @_enable_iam_authentication.setter
    def _enable_iam_authentication(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "enableIamAuthentication", value)


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.DatabaseInstanceFromSnapshotProps",
    jsii_struct_bases=[DatabaseInstanceSourceProps],
    name_mapping={
        "vpc": "vpc",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "backup_retention": "backupRetention",
        "cloudwatch_logs_exports": "cloudwatchLogsExports",
        "cloudwatch_logs_retention": "cloudwatchLogsRetention",
        "cloudwatch_logs_retention_role": "cloudwatchLogsRetentionRole",
        "copy_tags_to_snapshot": "copyTagsToSnapshot",
        "delete_automated_backups": "deleteAutomatedBackups",
        "deletion_protection": "deletionProtection",
        "domain": "domain",
        "domain_role": "domainRole",
        "enable_performance_insights": "enablePerformanceInsights",
        "iam_authentication": "iamAuthentication",
        "instance_identifier": "instanceIdentifier",
        "iops": "iops",
        "max_allocated_storage": "maxAllocatedStorage",
        "monitoring_interval": "monitoringInterval",
        "monitoring_role": "monitoringRole",
        "multi_az": "multiAz",
        "option_group": "optionGroup",
        "performance_insight_encryption_key": "performanceInsightEncryptionKey",
        "performance_insight_retention": "performanceInsightRetention",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "processor_features": "processorFeatures",
        "removal_policy": "removalPolicy",
        "security_groups": "securityGroups",
        "storage_type": "storageType",
        "vpc_placement": "vpcPlacement",
        "vpc_subnets": "vpcSubnets",
        "engine": "engine",
        "allocated_storage": "allocatedStorage",
        "allow_major_version_upgrade": "allowMajorVersionUpgrade",
        "database_name": "databaseName",
        "instance_type": "instanceType",
        "license_model": "licenseModel",
        "master_user_password": "masterUserPassword",
        "master_user_password_encryption_key": "masterUserPasswordEncryptionKey",
        "parameter_group": "parameterGroup",
        "timezone": "timezone",
        "snapshot_identifier": "snapshotIdentifier",
        "generate_master_user_password": "generateMasterUserPassword",
        "master_username": "masterUsername",
    },
)
class DatabaseInstanceFromSnapshotProps(DatabaseInstanceSourceProps):
    def __init__(
        self,
        *,
        vpc: _IVpc_3795853f,
        auto_minor_version_upgrade: typing.Optional[bool] = None,
        availability_zone: typing.Optional[str] = None,
        backup_retention: typing.Optional[_Duration_5170c158] = None,
        cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        cloudwatch_logs_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        cloudwatch_logs_retention_role: typing.Optional[_IRole_e69bbae4] = None,
        copy_tags_to_snapshot: typing.Optional[bool] = None,
        delete_automated_backups: typing.Optional[bool] = None,
        deletion_protection: typing.Optional[bool] = None,
        domain: typing.Optional[str] = None,
        domain_role: typing.Optional[_IRole_e69bbae4] = None,
        enable_performance_insights: typing.Optional[bool] = None,
        iam_authentication: typing.Optional[bool] = None,
        instance_identifier: typing.Optional[str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[_Duration_5170c158] = None,
        monitoring_role: typing.Optional[_IRole_e69bbae4] = None,
        multi_az: typing.Optional[bool] = None,
        option_group: typing.Optional["IOptionGroup"] = None,
        performance_insight_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        performance_insight_retention: typing.Optional["PerformanceInsightRetention"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[str] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        processor_features: typing.Optional["ProcessorFeatures"] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        storage_type: typing.Optional["StorageType"] = None,
        vpc_placement: typing.Optional[_SubnetSelection_36a13cd6] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        engine: "IInstanceEngine",
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[bool] = None,
        database_name: typing.Optional[str] = None,
        instance_type: typing.Optional[_InstanceType_85a97b30] = None,
        license_model: typing.Optional["LicenseModel"] = None,
        master_user_password: typing.Optional[_SecretValue_99478b8b] = None,
        master_user_password_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        timezone: typing.Optional[str] = None,
        snapshot_identifier: str,
        generate_master_user_password: typing.Optional[bool] = None,
        master_username: typing.Optional[str] = None,
    ) -> None:
        """Construction properties for a DatabaseInstanceFromSnapshot.

        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. Default: Duration.days(1)
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: false
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: true
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_type: The storage type. Default: GP2
        :param vpc_placement: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param engine: The database engine.
        :param allocated_storage: The allocated storage size, specified in gigabytes (GB). Default: 100
        :param allow_major_version_upgrade: Whether to allow major version upgrades. Default: false
        :param database_name: The name of the database. Default: - no name
        :param instance_type: The name of the compute and memory capacity for the instance. Default: - m5.large (or, more specifically, db.m5.large)
        :param license_model: The license model. Default: - RDS default license model
        :param master_user_password: The master user password. Default: - a Secrets Manager generated password
        :param master_user_password_encryption_key: The KMS key used to encrypt the secret for the master user password. Default: - default master key
        :param parameter_group: The DB parameter group to associate with the instance. Default: - no parameter group
        :param timezone: The time zone of the instance. This is currently supported only by Microsoft Sql Server. Default: - RDS default timezone
        :param snapshot_identifier: The name or Amazon Resource Name (ARN) of the DB snapshot that's used to restore the DB instance. If you're restoring from a shared manual DB snapshot, you must specify the ARN of the snapshot.
        :param generate_master_user_password: Whether to generate a new master user password and store it in Secrets Manager. ``masterUsername`` must be specified with the **current** master user name of the snapshot when this property is set to true. Default: false
        :param master_username: The master user name. Specify this prop with the **current** master user name of the snapshot only when generating a new master user password with ``generateMasterUserPassword``. The value will be set in the generated secret attached to the instance. It is not possible to change the master user name of a RDS instance. Default: - inherited from the snapshot

        stability
        :stability: experimental
        """
        if isinstance(processor_features, dict):
            processor_features = ProcessorFeatures(**processor_features)
        if isinstance(vpc_placement, dict):
            vpc_placement = _SubnetSelection_36a13cd6(**vpc_placement)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            "vpc": vpc,
            "engine": engine,
            "snapshot_identifier": snapshot_identifier,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if backup_retention is not None:
            self._values["backup_retention"] = backup_retention
        if cloudwatch_logs_exports is not None:
            self._values["cloudwatch_logs_exports"] = cloudwatch_logs_exports
        if cloudwatch_logs_retention is not None:
            self._values["cloudwatch_logs_retention"] = cloudwatch_logs_retention
        if cloudwatch_logs_retention_role is not None:
            self._values["cloudwatch_logs_retention_role"] = cloudwatch_logs_retention_role
        if copy_tags_to_snapshot is not None:
            self._values["copy_tags_to_snapshot"] = copy_tags_to_snapshot
        if delete_automated_backups is not None:
            self._values["delete_automated_backups"] = delete_automated_backups
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if domain is not None:
            self._values["domain"] = domain
        if domain_role is not None:
            self._values["domain_role"] = domain_role
        if enable_performance_insights is not None:
            self._values["enable_performance_insights"] = enable_performance_insights
        if iam_authentication is not None:
            self._values["iam_authentication"] = iam_authentication
        if instance_identifier is not None:
            self._values["instance_identifier"] = instance_identifier
        if iops is not None:
            self._values["iops"] = iops
        if max_allocated_storage is not None:
            self._values["max_allocated_storage"] = max_allocated_storage
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_role is not None:
            self._values["monitoring_role"] = monitoring_role
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if option_group is not None:
            self._values["option_group"] = option_group
        if performance_insight_encryption_key is not None:
            self._values["performance_insight_encryption_key"] = performance_insight_encryption_key
        if performance_insight_retention is not None:
            self._values["performance_insight_retention"] = performance_insight_retention
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if processor_features is not None:
            self._values["processor_features"] = processor_features
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if vpc_placement is not None:
            self._values["vpc_placement"] = vpc_placement
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if allocated_storage is not None:
            self._values["allocated_storage"] = allocated_storage
        if allow_major_version_upgrade is not None:
            self._values["allow_major_version_upgrade"] = allow_major_version_upgrade
        if database_name is not None:
            self._values["database_name"] = database_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if license_model is not None:
            self._values["license_model"] = license_model
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password
        if master_user_password_encryption_key is not None:
            self._values["master_user_password_encryption_key"] = master_user_password_encryption_key
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if timezone is not None:
            self._values["timezone"] = timezone
        if generate_master_user_password is not None:
            self._values["generate_master_user_password"] = generate_master_user_password
        if master_username is not None:
            self._values["master_username"] = master_username

    @builtins.property
    def vpc(self) -> _IVpc_3795853f:
        """The VPC network where the DB subnet group should be created.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def auto_minor_version_upgrade(self) -> typing.Optional[bool]:
        """Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("auto_minor_version_upgrade")

    @builtins.property
    def availability_zone(self) -> typing.Optional[str]:
        """The name of the Availability Zone where the DB instance will be located.

        default
        :default: - no preference

        stability
        :stability: experimental
        """
        return self._values.get("availability_zone")

    @builtins.property
    def backup_retention(self) -> typing.Optional[_Duration_5170c158]:
        """The number of days during which automatic DB snapshots are retained.

        Set
        to zero to disable backups.

        default
        :default: Duration.days(1)

        stability
        :stability: experimental
        """
        return self._values.get("backup_retention")

    @builtins.property
    def cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """The list of log types that need to be enabled for exporting to CloudWatch Logs.

        default
        :default: - no log exports

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_exports")

    @builtins.property
    def cloudwatch_logs_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``Infinity``.

        default
        :default: - logs never expire

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_retention")

    @builtins.property
    def cloudwatch_logs_retention_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        default
        :default: - a new role is created.

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_retention_role")

    @builtins.property
    def copy_tags_to_snapshot(self) -> typing.Optional[bool]:
        """Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("copy_tags_to_snapshot")

    @builtins.property
    def delete_automated_backups(self) -> typing.Optional[bool]:
        """Indicates whether automated backups should be deleted or retained when you delete a DB instance.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("delete_automated_backups")

    @builtins.property
    def deletion_protection(self) -> typing.Optional[bool]:
        """Indicates whether the DB instance should have deletion protection enabled.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("deletion_protection")

    @builtins.property
    def domain(self) -> typing.Optional[str]:
        """The Active Directory directory ID to create the DB instance in.

        default
        :default: - Do not join domain

        stability
        :stability: experimental
        """
        return self._values.get("domain")

    @builtins.property
    def domain_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role to be used when making API calls to the Directory Service.

        The role needs the AWS-managed policy
        AmazonRDSDirectoryServiceAccess or equivalent.

        default
        :default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified

        stability
        :stability: experimental
        """
        return self._values.get("domain_role")

    @builtins.property
    def enable_performance_insights(self) -> typing.Optional[bool]:
        """Whether to enable Performance Insights for the DB instance.

        default
        :default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.

        stability
        :stability: experimental
        """
        return self._values.get("enable_performance_insights")

    @builtins.property
    def iam_authentication(self) -> typing.Optional[bool]:
        """Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("iam_authentication")

    @builtins.property
    def instance_identifier(self) -> typing.Optional[str]:
        """A name for the DB instance.

        If you specify a name, AWS CloudFormation
        converts it to lowercase.

        default
        :default: - a CloudFormation generated name

        stability
        :stability: experimental
        """
        return self._values.get("instance_identifier")

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) that the database provisions.

        The value must be equal to or greater than 1000.

        default
        :default: - no provisioned iops

        stability
        :stability: experimental
        """
        return self._values.get("iops")

    @builtins.property
    def max_allocated_storage(self) -> typing.Optional[jsii.Number]:
        """Upper limit to which RDS can scale the storage in GiB(Gibibyte).

        default
        :default: - No autoscaling of RDS instance

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling
        stability
        :stability: experimental
        """
        return self._values.get("max_allocated_storage")

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[_Duration_5170c158]:
        """The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance.

        default
        :default: - no enhanced monitoring

        stability
        :stability: experimental
        """
        return self._values.get("monitoring_interval")

    @builtins.property
    def monitoring_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that will be used to manage DB instance monitoring.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get("monitoring_role")

    @builtins.property
    def multi_az(self) -> typing.Optional[bool]:
        """Specifies if the database instance is a multiple Availability Zone deployment.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("multi_az")

    @builtins.property
    def option_group(self) -> typing.Optional["IOptionGroup"]:
        """The option group to associate with the instance.

        default
        :default: - no option group

        stability
        :stability: experimental
        """
        return self._values.get("option_group")

    @builtins.property
    def performance_insight_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The AWS KMS key for encryption of Performance Insights data.

        default
        :default: - default master key

        stability
        :stability: experimental
        """
        return self._values.get("performance_insight_encryption_key")

    @builtins.property
    def performance_insight_retention(
        self,
    ) -> typing.Optional["PerformanceInsightRetention"]:
        """The amount of time, in days, to retain Performance Insights data.

        default
        :default: 7

        stability
        :stability: experimental
        """
        return self._values.get("performance_insight_retention")

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port for the instance.

        default
        :default: - the default port for the chosen engine.

        stability
        :stability: experimental
        """
        return self._values.get("port")

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[str]:
        """The daily time range during which automated backups are performed.

        Constraints:

        - Must be in the format ``hh24:mi-hh24:mi``.
        - Must be in Universal Coordinated Time (UTC).
        - Must not conflict with the preferred maintenance window.
        - Must be at least 30 minutes.

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region. To see the time blocks available, see
          https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow

        stability
        :stability: experimental
        """
        return self._values.get("preferred_backup_window")

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """The weekly time range (in UTC) during which system maintenance can occur.

        Format: ``ddd:hh24:mi-ddd:hh24:mi``
        Constraint: Minimum 30-minute window

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region, occurring on a random day of the week. To see
          the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance

        stability
        :stability: experimental
        """
        return self._values.get("preferred_maintenance_window")

    @builtins.property
    def processor_features(self) -> typing.Optional["ProcessorFeatures"]:
        """The number of CPU cores and the number of threads per core.

        default
        :default:

        - the default number of CPU cores and threads per core for the
          chosen instance class.

        See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor

        stability
        :stability: experimental
        """
        return self._values.get("processor_features")

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update.

        default
        :default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)

        stability
        :stability: experimental
        """
        return self._values.get("removal_policy")

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The security groups to assign to the DB instance.

        default
        :default: - a new security group is created

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    @builtins.property
    def storage_type(self) -> typing.Optional["StorageType"]:
        """The storage type.

        default
        :default: GP2

        stability
        :stability: experimental
        """
        return self._values.get("storage_type")

    @builtins.property
    def vpc_placement(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The type of subnets to add to the created DB subnet group.

        default
        :default: - private subnets

        deprecated
        :deprecated: use ``vpcSubnets``

        stability
        :stability: deprecated
        """
        return self._values.get("vpc_placement")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The type of subnets to add to the created DB subnet group.

        default
        :default: - private subnets

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    @builtins.property
    def engine(self) -> "IInstanceEngine":
        """The database engine.

        stability
        :stability: experimental
        """
        return self._values.get("engine")

    @builtins.property
    def allocated_storage(self) -> typing.Optional[jsii.Number]:
        """The allocated storage size, specified in gigabytes (GB).

        default
        :default: 100

        stability
        :stability: experimental
        """
        return self._values.get("allocated_storage")

    @builtins.property
    def allow_major_version_upgrade(self) -> typing.Optional[bool]:
        """Whether to allow major version upgrades.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("allow_major_version_upgrade")

    @builtins.property
    def database_name(self) -> typing.Optional[str]:
        """The name of the database.

        default
        :default: - no name

        stability
        :stability: experimental
        """
        return self._values.get("database_name")

    @builtins.property
    def instance_type(self) -> typing.Optional[_InstanceType_85a97b30]:
        """The name of the compute and memory capacity for the instance.

        default
        :default: - m5.large (or, more specifically, db.m5.large)

        stability
        :stability: experimental
        """
        return self._values.get("instance_type")

    @builtins.property
    def license_model(self) -> typing.Optional["LicenseModel"]:
        """The license model.

        default
        :default: - RDS default license model

        stability
        :stability: experimental
        """
        return self._values.get("license_model")

    @builtins.property
    def master_user_password(self) -> typing.Optional[_SecretValue_99478b8b]:
        """The master user password.

        default
        :default: - a Secrets Manager generated password

        stability
        :stability: experimental
        """
        return self._values.get("master_user_password")

    @builtins.property
    def master_user_password_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The KMS key used to encrypt the secret for the master user password.

        default
        :default: - default master key

        stability
        :stability: experimental
        """
        return self._values.get("master_user_password_encryption_key")

    @builtins.property
    def parameter_group(self) -> typing.Optional["IParameterGroup"]:
        """The DB parameter group to associate with the instance.

        default
        :default: - no parameter group

        stability
        :stability: experimental
        """
        return self._values.get("parameter_group")

    @builtins.property
    def timezone(self) -> typing.Optional[str]:
        """The time zone of the instance.

        This is currently supported only by Microsoft Sql Server.

        default
        :default: - RDS default timezone

        stability
        :stability: experimental
        """
        return self._values.get("timezone")

    @builtins.property
    def snapshot_identifier(self) -> str:
        """The name or Amazon Resource Name (ARN) of the DB snapshot that's used to restore the DB instance.

        If you're restoring from a shared manual DB
        snapshot, you must specify the ARN of the snapshot.

        stability
        :stability: experimental
        """
        return self._values.get("snapshot_identifier")

    @builtins.property
    def generate_master_user_password(self) -> typing.Optional[bool]:
        """Whether to generate a new master user password and store it in Secrets Manager.

        ``masterUsername`` must be specified with the **current**
        master user name of the snapshot when this property is set to true.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("generate_master_user_password")

    @builtins.property
    def master_username(self) -> typing.Optional[str]:
        """The master user name.

        Specify this prop with the **current** master user name of the snapshot
        only when generating a new master user password with ``generateMasterUserPassword``.
        The value will be set in the generated secret attached to the instance.

        It is not possible to change the master user name of a RDS instance.

        default
        :default: - inherited from the snapshot

        stability
        :stability: experimental
        """
        return self._values.get("master_username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseInstanceFromSnapshotProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_rds.DatabaseInstanceProps",
    jsii_struct_bases=[DatabaseInstanceSourceProps],
    name_mapping={
        "vpc": "vpc",
        "auto_minor_version_upgrade": "autoMinorVersionUpgrade",
        "availability_zone": "availabilityZone",
        "backup_retention": "backupRetention",
        "cloudwatch_logs_exports": "cloudwatchLogsExports",
        "cloudwatch_logs_retention": "cloudwatchLogsRetention",
        "cloudwatch_logs_retention_role": "cloudwatchLogsRetentionRole",
        "copy_tags_to_snapshot": "copyTagsToSnapshot",
        "delete_automated_backups": "deleteAutomatedBackups",
        "deletion_protection": "deletionProtection",
        "domain": "domain",
        "domain_role": "domainRole",
        "enable_performance_insights": "enablePerformanceInsights",
        "iam_authentication": "iamAuthentication",
        "instance_identifier": "instanceIdentifier",
        "iops": "iops",
        "max_allocated_storage": "maxAllocatedStorage",
        "monitoring_interval": "monitoringInterval",
        "monitoring_role": "monitoringRole",
        "multi_az": "multiAz",
        "option_group": "optionGroup",
        "performance_insight_encryption_key": "performanceInsightEncryptionKey",
        "performance_insight_retention": "performanceInsightRetention",
        "port": "port",
        "preferred_backup_window": "preferredBackupWindow",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "processor_features": "processorFeatures",
        "removal_policy": "removalPolicy",
        "security_groups": "securityGroups",
        "storage_type": "storageType",
        "vpc_placement": "vpcPlacement",
        "vpc_subnets": "vpcSubnets",
        "engine": "engine",
        "allocated_storage": "allocatedStorage",
        "allow_major_version_upgrade": "allowMajorVersionUpgrade",
        "database_name": "databaseName",
        "instance_type": "instanceType",
        "license_model": "licenseModel",
        "master_user_password": "masterUserPassword",
        "master_user_password_encryption_key": "masterUserPasswordEncryptionKey",
        "parameter_group": "parameterGroup",
        "timezone": "timezone",
        "master_username": "masterUsername",
        "character_set_name": "characterSetName",
        "storage_encrypted": "storageEncrypted",
        "storage_encryption_key": "storageEncryptionKey",
    },
)
class DatabaseInstanceProps(DatabaseInstanceSourceProps):
    def __init__(
        self,
        *,
        vpc: _IVpc_3795853f,
        auto_minor_version_upgrade: typing.Optional[bool] = None,
        availability_zone: typing.Optional[str] = None,
        backup_retention: typing.Optional[_Duration_5170c158] = None,
        cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        cloudwatch_logs_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        cloudwatch_logs_retention_role: typing.Optional[_IRole_e69bbae4] = None,
        copy_tags_to_snapshot: typing.Optional[bool] = None,
        delete_automated_backups: typing.Optional[bool] = None,
        deletion_protection: typing.Optional[bool] = None,
        domain: typing.Optional[str] = None,
        domain_role: typing.Optional[_IRole_e69bbae4] = None,
        enable_performance_insights: typing.Optional[bool] = None,
        iam_authentication: typing.Optional[bool] = None,
        instance_identifier: typing.Optional[str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[_Duration_5170c158] = None,
        monitoring_role: typing.Optional[_IRole_e69bbae4] = None,
        multi_az: typing.Optional[bool] = None,
        option_group: typing.Optional["IOptionGroup"] = None,
        performance_insight_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        performance_insight_retention: typing.Optional["PerformanceInsightRetention"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[str] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        processor_features: typing.Optional["ProcessorFeatures"] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        storage_type: typing.Optional["StorageType"] = None,
        vpc_placement: typing.Optional[_SubnetSelection_36a13cd6] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        engine: "IInstanceEngine",
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[bool] = None,
        database_name: typing.Optional[str] = None,
        instance_type: typing.Optional[_InstanceType_85a97b30] = None,
        license_model: typing.Optional["LicenseModel"] = None,
        master_user_password: typing.Optional[_SecretValue_99478b8b] = None,
        master_user_password_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        timezone: typing.Optional[str] = None,
        master_username: str,
        character_set_name: typing.Optional[str] = None,
        storage_encrypted: typing.Optional[bool] = None,
        storage_encryption_key: typing.Optional[_IKey_3336c79d] = None,
    ) -> None:
        """Construction properties for a DatabaseInstance.

        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. Default: Duration.days(1)
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: false
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: true
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_type: The storage type. Default: GP2
        :param vpc_placement: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param engine: The database engine.
        :param allocated_storage: The allocated storage size, specified in gigabytes (GB). Default: 100
        :param allow_major_version_upgrade: Whether to allow major version upgrades. Default: false
        :param database_name: The name of the database. Default: - no name
        :param instance_type: The name of the compute and memory capacity for the instance. Default: - m5.large (or, more specifically, db.m5.large)
        :param license_model: The license model. Default: - RDS default license model
        :param master_user_password: The master user password. Default: - a Secrets Manager generated password
        :param master_user_password_encryption_key: The KMS key used to encrypt the secret for the master user password. Default: - default master key
        :param parameter_group: The DB parameter group to associate with the instance. Default: - no parameter group
        :param timezone: The time zone of the instance. This is currently supported only by Microsoft Sql Server. Default: - RDS default timezone
        :param master_username: The master user name.
        :param character_set_name: For supported engines, specifies the character set to associate with the DB instance. Default: - RDS default character set name
        :param storage_encrypted: Indicates whether the DB instance is encrypted. Default: - true if storageEncryptionKey has been provided, false otherwise
        :param storage_encryption_key: The KMS key that's used to encrypt the DB instance. Default: - default master key if storageEncrypted is true, no key otherwise

        stability
        :stability: experimental
        """
        if isinstance(processor_features, dict):
            processor_features = ProcessorFeatures(**processor_features)
        if isinstance(vpc_placement, dict):
            vpc_placement = _SubnetSelection_36a13cd6(**vpc_placement)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {
            "vpc": vpc,
            "engine": engine,
            "master_username": master_username,
        }
        if auto_minor_version_upgrade is not None:
            self._values["auto_minor_version_upgrade"] = auto_minor_version_upgrade
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if backup_retention is not None:
            self._values["backup_retention"] = backup_retention
        if cloudwatch_logs_exports is not None:
            self._values["cloudwatch_logs_exports"] = cloudwatch_logs_exports
        if cloudwatch_logs_retention is not None:
            self._values["cloudwatch_logs_retention"] = cloudwatch_logs_retention
        if cloudwatch_logs_retention_role is not None:
            self._values["cloudwatch_logs_retention_role"] = cloudwatch_logs_retention_role
        if copy_tags_to_snapshot is not None:
            self._values["copy_tags_to_snapshot"] = copy_tags_to_snapshot
        if delete_automated_backups is not None:
            self._values["delete_automated_backups"] = delete_automated_backups
        if deletion_protection is not None:
            self._values["deletion_protection"] = deletion_protection
        if domain is not None:
            self._values["domain"] = domain
        if domain_role is not None:
            self._values["domain_role"] = domain_role
        if enable_performance_insights is not None:
            self._values["enable_performance_insights"] = enable_performance_insights
        if iam_authentication is not None:
            self._values["iam_authentication"] = iam_authentication
        if instance_identifier is not None:
            self._values["instance_identifier"] = instance_identifier
        if iops is not None:
            self._values["iops"] = iops
        if max_allocated_storage is not None:
            self._values["max_allocated_storage"] = max_allocated_storage
        if monitoring_interval is not None:
            self._values["monitoring_interval"] = monitoring_interval
        if monitoring_role is not None:
            self._values["monitoring_role"] = monitoring_role
        if multi_az is not None:
            self._values["multi_az"] = multi_az
        if option_group is not None:
            self._values["option_group"] = option_group
        if performance_insight_encryption_key is not None:
            self._values["performance_insight_encryption_key"] = performance_insight_encryption_key
        if performance_insight_retention is not None:
            self._values["performance_insight_retention"] = performance_insight_retention
        if port is not None:
            self._values["port"] = port
        if preferred_backup_window is not None:
            self._values["preferred_backup_window"] = preferred_backup_window
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if processor_features is not None:
            self._values["processor_features"] = processor_features
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if storage_type is not None:
            self._values["storage_type"] = storage_type
        if vpc_placement is not None:
            self._values["vpc_placement"] = vpc_placement
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if allocated_storage is not None:
            self._values["allocated_storage"] = allocated_storage
        if allow_major_version_upgrade is not None:
            self._values["allow_major_version_upgrade"] = allow_major_version_upgrade
        if database_name is not None:
            self._values["database_name"] = database_name
        if instance_type is not None:
            self._values["instance_type"] = instance_type
        if license_model is not None:
            self._values["license_model"] = license_model
        if master_user_password is not None:
            self._values["master_user_password"] = master_user_password
        if master_user_password_encryption_key is not None:
            self._values["master_user_password_encryption_key"] = master_user_password_encryption_key
        if parameter_group is not None:
            self._values["parameter_group"] = parameter_group
        if timezone is not None:
            self._values["timezone"] = timezone
        if character_set_name is not None:
            self._values["character_set_name"] = character_set_name
        if storage_encrypted is not None:
            self._values["storage_encrypted"] = storage_encrypted
        if storage_encryption_key is not None:
            self._values["storage_encryption_key"] = storage_encryption_key

    @builtins.property
    def vpc(self) -> _IVpc_3795853f:
        """The VPC network where the DB subnet group should be created.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def auto_minor_version_upgrade(self) -> typing.Optional[bool]:
        """Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("auto_minor_version_upgrade")

    @builtins.property
    def availability_zone(self) -> typing.Optional[str]:
        """The name of the Availability Zone where the DB instance will be located.

        default
        :default: - no preference

        stability
        :stability: experimental
        """
        return self._values.get("availability_zone")

    @builtins.property
    def backup_retention(self) -> typing.Optional[_Duration_5170c158]:
        """The number of days during which automatic DB snapshots are retained.

        Set
        to zero to disable backups.

        default
        :default: Duration.days(1)

        stability
        :stability: experimental
        """
        return self._values.get("backup_retention")

    @builtins.property
    def cloudwatch_logs_exports(self) -> typing.Optional[typing.List[str]]:
        """The list of log types that need to be enabled for exporting to CloudWatch Logs.

        default
        :default: - no log exports

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_exports")

    @builtins.property
    def cloudwatch_logs_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``Infinity``.

        default
        :default: - logs never expire

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_retention")

    @builtins.property
    def cloudwatch_logs_retention_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        default
        :default: - a new role is created.

        stability
        :stability: experimental
        """
        return self._values.get("cloudwatch_logs_retention_role")

    @builtins.property
    def copy_tags_to_snapshot(self) -> typing.Optional[bool]:
        """Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("copy_tags_to_snapshot")

    @builtins.property
    def delete_automated_backups(self) -> typing.Optional[bool]:
        """Indicates whether automated backups should be deleted or retained when you delete a DB instance.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("delete_automated_backups")

    @builtins.property
    def deletion_protection(self) -> typing.Optional[bool]:
        """Indicates whether the DB instance should have deletion protection enabled.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("deletion_protection")

    @builtins.property
    def domain(self) -> typing.Optional[str]:
        """The Active Directory directory ID to create the DB instance in.

        default
        :default: - Do not join domain

        stability
        :stability: experimental
        """
        return self._values.get("domain")

    @builtins.property
    def domain_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role to be used when making API calls to the Directory Service.

        The role needs the AWS-managed policy
        AmazonRDSDirectoryServiceAccess or equivalent.

        default
        :default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified

        stability
        :stability: experimental
        """
        return self._values.get("domain_role")

    @builtins.property
    def enable_performance_insights(self) -> typing.Optional[bool]:
        """Whether to enable Performance Insights for the DB instance.

        default
        :default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.

        stability
        :stability: experimental
        """
        return self._values.get("enable_performance_insights")

    @builtins.property
    def iam_authentication(self) -> typing.Optional[bool]:
        """Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("iam_authentication")

    @builtins.property
    def instance_identifier(self) -> typing.Optional[str]:
        """A name for the DB instance.

        If you specify a name, AWS CloudFormation
        converts it to lowercase.

        default
        :default: - a CloudFormation generated name

        stability
        :stability: experimental
        """
        return self._values.get("instance_identifier")

    @builtins.property
    def iops(self) -> typing.Optional[jsii.Number]:
        """The number of I/O operations per second (IOPS) that the database provisions.

        The value must be equal to or greater than 1000.

        default
        :default: - no provisioned iops

        stability
        :stability: experimental
        """
        return self._values.get("iops")

    @builtins.property
    def max_allocated_storage(self) -> typing.Optional[jsii.Number]:
        """Upper limit to which RDS can scale the storage in GiB(Gibibyte).

        default
        :default: - No autoscaling of RDS instance

        see
        :see: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIOPS.StorageTypes.html#USER_PIOPS.Autoscaling
        stability
        :stability: experimental
        """
        return self._values.get("max_allocated_storage")

    @builtins.property
    def monitoring_interval(self) -> typing.Optional[_Duration_5170c158]:
        """The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance.

        default
        :default: - no enhanced monitoring

        stability
        :stability: experimental
        """
        return self._values.get("monitoring_interval")

    @builtins.property
    def monitoring_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Role that will be used to manage DB instance monitoring.

        default
        :default: - A role is automatically created for you

        stability
        :stability: experimental
        """
        return self._values.get("monitoring_role")

    @builtins.property
    def multi_az(self) -> typing.Optional[bool]:
        """Specifies if the database instance is a multiple Availability Zone deployment.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("multi_az")

    @builtins.property
    def option_group(self) -> typing.Optional["IOptionGroup"]:
        """The option group to associate with the instance.

        default
        :default: - no option group

        stability
        :stability: experimental
        """
        return self._values.get("option_group")

    @builtins.property
    def performance_insight_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The AWS KMS key for encryption of Performance Insights data.

        default
        :default: - default master key

        stability
        :stability: experimental
        """
        return self._values.get("performance_insight_encryption_key")

    @builtins.property
    def performance_insight_retention(
        self,
    ) -> typing.Optional["PerformanceInsightRetention"]:
        """The amount of time, in days, to retain Performance Insights data.

        default
        :default: 7

        stability
        :stability: experimental
        """
        return self._values.get("performance_insight_retention")

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port for the instance.

        default
        :default: - the default port for the chosen engine.

        stability
        :stability: experimental
        """
        return self._values.get("port")

    @builtins.property
    def preferred_backup_window(self) -> typing.Optional[str]:
        """The daily time range during which automated backups are performed.

        Constraints:

        - Must be in the format ``hh24:mi-hh24:mi``.
        - Must be in Universal Coordinated Time (UTC).
        - Must not conflict with the preferred maintenance window.
        - Must be at least 30 minutes.

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region. To see the time blocks available, see
          https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow

        stability
        :stability: experimental
        """
        return self._values.get("preferred_backup_window")

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[str]:
        """The weekly time range (in UTC) during which system maintenance can occur.

        Format: ``ddd:hh24:mi-ddd:hh24:mi``
        Constraint: Minimum 30-minute window

        default
        :default:

        - a 30-minute window selected at random from an 8-hour block of
          time for each AWS Region, occurring on a random day of the week. To see
          the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance

        stability
        :stability: experimental
        """
        return self._values.get("preferred_maintenance_window")

    @builtins.property
    def processor_features(self) -> typing.Optional["ProcessorFeatures"]:
        """The number of CPU cores and the number of threads per core.

        default
        :default:

        - the default number of CPU cores and threads per core for the
          chosen instance class.

        See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor

        stability
        :stability: experimental
        """
        return self._values.get("processor_features")

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_5986e9f3]:
        """The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update.

        default
        :default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)

        stability
        :stability: experimental
        """
        return self._values.get("removal_policy")

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The security groups to assign to the DB instance.

        default
        :default: - a new security group is created

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    @builtins.property
    def storage_type(self) -> typing.Optional["StorageType"]:
        """The storage type.

        default
        :default: GP2

        stability
        :stability: experimental
        """
        return self._values.get("storage_type")

    @builtins.property
    def vpc_placement(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The type of subnets to add to the created DB subnet group.

        default
        :default: - private subnets

        deprecated
        :deprecated: use ``vpcSubnets``

        stability
        :stability: deprecated
        """
        return self._values.get("vpc_placement")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """The type of subnets to add to the created DB subnet group.

        default
        :default: - private subnets

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    @builtins.property
    def engine(self) -> "IInstanceEngine":
        """The database engine.

        stability
        :stability: experimental
        """
        return self._values.get("engine")

    @builtins.property
    def allocated_storage(self) -> typing.Optional[jsii.Number]:
        """The allocated storage size, specified in gigabytes (GB).

        default
        :default: 100

        stability
        :stability: experimental
        """
        return self._values.get("allocated_storage")

    @builtins.property
    def allow_major_version_upgrade(self) -> typing.Optional[bool]:
        """Whether to allow major version upgrades.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("allow_major_version_upgrade")

    @builtins.property
    def database_name(self) -> typing.Optional[str]:
        """The name of the database.

        default
        :default: - no name

        stability
        :stability: experimental
        """
        return self._values.get("database_name")

    @builtins.property
    def instance_type(self) -> typing.Optional[_InstanceType_85a97b30]:
        """The name of the compute and memory capacity for the instance.

        default
        :default: - m5.large (or, more specifically, db.m5.large)

        stability
        :stability: experimental
        """
        return self._values.get("instance_type")

    @builtins.property
    def license_model(self) -> typing.Optional["LicenseModel"]:
        """The license model.

        default
        :default: - RDS default license model

        stability
        :stability: experimental
        """
        return self._values.get("license_model")

    @builtins.property
    def master_user_password(self) -> typing.Optional[_SecretValue_99478b8b]:
        """The master user password.

        default
        :default: - a Secrets Manager generated password

        stability
        :stability: experimental
        """
        return self._values.get("master_user_password")

    @builtins.property
    def master_user_password_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The KMS key used to encrypt the secret for the master user password.

        default
        :default: - default master key

        stability
        :stability: experimental
        """
        return self._values.get("master_user_password_encryption_key")

    @builtins.property
    def parameter_group(self) -> typing.Optional["IParameterGroup"]:
        """The DB parameter group to associate with the instance.

        default
        :default: - no parameter group

        stability
        :stability: experimental
        """
        return self._values.get("parameter_group")

    @builtins.property
    def timezone(self) -> typing.Optional[str]:
        """The time zone of the instance.

        This is currently supported only by Microsoft Sql Server.

        default
        :default: - RDS default timezone

        stability
        :stability: experimental
        """
        return self._values.get("timezone")

    @builtins.property
    def master_username(self) -> str:
        """The master user name.

        stability
        :stability: experimental
        """
        return self._values.get("master_username")

    @builtins.property
    def character_set_name(self) -> typing.Optional[str]:
        """For supported engines, specifies the character set to associate with the DB instance.

        default
        :default: - RDS default character set name

        stability
        :stability: experimental
        """
        return self._values.get("character_set_name")

    @builtins.property
    def storage_encrypted(self) -> typing.Optional[bool]:
        """Indicates whether the DB instance is encrypted.

        default
        :default: - true if storageEncryptionKey has been provided, false otherwise

        stability
        :stability: experimental
        """
        return self._values.get("storage_encrypted")

    @builtins.property
    def storage_encryption_key(self) -> typing.Optional[_IKey_3336c79d]:
        """The KMS key that's used to encrypt the DB instance.

        default
        :default: - default master key if storageEncrypted is true, no key otherwise

        stability
        :stability: experimental
        """
        return self._values.get("storage_encryption_key")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DatabaseInstanceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDatabaseInstance)
class DatabaseInstanceReadReplica(
    DatabaseInstanceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.DatabaseInstanceReadReplica",
):
    """A read replica database instance.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::RDS::DBInstance
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        instance_type: _InstanceType_85a97b30,
        source_database_instance: "IDatabaseInstance",
        storage_encrypted: typing.Optional[bool] = None,
        storage_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        vpc: _IVpc_3795853f,
        auto_minor_version_upgrade: typing.Optional[bool] = None,
        availability_zone: typing.Optional[str] = None,
        backup_retention: typing.Optional[_Duration_5170c158] = None,
        cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        cloudwatch_logs_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        cloudwatch_logs_retention_role: typing.Optional[_IRole_e69bbae4] = None,
        copy_tags_to_snapshot: typing.Optional[bool] = None,
        delete_automated_backups: typing.Optional[bool] = None,
        deletion_protection: typing.Optional[bool] = None,
        domain: typing.Optional[str] = None,
        domain_role: typing.Optional[_IRole_e69bbae4] = None,
        enable_performance_insights: typing.Optional[bool] = None,
        iam_authentication: typing.Optional[bool] = None,
        instance_identifier: typing.Optional[str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[_Duration_5170c158] = None,
        monitoring_role: typing.Optional[_IRole_e69bbae4] = None,
        multi_az: typing.Optional[bool] = None,
        option_group: typing.Optional["IOptionGroup"] = None,
        performance_insight_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        performance_insight_retention: typing.Optional["PerformanceInsightRetention"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[str] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        processor_features: typing.Optional["ProcessorFeatures"] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        storage_type: typing.Optional["StorageType"] = None,
        vpc_placement: typing.Optional[_SubnetSelection_36a13cd6] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param instance_type: The name of the compute and memory capacity classes.
        :param source_database_instance: The source database instance. Each DB instance can have a limited number of read replicas. For more information, see https://docs.aws.amazon.com/AmazonRDS/latest/DeveloperGuide/USER_ReadRepl.html.
        :param storage_encrypted: Indicates whether the DB instance is encrypted. Default: - true if storageEncryptionKey has been provided, false otherwise
        :param storage_encryption_key: The KMS key that's used to encrypt the DB instance. Default: - default master key if storageEncrypted is true, no key otherwise
        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. Default: Duration.days(1)
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: false
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: true
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_type: The storage type. Default: GP2
        :param vpc_placement: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets

        stability
        :stability: experimental
        """
        props = DatabaseInstanceReadReplicaProps(
            instance_type=instance_type,
            source_database_instance=source_database_instance,
            storage_encrypted=storage_encrypted,
            storage_encryption_key=storage_encryption_key,
            vpc=vpc,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            availability_zone=availability_zone,
            backup_retention=backup_retention,
            cloudwatch_logs_exports=cloudwatch_logs_exports,
            cloudwatch_logs_retention=cloudwatch_logs_retention,
            cloudwatch_logs_retention_role=cloudwatch_logs_retention_role,
            copy_tags_to_snapshot=copy_tags_to_snapshot,
            delete_automated_backups=delete_automated_backups,
            deletion_protection=deletion_protection,
            domain=domain,
            domain_role=domain_role,
            enable_performance_insights=enable_performance_insights,
            iam_authentication=iam_authentication,
            instance_identifier=instance_identifier,
            iops=iops,
            max_allocated_storage=max_allocated_storage,
            monitoring_interval=monitoring_interval,
            monitoring_role=monitoring_role,
            multi_az=multi_az,
            option_group=option_group,
            performance_insight_encryption_key=performance_insight_encryption_key,
            performance_insight_retention=performance_insight_retention,
            port=port,
            preferred_backup_window=preferred_backup_window,
            preferred_maintenance_window=preferred_maintenance_window,
            processor_features=processor_features,
            removal_policy=removal_policy,
            security_groups=security_groups,
            storage_type=storage_type,
            vpc_placement=vpc_placement,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(DatabaseInstanceReadReplica, self, [scope, id, props])

    @jsii.member(jsii_name="setLogRetention")
    def _set_log_retention(self) -> None:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "setLogRetention", [])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Access to network connections.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> str:
        """The instance endpoint address.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dbInstanceEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> str:
        """The instance endpoint port.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dbInstanceEndpointPort")

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> "Endpoint":
        """The instance endpoint.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceEndpoint")

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> str:
        """The instance identifier.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceIdentifier")

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def _instance_type(self) -> _InstanceType_85a97b30:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceType")

    @builtins.property
    @jsii.member(jsii_name="newCfnProps")
    def _new_cfn_props(self) -> "CfnDBInstanceProps":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "newCfnProps")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC where this database instance is deployed.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")

    @builtins.property
    @jsii.member(jsii_name="vpcPlacement")
    def _vpc_placement(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "vpcPlacement")

    @builtins.property
    @jsii.member(jsii_name="enableIamAuthentication")
    def _enable_iam_authentication(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "enableIamAuthentication")

    @_enable_iam_authentication.setter
    def _enable_iam_authentication(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "enableIamAuthentication", value)


@jsii.implements(IDatabaseProxy, _IConnectable_a587039f, _ISecretAttachmentTarget_0a569782)
class DatabaseProxy(
    _Resource_884d0774,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.DatabaseProxy",
):
    """RDS Database Proxy.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::RDS::DBProxy
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        proxy_target: "ProxyTarget",
        secrets: typing.List[_ISecret_75279d36],
        vpc: _IVpc_3795853f,
        borrow_timeout: typing.Optional[_Duration_5170c158] = None,
        db_proxy_name: typing.Optional[str] = None,
        debug_logging: typing.Optional[bool] = None,
        iam_auth: typing.Optional[bool] = None,
        idle_client_timeout: typing.Optional[_Duration_5170c158] = None,
        init_query: typing.Optional[str] = None,
        max_connections_percent: typing.Optional[jsii.Number] = None,
        max_idle_connections_percent: typing.Optional[jsii.Number] = None,
        require_tls: typing.Optional[bool] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        session_pinning_filters: typing.Optional[typing.List["SessionPinningFilter"]] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param proxy_target: DB proxy target: Instance or Cluster.
        :param secrets: The secret that the proxy uses to authenticate to the RDS DB instance or Aurora DB cluster. These secrets are stored within Amazon Secrets Manager. One or more secrets are required.
        :param vpc: The VPC to associate with the new proxy.
        :param borrow_timeout: The duration for a proxy to wait for a connection to become available in the connection pool. Only applies when the proxy has opened its maximum number of connections and all connections are busy with client sessions. Value must be between 1 second and 1 hour, or ``Duration.seconds(0)`` to represent unlimited. Default: cdk.Duration.seconds(120)
        :param db_proxy_name: The identifier for the proxy. This name must be unique for all proxies owned by your AWS account in the specified AWS Region. An identifier must begin with a letter and must contain only ASCII letters, digits, and hyphens; it can't end with a hyphen or contain two consecutive hyphens. Default: - Generated by CloudFormation (recommended)
        :param debug_logging: Whether the proxy includes detailed information about SQL statements in its logs. This information helps you to debug issues involving SQL behavior or the performance and scalability of the proxy connections. The debug information includes the text of SQL statements that you submit through the proxy. Thus, only enable this setting when needed for debugging, and only when you have security measures in place to safeguard any sensitive information that appears in the logs. Default: false
        :param iam_auth: Whether to require or disallow AWS Identity and Access Management (IAM) authentication for connections to the proxy. Default: false
        :param idle_client_timeout: The number of seconds that a connection to the proxy can be inactive before the proxy disconnects it. You can set this value higher or lower than the connection timeout limit for the associated database. Default: cdk.Duration.minutes(30)
        :param init_query: One or more SQL statements for the proxy to run when opening each new database connection. Typically used with SET statements to make sure that each connection has identical settings such as time zone and character set. For multiple statements, use semicolons as the separator. You can also include multiple variables in a single SET statement, such as SET x=1, y=2. not currently supported for PostgreSQL. Default: - no initialization query
        :param max_connections_percent: The maximum size of the connection pool for each target in a target group. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. 1-100 Default: 100
        :param max_idle_connections_percent: Controls how actively the proxy closes idle database connections in the connection pool. A high value enables the proxy to leave a high percentage of idle connections open. A low value causes the proxy to close idle client connections and return the underlying database connections to the connection pool. For Aurora MySQL, it is expressed as a percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group. between 0 and MaxConnectionsPercent Default: 50
        :param require_tls: A Boolean parameter that specifies whether Transport Layer Security (TLS) encryption is required for connections to the proxy. By enabling this setting, you can enforce encrypted TLS connections to the proxy. Default: true
        :param role: IAM role that the proxy uses to access secrets in AWS Secrets Manager. Default: - A role will automatically be created
        :param security_groups: One or more VPC security groups to associate with the new proxy. Default: - No security groups
        :param session_pinning_filters: Each item in the list represents a class of SQL operations that normally cause all later statements in a session using a proxy to be pinned to the same underlying database connection. Including an item in the list exempts that class of SQL operations from the pinning behavior. Default: - no session pinning filters
        :param vpc_subnets: The subnets used by the proxy. Default: - the VPC default strategy if not specified.

        stability
        :stability: experimental
        """
        props = DatabaseProxyProps(
            proxy_target=proxy_target,
            secrets=secrets,
            vpc=vpc,
            borrow_timeout=borrow_timeout,
            db_proxy_name=db_proxy_name,
            debug_logging=debug_logging,
            iam_auth=iam_auth,
            idle_client_timeout=idle_client_timeout,
            init_query=init_query,
            max_connections_percent=max_connections_percent,
            max_idle_connections_percent=max_idle_connections_percent,
            require_tls=require_tls,
            role=role,
            security_groups=security_groups,
            session_pinning_filters=session_pinning_filters,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(DatabaseProxy, self, [scope, id, props])

    @jsii.member(jsii_name="fromDatabaseProxyAttributes")
    @builtins.classmethod
    def from_database_proxy_attributes(
        cls,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        db_proxy_arn: str,
        db_proxy_name: str,
        endpoint: str,
        security_groups: typing.List[_ISecurityGroup_d72ab8e8],
    ) -> "IDatabaseProxy":
        """Import an existing database proxy.

        :param scope: -
        :param id: -
        :param db_proxy_arn: DB Proxy ARN.
        :param db_proxy_name: DB Proxy Name.
        :param endpoint: Endpoint.
        :param security_groups: The security groups of the instance.

        stability
        :stability: experimental
        """
        attrs = DatabaseProxyAttributes(
            db_proxy_arn=db_proxy_arn,
            db_proxy_name=db_proxy_name,
            endpoint=endpoint,
            security_groups=security_groups,
        )

        return jsii.sinvoke(cls, "fromDatabaseProxyAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> _SecretAttachmentTargetProps_b948cd13:
        """Renders the secret attachment target specifications.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "asSecretAttachmentTarget", [])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Access to network connections.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="dbProxyArn")
    def db_proxy_arn(self) -> str:
        """DB Proxy ARN.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "dbProxyArn")

    @builtins.property
    @jsii.member(jsii_name="dbProxyName")
    def db_proxy_name(self) -> str:
        """DB Proxy Name.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "dbProxyName")

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> str:
        """Endpoint.

        stability
        :stability: experimental
        attribute:
        :attribute:: true
        """
        return jsii.get(self, "endpoint")


@jsii.interface(jsii_type="monocdk-experiment.aws_rds.IClusterEngine")
class IClusterEngine(IEngine, jsii.compat.Protocol):
    """The interface representing a database cluster (as opposed to instance) engine.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IClusterEngineProxy

    @builtins.property
    @jsii.member(jsii_name="multiUserRotationApplication")
    def multi_user_rotation_application(self) -> _SecretRotationApplication_5d71a263:
        """The application used by this engine to perform rotation for a multi-user scenario.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="singleUserRotationApplication")
    def single_user_rotation_application(self) -> _SecretRotationApplication_5d71a263:
        """The application used by this engine to perform rotation for a single-user scenario.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="supportedLogTypes")
    def supported_log_types(self) -> typing.List[str]:
        """The log types that are available with this engine type.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="bindToCluster")
    def bind_to_cluster(
        self,
        scope: _Construct_f50a3f53,
        *,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        s3_export_role: typing.Optional[_IRole_e69bbae4] = None,
        s3_import_role: typing.Optional[_IRole_e69bbae4] = None,
    ) -> "ClusterEngineConfig":
        """Method called when the engine is used to create a new cluster.

        :param scope: -
        :param parameter_group: The customer-provided ParameterGroup. Default: - none
        :param s3_export_role: The role used for S3 exporting. Default: - none
        :param s3_import_role: The role used for S3 importing. Default: - none

        stability
        :stability: experimental
        """
        ...


class _IClusterEngineProxy(jsii.proxy_for(IEngine)):
    """The interface representing a database cluster (as opposed to instance) engine.

    stability
    :stability: experimental
    """

    __jsii_type__ = "monocdk-experiment.aws_rds.IClusterEngine"

    @builtins.property
    @jsii.member(jsii_name="multiUserRotationApplication")
    def multi_user_rotation_application(self) -> _SecretRotationApplication_5d71a263:
        """The application used by this engine to perform rotation for a multi-user scenario.

        stability
        :stability: experimental
        """
        return jsii.get(self, "multiUserRotationApplication")

    @builtins.property
    @jsii.member(jsii_name="singleUserRotationApplication")
    def single_user_rotation_application(self) -> _SecretRotationApplication_5d71a263:
        """The application used by this engine to perform rotation for a single-user scenario.

        stability
        :stability: experimental
        """
        return jsii.get(self, "singleUserRotationApplication")

    @builtins.property
    @jsii.member(jsii_name="supportedLogTypes")
    def supported_log_types(self) -> typing.List[str]:
        """The log types that are available with this engine type.

        stability
        :stability: experimental
        """
        return jsii.get(self, "supportedLogTypes")

    @jsii.member(jsii_name="bindToCluster")
    def bind_to_cluster(
        self,
        scope: _Construct_f50a3f53,
        *,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        s3_export_role: typing.Optional[_IRole_e69bbae4] = None,
        s3_import_role: typing.Optional[_IRole_e69bbae4] = None,
    ) -> "ClusterEngineConfig":
        """Method called when the engine is used to create a new cluster.

        :param scope: -
        :param parameter_group: The customer-provided ParameterGroup. Default: - none
        :param s3_export_role: The role used for S3 exporting. Default: - none
        :param s3_import_role: The role used for S3 importing. Default: - none

        stability
        :stability: experimental
        """
        options = ClusterEngineBindOptions(
            parameter_group=parameter_group,
            s3_export_role=s3_export_role,
            s3_import_role=s3_import_role,
        )

        return jsii.invoke(self, "bindToCluster", [scope, options])


@jsii.implements(IDatabaseInstance)
class DatabaseInstance(
    DatabaseInstanceBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_rds.DatabaseInstance",
):
    """A database instance.

    stability
    :stability: experimental
    resource:
    :resource:: AWS::RDS::DBInstance
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        master_username: str,
        character_set_name: typing.Optional[str] = None,
        storage_encrypted: typing.Optional[bool] = None,
        storage_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        engine: "IInstanceEngine",
        allocated_storage: typing.Optional[jsii.Number] = None,
        allow_major_version_upgrade: typing.Optional[bool] = None,
        database_name: typing.Optional[str] = None,
        instance_type: typing.Optional[_InstanceType_85a97b30] = None,
        license_model: typing.Optional["LicenseModel"] = None,
        master_user_password: typing.Optional[_SecretValue_99478b8b] = None,
        master_user_password_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        parameter_group: typing.Optional["IParameterGroup"] = None,
        timezone: typing.Optional[str] = None,
        vpc: _IVpc_3795853f,
        auto_minor_version_upgrade: typing.Optional[bool] = None,
        availability_zone: typing.Optional[str] = None,
        backup_retention: typing.Optional[_Duration_5170c158] = None,
        cloudwatch_logs_exports: typing.Optional[typing.List[str]] = None,
        cloudwatch_logs_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        cloudwatch_logs_retention_role: typing.Optional[_IRole_e69bbae4] = None,
        copy_tags_to_snapshot: typing.Optional[bool] = None,
        delete_automated_backups: typing.Optional[bool] = None,
        deletion_protection: typing.Optional[bool] = None,
        domain: typing.Optional[str] = None,
        domain_role: typing.Optional[_IRole_e69bbae4] = None,
        enable_performance_insights: typing.Optional[bool] = None,
        iam_authentication: typing.Optional[bool] = None,
        instance_identifier: typing.Optional[str] = None,
        iops: typing.Optional[jsii.Number] = None,
        max_allocated_storage: typing.Optional[jsii.Number] = None,
        monitoring_interval: typing.Optional[_Duration_5170c158] = None,
        monitoring_role: typing.Optional[_IRole_e69bbae4] = None,
        multi_az: typing.Optional[bool] = None,
        option_group: typing.Optional["IOptionGroup"] = None,
        performance_insight_encryption_key: typing.Optional[_IKey_3336c79d] = None,
        performance_insight_retention: typing.Optional["PerformanceInsightRetention"] = None,
        port: typing.Optional[jsii.Number] = None,
        preferred_backup_window: typing.Optional[str] = None,
        preferred_maintenance_window: typing.Optional[str] = None,
        processor_features: typing.Optional["ProcessorFeatures"] = None,
        removal_policy: typing.Optional[_RemovalPolicy_5986e9f3] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        storage_type: typing.Optional["StorageType"] = None,
        vpc_placement: typing.Optional[_SubnetSelection_36a13cd6] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param master_username: The master user name.
        :param character_set_name: For supported engines, specifies the character set to associate with the DB instance. Default: - RDS default character set name
        :param storage_encrypted: Indicates whether the DB instance is encrypted. Default: - true if storageEncryptionKey has been provided, false otherwise
        :param storage_encryption_key: The KMS key that's used to encrypt the DB instance. Default: - default master key if storageEncrypted is true, no key otherwise
        :param engine: The database engine.
        :param allocated_storage: The allocated storage size, specified in gigabytes (GB). Default: 100
        :param allow_major_version_upgrade: Whether to allow major version upgrades. Default: false
        :param database_name: The name of the database. Default: - no name
        :param instance_type: The name of the compute and memory capacity for the instance. Default: - m5.large (or, more specifically, db.m5.large)
        :param license_model: The license model. Default: - RDS default license model
        :param master_user_password: The master user password. Default: - a Secrets Manager generated password
        :param master_user_password_encryption_key: The KMS key used to encrypt the secret for the master user password. Default: - default master key
        :param parameter_group: The DB parameter group to associate with the instance. Default: - no parameter group
        :param timezone: The time zone of the instance. This is currently supported only by Microsoft Sql Server. Default: - RDS default timezone
        :param vpc: The VPC network where the DB subnet group should be created.
        :param auto_minor_version_upgrade: Indicates that minor engine upgrades are applied automatically to the DB instance during the maintenance window. Default: true
        :param availability_zone: The name of the Availability Zone where the DB instance will be located. Default: - no preference
        :param backup_retention: The number of days during which automatic DB snapshots are retained. Set to zero to disable backups. Default: Duration.days(1)
        :param cloudwatch_logs_exports: The list of log types that need to be enabled for exporting to CloudWatch Logs. Default: - no log exports
        :param cloudwatch_logs_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``Infinity``. Default: - logs never expire
        :param cloudwatch_logs_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - a new role is created.
        :param copy_tags_to_snapshot: Indicates whether to copy all of the user-defined tags from the DB instance to snapshots of the DB instance. Default: true
        :param delete_automated_backups: Indicates whether automated backups should be deleted or retained when you delete a DB instance. Default: false
        :param deletion_protection: Indicates whether the DB instance should have deletion protection enabled. Default: true
        :param domain: The Active Directory directory ID to create the DB instance in. Default: - Do not join domain
        :param domain_role: The IAM role to be used when making API calls to the Directory Service. The role needs the AWS-managed policy AmazonRDSDirectoryServiceAccess or equivalent. Default: - The role will be created for you if {@link DatabaseInstanceNewProps#domain} is specified
        :param enable_performance_insights: Whether to enable Performance Insights for the DB instance. Default: - false, unless ``performanceInsightRentention`` or ``performanceInsightEncryptionKey`` is set.
        :param iam_authentication: Whether to enable mapping of AWS Identity and Access Management (IAM) accounts to database accounts. Default: false
        :param instance_identifier: A name for the DB instance. If you specify a name, AWS CloudFormation converts it to lowercase. Default: - a CloudFormation generated name
        :param iops: The number of I/O operations per second (IOPS) that the database provisions. The value must be equal to or greater than 1000. Default: - no provisioned iops
        :param max_allocated_storage: Upper limit to which RDS can scale the storage in GiB(Gibibyte). Default: - No autoscaling of RDS instance
        :param monitoring_interval: The interval, in seconds, between points when Amazon RDS collects enhanced monitoring metrics for the DB instance. Default: - no enhanced monitoring
        :param monitoring_role: Role that will be used to manage DB instance monitoring. Default: - A role is automatically created for you
        :param multi_az: Specifies if the database instance is a multiple Availability Zone deployment. Default: false
        :param option_group: The option group to associate with the instance. Default: - no option group
        :param performance_insight_encryption_key: The AWS KMS key for encryption of Performance Insights data. Default: - default master key
        :param performance_insight_retention: The amount of time, in days, to retain Performance Insights data. Default: 7
        :param port: The port for the instance. Default: - the default port for the chosen engine.
        :param preferred_backup_window: The daily time range during which automated backups are performed. Constraints: - Must be in the format ``hh24:mi-hh24:mi``. - Must be in Universal Coordinated Time (UTC). - Must not conflict with the preferred maintenance window. - Must be at least 30 minutes. Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html#USER_WorkingWithAutomatedBackups.BackupWindow
        :param preferred_maintenance_window: The weekly time range (in UTC) during which system maintenance can occur. Format: ``ddd:hh24:mi-ddd:hh24:mi`` Constraint: Minimum 30-minute window Default: - a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week. To see the time blocks available, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_UpgradeDBInstance.Maintenance.html#Concepts.DBMaintenance
        :param processor_features: The number of CPU cores and the number of threads per core. Default: - the default number of CPU cores and threads per core for the chosen instance class. See https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html#USER_ConfigureProcessor
        :param removal_policy: The CloudFormation policy to apply when the instance is removed from the stack or replaced during an update. Default: - RemovalPolicy.SNAPSHOT (remove the resource, but retain a snapshot of the data)
        :param security_groups: The security groups to assign to the DB instance. Default: - a new security group is created
        :param storage_type: The storage type. Default: GP2
        :param vpc_placement: The type of subnets to add to the created DB subnet group. Default: - private subnets
        :param vpc_subnets: The type of subnets to add to the created DB subnet group. Default: - private subnets

        stability
        :stability: experimental
        """
        props = DatabaseInstanceProps(
            master_username=master_username,
            character_set_name=character_set_name,
            storage_encrypted=storage_encrypted,
            storage_encryption_key=storage_encryption_key,
            engine=engine,
            allocated_storage=allocated_storage,
            allow_major_version_upgrade=allow_major_version_upgrade,
            database_name=database_name,
            instance_type=instance_type,
            license_model=license_model,
            master_user_password=master_user_password,
            master_user_password_encryption_key=master_user_password_encryption_key,
            parameter_group=parameter_group,
            timezone=timezone,
            vpc=vpc,
            auto_minor_version_upgrade=auto_minor_version_upgrade,
            availability_zone=availability_zone,
            backup_retention=backup_retention,
            cloudwatch_logs_exports=cloudwatch_logs_exports,
            cloudwatch_logs_retention=cloudwatch_logs_retention,
            cloudwatch_logs_retention_role=cloudwatch_logs_retention_role,
            copy_tags_to_snapshot=copy_tags_to_snapshot,
            delete_automated_backups=delete_automated_backups,
            deletion_protection=deletion_protection,
            domain=domain,
            domain_role=domain_role,
            enable_performance_insights=enable_performance_insights,
            iam_authentication=iam_authentication,
            instance_identifier=instance_identifier,
            iops=iops,
            max_allocated_storage=max_allocated_storage,
            monitoring_interval=monitoring_interval,
            monitoring_role=monitoring_role,
            multi_az=multi_az,
            option_group=option_group,
            performance_insight_encryption_key=performance_insight_encryption_key,
            performance_insight_retention=performance_insight_retention,
            port=port,
            preferred_backup_window=preferred_backup_window,
            preferred_maintenance_window=preferred_maintenance_window,
            processor_features=processor_features,
            removal_policy=removal_policy,
            security_groups=security_groups,
            storage_type=storage_type,
            vpc_placement=vpc_placement,
            vpc_subnets=vpc_subnets,
        )

        jsii.create(DatabaseInstance, self, [scope, id, props])

    @jsii.member(jsii_name="addRotationMultiUser")
    def add_rotation_multi_user(
        self,
        id: str,
        *,
        secret: _ISecret_75279d36,
        automatically_after: typing.Optional[_Duration_5170c158] = None,
    ) -> _SecretRotation_312fb992:
        """Adds the multi user rotation to this instance.

        :param id: -
        :param secret: The secret to rotate. It must be a JSON string with the following format:: { "engine": <required: database engine>, "host": <required: instance host name>, "username": <required: username>, "password": <required: password>, "dbname": <optional: database name>, "port": <optional: if not specified, default port will be used>, "masterarn": <required: the arn of the master secret which will be used to create users/change passwords> }
        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: Duration.days(30)

        stability
        :stability: experimental
        """
        options = RotationMultiUserOptions(
            secret=secret, automatically_after=automatically_after
        )

        return jsii.invoke(self, "addRotationMultiUser", [id, options])

    @jsii.member(jsii_name="addRotationSingleUser")
    def add_rotation_single_user(
        self, automatically_after: typing.Optional[_Duration_5170c158] = None
    ) -> _SecretRotation_312fb992:
        """Adds the single user rotation of the master password to this instance.

        :param automatically_after: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addRotationSingleUser", [automatically_after])

    @jsii.member(jsii_name="setLogRetention")
    def _set_log_retention(self) -> None:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "setLogRetention", [])

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_231f38b5:
        """Access to network connections.

        stability
        :stability: experimental
        """
        return jsii.get(self, "connections")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> str:
        """The instance endpoint address.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dbInstanceEndpointAddress")

    @builtins.property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> str:
        """The instance endpoint port.

        stability
        :stability: experimental
        """
        return jsii.get(self, "dbInstanceEndpointPort")

    @builtins.property
    @jsii.member(jsii_name="instanceEndpoint")
    def instance_endpoint(self) -> "Endpoint":
        """The instance endpoint.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceEndpoint")

    @builtins.property
    @jsii.member(jsii_name="instanceIdentifier")
    def instance_identifier(self) -> str:
        """The instance identifier.

        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceIdentifier")

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def _instance_type(self) -> _InstanceType_85a97b30:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "instanceType")

    @builtins.property
    @jsii.member(jsii_name="newCfnProps")
    def _new_cfn_props(self) -> "CfnDBInstanceProps":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "newCfnProps")

    @builtins.property
    @jsii.member(jsii_name="sourceCfnProps")
    def _source_cfn_props(self) -> "CfnDBInstanceProps":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "sourceCfnProps")

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> _IVpc_3795853f:
        """The VPC where this database instance is deployed.

        stability
        :stability: experimental
        """
        return jsii.get(self, "vpc")

    @builtins.property
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Optional[_ISecret_75279d36]:
        """The AWS Secrets Manager secret attached to the instance.

        stability
        :stability: experimental
        """
        return jsii.get(self, "secret")

    @builtins.property
    @jsii.member(jsii_name="vpcPlacement")
    def _vpc_placement(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "vpcPlacement")

    @builtins.property
    @jsii.member(jsii_name="enableIamAuthentication")
    def _enable_iam_authentication(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "enableIamAuthentication")

    @_enable_iam_authentication.setter
    def _enable_iam_authentication(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "enableIamAuthentication", value)


__all__ = [
    "AuroraClusterEngineProps",
    "AuroraEngineVersion",
    "AuroraMysqlClusterEngineProps",
    "AuroraMysqlEngineVersion",
    "AuroraPostgresClusterEngineProps",
    "AuroraPostgresEngineVersion",
    "BackupProps",
    "CfnDBCluster",
    "CfnDBClusterParameterGroup",
    "CfnDBClusterParameterGroupProps",
    "CfnDBClusterProps",
    "CfnDBInstance",
    "CfnDBInstanceProps",
    "CfnDBParameterGroup",
    "CfnDBParameterGroupProps",
    "CfnDBProxy",
    "CfnDBProxyProps",
    "CfnDBProxyTargetGroup",
    "CfnDBProxyTargetGroupProps",
    "CfnDBSecurityGroup",
    "CfnDBSecurityGroupIngress",
    "CfnDBSecurityGroupIngressProps",
    "CfnDBSecurityGroupProps",
    "CfnDBSubnetGroup",
    "CfnDBSubnetGroupProps",
    "CfnEventSubscription",
    "CfnEventSubscriptionProps",
    "CfnOptionGroup",
    "CfnOptionGroupProps",
    "ClusterEngineBindOptions",
    "ClusterEngineConfig",
    "DatabaseCluster",
    "DatabaseClusterAttributes",
    "DatabaseClusterEngine",
    "DatabaseClusterProps",
    "DatabaseInstance",
    "DatabaseInstanceAttributes",
    "DatabaseInstanceBase",
    "DatabaseInstanceEngine",
    "DatabaseInstanceFromSnapshot",
    "DatabaseInstanceFromSnapshotProps",
    "DatabaseInstanceNewProps",
    "DatabaseInstanceProps",
    "DatabaseInstanceReadReplica",
    "DatabaseInstanceReadReplicaProps",
    "DatabaseInstanceSourceProps",
    "DatabaseProxy",
    "DatabaseProxyAttributes",
    "DatabaseProxyOptions",
    "DatabaseProxyProps",
    "DatabaseSecret",
    "DatabaseSecretProps",
    "Endpoint",
    "EngineVersion",
    "IClusterEngine",
    "IDatabaseCluster",
    "IDatabaseInstance",
    "IDatabaseProxy",
    "IEngine",
    "IInstanceEngine",
    "IOptionGroup",
    "IParameterGroup",
    "InstanceEngineBindOptions",
    "InstanceEngineConfig",
    "InstanceProps",
    "LicenseModel",
    "Login",
    "MariaDbEngineVersion",
    "MariaDbInstanceEngineProps",
    "MySqlInstanceEngineProps",
    "MysqlEngineVersion",
    "OptionConfiguration",
    "OptionGroup",
    "OptionGroupProps",
    "OracleEeInstanceEngineProps",
    "OracleEngineVersion",
    "OracleLegacyEngineVersion",
    "OracleSe1InstanceEngineProps",
    "OracleSe2InstanceEngineProps",
    "OracleSeInstanceEngineProps",
    "ParameterGroup",
    "ParameterGroupClusterBindOptions",
    "ParameterGroupClusterConfig",
    "ParameterGroupInstanceBindOptions",
    "ParameterGroupInstanceConfig",
    "ParameterGroupProps",
    "PerformanceInsightRetention",
    "PostgresEngineVersion",
    "PostgresInstanceEngineProps",
    "ProcessorFeatures",
    "ProxyTarget",
    "ProxyTargetConfig",
    "RotationMultiUserOptions",
    "SessionPinningFilter",
    "SqlServerEeInstanceEngineProps",
    "SqlServerEngineVersion",
    "SqlServerExInstanceEngineProps",
    "SqlServerSeInstanceEngineProps",
    "SqlServerWebInstanceEngineProps",
    "StorageType",
]

publication.publish()
