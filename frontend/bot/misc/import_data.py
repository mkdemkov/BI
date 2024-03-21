import csv


def form_data_csv(path):
    data = []
    counter = 1
    with open(path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=';')

        for row in csv_reader:
            row_data = tuple(map(int, row))
            row_data = (counter,) + row_data
            counter += 1
            data.append(row_data)
    return data
