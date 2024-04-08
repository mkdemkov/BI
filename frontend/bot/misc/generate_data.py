import csv
import random

SEPARATOR = ';'
ROW_COUNT = 100000
LOW = -100
HIGH = 100
COUNT_NUMBERS_IN_ROW = 4


def generate_csv():
    filepath = '../user_data/example.csv'
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=SEPARATOR)
        for _ in range(ROW_COUNT):
            row = [random.randint(LOW, HIGH) for _ in range(COUNT_NUMBERS_IN_ROW)]
            writer.writerow(row)


generate_csv()
