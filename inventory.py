from product import Product


class Inventory:

    def __init__(self) -> None:
        self.__products: list[Product] = []

    @property
    def products(self) -> list[Product]:

        return self.__products.copy()

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError("Only Product objects can be added.")
        if self.find_product(product.product_id) is not None:
            raise ValueError("A product with this ID already exists.")
        self.__products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.product_id.lower() == product_id.strip().lower():
                return product
        return None

    def search_product(self, product_id: str) -> Product | None:
        return self.find_product(product_id)

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def display_all(self) -> None:
        if not self.__products:
            print("No products in inventory.")
            return
        print(f"{'ID':<10} {'Name':<20} {'Price':>11} {'Stock':>8}")
        print("-" * 53)
        for product in self.__products:
            product.display_information()

    def display_all_products(self) -> None:
        self.display_all()

    def get_products(self) -> list[Product]:
        return self.__products.copy()
