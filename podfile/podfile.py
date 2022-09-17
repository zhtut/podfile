from podfile.yaml_target import YamlTarget
from podfile.module import Module


class Podfile:
    targets = list(YamlTarget)

    def __init__(self, podfile_path: str):
        self.podfile_path = podfile_path
        if podfile_path is None:
            return

    def add_source(self, source: str):
        self.sources.append(source)

    def remove_source(self, source: str):
        if source in self.sources:
            self.sources.remove(source)

    def target_with_name(self, name: str) -> YamlTarget:
        for target in self.targets:
            if target.name == name:
                return target
        return None

    def add_module(self, mod: Module):
        self.dependencies.append(mod)

    def remove_module(self, mod: Module):
        self.dependencies.remove(mod)

    def module_with_name(self, name: str) -> Module:
        for mo in self.dependencies:
            if mo.name == name:
                return mo
        return None
