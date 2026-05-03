from typing import Any


class CartManager:
    _instance: "CartManager | None" = None

    cart: list[dict[str, Any]]


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.cart = []
        return cls._instance


    def __init__(self) -> None:
        # Make basedpyright happy
        if not hasattr(self, "cart"):
            self.cart = []


    def get(self) -> list[dict[str, Any]]:
        return self.cart


    def add(self, item: dict[str, Any]):
        self.cart.append(item)


    def clear(self):
        self.cart.clear()


    def remove_index(self, index: int):
        if 0 <= index < len(self.cart):
            self.cart.pop(index)


    def find_by_name(self, name: str) -> dict[str, Any] | None:
        for item in self.cart:
            if item["name"] == name:
                return item

        return None