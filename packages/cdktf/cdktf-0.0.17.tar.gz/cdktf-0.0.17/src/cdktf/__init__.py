"""
# cdktf

cdktf is a framework for defining cloud infrastructure using Terraform providers and modules. It allows for
users to define infrastructure resources using higher-level programming languages.

## Build

Install dependencies

```bash
yarn install
```

Build the package

```bash
yarn build
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from ._jsii import *

import constructs


class App(constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktf.App"):
    """Represents a cdktf application.

    stability
    :stability: experimental
    """

    def __init__(
        self,
        *,
        outdir: typing.Optional[str] = None,
        stack_traces: typing.Optional[bool] = None,
    ) -> None:
        """Defines an app.

        :param outdir: The directory to output Terraform resources. Default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"
        :param stack_traces: 

        stability
        :stability: experimental
        """
        options = AppOptions(outdir=outdir, stack_traces=stack_traces)

        jsii.create(App, self, [options])

    @jsii.member(jsii_name="synth")
    def synth(self) -> None:
        """Synthesizes all resources to the output directory.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synth", [])

    @builtins.property
    @jsii.member(jsii_name="outdir")
    def outdir(self) -> str:
        """The output directory into which resources will be synthesized.

        stability
        :stability: experimental
        """
        return jsii.get(self, "outdir")


