from product import Product


class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("Order line must refer to a Product object.")
        if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
            raise ValueError("Order quantity must be a positive whole number.")
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity
