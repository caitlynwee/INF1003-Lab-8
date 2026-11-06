import json
from pathlib import Path
from inventory import Inventory
from digital_product import DigitalProduct
from physical_product import PhysicalProduct
from supplier import Supplier

DATA_FILE = Path(__file__).with_name("inventory.json")


def save_inventory(inventory: Inventory, filename: str | Path = DATA_FILE) -> None:
    products = [product.to_dict() for product in inventory.get_products()]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(products, file, indent=4)


def load_inventory(filename: str | Path = DATA_FILE) -> Inventory:
    inventory = Inventory()
    if not Path(filename).exists():
        return inventory

    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("Inventory JSON must contain a list of products.")

    # Reuse supplier instances when multiple products reference the same ID.
    suppliers: dict[str, Supplier] = {}
    for item in data:
        product_type = item.get("type")
        product_class = {
            "physical": PhysicalProduct,
            "digital": DigitalProduct,
        }.get(product_type)
        if product_class is None:
            raise ValueError(f"Unknown product type: {product_type!r}.")

        supplier_data = item.get("supplier")
        if supplier_data is None:
            supplier_data = {
                "supplier_id": "S-UNKNOWN",
                "name": "Supplier not recorded (Lab 7 data)",
                "contact_email": "unknown@example.invalid",
            }
        supplier_id = supplier_data["supplier_id"]
        if supplier_id not in suppliers:
            suppliers[supplier_id] = Supplier(
                supplier_id,
                supplier_data["name"],
                supplier_data["contact_email"],
            )
        else:
            if suppliers[supplier_id].to_dict() != supplier_data:
                raise ValueError(f"Conflicting supplier details for {supplier_id}.")

        extra_field = "weight" if product_type == "physical" else "download_size"
        inventory.add_product(product_class(
            item["product_id"], item["name"], item["price"],
            item["stock"], item[extra_field], suppliers[supplier_id],
        ))
    return inventory
