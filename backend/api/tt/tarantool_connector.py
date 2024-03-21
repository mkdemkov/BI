import tarantool
import os

from dotenv import load_dotenv

load_dotenv()


class TarantoolConnector:
    _host = "localhost"
    _port = 3301

    def __init__(self):
        self._user = os.getenv("TARANTOOL_USER")
        self._password = os.getenv("TARANTOOL_PASSWORD")
        self.connection = tarantool.connect(self._host, self._port, self._user, self._password)

    def get_workspace(self):
        workspace = self.connection.call('get_data').data
        return None if len(workspace) == 1 and workspace[0] == 0 else workspace

    def insert_tuples(self, data: []):
        try:
            if len(data):
                self.connection.call('insert_tuples', [data])
            return True
        except Exception as ex:
            print(str(ex))
            return False
