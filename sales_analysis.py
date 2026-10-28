def calculate_revenue(quantity, price):
    if quantity < 0 or price < 0:
        return 0
    return quantity * price

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

sales = [
    {"product": "Laptop", "quantity": 2, "price": 799.99},
    {"product": "Monitor", "quantity": 3, "price": 199.99},
    {"product": "Keyboard", "quantity": 5, "price": 49.99},
    {"product": "Headphone", "quantity": 6, "price": 299.99}
]

print(f"Highest Revenue Product: {find_highest_revenue_products(sales)}")

#     print(f"{sale['product']}: ${revenue:.2f}")
#
# print(f"\nTotal Revenue: ${total_revenue:.2f}")
# print(f"Total Items: {total_items: .2f}")
# print(f"Max Revenue Product: {max_revenue_items}")
#
# test_revenue = calculate_revenue(5, 20)
#
# print(f"\nTest Revenue: {test_revenue}")
#
# print(f"Normal sale: {calculate_revenue(5, 20)}")
# print(f"Negative quantity: {calculate_revenue(-5, 20)}")
# print(f"Zero quantity: {calculate_revenue(0, 20)}")
#
# print(calculate_revenue(5, -20))