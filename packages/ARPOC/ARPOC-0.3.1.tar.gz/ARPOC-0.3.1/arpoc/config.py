""" Configuration Module of ARPOC

After importing this file you have access to
the configuration with the `config.cfg` variable.
"""

import inspect
import logging
import os
from dataclasses import InitVar, asdict, dataclass, field, replace
from typing import Any, Dict, List, Optional

import yaml

from arpoc.exceptions import ConfigError

LOGGING = logging.getLogger()


@dataclass
class ProviderConfig:
    """
    Configuration for a single Open ID Connect Provider

    Attributes:
      -  **human_readable_name**: A name which arpoc uses when communicating 
            with the user / operator
      -  **configuration_url**: The base url of the OIDC provider. Without the 
            .well-known/ part
      -  **configuration_token**: The token ARPOC can use to register itself with 
            the OIDC provider
      -  **registration_token**: The token issued from the OIDC provider for a 
            specific client to obtain its configuration
      -  **registration_url**: The url where arpoc can obtain its configuration
            after registration.
      -  **method**: Either 'auto', 'GET', or 'POST'. The HTTP method ARPOC will
            use if the OIDC / OAuth standard gives a choice.
      -  **special_claim2scope**: A mapping from claim to scopes that will deliver
            the claims.

        **Mandatory arguments**:
          - configuration_url

          And either:
            - configuration_token
          Or:
            - registration_token
            - registration_url
    """

    baseuri: InitVar[str]
    """ arpoc's base uri

    :meta private: 
    """
    human_readable_name: str
    configuration_url: str = ""
    configuration_token: str = ""
    registration_token: str = ""
    registration_url: str = ""
    method: str = "auto"
    special_claim2scope: InitVar[dict] = None
    claim2scope: dict = field(init=False)
    redirect_paths: List[str] = field(default_factory=list)
    do_token_introspection: bool = True

    def __post_init__(self, baseuri: str, special_claim2scope: Dict) -> None:
        self.claim2scope = {
            "name": ['profile'],
            "family_name": ['profile'],
            "given_name": ['profile'],
            "middle_name": ['profile'],
            "nickname": ['profile'],
            "preferred_username": ['profile'],
            "profile": ['profile'],
            "picture": ['profile'],
            "website": ['profile'],
            "gender": ['profile'],
            "birthdate": ['profile'],
            "zoneinfo": ['profile'],
            "locale": ['profile'],
            "updated_at": ['profile'],
            "email": ["email"],
            "email_verified": ["email"],
            "address": ["address"],
            "phone": ["phone"],
            "phone_number_verified": ["phone"]
        }
        if special_claim2scope:
            for key, val in special_claim2scope.items():
                self.claim2scope[key] = val

        self.redirect_uris = []
        for redirect_path in self.redirect_paths:
            self.redirect_uris.append("{}{}".format(baseuri, redirect_path))

    def check_method(self):
        if self.method not in ["auto", "POST", "GET"]:
            raise ConfigError(f"Method of Provider {self.human_readable_name} is not valid; must be auto, POST or GET")

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)


def default_redirect() -> List:
    """ Default Redirect Path"""
    return ["/secure/redirect_uris"]


def default_json_dir() -> List:
    """ Default json path for access control entities """
    return ["/etc/arpoc/acl"]


