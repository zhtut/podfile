class InstallationMethod:
    clean: bool
    deduplicate_targets: bool
    deterministic_uuids: bool
    integrate_targets: bool
    lock_pod_sources: bool
    warn_for_multiple_pod_sources: bool
    warn_for_unused_master_specs_repo: bool
    share_schemes_for_development_pods: bool
    disable_input_output_paths: bool
    preserve_pod_file_structure: bool
    generate_multiple_pod_projects: bool
    incremental_installation: bool
    skip_pods_project_generation: bool

    _out_options: dict = None

    def __init__(self, install_info: dict = None):
        self.name = None
        self.options = {}
        if install_info:
            self.name = install_info.get("name")
            options: dict = install_info.get("options")
            if options:
                for (key, value) in self.options.items():
                    setattr(self, key, value)  # 则添加属性到对象中
                self.options = options

    def to_hash(self):
        hash_info = {}
        if self.name:
            hash_info["name"] = self.name

        self._out_options = {}

        self.options_value("clean")
        self.options_value("deduplicate_targets")
        self.options_value("deterministic_uuids")
        self.options_value("integrate_targets")
        self.options_value("lock_pod_sources")
        self.options_value("warn_for_multiple_pod_sources")
        self.options_value("warn_for_unused_master_specs_repo")
        self.options_value("share_schemes_for_development_pods")
        self.options_value("disable_input_output_paths")
        self.options_value("preserve_pod_file_structure")
        self.options_value("generate_multiple_pod_projects")
        self.options_value("incremental_installation")
        self.options_value("skip_pods_project_generation")

        if len(self._out_options.items()) > 0:
            hash_info["options"] = self._out_options

        self._out_options = None
        return hash_info

    def options_value(self, key: str):
        if hasattr(self, key):
            value = getattr(self, key)
            self._out_options[key] = value
