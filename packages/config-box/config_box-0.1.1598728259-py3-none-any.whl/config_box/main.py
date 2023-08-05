import hiyapyco

from .exception import ConfigBoxCredentialsRootNotFound, ConfigBoxCredentialNotFound, \
    ConfigBoxConfigurationRootNotFound, ConfigBoxConfigurationItemNotFound


class ConfigBox(object):
    def __init__(self, *args, **kwargs):
        self.paths = []
        for path in args:
            self.paths.append(path)
        self.config = hiyapyco.load(*args, **kwargs)

    def get_config_item(self, name: str) -> dict:
        configuration = self.config.get("configuration", None)
        if configuration is None:
            raise ConfigBoxConfigurationRootNotFound()
        config_item = next((sub for sub in configuration if sub['name'] == name), None)
        if config_item is None:
            raise ConfigBoxConfigurationItemNotFound()
        else:
            return config_item

    def get_credential(self, name: str) -> dict:
        credentials = self.config.get("credentials", None)
        if credentials is None:
            raise ConfigBoxCredentialsRootNotFound()
        credential = next((sub for sub in credentials if sub['name'] == name), None)
        if credential is None:
            raise ConfigBoxCredentialNotFound()
        else:
            return credential
