import pytest

from read_sales_csv import calculate_revenue, validate_sale


def test_calculate_revenue():
    assert calculate_revenue(3, 250) == 750
    assert calculate_revenue(2, 100) == 200
    assert calculate_revenue(0, 100) == 0

def test_invalid_quantity():
    invalid_sale = {"product": "Keyboard", "quantity": "-2", "price": "50"}
    with pytest.raises(ValueError, match="Quantity must be greater than 0"):
        validate_sale(invalid_sale)

def test_invalid_price():
    invalid_sale = {"product": "Monitor", "quantity": "3", "price": "-250"}
    with pytest.raises(ValueError, match="Price must be 0 or greater"):
        validate_sale(invalid_sale)

def test_invalid_product():
    invalid_sale = {"product": "   ", "quantity": "3", "price": "100"}
    with pytest.raises(ValueError, match="Product name is required"):
        validate_sale(invalid_sale)