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
        self.connection = tarantool.connect(self._host, self._port, self._user)
        # self.connection = tarantool.connect(self._host, self._port, self._user, self._password)

    def get_workspace(self):
        workspace = self.connection.call('select_optimal').data
        return None if len(workspace) == 1 and workspace[0] == 0 else workspace

    def insert_tuples(self, data: []):
        try:
            if len(data):
                self.connection.call('insert_tuples', [data])
            return True
        except Exception as ex:
            print(str(ex))
            return False

    def load_data_and_export(self):
        data = self.connection.space('workspace').select().data
        self.connection.call('remove_workspace')
        return data

    def clear_workspace(self):
        self.connection.call('remove_workspace')

    def multiply_data(self, num, col):
        self.connection.call('multiply_data', (num, col))
        data = self.get_workspace()
        return data

    def sum_data(self, num, col):
        self.connection.call('sum_data', (num, col))
        data = self.get_workspace()
        return data

    def diff_data(self, num, col):
        self.connection.call('diff_data', (num, col))
        data = self.get_workspace()
        return data

    def divide_data(self, num, col):
        self.connection.call('divide_data', (num, col))
        data = self.get_workspace()
        return data

    def divide_mod_data(self, num, col):
        self.connection.call('divide_mod_data', (num, col))
        data = self.get_workspace()
        return data
