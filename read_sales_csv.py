import csv, argparse

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


def extract_sales(filename):
    sales = []
    invalid_count = 0

    with open(filename, 'r', newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                validated_row = validate_sale(row)

                sales.append(validated_row)

            except (ValueError, KeyError) as e:
                invalid_count += 1
                product = row.get("product", "Unknown")
                print(f"Invalid entry: {product} - {e}")

    return sales, invalid_count

def load_sales(filename, sales_data):
    with open(filename, 'w', newline="") as file:
        columns = ["product", "quantity", "price", "revenue"]
        writer = csv.DictWriter(file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(sales_data)

def validate_sale(row):
    row["quantity"] = int(row["quantity"])

    if row["quantity"] <= 0:
        raise ValueError("Quantity must be greater than 0")

    row["price"] = float(row["price"])

    if row["price"] < 0:
        raise ValueError("Price must be 0 or greater")

    row["product"] = row["product"].strip()

    if not row["product"]:
        raise ValueError("Product name is required")

    return row

def run_pipeline(input_filename, output_filename):
    sales, invalid_count = extract_sales(input_filename)

    sales_data = add_revenue_to_sales(sales)

    load_sales(output_filename, sales_data)

    process_statistics = {
        "valid_records": len(sales),
        "invalid_records": invalid_count
    }

    return process_statistics

def main():
    parser = argparse.ArgumentParser(
        description="Extract, transform, and load sales data from CSV files."
    )
    parser.add_argument("input_filename", help="Path to the input CSV file")
    parser.add_argument("output_filename", help="Path to the output CSV file")
    args = parser.parse_args()

    statistics = run_pipeline(args.input_filename, args.output_filename)

    print(f"\nTotal valid records: {statistics['valid_records']}")
    print(f"Total invalid records: {statistics['invalid_records']}")

if __name__ == "__main__":
    main()