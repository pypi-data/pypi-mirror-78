# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from . import _utilities, _tables

__all__ = ['ProjectVariable']


class ProjectVariable(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 environment_scope: Optional[pulumi.Input[str]] = None,
                 key: Optional[pulumi.Input[str]] = None,
                 masked: Optional[pulumi.Input[bool]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 protected: Optional[pulumi.Input[bool]] = None,
                 value: Optional[pulumi.Input[str]] = None,
                 variable_type: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        This resource allows you to create and manage CI/CD variables for your GitLab projects.
        For further information on variables, consult the [gitlab
        documentation](https://docs.gitlab.com/ce/ci/variables/README.html#variables).

        ## Example Usage

        ```python
        import pulumi
        import pulumi_gitlab as gitlab

        example = gitlab.ProjectVariable("example",
            key="project_variable_key",
            project="12345",
            protected=False,
            value="project_variable_value")
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] environment_scope: The environment_scope of the variable
        :param pulumi.Input[str] key: The name of the variable.
        :param pulumi.Input[bool] masked: If set to `true`, the variable will be masked if it would have been written to the logs. Defaults to `false`.
        :param pulumi.Input[str] project: The name or id of the project to add the hook to.
        :param pulumi.Input[bool] protected: If set to `true`, the variable will be passed only to pipelines running on protected branches and tags. Defaults to `false`.
        :param pulumi.Input[str] value: The value of the variable.
        :param pulumi.Input[str] variable_type: The type of a variable. Available types are: env_var (default) and file.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['environment_scope'] = environment_scope
            if key is None:
                raise TypeError("Missing required property 'key'")
            __props__['key'] = key
            __props__['masked'] = masked
            if project is None:
                raise TypeError("Missing required property 'project'")
            __props__['project'] = project
            __props__['protected'] = protected
            if value is None:
                raise TypeError("Missing required property 'value'")
            __props__['value'] = value
            __props__['variable_type'] = variable_type
        super(ProjectVariable, __self__).__init__(
            'gitlab:index/projectVariable:ProjectVariable',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            environment_scope: Optional[pulumi.Input[str]] = None,
            key: Optional[pulumi.Input[str]] = None,
            masked: Optional[pulumi.Input[bool]] = None,
            project: Optional[pulumi.Input[str]] = None,
            protected: Optional[pulumi.Input[bool]] = None,
            value: Optional[pulumi.Input[str]] = None,
            variable_type: Optional[pulumi.Input[str]] = None) -> 'ProjectVariable':
        """
        Get an existing ProjectVariable resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] environment_scope: The environment_scope of the variable
        :param pulumi.Input[str] key: The name of the variable.
        :param pulumi.Input[bool] masked: If set to `true`, the variable will be masked if it would have been written to the logs. Defaults to `false`.
        :param pulumi.Input[str] project: The name or id of the project to add the hook to.
        :param pulumi.Input[bool] protected: If set to `true`, the variable will be passed only to pipelines running on protected branches and tags. Defaults to `false`.
        :param pulumi.Input[str] value: The value of the variable.
        :param pulumi.Input[str] variable_type: The type of a variable. Available types are: env_var (default) and file.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["environment_scope"] = environment_scope
        __props__["key"] = key
        __props__["masked"] = masked
        __props__["project"] = project
        __props__["protected"] = protected
        __props__["value"] = value
        __props__["variable_type"] = variable_type
        return ProjectVariable(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="environmentScope")
    def environment_scope(self) -> Optional[str]:
        """
        The environment_scope of the variable
        """
        return pulumi.get(self, "environment_scope")

    @property
    @pulumi.getter
    def key(self) -> str:
        """
        The name of the variable.
        """
        return pulumi.get(self, "key")

    @property
    @pulumi.getter
    def masked(self) -> Optional[bool]:
        """
        If set to `true`, the variable will be masked if it would have been written to the logs. Defaults to `false`.
        """
        return pulumi.get(self, "masked")

    @property
    @pulumi.getter
    def project(self) -> str:
        """
        The name or id of the project to add the hook to.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def protected(self) -> Optional[bool]:
        """
        If set to `true`, the variable will be passed only to pipelines running on protected branches and tags. Defaults to `false`.
        """
        return pulumi.get(self, "protected")

    @property
    @pulumi.getter
    def value(self) -> str:
        """
        The value of the variable.
        """
        return pulumi.get(self, "value")

    @property
    @pulumi.getter(name="variableType")
    def variable_type(self) -> Optional[str]:
        """
        The type of a variable. Available types are: env_var (default) and file.
        """
        return pulumi.get(self, "variable_type")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

