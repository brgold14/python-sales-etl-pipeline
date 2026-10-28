import csv

sales = []

with open('sales.csv', 'r', newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        sales.append(row)

print(sales)