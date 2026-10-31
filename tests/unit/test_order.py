"""
Unit Tests for OrderService
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.services.order import OrderService, OrderStatus
from src.services.billing import BillingService
from src.services.inventory import InventoryService


@pytest.fixture
def order_fixture():
    inv_svc = InventoryService()
    inv_svc.add_product("SKU-SERVER", "Enterprise Compute Node", 500.0, initial_stock=5)
    bill_svc = BillingService(default_currency="USD", tax_rate=0.18)
    order_svc = OrderService(inv_svc, bill_svc)
    return order_svc, inv_svc, bill_svc


def test_create_order_success(order_fixture):
    order_svc, inv_svc, bill_svc = order_fixture
    order = order_svc.create_order(
        user_id="usr_0001",
        customer_email="saksham@devops.org",
        item_requests=[{"sku": "SKU-SERVER", "quantity": 2}]
    )
    assert order.order_id.startswith("ORD-")
    assert order.status == OrderStatus.PENDING
    assert order.total_amount > 0

    # Stock should be reserved
    prod = inv_svc.get_product("SKU-SERVER")
    assert prod.reserved_quantity == 2
    assert prod.available_quantity == 3


def test_create_order_insufficient_stock(order_fixture):
    order_svc, inv_svc, bill_svc = order_fixture
    with pytest.raises(ValueError, match="Insufficient stock"):
        order_svc.create_order(
            user_id="usr_0001",
            customer_email="saksham@devops.org",
            item_requests=[{"sku": "SKU-SERVER", "quantity": 10}]
        )


def test_process_payment_flow(order_fixture):
    order_svc, inv_svc, bill_svc = order_fixture
    order = order_svc.create_order(
        user_id="usr_0001",
        customer_email="saksham@devops.org",
        item_requests=[{"sku": "SKU-SERVER", "quantity": 1}]
    )
    assert order_svc.process_payment(order.order_id) is True
    assert order.status == OrderStatus.PAID
    prod = inv_svc.get_product("SKU-SERVER")
    assert prod.stock_quantity == 4
    assert prod.reserved_quantity == 0


def test_cancel_order_releases_stock(order_fixture):
    order_svc, inv_svc, bill_svc = order_fixture
    order = order_svc.create_order(
        user_id="usr_0001",
        customer_email="saksham@devops.org",
        item_requests=[{"sku": "SKU-SERVER", "quantity": 2}]
    )
    assert order_svc.cancel_order(order.order_id) is True
    assert order.status == OrderStatus.CANCELLED
    prod = inv_svc.get_product("SKU-SERVER")
    assert prod.reserved_quantity == 0
    assert prod.available_quantity == 5
