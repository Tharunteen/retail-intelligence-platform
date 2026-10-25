
import pandas as pd
import pytest


@pytest.fixture
def sample_orders():
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


def test_order_ids_are_unique(sample_orders):
    assert sample_orders["order_id"].is_unique


def test_order_ids_are_not_null(sample_orders):
    assert sample_orders["order_id"].notna().all()


def test_quantity_is_positive(sample_orders):
    assert (sample_orders["quantity"] > 0).all()


def test_unit_price_is_non_negative(sample_orders):
    assert (sample_orders["unit_price"] >= 0).all()


def test_order_date_is_valid(sample_orders):
    parsed = pd.to_datetime(sample_orders["order_date"], errors="coerce")
    assert parsed.notna().all()


def test_duplicate_order_ids_are_detected(sample_orders):
    duplicated = pd.concat(
        [sample_orders, sample_orders.iloc[[0]]],
        ignore_index=True,
    )
    assert not duplicated["order_id"].is_unique
