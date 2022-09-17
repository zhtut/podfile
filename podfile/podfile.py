from podfile.target import Target
from common.module import Module
from common.file import File


class Podfile:
    podfile_path: str = None
    podfile_content: str = None
    targets = list(Target)

    def __init__(self, podfile_path: str):
        self.podfile_path = podfile_path
        if podfile_path is None:
            return

        with open(self.podfile_path, "r") as file:
            for line in file:


    def add_source(self, source: str):
        file = File(self.podfile_path)
        source_text = f"source '{source}'"
        file.add_text(source_text, search="source ")

    def remove_source(self, source: str):
        file = File(self.podfile_path)
        file.delete_line_with_text(source)

    def target_with_name(self, name: str) -> Target:
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
