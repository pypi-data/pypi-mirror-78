from .utils import Docs


class TestRegression(Docs):
    def setUp(self):
        super(TestRegression, self).setUp()
        self.base_folder = "docs"

    def test_level_1(self):
        ensure = "[configuration]\nauthor=A\ncode=C\n"
        absent = "keep me\n"
        append = "192.168.0.1 abc\n\n127.0.0.1 append"

        folder = "level-1-line-in-file"
        file_content_pairs = [
            ("ensure.txt", ensure),
            ("absent.txt", absent),
            ("append.txt", append),
        ]
        self.run_moban(["moban"], folder, file_content_pairs)
