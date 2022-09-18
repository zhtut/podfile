import os
from enum import Enum


class FileAction(Enum):
    addToPrefix = 0
    addToSuffix = 1
    replace = 2
    delete = 3


class FileAnchor(Enum):
    start = 1
    end = 2


class File:
    def __init__(self, path: str):
        if os.path.exists(path):
            if os.path.isfile(path):
                self.path = path
                with open(self.path, 'r') as read:
                    self.read_handler = read
            else:
                raise Exception(f"{path}不是普通文件，不能编辑")
        else:
            raise Exception(f"file不存在:{path}")

    def insert_line(self, line_str: str, anchor=FileAnchor.start):
        read = self.read_handler
        content = read.read()
        if anchor == FileAnchor.start:
            content = line_str + content
        else:
            content = content + line_str
        with open(self.path, 'w') as write:
            write.write(content)

    def delete_str(self, string: str, **kwargs):
        return self.process_str(string, action=FileAction.delete, **kwargs)

    def delete_line(self, line_str: str, **kwargs):
        return self.process_str(line_str, action=FileAction.delete, accurate=False, **kwargs)

    def add_string_to_prefix(self, string: str, search_str: str, **kwargs):
        return self.process_str(search_str=search_str, new_text=string, action=FileAction.addToPrefix, **kwargs)

    def add_string_to_suffix(self, string: str, search_str: str, **kwargs):
        return self.process_str(search_str=search_str, new_text=string, action=FileAction.addToSuffix, **kwargs)

    def add_line_to_prefix(self, string: str, search_str: str, **kwargs):
        return self.process_str(search_str=search_str, new_text=string, action=FileAction.addToPrefix, accurate=False,
                                **kwargs)

    def add_line_to_suffix(self, string: str, search_str: str, **kwargs):
        return self.process_str(search_str=search_str, new_text=string, action=FileAction.addToSuffix, accurate=False,
                                **kwargs)

    def process_str(self, search_str: str,
                    new_text: str = None,
                    accurate: bool = True,
                    action: FileAction = FileAction.addToSuffix,
                    once: bool = False) -> bool:
        """
        在文件中添加一段字符串
        :param search_str: 检索的字符串
        :param new_text: 需要添加的字符串
        :param accurate: 是否精确搜索，精确搜索会把字符串跟在字符串后面，否则跟在行后
        :param action: 做出的动作，可添加或者替换，添加可添加在前面或者后面
        :param once: 是否只操作一次
        :return: 返回是否操作成功
        """
        read = self.read_handler
        content = ""
        process = False
        for line in read:
            allow_many = not once
            once_not_process = once and not process
            if allow_many or once_not_process:
                find_index = line.find(search_str)
                if find_index != -1:
                    pre: str = None
                    suf: str = None
                    if accurate:
                        replace = line[find_index: find_index + len(search_str)]
                        pre = line[:find_index]
                        suf = line[find_index + len(search_str):]
                    else:
                        replace = line
                    new_line = ""
                    if pre:
                        new_line += pre
                    if action == FileAction.addToSuffix:
                        replace = replace + new_text
                    elif action == FileAction.addToPrefix:
                        replace = new_text + replace
                    elif action == FileAction.replace:
                        replace = new_text
                    elif action == FileAction.delete:
                        replace = ""

                    new_line += replace

                    if suf:
                        new_line += suf

                    line = new_line
                    process = True

            if content == "":
                content = line
            else:
                content += line

        if content != "":
            with open(self.path, 'w') as write:
                write.write(content)
            return True
        else:
            print("写入文件出现问题，没有生成content")
            return False
