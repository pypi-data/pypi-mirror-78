"""
saltfactories.hookspec
~~~~~~~~~~~~~~~~~~~~~~

Salt Factories Hooks
"""
import pytest


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_minion_configuration_defaults(
    request, factories_manager, root_dir, minion_id, master_port
):
    """
    Hook which should return a dictionary tailored for the provided minion_id

    Stops at the first non None result
    """


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_minion_configuration_overrides(
    request, factories_manager, root_dir, minion_id, config_defaults
):
    """
    Hook which should return a dictionary tailored for the provided minion_id.
    This dictionary will override the config_defaults dictionary.

    Stops at the first non None result
    """


def pytest_saltfactories_minion_verify_configuration(request, minion_config, username):
    """
    This hook is called to vefiry the provided minion configuration
    """


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_minion_write_configuration(request, minion_config):
    """
    This hook is called to write the provided minion configuration
    """


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_master_configuration_defaults(
    request, factories_manager, root_dir, master_id, order_masters
):
    """
    Hook which should return a dictionary tailored for the provided master_id

    Stops at the first non None result
    """


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_master_configuration_overrides(
    request, factories_manager, root_dir, master_id, config_defaults, order_masters
):
    """
    Hook which should return a dictionary tailored for the provided master_id.
    This dictionary will override the config_defaults dictionary.

    Stops at the first non None result
    """


def pytest_saltfactories_master_verify_configuration(request, master_config, username):
    """
    This hook is called to vefiry the provided master configuration
    """


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_master_write_configuration(request, master_config):
    """
    This hook is called to write the provided master configuration
    """


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_syndic_configuration_defaults(
    request, factories_manager, root_dir, syndic_id, syndic_master_port
):
    """
    Hook which should return a dictionary tailored for the provided syndic_id with 3 keys:

    * `master`: The default config for the master running along with the syndic
    * `minion`: The default config for the master running along with the syndic
    * `syndic`: The default config for the master running along with the syndic

    Stops at the first non None result
    """


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_syndic_configuration_overrides(
    request, factories_manager, root_dir, syndic_id, config_defaults
):
    """
    Hook which should return a dictionary tailored for the provided syndic_id.
    This dictionary will override the config_defaults dictionary.

    The returned dictionary should contain 3 keys:

    * `master`: The config overrides for the master running along with the syndic
    * `minion`: The config overrides for the master running along with the syndic
    * `syndic`: The config overridess for the master running along with the syndic

    The `config_defaults` parameter be None or have 3 keys, `master`, `minion`, `syndic`,
    while will contain the default options for each of the daemons.

    Stops at the first non None result
    """


def pytest_saltfactories_syndic_verify_configuration(request, syndic_config, username):
    """
    This hook is called to vefiry the provided syndic configuration
    """


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_syndic_write_configuration(request, syndic_config):
    """
    This hook is called to write the provided syndic configuration
    """


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_proxy_minion_configuration_defaults(
    request, factories_manager, root_dir, proxy_minion_id, master_port
):
    """
    Hook which should return a dictionary tailored for the provided proxy_minion_id

    Stops at the first non None result
    """


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_proxy_minion_configuration_overrides(
    request, factories_manager, root_dir, proxy_minion_id, config_defaults
):
    """
    Hook which should return a dictionary tailored for the provided proxy_minion_id.
    This dictionary will override the config_defaults dictionary.

    Stops at the first non None result
    """


def pytest_saltfactories_proxy_minion_verify_configuration(request, proxy_minion_config, username):
    """
    This hook is called to vefiry the provided proxy_minion configuration
    """


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_proxy_minion_write_configuration(request, proxy_minion_config):
    """
    This hook is called to write the provided proxy_minion configuration
    """


@pytest.hookspec(firstresult=True)
def pytest_saltfactories_handle_key_auth_event(
    factories_manager, master_id, minion_id, keystate, payload
):
    """
    This hook is called for every auth event on the masters
    """
