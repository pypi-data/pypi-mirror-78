# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from . import _utilities, _tables

__all__ = ['DeployToken']


class DeployToken(pulumi.CustomResource):
    def __init__(__self__,
                 resource_name,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 expires_at: Optional[pulumi.Input[str]] = None,
                 group: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 scopes: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None,
                 __name__=None,
                 __opts__=None):
        """
        This resource allows you to create and manage deploy token for your GitLab projects and groups.

        ## Example Usage
        ### Project

        ```python
        import pulumi
        import pulumi_gitlab as gitlab

        example = gitlab.DeployToken("example",
            expires_at="2020-03-14T00:00:00.000Z",
            project="example/deploying",
            scopes=[
                "read_repository",
                "read_registry",
            ],
            username="example-username")
        ```
        ### Group

        ```python
        import pulumi
        import pulumi_gitlab as gitlab

        example = gitlab.DeployToken("example",
            group="example/deploying",
            scopes=["read_repository"])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group: The name or id of the group to add the deploy token to.
               Either `project` or `group` must be set.
        :param pulumi.Input[str] name: A name to describe the deploy token with.
        :param pulumi.Input[str] project: The name or id of the project to add the deploy token to.
               Either `project` or `group` must be set.
        :param pulumi.Input[List[pulumi.Input[str]]] scopes: Valid values: `read_repository`, `read_registry`.
        :param pulumi.Input[str] username: A username for the deploy token. Default is `gitlab+deploy-token-{n}`.
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

            __props__['expires_at'] = expires_at
            __props__['group'] = group
            __props__['name'] = name
            __props__['project'] = project
            if scopes is None:
                raise TypeError("Missing required property 'scopes'")
            __props__['scopes'] = scopes
            __props__['username'] = username
            __props__['token'] = None
        super(DeployToken, __self__).__init__(
            'gitlab:index/deployToken:DeployToken',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            expires_at: Optional[pulumi.Input[str]] = None,
            group: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            scopes: Optional[pulumi.Input[List[pulumi.Input[str]]]] = None,
            token: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'DeployToken':
        """
        Get an existing DeployToken resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] group: The name or id of the group to add the deploy token to.
               Either `project` or `group` must be set.
        :param pulumi.Input[str] name: A name to describe the deploy token with.
        :param pulumi.Input[str] project: The name or id of the project to add the deploy token to.
               Either `project` or `group` must be set.
        :param pulumi.Input[List[pulumi.Input[str]]] scopes: Valid values: `read_repository`, `read_registry`.
        :param pulumi.Input[str] token: The secret token. This is only populated when creating a new deploy token.
        :param pulumi.Input[str] username: A username for the deploy token. Default is `gitlab+deploy-token-{n}`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()

        __props__["expires_at"] = expires_at
        __props__["group"] = group
        __props__["name"] = name
        __props__["project"] = project
        __props__["scopes"] = scopes
        __props__["token"] = token
        __props__["username"] = username
        return DeployToken(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="expiresAt")
    def expires_at(self) -> Optional[str]:
        return pulumi.get(self, "expires_at")

    @property
    @pulumi.getter
    def group(self) -> Optional[str]:
        """
        The name or id of the group to add the deploy token to.
        Either `project` or `group` must be set.
        """
        return pulumi.get(self, "group")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        A name to describe the deploy token with.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> Optional[str]:
        """
        The name or id of the project to add the deploy token to.
        Either `project` or `group` must be set.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter
    def scopes(self) -> List[str]:
        """
        Valid values: `read_repository`, `read_registry`.
        """
        return pulumi.get(self, "scopes")

    @property
    @pulumi.getter
    def token(self) -> str:
        """
        The secret token. This is only populated when creating a new deploy token.
        """
        return pulumi.get(self, "token")

    @property
    @pulumi.getter
    def username(self) -> str:
        """
        A username for the deploy token. Default is `gitlab+deploy-token-{n}`.
        """
        return pulumi.get(self, "username")

    def translate_output_property(self, prop):
        return _tables.CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return _tables.SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