#pylint: disable=too-many-instance-attributes
@dataclass
class ProxyConfig:
    """
    Configuration for the Proxy Setup

    Attributes:
      -  **keyfile**: The path to the private key file of the TLS keypair
      -  **certfile**: The path to the certificate chain file (full chain)
      -  **domainname**: The domain name where ARPOC will be available
      -  **contacts**: A list of mail contact adresses responsible for the ARPOC 
            instance

        Mandatory: **keyfile**, **certfile**, **domainname**, **contacts**
    """
    keyfile: str
    certfile: str
    domainname: str
    contacts: List[str]
    address: str = "0.0.0.0"
    tls_port: int = 443
    plain_port: int = 80
    https_only: bool = True
    username: str = "www-data"
    groupname: str = "www-data"
    secrets: str = "/var/lib/arpoc/secrets.yml"
    tls_redirect: str = "/TLSRedirect"
    auth: str = "/auth"
    redirect: List[str] = field(default_factory=default_redirect)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def __post_init__(self) -> None:
        assert isinstance(self.redirect, List)
        self.baseuri = "https://{}/".format(self.domainname)
        self.redirect_uris = []
        for redirect_path in self.redirect:
            # skip first slash if redirect_path has one
            rp = redirect_path[1:] if redirect_path.startswith('/') else redirect_path
            self.redirect_uris.append(f"{self.baseuri}{rp}")


@dataclass
class ServiceConfig:
    """
    Configuration for a single proxied Service

    Attributes:
      -  **origin_URL**: The URL that will be proxied, or the special page string; see :ref:`Special Pages <specialpagessection>`
      -  **proxy_URL**: The *path* under which *origin_URL* will be available.
      -  **AC**: The policy set which is evaluated to decide the access request
      -  **objectsetters**: Configuration for the objectsetters
      -  **obligations**: Configuration for obligations
      -  **authentication** Authentication information which will be used to request *origin_URL*

    Mandatory Arguments:
      - *origin_URL*
      - *proxy_URL*
      - *AC*
    """
    origin_URL: str
    proxy_URL: str
    AC: str
    objectsetters: dict = field(default_factory=dict)
    obligations: dict = field(default_factory=dict)
    authentication: dict = field(default_factory=dict)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)


@dataclass
class ACConfig:
    """ Configuration for the access control

    Attributes:
      - **json_dir**: The directory where the AC Entities are stored. The files
                    must end with ".json"
    """
    json_dir: List[str] = field(default_factory=default_json_dir)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)


@dataclass
class Misc:
    """ Misc Config Class 

    Attributes:
      -  **access_log**: The location to store the access log (HTTP requests)
      -  **error_log**: The location to store the error_log
      -  **daemonize**: If arpoc should start daemonized.
      -  **log_level**: ARPOC's log level. (DEBUG/INFO/ERROR/WARN). Affects also underlying libraries
      -  **pid_file**: Where ARPOC should store the process id file. Only used when daemonized.
      -  **plugin_dirs**: Where ARPOC should load plugins

    No mandatory arguments.
    """
    pid_file: str = "/var/run/arpoc.pid"
    daemonize: bool = True
    log_level: str = "INFO"
    access_log: str = "/var/log/arpoc/access.log"
    error_log: str = "/var/log/arpoc/error.log"
    plugin_dirs: List[str] = field(default_factory=list)

