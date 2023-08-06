import unittest
import csv

from quikcsv.decorator import QuikCSV


class Test_QuikCSV(unittest.TestCase):

    def test_single_dataset_data_only(self):
        datasets = [dict(
            data=[
                ['A', 'B', 'C'],
                ['1', '2', '3']
            ]
        )]

        @QuikCSV(datasets)
        def stub(csvs):
            reader = csv.reader(csvs[0])
            output = [row for row in reader]
            self.assertEqual(datasets[0]['data'], output)
        stub()

    def test_single_dataset_with_arg(self):
        datasets = [dict(
            data=[
                ['A', 'B', 'C'],
                ['1', '2', '3']
            ],
            arg='csv_'
        )]

        @QuikCSV(datasets)
        def stub(csv_):
            reader = csv.reader(csv_)
            output = [row for row in reader]
            self.assertEqual(datasets[0]['data'], output)
        stub()

        datasets[0]['arg'] = 'second'

        @QuikCSV(datasets)
        def stub_two(first, second):
            reader = csv.reader(second)
            output = [row for row in reader]
            self.assertEqual(datasets[0]['data'], output)
        stub_two(1)
        stub_two(1, 2)

    def test_single_dataset_with_opts_copy_pattern(self):
        datasets = [dict(
            data=[['a', 'b', 'c']],
            opts=dict(
                row_pattern='copy',
                add_rows=2
            )
        )]

        @QuikCSV(datasets)
        def stub(csvs):
            expected = [
                ['a', 'b', 'c'],
                ['a', 'b', 'c'],
                ['a', 'b', 'c']
            ]
            reader = csv.reader(csvs[0])
            output = [row for row in reader]
            self.assertEqual(expected, output)
        stub()

    def test_with_opts_func_pattern_no_increment(self):
        datasets = [dict(
            data=[['a', 'b', 'c']],
            opts=dict(
                row_pattern=lambda x: [i + 'a' for i in x],
                add_rows=2
            )
        )]

        @QuikCSV(datasets)
        def stub(csvs):
            expected = [
                ['a', 'b', 'c'],
                ['aa', 'ba', 'ca'],
                ['aa', 'ba', 'ca']
            ]
            reader = csv.reader(csvs[0])
            output = [row for row in reader]
            self.assertEqual(expected, output)
        stub()

    def test_with_opts_func_pattern_with_increment(self):
        datasets = [dict(
            data=[['a', 'b', 'c']],
            opts=dict(
                row_pattern=lambda x: [i + 'a' for i in x],
                add_rows=2,
                increment=True
            )
        )]

        @QuikCSV(datasets)
        def stub(csvs):
            expected = [
                ['a', 'b', 'c'],
                ['aa', 'ba', 'ca'],
                ['aaa', 'baa', 'caa']
            ]
            reader = csv.reader(csvs[0])
            output = [row for row in reader]
            self.assertEqual(expected, output)
        stub()
