from podfile.common import Common
from podfile.target import Target


class TargetDefinition(Common):
    name: str = None
    abstract = True
    children: list = None

    def __init__(self, definition_info: dict = None):
        if definition_info:
            super().parse_properties(definition_info)
            self.name = definition_info.get("name")
            self.abstract = definition_info.get("abstract")
            children = definition_info.get("children")
            children_objs = []
            if children:
                for child_info in children:
                    target = Target(child_info)
                    children_objs.append(target)
            self.children = children_objs

    def to_hash(self):
        hash_info = super().to_hash()
        if self.name:
            hash_info["name"] = self.name
        hash_info["abstract"] = self.abstract
        children = []
        for tar in self.children:
            children.append(tar.to_hash())
        hash_info["children"] = children
        return hash_info
