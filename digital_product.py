import math
from product import Product
from supplier import Supplier


class DigitalProduct(Product):

    def __init__(
        self, product_id: str, name: str, price: float, stock: int,
        download_size: float, supplier: Supplier,
    ) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        if (
            not isinstance(download_size, (int, float))
            or isinstance(download_size, bool)
            or not math.isfinite(download_size)
            or download_size < 0
        ):
            raise ValueError("Download size must be a non-negative number.")
        self.__download_size: float = float(download_size)

    @property
    def download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"           Download size: {self.__download_size:.2f} MB")

    def get_fulfilment_info(self) -> str:
        return "This product is delivered digitally."

    def to_dict(self) -> dict[str, object]:
        data = super().to_dict()
        data.update({"type": "digital", "download_size": self.__download_size})
        return data
