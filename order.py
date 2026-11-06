from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str) -> None:
        if not isinstance(order_id, str) or not order_id.strip():
            raise ValueError("Order ID cannot be empty.")
        self.order_id: str = order_id.strip()
        self.__order_lines: list[OrderLine] = []

    @property
    def order_lines(self) -> tuple[OrderLine, ...]:
        return tuple(self.__order_lines)

    def add_order_line(self, product: Product, quantity: int) -> None:
        # Composition: the owning Order creates the OrderLine internally.
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, line_number: int) -> bool:
        if not isinstance(line_number, int) or isinstance(line_number, bool):
            return False
        if not 1 <= line_number <= len(self.__order_lines):
            return False
        self.__order_lines.pop(line_number - 1)
        return True

    def cancel(self) -> None:
        self.__order_lines.clear()

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def display_information(self) -> None:
        print(f"Order ID: {self.order_id}")
        if not self.__order_lines:
            print("This order has no lines.")
        for number, line in enumerate(self.__order_lines, 1):
            print(f"  {number}. {line.product.name}: {line.quantity} × "
                  f"${line.product.price:.2f} = ${line.calculate_subtotal():.2f}")
        print(f"Order total: ${self.calculate_total():.2f}")
