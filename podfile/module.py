from podfile import util


class Module:
    use_modular_header: bool = False
    name: str = None
    tag: str = None
    git: str = None
    branch: str = None
    path: str = None

    def __init__(self, module_info: dict = None):
        if module_info:
            if isinstance(module_info, dict):
                for key in module_info:
                    self.name = key
                    arr: list = module_info.get(key)
                    if len(arr) > 0:
                        first = arr[0]
                        if isinstance(first, str):
                            self.tag: str = first
                        elif isinstance(first, dict):
                            self.git: str = first.get("git")
                            self.branch: str = first.get("branch")
                            self.tag: str = first.get("tag")
                            self.path: str = first.get("path")
            elif isinstance(module_info, str):
                self.name = module_info

    def to_hash(self):
        module_info = {}
        if self.git:
            module_info["git"] = self.git
            if self.branch:
                module_info["branch"] = self.branch
            elif self.tag:
                module_info["tag"] = self.tag
        elif self.path:
            module_info["path"] = self.path
        elif self.tag:
            module_info = self.tag

        module_info = util.process_pod_keys(module_info)
        hash_info = {self.name: [module_info]}
        return hash_info

    @property
    def pod_str(self):
        pod_str = f"  pod '{self.name}'"
        if self.git:
            pod_str += f", :git => '{self.git}'"
            if self.tag:
                pod_str += f", :tag => '{self.tag}'"
            elif self.branch:
                pod_str += f", :branch => '{self.branch}'"
        elif self.path:
            pod_str += f", :path => '{self.path}'"
        elif self.tag:
            pod_str += f", '{self.tag}'"

        return pod_str
