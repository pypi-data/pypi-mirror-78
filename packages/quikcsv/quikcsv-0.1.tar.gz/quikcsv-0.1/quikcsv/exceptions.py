

class Error(Exception):
    """Base Error"""
    pass


class UnevenColumnError(Error):

    def __init__(self, data, message="Mock data columns are uneven. Check \
                                      the length of your lists, they need to \
                                      match."):
        self.data = data
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.data} -> {self.message}'


class ArgError(Error):

    def __init__(self, message="arg must be specified on all datasets if \
                                specified on one."):
        self.message = message
        super().__init__(self.message)


class OptionError(Error):

    def __init__(self, message="Error with passed options."):
        self.message = message
        super().__init__(self.message)
