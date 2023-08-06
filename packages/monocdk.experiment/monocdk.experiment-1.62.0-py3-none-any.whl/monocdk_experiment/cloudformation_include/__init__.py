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
    CfnCondition as _CfnCondition_548166d0,
    CfnElement as _CfnElement_54343cf1,
    CfnMapping as _CfnMapping_b46343a2,
    CfnOutput as _CfnOutput_1185605a,
    CfnParameter as _CfnParameter_90f1d0df,
    CfnResource as _CfnResource_7760e8e4,
    CfnRule as _CfnRule_a373f272,
    Construct as _Construct_f50a3f53,
    NestedStack as _NestedStack_e205561c,
)


class CfnInclude(
    _CfnElement_54343cf1,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk-experiment.cloudformation_include.CfnInclude",
):
    """Construct to import an existing CloudFormation template file into a CDK application.

    All resources defined in the template file can be retrieved by calling the {@link getResource} method.
    Any modifications made on the returned resource objects will be reflected in the resulting CDK template.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: _Construct_f50a3f53,
        id: str,
        *,
        template_file: str,
        nested_stacks: typing.Optional[typing.Mapping[str, "CfnIncludeProps"]] = None,
        parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param template_file: Path to the template file. Both JSON and YAML template formats are supported.
        :param nested_stacks: Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from {@link CfnInclude.getNestedStack}. If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced

        stability
        :stability: experimental
        """
        props = CfnIncludeProps(
            template_file=template_file,
            nested_stacks=nested_stacks,
            parameters=parameters,
        )

        jsii.create(CfnInclude, self, [scope, id, props])

    @jsii.member(jsii_name="getCondition")
    def get_condition(self, condition_name: str) -> _CfnCondition_548166d0:
        """Returns the CfnCondition object from the 'Conditions' section of the CloudFormation template with the given name.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Condition with the given name is not present in the template,
        throws an exception.

        :param condition_name: the name of the Condition in the CloudFormation template file.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getCondition", [condition_name])

    @jsii.member(jsii_name="getMapping")
    def get_mapping(self, mapping_name: str) -> _CfnMapping_b46343a2:
        """Returns the CfnMapping object from the 'Mappings' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Mapping with the given name is not present in the template,
        an exception will be thrown.

        :param mapping_name: the name of the Mapping in the template to retrieve.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getMapping", [mapping_name])

    @jsii.member(jsii_name="getNestedStack")
    def get_nested_stack(self, logical_id: str) -> "IncludedNestedStack":
        """Returns the NestedStack with name logicalId.

        For a nested stack to be returned by this method, it must be specified in the {@link CfnIncludeProps.nestedStacks}
        property.

        :param logical_id: the ID of the stack to retrieve, as it appears in the template.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getNestedStack", [logical_id])

    @jsii.member(jsii_name="getOutput")
    def get_output(self, logical_id: str) -> _CfnOutput_1185605a:
        """Returns the CfnOutput object from the 'Outputs' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If an Output with the given name is not present in the template,
        throws an exception.

        :param logical_id: the name of the output to retrieve.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getOutput", [logical_id])

    @jsii.member(jsii_name="getParameter")
    def get_parameter(self, parameter_name: str) -> _CfnParameter_90f1d0df:
        """Returns the CfnParameter object from the 'Parameters' section of the included template.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Parameter with the given name is not present in the template,
        throws an exception.

        :param parameter_name: the name of the parameter to retrieve.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getParameter", [parameter_name])

    @jsii.member(jsii_name="getResource")
    def get_resource(self, logical_id: str) -> _CfnResource_7760e8e4:
        """Returns the low-level CfnResource from the template with the given logical ID.

        Any modifications performed on that resource will be reflected in the resulting CDK template.

        The returned object will be of the proper underlying class;
        you can always cast it to the correct type in your code::

            // assume the template contains an AWS::S3::Bucket with logical ID 'Bucket'
            const cfnBucket = cfnTemplate.getResource('Bucket') as s3.CfnBucket;
            // cfnBucket is of type s3.CfnBucket

        If the template does not contain a resource with the given logical ID,
        an exception will be thrown.

        :param logical_id: the logical ID of the resource in the CloudFormation template file.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getResource", [logical_id])

    @jsii.member(jsii_name="getRule")
    def get_rule(self, rule_name: str) -> _CfnRule_a373f272:
        """Returns the CfnRule object from the 'Rules' section of the CloudFormation template with the given name.

        Any modifications performed on that object will be reflected in the resulting CDK template.

        If a Rule with the given name is not present in the template,
        an exception will be thrown.

        :param rule_name: the name of the Rule in the CloudFormation template.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getRule", [rule_name])


@jsii.data_type(
    jsii_type="monocdk-experiment.cloudformation_include.CfnIncludeProps",
    jsii_struct_bases=[],
    name_mapping={
        "template_file": "templateFile",
        "nested_stacks": "nestedStacks",
        "parameters": "parameters",
    },
)
class CfnIncludeProps:
    def __init__(
        self,
        *,
        template_file: str,
        nested_stacks: typing.Optional[typing.Mapping[str, "CfnIncludeProps"]] = None,
        parameters: typing.Optional[typing.Mapping[str, typing.Any]] = None,
    ) -> None:
        """Construction properties of {@link CfnInclude}.

        :param template_file: Path to the template file. Both JSON and YAML template formats are supported.
        :param nested_stacks: Specifies the template files that define nested stacks that should be included. If your template specifies a stack that isn't included here, it won't be created as a NestedStack resource, and it won't be accessible from {@link CfnInclude.getNestedStack}. If you include a stack here with an ID that isn't in the template, or is in the template but is not a nested stack, template creation will fail and an error will be thrown. Default: - no nested stacks will be included
        :param parameters: Specifies parameters to be replaced by the values in this mapping. Any parameters in the template that aren't specified here will be left unmodified. If you include a parameter here with an ID that isn't in the template, template creation will fail and an error will be thrown. Default: - no parameters will be replaced

        stability
        :stability: experimental
        """
        self._values = {
            "template_file": template_file,
        }
        if nested_stacks is not None:
            self._values["nested_stacks"] = nested_stacks
        if parameters is not None:
            self._values["parameters"] = parameters

    @builtins.property
    def template_file(self) -> str:
        """Path to the template file.

        Both JSON and YAML template formats are supported.

        stability
        :stability: experimental
        """
        return self._values.get("template_file")

    @builtins.property
    def nested_stacks(self) -> typing.Optional[typing.Mapping[str, "CfnIncludeProps"]]:
        """Specifies the template files that define nested stacks that should be included.

        If your template specifies a stack that isn't included here, it won't be created as a NestedStack
        resource, and it won't be accessible from {@link CfnInclude.getNestedStack}.

        If you include a stack here with an ID that isn't in the template,
        or is in the template but is not a nested stack,
        template creation will fail and an error will be thrown.

        default
        :default: - no nested stacks will be included

        stability
        :stability: experimental
        """
        return self._values.get("nested_stacks")

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """Specifies parameters to be replaced by the values in this mapping.

        Any parameters in the template that aren't specified here will be left unmodified.
        If you include a parameter here with an ID that isn't in the template,
        template creation will fail and an error will be thrown.

        default
        :default: - no parameters will be replaced

        stability
        :stability: experimental
        """
        return self._values.get("parameters")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnIncludeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk-experiment.cloudformation_include.IncludedNestedStack",
    jsii_struct_bases=[],
    name_mapping={"included_template": "includedTemplate", "stack": "stack"},
)
class IncludedNestedStack:
    def __init__(
        self, *, included_template: "CfnInclude", stack: _NestedStack_e205561c
    ) -> None:
        """The type returned from {@link CfnInclude.getNestedStack}. Contains both the NestedStack object and CfnInclude representations of the child stack.

        :param included_template: The CfnInclude that respresents the template, which can be used to access Resources and other template elements.
        :param stack: The NestedStack object which respresents the scope of the template.

        stability
        :stability: experimental
        """
        self._values = {
            "included_template": included_template,
            "stack": stack,
        }

    @builtins.property
    def included_template(self) -> "CfnInclude":
        """The CfnInclude that respresents the template, which can be used to access Resources and other template elements.

        stability
        :stability: experimental
        """
        return self._values.get("included_template")

    @builtins.property
    def stack(self) -> _NestedStack_e205561c:
        """The NestedStack object which respresents the scope of the template.

        stability
        :stability: experimental
        """
        return self._values.get("stack")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IncludedNestedStack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnInclude",
    "CfnIncludeProps",
    "IncludedNestedStack",
]

publication.publish()
