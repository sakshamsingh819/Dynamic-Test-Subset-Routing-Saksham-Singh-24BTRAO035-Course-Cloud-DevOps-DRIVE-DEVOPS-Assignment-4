"""
Unit Tests for InventoryService
Author: Saksham Singh (24BTRAO035)
"""
import pytest
from src.services.inventory import InventoryService


@pytest.fixture
def inventory_service():
    svc = InventoryService()
    svc.add_product("SKU-LAPTOP-01", "Developer Workstation Pro", 1299.99, initial_stock=10, threshold=3)
    svc.add_product("SKU-MOUSE-02", "Ergonomic Optical Mouse", 49.99, initial_stock=2, threshold=5)
    return svc


def test_add_product_invalid_price(inventory_service):
    with pytest.raises(ValueError):
        inventory_service.add_product("SKU-BAD", "Bad", -10.0, 5)


def test_reserve_and_release_stock(inventory_service):
    # Available = 10
    assert inventory_service.reserve_stock("SKU-LAPTOP-01", 4) is True
    prod = inventory_service.get_product("SKU-LAPTOP-01")
    assert prod.available_quantity == 6
    assert prod.reserved_quantity == 4

    # Release 2
    assert inventory_service.release_reservation("SKU-LAPTOP-01", 2) is True
    assert prod.available_quantity == 8
    assert prod.reserved_quantity == 2


def test_reserve_excess_stock_fails(inventory_service):
    # Laptop has 10, asking for 15
    assert inventory_service.reserve_stock("SKU-LAPTOP-01", 15) is False


def test_commit_stock(inventory_service):
    inventory_service.reserve_stock("SKU-LAPTOP-01", 3)
    assert inventory_service.commit_stock("SKU-LAPTOP-01", 3) is True
    prod = inventory_service.get_product("SKU-LAPTOP-01")
    assert prod.stock_quantity == 7
    assert prod.reserved_quantity == 0


def test_low_stock_detection(inventory_service):
    # MOUSE-02 stock is 2, threshold is 5 -> low stock!
    lows = inventory_service.list_low_stock()
    assert "SKU-MOUSE-02" in lows
    assert "SKU-LAPTOP-01" not in lows
