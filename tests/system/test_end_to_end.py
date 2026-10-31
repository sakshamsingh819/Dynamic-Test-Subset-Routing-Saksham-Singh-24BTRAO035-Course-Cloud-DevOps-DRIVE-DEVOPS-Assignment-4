"""
System Smoke & Full Regression Validation Suite
Author: Saksham Singh (24BTRAO035)
Exercises all interconnected microservices in an end-to-end multi-tenant lifecycle.
"""
import pytest
from src.services.auth import AuthService
from src.services.inventory import InventoryService
from src.services.billing import BillingService
from src.services.order import OrderService, OrderStatus
from src.services.notifications import NotificationService


def test_complete_platform_workflow():
    # 1. Initialize core system services
    auth = AuthService()
    inventory = InventoryService()
    billing = BillingService(default_currency="USD", tax_rate=0.18)
    order_svc = OrderService(inventory, billing)
    notifier = NotificationService()

    # 2. Register candidate user
    user = auth.register_user("saksham.singh@devops.org", "StudentPass#2026")
    token = auth.issue_session_token(user)
    assert auth.verify_session_token(token) is True

    # 3. Provision catalog
    inventory.add_product("SKU-PRO-NODE", "Kubernetes Dedicated Node", 300.0, 5)

    # 4. Create and fulfill order
    order = order_svc.create_order(
        user_id=user.user_id,
        customer_email=user.email,
        item_requests=[{"sku": "SKU-PRO-NODE", "quantity": 1}]
    )
    assert order.status == OrderStatus.PENDING

    # 5. Process payment
    assert order_svc.process_payment(order.order_id) is True
    assert order.status == OrderStatus.PAID

    # 6. Notifications
    evt = notifier.send_email(
        recipient_email=user.email,
        subject="System Activation: Node Ready",
        message="Your dedicated cluster is now active."
    )
    assert evt.status == "delivered"
