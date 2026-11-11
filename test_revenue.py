import pytest, math, csv, sys, logging, read_sales_csv
from _pytest import monkeypatch

from read_sales_csv import calculate_revenue, validate_sale, extract_sales, load_sales, add_revenue_to_sales, run_pipeline, aggregate_revenue_by_product

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

def test_run_pipeline(tmp_path):
    input_file = tmp_path / "input_sales.csv"
    output_file = tmp_path / "output_sales.csv"

    input_file.write_text(
        "product,quantity,price\n"
        "Laptop,2,800\n"
        "Monitor,3,250\n"
        "Keyboard,abc,50\n"
        "Mouse,4,25\n"
        "Laptop,1,800\n"
    )

    statistics = run_pipeline(input_file, output_file)

    assert statistics["valid_records"] == 4
    assert statistics["invalid_records"] == 1
    assert statistics["revenue_by_product"]["Laptop"] == 2400.00
    assert statistics["revenue_by_product"]["Monitor"] == 750.00
    assert statistics["revenue_by_product"]["Mouse"] == 100.00
    assert "Keyboard" not in statistics["revenue_by_product"]
    assert output_file.exists()

def test_run_pipeline_missing_file(tmp_path, caplog):
    input_file = tmp_path / "missing_sales.csv"
    output_file = tmp_path / "output_sales.csv"

    with pytest.raises(FileNotFoundError) as exc_info:
        run_pipeline(input_file, output_file)

    assert not output_file.exists()
    assert "Failed to read sales file:" in caplog.text
    assert "missing_sales.csv" in str(exc_info.value)
    assert "missing_sales.csv" in caplog.text

def test_extract_sales_logs_invalid_record(tmp_path, caplog):
    input_file = tmp_path / "input_sales.csv"


    input_file.write_text(
        "product,quantity,price\n"
        "Laptop,2,800\n"
        "Keyboard,-1,50\n"
        "Mouse,3,25\n"
    )

    sales, invalid_count = extract_sales(input_file)

    assert len(sales) == 2
    assert invalid_count == 1
    assert "Invalid entry:" in caplog.text
    assert "Keyboard" in caplog.text
    assert any(
        record.levelname == "WARNING"
        and "Keyboard" in record.getMessage()
        for record in caplog.records
    )

def test_extract_sales_valid_records_no_warnings(tmp_path, caplog):
    input_file = tmp_path / "input_sales.csv"

    input_file.write_text(
        "product,quantity,price\n"
        "Laptop,2,800\n"
        "Mouse,3,25\n"
        "Monitor,1,250\n"
    )

    sales, invalid_count = extract_sales(input_file)

    assert len(sales) == 3
    assert invalid_count == 0
    assert not any(
        record.levelno >= logging.WARNING
        for record in caplog.records
    )

def test_run_pipeline_output_directory_missing(tmp_path, caplog):
    input_file = tmp_path / "input_sales.csv"
    output_file = tmp_path / "missing_folder" / "output_sales.csv"

    input_file.write_text(
        "product,quantity,price\n"
        "Laptop,2,800\n"
    )

    with pytest.raises(FileNotFoundError):
        run_pipeline(input_file, output_file)

    assert any(
        record.levelname == "ERROR"
        and "Failed to write sales file:" in record.getMessage()
        for record in caplog.records
    )

def test_run_pipeline_input_permission_error(tmp_path, monkeypatch, caplog):
    input_file = tmp_path / "input_sales.csv"
    output_file = tmp_path / "output_sales.csv"

    def fake_extract_sales(filename):
        raise PermissionError("Access Denied")

    monkeypatch.setattr(
        read_sales_csv, "extract_sales", fake_extract_sales
    )

    with pytest.raises(PermissionError):
        run_pipeline(input_file, output_file)

    assert any(
        record.levelname == "ERROR"
        and "Failed to read sales file:" in record.getMessage()
        for record in caplog.records
    )

def test_aggregate_revenue_by_product():
    sales = [
        {"product": "Laptop", "quantity": 2, "revenue": 1600.00},
        {"product": "Mouse", "quantity": 3, "revenue": 75.00},
        {"product": "Laptop", "quantity": 1, "revenue": 800.00},
        {"product": "Mouse", "quantity": 2, "revenue": 50.00},
        {"product": "Monitor", "quantity": 1, "revenue": 250.00}
    ]

    result = aggregate_revenue_by_product(sales)

    assert len(result) == 3
    assert result["Laptop"] == 2400.00
    assert result["Mouse"] == 125.00
    assert result["Monitor"] == 250.00

def test_aggregate_revenue_by_product_empty():
    sales = []
    result = aggregate_revenue_by_product(sales)

    assert result == {}