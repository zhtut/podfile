import unittest
from podfile.file import File


class MyTestCase(unittest.TestCase):
    @property
    def file_path(self):
        return "text.txt"

    def reset_file(self):
        file_content = "123\n456\n789\n012"
        with open(self.file_path, "w") as file:
            file.write(file_content)

    @property
    def file_content(self):
        with open(self.file_path, 'r') as read:
            return read.read()

    def test_file(self):
        self.reset_file()
        file = File(self.file_path)
        file.delete_str("12")
        print(self.file_content)
        self.assertEquals(self.file_content, "3\n456\n789\n0")

        self.reset_file()
        file.delete_line("12")
        print(self.file_content)
        self.assertEquals(self.file_content, "456\n789\n")

        self.reset_file()
        file.delete_line("12", once=True)
        print(self.file_content)
        self.assertEquals(self.file_content, "456\n789\n012")

        self.reset_file()
        file.delete_line("789")
        print(self.file_content)
        self.assertEquals(self.file_content, "123\n456\n012")

        self.reset_file()
        file.add_string_to_prefix("aaa", "8")
        print(self.file_content)
        self.assertEquals(self.file_content, "123\n456\n7aaa89\n012")

        self.reset_file()
        file.add_string_to_suffix("aaa", "8")
        print(self.file_content)
        self.assertEquals(self.file_content, "123\n456\n78aaa9\n012")


if __name__ == '__main__':
    unittest.main()
