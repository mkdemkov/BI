import tarantool

from fastapi import FastAPI
from typing import List

from tt.tarantool_connector import TarantoolConnector

app = FastAPI()
tt = TarantoolConnector()


@app.get('/get_workspace')
async def get_data():
    result = tt.get_workspace()
    return result


@app.get('/export_workspace')
async def export_workspace():
    result = tt.load_data_and_export()
    return result


@app.post('/import_data')
async def import_data(data: List[List[int]]):
    tt.clear_workspace()
    tuples_data = [tuple(item) for item in data]
    res = tt.insert_tuples(tuples_data)
    if res:
        return data
