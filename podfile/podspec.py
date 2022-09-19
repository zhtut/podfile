import glob
import os
import json


# podspec的类，可以编辑各项属性，并生成新的json文件供其他地方使用，
# 编辑podspec文件不好编辑，转成json很好处理，然后生成json文件也是一样使用
class PodSpec:

    def __init__(self, path: str):
        if path is None:
            raise Exception(f"path是空的")

        if not os.path.exists(path):
            raise Exception(f"path文件不存在：{path}")

        # 原始path
        self.path = path

        if os.path.isdir(path):
            search_result = glob.glob(f"{path}/*.podspec.json")
            if search_result is not None and len(search_result) > 0:
                self.podspec_json_path = search_result[0]
            else:
                search_result = glob.glob(f"{path}/*.podspec")
                if search_result is not None and len(search_result) > 0:
                    search_podspec_path = search_result[0]
                    self.podspec_json_path = f"{search_podspec_path}.json"
                    change_json_cmd = f"pod ipc spec {search_podspec_path} >{self.podspec_json_path}"
                    os.system(change_json_cmd)
                else:
                    raise Exception("没有找到pod类型的文件")
        else:
            if path.endswith(".podspec.json"):
                self.podspec_json_path = path
            elif path.endswith(".podspec"):
                self.podspec_json_path = f"{path}.json"
                change_json_cmd = f"pod ipc spec {path} >{self.podspec_json_path}"
                os.system(change_json_cmd)
            else:
                raise Exception("没有找到pod类型的文件")

        with open(self.podspec_json_path, "r") as file_handler:
            self.podspec_json_content = json.load(file_handler)

    # 删除原始文件
    def remove_podspec(self):
        os.remove(self.path)

    # 保存到json文件
    def save(self):
        with open(self.podspec_json_path, 'w') as handler:
            json.dump(self.podspec_json_content, handler, indent=4)

    # 移除某个key
    def remove_key(self, key):
        del self.podspec_json_content[key]
        self.save()

    # 获取某个值
    def value_for_key(self, key: str):
        return self.podspec_json_content.get(key)

    # 设置某项值，如设置swift_version可使用
    # podspec_obj.set_value_for_key("5.5", "swift_version")
    def set_value_for_key(self, value, key: str):
        self.podspec_json_content[key] = value
        self.save()

    # 名称
    @property
    def name(self):
        return self.value_for_key("name")

    @name.setter
    def name(self, new_value):
        self.set_value_for_key(new_value, "name")

    # 版本
    @property
    def version(self):
        return self.value_for_key("version")

    @version.setter
    def version(self, new_value):
        self.set_value_for_key(new_value, "version")

    # 版本
    @property
    def source(self):
        return self.value_for_key("source")

    @source.setter
    def source(self, new_value):
        self.set_value_for_key(new_value, "source")

    @property
    def source_is_http(self):
        return 'http' in self.source

    @property
    def source_is_git(self):
        return 'git' in self.source

    def change_source_url(self, new_url):
        source = self.source
        if self.source_is_git:
            source["git"] = new_url
        elif self.source_is_http:
            source["http"] = new_url
        self.source = source

    def change_source_tag(self, new_tag: str):
        source = self.source
        source["tag"] = new_tag
        self.source = source

    # 版本
    @property
    def source_files(self):
        return self.value_for_key("source_files")

    @source_files.setter
    def source_files(self, new_value):
        self.set_value_for_key(new_value, "source_files")
