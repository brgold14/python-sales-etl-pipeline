from typing import cast


def calculate_revenue(quantity, price):
    return quantity * price

def filter_high_revenue_sales(sales):
    filtered_sales = []
    for sale in sales:
        revenue = calculate_revenue(sale["quantity"], sale["price"])
        if revenue > threshold:
            sale["revenue"] = revenue
            filtered_sales.append(sale)
    return filtered_sales

def calculate_total_revenue(sales):
    total_revenue = 0
    for sale in sales:
        revenue = calculate_revenue(sale["quantity"], sale["price"])
        total_revenue += revenue
    return total_revenue

def find_highest_revenue_products(sales):
    total_revenue = 0
    #total_items = 0
    max_revenue = 0
    max_revenue_items = ""
    for sale in sales:
        revenue = calculate_revenue(sale["quantity"], sale["price"])
        if revenue > max_revenue:
            max_revenue = revenue
            max_revenue_items = sale["product"]
        total_revenue += revenue
        #items = sale["quantity"]
        #total_items += items
    return max_revenue_items

def generate_sales_summary(sales):
    sale_summary = {}
    sale_summary["total_revenue"] = calculate_total_revenue(sales)
    sale_summary["highest_revenue_product"] = find_highest_revenue_products(sales)
    return sale_summary

def add_revenue_to_sales(sales):
    updated_sales = []
    for sale in sales:
        sale_copy = sale.copy()
        revenue = calculate_revenue(sale["quantity"], sale["price"])
        sale_copy["revenue"] = revenue
        updated_sales.append(sale_copy)
    return updated_sales


sales = [
    {"product": "Laptop", "quantity": 2, "price": 800},
    {"product": "Monitor", "quantity": 3, "price": 250},
    {"product": "Keyboard", "quantity": 5, "price": 50},
    {"product": "Mouse", "quantity": 10, "price": 25}
]

updated_sales = add_revenue_to_sales(sales)

print("Original:", sales[0])
print("Updated:", updated_sales[0])
#summary = generate_sales_summary(sales)

# print(f"\nSales Summary \n-------------")
# print(f"Total Revenue: ${summary['total_revenue']:.2f}")
# print(f"Highest Revenue Product: {summary["highest_revenue_product"]}")
# print(generate_sales_summary(sales))

# filtered_sales = filter_high_revenue_sales(sales, 1000)
# for sale in filtered_sales:
#     print(f"{sale['product']}: ${sale['revenue']:.2f}")
# print(f"Number of high revenue sales: {len(filtered_sales)}")
#
# high_revenue_sales = []
#
# for sale in sales:
#     revenue = calculate_revenue(sale["quantity"], sale["price"])
#     if revenue > 500:
#         sale["revenue"] = revenue
#         high_revenue_sales.append(sale)

# print(high_revenue_sales)
# print(f"\nNumber of high revenue sales: {len(high_revenue_sales)}")
# print(sales[0])
#
# print(f"Total Revenue: ${calculate_total_revenue(sales):.2f}")