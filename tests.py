import unittest
from diff import text_diff


class PriceFormatTestCase(unittest.TestCase):
    def test_change_string(self):
        self.assertEqual(
            text_diff(
                '111\n'
                '222\n'
                '333\n'
                '444\n'
                '555',

                '111\n'
                '2222\n'
                '333\n'
                '444\n'
                '555'
            ),
            '111\n'
            '<del class="diff modified">222\n'
            '</del><ins class="diff modified">2222\n'
            '</ins>333\n'
            '444\n'
            '555'
        )

    def test_change_strings_position(self):
        self.assertEqual(
            text_diff(
                '111\n'
                '222\n'
                '333\n'
                '444\n'
                '555',

                '111\n'
                '333\n'
                '222\n'
                '444\n'
                '555'
            ),
            '111\n'
            '222\n'
            '333\n'
            '444\n'
            '555'
        )

    def test_del_string(self):
        self.assertEqual(
            text_diff(
                '111\n'
                '222\n'
                '333\n'
                '444\n'
                '555',

                '111\n'
                '222\n'
                '444\n'
                '555'
            ),
            '111\n'
            '222\n'
            '<del class="diff deleted">333\n'
            '</del>444\n'
            '555'
        )

    def test_add_string(self):
        self.assertEqual(
            text_diff(
                '111\n'
                '222\n'
                '333\n'
                '444\n'
                '555',

                '111\n'
                '222\n'
                '2233\n'
                '333\n'
                '444\n'
                '555'
            ),
            '111\n'
            '222\n'
            '<ins class="diff inserted">2233\n'
            '</ins>333\n'
            '444\n'
            '555'
        )

    def test_change_position_and_text(self):
        self.assertEqual(
            text_diff(
                '111\n'
                '222\n'
                '333\n'
                '444\n'
                '555',

                '111\n'
                '333\n'
                '223\n'
                '444\n'
                '555'
            ),
            '111\n'
            '<del class="diff modified">222\n'
            '</del><ins class="diff modified">223\n'
            '</ins>333\n'
            '444\n'
            '555'
        )

    def test_config(self):
        self.assertEqual(
            text_diff(
                '111\n'
                '222\n'
                '333\n'
                '444\n'
                '555',

                '000\n'
                '111\n'
                '223\n'
                '333\n'
                '444\n',
                {
                    "deleted_element": "span",
                    "inserted_element": "span",
                    "modified_class": "diff modified test",
                    "deleted_class": "diff deleted test",
                    "inserted_class": "diff inserted test"
                }
            ),
            '<span class="diff inserted test">000\n'
            '</span>111\n'
            '<span class="diff modified test">222\n'
            '</span><span class="diff modified test">223\n'
            '</span>333\n'
            '444\n'
            '<span class="diff deleted test">555</span>'

        )


if __name__ == '__main__':
    unittest.main()
