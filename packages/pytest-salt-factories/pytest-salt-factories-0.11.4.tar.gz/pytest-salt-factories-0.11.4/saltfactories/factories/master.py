"""
saltfactories.factories.master
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Master Factory
"""

try:
    import salt.config
    import salt.utils.files
    import salt.utils.dictupdate
except ImportError:  # pragma: no cover
    # We need salt to test salt with saltfactories, and, when pytest is rewriting modules for proper assertion
    # reporting, we still haven't had a chance to inject the salt path into sys.modules, so we'll hit this
    # import error, but its safe to pass
    pass

from saltfactories.utils import ports


class MasterFactory:
    @staticmethod
    def default_config(
        root_dir, master_id, config_defaults=None, config_overrides=None, order_masters=False,
    ):
        if config_defaults is None:
            config_defaults = {}

        conf_dir = root_dir.join("conf").ensure(dir=True)
        conf_file = conf_dir.join("master").strpath
        state_tree_root = root_dir.join("state-tree").ensure(dir=True)
        state_tree_root_base = state_tree_root.join("base").ensure(dir=True).strpath
        state_tree_root_prod = state_tree_root.join("prod").ensure(dir=True).strpath
        pillar_tree_root = root_dir.join("pillar-tree").ensure(dir=True)
        pillar_tree_root_base = pillar_tree_root.join("base").ensure(dir=True).strpath
        pillar_tree_root_prod = pillar_tree_root.join("prod").ensure(dir=True).strpath

        _config_defaults = {
            "id": master_id,
            "conf_file": conf_file,
            "root_dir": root_dir.strpath,
            "interface": "127.0.0.1",
            "publish_port": ports.get_unused_localhost_port(),
            "ret_port": ports.get_unused_localhost_port(),
            "tcp_master_pub_port": ports.get_unused_localhost_port(),
            "tcp_master_pull_port": ports.get_unused_localhost_port(),
            "tcp_master_publish_pull": ports.get_unused_localhost_port(),
            "tcp_master_workers": ports.get_unused_localhost_port(),
            "pidfile": "run/master.pid",
            "pki_dir": "pki",
            "cachedir": "cache",
            "sock_dir": "run/master",
            "fileserver_list_cache_time": 0,
            "fileserver_backend": ["roots"],
            "pillar_opts": False,
            "peer": {".*": ["test.*"]},
            "log_file": "logs/master.log",
            "log_level_logfile": "debug",
            "api_logfile": "logs/api.log",
            "key_logfile": "logs/key.log",
            "token_dir": "tokens",
            "token_file": root_dir.join("ksfjhdgiuebfgnkefvsikhfjdgvkjahcsidk").strpath,
            "file_buffer_size": 8192,
            "log_fmt_console": "%(asctime)s,%(msecs)03.0f [%(name)-17s:%(lineno)-4d][%(levelname)-8s][%(processName)18s(%(process)d)] %(message)s",
            "log_fmt_logfile": "[%(asctime)s,%(msecs)03.0f][%(name)-17s:%(lineno)-4d][%(levelname)-8s][%(processName)18s(%(process)d)] %(message)s",
            "file_roots": {"base": state_tree_root_base, "prod": state_tree_root_prod},
            "pillar_roots": {"base": pillar_tree_root_base, "prod": pillar_tree_root_prod},
            "order_masters": order_masters,
            "max_open_files": 10240,
            "pytest-master": {"log": {"prefix": "{{cli_name}}({})".format(master_id)},},
        }
        # Merge in the initial default options with the internal _config_defaults
        salt.utils.dictupdate.update(config_defaults, _config_defaults, merge_lists=True)

        if config_overrides:
            # Merge in the default options with the master_config_overrides
            salt.utils.dictupdate.update(config_defaults, config_overrides, merge_lists=True)

        return config_defaults
