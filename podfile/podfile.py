import json
import os.path
import subprocess
import yaml
from podfile.install import InstallationMethod
from podfile.definition import TargetDefinition


class Podfile:
    def __init__(self, podfile_path: str):
        self.installation_method = InstallationMethod()
        self.target_definitions = []
        self.sources = []

        self.podfile_path = podfile_path

        podfile_json = subprocess.getoutput(f"pod ipc podfile-json {podfile_path}")
        print(f"podfile_json:{podfile_json}")
        podfile_info = json.loads(podfile_json)
        self.podfile_info = podfile_info

        target_definitions: list = self.podfile_info.get("target_definitions")
        self.target_definitions = [TargetDefinition(info) for info in target_definitions]

        self.sources = self.podfile_info.get("sources")

        # 解析install的方法
        installation_method: dict = self.podfile_info.get("installation_method")
        if installation_method:
            self.installation_method = InstallationMethod(installation_method)

    def target_with_name(self, name: str):
        for target_definition in self.target_definitions:
            for target in target_definition.children:
                if target.name == name:
                    return target
        return None

    def to_hash(self):
        podfile_info = {}
        if self.sources:
            podfile_info["sources"] = self.sources
        target_definitions = [definition.to_hash() for definition in self.target_definitions]
        podfile_info["target_definitions"] = target_definitions
        if self.installation_method:
            install_method_hash = self.installation_method.to_hash()
            if install_method_hash:
                podfile_info["installation_method"] = install_method_hash

        return podfile_info

    def dump_yaml(self):
        project_root = self.podfile_path[:self.podfile_path.rfind("/")]
        file_name = "CocoaPods.podfile.yaml"
        yaml_file_path = os.path.join(project_root, file_name)
        content = self.to_hash()
        print(f"即将写入文件：{content}")
        with open(yaml_file_path, "w") as file:
            yaml.dump(content, file, explicit_start=True)
        return yaml_file_path

    def remove_original(self):
        os.remove(self.podfile_path)

    def add_source(self, source: str):
        self.sources.append(source)

    def remove_source(self, source: str):
        if source in self.sources:
            self.sources.remove(source)
