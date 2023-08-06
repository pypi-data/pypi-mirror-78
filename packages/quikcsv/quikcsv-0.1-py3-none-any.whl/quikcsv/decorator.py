import csv
import io
from functools import wraps
import inspect

from .validation import validate
from .options import apply_options


def QuikCSV(datasets):
    """
    Decorator to quickly create temporary CSV mock files. These are passed to
    specified arguments in the decorated function (or to the first argument by
    default). These files are used like any other file in Python, but don't
    need to be opened or closed.

    Parameters
    ----------
    datasets: dict[]
        List of dictionaries which specificy the data to mock in the csv.
    """
    def outer(func):
        @wraps(func)
        def inner(*args, **kwargs):
            csvs = []
            validate(datasets)
            try:
                for dataset in datasets:
                    data_ = apply_options(
                        dataset['data'],
                        dataset.get('opts')
                    )
                    stream = io.StringIO()
                    writer = csv.writer(stream)
                    writer.writerows(data_)
                    stream.seek(0)
                    if dataset.get('arg'):
                        arg_names = inspect.getfullargspec(func).args
                        index = arg_names.index(dataset['arg'])
                        args = args[:index] + args[index+1:]
                        args = args[:index] + (stream,) + args[index:]
                    else:
                        csvs.append(stream)
                if len(csvs) > 0:
                    return func(csvs, *args, **kwargs)
                else:
                    return func(*args, **kwargs)
            finally:
                for stream in csvs:
                    stream.close()
        return inner
    return outer
