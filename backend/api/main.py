from fastapi import FastAPI
from typing import List, Dict

from tt.tarantool_connector import TarantoolConnector

app = FastAPI()
tt = TarantoolConnector()


@app.get('/get_workspace')
async def get_data():
    result = tt.get_workspace()
    return result


@app.get('/get_workspace_optimal')
async def get_data_optimal():
    result = tt.get_workspace_optimal()
    return result


@app.get('/export_workspace')
async def export_workspace():
    result = tt.load_data_and_export()
    return result


@app.post('/import_data')
async def import_data(data: List[List[int]]):
    tt.clear_workspace()
    tuples_data = [tuple(item) for item in data]
    tt.insert_tuples(tuples_data)
    res = tt.get_workspace()
    return res


@app.post('/transform_data')
async def transform_data(data: Dict):
    num, col = data['number'], data['column']
    if data['operation'] == 'Умножение':
        result = tt.multiply_data(num, col)
    elif data['operation'] == 'Сложение':
        result = tt.sum_data(num, col)
    elif data['operation'] == 'Вычитание':
        result = tt.diff_data(num, col)
    elif data['operation'] == 'Целая часть':
        result = tt.divide_data(num, col)
    else:
        result = tt.divide_mod_data(num, col)

    return result
