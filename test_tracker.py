import pytest
import pandas as pd
from database import add_transaction, get_transactions, reset_data

@pytest.fixture(autouse=True)
def run_around_tests():
    """Reset database before each test"""
    reset_data()
    yield
    reset_data()

def test_add_transaction():
    add_transaction(
        amount=100,
        description="Test Transaction",
        category="Food",
        txn_type="expense",
        payment_method="Cash",
        txn_date="2025-02-04"
    )
    transactions = get_transactions()
    df = pd.DataFrame(transactions, columns=["id", "amount", "description", "category", "type", "payment_method", "date"])
    assert not df.empty
    assert df.iloc[0]["description"] == "Test Transaction"
