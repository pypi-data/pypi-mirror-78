import unittest

from quikcsv import validation, exceptions


class Test_Column_Length_Validation(unittest.TestCase):

    def test_even_columns_should_not_raise_error(self):
        datasets = [
            dict(
                data=[
                    ['a', 'b', 'c'],
                    ['a', 'b', 'c']
                ]
            )
        ]
        validation._check_col_length(datasets)

    def test_uneven_columns_should_raise_error(self):
        datasets = [
            dict(
                data=[
                    ['a', 'b'],
                    ['a', 'b', 'c']
                ]
            )
        ]
        with self.assertRaises(exceptions.UnevenColumnError):
            validation._check_col_length(datasets)

    def test_two_datasets(self):
        datasets = [
            dict(
                data=[
                    ['a', 'b', 'c'],
                    ['a', 'b', 'c']
                ]
            ),
            dict(
                data=[
                    ['a', 'b', 'c', 'd'],
                    ['a', 'b', 'c', 'd'],
                ]
            )
        ]
        validation._check_col_length(datasets)


class Test_Arg_Consistency(unittest.TestCase):

    def test_assigning_two_different_args_should_not_raise_error(self):
        datasets = [
            dict(
                data=[
                    ['a', 'b', 'c'],
                    ['a', 'b', 'c']
                ],
                arg='one'
            ),
            dict(
                data=[
                    ['a', 'b', 'c', 'd'],
                    ['a', 'b', 'c', 'd'],
                ],
                arg='two'
            )
        ]
        validation._check_arg_consistency(datasets)

    def test_assigning_same_arg_should_raise_error(self):
        datasets = [
            dict(
                data=[
                    ['a', 'b', 'c'],
                    ['a', 'b', 'c']
                ],
                arg='one'
            ),
            dict(
                data=[
                    ['a', 'b', 'c', 'd'],
                    ['a', 'b', 'c', 'd'],
                ],
                arg='one'
            )
        ]
        try:
            validation._check_arg_consistency(datasets)
            self.fail('ArgError not raised.')
        except exceptions.ArgError as e:
            self.assertEqual(e.message, 'arg one already assigned.')


class Test_Check_Dataset_Options(unittest.TestCase):

    def test_required_options_should_validate(self):
        datasets = [
            dict(
                data=[
                    ['a', 'b', 'c'],
                    ['a', 'b', 'c']
                ],
                opts={
                    'row_pattern': 'copy',
                    'add_rows': 2
                }
            )
        ]
        try:
            validation._check_dataset_options(datasets)
        except exceptions.OptionError:
            self.fail('Options did not validate.')

    def test_missing_required_options_should_not_validate(self):
        datasets = [
            dict(
                data=[
                    ['a', 'b', 'c'],
                    ['a', 'b', 'c']
                ],
                opts={
                    'row_pattern': 'copy'
                }
            )
        ]
        try:
            validation._check_dataset_options(datasets)
            self.fail('OptionsError wasn not raised.')
        except exceptions.OptionError as e:
            self.assertEqual(e.message, 'Options must include [\'row_pattern\', \
                                         \'add_rows\']')
        datasets = [
            dict(
                data=[
                    ['a', 'b', 'c'],
                    ['a', 'b', 'c']
                ],
                opts={
                    'add_rows': 2
                }
            )
        ]
        try:
            validation._check_dataset_options(datasets)
            self.fail('OptionsError wasn not raised.')
        except exceptions.OptionError as e:
            self.assertEqual(e.message, 'Options must include [\'row_pattern\', \
                                         \'add_rows\']')

    def test_passing_invalid_options_should_not_validate(self):
        datasets = [
            dict(
                data=[
                    ['a', 'b', 'c'],
                    ['a', 'b', 'c']
                ],
                opts={
                    'row_pattern': 'copy',
                    'add_rows': 2,
                    'invalid': 0
                }
            )
        ]
        try:
            validation._check_dataset_options(datasets)
            self.fail('OptionsError was not raised.')
        except exceptions.OptionError as e:
            self.assertEqual(e.message, 'Invalid option invalid.')

    def test_row_pattern_option_valid_checks(self):
        datasets = [
            dict(
                data=[
                    ['a', 'b', 'c'],
                    ['a', 'b', 'c']
                ],
                opts={
                    'row_pattern': 'bad_pattern',
                    'add_rows': 2,
                }
            )
        ]
        try:
            validation._check_dataset_options(datasets)
            self.fail('OptionsError was not raised.')
        except exceptions.OptionError as e:
            self.assertEqual(e.message, 'row_pattern option must be one of \
                                         [\'copy\'] or a function')
