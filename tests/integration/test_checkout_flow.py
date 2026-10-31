"""
Integration Test: End-to-End E-Commerce Checkout Lifecycle
Author: Saksham Singh (24BTRAO035)
Verifies multi-service integration across Inventory, Billing, Order, and Notifications.
"""
import pytest
from src.services.inventory import InventoryService
from src.services.billing import BillingService
from src.services.order import OrderService, OrderStatus
from src.services.notifications import NotificationService


def test_complete_checkout_pipeline():
    # Setup services
    inventory = InventoryService()
    billing = BillingService(default_currency="USD", tax_rate=0.18)
    order_svc = OrderService(inventory, billing)
    notifier = NotificationService()

    # Seed products
    inventory.add_product("SKU-GPU", "NVIDIA RTX 5090 Cloud Instance", 400.0, initial_stock=10)
    inventory.add_product("SKU-STORAGE", "NVMe 2TB Volume", 100.0, initial_stock=20)

    # Place order: 1 GPU ($400) + 2 Storage ($200) = $600 Subtotal
    # $600 qualifies for 15% discount ($90) -> $510 Taxable + 18% tax ($91.80) = $601.80
    order = order_svc.create_order(
        user_id="usr_cloud_dev",
        customer_email="saksham.cloud@devops.org",
        item_requests=[
            {"sku": "SKU-GPU", "quantity": 1},
            {"sku": "SKU-STORAGE", "quantity": 2}
        ]
    )

    assert order.status == OrderStatus.PENDING
    assert order.total_amount == 601.80

    # Settle payment
    assert order_svc.process_payment(order.order_id) is True
    assert order.status == OrderStatus.PAID

    # Dispatch receipt notification
    evt = notifier.send_email(
        recipient_email=order.customer_email,
        subject=f"Order Confirmed: {order.order_id}",
        message=f"Thank you. Your payment of ${order.total_amount} has been processed."
    )
    assert evt.status == "delivered"

    # Verify inventory was committed
    gpu = inventory.get_product("SKU-GPU")
    assert gpu.stock_quantity == 9
    assert gpu.reserved_quantity == 0
