"""
Inventory Management Service
Author: Saksham Singh (24BTRAO035)
Handles catalog SKU stock allocations, reservations, and inventory health alerts.
"""
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class InventoryItem:
    sku: str
    title: str
    unit_price: float
    stock_quantity: int
    reserved_quantity: int = 0
    low_stock_threshold: int = 5

    @property
    def available_quantity(self) -> int:
        return max(0, self.stock_quantity - self.reserved_quantity)

    @property
    def is_low_stock(self) -> bool:
        return self.available_quantity <= self.low_stock_threshold


class InventoryService:
    """Manages stock level checks, transactional reservations, and replenishment."""

    def __init__(self):
        self._catalog: Dict[str, InventoryItem] = {}

    def add_product(self, sku: str, title: str, unit_price: float, initial_stock: int, threshold: int = 5) -> InventoryItem:
        if unit_price <= 0:
            raise ValueError(f"Price must be strictly positive: {unit_price}")
        if initial_stock < 0:
            raise ValueError(f"Stock cannot be negative: {initial_stock}")
        sku_clean = sku.strip().upper()
        item = InventoryItem(
            sku=sku_clean,
            title=title.strip(),
            unit_price=unit_price,
            stock_quantity=initial_stock,
            low_stock_threshold=threshold
        )
        self._catalog[sku_clean] = item
        return item

    def reserve_stock(self, sku: str, quantity: int) -> bool:
        sku_clean = sku.strip().upper()
        item = self._catalog.get(sku_clean)
        if not item or quantity <= 0:
            return False
        if item.available_quantity >= quantity:
            item.reserved_quantity += quantity
            return True
        return False

    def release_reservation(self, sku: str, quantity: int) -> bool:
        sku_clean = sku.strip().upper()
        item = self._catalog.get(sku_clean)
        if not item or quantity <= 0:
            return False
        released = min(item.reserved_quantity, quantity)
        item.reserved_quantity -= released
        return True

    def commit_stock(self, sku: str, quantity: int) -> bool:
        """Deducts reserved stock upon confirmed payment."""
        sku_clean = sku.strip().upper()
        item = self._catalog.get(sku_clean)
        if not item or quantity <= 0:
            return False
        if item.reserved_quantity >= quantity and item.stock_quantity >= quantity:
            item.reserved_quantity -= quantity
            item.stock_quantity -= quantity
            return True
        return False

    def get_product(self, sku: str) -> Optional[InventoryItem]:
        return self._catalog.get(sku.strip().upper())

    def list_low_stock(self) -> Dict[str, InventoryItem]:
        return {sku: item for sku, item in self._catalog.items() if item.is_low_stock}
