import json
import os.path
import subprocess
import yaml
from podfile import target


class Podfile:
    def __init__(self, podfile_path: str):
        self.targets = None
        self.podfile_path = podfile_path

        podfile_json = subprocess.getoutput(f"pod ipc podfile-json {podfile_path}")
        print(f"podfile_json:{podfile_json}")
        podfile_info = json.loads(podfile_json)
        self.podfile_info = podfile_info

        self.targets = []
        target_definitions: list = self.podfile_info.get("target_definitions")
        for target_definition in target_definitions:
            name = target_definition.get("name")
            if name == "Pods":
                children: list = target_definition.get("children")
                for child in children:
                    self.targets.append(target.Target(child))

        sources: list = self.podfile_info.get("sources")
        self.sources = sources
        if not self.sources:
            self.sources = []

    def target_with_name(self, name: str):
        for tar in self.targets:
            if tar.name == name:
                return tar
        return None

    def to_hash(self):
        target_infos = []
        for tar in self.targets:
            target_infos.append(tar.to_hash())
        podfile_info = {"sources": self.sources, "target_definitions": [{
            "name": "Pods",
            "abstract": True,
            "children": target_infos
        }]
                        }
        return podfile_info

    def dump_yaml(self):
        project_root = self.podfile_path[:self.podfile_path.rfind("/")]
        file_name = "CocoaPods.sources.yaml"
        yaml_file_path = os.path.join(project_root, file_name)
        content = self.to_hash()
        print(f"即将写入文件：{content}")
        yaml_str = yaml.dump(content)
        print(f"yaml内容：{yaml_str}")
        with open(yaml_file_path, "w") as file:
            file.write(yaml_str)
        return yaml_file_path

    def remove_original(self):
        os.remove(self.podfile_path)

    def add_source(self, source: str):
        self.sources.append(source)

    def remove_source(self, source: str):
        if source in self.sources:
            self.sources.remove(source)
