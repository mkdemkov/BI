import tarantool

from fastapi import FastAPI
from tt.tarantool_connector import TarantoolConnector

app = FastAPI()
tt = TarantoolConnector()


@app.get('/get_workspace')
async def get_data():
    result = tt.get_workspace()
    return result
