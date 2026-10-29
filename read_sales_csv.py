import csv

def calculate_revenue(quantity, price):
    return quantity * price

def add_revenue_to_sales(sales):
    updated_sales = []
    for sale in sales:
        sale_copy = sale.copy()
        revenue = calculate_revenue(sale["quantity"], sale["price"])
        sale_copy["revenue"] = revenue
        updated_sales.append(sale_copy)
    return updated_sales

sales = []
invalid_count = 0

with open('sales.csv', 'r', newline="") as file:
    reader = csv.DictReader(file)

    for row in reader:
        try:
            row["quantity"] = int(row["quantity"])
            row["price"] = float(row["price"])
            sales.append(row)
        except ValueError as e:
            invalid_count += 1
            print(f"Invalid entry: {row['product']} - {e}")

sales_data = add_revenue_to_sales(sales)
for sale in sales_data:
    print(sale)

print(f"\nValid records: {len(sales)}")
print(f"Invalid records: {invalid_count}")

with open('sales_with_revenue.csv', 'w', newline="") as file:
    columns = ["product", "quantity", "price", "revenue"]
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(sales_data)