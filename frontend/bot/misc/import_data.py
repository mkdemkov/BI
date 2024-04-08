import csv
import openpyxl


def form_data_csv(path):
    data = []
    counter = 1

    with open(path, 'r', newline='') as file:
        try:
            dialect = csv.Sniffer().sniff(file.read(1024))
            file.seek(0)
        except csv.Error:
            dialect = csv.excel
            dialect.delimiter = ';'

        csv_reader = csv.reader(file, dialect)

        for row in csv_reader:
            try:
                row_data = tuple(map(int, row))
                row_data = (counter,) + row_data
                counter += 1
                data.append(row_data)
            except ValueError:
                print(f"Skipping row {counter}: cannot convert all to int - {row}")
                continue

    return data


def form_data_excel(path):
    data = []
    counter = 1

    workbook = openpyxl.load_workbook(path)
    worksheet = workbook.active

    for row in worksheet.iter_rows():
        try:
            row_data = tuple(int(cell.value) for cell in row)
            row_data = (counter,) + row_data
            counter += 1
            data.append(row_data)
        except ValueError:
            print(f"Skipping row {counter}: cannot convert all to int")
            continue

    workbook.close()
    return data
