from logging import getLogger

logger = getLogger(__name__)


class Env:
    protocol: str
    host: str
    port: int

    def __init__(self, protocol: str = 'http://', host: str = 'localhost', port: int = 5000):
        self.protocol = protocol
        self.host = host
        self.port = port

        logger.debug(f'{protocol}, {host}, {port}')

    @property
    def base_url(self):
        url = f'{self.protocol}{self.host}'
        if self.port:
            url = f'{url}:{self.port}'

        return url


class DevEnv(Env):

    def __init__(self, protocol: str = 'http://', host: str = 'localhost', port: int = 8000):
        logger.debug(f'dev: {protocol}, {host}, {port}')
        super().__init__(protocol, host, port)


class TestEnv(Env):

    def __init__(self, protocol: str = 'https://', host: str = 'localhost', port: int = None):
        super().__init__(protocol, host, port)


class ProdEnv(Env):

    def __init__(self, protocol: str = 'https://', host: str = 'localhost', port: int = None):
        super().__init__(protocol, host, port)
