from podfile.module import Module
from podfile.common import Common


class YamlTarget(Common):
    name: str = None
    dependencies: list() = None

    def __init__(self, target_info: dict = None):
        if not target_info:
            return
        super().parse_properties(target_info)
        self.name = target_info.get("name")
        dependencies = list()
        use_modular_headers: dict = target_info.get("use_modular_headers")
        for_pods = list()
        if use_modular_headers:
            for_pods = use_modular_headers.get("for_pods")
        for var in target_info.get("dependencies"):
            lib_info: dict = var
            mo = Module(lib_info)
            if for_pods:
                if mo.name in for_pods:
                    mo.use_modular_header = True
            dependencies.append(mo)
        self.dependencies = dependencies

    def add_module(self, mod: Module):
        self.dependencies.append(mod)

    def remove_module(self, mod: Module):
        self.dependencies.remove(mod)

    def module_with_name(self, name: str):
        for mo in self.dependencies:
            if mo.name == name:
                return mo
        return None

    def to_hash(self):
        target_info = super().to_hash()
        target_info["name"] = self.name
        dependencies = []
        for_pods = []
        for dep in self.dependencies:
            dependencies.append(dep.to_hash())
            if dep.use_modular_header:
                for_pods.append(dep.name)
        target_info["dependencies"] = dependencies
        if len(for_pods) > 0:
            target_info["use_modular_headers"] = {"for_pods": for_pods}
        return target_info
