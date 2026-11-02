import pytest, math, csv

from read_sales_csv import calculate_revenue, validate_sale, extract_sales, load_sales, add_revenue_to_sales

@pytest.mark.parametrize(
    "quantity, price, expected",
    [
        (3,250,750),
        (2, 100, 200),
        (0,100,0),
        (5,19.99, 99.95)
    ]
)
def test_calculate_revenue(quantity, price, expected):
    assert math.isclose(calculate_revenue(quantity, price), expected)

@pytest.mark.parametrize(
    "invalid_sale, expected_error",
    [
        (
            {"product": "Keyboard", "quantity": "-2", "price": "50"},
            "Quantity must be greater than 0"
        ),
        (
            {"product": "Monitor", "quantity": "3", "price": "-250"},
            "Price must be 0 or greater"
        ),
        (
                {"product": "   ", "quantity": "3", "price": "100"},
            "Product name is required"
        ),
    ]
)
def test_invalid_sales_parameterized(invalid_sale, expected_error):
    with pytest.raises(ValueError, match=expected_error):
        validate_sale(invalid_sale)

def test_extract_sales(tmp_path):
    test_file = tmp_path / "test_sales.csv"
    test_file.write_text(
        "product,quantity,price\n"
        "Laptop,2,800\n"
        "Monitor,3,250\n"
    )

    sales, invalid_count = extract_sales(test_file)

    assert len(sales) == 2
    assert invalid_count == 0
    assert sales[0]["product"] == "Laptop"
    assert sales[0]["quantity"] == 2
    assert sales[1]["price"] == 250.0
    assert isinstance(sales[0]["quantity"], int)
    assert isinstance(sales[1]["price"], float)

def test_extract_sales_with_invalid_records(tmp_path):
    test_file = tmp_path / "test_sales.csv"
    test_file.write_text(
        "product,quantity,price\n"
        "Laptop,2,800\n"
        "Keyboard,abc,500\n"
        "Monitor,3,250\n"
        "Mouse,-5,25\n"
        "Headphones,4,-20"
    )

    sales, invalid_count = extract_sales(test_file)

    assert len(sales) == 2
    assert invalid_count == 3
    assert sales[0]["product"] == "Laptop"
    assert sales[1]["product"] == "Monitor"

def test_load_sales(tmp_path):
    test_file = tmp_path / "output_sales.csv"
    sales_data = [
        {"product": "Laptop", "quantity": 2, "price": 800.0, "revenue": 1600.0},
        {"product": "Monitor", "quantity": 3, "price": 250.0, "revenue": 750.0}
    ]

    load_sales(test_file, sales_data)

    with open(test_file, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert len(rows) == 2
    assert rows[0]["product"] == "Laptop"
    assert rows[1]["revenue"] == "750.0"
    assert reader.fieldnames == ["product", "quantity", "price", "revenue"]

def test_add_revenue_to_sales():
    sales = [
        {"product": "Laptop", "quantity": 2, "price": 800.0},
        {"product": "Monitor", "quantity": 3, "price": 250.0}
    ]

    updated_sales = add_revenue_to_sales(sales)

    assert len(updated_sales) == 2
    assert updated_sales[0]["revenue"] == 1600.00
    assert updated_sales[1]["revenue"] == 750.0
    assert "revenue" not in sales[0] and "revenue" not in sales[1]

def test_add_revenue_to_sales_empty_list():
    sales = []

    updated_sales = add_revenue_to_sales(sales)

    assert updated_sales == []
    assert isinstance(updated_sales, list)

def test_add_revenue_to_sales_missing_price():
    sales = [
        {"product": "Laptop", "quantity": 2}
    ]

    with pytest.raises(KeyError, match="price"):
        add_revenue_to_sales(sales)

def test_sales_etl_pipeline(tmp_path):
    input_file = tmp_path / "input_sales.csv"
    output_file = tmp_path / "output_sales.csv"

    input_file.write_text(
        "product,quantity,price\n"
        "Laptop,2,800\n"
        "Monitor,3,250\n"
        "Keyboard,abc,50\n"
        "Mouse,4,25\n"
    )

    sales, invalid_count = extract_sales(input_file)

    assert len(sales) == 3
    assert invalid_count == 1

    sales_data = add_revenue_to_sales(sales)

    load_sales(output_file, sales_data)

    with open(output_file, "r", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    assert len(rows) == 3
    assert rows[0]["product"] == "Laptop"
    assert rows[1]["revenue"] == "750.0"
    assert rows[2]["revenue"] == "100.0"
