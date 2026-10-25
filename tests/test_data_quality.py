
import pandas as pd
import pytest


REQUIRED_COLUMNS = {
    "order_id",
    "quantity",
    "unit_price",
    "order_date",
}


def validate_orders(df: pd.DataFrame) -> list[str]:
    """Return data-quality errors found in an order dataset."""
    errors = []

    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        return [f"Missing required columns: {sorted(missing_columns)}"]

    if df["order_id"].isna().any():
        errors.append("Null order IDs found")

    if df["order_id"].duplicated().any():
        errors.append("Duplicate order IDs found")

    if df["quantity"].isna().any() or (df["quantity"] <= 0).any():
        errors.append("Quantity must be positive and non-null")

    if df["unit_price"].isna().any() or (df["unit_price"] < 0).any():
        errors.append("Unit price must be non-negative and non-null")

    dates = pd.to_datetime(df["order_date"], errors="coerce")
    if dates.isna().any():
        errors.append("Invalid or missing order dates found")

    return errors


@pytest.fixture
def valid_orders():
    return pd.DataFrame([
        {
            "order_id": "ORD-001",
            "quantity": 2,
            "unit_price": 100.0,
            "order_date": "2026-10-25",
        },
        {
            "order_id": "ORD-002",
            "quantity": 1,
            "unit_price": 250.0,
            "order_date": "2026-10-25",
        },
    ])


def test_valid_orders_pass(valid_orders):
    assert validate_orders(valid_orders) == []


def test_duplicate_orders_are_rejected(valid_orders):
    duplicated = pd.concat(
        [valid_orders, valid_orders.iloc[[0]]],
        ignore_index=True,
    )
    assert "Duplicate order IDs found" in validate_orders(duplicated)


def test_null_order_id_is_rejected(valid_orders):
    valid_orders.loc[0, "order_id"] = None
    assert "Null order IDs found" in validate_orders(valid_orders)


def test_invalid_quantity_is_rejected(valid_orders):
    valid_orders.loc[0, "quantity"] = 0
    assert "Quantity must be positive and non-null" in validate_orders(
        valid_orders
    )


def test_negative_price_is_rejected(valid_orders):
    valid_orders.loc[0, "unit_price"] = -10
    assert "Unit price must be non-negative and non-null" in validate_orders(
        valid_orders
    )


def test_invalid_date_is_rejected(valid_orders):
    valid_orders.loc[0, "order_date"] = "not-a-date"
    assert "Invalid or missing order dates found" in validate_orders(
        valid_orders
    )


def test_missing_column_is_detected(valid_orders):
    valid_orders.drop(columns=["quantity"], inplace=True)
    errors = validate_orders(valid_orders)
    assert any("Missing required columns" in error for error in errors)
