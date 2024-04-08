import csv
import openpyxl

from frontend.bot.get_info_from_api import load_data

SEPARATOR = ';'


async def process_csv_export():
    data = await load_data()
    csv_filepath = 'data.csv'

    with open(csv_filepath, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=SEPARATOR)
        for row in data:
            writer.writerow(row[1:])


async def process_excel_export():
    data = await load_data()
    excel_filepath = 'data.xlsx'

    workbook = openpyxl.Workbook()
    sheet = workbook.active

    for row in data:
        sheet.append(row[1:])

    workbook.save(filename=excel_filepath)
