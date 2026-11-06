from contextlib import redirect_stdout
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from digital_product import DigitalProduct
from file_handling import load_inventory, save_inventory
from inventory import Inventory
from main import show_product_details
from order import Order
from physical_product import PhysicalProduct
from supplier import Supplier


class Lab8Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.supplier = Supplier("S001", "Tech Supplies", "tech@example.com")
        self.physical = PhysicalProduct("P001", "Laptop", 1200, 15, 2.4, self.supplier)
        self.digital = DigitalProduct("P002", "E-book", 30, 100, 25.0, self.supplier)

    def test_supplier_association_survives_deleting_variable(self) -> None:
        supplier = Supplier("S002", "Books Vendor", "books@example.com")
        product = DigitalProduct("P003", "Guide", 12, 20, 5, supplier)
        del supplier
        self.assertEqual(product.supplier.name, "Books Vendor")
        with redirect_stdout(StringIO()) as out:
            product.supplier.display_information()
        self.assertIn("Books Vendor", out.getvalue())

    def test_aggregation_allows_transfer_without_destruction(self) -> None:
        first, second = Inventory(), Inventory()
        first.add_product(self.physical)
        self.assertIs(first.find_product("p001"), self.physical)
        self.assertTrue(first.remove_product("P001"))
        self.assertIsNone(first.find_product("P001"))
        self.assertEqual(self.physical.name, "Laptop")
        second.add_product(self.physical)
        self.assertIs(second.find_product("P001"), self.physical)

    def test_find_and_remove_missing_product(self) -> None:
        inventory = Inventory()
        self.assertIsNone(inventory.find_product("MISSING"))
        self.assertFalse(inventory.remove_product("MISSING"))

    def test_order_composition_totals_and_identity(self) -> None:
        one, two = Order("O001"), Order("O002")
        one.add_order_line(self.physical, 2)
        one.add_order_line(self.digital, 1)
        two.add_order_line(self.physical, 1)
        self.assertAlmostEqual(one.calculate_total(), 2430.0)
        self.assertIsNot(one.order_lines[0], two.order_lines[0])
        self.assertIs(one.order_lines[0].product, two.order_lines[0].product)
        self.assertTrue(one.remove_order_line(1))
        self.assertAlmostEqual(one.calculate_total(), 30.0)
        one.cancel()
        self.assertEqual(len(one.order_lines), 0)
        self.assertEqual(self.physical.name, "Laptop")

    def test_subclass_lsp_stock_contract(self) -> None:
        for product in (self.physical, self.digital):
            product.update_stock(42)
            self.assertEqual(product.stock, 42)
            self.assertIsInstance(product.get_fulfilment_info(), str)
            with self.assertRaises(ValueError):
                product.update_stock(-1)

    def test_polymorphic_collection_and_common_function(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)
        with redirect_stdout(StringIO()) as output:
            for product in inventory.products:
                show_product_details(product)
            inventory.display_all_products()
        text = output.getvalue()
        self.assertIn("physical shipping", text)
        self.assertIn("delivered digitally", text)
        self.assertIn("Laptop", text)
        self.assertIn("E-book", text)

    def test_supplier_saved_and_reused_after_loading(self) -> None:
        inventory = Inventory()
        inventory.add_product(self.physical)
        inventory.add_product(self.digital)
        with TemporaryDirectory() as folder:
            location = Path(folder) / "products.json"
            save_inventory(inventory, location)
            loaded = load_inventory(location)
            loaded_physical = loaded.find_product("P001")
            loaded_digital = loaded.find_product("P002")
            self.assertIsNotNone(loaded_physical)
            self.assertIsNotNone(loaded_digital)
            self.assertIs(loaded_physical.supplier, loaded_digital.supplier)
            self.assertEqual(loaded_physical.supplier.contact_email, "tech@example.com")

    def test_old_lab7_json_loads_with_placeholder_supplier(self) -> None:
        old_data = [{"product_id": "P001", "name": "Laptop", "price": 1200,
                     "stock": 15, "type": "physical", "weight": 2.4}]
        with TemporaryDirectory() as folder:
            location = Path(folder) / "legacy.json"
            location.write_text(json.dumps(old_data), encoding="utf-8")
            loaded = load_inventory(location)
            self.assertEqual(loaded.find_product("P001").supplier.supplier_id, "S-UNKNOWN")

    def test_validation_and_private_product_price(self) -> None:
        self.assertAlmostEqual(self.physical.price, 1200.0)
        with self.assertRaises(TypeError):
            PhysicalProduct("P002", "Mouse", 20, 4, 1.0, "Company")
        with self.assertRaises(ValueError):
            Order("O1").add_order_line(self.physical, 0)
        with self.assertRaises(ValueError):
            self.physical.update_stock(-100)


if __name__ == "__main__":
    unittest.main()
