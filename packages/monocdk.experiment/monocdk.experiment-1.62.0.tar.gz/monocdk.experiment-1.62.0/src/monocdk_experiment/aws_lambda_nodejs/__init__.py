import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from .._jsii import *

from .. import Construct as _Construct_f50a3f53, Duration as _Duration_5170c158
from ..aws_codeguruprofiler import IProfilingGroup as _IProfilingGroup_ca898ddc
from ..aws_ec2 import (
    ISecurityGroup as _ISecurityGroup_d72ab8e8,
    IVpc as _IVpc_3795853f,
    SubnetSelection as _SubnetSelection_36a13cd6,
)
from ..aws_iam import (
    IRole as _IRole_e69bbae4, PolicyStatement as _PolicyStatement_f75dc775
)
from ..aws_lambda import (
    AssetCode as _AssetCode_763678ad,
    FileSystem as _FileSystem_132c0ce7,
    Function as _Function_c537766c,
    FunctionOptions as _FunctionOptions_83fb7178,
    IDestination as _IDestination_7081f282,
    IEventSource as _IEventSource_0e6bcb85,
    ILayerVersion as _ILayerVersion_aa5e0c0c,
    LogRetentionRetryOptions as _LogRetentionRetryOptions_09658088,
    Runtime as _Runtime_8b970b80,
    Tracing as _Tracing_34f0a955,
    VersionOptions as _VersionOptions_9a55a63d,
)
from ..aws_logs import RetentionDays as _RetentionDays_bdc7ad1f
from ..aws_sqs import IQueue as _IQueue_b743f559


class Bundling(
    metaclass=jsii.JSIIMeta, jsii_type="monocdk-experiment.aws_lambda_nodejs.Bundling"
):
    """Bundling.

    stability
    :stability: experimental
    """

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(Bundling, self, [])

    @jsii.member(jsii_name="parcel")
    @builtins.classmethod
    def parcel(
        cls,
        *,
        entry: str,
        runtime: _Runtime_8b970b80,
        build_args: typing.Optional[typing.Mapping[str, str]] = None,
        cache_dir: typing.Optional[str] = None,
        external_modules: typing.Optional[typing.List[str]] = None,
        force_docker_bundling: typing.Optional[bool] = None,
        minify: typing.Optional[bool] = None,
        node_modules: typing.Optional[typing.List[str]] = None,
        parcel_environment: typing.Optional[typing.Mapping[str, str]] = None,
        parcel_version: typing.Optional[str] = None,
        project_root: typing.Optional[str] = None,
        source_maps: typing.Optional[bool] = None,
    ) -> _AssetCode_763678ad:
        """Parcel bundled Lambda asset code.

        :param entry: Entry file.
        :param runtime: The runtime of the lambda function.
        :param build_args: Build arguments to pass when building the bundling image. Default: - no build arguments are passed
        :param cache_dir: The cache directory (relative to the project root). Parcel uses a filesystem cache for fast rebuilds. Default: - ``.parcel-cache`` in the working directory
        :param external_modules: A list of modules that should be considered as externals (already available in the runtime). Default: ['aws-sdk']
        :param force_docker_bundling: Force bundling in a Docker container even if local bundling is possible.This is useful if your function relies on node modules that should be installed (``nodeModules``) in a Lambda compatible environment. Default: false
        :param minify: Whether to minify files when bundling. Default: false
        :param node_modules: A list of modules that should be installed instead of bundled. Modules are installed in a Lambda compatible environnment. Default: - all modules are bundled
        :param parcel_environment: Environment variables defined when Parcel runs. Default: - no environment variables are defined.
        :param parcel_version: The version of Parcel to use when running in a Docker container. Default: - 2.0.0-beta.1
        :param project_root: The root of the project. This will be used as the source for the volume mounted in the Docker container. If you specify this prop, ensure that this path includes ``entry`` and any module/dependencies used by your function otherwise bundling will not be possible. Default: - the closest path containing a .git folder
        :param source_maps: Whether to include source maps when bundling. Default: false

        stability
        :stability: experimental
        """
        options = ParcelOptions(
            entry=entry,
            runtime=runtime,
            build_args=build_args,
            cache_dir=cache_dir,
            external_modules=external_modules,
            force_docker_bundling=force_docker_bundling,
            minify=minify,
            node_modules=node_modules,
            parcel_environment=parcel_environment,
            parcel_version=parcel_version,
            project_root=project_root,
            source_maps=source_maps,
        )

        return jsii.sinvoke(cls, "parcel", [options])


