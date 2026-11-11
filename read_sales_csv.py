import csv, argparse, logging
from logging import StreamHandler


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
                logging.warning(f"Invalid entry: %s - %s", product, e)

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

def aggregate_revenue_by_product(sales):
    aggregated_revenue = {}

    for sale in sales:
        product = sale["product"]
        revenue = sale["revenue"]

        aggregated_revenue[product] = aggregated_revenue.get(product, 0) + revenue

    return aggregated_revenue

def run_pipeline(input_filename, output_filename):
    logging.info("Starting ETL pipeline. Input file: %s", input_filename)

    try:
        sales, invalid_count = extract_sales(input_filename)

    except OSError:
        logging.exception("Failed to read sales file: %s", input_filename)
        raise

    sales_data = add_revenue_to_sales(sales)
    revenue_summary = aggregate_revenue_by_product(sales_data)

    try:
        load_sales(output_filename, sales_data)
        logging.info("Successfully wrote output file: %s", output_filename)

    except OSError:
        logging.exception("Failed to write sales file: %s", output_filename)
        raise

    process_statistics = {
        "valid_records": len(sales),
        "invalid_records": invalid_count,
        "revenue_by_product": revenue_summary
    }

    logging.info("ETL pipeline completed. Valid Records: %s, Invalid Records: %s",
                 process_statistics["valid_records"],
                 process_statistics["invalid_records"]
                 )

    return process_statistics


def main():
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("pipeline.log", mode="a")
    file_handler.setLevel(logging.INFO)
    console_handler.setLevel(logging.WARNING)

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[console_handler,
                                  file_handler]
                        )

    parser = argparse.ArgumentParser(
        description="Extract, transform, and load sales data from CSV files."
    )
    parser.add_argument("input_filename", help="Path to the input CSV file")
    parser.add_argument("output_filename", help="Path to the output CSV file")
    args = parser.parse_args()

    statistics = run_pipeline(args.input_filename, args.output_filename)

    print(f"\nTotal valid records: {statistics['valid_records']}")
    print(f"Total invalid records: {statistics['invalid_records']}")
    print("\nRevenue by Product:")
    for product, revenue in statistics['revenue_by_product'].items():
        print(f"{product}: ${revenue:.2f}")

if __name__ == "__main__":
    main()