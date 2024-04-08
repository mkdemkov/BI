import csv
import time

import tarantool

connection = tarantool.connect('localhost', 3301)

csv_file_path = 'backend/tarantool/million_10.csv'

data = []
start_time = time.time()
counter = 1
batch_size = 100000
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')

    for row in csv_reader:
        row_data = tuple(map(float, row))
        row_data = (counter,) + row_data
        counter += 1
        data.append(row_data)
        if len(data) >= batch_size:
            connection.call('insert_tuples', [data])
            data.clear()

if len(data):
    connection.call('insert_tuples', [data])
end_time = time.time()

print((end_time - start_time) * 1000)
