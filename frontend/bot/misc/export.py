import csv

from frontend.bot.get_info_from_api import load_data


async def process_csv_export():
    data = await load_data()
    csv_filepath = 'data.csv'

    with open(csv_filepath, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for row in data:
            writer.writerow(row[1:])

    return True
