# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union
from .. import _utilities, _tables

__all__ = [
    'base_url',
    'cacert_file',
    'client_cert',
    'client_key',
    'insecure',
    'token',
]

__config__ = pulumi.Config('gitlab')

base_url = __config__.get('baseUrl') or _utilities.get_env('GITLAB_BASE_URL')
"""
The GitLab Base API URL
"""

cacert_file = __config__.get('cacertFile')
"""
A file containing the ca certificate to use in case ssl certificate is not from a standard chain
"""

client_cert = __config__.get('clientCert')
"""
File path to client certificate when GitLab instance is behind company proxy. File must contain PEM encoded data.
"""

client_key = __config__.get('clientKey')
"""
File path to client key when GitLab instance is behind company proxy. File must contain PEM encoded data.
"""

insecure = __config__.get('insecure')
"""
Disable SSL verification of API calls
"""

token = __config__.get('token') or _utilities.get_env('GITLAB_TOKEN')
"""
The OAuth token used to connect to GitLab.
"""

