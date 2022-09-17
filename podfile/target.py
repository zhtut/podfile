class Target:
    def __init__(self, podfile_path: str, name: str, content: str):
        self.podfile_path = podfile_path
        self.name = name
        self.content = content
