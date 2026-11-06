from abc import ABC, abstractmethod


class CanBeShipped(ABC):

    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculate the cost to ship this item."""
        raise NotImplementedError
