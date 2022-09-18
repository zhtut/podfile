import json
import os.path
import subprocess
import yaml
from yaml_podfile.install import InstallationMethod
from yaml_podfile.definition import TargetDefinition
from yaml_podfile.yaml_target import YamlTarget


class YamlPodfile:
    """
    找到Podfile，编辑后生成yaml类型的Podfile，名称为CocoaPods.podfile.yaml，转成这个文件后，pod install会优先使用这个文件，
    但是yaml格式目前功能不全，pod ipc 转为yaml后，自定义插件的方法会丢失，post_install的方法也会丢失
    """

    def __init__(self, podfile_path: str):
        if podfile_path is None:
            raise Exception("podfile变量为空")
        if not os.path.exists(podfile_path):
            raise Exception(f"podfile不存在：{podfile_path}")

        self.podfile_path = podfile_path
        self.installation_method = InstallationMethod()
        self.target_definitions = []
        self.sources = []
        self.plugins = {}

        podfile_json = subprocess.getoutput(f"pod ipc podfile-json {podfile_path}")
        print(f"podfile_json:{podfile_json}")
        podfile_info = json.loads(podfile_json)
        self.podfile_info = podfile_info

        target_definitions: list = self.podfile_info.get("target_definitions")
        self.target_definitions = [TargetDefinition(info) for info in target_definitions]

        self.sources: list = self.podfile_info.get("sources")

        self.plugins: dict = self.podfile_info.get("plugins")

        # 解析install的方法
        installation_method: dict = self.podfile_info.get("installation_method")
        if installation_method:
            self.installation_method = InstallationMethod(installation_method)

    def target_with_name(self, name: str) -> YamlTarget:
        for target_definition in self.target_definitions:
            for target in target_definition.children:
                if target.name == name:
                    return target
        return None

    def to_hash(self) -> dict:
        podfile_info = {}
        if len(self.sources) > 0:
            podfile_info["sources"] = self.sources
        if len(self.plugins) > 0:
            podfile_info["plugins"] = self.plugins

        target_definitions = [definition.to_hash() for definition in self.target_definitions]
        podfile_info["target_definitions"] = target_definitions
        if self.installation_method:
            install_method_hash = self.installation_method.to_hash()
            if install_method_hash:
                podfile_info["installation_method"] = install_method_hash

        return podfile_info

    def dump_yaml(self) -> str:
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
