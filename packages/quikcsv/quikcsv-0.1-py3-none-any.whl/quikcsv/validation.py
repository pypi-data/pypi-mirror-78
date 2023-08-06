"""Handlers for ensuring the mock data passed will work."""
import types

from .exceptions import UnevenColumnError, ArgError, OptionError


def _check_col_length(datasets):
    """
    Ensures the length of all data columns are equal within each
    dataset.

    Parameters
    ----------
    datasets: dict[]
        List of datasets to validate.

    Raises
    ------
    UnevenColumnError
        If the columns do not equal each other.
    """
    for dataset in datasets:
        data = dataset['data']
        col_length = len(data[0])
        for row in data:
            if len(row) != col_length:
                raise UnevenColumnError(data)


def _check_arg_consistency(datasets):
    """
    Ensures if arg is specified on one dataset, it is specified on all
    datasets. Also checks that the same arg is not reused for multiple
    csv assignments.

    Parameters
    ----------
    datasets: dict[]
        List of dicts containing the datasets.

    Raises
    ------
    ArgError
        If arg is specified on one dataset and not all others.
    """
    specified = False
    assigned_args = []
    for dataset in datasets:
        if dataset.get('arg'):
            if dataset['arg'] in assigned_args:
                raise ArgError(f'arg {dataset["arg"]} already assigned.')
            assigned_args.append(dataset['arg'])
            specified = True
        if specified and not dataset.get('arg'):
            raise ArgError


def _check_dataset_options(datasets):
    """
    Ensures that for each dataset, if options are provided that they
    are valid.

    Parameters
    ----------
    datasets: dict[]
        List of dicts containing the datasets.

    Raises
    ------
    OptionError
        If options do not meet the requirements.
    """
    for dataset in datasets:
        if not dataset.get('opts'):
            continue

        valid_options = [
            'row_pattern',
            'add_rows',
            'base_row_index',
            'increment'
        ]
        if not all(val in list(dataset['opts'].keys()) for val in valid_options[:2]):  # noqa
            raise OptionError(f'Options must include {valid_options[:2]}')
        for key in dataset['opts'].keys():
            if key not in valid_options:
                raise OptionError(f'Invalid option {key}.')  # noqa
        if (dataset['opts']['row_pattern'] not in ['copy']
                and
                not callable(dataset['opts']['row_pattern'])):
            raise OptionError(f'row_pattern option must be one of [\'copy\'] or a function')  # noqa


def validate(datasets):
    """
    Helper function to apply all validations.

    Parameters
    ----------
    datasets: dict[]
        list of datasets to validate.
    """
    _check_col_length(datasets)
    _check_arg_consistency(datasets)
    _check_dataset_options(datasets)
