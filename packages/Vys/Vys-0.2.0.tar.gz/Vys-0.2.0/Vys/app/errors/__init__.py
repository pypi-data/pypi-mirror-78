#! python3


class LoginError(Exception):
    pass


class ServerError(Exception):
    pass


class DbError(Exception):
    def __init__(self, message, info=None):
        self.message = message
        self.info = info
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.info or self.message


class SchemaError(Exception):
    def __init__(self, message, info=None):
        self.message = message
        self.info = info
        super().__init__(self.message)

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.info or self.message
