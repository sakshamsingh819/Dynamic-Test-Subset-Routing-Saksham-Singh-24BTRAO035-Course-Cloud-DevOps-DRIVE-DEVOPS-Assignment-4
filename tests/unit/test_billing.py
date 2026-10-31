"""
Unit Tests for BillingService
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.services.billing import BillingService, InvoiceItem


@pytest.fixture
def billing_service():
    return BillingService(default_currency="USD", tax_rate=0.18)


def test_calculate_discount_tiers(billing_service):
    assert billing_service.calculate_discount(50.0) == 0.0
    assert billing_service.calculate_discount(150.0) == 7.50   # 5% of 150
    assert billing_service.calculate_discount(250.0) == 25.00  # 10% of 250
    assert billing_service.calculate_discount(600.0) == 90.00  # 15% of 600


def test_calculate_discount_negative(billing_service):
    with pytest.raises(ValueError):
        billing_service.calculate_discount(-10.0)


def test_calculate_tax(billing_service):
    tax = billing_service.calculate_tax(100.0)
    assert tax == 18.00


def test_currency_conversion(billing_service):
    # 100 USD to INR (rate 83.5)
    inr = billing_service.convert_currency(100.0, "USD", "INR")
    assert inr == 8350.0
    # Round-trip check USD -> EUR -> USD
    eur = billing_service.convert_currency(100.0, "USD", "EUR")
    assert eur == 92.0
    back_usd = billing_service.convert_currency(eur, "EUR", "USD")
    assert abs(back_usd - 100.0) < 0.1


def test_generate_invoice_flow(billing_service):
    items = [
        InvoiceItem(description="Cloud GPU Server Tier-A", unit_price=250.0, quantity=2),  # 500
        InvoiceItem(description="Persistent Storage 1TB", unit_price=50.0, quantity=2),   # 100
    ]
    # Subtotal = 600 -> Discount 15% = 90 -> Taxable = 510 -> Tax 18% = 91.80 -> Total = 601.80
    inv = billing_service.generate_invoice(user_id="usr_0001", items=items)
    assert inv.subtotal == 600.00
    assert inv.discount_amount == 90.00
    assert inv.tax_amount == 91.80
    assert inv.total_amount == 601.80
    assert inv.status == "issued"
    assert billing_service.get_invoice(inv.invoice_id) is not None
