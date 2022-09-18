import os.path
from common.file import *
from common.module import Module
from yaml_podfile.yaml_podfile import YamlPodfile
from yaml_podfile.yaml_target import YamlTarget


class Podfile:
    podfile_path: str = None
    yaml_podfile: YamlPodfile = None

    def __init__(self, podfile_path: str):
        self.podfile_path = podfile_path
        if podfile_path is None:
            raise Exception("podfile变量为空")
        if not os.path.exists(podfile_path):
            raise Exception(f"podfile不存在：{podfile_path}")

        yaml_podfile = YamlPodfile(podfile_path)
        self.yaml_podfile = yaml_podfile

    def add_source(self, source: str):
        file = File(self.podfile_path)
        source_text = f"source '{source}'"
        if file.read_handler.read().find("source") != -1:
            file.add_text(source_text, search="source ")
        else:
            file.insert_line(source_text)

    def remove_source(self, source: str):
        file = File(self.podfile_path)
        file.delete_line_with_text(source)

    def add_module_for_target(self, module: Module, target_name: str):
        pod_str = module.pod_str
        target = self.yaml_podfile.target_with_name(target_name)
        contain = False
        for dep in target.dependencies:
            if dep.name == module.name:
                contain = True
                break
        file = File(self.podfile_path)
        if contain:
            file.process_str(module.name, pod_str, False, FileAction.replace)
        else:
            file.add_line_to_suffix(pod_str, f"target '{target_name}'")