class OIDCProxyConfig:
    """ Config Container Which for all specific configuration """
    def __init__(self,
                 config_file: Optional[str] = None,
                 std_config: Optional[str] = '/etc/arpoc/config.yml'):

        self.openid_providers: Dict[str, ProviderConfig] = {}
        self.proxy: ProxyConfig = ProxyConfig("", "", "", [""])
        self.services: Dict[str, ServiceConfig] = {}
        self.access_control = ACConfig()
        self.misc: Misc = Misc()

        default_paths = [std_config]
        if 'OIDC_PROXY_CONFIG' in os.environ:
            default_paths.append(os.environ['OIDC_PROXY_CONFIG'])

        if config_file:
            default_paths.append(config_file)

        for filepath in default_paths:
            if filepath:
                try:
                    self.read_file(filepath)
                except IOError:
                    pass
        self.check_config()

    def add_provider(self, name: str, prov_cfg: ProviderConfig) -> None:
        """ Adds the provider with key <name> to the configuration """
        self.openid_providers[name] = prov_cfg

    def check_redirect_uri(self) -> None:
        """ Checks if every redirect uri in the provider config is also in the proxy list """
        for _, provider_obj in self.openid_providers.items():
            for redirect_url in provider_obj.redirect_uris:
                if redirect_url not in self.proxy.redirect:
                    raise ConfigError(f"{provider_obj.human_readable_name} has an invalid redirect_path")

    def check_config_proxy_url(self) -> None:
        """ Checks for duplicates in the proxy_url """
        proxy_urls: List[str] = []
        for key, service in self.services.items():
            if service.proxy_URL in proxy_urls:
                raise ConfigError("Bound different services to the same URL")
            proxy_urls.append(service.proxy_URL)

        assert self.proxy is not None

    def check_config(self) -> None:
        """ Make consistency checks for the arpoc config """
        LOGGING.debug("checking config consistency")
        for provider in self.openid_providers.values():
            attrs = (getattr(provider, name) for name in dir(provider) if name.startswith("check_"))
            methods = filter(inspect.ismethod, attrs)
            for method in methods:
                method()

        attrs = (getattr(self, name) for name in dir(self) if name.startswith("check_") and name != "check_config")
        methods = filter(inspect.ismethod, attrs)
        for method in methods:
            method()

    def merge_config(self, new_cfg: Dict) -> None:
        """Merges the current configuration with  a new configuration dict  """
        if 'proxy' in new_cfg:
            if self.proxy:
                self.proxy = replace(self.proxy, **new_cfg['proxy'])
            else:
                self.proxy = ProxyConfig(**new_cfg['proxy'])

        if 'services' in new_cfg:
            for key, val in new_cfg['services'].items():
                service_cfg = ServiceConfig(**val)
                self.services[key] = service_cfg
        if 'openid_providers' in new_cfg:
            for key, val in new_cfg['openid_providers'].items():
                provider_cfg = ProviderConfig(self.proxy.baseuri, **val)
                self.openid_providers[key] = provider_cfg
        if 'access_control' in new_cfg:
            self.access_control = ACConfig(**new_cfg['access_control'])

        if 'misc' in new_cfg:
            if self.misc:
                self.misc = replace(self.misc, **new_cfg['misc'])
            else:
                self.misc = Misc(**new_cfg['misc'])

    def read_file(self, filepath: str) -> None:
        """ Read the YAML file <filepath> and add the contents to the current configuration """
        with open(filepath, 'r') as ymlfile:
            new_cfg = yaml.safe_load(ymlfile)

        self.merge_config(new_cfg)

    def print_config(self) -> None:
        """ Print the current config """
        cfg: Dict[str, Dict] = dict()
        cfg['services'] = dict()
        cfg['openid_providers'] = dict()

        for services_key, services_obj in self.services.items():
            cfg['services'][services_key] = asdict(services_obj)
        for providers_key, providers_obj in self.openid_providers.items():
            cfg['openid_providers'][providers_key] = asdict(providers_obj)
        cfg['proxy'] = asdict(self.proxy)
        cfg['access_control'] = asdict(self.access_control)
        print(yaml.dump(cfg, sort_keys=False))

    @staticmethod
    def print_sample_config() -> None:
        """ Prints a sample config """
        provider = ProviderConfig("", "", "", "", "", "")
        proxy = ProxyConfig("", "", "", [""], "")
        service = ServiceConfig("", "", "", {}, {})
        ac_config = ACConfig()
        misc = Misc()

        # delete the default values of claim2scope
        provider_dict = asdict(provider)
        del provider_dict['claim2scope']
        del provider_dict['do_token_introspection']

        cfg = {
            "openid_providers": {
                "example": provider_dict
            },
            "proxy": asdict(proxy),
            "services": {
                "example": asdict(service)
            },
            "access_control": asdict(ac_config),
            "misc": asdict(misc)
        }
        print(yaml.dump(cfg, sort_keys=False))


cfg: Optional[OIDCProxyConfig] = None

if __name__ == "__main__":
    cfg = OIDCProxyConfig()
    cfg.print_sample_config()
