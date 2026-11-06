"""Run this script to demonstrate every Lab 8 relationship in one screenshot."""

from digital_product import DigitalProduct
from inventory import Inventory
from main import show_product_details
from order import Order
from physical_product import PhysicalProduct
from supplier import Supplier


def main() -> None:
    print("=== SECTION 2: ASSOCIATION — Supplier and Product ===")
    supplier = Supplier("S001", "Tech Supplier", "contact@tech.example")
    laptop = PhysicalProduct("P001", "Laptop", 1200, 5, 2.4, supplier)
    ebook = DigitalProduct("P002", "Python E-book", 30, 50, 15, supplier)
    print("Both products share the same Supplier object:", laptop.supplier is ebook.supplier)
    del supplier
    print("After del supplier, laptop still knows its supplier:")
    laptop.supplier.display_information()

    print("\n=== SECTION 3: AGGREGATION — Inventory and Product ===")
    inventory_a = Inventory()
    inventory_b = Inventory()
    inventory_a.add_product(laptop)
    print("Laptop in Inventory A:", inventory_a.find_product("P001") is laptop)
    inventory_a.remove_product("P001")
    print("Removed from A; product still works:", laptop.name)
    inventory_b.add_product(laptop)
    print("Same laptop object added to B:", inventory_b.find_product("P001") is laptop)

    print("\n=== SECTION 4: COMPOSITION — Order and OrderLine ===")
    order_a = Order("O001")
    order_a.add_order_line(laptop, 2)
    order_a.add_order_line(ebook, 1)
    order_a.display_information()
    order_b = Order("O002")
    order_b.add_order_line(laptop, 1)
    print("Two orders create distinct order lines:", order_a.order_lines[0] is not order_b.order_lines[0])
    print("The order lines reference the same Product:", order_a.order_lines[0].product is order_b.order_lines[0].product)
    order_b.cancel()
    print("Cancelled order has 0 order lines:", len(order_b.order_lines) == 0)

    print("\n=== SECTIONS 6-7: LSP and POLYMORPHISM ===")
    inventory_b.add_product(ebook)
    for product in inventory_b.products:  # a list[Product], with both subclasses
        show_product_details(product)
        product.update_stock(10)
        print("           Updated stock:", product.stock)


if __name__ == "__main__":
    main()
