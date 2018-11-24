import unittest
from diff import text_diff


class TextDiffTestCase(unittest.TestCase):
    def test_change_string(self):
        self.assertEqual(
            text_diff("111\n222\n333\n444\n555", "111\n2222\n333\n444\n555"),
            "111\n"
            "<del class=\"diff modified\">222\n"
            "</del><ins class=\"diff modified\">2222\n"
            "</ins>333\n"
            "444\n"
            "555"
        )

    def test_change_strings_position(self):
        self.assertEqual(
            text_diff("111\n222\n333\n444\n555", "111\n333\n222\n444\n555"),
            "111\n"
            "<ins class=\"diff inserted\">333\n"
            "</ins>222\n"
            "<del class=\"diff deleted\">333\n"
            "</del>444\n"
            "555"
        )

    def test_del_string(self):
        self.assertEqual(
            text_diff("111\n222\n333\n444\n555", "111\n222\n444\n555"),
            "111\n222\n<del class=\"diff deleted\">333\n</del>444\n555"
        )

    def test_del_string2(self):
        self.assertEqual(
            text_diff("111\n222\n333\n444\n555", "222\n112\n333\n444"),
            "<del class=\"diff deleted\">111\n"
            "</del>222\n"
            "<ins class=\"diff inserted\">112\n"
            "</ins>333\n"
            "<del class=\"diff modified\">444\n"
            "555</del><ins class=\"diff modified\">444</ins>"
        )

    def test_add_string(self):
        self.assertEqual(
            text_diff(
                "111\n"
                "222\n"
                "333\n"
                "444\n"
                "555",

                "111\n"
                "222\n"
                "2233\n"
                "333\n"
                "444\n"
                "555"
            ),
            "111\n"
            "222\n"
            "<ins class=\"diff inserted\">2233\n"
            "</ins>333\n"
            "444\n"
            "555"
        )

    def test_change_position_and_text(self):
        self.assertEqual(
            text_diff("111\n222\n333\n444\n555", "111\n333\n223\n444\n555"),
            "111\n"
            "<del class=\"diff deleted\">222\n"
            "</del>333\n"
            "<ins class=\"diff inserted\">223\n"
            "</ins>444\n"
            "555"
        )

    def test_config(self):
        config = {
            "deleted_element": "span", "inserted_element": "span",
            "modified_class": "test", "deleted_class": "test",
            "inserted_class": "test"
        }
        self.assertEqual(

            text_diff(
                "111\n222\n333\n444\n555",
                "000\n111\n223\n333\n444\n",
                config
            ),
            "<span class=\"test\">000\n"
            "</span>111\n"
            "<span class=\"test\">222\n"
            "</span><span class=\"test\">223\n"
            "</span>333\n"
            "444\n"
            "<span class=\"test\">555</span>"
        )


if __name__ == "__main__":
    unittest.main()
