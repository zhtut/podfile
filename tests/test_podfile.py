import os
import subprocess
from unittest import TestCase

from podfile.podfile import Podfile
from podfile.module import Module
from podfile.target import Target


class TestPodfile(TestCase):

    def test_transform(self):
        podfile_path = "PodfileExample/Podfile"
        yaml_path = "PodfileExample/CocoaPods.podfile.yaml"
        origin_yaml = "PodfileExample/origin_CocoaPods.podfile.yaml"
        if os.path.exists(yaml_path):
            os.remove(yaml_path)
        if os.path.exists(origin_yaml):
            os.remove(origin_yaml)
        command = f"pod ipc podfile {podfile_path}"
        yaml_content = subprocess.getoutput(command)
        with open(yaml_path, "w") as w:
            w.write(yaml_content)
        os.system(f'mv {yaml_path} {origin_yaml}')
        podfile_obj = Podfile(podfile_path)
        podfile_obj.dump_yaml()

    def test_add_module(self):
        podfile_path = "PodfileExample/Podfile"
        yaml_path = "PodfileExample/CocoaPods.podfile.yaml"
        if os.path.exists(yaml_path):
            os.remove(yaml_path)
        podfile_obj = Podfile(podfile_path)
        tar: Target = podfile_obj.target_with_name("PodfileExample")
        new_module = Module()
        new_module.name = "Alamofire"
        new_module.tag = "5.6.1"
        tar.add_module(new_module)
        tar.platform.ios = "13.0"
        podfile_obj.dump_yaml()
