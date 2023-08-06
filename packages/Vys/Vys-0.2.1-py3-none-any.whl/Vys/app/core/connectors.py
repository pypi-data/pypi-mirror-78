#! python3


class Connect:
    def __init__(
            self, base_url,
            headers=None,
            params=None,
            auth=None,
            auth_type=None,
            body=None
    ):
        self._base_url = base_url
        self._headers = {}
        self._params = {}
        self._auth = None
        self._auth_type = None
        self._data = {}
        self._auth_body = None

    def __str__(self):
        return f'This is the core Connector module. '

    def __repr__(self):
        return f'test'


if __name__ == '__main__':
    pass