@jsii.data_type(
    jsii_type="cdktf.AppOptions",
    jsii_struct_bases=[],
    name_mapping={"outdir": "outdir", "stack_traces": "stackTraces"},
)
class AppOptions:
    def __init__(
        self,
        *,
        outdir: typing.Optional[str] = None,
        stack_traces: typing.Optional[bool] = None,
    ) -> None:
        """
        :param outdir: The directory to output Terraform resources. Default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"
        :param stack_traces: 

        stability
        :stability: experimental
        """
        self._values = {}
        if outdir is not None:
            self._values["outdir"] = outdir
        if stack_traces is not None:
            self._values["stack_traces"] = stack_traces

    @builtins.property
    def outdir(self) -> typing.Optional[str]:
        """The directory to output Terraform resources.

        default
        :default: - CDKTF_OUTDIR if defined, otherwise "cdktf.out"

        stability
        :stability: experimental
        """
        return self._values.get("outdir")

    @builtins.property
    def stack_traces(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("stack_traces")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.ArtifactoryBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "password": "password",
        "repo": "repo",
        "subpath": "subpath",
        "url": "url",
        "username": "username",
    },
)
class ArtifactoryBackendProps:
    def __init__(
        self, *, password: str, repo: str, subpath: str, url: str, username: str
    ) -> None:
        """
        :param password: 
        :param repo: 
        :param subpath: 
        :param url: 
        :param username: 

        stability
        :stability: experimental
        """
        self._values = {
            "password": password,
            "repo": repo,
            "subpath": subpath,
            "url": url,
            "username": username,
        }

    @builtins.property
    def password(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("password")

    @builtins.property
    def repo(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("repo")

    @builtins.property
    def subpath(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("subpath")

    @builtins.property
    def url(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("url")

    @builtins.property
    def username(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactoryBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.AzurermBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "container_name": "containerName",
        "key": "key",
        "storage_account_name": "storageAccountName",
        "access_key": "accessKey",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "endpoint": "endpoint",
        "environment": "environment",
        "msi_endpoint": "msiEndpoint",
        "resource_group_name": "resourceGroupName",
        "sas_token": "sasToken",
        "subscription_id": "subscriptionId",
        "tenant_id": "tenantId",
        "use_msi": "useMsi",
    },
)
class AzurermBackendProps:
    def __init__(
        self,
        *,
        container_name: str,
        key: str,
        storage_account_name: str,
        access_key: typing.Optional[str] = None,
        client_id: typing.Optional[str] = None,
        client_secret: typing.Optional[str] = None,
        endpoint: typing.Optional[str] = None,
        environment: typing.Optional[str] = None,
        msi_endpoint: typing.Optional[str] = None,
        resource_group_name: typing.Optional[str] = None,
        sas_token: typing.Optional[str] = None,
        subscription_id: typing.Optional[str] = None,
        tenant_id: typing.Optional[str] = None,
        use_msi: typing.Optional[bool] = None,
    ) -> None:
        """
        :param container_name: 
        :param key: 
        :param storage_account_name: 
        :param access_key: 
        :param client_id: 
        :param client_secret: 
        :param endpoint: 
        :param environment: 
        :param msi_endpoint: 
        :param resource_group_name: 
        :param sas_token: 
        :param subscription_id: 
        :param tenant_id: 
        :param use_msi: 

        stability
        :stability: experimental
        """
        self._values = {
            "container_name": container_name,
            "key": key,
            "storage_account_name": storage_account_name,
        }
        if access_key is not None:
            self._values["access_key"] = access_key
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if environment is not None:
            self._values["environment"] = environment
        if msi_endpoint is not None:
            self._values["msi_endpoint"] = msi_endpoint
        if resource_group_name is not None:
            self._values["resource_group_name"] = resource_group_name
        if sas_token is not None:
            self._values["sas_token"] = sas_token
        if subscription_id is not None:
            self._values["subscription_id"] = subscription_id
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if use_msi is not None:
            self._values["use_msi"] = use_msi

    @builtins.property
    def container_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("container_name")

    @builtins.property
    def key(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key")

    @builtins.property
    def storage_account_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("storage_account_name")

    @builtins.property
    def access_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("access_key")

    @builtins.property
    def client_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("client_id")

    @builtins.property
    def client_secret(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("client_secret")

    @builtins.property
    def endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("endpoint")

    @builtins.property
    def environment(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("environment")

    @builtins.property
    def msi_endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("msi_endpoint")

    @builtins.property
    def resource_group_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("resource_group_name")

    @builtins.property
    def sas_token(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("sas_token")

    @builtins.property
    def subscription_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("subscription_id")

    @builtins.property
    def tenant_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("tenant_id")

    @builtins.property
    def use_msi(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("use_msi")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AzurermBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BooleanMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.BooleanMap"):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self, terraform_resource: "ITerraformResource", terraform_attribute: str
    ) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        jsii.create(BooleanMap, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: str) -> bool:
        """
        :param key: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "lookup", [key])

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformAttribute")

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> "ITerraformResource":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResource")

    @_terraform_resource.setter
    def _terraform_resource(self, value: "ITerraformResource") -> None:
        jsii.set(self, "terraformResource", value)


class ComplexComputedList(
    metaclass=jsii.JSIIMeta, jsii_type="cdktf.ComplexComputedList"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        terraform_resource: "ITerraformResource",
        terraform_attribute: str,
        index: str,
    ) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -
        :param index: -

        stability
        :stability: experimental
        """
        jsii.create(ComplexComputedList, self, [terraform_resource, terraform_attribute, index])

    @jsii.member(jsii_name="getBooleanAttribute")
    def get_boolean_attribute(self, terraform_attribute: str) -> bool:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getBooleanAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getListAttribute")
    def get_list_attribute(self, terraform_attribute: str) -> typing.List[str]:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getListAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getNumberAttribute")
    def get_number_attribute(self, terraform_attribute: str) -> jsii.Number:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getNumberAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getStringAttribute")
    def get_string_attribute(self, terraform_attribute: str) -> str:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getStringAttribute", [terraform_attribute])

    @jsii.member(jsii_name="interpolationForAttribute")
    def _interpolation_for_attribute(self, property: str) -> str:
        """
        :param property: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "interpolationForAttribute", [property])

    @builtins.property
    @jsii.member(jsii_name="index")
    def _index(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "index")

    @_index.setter
    def _index(self, value: str) -> None:
        jsii.set(self, "index", value)

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformAttribute")

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> "ITerraformResource":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResource")

    @_terraform_resource.setter
    def _terraform_resource(self, value: "ITerraformResource") -> None:
        jsii.set(self, "terraformResource", value)


@jsii.data_type(
    jsii_type="cdktf.ConsulBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_token": "accessToken",
        "path": "path",
        "address": "address",
        "ca_file": "caFile",
        "cert_file": "certFile",
        "datacenter": "datacenter",
        "gzip": "gzip",
        "http_auth": "httpAuth",
        "key_file": "keyFile",
        "lock": "lock",
        "scheme": "scheme",
    },
)
class ConsulBackendProps:
    def __init__(
        self,
        *,
        access_token: str,
        path: str,
        address: typing.Optional[str] = None,
        ca_file: typing.Optional[str] = None,
        cert_file: typing.Optional[str] = None,
        datacenter: typing.Optional[str] = None,
        gzip: typing.Optional[bool] = None,
        http_auth: typing.Optional[str] = None,
        key_file: typing.Optional[str] = None,
        lock: typing.Optional[bool] = None,
        scheme: typing.Optional[str] = None,
    ) -> None:
        """
        :param access_token: 
        :param path: 
        :param address: 
        :param ca_file: 
        :param cert_file: 
        :param datacenter: 
        :param gzip: 
        :param http_auth: 
        :param key_file: 
        :param lock: 
        :param scheme: 

        stability
        :stability: experimental
        """
        self._values = {
            "access_token": access_token,
            "path": path,
        }
        if address is not None:
            self._values["address"] = address
        if ca_file is not None:
            self._values["ca_file"] = ca_file
        if cert_file is not None:
            self._values["cert_file"] = cert_file
        if datacenter is not None:
            self._values["datacenter"] = datacenter
        if gzip is not None:
            self._values["gzip"] = gzip
        if http_auth is not None:
            self._values["http_auth"] = http_auth
        if key_file is not None:
            self._values["key_file"] = key_file
        if lock is not None:
            self._values["lock"] = lock
        if scheme is not None:
            self._values["scheme"] = scheme

    @builtins.property
    def access_token(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("access_token")

    @builtins.property
    def path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("path")

    @builtins.property
    def address(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("address")

    @builtins.property
    def ca_file(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("ca_file")

    @builtins.property
    def cert_file(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("cert_file")

    @builtins.property
    def datacenter(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("datacenter")

    @builtins.property
    def gzip(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("gzip")

    @builtins.property
    def http_auth(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("http_auth")

    @builtins.property
    def key_file(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key_file")

    @builtins.property
    def lock(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lock")

    @builtins.property
    def scheme(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("scheme")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConsulBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.CosBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "acl": "acl",
        "encrypt": "encrypt",
        "key": "key",
        "prefix": "prefix",
        "region": "region",
        "secret_id": "secretId",
        "secret_key": "secretKey",
    },
)
class CosBackendProps:
    def __init__(
        self,
        *,
        bucket: str,
        acl: typing.Optional[str] = None,
        encrypt: typing.Optional[bool] = None,
        key: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
        secret_id: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
    ) -> None:
        """
        :param bucket: 
        :param acl: 
        :param encrypt: 
        :param key: 
        :param prefix: 
        :param region: 
        :param secret_id: 
        :param secret_key: 

        stability
        :stability: experimental
        """
        self._values = {
            "bucket": bucket,
        }
        if acl is not None:
            self._values["acl"] = acl
        if encrypt is not None:
            self._values["encrypt"] = encrypt
        if key is not None:
            self._values["key"] = key
        if prefix is not None:
            self._values["prefix"] = prefix
        if region is not None:
            self._values["region"] = region
        if secret_id is not None:
            self._values["secret_id"] = secret_id
        if secret_key is not None:
            self._values["secret_key"] = secret_key

    @builtins.property
    def bucket(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("bucket")

    @builtins.property
    def acl(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("acl")

    @builtins.property
    def encrypt(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("encrypt")

    @builtins.property
    def key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key")

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("prefix")

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("region")

    @builtins.property
    def secret_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("secret_id")

    @builtins.property
    def secret_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("secret_key")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CosBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateConfig",
    jsii_struct_bases=[],
    name_mapping={"defaults": "defaults", "workspace": "workspace"},
)
class DataTerraformRemoteStateConfig:
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 

        stability
        :stability: experimental
        """
        self._values = {}
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateConsulConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, ConsulBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "access_token": "accessToken",
        "path": "path",
        "address": "address",
        "ca_file": "caFile",
        "cert_file": "certFile",
        "datacenter": "datacenter",
        "gzip": "gzip",
        "http_auth": "httpAuth",
        "key_file": "keyFile",
        "lock": "lock",
        "scheme": "scheme",
    },
)
class DataTerraformRemoteStateConsulConfig(
    DataTerraformRemoteStateConfig, ConsulBackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        access_token: str,
        path: str,
        address: typing.Optional[str] = None,
        ca_file: typing.Optional[str] = None,
        cert_file: typing.Optional[str] = None,
        datacenter: typing.Optional[str] = None,
        gzip: typing.Optional[bool] = None,
        http_auth: typing.Optional[str] = None,
        key_file: typing.Optional[str] = None,
        lock: typing.Optional[bool] = None,
        scheme: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param access_token: 
        :param path: 
        :param address: 
        :param ca_file: 
        :param cert_file: 
        :param datacenter: 
        :param gzip: 
        :param http_auth: 
        :param key_file: 
        :param lock: 
        :param scheme: 

        stability
        :stability: experimental
        """
        self._values = {
            "access_token": access_token,
            "path": path,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if address is not None:
            self._values["address"] = address
        if ca_file is not None:
            self._values["ca_file"] = ca_file
        if cert_file is not None:
            self._values["cert_file"] = cert_file
        if datacenter is not None:
            self._values["datacenter"] = datacenter
        if gzip is not None:
            self._values["gzip"] = gzip
        if http_auth is not None:
            self._values["http_auth"] = http_auth
        if key_file is not None:
            self._values["key_file"] = key_file
        if lock is not None:
            self._values["lock"] = lock
        if scheme is not None:
            self._values["scheme"] = scheme

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def access_token(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("access_token")

    @builtins.property
    def path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("path")

    @builtins.property
    def address(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("address")

    @builtins.property
    def ca_file(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("ca_file")

    @builtins.property
    def cert_file(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("cert_file")

    @builtins.property
    def datacenter(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("datacenter")

    @builtins.property
    def gzip(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("gzip")

    @builtins.property
    def http_auth(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("http_auth")

    @builtins.property
    def key_file(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key_file")

    @builtins.property
    def lock(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lock")

    @builtins.property
    def scheme(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("scheme")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateConsulConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateCosConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, CosBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "bucket": "bucket",
        "acl": "acl",
        "encrypt": "encrypt",
        "key": "key",
        "prefix": "prefix",
        "region": "region",
        "secret_id": "secretId",
        "secret_key": "secretKey",
    },
)
class DataTerraformRemoteStateCosConfig(
    DataTerraformRemoteStateConfig, CosBackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        bucket: str,
        acl: typing.Optional[str] = None,
        encrypt: typing.Optional[bool] = None,
        key: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
        secret_id: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param bucket: 
        :param acl: 
        :param encrypt: 
        :param key: 
        :param prefix: 
        :param region: 
        :param secret_id: 
        :param secret_key: 

        stability
        :stability: experimental
        """
        self._values = {
            "bucket": bucket,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if acl is not None:
            self._values["acl"] = acl
        if encrypt is not None:
            self._values["encrypt"] = encrypt
        if key is not None:
            self._values["key"] = key
        if prefix is not None:
            self._values["prefix"] = prefix
        if region is not None:
            self._values["region"] = region
        if secret_id is not None:
            self._values["secret_id"] = secret_id
        if secret_key is not None:
            self._values["secret_key"] = secret_key

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def bucket(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("bucket")

    @builtins.property
    def acl(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("acl")

    @builtins.property
    def encrypt(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("encrypt")

    @builtins.property
    def key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key")

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("prefix")

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("region")

    @builtins.property
    def secret_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("secret_id")

    @builtins.property
    def secret_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("secret_key")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateCosConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.EncodingOptions",
    jsii_struct_bases=[],
    name_mapping={"display_hint": "displayHint"},
)
class EncodingOptions:
    def __init__(self, *, display_hint: typing.Optional[str] = None) -> None:
        """Properties to string encodings.

        :param display_hint: A hint for the Token's purpose when stringifying it. Default: - no display hint

        stability
        :stability: experimental
        """
        self._values = {}
        if display_hint is not None:
            self._values["display_hint"] = display_hint

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """A hint for the Token's purpose when stringifying it.

        default
        :default: - no display hint

        stability
        :stability: experimental
        """
        return self._values.get("display_hint")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EncodingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.EtcdBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "endpoints": "endpoints",
        "path": "path",
        "password": "password",
        "username": "username",
    },
)
class EtcdBackendProps:
    def __init__(
        self,
        *,
        endpoints: str,
        path: str,
        password: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param endpoints: 
        :param path: 
        :param password: 
        :param username: 

        stability
        :stability: experimental
        """
        self._values = {
            "endpoints": endpoints,
            "path": path,
        }
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def endpoints(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("endpoints")

    @builtins.property
    def path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("path")

    @builtins.property
    def password(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("password")

    @builtins.property
    def username(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EtcdBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.EtcdV3BackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "endpoints": "endpoints",
        "cacert_path": "cacertPath",
        "cert_path": "certPath",
        "key_path": "keyPath",
        "lock": "lock",
        "password": "password",
        "prefix": "prefix",
        "username": "username",
    },
)
class EtcdV3BackendProps:
    def __init__(
        self,
        *,
        endpoints: typing.List[str],
        cacert_path: typing.Optional[str] = None,
        cert_path: typing.Optional[str] = None,
        key_path: typing.Optional[str] = None,
        lock: typing.Optional[bool] = None,
        password: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param endpoints: 
        :param cacert_path: 
        :param cert_path: 
        :param key_path: 
        :param lock: 
        :param password: 
        :param prefix: 
        :param username: 

        stability
        :stability: experimental
        """
        self._values = {
            "endpoints": endpoints,
        }
        if cacert_path is not None:
            self._values["cacert_path"] = cacert_path
        if cert_path is not None:
            self._values["cert_path"] = cert_path
        if key_path is not None:
            self._values["key_path"] = key_path
        if lock is not None:
            self._values["lock"] = lock
        if password is not None:
            self._values["password"] = password
        if prefix is not None:
            self._values["prefix"] = prefix
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def endpoints(self) -> typing.List[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("endpoints")

    @builtins.property
    def cacert_path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("cacert_path")

    @builtins.property
    def cert_path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("cert_path")

    @builtins.property
    def key_path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key_path")

    @builtins.property
    def lock(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lock")

    @builtins.property
    def password(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("password")

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("prefix")

    @builtins.property
    def username(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EtcdV3BackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.GcsBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "access_token": "accessToken",
        "credentials": "credentials",
        "encryption_key": "encryptionKey",
        "prefix": "prefix",
    },
)
class GcsBackendProps:
    def __init__(
        self,
        *,
        bucket: str,
        access_token: typing.Optional[str] = None,
        credentials: typing.Optional[str] = None,
        encryption_key: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
    ) -> None:
        """
        :param bucket: 
        :param access_token: 
        :param credentials: 
        :param encryption_key: 
        :param prefix: 

        stability
        :stability: experimental
        """
        self._values = {
            "bucket": bucket,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if credentials is not None:
            self._values["credentials"] = credentials
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def bucket(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("bucket")

    @builtins.property
    def access_token(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("access_token")

    @builtins.property
    def credentials(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("credentials")

    @builtins.property
    def encryption_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("encryption_key")

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("prefix")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GcsBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.HttpBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "address": "address",
        "lock_address": "lockAddress",
        "lock_method": "lockMethod",
        "password": "password",
        "retry_max": "retryMax",
        "retry_wait_max": "retryWaitMax",
        "retry_wait_min": "retryWaitMin",
        "skip_cert_verification": "skipCertVerification",
        "unlock_address": "unlockAddress",
        "unlock_method": "unlockMethod",
        "update_method": "updateMethod",
        "username": "username",
    },
)
class HttpBackendProps:
    def __init__(
        self,
        *,
        address: str,
        lock_address: typing.Optional[str] = None,
        lock_method: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        retry_max: typing.Optional[jsii.Number] = None,
        retry_wait_max: typing.Optional[jsii.Number] = None,
        retry_wait_min: typing.Optional[jsii.Number] = None,
        skip_cert_verification: typing.Optional[bool] = None,
        unlock_address: typing.Optional[str] = None,
        unlock_method: typing.Optional[str] = None,
        update_method: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param address: 
        :param lock_address: 
        :param lock_method: 
        :param password: 
        :param retry_max: 
        :param retry_wait_max: 
        :param retry_wait_min: 
        :param skip_cert_verification: 
        :param unlock_address: 
        :param unlock_method: 
        :param update_method: 
        :param username: 

        stability
        :stability: experimental
        """
        self._values = {
            "address": address,
        }
        if lock_address is not None:
            self._values["lock_address"] = lock_address
        if lock_method is not None:
            self._values["lock_method"] = lock_method
        if password is not None:
            self._values["password"] = password
        if retry_max is not None:
            self._values["retry_max"] = retry_max
        if retry_wait_max is not None:
            self._values["retry_wait_max"] = retry_wait_max
        if retry_wait_min is not None:
            self._values["retry_wait_min"] = retry_wait_min
        if skip_cert_verification is not None:
            self._values["skip_cert_verification"] = skip_cert_verification
        if unlock_address is not None:
            self._values["unlock_address"] = unlock_address
        if unlock_method is not None:
            self._values["unlock_method"] = unlock_method
        if update_method is not None:
            self._values["update_method"] = update_method
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def address(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("address")

    @builtins.property
    def lock_address(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lock_address")

    @builtins.property
    def lock_method(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lock_method")

    @builtins.property
    def password(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("password")

    @builtins.property
    def retry_max(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("retry_max")

    @builtins.property
    def retry_wait_max(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("retry_wait_max")

    @builtins.property
    def retry_wait_min(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("retry_wait_min")

    @builtins.property
    def skip_cert_verification(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("skip_cert_verification")

    @builtins.property
    def unlock_address(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("unlock_address")

    @builtins.property
    def unlock_method(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("unlock_method")

    @builtins.property
    def update_method(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("update_method")

    @builtins.property
    def username(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdktf.IAnyProducer")
class IAnyProducer(jsii.compat.Protocol):
    """Interface for lazy untyped value producers.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IAnyProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Any:
        """Produce the value.

        :param context: -

        stability
        :stability: experimental
        """
        ...


class _IAnyProducerProxy:
    """Interface for lazy untyped value producers.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.IAnyProducer"

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Any:
        """Produce the value.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="cdktf.IFragmentConcatenator")
class IFragmentConcatenator(jsii.compat.Protocol):
    """Function used to concatenate symbols in the target document language.

    Interface so it could potentially be exposed over jsii.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IFragmentConcatenatorProxy

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        ...


class _IFragmentConcatenatorProxy:
    """Function used to concatenate symbols in the target document language.

    Interface so it could potentially be exposed over jsii.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.IFragmentConcatenator"

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "join", [left, right])


@jsii.interface(jsii_type="cdktf.IListProducer")
class IListProducer(jsii.compat.Protocol):
    """Interface for lazy list producers.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IListProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[typing.List[str]]:
        """Produce the list value.

        :param context: -

        stability
        :stability: experimental
        """
        ...


class _IListProducerProxy:
    """Interface for lazy list producers.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.IListProducer"

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[typing.List[str]]:
        """Produce the list value.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="cdktf.INumberProducer")
class INumberProducer(jsii.compat.Protocol):
    """Interface for lazy number producers.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _INumberProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[jsii.Number]:
        """Produce the number value.

        :param context: -

        stability
        :stability: experimental
        """
        ...


class _INumberProducerProxy:
    """Interface for lazy number producers.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.INumberProducer"

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[jsii.Number]:
        """Produce the number value.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="cdktf.IPostProcessor")
class IPostProcessor(jsii.compat.Protocol):
    """A Token that can post-process the complete resolved value, after resolve() has recursed over it.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IPostProcessorProxy

    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, context: "IResolveContext") -> typing.Any:
        """Process the completely resolved value, after full recursion/resolution has happened.

        :param input: -
        :param context: -

        stability
        :stability: experimental
        """
        ...


class _IPostProcessorProxy:
    """A Token that can post-process the complete resolved value, after resolve() has recursed over it.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.IPostProcessor"

    @jsii.member(jsii_name="postProcess")
    def post_process(self, input: typing.Any, context: "IResolveContext") -> typing.Any:
        """Process the completely resolved value, after full recursion/resolution has happened.

        :param input: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "postProcess", [input, context])


@jsii.interface(jsii_type="cdktf.IRemoteWorkspace")
class IRemoteWorkspace(jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IRemoteWorkspaceProxy


class _IRemoteWorkspaceProxy:
    """
    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.IRemoteWorkspace"
    pass


@jsii.interface(jsii_type="cdktf.IResolvable")
class IResolvable(jsii.compat.Protocol):
    """Interface for values that can be resolvable later.

    Tokens are special objects that participate in synthesis.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResolvableProxy

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param context: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return a string representation of this resolvable object.

        Returns a reversible string representation.

        stability
        :stability: experimental
        """
        ...


class _IResolvableProxy:
    """Interface for values that can be resolvable later.

    Tokens are special objects that participate in synthesis.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.IResolvable"

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[str]:
        """The creation stack of this resolvable which will be appended to errors thrown during resolution.

        If this returns an empty array the stack will not be attached.

        stability
        :stability: experimental
        """
        return jsii.get(self, "creationStack")

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: "IResolveContext") -> typing.Any:
        """Produce the Token's value at resolution time.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolve", [context])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return a string representation of this resolvable object.

        Returns a reversible string representation.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toString", [])


@jsii.interface(jsii_type="cdktf.IResolveContext")
class IResolveContext(jsii.compat.Protocol):
    """Current resolution context for tokens.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResolveContextProxy

    @builtins.property
    @jsii.member(jsii_name="preparing")
    def preparing(self) -> bool:
        """True when we are still preparing, false if we're rendering the final output.

        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> constructs.IConstruct:
        """The scope from which resolution has been initiated.

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="registerPostProcessor")
    def register_post_processor(self, post_processor: "IPostProcessor") -> None:
        """Use this postprocessor after the entire token structure has been resolved.

        :param post_processor: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="resolve")
    def resolve(self, x: typing.Any) -> typing.Any:
        """Resolve an inner object.

        :param x: -

        stability
        :stability: experimental
        """
        ...


class _IResolveContextProxy:
    """Current resolution context for tokens.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.IResolveContext"

    @builtins.property
    @jsii.member(jsii_name="preparing")
    def preparing(self) -> bool:
        """True when we are still preparing, false if we're rendering the final output.

        stability
        :stability: experimental
        """
        return jsii.get(self, "preparing")

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> constructs.IConstruct:
        """The scope from which resolution has been initiated.

        stability
        :stability: experimental
        """
        return jsii.get(self, "scope")

    @jsii.member(jsii_name="registerPostProcessor")
    def register_post_processor(self, post_processor: "IPostProcessor") -> None:
        """Use this postprocessor after the entire token structure has been resolved.

        :param post_processor: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "registerPostProcessor", [post_processor])

    @jsii.member(jsii_name="resolve")
    def resolve(self, x: typing.Any) -> typing.Any:
        """Resolve an inner object.

        :param x: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolve", [x])


@jsii.interface(jsii_type="cdktf.IResource")
class IResource(constructs.IConstruct, jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IResourceProxy

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "TerraformStack":
        """The stack in which this resource is defined.

        stability
        :stability: experimental
        """
        ...


class _IResourceProxy(jsii.proxy_for(constructs.IConstruct)):
    """
    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.IResource"

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "TerraformStack":
        """The stack in which this resource is defined.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stack")


@jsii.interface(jsii_type="cdktf.IStringProducer")
class IStringProducer(jsii.compat.Protocol):
    """Interface for lazy string producers.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _IStringProducerProxy

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[str]:
        """Produce the string value.

        :param context: -

        stability
        :stability: experimental
        """
        ...


class _IStringProducerProxy:
    """Interface for lazy string producers.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.IStringProducer"

    @jsii.member(jsii_name="produce")
    def produce(self, context: "IResolveContext") -> typing.Optional[str]:
        """Produce the string value.

        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "produce", [context])


@jsii.interface(jsii_type="cdktf.ITerraformResource")
class ITerraformResource(jsii.compat.Protocol):
    """
    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITerraformResourceProxy

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="friendlyUniqueId")
    def friendly_unique_id(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        ...

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        ...

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[str]]:
        """
        stability
        :stability: experimental
        """
        ...

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[str]]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        ...

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional["TerraformResourceLifecycle"]) -> None:
        ...

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        ...

    @provider.setter
    def provider(self, value: typing.Optional["TerraformProvider"]) -> None:
        ...

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(self, terraform_attribute: str) -> str:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        ...


class _ITerraformResourceProxy:
    """
    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.ITerraformResource"

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "fqn")

    @builtins.property
    @jsii.member(jsii_name="friendlyUniqueId")
    def friendly_unique_id(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "friendlyUniqueId")

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResourceType")

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "count")

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[str]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "dependsOn")

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "lifecycle")

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional["TerraformResourceLifecycle"]) -> None:
        jsii.set(self, "lifecycle", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "provider")

    @provider.setter
    def provider(self, value: typing.Optional["TerraformProvider"]) -> None:
        jsii.set(self, "provider", value)

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(self, terraform_attribute: str) -> str:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "interpolationForAttribute", [terraform_attribute])


@jsii.interface(jsii_type="cdktf.ITokenMapper")
class ITokenMapper(jsii.compat.Protocol):
    """Interface to apply operation to tokens in a string.

    Interface so it can be exported via jsii.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITokenMapperProxy

    @jsii.member(jsii_name="mapToken")
    def map_token(self, t: "IResolvable") -> typing.Any:
        """Replace a single token.

        :param t: -

        stability
        :stability: experimental
        """
        ...


class _ITokenMapperProxy:
    """Interface to apply operation to tokens in a string.

    Interface so it can be exported via jsii.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.ITokenMapper"

    @jsii.member(jsii_name="mapToken")
    def map_token(self, t: "IResolvable") -> typing.Any:
        """Replace a single token.

        :param t: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "mapToken", [t])


@jsii.interface(jsii_type="cdktf.ITokenResolver")
class ITokenResolver(jsii.compat.Protocol):
    """How to resolve tokens.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ITokenResolverProxy

    @jsii.member(jsii_name="resolveList")
    def resolve_list(
        self, l: typing.List[str], context: "IResolveContext"
    ) -> typing.Any:
        """Resolve a tokenized list.

        :param l: -
        :param context: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="resolveString")
    def resolve_string(
        self, s: "TokenizedStringFragments", context: "IResolveContext"
    ) -> typing.Any:
        """Resolve a string with at least one stringified token in it.

        (May use concatenation)

        :param s: -
        :param context: -

        stability
        :stability: experimental
        """
        ...

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(
        self,
        t: "IResolvable",
        context: "IResolveContext",
        post_processor: "IPostProcessor",
    ) -> typing.Any:
        """Resolve a single token.

        :param t: -
        :param context: -
        :param post_processor: -

        stability
        :stability: experimental
        """
        ...


class _ITokenResolverProxy:
    """How to resolve tokens.

    stability
    :stability: experimental
    """

    __jsii_type__ = "cdktf.ITokenResolver"

    @jsii.member(jsii_name="resolveList")
    def resolve_list(
        self, l: typing.List[str], context: "IResolveContext"
    ) -> typing.Any:
        """Resolve a tokenized list.

        :param l: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveList", [l, context])

    @jsii.member(jsii_name="resolveString")
    def resolve_string(
        self, s: "TokenizedStringFragments", context: "IResolveContext"
    ) -> typing.Any:
        """Resolve a string with at least one stringified token in it.

        (May use concatenation)

        :param s: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveString", [s, context])

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(
        self,
        t: "IResolvable",
        context: "IResolveContext",
        post_processor: "IPostProcessor",
    ) -> typing.Any:
        """Resolve a single token.

        :param t: -
        :param context: -
        :param post_processor: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveToken", [t, context, post_processor])


class Lazy(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Lazy"):
    """Lazily produce a value.

    Can be used to return a string, list or numeric value whose actual value
    will only be calculated later, during synthesis.

    stability
    :stability: experimental
    """

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(Lazy, self, [])

    @jsii.member(jsii_name="anyValue")
    @builtins.classmethod
    def any_value(
        cls,
        producer: "IAnyProducer",
        *,
        display_hint: typing.Optional[str] = None,
        omit_empty_array: typing.Optional[bool] = None,
    ) -> "IResolvable":
        """Produces a lazy token from an untyped value.

        :param producer: The lazy producer.
        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty_array: If the produced value is an array and it is empty, return 'undefined' instead. Default: false

        stability
        :stability: experimental
        """
        options = LazyAnyValueOptions(
            display_hint=display_hint, omit_empty_array=omit_empty_array
        )

        return jsii.sinvoke(cls, "anyValue", [producer, options])

    @jsii.member(jsii_name="listValue")
    @builtins.classmethod
    def list_value(
        cls,
        producer: "IListProducer",
        *,
        display_hint: typing.Optional[str] = None,
        omit_empty: typing.Optional[bool] = None,
    ) -> typing.List[str]:
        """Returns a list-ified token for a lazy value.

        :param producer: The producer.
        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty: If the produced list is empty, return 'undefined' instead. Default: false

        stability
        :stability: experimental
        """
        options = LazyListValueOptions(
            display_hint=display_hint, omit_empty=omit_empty
        )

        return jsii.sinvoke(cls, "listValue", [producer, options])

    @jsii.member(jsii_name="numberValue")
    @builtins.classmethod
    def number_value(cls, producer: "INumberProducer") -> jsii.Number:
        """Returns a numberified token for a lazy value.

        :param producer: The producer.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "numberValue", [producer])

    @jsii.member(jsii_name="stringValue")
    @builtins.classmethod
    def string_value(
        cls, producer: "IStringProducer", *, display_hint: typing.Optional[str] = None
    ) -> str:
        """Returns a stringified token for a lazy value.

        :param producer: The producer.
        :param display_hint: Use the given name as a display hint. Default: - No hint

        stability
        :stability: experimental
        """
        options = LazyStringValueOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "stringValue", [producer, options])


@jsii.data_type(
    jsii_type="cdktf.LazyAnyValueOptions",
    jsii_struct_bases=[],
    name_mapping={"display_hint": "displayHint", "omit_empty_array": "omitEmptyArray"},
)
class LazyAnyValueOptions:
    def __init__(
        self,
        *,
        display_hint: typing.Optional[str] = None,
        omit_empty_array: typing.Optional[bool] = None,
    ) -> None:
        """Options for creating lazy untyped tokens.

        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty_array: If the produced value is an array and it is empty, return 'undefined' instead. Default: false

        stability
        :stability: experimental
        """
        self._values = {}
        if display_hint is not None:
            self._values["display_hint"] = display_hint
        if omit_empty_array is not None:
            self._values["omit_empty_array"] = omit_empty_array

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint

        stability
        :stability: experimental
        """
        return self._values.get("display_hint")

    @builtins.property
    def omit_empty_array(self) -> typing.Optional[bool]:
        """If the produced value is an array and it is empty, return 'undefined' instead.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("omit_empty_array")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LazyAnyValueOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.LazyListValueOptions",
    jsii_struct_bases=[],
    name_mapping={"display_hint": "displayHint", "omit_empty": "omitEmpty"},
)
class LazyListValueOptions:
    def __init__(
        self,
        *,
        display_hint: typing.Optional[str] = None,
        omit_empty: typing.Optional[bool] = None,
    ) -> None:
        """Options for creating a lazy list token.

        :param display_hint: Use the given name as a display hint. Default: - No hint
        :param omit_empty: If the produced list is empty, return 'undefined' instead. Default: false

        stability
        :stability: experimental
        """
        self._values = {}
        if display_hint is not None:
            self._values["display_hint"] = display_hint
        if omit_empty is not None:
            self._values["omit_empty"] = omit_empty

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint

        stability
        :stability: experimental
        """
        return self._values.get("display_hint")

    @builtins.property
    def omit_empty(self) -> typing.Optional[bool]:
        """If the produced list is empty, return 'undefined' instead.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("omit_empty")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LazyListValueOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.LazyStringValueOptions",
    jsii_struct_bases=[],
    name_mapping={"display_hint": "displayHint"},
)
class LazyStringValueOptions:
    def __init__(self, *, display_hint: typing.Optional[str] = None) -> None:
        """Options for creating a lazy string token.

        :param display_hint: Use the given name as a display hint. Default: - No hint

        stability
        :stability: experimental
        """
        self._values = {}
        if display_hint is not None:
            self._values["display_hint"] = display_hint

    @builtins.property
    def display_hint(self) -> typing.Optional[str]:
        """Use the given name as a display hint.

        default
        :default: - No hint

        stability
        :stability: experimental
        """
        return self._values.get("display_hint")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LazyStringValueOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.LocalBackendProps",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "workspace_dir": "workspaceDir"},
)
class LocalBackendProps:
    def __init__(
        self,
        *,
        path: typing.Optional[str] = None,
        workspace_dir: typing.Optional[str] = None,
    ) -> None:
        """
        :param path: 
        :param workspace_dir: 

        stability
        :stability: experimental
        """
        self._values = {}
        if path is not None:
            self._values["path"] = path
        if workspace_dir is not None:
            self._values["workspace_dir"] = workspace_dir

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("path")

    @builtins.property
    def workspace_dir(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace_dir")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LocalBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.MantaBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "key_id": "keyId",
        "path": "path",
        "insecure_skip_tls_verify": "insecureSkipTlsVerify",
        "key_material": "keyMaterial",
        "object_name": "objectName",
        "url": "url",
        "user": "user",
    },
)
class MantaBackendProps:
    def __init__(
        self,
        *,
        account: str,
        key_id: str,
        path: str,
        insecure_skip_tls_verify: typing.Optional[bool] = None,
        key_material: typing.Optional[str] = None,
        object_name: typing.Optional[str] = None,
        url: typing.Optional[str] = None,
        user: typing.Optional[str] = None,
    ) -> None:
        """
        :param account: 
        :param key_id: 
        :param path: 
        :param insecure_skip_tls_verify: 
        :param key_material: 
        :param object_name: 
        :param url: 
        :param user: 

        stability
        :stability: experimental
        """
        self._values = {
            "account": account,
            "key_id": key_id,
            "path": path,
        }
        if insecure_skip_tls_verify is not None:
            self._values["insecure_skip_tls_verify"] = insecure_skip_tls_verify
        if key_material is not None:
            self._values["key_material"] = key_material
        if object_name is not None:
            self._values["object_name"] = object_name
        if url is not None:
            self._values["url"] = url
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def account(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("account")

    @builtins.property
    def key_id(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key_id")

    @builtins.property
    def path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("path")

    @builtins.property
    def insecure_skip_tls_verify(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("insecure_skip_tls_verify")

    @builtins.property
    def key_material(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key_material")

    @builtins.property
    def object_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("object_name")

    @builtins.property
    def url(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("url")

    @builtins.property
    def user(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("user")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MantaBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRemoteWorkspace)
class NamedRemoteWorkspace(
    metaclass=jsii.JSIIMeta, jsii_type="cdktf.NamedRemoteWorkspace"
):
    """
    stability
    :stability: experimental
    """

    def __init__(self, name: str) -> None:
        """
        :param name: -

        stability
        :stability: experimental
        """
        jsii.create(NamedRemoteWorkspace, self, [name])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str) -> None:
        jsii.set(self, "name", value)


class NumberMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.NumberMap"):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self, terraform_resource: "ITerraformResource", terraform_attribute: str
    ) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        jsii.create(NumberMap, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: str) -> jsii.Number:
        """
        :param key: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "lookup", [key])

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformAttribute")

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> "ITerraformResource":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResource")

    @_terraform_resource.setter
    def _terraform_resource(self, value: "ITerraformResource") -> None:
        jsii.set(self, "terraformResource", value)


@jsii.data_type(
    jsii_type="cdktf.OssAssumeRole",
    jsii_struct_bases=[],
    name_mapping={
        "role_arn": "roleArn",
        "policy": "policy",
        "session_expiration": "sessionExpiration",
        "session_name": "sessionName",
    },
)
class OssAssumeRole:
    def __init__(
        self,
        *,
        role_arn: str,
        policy: typing.Optional[str] = None,
        session_expiration: typing.Optional[jsii.Number] = None,
        session_name: typing.Optional[str] = None,
    ) -> None:
        """
        :param role_arn: 
        :param policy: 
        :param session_expiration: 
        :param session_name: 

        stability
        :stability: experimental
        """
        self._values = {
            "role_arn": role_arn,
        }
        if policy is not None:
            self._values["policy"] = policy
        if session_expiration is not None:
            self._values["session_expiration"] = session_expiration
        if session_name is not None:
            self._values["session_name"] = session_name

    @builtins.property
    def role_arn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("role_arn")

    @builtins.property
    def policy(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("policy")

    @builtins.property
    def session_expiration(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("session_expiration")

    @builtins.property
    def session_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("session_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OssAssumeRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.OssBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "access_key": "accessKey",
        "acl": "acl",
        "assume_role": "assumeRole",
        "ecs_role_name": "ecsRoleName",
        "encrypt": "encrypt",
        "endpoint": "endpoint",
        "key": "key",
        "prefix": "prefix",
        "profile": "profile",
        "region": "region",
        "secret_key": "secretKey",
        "security_token": "securityToken",
        "shared_credentials_file": "sharedCredentialsFile",
        "tablestore_endpoint": "tablestoreEndpoint",
        "tablestore_table": "tablestoreTable",
    },
)
class OssBackendProps:
    def __init__(
        self,
        *,
        bucket: str,
        access_key: typing.Optional[str] = None,
        acl: typing.Optional[str] = None,
        assume_role: typing.Optional["OssAssumeRole"] = None,
        ecs_role_name: typing.Optional[str] = None,
        encrypt: typing.Optional[bool] = None,
        endpoint: typing.Optional[str] = None,
        key: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
        profile: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
        security_token: typing.Optional[str] = None,
        shared_credentials_file: typing.Optional[str] = None,
        tablestore_endpoint: typing.Optional[str] = None,
        tablestore_table: typing.Optional[str] = None,
    ) -> None:
        """
        :param bucket: 
        :param access_key: 
        :param acl: 
        :param assume_role: 
        :param ecs_role_name: 
        :param encrypt: 
        :param endpoint: 
        :param key: 
        :param prefix: 
        :param profile: 
        :param region: 
        :param secret_key: 
        :param security_token: 
        :param shared_credentials_file: 
        :param tablestore_endpoint: 
        :param tablestore_table: 

        stability
        :stability: experimental
        """
        if isinstance(assume_role, dict):
            assume_role = OssAssumeRole(**assume_role)
        self._values = {
            "bucket": bucket,
        }
        if access_key is not None:
            self._values["access_key"] = access_key
        if acl is not None:
            self._values["acl"] = acl
        if assume_role is not None:
            self._values["assume_role"] = assume_role
        if ecs_role_name is not None:
            self._values["ecs_role_name"] = ecs_role_name
        if encrypt is not None:
            self._values["encrypt"] = encrypt
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if key is not None:
            self._values["key"] = key
        if prefix is not None:
            self._values["prefix"] = prefix
        if profile is not None:
            self._values["profile"] = profile
        if region is not None:
            self._values["region"] = region
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if security_token is not None:
            self._values["security_token"] = security_token
        if shared_credentials_file is not None:
            self._values["shared_credentials_file"] = shared_credentials_file
        if tablestore_endpoint is not None:
            self._values["tablestore_endpoint"] = tablestore_endpoint
        if tablestore_table is not None:
            self._values["tablestore_table"] = tablestore_table

    @builtins.property
    def bucket(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("bucket")

    @builtins.property
    def access_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("access_key")

    @builtins.property
    def acl(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("acl")

    @builtins.property
    def assume_role(self) -> typing.Optional["OssAssumeRole"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("assume_role")

    @builtins.property
    def ecs_role_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("ecs_role_name")

    @builtins.property
    def encrypt(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("encrypt")

    @builtins.property
    def endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("endpoint")

    @builtins.property
    def key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key")

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("prefix")

    @builtins.property
    def profile(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("profile")

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("region")

    @builtins.property
    def secret_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("secret_key")

    @builtins.property
    def security_token(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("security_token")

    @builtins.property
    def shared_credentials_file(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("shared_credentials_file")

    @builtins.property
    def tablestore_endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("tablestore_endpoint")

    @builtins.property
    def tablestore_table(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("tablestore_table")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OssBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.PgBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "conn_str": "connStr",
        "schema_name": "schemaName",
        "skip_schema_creation": "skipSchemaCreation",
    },
)
class PgBackendProps:
    def __init__(
        self,
        *,
        conn_str: str,
        schema_name: typing.Optional[str] = None,
        skip_schema_creation: typing.Optional[bool] = None,
    ) -> None:
        """
        :param conn_str: 
        :param schema_name: 
        :param skip_schema_creation: 

        stability
        :stability: experimental
        """
        self._values = {
            "conn_str": conn_str,
        }
        if schema_name is not None:
            self._values["schema_name"] = schema_name
        if skip_schema_creation is not None:
            self._values["skip_schema_creation"] = skip_schema_creation

    @builtins.property
    def conn_str(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("conn_str")

    @builtins.property
    def schema_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("schema_name")

    @builtins.property
    def skip_schema_creation(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("skip_schema_creation")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PgBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IRemoteWorkspace)
class PrefixedRemoteWorkspaces(
    metaclass=jsii.JSIIMeta, jsii_type="cdktf.PrefixedRemoteWorkspaces"
):
    """
    stability
    :stability: experimental
    """

    def __init__(self, prefix: str) -> None:
        """
        :param prefix: -

        stability
        :stability: experimental
        """
        jsii.create(PrefixedRemoteWorkspaces, self, [prefix])

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "prefix")

    @prefix.setter
    def prefix(self, value: str) -> None:
        jsii.set(self, "prefix", value)


@jsii.data_type(
    jsii_type="cdktf.RemoteBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "organization": "organization",
        "workspaces": "workspaces",
        "hostname": "hostname",
        "token": "token",
    },
)
class RemoteBackendProps:
    def __init__(
        self,
        *,
        organization: str,
        workspaces: "IRemoteWorkspace",
        hostname: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
    ) -> None:
        """
        :param organization: 
        :param workspaces: 
        :param hostname: 
        :param token: 

        stability
        :stability: experimental
        """
        self._values = {
            "organization": organization,
            "workspaces": workspaces,
        }
        if hostname is not None:
            self._values["hostname"] = hostname
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def organization(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("organization")

    @builtins.property
    def workspaces(self) -> "IRemoteWorkspace":
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspaces")

    @builtins.property
    def hostname(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("hostname")

    @builtins.property
    def token(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("token")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RemoteBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.ResolveOptions",
    jsii_struct_bases=[],
    name_mapping={"resolver": "resolver", "scope": "scope", "preparing": "preparing"},
)
class ResolveOptions:
    def __init__(
        self,
        *,
        resolver: "ITokenResolver",
        scope: constructs.IConstruct,
        preparing: typing.Optional[bool] = None,
    ) -> None:
        """Options to the resolve() operation.

        NOT the same as the ResolveContext; ResolveContext is exposed to Token
        implementors and resolution hooks, whereas this struct is just to bundle
        a number of things that would otherwise be arguments to resolve() in a
        readable way.

        :param resolver: The resolver to apply to any resolvable tokens found.
        :param scope: The scope from which resolution is performed.
        :param preparing: Whether the resolution is being executed during the prepare phase or not. Default: false

        stability
        :stability: experimental
        """
        self._values = {
            "resolver": resolver,
            "scope": scope,
        }
        if preparing is not None:
            self._values["preparing"] = preparing

    @builtins.property
    def resolver(self) -> "ITokenResolver":
        """The resolver to apply to any resolvable tokens found.

        stability
        :stability: experimental
        """
        return self._values.get("resolver")

    @builtins.property
    def scope(self) -> constructs.IConstruct:
        """The scope from which resolution is performed.

        stability
        :stability: experimental
        """
        return self._values.get("scope")

    @builtins.property
    def preparing(self) -> typing.Optional[bool]:
        """Whether the resolution is being executed during the prepare phase or not.

        default
        :default: false

        stability
        :stability: experimental
        """
        return self._values.get("preparing")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ResolveOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IResource)
class Resource(
    constructs.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="cdktf.Resource"
):
    """A construct which represents a resource.

    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ResourceProxy

    def __init__(self, scope: constructs.Construct, id: str) -> None:
        """
        :param scope: -
        :param id: -

        stability
        :stability: experimental
        """
        jsii.create(Resource, self, [scope, id])

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "TerraformStack":
        """The stack in which this resource is defined.

        stability
        :stability: experimental
        """
        return jsii.get(self, "stack")


class _ResourceProxy(Resource):
    pass


@jsii.data_type(
    jsii_type="cdktf.S3BackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "bucket": "bucket",
        "key": "key",
        "access_key": "accessKey",
        "acl": "acl",
        "assume_role_policy": "assumeRolePolicy",
        "dynamodb_endpoint": "dynamodbEndpoint",
        "dynamodb_table": "dynamodbTable",
        "encrypt": "encrypt",
        "endpoint": "endpoint",
        "external_id": "externalId",
        "force_path_style": "forcePathStyle",
        "iam_endpoint": "iamEndpoint",
        "kms_key_id": "kmsKeyId",
        "max_retries": "maxRetries",
        "profile": "profile",
        "region": "region",
        "role_arn": "roleArn",
        "secret_key": "secretKey",
        "session_name": "sessionName",
        "shared_credentials_file": "sharedCredentialsFile",
        "skip_credentials_validation": "skipCredentialsValidation",
        "skip_metadata_api_check": "skipMetadataApiCheck",
        "sse_customer_key": "sseCustomerKey",
        "sts_endpoint": "stsEndpoint",
        "token": "token",
        "workspace_key_prefix": "workspaceKeyPrefix",
    },
)
class S3BackendProps:
    def __init__(
        self,
        *,
        bucket: str,
        key: str,
        access_key: typing.Optional[str] = None,
        acl: typing.Optional[str] = None,
        assume_role_policy: typing.Optional[str] = None,
        dynamodb_endpoint: typing.Optional[str] = None,
        dynamodb_table: typing.Optional[str] = None,
        encrypt: typing.Optional[bool] = None,
        endpoint: typing.Optional[str] = None,
        external_id: typing.Optional[str] = None,
        force_path_style: typing.Optional[bool] = None,
        iam_endpoint: typing.Optional[str] = None,
        kms_key_id: typing.Optional[str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        profile: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
        role_arn: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
        session_name: typing.Optional[str] = None,
        shared_credentials_file: typing.Optional[str] = None,
        skip_credentials_validation: typing.Optional[bool] = None,
        skip_metadata_api_check: typing.Optional[bool] = None,
        sse_customer_key: typing.Optional[str] = None,
        sts_endpoint: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        workspace_key_prefix: typing.Optional[str] = None,
    ) -> None:
        """
        :param bucket: 
        :param key: 
        :param access_key: 
        :param acl: 
        :param assume_role_policy: 
        :param dynamodb_endpoint: 
        :param dynamodb_table: 
        :param encrypt: 
        :param endpoint: 
        :param external_id: 
        :param force_path_style: 
        :param iam_endpoint: 
        :param kms_key_id: 
        :param max_retries: 
        :param profile: 
        :param region: 
        :param role_arn: 
        :param secret_key: 
        :param session_name: 
        :param shared_credentials_file: 
        :param skip_credentials_validation: 
        :param skip_metadata_api_check: 
        :param sse_customer_key: 
        :param sts_endpoint: 
        :param token: 
        :param workspace_key_prefix: 

        stability
        :stability: experimental
        """
        self._values = {
            "bucket": bucket,
            "key": key,
        }
        if access_key is not None:
            self._values["access_key"] = access_key
        if acl is not None:
            self._values["acl"] = acl
        if assume_role_policy is not None:
            self._values["assume_role_policy"] = assume_role_policy
        if dynamodb_endpoint is not None:
            self._values["dynamodb_endpoint"] = dynamodb_endpoint
        if dynamodb_table is not None:
            self._values["dynamodb_table"] = dynamodb_table
        if encrypt is not None:
            self._values["encrypt"] = encrypt
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if external_id is not None:
            self._values["external_id"] = external_id
        if force_path_style is not None:
            self._values["force_path_style"] = force_path_style
        if iam_endpoint is not None:
            self._values["iam_endpoint"] = iam_endpoint
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if profile is not None:
            self._values["profile"] = profile
        if region is not None:
            self._values["region"] = region
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if session_name is not None:
            self._values["session_name"] = session_name
        if shared_credentials_file is not None:
            self._values["shared_credentials_file"] = shared_credentials_file
        if skip_credentials_validation is not None:
            self._values["skip_credentials_validation"] = skip_credentials_validation
        if skip_metadata_api_check is not None:
            self._values["skip_metadata_api_check"] = skip_metadata_api_check
        if sse_customer_key is not None:
            self._values["sse_customer_key"] = sse_customer_key
        if sts_endpoint is not None:
            self._values["sts_endpoint"] = sts_endpoint
        if token is not None:
            self._values["token"] = token
        if workspace_key_prefix is not None:
            self._values["workspace_key_prefix"] = workspace_key_prefix

    @builtins.property
    def bucket(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("bucket")

    @builtins.property
    def key(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key")

    @builtins.property
    def access_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("access_key")

    @builtins.property
    def acl(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("acl")

    @builtins.property
    def assume_role_policy(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("assume_role_policy")

    @builtins.property
    def dynamodb_endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("dynamodb_endpoint")

    @builtins.property
    def dynamodb_table(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("dynamodb_table")

    @builtins.property
    def encrypt(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("encrypt")

    @builtins.property
    def endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("endpoint")

    @builtins.property
    def external_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("external_id")

    @builtins.property
    def force_path_style(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("force_path_style")

    @builtins.property
    def iam_endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("iam_endpoint")

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("kms_key_id")

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("max_retries")

    @builtins.property
    def profile(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("profile")

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("region")

    @builtins.property
    def role_arn(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("role_arn")

    @builtins.property
    def secret_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("secret_key")

    @builtins.property
    def session_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("session_name")

    @builtins.property
    def shared_credentials_file(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("shared_credentials_file")

    @builtins.property
    def skip_credentials_validation(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("skip_credentials_validation")

    @builtins.property
    def skip_metadata_api_check(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("skip_metadata_api_check")

    @builtins.property
    def sse_customer_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("sse_customer_key")

    @builtins.property
    def sts_endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("sts_endpoint")

    @builtins.property
    def token(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("token")

    @builtins.property
    def workspace_key_prefix(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace_key_prefix")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3BackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IFragmentConcatenator)
class StringConcat(metaclass=jsii.JSIIMeta, jsii_type="cdktf.StringConcat"):
    """Converts all fragments to strings and concats those.

    Drops 'undefined's.

    stability
    :stability: experimental
    """

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(StringConcat, self, [])

    @jsii.member(jsii_name="join")
    def join(self, left: typing.Any, right: typing.Any) -> typing.Any:
        """Join the fragment on the left and on the right.

        :param left: -
        :param right: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "join", [left, right])


class StringMap(metaclass=jsii.JSIIMeta, jsii_type="cdktf.StringMap"):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self, terraform_resource: "ITerraformResource", terraform_attribute: str
    ) -> None:
        """
        :param terraform_resource: -
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        jsii.create(StringMap, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="lookup")
    def lookup(self, key: str) -> str:
        """
        :param key: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "lookup", [key])

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformAttribute")

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: str) -> None:
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> "ITerraformResource":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResource")

    @_terraform_resource.setter
    def _terraform_resource(self, value: "ITerraformResource") -> None:
        jsii.set(self, "terraformResource", value)


@jsii.data_type(
    jsii_type="cdktf.SwiftBackendProps",
    jsii_struct_bases=[],
    name_mapping={
        "container": "container",
        "application_credential_id": "applicationCredentialId",
        "application_credential_name": "applicationCredentialName",
        "application_credential_secret": "applicationCredentialSecret",
        "archive_container": "archiveContainer",
        "auth_url": "authUrl",
        "cacert_file": "cacertFile",
        "cert": "cert",
        "cloud": "cloud",
        "default_domain": "defaultDomain",
        "domain_id": "domainId",
        "domain_name": "domainName",
        "expire_after": "expireAfter",
        "insecure": "insecure",
        "key": "key",
        "password": "password",
        "project_domain_id": "projectDomainId",
        "project_domain_name": "projectDomainName",
        "region_name": "regionName",
        "state_name": "stateName",
        "tenant_id": "tenantId",
        "tenant_name": "tenantName",
        "token": "token",
        "user_domain_id": "userDomainId",
        "user_domain_name": "userDomainName",
        "user_id": "userId",
        "user_name": "userName",
    },
)
class SwiftBackendProps:
    def __init__(
        self,
        *,
        container: str,
        application_credential_id: typing.Optional[str] = None,
        application_credential_name: typing.Optional[str] = None,
        application_credential_secret: typing.Optional[str] = None,
        archive_container: typing.Optional[str] = None,
        auth_url: typing.Optional[str] = None,
        cacert_file: typing.Optional[str] = None,
        cert: typing.Optional[str] = None,
        cloud: typing.Optional[str] = None,
        default_domain: typing.Optional[str] = None,
        domain_id: typing.Optional[str] = None,
        domain_name: typing.Optional[str] = None,
        expire_after: typing.Optional[str] = None,
        insecure: typing.Optional[bool] = None,
        key: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        project_domain_id: typing.Optional[str] = None,
        project_domain_name: typing.Optional[str] = None,
        region_name: typing.Optional[str] = None,
        state_name: typing.Optional[str] = None,
        tenant_id: typing.Optional[str] = None,
        tenant_name: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        user_domain_id: typing.Optional[str] = None,
        user_domain_name: typing.Optional[str] = None,
        user_id: typing.Optional[str] = None,
        user_name: typing.Optional[str] = None,
    ) -> None:
        """
        :param container: 
        :param application_credential_id: 
        :param application_credential_name: 
        :param application_credential_secret: 
        :param archive_container: 
        :param auth_url: 
        :param cacert_file: 
        :param cert: 
        :param cloud: 
        :param default_domain: 
        :param domain_id: 
        :param domain_name: 
        :param expire_after: 
        :param insecure: 
        :param key: 
        :param password: 
        :param project_domain_id: 
        :param project_domain_name: 
        :param region_name: 
        :param state_name: 
        :param tenant_id: 
        :param tenant_name: 
        :param token: 
        :param user_domain_id: 
        :param user_domain_name: 
        :param user_id: 
        :param user_name: 

        stability
        :stability: experimental
        """
        self._values = {
            "container": container,
        }
        if application_credential_id is not None:
            self._values["application_credential_id"] = application_credential_id
        if application_credential_name is not None:
            self._values["application_credential_name"] = application_credential_name
        if application_credential_secret is not None:
            self._values["application_credential_secret"] = application_credential_secret
        if archive_container is not None:
            self._values["archive_container"] = archive_container
        if auth_url is not None:
            self._values["auth_url"] = auth_url
        if cacert_file is not None:
            self._values["cacert_file"] = cacert_file
        if cert is not None:
            self._values["cert"] = cert
        if cloud is not None:
            self._values["cloud"] = cloud
        if default_domain is not None:
            self._values["default_domain"] = default_domain
        if domain_id is not None:
            self._values["domain_id"] = domain_id
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if expire_after is not None:
            self._values["expire_after"] = expire_after
        if insecure is not None:
            self._values["insecure"] = insecure
        if key is not None:
            self._values["key"] = key
        if password is not None:
            self._values["password"] = password
        if project_domain_id is not None:
            self._values["project_domain_id"] = project_domain_id
        if project_domain_name is not None:
            self._values["project_domain_name"] = project_domain_name
        if region_name is not None:
            self._values["region_name"] = region_name
        if state_name is not None:
            self._values["state_name"] = state_name
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if tenant_name is not None:
            self._values["tenant_name"] = tenant_name
        if token is not None:
            self._values["token"] = token
        if user_domain_id is not None:
            self._values["user_domain_id"] = user_domain_id
        if user_domain_name is not None:
            self._values["user_domain_name"] = user_domain_name
        if user_id is not None:
            self._values["user_id"] = user_id
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def container(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("container")

    @builtins.property
    def application_credential_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("application_credential_id")

    @builtins.property
    def application_credential_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("application_credential_name")

    @builtins.property
    def application_credential_secret(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("application_credential_secret")

    @builtins.property
    def archive_container(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("archive_container")

    @builtins.property
    def auth_url(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("auth_url")

    @builtins.property
    def cacert_file(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("cacert_file")

    @builtins.property
    def cert(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("cert")

    @builtins.property
    def cloud(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("cloud")

    @builtins.property
    def default_domain(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("default_domain")

    @builtins.property
    def domain_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("domain_id")

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("domain_name")

    @builtins.property
    def expire_after(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("expire_after")

    @builtins.property
    def insecure(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("insecure")

    @builtins.property
    def key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key")

    @builtins.property
    def password(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("password")

    @builtins.property
    def project_domain_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("project_domain_id")

    @builtins.property
    def project_domain_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("project_domain_name")

    @builtins.property
    def region_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("region_name")

    @builtins.property
    def state_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("state_name")

    @builtins.property
    def tenant_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("tenant_id")

    @builtins.property
    def tenant_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("tenant_name")

    @builtins.property
    def token(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("token")

    @builtins.property
    def user_domain_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("user_domain_id")

    @builtins.property
    def user_domain_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("user_domain_name")

    @builtins.property
    def user_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("user_id")

    @builtins.property
    def user_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("user_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SwiftBackendProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TerraformElement(
    constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformElement"
):
    """
    stability
    :stability: experimental
    """

    def __init__(self, scope: constructs.Construct, id: str) -> None:
        """
        :param scope: -
        :param id: -

        stability
        :stability: experimental
        """
        jsii.create(TerraformElement, self, [scope, id])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: str, value: typing.Any) -> None:
        """
        :param path: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addOverride", [path, value])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="constructNode")
    def construct_node(self) -> constructs.Node:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "constructNode")

    @builtins.property
    @jsii.member(jsii_name="constructNodeMetadata")
    def _construct_node_metadata(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "constructNodeMetadata")

    @builtins.property
    @jsii.member(jsii_name="friendlyUniqueId")
    def friendly_unique_id(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "friendlyUniqueId")

    @builtins.property
    @jsii.member(jsii_name="rawOverrides")
    def _raw_overrides(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "rawOverrides")

    @builtins.property
    @jsii.member(jsii_name="stack")
    def stack(self) -> "TerraformStack":
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "stack")


@jsii.data_type(
    jsii_type="cdktf.TerraformElementMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "path": "path",
        "stack_trace": "stackTrace",
        "unique_id": "uniqueId",
    },
)
class TerraformElementMetadata:
    def __init__(
        self, *, path: str, stack_trace: typing.List[str], unique_id: str
    ) -> None:
        """
        :param path: 
        :param stack_trace: 
        :param unique_id: 

        stability
        :stability: experimental
        """
        self._values = {
            "path": path,
            "stack_trace": stack_trace,
            "unique_id": unique_id,
        }

    @builtins.property
    def path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("path")

    @builtins.property
    def stack_trace(self) -> typing.List[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("stack_trace")

    @builtins.property
    def unique_id(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("unique_id")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformElementMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.TerraformGeneratorMetadata",
    jsii_struct_bases=[],
    name_mapping={
        "provider_name": "providerName",
        "provider_version_constraint": "providerVersionConstraint",
    },
)
class TerraformGeneratorMetadata:
    def __init__(
        self,
        *,
        provider_name: str,
        provider_version_constraint: typing.Optional[str] = None,
    ) -> None:
        """
        :param provider_name: 
        :param provider_version_constraint: 

        stability
        :stability: experimental
        """
        self._values = {
            "provider_name": provider_name,
        }
        if provider_version_constraint is not None:
            self._values["provider_version_constraint"] = provider_version_constraint

    @builtins.property
    def provider_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider_name")

    @builtins.property
    def provider_version_constraint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider_version_constraint")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformGeneratorMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.TerraformMetaArguments",
    jsii_struct_bases=[],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
    },
)
class TerraformMetaArguments:
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List["TerraformResource"]] = None,
        lifecycle: typing.Optional["TerraformResourceLifecycle"] = None,
        provider: typing.Optional["TerraformProvider"] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 

        stability
        :stability: experimental
        """
        if isinstance(lifecycle, dict):
            lifecycle = TerraformResourceLifecycle(**lifecycle)
        self._values = {}
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformMetaArguments(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TerraformModule(
    TerraformElement,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf.TerraformModule",
):
    """
    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _TerraformModuleProxy

    def __init__(
        self, scope: constructs.Construct, id: str, *, source: str, version: str
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param source: 
        :param version: 

        stability
        :stability: experimental
        """
        options = TerraformModuleOptions(source=source, version=version)

        jsii.create(TerraformModule, self, [scope, id, options])

    @jsii.member(jsii_name="interpolationForOutput")
    def interpolation_for_output(self, module_output: str) -> typing.Any:
        """
        :param module_output: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "interpolationForOutput", [module_output])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "source")

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "version")


class _TerraformModuleProxy(TerraformModule):
    pass


@jsii.data_type(
    jsii_type="cdktf.TerraformModuleOptions",
    jsii_struct_bases=[],
    name_mapping={"source": "source", "version": "version"},
)
class TerraformModuleOptions:
    def __init__(self, *, source: str, version: str) -> None:
        """
        :param source: 
        :param version: 

        stability
        :stability: experimental
        """
        self._values = {
            "source": source,
            "version": version,
        }

    @builtins.property
    def source(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("source")

    @builtins.property
    def version(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformModuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TerraformOutput(
    TerraformElement, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformOutput"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        depends_on: typing.Optional[typing.List["TerraformResource"]] = None,
        description: typing.Optional[str] = None,
        sensitive: typing.Optional[bool] = None,
        value: typing.Optional[typing.Union[str, jsii.Number, bool, typing.List[typing.Any], typing.Mapping[str, typing.Any]]] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param depends_on: 
        :param description: 
        :param sensitive: 
        :param value: 

        stability
        :stability: experimental
        """
        config = TerraformOutputConfig(
            depends_on=depends_on,
            description=description,
            sensitive=sensitive,
            value=value,
        )

        jsii.create(TerraformOutput, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "dependsOn")

    @depends_on.setter
    def depends_on(
        self, value: typing.Optional[typing.List["TerraformResource"]]
    ) -> None:
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "description")

    @description.setter
    def description(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="sensitive")
    def sensitive(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "sensitive")

    @sensitive.setter
    def sensitive(self, value: typing.Optional[bool]) -> None:
        jsii.set(self, "sensitive", value)

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(
        self,
    ) -> typing.Optional[typing.Union[str, jsii.Number, bool, typing.List[typing.Any], typing.Mapping[str, typing.Any]]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "value")

    @value.setter
    def value(
        self,
        value: typing.Optional[typing.Union[str, jsii.Number, bool, typing.List[typing.Any], typing.Mapping[str, typing.Any]]],
    ) -> None:
        jsii.set(self, "value", value)


@jsii.data_type(
    jsii_type="cdktf.TerraformOutputConfig",
    jsii_struct_bases=[],
    name_mapping={
        "depends_on": "dependsOn",
        "description": "description",
        "sensitive": "sensitive",
        "value": "value",
    },
)
class TerraformOutputConfig:
    def __init__(
        self,
        *,
        depends_on: typing.Optional[typing.List["TerraformResource"]] = None,
        description: typing.Optional[str] = None,
        sensitive: typing.Optional[bool] = None,
        value: typing.Optional[typing.Union[str, jsii.Number, bool, typing.List[typing.Any], typing.Mapping[str, typing.Any]]] = None,
    ) -> None:
        """
        :param depends_on: 
        :param description: 
        :param sensitive: 
        :param value: 

        stability
        :stability: experimental
        """
        self._values = {}
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if description is not None:
            self._values["description"] = description
        if sensitive is not None:
            self._values["sensitive"] = sensitive
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def description(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("description")

    @builtins.property
    def sensitive(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("sensitive")

    @builtins.property
    def value(
        self,
    ) -> typing.Optional[typing.Union[str, jsii.Number, bool, typing.List[typing.Any], typing.Mapping[str, typing.Any]]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("value")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformOutputConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TerraformProvider(
    TerraformElement,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf.TerraformProvider",
):
    """
    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _TerraformProviderProxy

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        terraform_resource_type: str,
        terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"] = None,
        terraform_provider_source: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 
        :param terraform_provider_source: 

        stability
        :stability: experimental
        """
        config = TerraformProviderConfig(
            terraform_resource_type=terraform_resource_type,
            terraform_generator_metadata=terraform_generator_metadata,
            terraform_provider_source=terraform_provider_source,
        )

        jsii.create(TerraformProvider, self, [scope, id, config])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """Adds this resource to the terraform JSON output.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "fqn")

    @builtins.property
    @jsii.member(jsii_name="metaAttributes")
    def meta_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "metaAttributes")

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResourceType")

    @builtins.property
    @jsii.member(jsii_name="terraformGeneratorMetadata")
    def terraform_generator_metadata(
        self,
    ) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformGeneratorMetadata")

    @builtins.property
    @jsii.member(jsii_name="terraformProviderSource")
    def terraform_provider_source(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformProviderSource")

    @builtins.property
    @jsii.member(jsii_name="alias")
    def alias(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "alias")

    @alias.setter
    def alias(self, value: typing.Optional[str]) -> None:
        jsii.set(self, "alias", value)


class _TerraformProviderProxy(TerraformProvider):
    pass


@jsii.data_type(
    jsii_type="cdktf.TerraformProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "terraform_resource_type": "terraformResourceType",
        "terraform_generator_metadata": "terraformGeneratorMetadata",
        "terraform_provider_source": "terraformProviderSource",
    },
)
class TerraformProviderConfig:
    def __init__(
        self,
        *,
        terraform_resource_type: str,
        terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"] = None,
        terraform_provider_source: typing.Optional[str] = None,
    ) -> None:
        """
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 
        :param terraform_provider_source: 

        stability
        :stability: experimental
        """
        if isinstance(terraform_generator_metadata, dict):
            terraform_generator_metadata = TerraformGeneratorMetadata(**terraform_generator_metadata)
        self._values = {
            "terraform_resource_type": terraform_resource_type,
        }
        if terraform_generator_metadata is not None:
            self._values["terraform_generator_metadata"] = terraform_generator_metadata
        if terraform_provider_source is not None:
            self._values["terraform_provider_source"] = terraform_provider_source

    @builtins.property
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("terraform_resource_type")

    @builtins.property
    def terraform_generator_metadata(
        self,
    ) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("terraform_generator_metadata")

    @builtins.property
    def terraform_provider_source(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("terraform_provider_source")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TerraformRemoteState(
    TerraformElement,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf.TerraformRemoteState",
):
    """
    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _TerraformRemoteStateProxy

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        backend: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param backend: -
        :param defaults: 
        :param workspace: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateConfig(defaults=defaults, workspace=workspace)

        jsii.create(TerraformRemoteState, self, [scope, id, backend, config])

    @jsii.member(jsii_name="get")
    def get(self, output: str) -> typing.Any:
        """
        :param output: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "get", [output])

    @jsii.member(jsii_name="getBoolean")
    def get_boolean(self, output: str) -> bool:
        """
        :param output: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getBoolean", [output])

    @jsii.member(jsii_name="getList")
    def get_list(self, output: str) -> typing.List[str]:
        """
        :param output: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getList", [output])

    @jsii.member(jsii_name="getNumber")
    def get_number(self, output: str) -> jsii.Number:
        """
        :param output: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getNumber", [output])

    @jsii.member(jsii_name="getString")
    def get_string(self, output: str) -> str:
        """
        :param output: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getString", [output])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """Adds this resource to the terraform JSON output.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])


class _TerraformRemoteStateProxy(TerraformRemoteState):
    pass


@jsii.implements(ITerraformResource)
class TerraformResource(
    TerraformElement, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformResource"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        terraform_resource_type: str,
        terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List["TerraformResource"]] = None,
        lifecycle: typing.Optional["TerraformResourceLifecycle"] = None,
        provider: typing.Optional["TerraformProvider"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 

        stability
        :stability: experimental
        """
        config = TerraformResourceConfig(
            terraform_resource_type=terraform_resource_type,
            terraform_generator_metadata=terraform_generator_metadata,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(TerraformResource, self, [scope, id, config])

    @jsii.member(jsii_name="getBooleanAttribute")
    def get_boolean_attribute(self, terraform_attribute: str) -> bool:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getBooleanAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getListAttribute")
    def get_list_attribute(self, terraform_attribute: str) -> typing.List[str]:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getListAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getNumberAttribute")
    def get_number_attribute(self, terraform_attribute: str) -> jsii.Number:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getNumberAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getStringAttribute")
    def get_string_attribute(self, terraform_attribute: str) -> str:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getStringAttribute", [terraform_attribute])

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(self, terraform_attribute: str) -> str:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "interpolationForAttribute", [terraform_attribute])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """Adds this resource to the terraform JSON output.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "fqn")

    @builtins.property
    @jsii.member(jsii_name="terraformMetaArguments")
    def terraform_meta_arguments(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformMetaArguments")

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResourceType")

    @builtins.property
    @jsii.member(jsii_name="terraformGeneratorMetadata")
    def terraform_generator_metadata(
        self,
    ) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformGeneratorMetadata")

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "count")

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[str]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "dependsOn")

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "lifecycle")

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional["TerraformResourceLifecycle"]) -> None:
        jsii.set(self, "lifecycle", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "provider")

    @provider.setter
    def provider(self, value: typing.Optional["TerraformProvider"]) -> None:
        jsii.set(self, "provider", value)


@jsii.data_type(
    jsii_type="cdktf.TerraformResourceConfig",
    jsii_struct_bases=[TerraformMetaArguments],
    name_mapping={
        "count": "count",
        "depends_on": "dependsOn",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "terraform_resource_type": "terraformResourceType",
        "terraform_generator_metadata": "terraformGeneratorMetadata",
    },
)
class TerraformResourceConfig(TerraformMetaArguments):
    def __init__(
        self,
        *,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List["TerraformResource"]] = None,
        lifecycle: typing.Optional["TerraformResourceLifecycle"] = None,
        provider: typing.Optional["TerraformProvider"] = None,
        terraform_resource_type: str,
        terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"] = None,
    ) -> None:
        """
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 

        stability
        :stability: experimental
        """
        if isinstance(lifecycle, dict):
            lifecycle = TerraformResourceLifecycle(**lifecycle)
        if isinstance(terraform_generator_metadata, dict):
            terraform_generator_metadata = TerraformGeneratorMetadata(**terraform_generator_metadata)
        self._values = {
            "terraform_resource_type": terraform_resource_type,
        }
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if terraform_generator_metadata is not None:
            self._values["terraform_generator_metadata"] = terraform_generator_metadata

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("count")

    @builtins.property
    def depends_on(self) -> typing.Optional[typing.List["TerraformResource"]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("depends_on")

    @builtins.property
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lifecycle")

    @builtins.property
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("provider")

    @builtins.property
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("terraform_resource_type")

    @builtins.property
    def terraform_generator_metadata(
        self,
    ) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("terraform_generator_metadata")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformResourceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.TerraformResourceLifecycle",
    jsii_struct_bases=[],
    name_mapping={
        "create_before_destroy": "createBeforeDestroy",
        "ignore_changes": "ignoreChanges",
        "prevent_destroy": "preventDestroy",
    },
)
class TerraformResourceLifecycle:
    def __init__(
        self,
        *,
        create_before_destroy: typing.Optional[bool] = None,
        ignore_changes: typing.Optional[typing.List[str]] = None,
        prevent_destroy: typing.Optional[bool] = None,
    ) -> None:
        """
        :param create_before_destroy: 
        :param ignore_changes: 
        :param prevent_destroy: 

        stability
        :stability: experimental
        """
        self._values = {}
        if create_before_destroy is not None:
            self._values["create_before_destroy"] = create_before_destroy
        if ignore_changes is not None:
            self._values["ignore_changes"] = ignore_changes
        if prevent_destroy is not None:
            self._values["prevent_destroy"] = prevent_destroy

    @builtins.property
    def create_before_destroy(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("create_before_destroy")

    @builtins.property
    def ignore_changes(self) -> typing.Optional[typing.List[str]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("ignore_changes")

    @builtins.property
    def prevent_destroy(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("prevent_destroy")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformResourceLifecycle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TerraformStack(
    constructs.Construct, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformStack"
):
    """
    stability
    :stability: experimental
    """

    def __init__(self, scope: constructs.Construct, id: str) -> None:
        """
        :param scope: -
        :param id: -

        stability
        :stability: experimental
        """
        jsii.create(TerraformStack, self, [scope, id])

    @jsii.member(jsii_name="isStack")
    @builtins.classmethod
    def is_stack(cls, x: typing.Any) -> bool:
        """
        :param x: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isStack", [x])

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, construct: constructs.IConstruct) -> "TerraformStack":
        """
        :param construct: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "of", [construct])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, path: str, value: typing.Any) -> None:
        """
        :param path: -
        :param value: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addOverride", [path, value])

    @jsii.member(jsii_name="allProviders")
    def all_providers(self) -> typing.List["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "allProviders", [])

    @jsii.member(jsii_name="onSynthesize")
    def _on_synthesize(self, session: constructs.ISynthesisSession) -> None:
        """Allows this construct to emit artifacts into the cloud assembly during synthesis.

        This method is usually implemented by framework-level constructs such as ``Stack`` and ``Asset``
        as they participate in synthesizing the cloud assembly.

        :param session: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "onSynthesize", [session])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="artifactFile")
    def artifact_file(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "artifactFile")


@jsii.data_type(
    jsii_type="cdktf.TerraformStackMetadata",
    jsii_struct_bases=[],
    name_mapping={"stack_name": "stackName", "version": "version"},
)
class TerraformStackMetadata:
    def __init__(self, *, stack_name: str, version: str) -> None:
        """
        :param stack_name: 
        :param version: 

        stability
        :stability: experimental
        """
        self._values = {
            "stack_name": stack_name,
            "version": version,
        }

    @builtins.property
    def stack_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("stack_name")

    @builtins.property
    def version(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("version")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TerraformStackMetadata(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Testing(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Testing"):
    """Testing utilities for cdktf applications.

    stability
    :stability: experimental
    """

    @jsii.member(jsii_name="app")
    @builtins.classmethod
    def app(cls) -> "App":
        """Returns an app for testing with the following properties: - Output directory is a temp dir.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "app", [])

    @jsii.member(jsii_name="stubVersion")
    @builtins.classmethod
    def stub_version(cls, app: "App") -> "App":
        """
        :param app: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stubVersion", [app])

    @jsii.member(jsii_name="synth")
    @builtins.classmethod
    def synth(cls, stack: "TerraformStack") -> str:
        """Returns the Terraform synthesized JSON.

        :param stack: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "synth", [stack])


class Token(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Token"):
    """Represents a special or lazily-evaluated value.

    Can be used to delay evaluation of a certain value in case, for example,
    that it requires some context or late-bound data. Can also be used to
    mark values that need special processing at document rendering time.

    Tokens can be embedded into strings while retaining their original
    semantics.

    stability
    :stability: experimental
    """

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(Token, self, [])

    @jsii.member(jsii_name="asAny")
    @builtins.classmethod
    def as_any(cls, value: typing.Any) -> "IResolvable":
        """Return a resolvable representation of the given value.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "asAny", [value])

    @jsii.member(jsii_name="asList")
    @builtins.classmethod
    def as_list(
        cls, value: typing.Any, *, display_hint: typing.Optional[str] = None
    ) -> typing.List[str]:
        """Return a reversible list representation of this token.

        :param value: -
        :param display_hint: A hint for the Token's purpose when stringifying it. Default: - no display hint

        stability
        :stability: experimental
        """
        options = EncodingOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "asList", [value, options])

    @jsii.member(jsii_name="asNumber")
    @builtins.classmethod
    def as_number(cls, value: typing.Any) -> jsii.Number:
        """Return a reversible number representation of this token.

        :param value: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "asNumber", [value])

    @jsii.member(jsii_name="asString")
    @builtins.classmethod
    def as_string(
        cls, value: typing.Any, *, display_hint: typing.Optional[str] = None
    ) -> str:
        """Return a reversible string representation of this token.

        If the Token is initialized with a literal, the stringified value of the
        literal is returned. Otherwise, a special quoted string representation
        of the Token is returned that can be embedded into other strings.

        Strings with quoted Tokens in them can be restored back into
        complex values with the Tokens restored by calling ``resolve()``
        on the string.

        :param value: -
        :param display_hint: A hint for the Token's purpose when stringifying it. Default: - no display hint

        stability
        :stability: experimental
        """
        options = EncodingOptions(display_hint=display_hint)

        return jsii.sinvoke(cls, "asString", [value, options])

    @jsii.member(jsii_name="isUnresolved")
    @builtins.classmethod
    def is_unresolved(cls, obj: typing.Any) -> bool:
        """Returns true if obj represents an unresolved value.

        One of these must be true:

        - ``obj`` is an IResolvable
        - ``obj`` is a string containing at least one encoded ``IResolvable``
        - ``obj`` is either an encoded number or list

        This does NOT recurse into lists or objects to see if they
        containing resolvables.

        :param obj: The object to test.

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isUnresolved", [obj])


class Tokenization(metaclass=jsii.JSIIMeta, jsii_type="cdktf.Tokenization"):
    """Less oft-needed functions to manipulate Tokens.

    stability
    :stability: experimental
    """

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(Tokenization, self, [])

    @jsii.member(jsii_name="isResolvable")
    @builtins.classmethod
    def is_resolvable(cls, obj: typing.Any) -> bool:
        """Return whether the given object is an IResolvable object.

        This is different from Token.isUnresolved() which will also check for
        encoded Tokens, whereas this method will only do a type check on the given
        object.

        :param obj: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "isResolvable", [obj])

    @jsii.member(jsii_name="resolve")
    @builtins.classmethod
    def resolve(
        cls,
        obj: typing.Any,
        *,
        resolver: "ITokenResolver",
        scope: constructs.IConstruct,
        preparing: typing.Optional[bool] = None,
    ) -> typing.Any:
        """Resolves an object by evaluating all tokens and removing any undefined or empty objects or arrays.

        Values can only be primitives, arrays or tokens. Other objects (i.e. with methods) will be rejected.

        :param obj: The object to resolve.
        :param resolver: The resolver to apply to any resolvable tokens found.
        :param scope: The scope from which resolution is performed.
        :param preparing: Whether the resolution is being executed during the prepare phase or not. Default: false

        stability
        :stability: experimental
        """
        options = ResolveOptions(resolver=resolver, scope=scope, preparing=preparing)

        return jsii.sinvoke(cls, "resolve", [obj, options])

    @jsii.member(jsii_name="reverseList")
    @builtins.classmethod
    def reverse_list(cls, l: typing.List[str]) -> typing.Optional["IResolvable"]:
        """Un-encode a Tokenized value from a list.

        :param l: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "reverseList", [l])

    @jsii.member(jsii_name="reverseNumber")
    @builtins.classmethod
    def reverse_number(cls, n: jsii.Number) -> typing.Optional["IResolvable"]:
        """Un-encode a Tokenized value from a number.

        :param n: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "reverseNumber", [n])

    @jsii.member(jsii_name="reverseString")
    @builtins.classmethod
    def reverse_string(cls, s: str) -> "TokenizedStringFragments":
        """Un-encode a string potentially containing encoded tokens.

        :param s: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "reverseString", [s])

    @jsii.member(jsii_name="stringifyNumber")
    @builtins.classmethod
    def stringify_number(cls, x: jsii.Number) -> str:
        """Stringify a number directly or lazily if it's a Token.

        If it is an object (i.e., { Ref: 'SomeLogicalId' }), return it as-is.

        :param x: -

        stability
        :stability: experimental
        """
        return jsii.sinvoke(cls, "stringifyNumber", [x])


class TokenizedStringFragments(
    metaclass=jsii.JSIIMeta, jsii_type="cdktf.TokenizedStringFragments"
):
    """Fragments of a concatenated string containing stringified Tokens.

    stability
    :stability: experimental
    """

    def __init__(self) -> None:
        """
        stability
        :stability: experimental
        """
        jsii.create(TokenizedStringFragments, self, [])

    @jsii.member(jsii_name="addIntrinsic")
    def add_intrinsic(self, value: typing.Any) -> None:
        """Adds an intrinsic fragment.

        :param value: the intrinsic value to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addIntrinsic", [value])

    @jsii.member(jsii_name="addLiteral")
    def add_literal(self, lit: typing.Any) -> None:
        """Adds a literal fragment.

        :param lit: the literal to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addLiteral", [lit])

    @jsii.member(jsii_name="addToken")
    def add_token(self, token: "IResolvable") -> None:
        """Adds a token fragment.

        :param token: the token to add.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "addToken", [token])

    @jsii.member(jsii_name="join")
    def join(self, concat: "IFragmentConcatenator") -> typing.Any:
        """Combine the string fragments using the given joiner.

        If there are any

        :param concat: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "join", [concat])

    @jsii.member(jsii_name="mapTokens")
    def map_tokens(self, mapper: "ITokenMapper") -> "TokenizedStringFragments":
        """Apply a transformation function to all tokens in the string.

        :param mapper: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "mapTokens", [mapper])

    @builtins.property
    @jsii.member(jsii_name="firstValue")
    def first_value(self) -> typing.Any:
        """Returns the first value.

        stability
        :stability: experimental
        """
        return jsii.get(self, "firstValue")

    @builtins.property
    @jsii.member(jsii_name="length")
    def length(self) -> jsii.Number:
        """Returns the number of fragments.

        stability
        :stability: experimental
        """
        return jsii.get(self, "length")

    @builtins.property
    @jsii.member(jsii_name="tokens")
    def tokens(self) -> typing.List["IResolvable"]:
        """Return all Tokens from this string.

        stability
        :stability: experimental
        """
        return jsii.get(self, "tokens")

    @builtins.property
    @jsii.member(jsii_name="firstToken")
    def first_token(self) -> typing.Optional["IResolvable"]:
        """Returns the first token.

        stability
        :stability: experimental
        """
        return jsii.get(self, "firstToken")


class DataTerraformRemoteState(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteState",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        organization: str,
        workspaces: "IRemoteWorkspace",
        hostname: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param organization: 
        :param workspaces: 
        :param hostname: 
        :param token: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateRemoteConfig(
            defaults=defaults,
            workspace=workspace,
            organization=organization,
            workspaces=workspaces,
            hostname=hostname,
            token=token,
        )

        jsii.create(DataTerraformRemoteState, self, [scope, id, config])


class DataTerraformRemoteStateArtifactory(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateArtifactory",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        password: str,
        repo: str,
        subpath: str,
        url: str,
        username: str,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param password: 
        :param repo: 
        :param subpath: 
        :param url: 
        :param username: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateArtifactoryConfig(
            defaults=defaults,
            workspace=workspace,
            password=password,
            repo=repo,
            subpath=subpath,
            url=url,
            username=username,
        )

        jsii.create(DataTerraformRemoteStateArtifactory, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateArtifactoryConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, ArtifactoryBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "password": "password",
        "repo": "repo",
        "subpath": "subpath",
        "url": "url",
        "username": "username",
    },
)
class DataTerraformRemoteStateArtifactoryConfig(
    DataTerraformRemoteStateConfig, ArtifactoryBackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        password: str,
        repo: str,
        subpath: str,
        url: str,
        username: str,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param password: 
        :param repo: 
        :param subpath: 
        :param url: 
        :param username: 

        stability
        :stability: experimental
        """
        self._values = {
            "password": password,
            "repo": repo,
            "subpath": subpath,
            "url": url,
            "username": username,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def password(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("password")

    @builtins.property
    def repo(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("repo")

    @builtins.property
    def subpath(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("subpath")

    @builtins.property
    def url(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("url")

    @builtins.property
    def username(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateArtifactoryConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateAzurerm(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateAzurerm",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        container_name: str,
        key: str,
        storage_account_name: str,
        access_key: typing.Optional[str] = None,
        client_id: typing.Optional[str] = None,
        client_secret: typing.Optional[str] = None,
        endpoint: typing.Optional[str] = None,
        environment: typing.Optional[str] = None,
        msi_endpoint: typing.Optional[str] = None,
        resource_group_name: typing.Optional[str] = None,
        sas_token: typing.Optional[str] = None,
        subscription_id: typing.Optional[str] = None,
        tenant_id: typing.Optional[str] = None,
        use_msi: typing.Optional[bool] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param container_name: 
        :param key: 
        :param storage_account_name: 
        :param access_key: 
        :param client_id: 
        :param client_secret: 
        :param endpoint: 
        :param environment: 
        :param msi_endpoint: 
        :param resource_group_name: 
        :param sas_token: 
        :param subscription_id: 
        :param tenant_id: 
        :param use_msi: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateAzurermConfig(
            defaults=defaults,
            workspace=workspace,
            container_name=container_name,
            key=key,
            storage_account_name=storage_account_name,
            access_key=access_key,
            client_id=client_id,
            client_secret=client_secret,
            endpoint=endpoint,
            environment=environment,
            msi_endpoint=msi_endpoint,
            resource_group_name=resource_group_name,
            sas_token=sas_token,
            subscription_id=subscription_id,
            tenant_id=tenant_id,
            use_msi=use_msi,
        )

        jsii.create(DataTerraformRemoteStateAzurerm, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateAzurermConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, AzurermBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "container_name": "containerName",
        "key": "key",
        "storage_account_name": "storageAccountName",
        "access_key": "accessKey",
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "endpoint": "endpoint",
        "environment": "environment",
        "msi_endpoint": "msiEndpoint",
        "resource_group_name": "resourceGroupName",
        "sas_token": "sasToken",
        "subscription_id": "subscriptionId",
        "tenant_id": "tenantId",
        "use_msi": "useMsi",
    },
)
class DataTerraformRemoteStateAzurermConfig(
    DataTerraformRemoteStateConfig, AzurermBackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        container_name: str,
        key: str,
        storage_account_name: str,
        access_key: typing.Optional[str] = None,
        client_id: typing.Optional[str] = None,
        client_secret: typing.Optional[str] = None,
        endpoint: typing.Optional[str] = None,
        environment: typing.Optional[str] = None,
        msi_endpoint: typing.Optional[str] = None,
        resource_group_name: typing.Optional[str] = None,
        sas_token: typing.Optional[str] = None,
        subscription_id: typing.Optional[str] = None,
        tenant_id: typing.Optional[str] = None,
        use_msi: typing.Optional[bool] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param container_name: 
        :param key: 
        :param storage_account_name: 
        :param access_key: 
        :param client_id: 
        :param client_secret: 
        :param endpoint: 
        :param environment: 
        :param msi_endpoint: 
        :param resource_group_name: 
        :param sas_token: 
        :param subscription_id: 
        :param tenant_id: 
        :param use_msi: 

        stability
        :stability: experimental
        """
        self._values = {
            "container_name": container_name,
            "key": key,
            "storage_account_name": storage_account_name,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if access_key is not None:
            self._values["access_key"] = access_key
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if environment is not None:
            self._values["environment"] = environment
        if msi_endpoint is not None:
            self._values["msi_endpoint"] = msi_endpoint
        if resource_group_name is not None:
            self._values["resource_group_name"] = resource_group_name
        if sas_token is not None:
            self._values["sas_token"] = sas_token
        if subscription_id is not None:
            self._values["subscription_id"] = subscription_id
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if use_msi is not None:
            self._values["use_msi"] = use_msi

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def container_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("container_name")

    @builtins.property
    def key(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key")

    @builtins.property
    def storage_account_name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("storage_account_name")

    @builtins.property
    def access_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("access_key")

    @builtins.property
    def client_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("client_id")

    @builtins.property
    def client_secret(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("client_secret")

    @builtins.property
    def endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("endpoint")

    @builtins.property
    def environment(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("environment")

    @builtins.property
    def msi_endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("msi_endpoint")

    @builtins.property
    def resource_group_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("resource_group_name")

    @builtins.property
    def sas_token(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("sas_token")

    @builtins.property
    def subscription_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("subscription_id")

    @builtins.property
    def tenant_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("tenant_id")

    @builtins.property
    def use_msi(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("use_msi")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateAzurermConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateConsul(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateConsul",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        access_token: str,
        path: str,
        address: typing.Optional[str] = None,
        ca_file: typing.Optional[str] = None,
        cert_file: typing.Optional[str] = None,
        datacenter: typing.Optional[str] = None,
        gzip: typing.Optional[bool] = None,
        http_auth: typing.Optional[str] = None,
        key_file: typing.Optional[str] = None,
        lock: typing.Optional[bool] = None,
        scheme: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param access_token: 
        :param path: 
        :param address: 
        :param ca_file: 
        :param cert_file: 
        :param datacenter: 
        :param gzip: 
        :param http_auth: 
        :param key_file: 
        :param lock: 
        :param scheme: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateConsulConfig(
            defaults=defaults,
            workspace=workspace,
            access_token=access_token,
            path=path,
            address=address,
            ca_file=ca_file,
            cert_file=cert_file,
            datacenter=datacenter,
            gzip=gzip,
            http_auth=http_auth,
            key_file=key_file,
            lock=lock,
            scheme=scheme,
        )

        jsii.create(DataTerraformRemoteStateConsul, self, [scope, id, config])


class DataTerraformRemoteStateCos(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateCos",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        bucket: str,
        acl: typing.Optional[str] = None,
        encrypt: typing.Optional[bool] = None,
        key: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
        secret_id: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param bucket: 
        :param acl: 
        :param encrypt: 
        :param key: 
        :param prefix: 
        :param region: 
        :param secret_id: 
        :param secret_key: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateCosConfig(
            defaults=defaults,
            workspace=workspace,
            bucket=bucket,
            acl=acl,
            encrypt=encrypt,
            key=key,
            prefix=prefix,
            region=region,
            secret_id=secret_id,
            secret_key=secret_key,
        )

        jsii.create(DataTerraformRemoteStateCos, self, [scope, id, config])


class DataTerraformRemoteStateEtcd(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateEtcd",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        endpoints: str,
        path: str,
        password: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param endpoints: 
        :param path: 
        :param password: 
        :param username: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateEtcdConfig(
            defaults=defaults,
            workspace=workspace,
            endpoints=endpoints,
            path=path,
            password=password,
            username=username,
        )

        jsii.create(DataTerraformRemoteStateEtcd, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateEtcdConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, EtcdBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "endpoints": "endpoints",
        "path": "path",
        "password": "password",
        "username": "username",
    },
)
class DataTerraformRemoteStateEtcdConfig(
    DataTerraformRemoteStateConfig, EtcdBackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        endpoints: str,
        path: str,
        password: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param endpoints: 
        :param path: 
        :param password: 
        :param username: 

        stability
        :stability: experimental
        """
        self._values = {
            "endpoints": endpoints,
            "path": path,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if password is not None:
            self._values["password"] = password
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def endpoints(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("endpoints")

    @builtins.property
    def path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("path")

    @builtins.property
    def password(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("password")

    @builtins.property
    def username(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateEtcdConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateEtcdV3(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateEtcdV3",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        endpoints: typing.List[str],
        cacert_path: typing.Optional[str] = None,
        cert_path: typing.Optional[str] = None,
        key_path: typing.Optional[str] = None,
        lock: typing.Optional[bool] = None,
        password: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param endpoints: 
        :param cacert_path: 
        :param cert_path: 
        :param key_path: 
        :param lock: 
        :param password: 
        :param prefix: 
        :param username: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateEtcdV3Config(
            defaults=defaults,
            workspace=workspace,
            endpoints=endpoints,
            cacert_path=cacert_path,
            cert_path=cert_path,
            key_path=key_path,
            lock=lock,
            password=password,
            prefix=prefix,
            username=username,
        )

        jsii.create(DataTerraformRemoteStateEtcdV3, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateEtcdV3Config",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, EtcdV3BackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "endpoints": "endpoints",
        "cacert_path": "cacertPath",
        "cert_path": "certPath",
        "key_path": "keyPath",
        "lock": "lock",
        "password": "password",
        "prefix": "prefix",
        "username": "username",
    },
)
class DataTerraformRemoteStateEtcdV3Config(
    DataTerraformRemoteStateConfig, EtcdV3BackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        endpoints: typing.List[str],
        cacert_path: typing.Optional[str] = None,
        cert_path: typing.Optional[str] = None,
        key_path: typing.Optional[str] = None,
        lock: typing.Optional[bool] = None,
        password: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param endpoints: 
        :param cacert_path: 
        :param cert_path: 
        :param key_path: 
        :param lock: 
        :param password: 
        :param prefix: 
        :param username: 

        stability
        :stability: experimental
        """
        self._values = {
            "endpoints": endpoints,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if cacert_path is not None:
            self._values["cacert_path"] = cacert_path
        if cert_path is not None:
            self._values["cert_path"] = cert_path
        if key_path is not None:
            self._values["key_path"] = key_path
        if lock is not None:
            self._values["lock"] = lock
        if password is not None:
            self._values["password"] = password
        if prefix is not None:
            self._values["prefix"] = prefix
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def endpoints(self) -> typing.List[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("endpoints")

    @builtins.property
    def cacert_path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("cacert_path")

    @builtins.property
    def cert_path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("cert_path")

    @builtins.property
    def key_path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key_path")

    @builtins.property
    def lock(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lock")

    @builtins.property
    def password(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("password")

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("prefix")

    @builtins.property
    def username(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateEtcdV3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateGcs(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateGcs",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        bucket: str,
        access_token: typing.Optional[str] = None,
        credentials: typing.Optional[str] = None,
        encryption_key: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param bucket: 
        :param access_token: 
        :param credentials: 
        :param encryption_key: 
        :param prefix: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateGcsConfig(
            defaults=defaults,
            workspace=workspace,
            bucket=bucket,
            access_token=access_token,
            credentials=credentials,
            encryption_key=encryption_key,
            prefix=prefix,
        )

        jsii.create(DataTerraformRemoteStateGcs, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateGcsConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, GcsBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "bucket": "bucket",
        "access_token": "accessToken",
        "credentials": "credentials",
        "encryption_key": "encryptionKey",
        "prefix": "prefix",
    },
)
class DataTerraformRemoteStateGcsConfig(
    DataTerraformRemoteStateConfig, GcsBackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        bucket: str,
        access_token: typing.Optional[str] = None,
        credentials: typing.Optional[str] = None,
        encryption_key: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param bucket: 
        :param access_token: 
        :param credentials: 
        :param encryption_key: 
        :param prefix: 

        stability
        :stability: experimental
        """
        self._values = {
            "bucket": bucket,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if access_token is not None:
            self._values["access_token"] = access_token
        if credentials is not None:
            self._values["credentials"] = credentials
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def bucket(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("bucket")

    @builtins.property
    def access_token(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("access_token")

    @builtins.property
    def credentials(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("credentials")

    @builtins.property
    def encryption_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("encryption_key")

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("prefix")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateGcsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateHttp(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateHttp",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        address: str,
        lock_address: typing.Optional[str] = None,
        lock_method: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        retry_max: typing.Optional[jsii.Number] = None,
        retry_wait_max: typing.Optional[jsii.Number] = None,
        retry_wait_min: typing.Optional[jsii.Number] = None,
        skip_cert_verification: typing.Optional[bool] = None,
        unlock_address: typing.Optional[str] = None,
        unlock_method: typing.Optional[str] = None,
        update_method: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param address: 
        :param lock_address: 
        :param lock_method: 
        :param password: 
        :param retry_max: 
        :param retry_wait_max: 
        :param retry_wait_min: 
        :param skip_cert_verification: 
        :param unlock_address: 
        :param unlock_method: 
        :param update_method: 
        :param username: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateHttpConfig(
            defaults=defaults,
            workspace=workspace,
            address=address,
            lock_address=lock_address,
            lock_method=lock_method,
            password=password,
            retry_max=retry_max,
            retry_wait_max=retry_wait_max,
            retry_wait_min=retry_wait_min,
            skip_cert_verification=skip_cert_verification,
            unlock_address=unlock_address,
            unlock_method=unlock_method,
            update_method=update_method,
            username=username,
        )

        jsii.create(DataTerraformRemoteStateHttp, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateHttpConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, HttpBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "address": "address",
        "lock_address": "lockAddress",
        "lock_method": "lockMethod",
        "password": "password",
        "retry_max": "retryMax",
        "retry_wait_max": "retryWaitMax",
        "retry_wait_min": "retryWaitMin",
        "skip_cert_verification": "skipCertVerification",
        "unlock_address": "unlockAddress",
        "unlock_method": "unlockMethod",
        "update_method": "updateMethod",
        "username": "username",
    },
)
class DataTerraformRemoteStateHttpConfig(
    DataTerraformRemoteStateConfig, HttpBackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        address: str,
        lock_address: typing.Optional[str] = None,
        lock_method: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        retry_max: typing.Optional[jsii.Number] = None,
        retry_wait_max: typing.Optional[jsii.Number] = None,
        retry_wait_min: typing.Optional[jsii.Number] = None,
        skip_cert_verification: typing.Optional[bool] = None,
        unlock_address: typing.Optional[str] = None,
        unlock_method: typing.Optional[str] = None,
        update_method: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param address: 
        :param lock_address: 
        :param lock_method: 
        :param password: 
        :param retry_max: 
        :param retry_wait_max: 
        :param retry_wait_min: 
        :param skip_cert_verification: 
        :param unlock_address: 
        :param unlock_method: 
        :param update_method: 
        :param username: 

        stability
        :stability: experimental
        """
        self._values = {
            "address": address,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if lock_address is not None:
            self._values["lock_address"] = lock_address
        if lock_method is not None:
            self._values["lock_method"] = lock_method
        if password is not None:
            self._values["password"] = password
        if retry_max is not None:
            self._values["retry_max"] = retry_max
        if retry_wait_max is not None:
            self._values["retry_wait_max"] = retry_wait_max
        if retry_wait_min is not None:
            self._values["retry_wait_min"] = retry_wait_min
        if skip_cert_verification is not None:
            self._values["skip_cert_verification"] = skip_cert_verification
        if unlock_address is not None:
            self._values["unlock_address"] = unlock_address
        if unlock_method is not None:
            self._values["unlock_method"] = unlock_method
        if update_method is not None:
            self._values["update_method"] = update_method
        if username is not None:
            self._values["username"] = username

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def address(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("address")

    @builtins.property
    def lock_address(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lock_address")

    @builtins.property
    def lock_method(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("lock_method")

    @builtins.property
    def password(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("password")

    @builtins.property
    def retry_max(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("retry_max")

    @builtins.property
    def retry_wait_max(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("retry_wait_max")

    @builtins.property
    def retry_wait_min(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("retry_wait_min")

    @builtins.property
    def skip_cert_verification(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("skip_cert_verification")

    @builtins.property
    def unlock_address(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("unlock_address")

    @builtins.property
    def unlock_method(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("unlock_method")

    @builtins.property
    def update_method(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("update_method")

    @builtins.property
    def username(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("username")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateHttpConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateLocal(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateLocal",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        path: typing.Optional[str] = None,
        workspace_dir: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param path: 
        :param workspace_dir: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateLocalConfig(
            defaults=defaults,
            workspace=workspace,
            path=path,
            workspace_dir=workspace_dir,
        )

        jsii.create(DataTerraformRemoteStateLocal, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateLocalConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, LocalBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "path": "path",
        "workspace_dir": "workspaceDir",
    },
)
class DataTerraformRemoteStateLocalConfig(
    DataTerraformRemoteStateConfig, LocalBackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        path: typing.Optional[str] = None,
        workspace_dir: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param path: 
        :param workspace_dir: 

        stability
        :stability: experimental
        """
        self._values = {}
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if path is not None:
            self._values["path"] = path
        if workspace_dir is not None:
            self._values["workspace_dir"] = workspace_dir

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def path(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("path")

    @builtins.property
    def workspace_dir(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace_dir")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateLocalConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateManta(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateManta",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        account: str,
        key_id: str,
        path: str,
        insecure_skip_tls_verify: typing.Optional[bool] = None,
        key_material: typing.Optional[str] = None,
        object_name: typing.Optional[str] = None,
        url: typing.Optional[str] = None,
        user: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param account: 
        :param key_id: 
        :param path: 
        :param insecure_skip_tls_verify: 
        :param key_material: 
        :param object_name: 
        :param url: 
        :param user: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateMantaConfig(
            defaults=defaults,
            workspace=workspace,
            account=account,
            key_id=key_id,
            path=path,
            insecure_skip_tls_verify=insecure_skip_tls_verify,
            key_material=key_material,
            object_name=object_name,
            url=url,
            user=user,
        )

        jsii.create(DataTerraformRemoteStateManta, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateMantaConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, MantaBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "account": "account",
        "key_id": "keyId",
        "path": "path",
        "insecure_skip_tls_verify": "insecureSkipTlsVerify",
        "key_material": "keyMaterial",
        "object_name": "objectName",
        "url": "url",
        "user": "user",
    },
)
class DataTerraformRemoteStateMantaConfig(
    DataTerraformRemoteStateConfig, MantaBackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        account: str,
        key_id: str,
        path: str,
        insecure_skip_tls_verify: typing.Optional[bool] = None,
        key_material: typing.Optional[str] = None,
        object_name: typing.Optional[str] = None,
        url: typing.Optional[str] = None,
        user: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param account: 
        :param key_id: 
        :param path: 
        :param insecure_skip_tls_verify: 
        :param key_material: 
        :param object_name: 
        :param url: 
        :param user: 

        stability
        :stability: experimental
        """
        self._values = {
            "account": account,
            "key_id": key_id,
            "path": path,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if insecure_skip_tls_verify is not None:
            self._values["insecure_skip_tls_verify"] = insecure_skip_tls_verify
        if key_material is not None:
            self._values["key_material"] = key_material
        if object_name is not None:
            self._values["object_name"] = object_name
        if url is not None:
            self._values["url"] = url
        if user is not None:
            self._values["user"] = user

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def account(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("account")

    @builtins.property
    def key_id(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key_id")

    @builtins.property
    def path(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("path")

    @builtins.property
    def insecure_skip_tls_verify(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("insecure_skip_tls_verify")

    @builtins.property
    def key_material(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key_material")

    @builtins.property
    def object_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("object_name")

    @builtins.property
    def url(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("url")

    @builtins.property
    def user(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("user")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateMantaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateOss(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateOss",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        bucket: str,
        access_key: typing.Optional[str] = None,
        acl: typing.Optional[str] = None,
        assume_role: typing.Optional["OssAssumeRole"] = None,
        ecs_role_name: typing.Optional[str] = None,
        encrypt: typing.Optional[bool] = None,
        endpoint: typing.Optional[str] = None,
        key: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
        profile: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
        security_token: typing.Optional[str] = None,
        shared_credentials_file: typing.Optional[str] = None,
        tablestore_endpoint: typing.Optional[str] = None,
        tablestore_table: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param bucket: 
        :param access_key: 
        :param acl: 
        :param assume_role: 
        :param ecs_role_name: 
        :param encrypt: 
        :param endpoint: 
        :param key: 
        :param prefix: 
        :param profile: 
        :param region: 
        :param secret_key: 
        :param security_token: 
        :param shared_credentials_file: 
        :param tablestore_endpoint: 
        :param tablestore_table: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateOssConfig(
            defaults=defaults,
            workspace=workspace,
            bucket=bucket,
            access_key=access_key,
            acl=acl,
            assume_role=assume_role,
            ecs_role_name=ecs_role_name,
            encrypt=encrypt,
            endpoint=endpoint,
            key=key,
            prefix=prefix,
            profile=profile,
            region=region,
            secret_key=secret_key,
            security_token=security_token,
            shared_credentials_file=shared_credentials_file,
            tablestore_endpoint=tablestore_endpoint,
            tablestore_table=tablestore_table,
        )

        jsii.create(DataTerraformRemoteStateOss, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateOssConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, OssBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "bucket": "bucket",
        "access_key": "accessKey",
        "acl": "acl",
        "assume_role": "assumeRole",
        "ecs_role_name": "ecsRoleName",
        "encrypt": "encrypt",
        "endpoint": "endpoint",
        "key": "key",
        "prefix": "prefix",
        "profile": "profile",
        "region": "region",
        "secret_key": "secretKey",
        "security_token": "securityToken",
        "shared_credentials_file": "sharedCredentialsFile",
        "tablestore_endpoint": "tablestoreEndpoint",
        "tablestore_table": "tablestoreTable",
    },
)
class DataTerraformRemoteStateOssConfig(
    DataTerraformRemoteStateConfig, OssBackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        bucket: str,
        access_key: typing.Optional[str] = None,
        acl: typing.Optional[str] = None,
        assume_role: typing.Optional["OssAssumeRole"] = None,
        ecs_role_name: typing.Optional[str] = None,
        encrypt: typing.Optional[bool] = None,
        endpoint: typing.Optional[str] = None,
        key: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
        profile: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
        security_token: typing.Optional[str] = None,
        shared_credentials_file: typing.Optional[str] = None,
        tablestore_endpoint: typing.Optional[str] = None,
        tablestore_table: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param bucket: 
        :param access_key: 
        :param acl: 
        :param assume_role: 
        :param ecs_role_name: 
        :param encrypt: 
        :param endpoint: 
        :param key: 
        :param prefix: 
        :param profile: 
        :param region: 
        :param secret_key: 
        :param security_token: 
        :param shared_credentials_file: 
        :param tablestore_endpoint: 
        :param tablestore_table: 

        stability
        :stability: experimental
        """
        if isinstance(assume_role, dict):
            assume_role = OssAssumeRole(**assume_role)
        self._values = {
            "bucket": bucket,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if access_key is not None:
            self._values["access_key"] = access_key
        if acl is not None:
            self._values["acl"] = acl
        if assume_role is not None:
            self._values["assume_role"] = assume_role
        if ecs_role_name is not None:
            self._values["ecs_role_name"] = ecs_role_name
        if encrypt is not None:
            self._values["encrypt"] = encrypt
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if key is not None:
            self._values["key"] = key
        if prefix is not None:
            self._values["prefix"] = prefix
        if profile is not None:
            self._values["profile"] = profile
        if region is not None:
            self._values["region"] = region
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if security_token is not None:
            self._values["security_token"] = security_token
        if shared_credentials_file is not None:
            self._values["shared_credentials_file"] = shared_credentials_file
        if tablestore_endpoint is not None:
            self._values["tablestore_endpoint"] = tablestore_endpoint
        if tablestore_table is not None:
            self._values["tablestore_table"] = tablestore_table

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def bucket(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("bucket")

    @builtins.property
    def access_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("access_key")

    @builtins.property
    def acl(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("acl")

    @builtins.property
    def assume_role(self) -> typing.Optional["OssAssumeRole"]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("assume_role")

    @builtins.property
    def ecs_role_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("ecs_role_name")

    @builtins.property
    def encrypt(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("encrypt")

    @builtins.property
    def endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("endpoint")

    @builtins.property
    def key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key")

    @builtins.property
    def prefix(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("prefix")

    @builtins.property
    def profile(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("profile")

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("region")

    @builtins.property
    def secret_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("secret_key")

    @builtins.property
    def security_token(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("security_token")

    @builtins.property
    def shared_credentials_file(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("shared_credentials_file")

    @builtins.property
    def tablestore_endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("tablestore_endpoint")

    @builtins.property
    def tablestore_table(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("tablestore_table")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateOssConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStatePg(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStatePg",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        conn_str: str,
        schema_name: typing.Optional[str] = None,
        skip_schema_creation: typing.Optional[bool] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param conn_str: 
        :param schema_name: 
        :param skip_schema_creation: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStatePgConfig(
            defaults=defaults,
            workspace=workspace,
            conn_str=conn_str,
            schema_name=schema_name,
            skip_schema_creation=skip_schema_creation,
        )

        jsii.create(DataTerraformRemoteStatePg, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStatePgConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, PgBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "conn_str": "connStr",
        "schema_name": "schemaName",
        "skip_schema_creation": "skipSchemaCreation",
    },
)
class DataTerraformRemoteStatePgConfig(DataTerraformRemoteStateConfig, PgBackendProps):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        conn_str: str,
        schema_name: typing.Optional[str] = None,
        skip_schema_creation: typing.Optional[bool] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param conn_str: 
        :param schema_name: 
        :param skip_schema_creation: 

        stability
        :stability: experimental
        """
        self._values = {
            "conn_str": conn_str,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if schema_name is not None:
            self._values["schema_name"] = schema_name
        if skip_schema_creation is not None:
            self._values["skip_schema_creation"] = skip_schema_creation

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def conn_str(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("conn_str")

    @builtins.property
    def schema_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("schema_name")

    @builtins.property
    def skip_schema_creation(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("skip_schema_creation")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStatePgConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateRemoteConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, RemoteBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "organization": "organization",
        "workspaces": "workspaces",
        "hostname": "hostname",
        "token": "token",
    },
)
class DataTerraformRemoteStateRemoteConfig(
    DataTerraformRemoteStateConfig, RemoteBackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        organization: str,
        workspaces: "IRemoteWorkspace",
        hostname: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param organization: 
        :param workspaces: 
        :param hostname: 
        :param token: 

        stability
        :stability: experimental
        """
        self._values = {
            "organization": organization,
            "workspaces": workspaces,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if hostname is not None:
            self._values["hostname"] = hostname
        if token is not None:
            self._values["token"] = token

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def organization(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("organization")

    @builtins.property
    def workspaces(self) -> "IRemoteWorkspace":
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspaces")

    @builtins.property
    def hostname(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("hostname")

    @builtins.property
    def token(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("token")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateRemoteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateS3(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateS3",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        bucket: str,
        key: str,
        access_key: typing.Optional[str] = None,
        acl: typing.Optional[str] = None,
        assume_role_policy: typing.Optional[str] = None,
        dynamodb_endpoint: typing.Optional[str] = None,
        dynamodb_table: typing.Optional[str] = None,
        encrypt: typing.Optional[bool] = None,
        endpoint: typing.Optional[str] = None,
        external_id: typing.Optional[str] = None,
        force_path_style: typing.Optional[bool] = None,
        iam_endpoint: typing.Optional[str] = None,
        kms_key_id: typing.Optional[str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        profile: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
        role_arn: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
        session_name: typing.Optional[str] = None,
        shared_credentials_file: typing.Optional[str] = None,
        skip_credentials_validation: typing.Optional[bool] = None,
        skip_metadata_api_check: typing.Optional[bool] = None,
        sse_customer_key: typing.Optional[str] = None,
        sts_endpoint: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        workspace_key_prefix: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param bucket: 
        :param key: 
        :param access_key: 
        :param acl: 
        :param assume_role_policy: 
        :param dynamodb_endpoint: 
        :param dynamodb_table: 
        :param encrypt: 
        :param endpoint: 
        :param external_id: 
        :param force_path_style: 
        :param iam_endpoint: 
        :param kms_key_id: 
        :param max_retries: 
        :param profile: 
        :param region: 
        :param role_arn: 
        :param secret_key: 
        :param session_name: 
        :param shared_credentials_file: 
        :param skip_credentials_validation: 
        :param skip_metadata_api_check: 
        :param sse_customer_key: 
        :param sts_endpoint: 
        :param token: 
        :param workspace_key_prefix: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateS3Config(
            defaults=defaults,
            workspace=workspace,
            bucket=bucket,
            key=key,
            access_key=access_key,
            acl=acl,
            assume_role_policy=assume_role_policy,
            dynamodb_endpoint=dynamodb_endpoint,
            dynamodb_table=dynamodb_table,
            encrypt=encrypt,
            endpoint=endpoint,
            external_id=external_id,
            force_path_style=force_path_style,
            iam_endpoint=iam_endpoint,
            kms_key_id=kms_key_id,
            max_retries=max_retries,
            profile=profile,
            region=region,
            role_arn=role_arn,
            secret_key=secret_key,
            session_name=session_name,
            shared_credentials_file=shared_credentials_file,
            skip_credentials_validation=skip_credentials_validation,
            skip_metadata_api_check=skip_metadata_api_check,
            sse_customer_key=sse_customer_key,
            sts_endpoint=sts_endpoint,
            token=token,
            workspace_key_prefix=workspace_key_prefix,
        )

        jsii.create(DataTerraformRemoteStateS3, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateS3Config",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, S3BackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "bucket": "bucket",
        "key": "key",
        "access_key": "accessKey",
        "acl": "acl",
        "assume_role_policy": "assumeRolePolicy",
        "dynamodb_endpoint": "dynamodbEndpoint",
        "dynamodb_table": "dynamodbTable",
        "encrypt": "encrypt",
        "endpoint": "endpoint",
        "external_id": "externalId",
        "force_path_style": "forcePathStyle",
        "iam_endpoint": "iamEndpoint",
        "kms_key_id": "kmsKeyId",
        "max_retries": "maxRetries",
        "profile": "profile",
        "region": "region",
        "role_arn": "roleArn",
        "secret_key": "secretKey",
        "session_name": "sessionName",
        "shared_credentials_file": "sharedCredentialsFile",
        "skip_credentials_validation": "skipCredentialsValidation",
        "skip_metadata_api_check": "skipMetadataApiCheck",
        "sse_customer_key": "sseCustomerKey",
        "sts_endpoint": "stsEndpoint",
        "token": "token",
        "workspace_key_prefix": "workspaceKeyPrefix",
    },
)
class DataTerraformRemoteStateS3Config(DataTerraformRemoteStateConfig, S3BackendProps):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        bucket: str,
        key: str,
        access_key: typing.Optional[str] = None,
        acl: typing.Optional[str] = None,
        assume_role_policy: typing.Optional[str] = None,
        dynamodb_endpoint: typing.Optional[str] = None,
        dynamodb_table: typing.Optional[str] = None,
        encrypt: typing.Optional[bool] = None,
        endpoint: typing.Optional[str] = None,
        external_id: typing.Optional[str] = None,
        force_path_style: typing.Optional[bool] = None,
        iam_endpoint: typing.Optional[str] = None,
        kms_key_id: typing.Optional[str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        profile: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
        role_arn: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
        session_name: typing.Optional[str] = None,
        shared_credentials_file: typing.Optional[str] = None,
        skip_credentials_validation: typing.Optional[bool] = None,
        skip_metadata_api_check: typing.Optional[bool] = None,
        sse_customer_key: typing.Optional[str] = None,
        sts_endpoint: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        workspace_key_prefix: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param bucket: 
        :param key: 
        :param access_key: 
        :param acl: 
        :param assume_role_policy: 
        :param dynamodb_endpoint: 
        :param dynamodb_table: 
        :param encrypt: 
        :param endpoint: 
        :param external_id: 
        :param force_path_style: 
        :param iam_endpoint: 
        :param kms_key_id: 
        :param max_retries: 
        :param profile: 
        :param region: 
        :param role_arn: 
        :param secret_key: 
        :param session_name: 
        :param shared_credentials_file: 
        :param skip_credentials_validation: 
        :param skip_metadata_api_check: 
        :param sse_customer_key: 
        :param sts_endpoint: 
        :param token: 
        :param workspace_key_prefix: 

        stability
        :stability: experimental
        """
        self._values = {
            "bucket": bucket,
            "key": key,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if access_key is not None:
            self._values["access_key"] = access_key
        if acl is not None:
            self._values["acl"] = acl
        if assume_role_policy is not None:
            self._values["assume_role_policy"] = assume_role_policy
        if dynamodb_endpoint is not None:
            self._values["dynamodb_endpoint"] = dynamodb_endpoint
        if dynamodb_table is not None:
            self._values["dynamodb_table"] = dynamodb_table
        if encrypt is not None:
            self._values["encrypt"] = encrypt
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if external_id is not None:
            self._values["external_id"] = external_id
        if force_path_style is not None:
            self._values["force_path_style"] = force_path_style
        if iam_endpoint is not None:
            self._values["iam_endpoint"] = iam_endpoint
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if max_retries is not None:
            self._values["max_retries"] = max_retries
        if profile is not None:
            self._values["profile"] = profile
        if region is not None:
            self._values["region"] = region
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if secret_key is not None:
            self._values["secret_key"] = secret_key
        if session_name is not None:
            self._values["session_name"] = session_name
        if shared_credentials_file is not None:
            self._values["shared_credentials_file"] = shared_credentials_file
        if skip_credentials_validation is not None:
            self._values["skip_credentials_validation"] = skip_credentials_validation
        if skip_metadata_api_check is not None:
            self._values["skip_metadata_api_check"] = skip_metadata_api_check
        if sse_customer_key is not None:
            self._values["sse_customer_key"] = sse_customer_key
        if sts_endpoint is not None:
            self._values["sts_endpoint"] = sts_endpoint
        if token is not None:
            self._values["token"] = token
        if workspace_key_prefix is not None:
            self._values["workspace_key_prefix"] = workspace_key_prefix

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def bucket(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("bucket")

    @builtins.property
    def key(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key")

    @builtins.property
    def access_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("access_key")

    @builtins.property
    def acl(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("acl")

    @builtins.property
    def assume_role_policy(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("assume_role_policy")

    @builtins.property
    def dynamodb_endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("dynamodb_endpoint")

    @builtins.property
    def dynamodb_table(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("dynamodb_table")

    @builtins.property
    def encrypt(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("encrypt")

    @builtins.property
    def endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("endpoint")

    @builtins.property
    def external_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("external_id")

    @builtins.property
    def force_path_style(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("force_path_style")

    @builtins.property
    def iam_endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("iam_endpoint")

    @builtins.property
    def kms_key_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("kms_key_id")

    @builtins.property
    def max_retries(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("max_retries")

    @builtins.property
    def profile(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("profile")

    @builtins.property
    def region(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("region")

    @builtins.property
    def role_arn(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("role_arn")

    @builtins.property
    def secret_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("secret_key")

    @builtins.property
    def session_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("session_name")

    @builtins.property
    def shared_credentials_file(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("shared_credentials_file")

    @builtins.property
    def skip_credentials_validation(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("skip_credentials_validation")

    @builtins.property
    def skip_metadata_api_check(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("skip_metadata_api_check")

    @builtins.property
    def sse_customer_key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("sse_customer_key")

    @builtins.property
    def sts_endpoint(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("sts_endpoint")

    @builtins.property
    def token(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("token")

    @builtins.property
    def workspace_key_prefix(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace_key_prefix")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateS3Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DataTerraformRemoteStateSwift(
    TerraformRemoteState,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdktf.DataTerraformRemoteStateSwift",
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        container: str,
        application_credential_id: typing.Optional[str] = None,
        application_credential_name: typing.Optional[str] = None,
        application_credential_secret: typing.Optional[str] = None,
        archive_container: typing.Optional[str] = None,
        auth_url: typing.Optional[str] = None,
        cacert_file: typing.Optional[str] = None,
        cert: typing.Optional[str] = None,
        cloud: typing.Optional[str] = None,
        default_domain: typing.Optional[str] = None,
        domain_id: typing.Optional[str] = None,
        domain_name: typing.Optional[str] = None,
        expire_after: typing.Optional[str] = None,
        insecure: typing.Optional[bool] = None,
        key: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        project_domain_id: typing.Optional[str] = None,
        project_domain_name: typing.Optional[str] = None,
        region_name: typing.Optional[str] = None,
        state_name: typing.Optional[str] = None,
        tenant_id: typing.Optional[str] = None,
        tenant_name: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        user_domain_id: typing.Optional[str] = None,
        user_domain_name: typing.Optional[str] = None,
        user_id: typing.Optional[str] = None,
        user_name: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param defaults: 
        :param workspace: 
        :param container: 
        :param application_credential_id: 
        :param application_credential_name: 
        :param application_credential_secret: 
        :param archive_container: 
        :param auth_url: 
        :param cacert_file: 
        :param cert: 
        :param cloud: 
        :param default_domain: 
        :param domain_id: 
        :param domain_name: 
        :param expire_after: 
        :param insecure: 
        :param key: 
        :param password: 
        :param project_domain_id: 
        :param project_domain_name: 
        :param region_name: 
        :param state_name: 
        :param tenant_id: 
        :param tenant_name: 
        :param token: 
        :param user_domain_id: 
        :param user_domain_name: 
        :param user_id: 
        :param user_name: 

        stability
        :stability: experimental
        """
        config = DataTerraformRemoteStateSwiftConfig(
            defaults=defaults,
            workspace=workspace,
            container=container,
            application_credential_id=application_credential_id,
            application_credential_name=application_credential_name,
            application_credential_secret=application_credential_secret,
            archive_container=archive_container,
            auth_url=auth_url,
            cacert_file=cacert_file,
            cert=cert,
            cloud=cloud,
            default_domain=default_domain,
            domain_id=domain_id,
            domain_name=domain_name,
            expire_after=expire_after,
            insecure=insecure,
            key=key,
            password=password,
            project_domain_id=project_domain_id,
            project_domain_name=project_domain_name,
            region_name=region_name,
            state_name=state_name,
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            token=token,
            user_domain_id=user_domain_id,
            user_domain_name=user_domain_name,
            user_id=user_id,
            user_name=user_name,
        )

        jsii.create(DataTerraformRemoteStateSwift, self, [scope, id, config])


@jsii.data_type(
    jsii_type="cdktf.DataTerraformRemoteStateSwiftConfig",
    jsii_struct_bases=[DataTerraformRemoteStateConfig, SwiftBackendProps],
    name_mapping={
        "defaults": "defaults",
        "workspace": "workspace",
        "container": "container",
        "application_credential_id": "applicationCredentialId",
        "application_credential_name": "applicationCredentialName",
        "application_credential_secret": "applicationCredentialSecret",
        "archive_container": "archiveContainer",
        "auth_url": "authUrl",
        "cacert_file": "cacertFile",
        "cert": "cert",
        "cloud": "cloud",
        "default_domain": "defaultDomain",
        "domain_id": "domainId",
        "domain_name": "domainName",
        "expire_after": "expireAfter",
        "insecure": "insecure",
        "key": "key",
        "password": "password",
        "project_domain_id": "projectDomainId",
        "project_domain_name": "projectDomainName",
        "region_name": "regionName",
        "state_name": "stateName",
        "tenant_id": "tenantId",
        "tenant_name": "tenantName",
        "token": "token",
        "user_domain_id": "userDomainId",
        "user_domain_name": "userDomainName",
        "user_id": "userId",
        "user_name": "userName",
    },
)
class DataTerraformRemoteStateSwiftConfig(
    DataTerraformRemoteStateConfig, SwiftBackendProps
):
    def __init__(
        self,
        *,
        defaults: typing.Optional[typing.Mapping[str, typing.Any]] = None,
        workspace: typing.Optional[str] = None,
        container: str,
        application_credential_id: typing.Optional[str] = None,
        application_credential_name: typing.Optional[str] = None,
        application_credential_secret: typing.Optional[str] = None,
        archive_container: typing.Optional[str] = None,
        auth_url: typing.Optional[str] = None,
        cacert_file: typing.Optional[str] = None,
        cert: typing.Optional[str] = None,
        cloud: typing.Optional[str] = None,
        default_domain: typing.Optional[str] = None,
        domain_id: typing.Optional[str] = None,
        domain_name: typing.Optional[str] = None,
        expire_after: typing.Optional[str] = None,
        insecure: typing.Optional[bool] = None,
        key: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        project_domain_id: typing.Optional[str] = None,
        project_domain_name: typing.Optional[str] = None,
        region_name: typing.Optional[str] = None,
        state_name: typing.Optional[str] = None,
        tenant_id: typing.Optional[str] = None,
        tenant_name: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        user_domain_id: typing.Optional[str] = None,
        user_domain_name: typing.Optional[str] = None,
        user_id: typing.Optional[str] = None,
        user_name: typing.Optional[str] = None,
    ) -> None:
        """
        :param defaults: 
        :param workspace: 
        :param container: 
        :param application_credential_id: 
        :param application_credential_name: 
        :param application_credential_secret: 
        :param archive_container: 
        :param auth_url: 
        :param cacert_file: 
        :param cert: 
        :param cloud: 
        :param default_domain: 
        :param domain_id: 
        :param domain_name: 
        :param expire_after: 
        :param insecure: 
        :param key: 
        :param password: 
        :param project_domain_id: 
        :param project_domain_name: 
        :param region_name: 
        :param state_name: 
        :param tenant_id: 
        :param tenant_name: 
        :param token: 
        :param user_domain_id: 
        :param user_domain_name: 
        :param user_id: 
        :param user_name: 

        stability
        :stability: experimental
        """
        self._values = {
            "container": container,
        }
        if defaults is not None:
            self._values["defaults"] = defaults
        if workspace is not None:
            self._values["workspace"] = workspace
        if application_credential_id is not None:
            self._values["application_credential_id"] = application_credential_id
        if application_credential_name is not None:
            self._values["application_credential_name"] = application_credential_name
        if application_credential_secret is not None:
            self._values["application_credential_secret"] = application_credential_secret
        if archive_container is not None:
            self._values["archive_container"] = archive_container
        if auth_url is not None:
            self._values["auth_url"] = auth_url
        if cacert_file is not None:
            self._values["cacert_file"] = cacert_file
        if cert is not None:
            self._values["cert"] = cert
        if cloud is not None:
            self._values["cloud"] = cloud
        if default_domain is not None:
            self._values["default_domain"] = default_domain
        if domain_id is not None:
            self._values["domain_id"] = domain_id
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if expire_after is not None:
            self._values["expire_after"] = expire_after
        if insecure is not None:
            self._values["insecure"] = insecure
        if key is not None:
            self._values["key"] = key
        if password is not None:
            self._values["password"] = password
        if project_domain_id is not None:
            self._values["project_domain_id"] = project_domain_id
        if project_domain_name is not None:
            self._values["project_domain_name"] = project_domain_name
        if region_name is not None:
            self._values["region_name"] = region_name
        if state_name is not None:
            self._values["state_name"] = state_name
        if tenant_id is not None:
            self._values["tenant_id"] = tenant_id
        if tenant_name is not None:
            self._values["tenant_name"] = tenant_name
        if token is not None:
            self._values["token"] = token
        if user_domain_id is not None:
            self._values["user_domain_id"] = user_domain_id
        if user_domain_name is not None:
            self._values["user_domain_name"] = user_domain_name
        if user_id is not None:
            self._values["user_id"] = user_id
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def defaults(self) -> typing.Optional[typing.Mapping[str, typing.Any]]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("defaults")

    @builtins.property
    def workspace(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("workspace")

    @builtins.property
    def container(self) -> str:
        """
        stability
        :stability: experimental
        """
        return self._values.get("container")

    @builtins.property
    def application_credential_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("application_credential_id")

    @builtins.property
    def application_credential_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("application_credential_name")

    @builtins.property
    def application_credential_secret(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("application_credential_secret")

    @builtins.property
    def archive_container(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("archive_container")

    @builtins.property
    def auth_url(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("auth_url")

    @builtins.property
    def cacert_file(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("cacert_file")

    @builtins.property
    def cert(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("cert")

    @builtins.property
    def cloud(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("cloud")

    @builtins.property
    def default_domain(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("default_domain")

    @builtins.property
    def domain_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("domain_id")

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("domain_name")

    @builtins.property
    def expire_after(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("expire_after")

    @builtins.property
    def insecure(self) -> typing.Optional[bool]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("insecure")

    @builtins.property
    def key(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("key")

    @builtins.property
    def password(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("password")

    @builtins.property
    def project_domain_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("project_domain_id")

    @builtins.property
    def project_domain_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("project_domain_name")

    @builtins.property
    def region_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("region_name")

    @builtins.property
    def state_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("state_name")

    @builtins.property
    def tenant_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("tenant_id")

    @builtins.property
    def tenant_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("tenant_name")

    @builtins.property
    def token(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("token")

    @builtins.property
    def user_domain_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("user_domain_id")

    @builtins.property
    def user_domain_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("user_domain_name")

    @builtins.property
    def user_id(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("user_id")

    @builtins.property
    def user_name(self) -> typing.Optional[str]:
        """
        stability
        :stability: experimental
        """
        return self._values.get("user_name")

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DataTerraformRemoteStateSwiftConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(ITokenResolver)
class DefaultTokenResolver(
    metaclass=jsii.JSIIMeta, jsii_type="cdktf.DefaultTokenResolver"
):
    """Default resolver implementation.

    stability
    :stability: experimental
    """

    def __init__(self, concat: "IFragmentConcatenator") -> None:
        """
        :param concat: -

        stability
        :stability: experimental
        """
        jsii.create(DefaultTokenResolver, self, [concat])

    @jsii.member(jsii_name="resolveList")
    def resolve_list(
        self, xs: typing.List[str], context: "IResolveContext"
    ) -> typing.Any:
        """Resolve a tokenized list.

        :param xs: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveList", [xs, context])

    @jsii.member(jsii_name="resolveString")
    def resolve_string(
        self, fragments: "TokenizedStringFragments", context: "IResolveContext"
    ) -> typing.Any:
        """Resolve string fragments to Tokens.

        :param fragments: -
        :param context: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveString", [fragments, context])

    @jsii.member(jsii_name="resolveToken")
    def resolve_token(
        self,
        t: "IResolvable",
        context: "IResolveContext",
        post_processor: "IPostProcessor",
    ) -> typing.Any:
        """Default Token resolution.

        Resolve the Token, recurse into whatever it returns,
        then finally post-process it.

        :param t: -
        :param context: -
        :param post_processor: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "resolveToken", [t, context, post_processor])


class TerraformBackend(
    TerraformElement,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdktf.TerraformBackend",
):
    """
    stability
    :stability: experimental
    """

    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _TerraformBackendProxy

    def __init__(self, scope: constructs.Construct, id: str, name: str) -> None:
        """
        :param scope: -
        :param id: -
        :param name: -

        stability
        :stability: experimental
        """
        jsii.create(TerraformBackend, self, [scope, id, name])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """Adds this resource to the terraform JSON output.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="name")
    def _name(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "name")


class _TerraformBackendProxy(TerraformBackend):
    pass


@jsii.implements(ITerraformResource)
class TerraformDataSource(
    TerraformElement, metaclass=jsii.JSIIMeta, jsii_type="cdktf.TerraformDataSource"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        id: str,
        *,
        terraform_resource_type: str,
        terraform_generator_metadata: typing.Optional["TerraformGeneratorMetadata"] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.List["TerraformResource"]] = None,
        lifecycle: typing.Optional["TerraformResourceLifecycle"] = None,
        provider: typing.Optional["TerraformProvider"] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param terraform_resource_type: 
        :param terraform_generator_metadata: 
        :param count: 
        :param depends_on: 
        :param lifecycle: 
        :param provider: 

        stability
        :stability: experimental
        """
        config = TerraformResourceConfig(
            terraform_resource_type=terraform_resource_type,
            terraform_generator_metadata=terraform_generator_metadata,
            count=count,
            depends_on=depends_on,
            lifecycle=lifecycle,
            provider=provider,
        )

        jsii.create(TerraformDataSource, self, [scope, id, config])

    @jsii.member(jsii_name="getBooleanAttribute")
    def get_boolean_attribute(self, terraform_attribute: str) -> bool:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getBooleanAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getListAttribute")
    def get_list_attribute(self, terraform_attribute: str) -> typing.List[str]:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getListAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getNumberAttribute")
    def get_number_attribute(self, terraform_attribute: str) -> jsii.Number:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getNumberAttribute", [terraform_attribute])

    @jsii.member(jsii_name="getStringAttribute")
    def get_string_attribute(self, terraform_attribute: str) -> str:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "getStringAttribute", [terraform_attribute])

    @jsii.member(jsii_name="interpolationForAttribute")
    def interpolation_for_attribute(self, terraform_attribute: str) -> str:
        """
        :param terraform_attribute: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "interpolationForAttribute", [terraform_attribute])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])

    @jsii.member(jsii_name="toTerraform")
    def to_terraform(self) -> typing.Any:
        """Adds this resource to the terraform JSON output.

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "toTerraform", [])

    @builtins.property
    @jsii.member(jsii_name="fqn")
    def fqn(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "fqn")

    @builtins.property
    @jsii.member(jsii_name="terraformMetaArguments")
    def terraform_meta_arguments(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformMetaArguments")

    @builtins.property
    @jsii.member(jsii_name="terraformResourceType")
    def terraform_resource_type(self) -> str:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformResourceType")

    @builtins.property
    @jsii.member(jsii_name="terraformGeneratorMetadata")
    def terraform_generator_metadata(
        self,
    ) -> typing.Optional["TerraformGeneratorMetadata"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "terraformGeneratorMetadata")

    @builtins.property
    @jsii.member(jsii_name="count")
    def count(self) -> typing.Optional[jsii.Number]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "count")

    @count.setter
    def count(self, value: typing.Optional[jsii.Number]) -> None:
        jsii.set(self, "count", value)

    @builtins.property
    @jsii.member(jsii_name="dependsOn")
    def depends_on(self) -> typing.Optional[typing.List[str]]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "dependsOn")

    @depends_on.setter
    def depends_on(self, value: typing.Optional[typing.List[str]]) -> None:
        jsii.set(self, "dependsOn", value)

    @builtins.property
    @jsii.member(jsii_name="lifecycle")
    def lifecycle(self) -> typing.Optional["TerraformResourceLifecycle"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "lifecycle")

    @lifecycle.setter
    def lifecycle(self, value: typing.Optional["TerraformResourceLifecycle"]) -> None:
        jsii.set(self, "lifecycle", value)

    @builtins.property
    @jsii.member(jsii_name="provider")
    def provider(self) -> typing.Optional["TerraformProvider"]:
        """
        stability
        :stability: experimental
        """
        return jsii.get(self, "provider")

    @provider.setter
    def provider(self, value: typing.Optional["TerraformProvider"]) -> None:
        jsii.set(self, "provider", value)


class ArtifactoryBackend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.ArtifactoryBackend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        password: str,
        repo: str,
        subpath: str,
        url: str,
        username: str,
    ) -> None:
        """
        :param scope: -
        :param password: 
        :param repo: 
        :param subpath: 
        :param url: 
        :param username: 

        stability
        :stability: experimental
        """
        props = ArtifactoryBackendProps(
            password=password, repo=repo, subpath=subpath, url=url, username=username
        )

        jsii.create(ArtifactoryBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class AzurermBackend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.AzurermBackend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        container_name: str,
        key: str,
        storage_account_name: str,
        access_key: typing.Optional[str] = None,
        client_id: typing.Optional[str] = None,
        client_secret: typing.Optional[str] = None,
        endpoint: typing.Optional[str] = None,
        environment: typing.Optional[str] = None,
        msi_endpoint: typing.Optional[str] = None,
        resource_group_name: typing.Optional[str] = None,
        sas_token: typing.Optional[str] = None,
        subscription_id: typing.Optional[str] = None,
        tenant_id: typing.Optional[str] = None,
        use_msi: typing.Optional[bool] = None,
    ) -> None:
        """
        :param scope: -
        :param container_name: 
        :param key: 
        :param storage_account_name: 
        :param access_key: 
        :param client_id: 
        :param client_secret: 
        :param endpoint: 
        :param environment: 
        :param msi_endpoint: 
        :param resource_group_name: 
        :param sas_token: 
        :param subscription_id: 
        :param tenant_id: 
        :param use_msi: 

        stability
        :stability: experimental
        """
        props = AzurermBackendProps(
            container_name=container_name,
            key=key,
            storage_account_name=storage_account_name,
            access_key=access_key,
            client_id=client_id,
            client_secret=client_secret,
            endpoint=endpoint,
            environment=environment,
            msi_endpoint=msi_endpoint,
            resource_group_name=resource_group_name,
            sas_token=sas_token,
            subscription_id=subscription_id,
            tenant_id=tenant_id,
            use_msi=use_msi,
        )

        jsii.create(AzurermBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class ConsulBackend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.ConsulBackend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        access_token: str,
        path: str,
        address: typing.Optional[str] = None,
        ca_file: typing.Optional[str] = None,
        cert_file: typing.Optional[str] = None,
        datacenter: typing.Optional[str] = None,
        gzip: typing.Optional[bool] = None,
        http_auth: typing.Optional[str] = None,
        key_file: typing.Optional[str] = None,
        lock: typing.Optional[bool] = None,
        scheme: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param access_token: 
        :param path: 
        :param address: 
        :param ca_file: 
        :param cert_file: 
        :param datacenter: 
        :param gzip: 
        :param http_auth: 
        :param key_file: 
        :param lock: 
        :param scheme: 

        stability
        :stability: experimental
        """
        props = ConsulBackendProps(
            access_token=access_token,
            path=path,
            address=address,
            ca_file=ca_file,
            cert_file=cert_file,
            datacenter=datacenter,
            gzip=gzip,
            http_auth=http_auth,
            key_file=key_file,
            lock=lock,
            scheme=scheme,
        )

        jsii.create(ConsulBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class CosBackend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.CosBackend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        bucket: str,
        acl: typing.Optional[str] = None,
        encrypt: typing.Optional[bool] = None,
        key: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
        secret_id: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param bucket: 
        :param acl: 
        :param encrypt: 
        :param key: 
        :param prefix: 
        :param region: 
        :param secret_id: 
        :param secret_key: 

        stability
        :stability: experimental
        """
        props = CosBackendProps(
            bucket=bucket,
            acl=acl,
            encrypt=encrypt,
            key=key,
            prefix=prefix,
            region=region,
            secret_id=secret_id,
            secret_key=secret_key,
        )

        jsii.create(CosBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class EtcdBackend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.EtcdBackend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        endpoints: str,
        path: str,
        password: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param endpoints: 
        :param path: 
        :param password: 
        :param username: 

        stability
        :stability: experimental
        """
        props = EtcdBackendProps(
            endpoints=endpoints, path=path, password=password, username=username
        )

        jsii.create(EtcdBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class EtcdV3Backend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.EtcdV3Backend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        endpoints: typing.List[str],
        cacert_path: typing.Optional[str] = None,
        cert_path: typing.Optional[str] = None,
        key_path: typing.Optional[str] = None,
        lock: typing.Optional[bool] = None,
        password: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param endpoints: 
        :param cacert_path: 
        :param cert_path: 
        :param key_path: 
        :param lock: 
        :param password: 
        :param prefix: 
        :param username: 

        stability
        :stability: experimental
        """
        props = EtcdV3BackendProps(
            endpoints=endpoints,
            cacert_path=cacert_path,
            cert_path=cert_path,
            key_path=key_path,
            lock=lock,
            password=password,
            prefix=prefix,
            username=username,
        )

        jsii.create(EtcdV3Backend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class GcsBackend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.GcsBackend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        bucket: str,
        access_token: typing.Optional[str] = None,
        credentials: typing.Optional[str] = None,
        encryption_key: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param bucket: 
        :param access_token: 
        :param credentials: 
        :param encryption_key: 
        :param prefix: 

        stability
        :stability: experimental
        """
        props = GcsBackendProps(
            bucket=bucket,
            access_token=access_token,
            credentials=credentials,
            encryption_key=encryption_key,
            prefix=prefix,
        )

        jsii.create(GcsBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class HttpBackend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.HttpBackend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        address: str,
        lock_address: typing.Optional[str] = None,
        lock_method: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        retry_max: typing.Optional[jsii.Number] = None,
        retry_wait_max: typing.Optional[jsii.Number] = None,
        retry_wait_min: typing.Optional[jsii.Number] = None,
        skip_cert_verification: typing.Optional[bool] = None,
        unlock_address: typing.Optional[str] = None,
        unlock_method: typing.Optional[str] = None,
        update_method: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param address: 
        :param lock_address: 
        :param lock_method: 
        :param password: 
        :param retry_max: 
        :param retry_wait_max: 
        :param retry_wait_min: 
        :param skip_cert_verification: 
        :param unlock_address: 
        :param unlock_method: 
        :param update_method: 
        :param username: 

        stability
        :stability: experimental
        """
        props = HttpBackendProps(
            address=address,
            lock_address=lock_address,
            lock_method=lock_method,
            password=password,
            retry_max=retry_max,
            retry_wait_max=retry_wait_max,
            retry_wait_min=retry_wait_min,
            skip_cert_verification=skip_cert_verification,
            unlock_address=unlock_address,
            unlock_method=unlock_method,
            update_method=update_method,
            username=username,
        )

        jsii.create(HttpBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class LocalBackend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.LocalBackend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        path: typing.Optional[str] = None,
        workspace_dir: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param path: 
        :param workspace_dir: 

        stability
        :stability: experimental
        """
        props = LocalBackendProps(path=path, workspace_dir=workspace_dir)

        jsii.create(LocalBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class MantaBackend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.MantaBackend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        account: str,
        key_id: str,
        path: str,
        insecure_skip_tls_verify: typing.Optional[bool] = None,
        key_material: typing.Optional[str] = None,
        object_name: typing.Optional[str] = None,
        url: typing.Optional[str] = None,
        user: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param account: 
        :param key_id: 
        :param path: 
        :param insecure_skip_tls_verify: 
        :param key_material: 
        :param object_name: 
        :param url: 
        :param user: 

        stability
        :stability: experimental
        """
        props = MantaBackendProps(
            account=account,
            key_id=key_id,
            path=path,
            insecure_skip_tls_verify=insecure_skip_tls_verify,
            key_material=key_material,
            object_name=object_name,
            url=url,
            user=user,
        )

        jsii.create(MantaBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class OssBackend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.OssBackend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        bucket: str,
        access_key: typing.Optional[str] = None,
        acl: typing.Optional[str] = None,
        assume_role: typing.Optional["OssAssumeRole"] = None,
        ecs_role_name: typing.Optional[str] = None,
        encrypt: typing.Optional[bool] = None,
        endpoint: typing.Optional[str] = None,
        key: typing.Optional[str] = None,
        prefix: typing.Optional[str] = None,
        profile: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
        security_token: typing.Optional[str] = None,
        shared_credentials_file: typing.Optional[str] = None,
        tablestore_endpoint: typing.Optional[str] = None,
        tablestore_table: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param bucket: 
        :param access_key: 
        :param acl: 
        :param assume_role: 
        :param ecs_role_name: 
        :param encrypt: 
        :param endpoint: 
        :param key: 
        :param prefix: 
        :param profile: 
        :param region: 
        :param secret_key: 
        :param security_token: 
        :param shared_credentials_file: 
        :param tablestore_endpoint: 
        :param tablestore_table: 

        stability
        :stability: experimental
        """
        props = OssBackendProps(
            bucket=bucket,
            access_key=access_key,
            acl=acl,
            assume_role=assume_role,
            ecs_role_name=ecs_role_name,
            encrypt=encrypt,
            endpoint=endpoint,
            key=key,
            prefix=prefix,
            profile=profile,
            region=region,
            secret_key=secret_key,
            security_token=security_token,
            shared_credentials_file=shared_credentials_file,
            tablestore_endpoint=tablestore_endpoint,
            tablestore_table=tablestore_table,
        )

        jsii.create(OssBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class PgBackend(TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.PgBackend"):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        conn_str: str,
        schema_name: typing.Optional[str] = None,
        skip_schema_creation: typing.Optional[bool] = None,
    ) -> None:
        """
        :param scope: -
        :param conn_str: 
        :param schema_name: 
        :param skip_schema_creation: 

        stability
        :stability: experimental
        """
        props = PgBackendProps(
            conn_str=conn_str,
            schema_name=schema_name,
            skip_schema_creation=skip_schema_creation,
        )

        jsii.create(PgBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class RemoteBackend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.RemoteBackend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        organization: str,
        workspaces: "IRemoteWorkspace",
        hostname: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param organization: 
        :param workspaces: 
        :param hostname: 
        :param token: 

        stability
        :stability: experimental
        """
        props = RemoteBackendProps(
            organization=organization,
            workspaces=workspaces,
            hostname=hostname,
            token=token,
        )

        jsii.create(RemoteBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class S3Backend(TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.S3Backend"):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        bucket: str,
        key: str,
        access_key: typing.Optional[str] = None,
        acl: typing.Optional[str] = None,
        assume_role_policy: typing.Optional[str] = None,
        dynamodb_endpoint: typing.Optional[str] = None,
        dynamodb_table: typing.Optional[str] = None,
        encrypt: typing.Optional[bool] = None,
        endpoint: typing.Optional[str] = None,
        external_id: typing.Optional[str] = None,
        force_path_style: typing.Optional[bool] = None,
        iam_endpoint: typing.Optional[str] = None,
        kms_key_id: typing.Optional[str] = None,
        max_retries: typing.Optional[jsii.Number] = None,
        profile: typing.Optional[str] = None,
        region: typing.Optional[str] = None,
        role_arn: typing.Optional[str] = None,
        secret_key: typing.Optional[str] = None,
        session_name: typing.Optional[str] = None,
        shared_credentials_file: typing.Optional[str] = None,
        skip_credentials_validation: typing.Optional[bool] = None,
        skip_metadata_api_check: typing.Optional[bool] = None,
        sse_customer_key: typing.Optional[str] = None,
        sts_endpoint: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        workspace_key_prefix: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param bucket: 
        :param key: 
        :param access_key: 
        :param acl: 
        :param assume_role_policy: 
        :param dynamodb_endpoint: 
        :param dynamodb_table: 
        :param encrypt: 
        :param endpoint: 
        :param external_id: 
        :param force_path_style: 
        :param iam_endpoint: 
        :param kms_key_id: 
        :param max_retries: 
        :param profile: 
        :param region: 
        :param role_arn: 
        :param secret_key: 
        :param session_name: 
        :param shared_credentials_file: 
        :param skip_credentials_validation: 
        :param skip_metadata_api_check: 
        :param sse_customer_key: 
        :param sts_endpoint: 
        :param token: 
        :param workspace_key_prefix: 

        stability
        :stability: experimental
        """
        props = S3BackendProps(
            bucket=bucket,
            key=key,
            access_key=access_key,
            acl=acl,
            assume_role_policy=assume_role_policy,
            dynamodb_endpoint=dynamodb_endpoint,
            dynamodb_table=dynamodb_table,
            encrypt=encrypt,
            endpoint=endpoint,
            external_id=external_id,
            force_path_style=force_path_style,
            iam_endpoint=iam_endpoint,
            kms_key_id=kms_key_id,
            max_retries=max_retries,
            profile=profile,
            region=region,
            role_arn=role_arn,
            secret_key=secret_key,
            session_name=session_name,
            shared_credentials_file=shared_credentials_file,
            skip_credentials_validation=skip_credentials_validation,
            skip_metadata_api_check=skip_metadata_api_check,
            sse_customer_key=sse_customer_key,
            sts_endpoint=sts_endpoint,
            token=token,
            workspace_key_prefix=workspace_key_prefix,
        )

        jsii.create(S3Backend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


class SwiftBackend(
    TerraformBackend, metaclass=jsii.JSIIMeta, jsii_type="cdktf.SwiftBackend"
):
    """
    stability
    :stability: experimental
    """

    def __init__(
        self,
        scope: constructs.Construct,
        *,
        container: str,
        application_credential_id: typing.Optional[str] = None,
        application_credential_name: typing.Optional[str] = None,
        application_credential_secret: typing.Optional[str] = None,
        archive_container: typing.Optional[str] = None,
        auth_url: typing.Optional[str] = None,
        cacert_file: typing.Optional[str] = None,
        cert: typing.Optional[str] = None,
        cloud: typing.Optional[str] = None,
        default_domain: typing.Optional[str] = None,
        domain_id: typing.Optional[str] = None,
        domain_name: typing.Optional[str] = None,
        expire_after: typing.Optional[str] = None,
        insecure: typing.Optional[bool] = None,
        key: typing.Optional[str] = None,
        password: typing.Optional[str] = None,
        project_domain_id: typing.Optional[str] = None,
        project_domain_name: typing.Optional[str] = None,
        region_name: typing.Optional[str] = None,
        state_name: typing.Optional[str] = None,
        tenant_id: typing.Optional[str] = None,
        tenant_name: typing.Optional[str] = None,
        token: typing.Optional[str] = None,
        user_domain_id: typing.Optional[str] = None,
        user_domain_name: typing.Optional[str] = None,
        user_id: typing.Optional[str] = None,
        user_name: typing.Optional[str] = None,
    ) -> None:
        """
        :param scope: -
        :param container: 
        :param application_credential_id: 
        :param application_credential_name: 
        :param application_credential_secret: 
        :param archive_container: 
        :param auth_url: 
        :param cacert_file: 
        :param cert: 
        :param cloud: 
        :param default_domain: 
        :param domain_id: 
        :param domain_name: 
        :param expire_after: 
        :param insecure: 
        :param key: 
        :param password: 
        :param project_domain_id: 
        :param project_domain_name: 
        :param region_name: 
        :param state_name: 
        :param tenant_id: 
        :param tenant_name: 
        :param token: 
        :param user_domain_id: 
        :param user_domain_name: 
        :param user_id: 
        :param user_name: 

        stability
        :stability: experimental
        """
        props = SwiftBackendProps(
            container=container,
            application_credential_id=application_credential_id,
            application_credential_name=application_credential_name,
            application_credential_secret=application_credential_secret,
            archive_container=archive_container,
            auth_url=auth_url,
            cacert_file=cacert_file,
            cert=cert,
            cloud=cloud,
            default_domain=default_domain,
            domain_id=domain_id,
            domain_name=domain_name,
            expire_after=expire_after,
            insecure=insecure,
            key=key,
            password=password,
            project_domain_id=project_domain_id,
            project_domain_name=project_domain_name,
            region_name=region_name,
            state_name=state_name,
            tenant_id=tenant_id,
            tenant_name=tenant_name,
            token=token,
            user_domain_id=user_domain_id,
            user_domain_name=user_domain_name,
            user_id=user_id,
            user_name=user_name,
        )

        jsii.create(SwiftBackend, self, [scope, props])

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[str, typing.Any]:
        """
        stability
        :stability: experimental
        """
        return jsii.invoke(self, "synthesizeAttributes", [])


__all__ = [
    "App",
    "AppOptions",
    "ArtifactoryBackend",
    "ArtifactoryBackendProps",
    "AzurermBackend",
    "AzurermBackendProps",
    "BooleanMap",
    "ComplexComputedList",
    "ConsulBackend",
    "ConsulBackendProps",
    "CosBackend",
    "CosBackendProps",
    "DataTerraformRemoteState",
    "DataTerraformRemoteStateArtifactory",
    "DataTerraformRemoteStateArtifactoryConfig",
    "DataTerraformRemoteStateAzurerm",
    "DataTerraformRemoteStateAzurermConfig",
    "DataTerraformRemoteStateConfig",
    "DataTerraformRemoteStateConsul",
    "DataTerraformRemoteStateConsulConfig",
    "DataTerraformRemoteStateCos",
    "DataTerraformRemoteStateCosConfig",
    "DataTerraformRemoteStateEtcd",
    "DataTerraformRemoteStateEtcdConfig",
    "DataTerraformRemoteStateEtcdV3",
    "DataTerraformRemoteStateEtcdV3Config",
    "DataTerraformRemoteStateGcs",
    "DataTerraformRemoteStateGcsConfig",
    "DataTerraformRemoteStateHttp",
    "DataTerraformRemoteStateHttpConfig",
    "DataTerraformRemoteStateLocal",
    "DataTerraformRemoteStateLocalConfig",
    "DataTerraformRemoteStateManta",
    "DataTerraformRemoteStateMantaConfig",
    "DataTerraformRemoteStateOss",
    "DataTerraformRemoteStateOssConfig",
    "DataTerraformRemoteStatePg",
    "DataTerraformRemoteStatePgConfig",
    "DataTerraformRemoteStateRemoteConfig",
    "DataTerraformRemoteStateS3",
    "DataTerraformRemoteStateS3Config",
    "DataTerraformRemoteStateSwift",
    "DataTerraformRemoteStateSwiftConfig",
    "DefaultTokenResolver",
    "EncodingOptions",
    "EtcdBackend",
    "EtcdBackendProps",
    "EtcdV3Backend",
    "EtcdV3BackendProps",
    "GcsBackend",
    "GcsBackendProps",
    "HttpBackend",
    "HttpBackendProps",
    "IAnyProducer",
    "IFragmentConcatenator",
    "IListProducer",
    "INumberProducer",
    "IPostProcessor",
    "IRemoteWorkspace",
    "IResolvable",
    "IResolveContext",
    "IResource",
    "IStringProducer",
    "ITerraformResource",
    "ITokenMapper",
    "ITokenResolver",
    "Lazy",
    "LazyAnyValueOptions",
    "LazyListValueOptions",
    "LazyStringValueOptions",
    "LocalBackend",
    "LocalBackendProps",
    "MantaBackend",
    "MantaBackendProps",
    "NamedRemoteWorkspace",
    "NumberMap",
    "OssAssumeRole",
    "OssBackend",
    "OssBackendProps",
    "PgBackend",
    "PgBackendProps",
    "PrefixedRemoteWorkspaces",
    "RemoteBackend",
    "RemoteBackendProps",
    "ResolveOptions",
    "Resource",
    "S3Backend",
    "S3BackendProps",
    "StringConcat",
    "StringMap",
    "SwiftBackend",
    "SwiftBackendProps",
    "TerraformBackend",
    "TerraformDataSource",
    "TerraformElement",
    "TerraformElementMetadata",
    "TerraformGeneratorMetadata",
    "TerraformMetaArguments",
    "TerraformModule",
    "TerraformModuleOptions",
    "TerraformOutput",
    "TerraformOutputConfig",
    "TerraformProvider",
    "TerraformProviderConfig",
    "TerraformRemoteState",
    "TerraformResource",
    "TerraformResourceConfig",
    "TerraformResourceLifecycle",
    "TerraformStack",
    "TerraformStackMetadata",
    "Testing",
    "Token",
    "Tokenization",
    "TokenizedStringFragments",
]

publication.publish()
