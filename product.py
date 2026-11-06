\
from abc import ABC, abstractmethod
from supplier import Supplier


class Product(ABC):
    def __init__(
        self, product_id: str, name: str, price: float, stock: int,
        supplier: Supplier,
    ) -> None:
        if not isinstance(product_id, str) or not product_id.strip():
            raise ValueError("Product ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Product name cannot be empty.")
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if not isinstance(stock, int) or isinstance(stock, bool) or stock < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        if not isinstance(supplier, Supplier):
            raise TypeError("Supplier must be a Supplier object.")

        self.__product_id: str = product_id.strip()
        self.__name: str = name.strip()
        self.__price: float = float(price)
        self.__stock: int = stock
        self.supplier: Supplier = supplier  # association: supplier owns its own lifecycle

    @property
    def product_id(self) -> str:
        return self.__product_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def price(self) -> float:
        """Read-only price used by OrderLine.calculate_subtotal()."""
        return self.__price

    @property
    def stock(self) -> int:
        return self.__stock

    def update_stock(self, quantity: int) -> None:
        """Set the stock quantity to a new non-negative total (both subclasses)."""
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity < 0:
            raise ValueError("Stock must be a non-negative whole number.")
        self.__stock = quantity

    def display_information(self) -> None:
        print(f"{self.__product_id:<10} {self.__name:<20} ${self.__price:>10.2f} {self.__stock:>8}")
        print(f"           Supplier: {self.supplier.name} ({self.supplier.supplier_id})")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Return how this product is fulfilled."""
        raise NotImplementedError

    def to_dict(self) -> dict[str, object]:
        """Return JSON-serializable data, including the associated supplier."""
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.supplier.to_dict(),
        }
