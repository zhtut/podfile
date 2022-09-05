from unittest import TestCase
from podfile import podfile
from podfile import module
from podfile import target


class TestPodfile(TestCase):

    def test_list_targets(self):
        print(self.podfile_obj.targets)

    def test_add_module(self):
        podfile_path = "PodfileExample/Podfile"
        podfile_obj = podfile.Podfile(podfile_path)
        podfile_obj.add_source("https://github.com/CocoaPods/Specs.git")
        tar: target.Target = podfile_obj.target_with_name("PodfileExample")
        new_module = module.Module()
        new_module.name = "Alamofire"
        new_module.tag = "5.6.1"
        tar.add_module(new_module)
        yaml_path = podfile_obj.dump_yaml()
        print(f"yaml生成在{yaml_path}")
