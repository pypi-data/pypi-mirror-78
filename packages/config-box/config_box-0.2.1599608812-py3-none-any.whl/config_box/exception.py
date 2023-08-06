class ConfigBoxException(Exception):
    pass


class ConfigBoxCredentialsRootNotFound(ConfigBoxException):
    pass


class ConfigBoxCredentialNotFound(ConfigBoxException):
    pass


class ConfigBoxConfigurationRootNotFound(ConfigBoxException):
    pass


class ConfigBoxConfigurationItemNotFound(ConfigBoxException):
    pass