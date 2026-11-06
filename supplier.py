class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if not isinstance(supplier_id, str) or not supplier_id.strip():
            raise ValueError("Supplier ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Supplier name cannot be empty.")
        if not isinstance(contact_email, str) or "@" not in contact_email or not contact_email.strip():
            raise ValueError("Please enter a valid supplier email address.")

        self.supplier_id: str = supplier_id.strip()
        self.name: str = name.strip()
        self.contact_email: str = contact_email.strip()

    def display_information(self) -> None:
        print(f"Supplier ID: {self.supplier_id}")
        print(f"Supplier Name: {self.name}")
        print(f"Contact Email: {self.contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email,
        }
