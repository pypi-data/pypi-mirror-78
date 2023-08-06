"""
Handling of options passed to the decorator to generate more rows of data.
"""


def _copy_rows(data, num_rows, base_row_index=0):
    """
    Copies one list from a list of lists and adds it to the same list n times.

    Parameters
    ----------
    data: [][]
        Dataset to apply the function to. This will be mutated.
    base_row_index: int
        The index of the row to copy
    num_rows: int
        The number of times to copy the base row.

    Returns
    -------
    [][]
        List of lists, containing the additional copied data.
    """
    copies = [data[base_row_index] for _ in range(num_rows)]
    return data + copies


def _apply_func(data, func, num_rows, base_row_index=0, increment=False):
    """
    Apply the function to the base row which returns a new row.
    This is then added to the dataset n times.

    Parameters
    ----------
    data: [][]
        List to apply the function to.
    func: function
        The function to apply to the row. This won't alter the initial row
        it is applied to.
    base_row_index: int
        The index of the row to first apply the function to.
    num_rows: int
        The number of times this function should be applied. Will result in
        this many new rows added to the dataset.
    increment: boolean
        If true, the function will be applied to the newly created rows rather
        than the base row on further iterations.

    Returns
    -------
    [][]
        The mutated list with the new rows added.
    """
    row = list(data[base_row_index])
    curr_index = base_row_index
    for _ in range(num_rows):
        data.append(func(row))
        if increment:
            curr_index += 1
            row = list(data[curr_index])
    return data


def apply_options(data, opts):
    """
    Applies the passed options to the dataset.

    Parameters
    ----------
    data: [][]
        List of lists containing the mock csv data.
    opts: dict
        Dictionary of options used to determine how to mutate the data.
        Options are as follows:
            add_rows: int
                The number of rows to add onto the mock dataset.
            row_pattern: str or function
                if str, should be 'copy' to apply the copy function.
                if function, will be used to create the new rows.
            base_row_index: int
                The index of the base row to apply the row pattern to.
            increment: boolean,
                If true and row_pattern is a function, the function will
                be applied incrementally on the dataset, rather than just
                on the base row over and over again.

    Returns
    -------
    [][]
        The dataset with the new rows added.
    """
    if not opts:
        return data
    if opts['row_pattern'] == 'copy':
        data = _copy_rows(
            data=data,
            num_rows=opts['add_rows'],
            base_row_index=opts.get('base_row_index') or 0
        )
    else:
        data = _apply_func(
            data=data,
            func=opts['row_pattern'],
            num_rows=opts['add_rows'],
            base_row_index=opts.get('base_row_index') or 0,
            increment=opts.get('increment') or False
        )
    return data
