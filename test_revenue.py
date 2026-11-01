import pytest, math

from read_sales_csv import calculate_revenue, validate_sale

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