class NodejsFunction(
    _Function_c537766c,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.aws_lambda_nodejs.NodejsFunction",
):
    """A Node.js Lambda function bundled using Parcel.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        aws_sdk_connection_reuse: typing.Optional[bool] = None,
        entry: typing.Optional[str] = None,
        handler: typing.Optional[str] = None,
        runtime: typing.Optional[_Runtime_8b970b80] = None,
        allow_all_outbound: typing.Optional[bool] = None,
        allow_public_subnet: typing.Optional[bool] = None,
        current_version_options: typing.Optional[_VersionOptions_9a55a63d] = None,
        dead_letter_queue: typing.Optional[_IQueue_b743f559] = None,
        dead_letter_queue_enabled: typing.Optional[bool] = None,
        description: typing.Optional[str] = None,
        environment: typing.Optional[typing.Mapping[str, str]] = None,
        events: typing.Optional[typing.List[_IEventSource_0e6bcb85]] = None,
        filesystem: typing.Optional[_FileSystem_132c0ce7] = None,
        function_name: typing.Optional[str] = None,
        initial_policy: typing.Optional[typing.List[_PolicyStatement_f75dc775]] = None,
        layers: typing.Optional[typing.List[_ILayerVersion_aa5e0c0c]] = None,
        log_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        log_retention_retry_options: typing.Optional[_LogRetentionRetryOptions_09658088] = None,
        log_retention_role: typing.Optional[_IRole_e69bbae4] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[bool] = None,
        profiling_group: typing.Optional[_IProfilingGroup_ca898ddc] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_group: typing.Optional[_ISecurityGroup_d72ab8e8] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        tracing: typing.Optional[_Tracing_34f0a955] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        build_args: typing.Optional[typing.Mapping[str, str]] = None,
        cache_dir: typing.Optional[str] = None,
        external_modules: typing.Optional[typing.List[str]] = None,
        force_docker_bundling: typing.Optional[bool] = None,
        minify: typing.Optional[bool] = None,
        node_modules: typing.Optional[typing.List[str]] = None,
        parcel_environment: typing.Optional[typing.Mapping[str, str]] = None,
        parcel_version: typing.Optional[str] = None,
        project_root: typing.Optional[str] = None,
        source_maps: typing.Optional[bool] = None,
        max_event_age: typing.Optional[_Duration_5170c158] = None,
        on_failure: typing.Optional[_IDestination_7081f282] = None,
        on_success: typing.Optional[_IDestination_7081f282] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param aws_sdk_connection_reuse: Whether to automatically reuse TCP connections when working with the AWS SDK for JavaScript. This sets the ``AWS_NODEJS_CONNECTION_REUSE_ENABLED`` environment variable to ``1``. Default: true
        :param entry: Path to the entry file (JavaScript or TypeScript). Default: - Derived from the name of the defining file and the construct's id. If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts`` and ``stack.my-handler.js``.
        :param handler: The name of the exported handler in the entry file. Default: handler
        :param runtime: The runtime environment. Only runtimes of the Node.js family are supported. Default: - ``NODEJS_12_X`` if ``process.versions.node`` >= '12.0.0', ``NODEJS_10_X`` otherwise.
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: Enable profiling. Default: - No profiling.
        :param profiling_group: Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param build_args: Build arguments to pass when building the bundling image. Default: - no build arguments are passed
        :param cache_dir: The cache directory (relative to the project root). Parcel uses a filesystem cache for fast rebuilds. Default: - ``.parcel-cache`` in the working directory
        :param external_modules: A list of modules that should be considered as externals (already available in the runtime). Default: ['aws-sdk']
        :param force_docker_bundling: Force bundling in a Docker container even if local bundling is possible.This is useful if your function relies on node modules that should be installed (``nodeModules``) in a Lambda compatible environment. Default: false
        :param minify: Whether to minify files when bundling. Default: false
        :param node_modules: A list of modules that should be installed instead of bundled. Modules are installed in a Lambda compatible environnment. Default: - all modules are bundled
        :param parcel_environment: Environment variables defined when Parcel runs. Default: - no environment variables are defined.
        :param parcel_version: The version of Parcel to use when running in a Docker container. Default: - 2.0.0-beta.1
        :param project_root: The root of the project. This will be used as the source for the volume mounted in the Docker container. If you specify this prop, ensure that this path includes ``entry`` and any module/dependencies used by your function otherwise bundling will not be possible. Default: - the closest path containing a .git folder
        :param source_maps: Whether to include source maps when bundling. Default: false
        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        stability
        :stability: experimental
        """
        props = NodejsFunctionProps(
            aws_sdk_connection_reuse=aws_sdk_connection_reuse,
            entry=entry,
            handler=handler,
            runtime=runtime,
            allow_all_outbound=allow_all_outbound,
            allow_public_subnet=allow_public_subnet,
            current_version_options=current_version_options,
            dead_letter_queue=dead_letter_queue,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
            description=description,
            environment=environment,
            events=events,
            filesystem=filesystem,
            function_name=function_name,
            initial_policy=initial_policy,
            layers=layers,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            memory_size=memory_size,
            profiling=profiling,
            profiling_group=profiling_group,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            security_group=security_group,
            security_groups=security_groups,
            timeout=timeout,
            tracing=tracing,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            build_args=build_args,
            cache_dir=cache_dir,
            external_modules=external_modules,
            force_docker_bundling=force_docker_bundling,
            minify=minify,
            node_modules=node_modules,
            parcel_environment=parcel_environment,
            parcel_version=parcel_version,
            project_root=project_root,
            source_maps=source_maps,
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
        )

        jsii.create(NodejsFunction, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_lambda_nodejs.ParcelBaseOptions",
    jsii_struct_bases=[],
    name_mapping={
        "build_args": "buildArgs",
        "cache_dir": "cacheDir",
        "external_modules": "externalModules",
        "force_docker_bundling": "forceDockerBundling",
        "minify": "minify",
        "node_modules": "nodeModules",
        "parcel_environment": "parcelEnvironment",
        "parcel_version": "parcelVersion",
        "project_root": "projectRoot",
        "source_maps": "sourceMaps",
    },
)
class ParcelBaseOptions:
    def __init__(
        self,
        *,
        build_args: typing.Optional[typing.Mapping[str, str]] = None,
        cache_dir: typing.Optional[str] = None,
        external_modules: typing.Optional[typing.List[str]] = None,
        force_docker_bundling: typing.Optional[bool] = None,
        minify: typing.Optional[bool] = None,
        node_modules: typing.Optional[typing.List[str]] = None,
        parcel_environment: typing.Optional[typing.Mapping[str, str]] = None,
        parcel_version: typing.Optional[str] = None,
        project_root: typing.Optional[str] = None,
        source_maps: typing.Optional[bool] = None,
    ) -> None:
        """Base options for Parcel bundling.

        :param build_args: Build arguments to pass when building the bundling image. Default: - no build arguments are passed
        :param cache_dir: The cache directory (relative to the project root). Parcel uses a filesystem cache for fast rebuilds. Default: - ``.parcel-cache`` in the working directory
        :param external_modules: A list of modules that should be considered as externals (already available in the runtime). Default: ['aws-sdk']
        :param force_docker_bundling: Force bundling in a Docker container even if local bundling is possible.This is useful if your function relies on node modules that should be installed (``nodeModules``) in a Lambda compatible environment. Default: false
        :param minify: Whether to minify files when bundling. Default: false
        :param node_modules: A list of modules that should be installed instead of bundled. Modules are installed in a Lambda compatible environnment. Default: - all modules are bundled
        :param parcel_environment: Environment variables defined when Parcel runs. Default: - no environment variables are defined.
        :param parcel_version: The version of Parcel to use when running in a Docker container. Default: - 2.0.0-beta.1
        :param project_root: The root of the project. This will be used as the source for the volume mounted in the Docker container. If you specify this prop, ensure that this path includes ``entry`` and any module/dependencies used by your function otherwise bundling will not be possible. Default: - the closest path containing a .git folder
        :param source_maps: Whether to include source maps when bundling. Default: false

        stability
        :stability: experimental
        """
        self._values = {}
        if build_args is not None:
            self._values["build_args"] = build_args
        if cache_dir is not None:
            self._values["cache_dir"] = cache_dir
        if external_modules is not None:
            self._values["external_modules"] = external_modules
        if force_docker_bundling is not None:
            self._values["force_docker_bundling"] = force_docker_bundling
        if minify is not None:
            self._values["minify"] = minify
        if node_modules is not None:
            self._values["node_modules"] = node_modules
        if parcel_environment is not None:
            self._values["parcel_environment"] = parcel_environment
        if parcel_version is not None:
            self._values["parcel_version"] = parcel_version
        if project_root is not None:
            self._values["project_root"] = project_root
        if source_maps is not None:
            self._values["source_maps"] = source_maps

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Build arguments to pass when building the bundling image.

        default
        :default: - no build arguments are passed

        stability
        :stability: experimental
        """
        return self._values.get("build_args")

    @builtins.property
    def cache_dir(self) -> typing.Optional[str]:
        """The cache directory (relative to the project root).

        Parcel uses a filesystem cache for fast rebuilds.

        default
        :default: - ``.parcel-cache`` in the working directory

        stability
        :stability: experimental
        """
        return self._values.get("cache_dir")

    @builtins.property
    def external_modules(self) -> typing.Optional[typing.List[str]]:
        """A list of modules that should be considered as externals (already available in the runtime).

        default
        :default: ['aws-sdk']

        stability
        :stability: experimental
        """
        return self._values.get("external_modules")

    @builtins.property
    def force_docker_bundling(self) -> typing.Optional[bool]:
        """Force bundling in a Docker container even if local bundling is possible.This  is useful if your function relies on node modules that should be installed (``nodeModules``) in a Lambda compatible environment.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("force_docker_bundling")

    @builtins.property
    def minify(self) -> typing.Optional[bool]:
        """Whether to minify files when bundling.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("minify")

    @builtins.property
    def node_modules(self) -> typing.Optional[typing.List[str]]:
        """A list of modules that should be installed instead of bundled.

        Modules are
        installed in a Lambda compatible environnment.

        default
        :default: - all modules are bundled

        stability
        :stability: experimental
        """
        return self._values.get("node_modules")

    @builtins.property
    def parcel_environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Environment variables defined when Parcel runs.

        default
        :default: - no environment variables are defined.

        stability
        :stability: experimental
        """
        return self._values.get("parcel_environment")

    @builtins.property
    def parcel_version(self) -> typing.Optional[str]:
        """The version of Parcel to use when running in a Docker container.

        default
        :default: - 2.0.0-beta.1

        stability
        :stability: experimental
        """
        return self._values.get("parcel_version")

    @builtins.property
    def project_root(self) -> typing.Optional[str]:
        """The root of the project.

        This will be used as the source for the volume
        mounted in the Docker container. If you specify this prop, ensure that
        this path includes ``entry`` and any module/dependencies used by your
        function otherwise bundling will not be possible.

        default
        :default: - the closest path containing a .git folder

        stability
        :stability: experimental
        """
        return self._values.get("project_root")

    @builtins.property
    def source_maps(self) -> typing.Optional[bool]:
        """Whether to include source maps when bundling.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("source_maps")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParcelBaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_lambda_nodejs.ParcelOptions",
    jsii_struct_bases=[ParcelBaseOptions],
    name_mapping={
        "build_args": "buildArgs",
        "cache_dir": "cacheDir",
        "external_modules": "externalModules",
        "force_docker_bundling": "forceDockerBundling",
        "minify": "minify",
        "node_modules": "nodeModules",
        "parcel_environment": "parcelEnvironment",
        "parcel_version": "parcelVersion",
        "project_root": "projectRoot",
        "source_maps": "sourceMaps",
        "entry": "entry",
        "runtime": "runtime",
    },
)
class ParcelOptions(ParcelBaseOptions):
    def __init__(
        self,
        *,
        build_args: typing.Optional[typing.Mapping[str, str]] = None,
        cache_dir: typing.Optional[str] = None,
        external_modules: typing.Optional[typing.List[str]] = None,
        force_docker_bundling: typing.Optional[bool] = None,
        minify: typing.Optional[bool] = None,
        node_modules: typing.Optional[typing.List[str]] = None,
        parcel_environment: typing.Optional[typing.Mapping[str, str]] = None,
        parcel_version: typing.Optional[str] = None,
        project_root: typing.Optional[str] = None,
        source_maps: typing.Optional[bool] = None,
        entry: str,
        runtime: _Runtime_8b970b80,
    ) -> None:
        """Options for Parcel bundling.

        :param build_args: Build arguments to pass when building the bundling image. Default: - no build arguments are passed
        :param cache_dir: The cache directory (relative to the project root). Parcel uses a filesystem cache for fast rebuilds. Default: - ``.parcel-cache`` in the working directory
        :param external_modules: A list of modules that should be considered as externals (already available in the runtime). Default: ['aws-sdk']
        :param force_docker_bundling: Force bundling in a Docker container even if local bundling is possible.This is useful if your function relies on node modules that should be installed (``nodeModules``) in a Lambda compatible environment. Default: false
        :param minify: Whether to minify files when bundling. Default: false
        :param node_modules: A list of modules that should be installed instead of bundled. Modules are installed in a Lambda compatible environnment. Default: - all modules are bundled
        :param parcel_environment: Environment variables defined when Parcel runs. Default: - no environment variables are defined.
        :param parcel_version: The version of Parcel to use when running in a Docker container. Default: - 2.0.0-beta.1
        :param project_root: The root of the project. This will be used as the source for the volume mounted in the Docker container. If you specify this prop, ensure that this path includes ``entry`` and any module/dependencies used by your function otherwise bundling will not be possible. Default: - the closest path containing a .git folder
        :param source_maps: Whether to include source maps when bundling. Default: false
        :param entry: Entry file.
        :param runtime: The runtime of the lambda function.

        stability
        :stability: experimental
        """
        self._values = {
            "entry": entry,
            "runtime": runtime,
        }
        if build_args is not None:
            self._values["build_args"] = build_args
        if cache_dir is not None:
            self._values["cache_dir"] = cache_dir
        if external_modules is not None:
            self._values["external_modules"] = external_modules
        if force_docker_bundling is not None:
            self._values["force_docker_bundling"] = force_docker_bundling
        if minify is not None:
            self._values["minify"] = minify
        if node_modules is not None:
            self._values["node_modules"] = node_modules
        if parcel_environment is not None:
            self._values["parcel_environment"] = parcel_environment
        if parcel_version is not None:
            self._values["parcel_version"] = parcel_version
        if project_root is not None:
            self._values["project_root"] = project_root
        if source_maps is not None:
            self._values["source_maps"] = source_maps

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Build arguments to pass when building the bundling image.

        default
        :default: - no build arguments are passed

        stability
        :stability: experimental
        """
        return self._values.get("build_args")

    @builtins.property
    def cache_dir(self) -> typing.Optional[str]:
        """The cache directory (relative to the project root).

        Parcel uses a filesystem cache for fast rebuilds.

        default
        :default: - ``.parcel-cache`` in the working directory

        stability
        :stability: experimental
        """
        return self._values.get("cache_dir")

    @builtins.property
    def external_modules(self) -> typing.Optional[typing.List[str]]:
        """A list of modules that should be considered as externals (already available in the runtime).

        default
        :default: ['aws-sdk']

        stability
        :stability: experimental
        """
        return self._values.get("external_modules")

    @builtins.property
    def force_docker_bundling(self) -> typing.Optional[bool]:
        """Force bundling in a Docker container even if local bundling is possible.This  is useful if your function relies on node modules that should be installed (``nodeModules``) in a Lambda compatible environment.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("force_docker_bundling")

    @builtins.property
    def minify(self) -> typing.Optional[bool]:
        """Whether to minify files when bundling.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("minify")

    @builtins.property
    def node_modules(self) -> typing.Optional[typing.List[str]]:
        """A list of modules that should be installed instead of bundled.

        Modules are
        installed in a Lambda compatible environnment.

        default
        :default: - all modules are bundled

        stability
        :stability: experimental
        """
        return self._values.get("node_modules")

    @builtins.property
    def parcel_environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Environment variables defined when Parcel runs.

        default
        :default: - no environment variables are defined.

        stability
        :stability: experimental
        """
        return self._values.get("parcel_environment")

    @builtins.property
    def parcel_version(self) -> typing.Optional[str]:
        """The version of Parcel to use when running in a Docker container.

        default
        :default: - 2.0.0-beta.1

        stability
        :stability: experimental
        """
        return self._values.get("parcel_version")

    @builtins.property
    def project_root(self) -> typing.Optional[str]:
        """The root of the project.

        This will be used as the source for the volume
        mounted in the Docker container. If you specify this prop, ensure that
        this path includes ``entry`` and any module/dependencies used by your
        function otherwise bundling will not be possible.

        default
        :default: - the closest path containing a .git folder

        stability
        :stability: experimental
        """
        return self._values.get("project_root")

    @builtins.property
    def source_maps(self) -> typing.Optional[bool]:
        """Whether to include source maps when bundling.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("source_maps")

    @builtins.property
    def entry(self) -> str:
        """Entry file.

        stability
        :stability: experimental
        """
        return self._values.get("entry")

    @builtins.property
    def runtime(self) -> _Runtime_8b970b80:
        """The runtime of the lambda function.

        stability
        :stability: experimental
        """
        return self._values.get("runtime")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ParcelOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.aws_lambda_nodejs.NodejsFunctionProps",
    jsii_struct_bases=[_FunctionOptions_83fb7178, ParcelBaseOptions],
    name_mapping={
        "max_event_age": "maxEventAge",
        "on_failure": "onFailure",
        "on_success": "onSuccess",
        "retry_attempts": "retryAttempts",
        "allow_all_outbound": "allowAllOutbound",
        "allow_public_subnet": "allowPublicSubnet",
        "current_version_options": "currentVersionOptions",
        "dead_letter_queue": "deadLetterQueue",
        "dead_letter_queue_enabled": "deadLetterQueueEnabled",
        "description": "description",
        "environment": "environment",
        "events": "events",
        "filesystem": "filesystem",
        "function_name": "functionName",
        "initial_policy": "initialPolicy",
        "layers": "layers",
        "log_retention": "logRetention",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "log_retention_role": "logRetentionRole",
        "memory_size": "memorySize",
        "profiling": "profiling",
        "profiling_group": "profilingGroup",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "timeout": "timeout",
        "tracing": "tracing",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "build_args": "buildArgs",
        "cache_dir": "cacheDir",
        "external_modules": "externalModules",
        "force_docker_bundling": "forceDockerBundling",
        "minify": "minify",
        "node_modules": "nodeModules",
        "parcel_environment": "parcelEnvironment",
        "parcel_version": "parcelVersion",
        "project_root": "projectRoot",
        "source_maps": "sourceMaps",
        "aws_sdk_connection_reuse": "awsSdkConnectionReuse",
        "entry": "entry",
        "handler": "handler",
        "runtime": "runtime",
    },
)
class NodejsFunctionProps(_FunctionOptions_83fb7178, ParcelBaseOptions):
    def __init__(
        self,
        *,
        max_event_age: typing.Optional[_Duration_5170c158] = None,
        on_failure: typing.Optional[_IDestination_7081f282] = None,
        on_success: typing.Optional[_IDestination_7081f282] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        allow_all_outbound: typing.Optional[bool] = None,
        allow_public_subnet: typing.Optional[bool] = None,
        current_version_options: typing.Optional[_VersionOptions_9a55a63d] = None,
        dead_letter_queue: typing.Optional[_IQueue_b743f559] = None,
        dead_letter_queue_enabled: typing.Optional[bool] = None,
        description: typing.Optional[str] = None,
        environment: typing.Optional[typing.Mapping[str, str]] = None,
        events: typing.Optional[typing.List[_IEventSource_0e6bcb85]] = None,
        filesystem: typing.Optional[_FileSystem_132c0ce7] = None,
        function_name: typing.Optional[str] = None,
        initial_policy: typing.Optional[typing.List[_PolicyStatement_f75dc775]] = None,
        layers: typing.Optional[typing.List[_ILayerVersion_aa5e0c0c]] = None,
        log_retention: typing.Optional[_RetentionDays_bdc7ad1f] = None,
        log_retention_retry_options: typing.Optional[_LogRetentionRetryOptions_09658088] = None,
        log_retention_role: typing.Optional[_IRole_e69bbae4] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[bool] = None,
        profiling_group: typing.Optional[_IProfilingGroup_ca898ddc] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_IRole_e69bbae4] = None,
        security_group: typing.Optional[_ISecurityGroup_d72ab8e8] = None,
        security_groups: typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]] = None,
        timeout: typing.Optional[_Duration_5170c158] = None,
        tracing: typing.Optional[_Tracing_34f0a955] = None,
        vpc: typing.Optional[_IVpc_3795853f] = None,
        vpc_subnets: typing.Optional[_SubnetSelection_36a13cd6] = None,
        build_args: typing.Optional[typing.Mapping[str, str]] = None,
        cache_dir: typing.Optional[str] = None,
        external_modules: typing.Optional[typing.List[str]] = None,
        force_docker_bundling: typing.Optional[bool] = None,
        minify: typing.Optional[bool] = None,
        node_modules: typing.Optional[typing.List[str]] = None,
        parcel_environment: typing.Optional[typing.Mapping[str, str]] = None,
        parcel_version: typing.Optional[str] = None,
        project_root: typing.Optional[str] = None,
        source_maps: typing.Optional[bool] = None,
        aws_sdk_connection_reuse: typing.Optional[bool] = None,
        entry: typing.Optional[str] = None,
        handler: typing.Optional[str] = None,
        runtime: typing.Optional[_Runtime_8b970b80] = None,
    ) -> None:
        """Properties for a NodejsFunction.

        :param max_event_age: The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: The destination for failed invocations. Default: - no destination
        :param on_success: The destination for successful invocations. Default: - no destination
        :param retry_attempts: The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param allow_all_outbound: Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param current_version_options: Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: The SQS queue to use if DLQ is enabled. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param description: A description of the function. Default: - No description.
        :param environment: Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param events: Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param layers: A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by mulitple functions. Default: - No layers.
        :param log_retention: The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: Enable profiling. Default: - No profiling.
        :param profiling_group: Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param build_args: Build arguments to pass when building the bundling image. Default: - no build arguments are passed
        :param cache_dir: The cache directory (relative to the project root). Parcel uses a filesystem cache for fast rebuilds. Default: - ``.parcel-cache`` in the working directory
        :param external_modules: A list of modules that should be considered as externals (already available in the runtime). Default: ['aws-sdk']
        :param force_docker_bundling: Force bundling in a Docker container even if local bundling is possible.This is useful if your function relies on node modules that should be installed (``nodeModules``) in a Lambda compatible environment. Default: false
        :param minify: Whether to minify files when bundling. Default: false
        :param node_modules: A list of modules that should be installed instead of bundled. Modules are installed in a Lambda compatible environnment. Default: - all modules are bundled
        :param parcel_environment: Environment variables defined when Parcel runs. Default: - no environment variables are defined.
        :param parcel_version: The version of Parcel to use when running in a Docker container. Default: - 2.0.0-beta.1
        :param project_root: The root of the project. This will be used as the source for the volume mounted in the Docker container. If you specify this prop, ensure that this path includes ``entry`` and any module/dependencies used by your function otherwise bundling will not be possible. Default: - the closest path containing a .git folder
        :param source_maps: Whether to include source maps when bundling. Default: false
        :param aws_sdk_connection_reuse: Whether to automatically reuse TCP connections when working with the AWS SDK for JavaScript. This sets the ``AWS_NODEJS_CONNECTION_REUSE_ENABLED`` environment variable to ``1``. Default: true
        :param entry: Path to the entry file (JavaScript or TypeScript). Default: - Derived from the name of the defining file and the construct's id. If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts`` and ``stack.my-handler.js``.
        :param handler: The name of the exported handler in the entry file. Default: handler
        :param runtime: The runtime environment. Only runtimes of the Node.js family are supported. Default: - ``NODEJS_12_X`` if ``process.versions.node`` >= '12.0.0', ``NODEJS_10_X`` otherwise.

        stability
        :stability: experimental
        """
        if isinstance(current_version_options, dict):
            current_version_options = _VersionOptions_9a55a63d(**current_version_options)
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = _LogRetentionRetryOptions_09658088(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_36a13cd6(**vpc_subnets)
        self._values = {}
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if on_success is not None:
            self._values["on_success"] = on_success
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if allow_public_subnet is not None:
            self._values["allow_public_subnet"] = allow_public_subnet
        if current_version_options is not None:
            self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None:
            self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if description is not None:
            self._values["description"] = description
        if environment is not None:
            self._values["environment"] = environment
        if events is not None:
            self._values["events"] = events
        if filesystem is not None:
            self._values["filesystem"] = filesystem
        if function_name is not None:
            self._values["function_name"] = function_name
        if initial_policy is not None:
            self._values["initial_policy"] = initial_policy
        if layers is not None:
            self._values["layers"] = layers
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None:
            self._values["log_retention_role"] = log_retention_role
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if profiling is not None:
            self._values["profiling"] = profiling
        if profiling_group is not None:
            self._values["profiling_group"] = profiling_group
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing is not None:
            self._values["tracing"] = tracing
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if build_args is not None:
            self._values["build_args"] = build_args
        if cache_dir is not None:
            self._values["cache_dir"] = cache_dir
        if external_modules is not None:
            self._values["external_modules"] = external_modules
        if force_docker_bundling is not None:
            self._values["force_docker_bundling"] = force_docker_bundling
        if minify is not None:
            self._values["minify"] = minify
        if node_modules is not None:
            self._values["node_modules"] = node_modules
        if parcel_environment is not None:
            self._values["parcel_environment"] = parcel_environment
        if parcel_version is not None:
            self._values["parcel_version"] = parcel_version
        if project_root is not None:
            self._values["project_root"] = project_root
        if source_maps is not None:
            self._values["source_maps"] = source_maps
        if aws_sdk_connection_reuse is not None:
            self._values["aws_sdk_connection_reuse"] = aws_sdk_connection_reuse
        if entry is not None:
            self._values["entry"] = entry
        if handler is not None:
            self._values["handler"] = handler
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_5170c158]:
        """The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        default
        :default: Duration.hours(6)

        stability
        :stability: experimental
        """
        return self._values.get("max_event_age")

    @builtins.property
    def on_failure(self) -> typing.Optional[_IDestination_7081f282]:
        """The destination for failed invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get("on_failure")

    @builtins.property
    def on_success(self) -> typing.Optional[_IDestination_7081f282]:
        """The destination for successful invocations.

        default
        :default: - no destination

        stability
        :stability: experimental
        """
        return self._values.get("on_success")

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        """The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        default
        :default: 2

        stability
        :stability: experimental
        """
        return self._values.get("retry_attempts")

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[bool]:
        """Whether to allow the Lambda to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        default
        :default: true

        stability
        :stability: experimental
        """
        return self._values.get("allow_all_outbound")

    @builtins.property
    def allow_public_subnet(self) -> typing.Optional[bool]:
        """Lambda Functions in a public subnet can NOT access the internet.

        Use this property to acknowledge this limitation and still place the function in a public subnet.

        default
        :default: false

        see
        :see: https://stackoverflow.com/questions/52992085/why-cant-an-aws-lambda-function-inside-a-public-subnet-in-a-vpc-connect-to-the/52994841#52994841
        stability
        :stability: experimental
        """
        return self._values.get("allow_public_subnet")

    @builtins.property
    def current_version_options(self) -> typing.Optional[_VersionOptions_9a55a63d]:
        """Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        default
        :default: - default options as described in ``VersionOptions``

        stability
        :stability: experimental
        """
        return self._values.get("current_version_options")

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_b743f559]:
        """The SQS queue to use if DLQ is enabled.

        default
        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``

        stability
        :stability: experimental
        """
        return self._values.get("dead_letter_queue")

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[bool]:
        """Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        default
        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.

        stability
        :stability: experimental
        """
        return self._values.get("dead_letter_queue_enabled")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """A description of the function.

        default
        :default: - No description.

        stability
        :stability: experimental
        """
        return self._values.get("description")

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        default
        :default: - No environment variables.

        stability
        :stability: experimental
        """
        return self._values.get("environment")

    @builtins.property
    def events(self) -> typing.Optional[typing.List[_IEventSource_0e6bcb85]]:
        """Event sources for this function.

        You can also add event sources using ``addEventSource``.

        default
        :default: - No event sources.

        stability
        :stability: experimental
        """
        return self._values.get("events")

    @builtins.property
    def filesystem(self) -> typing.Optional[_FileSystem_132c0ce7]:
        """The filesystem configuration for the lambda function.

        default
        :default: - will not mount any filesystem

        stability
        :stability: experimental
        """
        return self._values.get("filesystem")

    @builtins.property
    def function_name(self) -> typing.Optional[str]:
        """A name for the function.

        default
        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
          ID for the function's name. For more information, see Name Type.

        stability
        :stability: experimental
        """
        return self._values.get("function_name")

    @builtins.property
    def initial_policy(self) -> typing.Optional[typing.List[_PolicyStatement_f75dc775]]:
        """Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        default
        :default: - No policy statements are added to the created Lambda role.

        stability
        :stability: experimental
        """
        return self._values.get("initial_policy")

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[_ILayerVersion_aa5e0c0c]]:
        """A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by mulitple functions.

        default
        :default: - No layers.

        stability
        :stability: experimental
        """
        return self._values.get("layers")

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_bdc7ad1f]:
        """The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        default
        :default: logs.RetentionDays.INFINITE

        stability
        :stability: experimental
        """
        return self._values.get("log_retention")

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional[_LogRetentionRetryOptions_09658088]:
        """When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        default
        :default: - Default AWS SDK retry options.

        stability
        :stability: experimental
        """
        return self._values.get("log_retention_retry_options")

    @builtins.property
    def log_retention_role(self) -> typing.Optional[_IRole_e69bbae4]:
        """The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        default
        :default: - A new role is created.

        stability
        :stability: experimental
        """
        return self._values.get("log_retention_role")

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        """The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        default
        :default: 128

        stability
        :stability: experimental
        """
        return self._values.get("memory_size")

    @builtins.property
    def profiling(self) -> typing.Optional[bool]:
        """Enable profiling.

        default
        :default: - No profiling.

        see
        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        stability
        :stability: experimental
        """
        return self._values.get("profiling")

    @builtins.property
    def profiling_group(self) -> typing.Optional[_IProfilingGroup_ca898ddc]:
        """Profiling Group.

        default
        :default: - A new profiling group will be created if ``profiling`` is set.

        see
        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        stability
        :stability: experimental
        """
        return self._values.get("profiling_group")

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        """The maximum of concurrent executions you want to reserve for the function.

        default
        :default: - No specific limit - account limit.

        see
        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        stability
        :stability: experimental
        """
        return self._values.get("reserved_concurrent_executions")

    @builtins.property
    def role(self) -> typing.Optional[_IRole_e69bbae4]:
        """Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        default
        :default:

        - A unique role will be generated for this lambda function.
          Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.

        stability
        :stability: experimental
        """
        return self._values.get("role")

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_d72ab8e8]:
        """What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead.

        Only used if 'vpc' is supplied.

        Use securityGroups property instead.
        Function constructor will throw an error if both are specified.

        default
        :default:

        - If the function is placed within a VPC and a security group is
          not specified, either by this or securityGroups prop, a dedicated security
          group will be created for this function.

        deprecated
        :deprecated: - This property is deprecated, use securityGroups instead

        stability
        :stability: deprecated
        """
        return self._values.get("security_group")

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_d72ab8e8]]:
        """The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        default
        :default:

        - If the function is placed within a VPC and a security group is
          not specified, either by this or securityGroup prop, a dedicated security
          group will be created for this function.

        stability
        :stability: experimental
        """
        return self._values.get("security_groups")

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_5170c158]:
        """The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        default
        :default: Duration.seconds(3)

        stability
        :stability: experimental
        """
        return self._values.get("timeout")

    @builtins.property
    def tracing(self) -> typing.Optional[_Tracing_34f0a955]:
        """Enable AWS X-Ray Tracing for Lambda Function.

        default
        :default: Tracing.Disabled

        stability
        :stability: experimental
        """
        return self._values.get("tracing")

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_3795853f]:
        """VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.

        default
        :default: - Function is not placed within a VPC.

        stability
        :stability: experimental
        """
        return self._values.get("vpc")

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_36a13cd6]:
        """Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied. Note: internet access for Lambdas
        requires a NAT gateway, so picking Public subnets is not allowed.

        default
        :default: - the Vpc default strategy if not specified

        stability
        :stability: experimental
        """
        return self._values.get("vpc_subnets")

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Build arguments to pass when building the bundling image.

        default
        :default: - no build arguments are passed

        stability
        :stability: experimental
        """
        return self._values.get("build_args")

    @builtins.property
    def cache_dir(self) -> typing.Optional[str]:
        """The cache directory (relative to the project root).

        Parcel uses a filesystem cache for fast rebuilds.

        default
        :default: - ``.parcel-cache`` in the working directory

        stability
        :stability: experimental
        """
        return self._values.get("cache_dir")

    @builtins.property
    def external_modules(self) -> typing.Optional[typing.List[str]]:
        """A list of modules that should be considered as externals (already available in the runtime).

        default
        :default: ['aws-sdk']

        stability
        :stability: experimental
        """
        return self._values.get("external_modules")

    @builtins.property
    def force_docker_bundling(self) -> typing.Optional[bool]:
        """Force bundling in a Docker container even if local bundling is possible.This  is useful if your function relies on node modules that should be installed (``nodeModules``) in a Lambda compatible environment.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("force_docker_bundling")

    @builtins.property
    def minify(self) -> typing.Optional[bool]:
        """Whether to minify files when bundling.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("minify")

    @builtins.property
    def node_modules(self) -> typing.Optional[typing.List[str]]:
        """A list of modules that should be installed instead of bundled.

        Modules are
        installed in a Lambda compatible environnment.

        default
        :default: - all modules are bundled

        stability
        :stability: experimental
        """
        return self._values.get("node_modules")

    @builtins.property
    def parcel_environment(self) -> typing.Optional[typing.Mapping[str, str]]:
        """Environment variables defined when Parcel runs.

        default
        :default: - no environment variables are defined.

        stability
        :stability: experimental
        """
        return self._values.get("parcel_environment")

    @builtins.property
    def parcel_version(self) -> typing.Optional[str]:
        """The version of Parcel to use when running in a Docker container.

        default
        :default: - 2.0.0-beta.1

        stability
        :stability: experimental
        """
        return self._values.get("parcel_version")

    @builtins.property
    def project_root(self) -> typing.Optional[str]:
        """The root of the project.

        This will be used as the source for the volume
        mounted in the Docker container. If you specify this prop, ensure that
        this path includes ``entry`` and any module/dependencies used by your
        function otherwise bundling will not be possible.

        default
        :default: - the closest path containing a .git folder

        stability
        :stability: experimental
        """
        return self._values.get("project_root")

    @builtins.property
    def source_maps(self) -> typing.Optional[bool]:
        """Whether to include source maps when bundling.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("source_maps")

    @builtins.property
    def aws_sdk_connection_reuse(self) -> typing.Optional[bool]:
        """Whether to automatically reuse TCP connections when working with the AWS SDK for JavaScript.

        This sets the ``AWS_NODEJS_CONNECTION_REUSE_ENABLED`` environment variable
        to ``1``.

        default
        :default: true

        see
        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/node-reusing-connections.html
        stability
        :stability: experimental
        """
        return self._values.get("aws_sdk_connection_reuse")

    @builtins.property
    def entry(self) -> typing.Optional[str]:
        """Path to the entry file (JavaScript or TypeScript).

        default
        :default:

        - Derived from the name of the defining file and the construct's id.
          If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id
          (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts``
          and ``stack.my-handler.js``.

        stability
        :stability: experimental
        """
        return self._values.get("entry")

    @builtins.property
    def handler(self) -> typing.Optional[str]:
        """The name of the exported handler in the entry file.

        default
        :default: handler

        stability
        :stability: experimental
        """
        return self._values.get("handler")

    @builtins.property
    def runtime(self) -> typing.Optional[_Runtime_8b970b80]:
        """The runtime environment.

        Only runtimes of the Node.js family are
        supported.

        default
        :default:

        - ``NODEJS_12_X`` if ``process.versions.node`` >= '12.0.0',
          ``NODEJS_10_X`` otherwise.

        stability
        :stability: experimental
        """
        return self._values.get("runtime")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodejsFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Bundling",
    "NodejsFunction",
    "NodejsFunctionProps",
    "ParcelBaseOptions",
    "ParcelOptions",
]

publication.publish()
