import unittest

from quikcsv import options as opts


class Test_Copy_Rows(unittest.TestCase):

    def test_valid_input(self):
        data = [
            ['a', 'b', 'c'],
            ['d', 'e', 'f']
        ]
        expected = [
            ['a', 'b', 'c'],
            ['d', 'e', 'f'],
            ['d', 'e', 'f'],
            ['d', 'e', 'f']
        ]
        output = opts._copy_rows(data, 2, 1)
        self.assertEqual(output, expected)

    def test_bad_base_index(self):
        data = [['a', 'b', 'c']]
        with self.assertRaises(IndexError):
            opts._copy_rows(data, 1, 2)


class Test_Apply_Func(unittest.TestCase):

    def test_valid_input_no_increment(self):
        data = [['a', 'b', 'c']]
        expected = [
            ['a', 'b', 'c'],
            ['aa', 'ba', 'ca'],
            ['aa', 'ba', 'ca'],
        ]
        output = opts._apply_func(
            data,
            lambda x: [i + 'a' for i in x],
            2
        )
        self.assertEqual(expected, output)

    def test_valid_input_with_increment(self):
        data = [['a', 'b', 'c']]
        expected = [
            ['a', 'b', 'c'],
            ['aa', 'ba', 'ca'],
            ['aaa', 'baa', 'caa']
        ]

        output = opts._apply_func(
            data=data,
            func=lambda x: [i + 'a' for i in x],
            num_rows=2,
            increment=True
        )
        self.assertEqual(expected, output)


class Test_Apply_Options(unittest.TestCase):

    def test_with_copy_pattern(self):
        data = [['a', 'b', 'c']]
        expected = [
            ['a', 'b', 'c'],
            ['a', 'b', 'c'],
            ['a', 'b', 'c']
        ]
        output = opts.apply_options(
            data,
            opts=dict(
                add_rows=2,
                row_pattern='copy'
            )
        )
        self.assertEqual(expected, output)

    def test_with_custom_func_pattern(self):
        data = [['a', 'b', 'c']]
        expected = [
            ['a', 'b', 'c'],
            ['aa', 'ba', 'ca'],
            ['aa', 'ba', 'ca']
        ]
        output = opts.apply_options(
            data,
            opts=dict(
                add_rows=2,
                row_pattern=lambda x: [i + 'a' for i in x]
            )
        )
        self.assertEqual(expected, output)

    def test_with_custom_func_pattern_and_increment(self):
        data = [['a', 'b', 'c']]
        expected = [
            ['a', 'b', 'c'],
            ['aa', 'ba', 'ca'],
            ['aaa', 'baa', 'caa']
        ]
        output = opts.apply_options(
            data,
            opts=dict(
                add_rows=2,
                row_pattern=lambda x: [i + 'a' for i in x],
                increment=True
            )
        )
        self.assertEqual(expected, output)
