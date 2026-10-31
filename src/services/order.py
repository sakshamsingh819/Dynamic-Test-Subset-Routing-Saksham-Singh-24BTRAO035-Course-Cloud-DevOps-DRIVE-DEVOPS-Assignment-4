"""
Order Processing Domain Service
Author: Saksham Singh (24BTRAO035)
Coordinates multi-item checkouts, inventory reservation, and invoicing.
"""
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional
import time

from src.services.billing import BillingService, InvoiceItem, Invoice
from src.services.inventory import InventoryService
from src.utils.validators import validate_email


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FULFILLED = "FULFILLED"
    CANCELLED = "CANCELLED"


@dataclass
class OrderItem:
    sku: str
    quantity: int
    unit_price: float


@dataclass
class Order:
    order_id: str
    user_id: str
    customer_email: str
    items: List[OrderItem]
    total_amount: float
    status: OrderStatus = OrderStatus.PENDING
    invoice_id: Optional[str] = None
    created_at: float = field(default_factory=time.time)


class OrderService:
    """Manages order creation, transactional reservations, and payment settlements."""

    def __init__(self, inventory_svc: InventoryService, billing_svc: BillingService):
        self.inventory_svc = inventory_svc
        self.billing_svc = billing_svc
        self._orders: Dict[str, Order] = {}

    def create_order(self, user_id: str, customer_email: str, item_requests: List[Dict[str, int]]) -> Order:
        if not validate_email(customer_email):
            raise ValueError(f"Invalid customer email: {customer_email}")
        if not item_requests:
            raise ValueError("Order must contain items")

        # Step 1: Verify inventory and calculate line items
        order_items: List[OrderItem] = []
        invoice_items: List[InvoiceItem] = []
        reserved_skus: List[tuple[str, int]] = []

        try:
            for req in item_requests:
                sku = req["sku"]
                qty = req["quantity"]
                prod = self.inventory_svc.get_product(sku)
                if not prod:
                    raise KeyError(f"Product SKU {sku} not found")

                # Reserve stock
                if not self.inventory_svc.reserve_stock(sku, qty):
                    raise ValueError(f"Insufficient stock for SKU {sku}")
                reserved_skus.append((sku, qty))

                order_items.append(OrderItem(sku=sku, quantity=qty, unit_price=prod.unit_price))
                invoice_items.append(InvoiceItem(description=prod.title, unit_price=prod.unit_price, quantity=qty))

            # Step 2: Generate invoice
            invoice = self.billing_svc.generate_invoice(user_id=user_id, items=invoice_items)

            # Step 3: Instantiate order
            order_id = f"ORD-{len(self._orders) + 5001}"
            order = Order(
                order_id=order_id,
                user_id=user_id,
                customer_email=customer_email,
                items=order_items,
                total_amount=invoice.total_amount,
                status=OrderStatus.PENDING,
                invoice_id=invoice.invoice_id
            )
            self._orders[order_id] = order
            return order

        except Exception:
            # Rollback reserved items if checkout aborts
            for r_sku, r_qty in reserved_skus:
                self.inventory_svc.release_reservation(r_sku, r_qty)
            raise

    def process_payment(self, order_id: str) -> bool:
        order = self._orders.get(order_id)
        if not order or order.status != OrderStatus.PENDING:
            return False

        # Deduct stock permanently
        for it in order.items:
            self.inventory_svc.commit_stock(it.sku, it.quantity)

        order.status = OrderStatus.PAID
        return True

    def cancel_order(self, order_id: str) -> bool:
        order = self._orders.get(order_id)
        if not order:
            return False

        if order.status == OrderStatus.PENDING:
            for it in order.items:
                self.inventory_svc.release_reservation(it.sku, it.quantity)
            order.status = OrderStatus.CANCELLED
            return True
        return False

    def get_order(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)
