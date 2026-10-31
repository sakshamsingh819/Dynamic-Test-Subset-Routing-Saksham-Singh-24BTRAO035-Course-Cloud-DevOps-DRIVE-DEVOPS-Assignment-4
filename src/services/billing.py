"""
Billing & Invoicing Service
Author: Saksham Singh (24BTRAO035)
Implements deterministic pricing, volume discounts, tax schedules, and currency conversions.
"""
from dataclasses import dataclass
from typing import Dict, List, Optional
import time

from src.utils.validators import validate_currency


@dataclass
class InvoiceItem:
    description: str
    unit_price: float
    quantity: int

    @property
    def total(self) -> float:
        return round(self.unit_price * self.quantity, 2)


@dataclass
class Invoice:
    invoice_id: str
    user_id: str
    items: List[InvoiceItem]
    currency: str
    subtotal: float
    discount_amount: float
    tax_amount: float
    total_amount: float
    status: str = "issued"
    issued_at: float = 0.0


class BillingService:
    """Calculates invoice totals with progressive discounting and GST tax schedules."""

    EXCHANGE_RATES: Dict[str, float] = {
        "USD": 1.0,
        "EUR": 0.92,
        "GBP": 0.79,
        "INR": 83.5,
        "JPY": 155.0,
    }

    def __init__(self, default_currency: str = "USD", tax_rate: float = 0.18):
        self.default_currency = default_currency
        self.tax_rate = tax_rate
        self._invoices: Dict[str, Invoice] = {}

    def calculate_discount(self, subtotal: float) -> float:
        """Progressive discount schedule: > $500: 15%, > $200: 10%, > $100: 5%"""
        if subtotal < 0:
            raise ValueError("Subtotal cannot be negative")
        if subtotal >= 500.0:
            return round(subtotal * 0.15, 2)
        elif subtotal >= 200.0:
            return round(subtotal * 0.10, 2)
        elif subtotal >= 100.0:
            return round(subtotal * 0.05, 2)
        return 0.0

    def calculate_tax(self, taxable_amount: float) -> float:
        if taxable_amount < 0:
            raise ValueError("Taxable amount cannot be negative")
        return round(taxable_amount * self.tax_rate, 2)

    def convert_currency(self, amount: float, from_curr: str, to_curr: str) -> float:
        if not validate_currency(from_curr) or not validate_currency(to_curr):
            raise ValueError(f"Unsupported currency pair: {from_curr}->{to_curr}")
        if amount < 0:
            raise ValueError("Amount cannot be negative")

        # Normalize to USD then convert to target currency
        usd_amount = amount / self.EXCHANGE_RATES[from_curr.upper()]
        converted = usd_amount * self.EXCHANGE_RATES[to_curr.upper()]
        return round(converted, 2)

    def generate_invoice(self, user_id: str, items: List[InvoiceItem], currency: Optional[str] = None) -> Invoice:
        if not items:
            raise ValueError("Invoice must contain at least one item")

        curr = currency or self.default_currency
        if not validate_currency(curr):
            raise ValueError(f"Invalid currency: {curr}")

        subtotal = round(sum(item.total for item in items), 2)
        discount = self.calculate_discount(subtotal)
        taxable = subtotal - discount
        tax = self.calculate_tax(taxable)
        final_total = round(taxable + tax, 2)

        invoice_id = f"INV-{len(self._invoices) + 1001}"
        invoice = Invoice(
            invoice_id=invoice_id,
            user_id=user_id,
            items=items,
            currency=curr.upper(),
            subtotal=subtotal,
            discount_amount=discount,
            tax_amount=tax,
            total_amount=final_total,
            status="issued",
            issued_at=time.time()
        )
        self._invoices[invoice_id] = invoice
        return invoice

    def get_invoice(self, invoice_id: str) -> Optional[Invoice]:
        return self._invoices.get(invoice_id)
