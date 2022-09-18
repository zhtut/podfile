from common.util import *


class Hash:
    @property
    def _properties(self):
        all_pro = []
        dirs = dir(self)
        for pro in dirs:
            if pro.startswith("_"):
                continue
            if not hasattr(self, pro):
                continue
            if pro == "to_hash":
                continue

            all_pro.append(pro)
        return all_pro

    def to_hash(self):
        info = {}
        properties = self._properties
        for pro in properties:
            value = getattr(self, pro)
            if value is None:
                continue
            # 这个是方法
            if isinstance(value, str) and value.find("<bound method") != -1:
                continue

            info[pro] = getattr(self, pro)
        return info


class UsesFrameworks(Hash):
    """
    "linkage":"dynamic",
    "packaging":"framework"
    """
    linkage: str = None
    packaging: str = None

    def __init__(self, hash_info: dict = None):
        if hash_info:
            self.linkage = hash_info.get("linkage")
            self.packaging = hash_info.get("packaging")


class Platform(Hash):
    ios: str
    osx: str
    tvos: str
    watchos: str

    def __init__(self, platform_info: dict = None):
        if platform_info:
            self.ios = platform_info.get("ios")
            self.osx = platform_info.get("osx")
            self.tvos = platform_info.get("tvos")
            self.watchos = platform_info.get("watchos")


# 有一些能用的属性的类，比如inhibit_warnings，可以放在外面，也可以放到target里面
class Common:
    _uses_frameworks = UsesFrameworks()
    inhibit_warnings = False
    use_modular_headers = False
    platform = Platform()

    def parse_properties(self, info: dict):
        uses_frameworks_info = info.get("uses_frameworks")
        if uses_frameworks_info:
            self.uses_frameworks = UsesFrameworks(uses_frameworks_info)
        if info.get("inhibit_warnings"):
            self.inhibit_warnings = True
        if info.get("use_modular_headers"):
            self.use_modular_headers = True

        platform_info = info.get("platform")
        if platform_info:
            self.platform = Platform(platform_info)

    @property
    def uses_frameworks(self):
        return self._uses_frameworks

    @uses_frameworks.setter
    def uses_frameworks(self, value):
        if isinstance(value, bool):
            if value:
                default = {
                    "linkage": "dynamic",
                    "packaging": "framework"
                }
                self._uses_frameworks = UsesFrameworks(default)
            else:
                self._uses_frameworks = None
        elif isinstance(value, dict):
            self._uses_frameworks = UsesFrameworks(value)
        else:
            self._uses_frameworks = value

    def to_hash(self):
        ret_hash = {}
        if self.uses_frameworks:
            uses_frameworks_dict = self.uses_frameworks.to_hash()
            if len(uses_frameworks_dict) > 0:
                ret_hash["uses_frameworks"] = process_pod_keys(uses_frameworks_dict)
        if self.inhibit_warnings:
            ret_hash["inhibit_warnings"] = {"all": True}
        if self.use_modular_headers:
            ret_hash["use_modular_headers"] = {"all": True}
        platform_hash = self.platform.to_hash()
        if len(platform_hash) > 0:
            ret_hash["platform"] = platform_hash
        return ret_hash
