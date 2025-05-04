class Item:
    """Represents an item in the game."""

    def __init__(
        self, name: str, description: str, value: int = 0, properties: dict = None
    ):
        self.name = name
        self.description = description
        self.value = value
        self.properties = properties if properties is not None else {}

    def to_dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class Character:
    """Represents a character in the game."""

    def __init__(
        self,
        name: str,
        hp: int,
        stamina: int = 100,
        money_oz: float = 0.0,
        inventory: list = None,
        location: str = "",
    ):
        self.name = name
        self.hp = hp
        self.stamina = stamina
        self.money_oz = money_oz
        self.inventory = inventory if inventory is not None else []
        self.location = location

    def to_dict(self):
        return {
            "name": self.name,
            "hp": self.hp,
            "stamina": self.stamina,
            "money_oz": self.money_oz,
            "inventory": [item.to_dict() for item in self.inventory],
            "location": self.location,
        }

    @classmethod
    def from_dict(cls, data):
        data["inventory"] = [
            Item.from_dict(item_data) for item_data in data.get("inventory", [])
        ]
        data["stamina"] = data.get("stamina", 100)
        data["money_oz"] = data.get("money_oz", 0.0)
        return cls(**data)


class Location:
    """Represents a location in the game world."""

    def __init__(
        self, name: str, description: str, exits: dict = None, items: list = None
    ):
        self.name = name
        self.description = description
        self.exits = exits if exits is not None else {}
        self.items = items if items is not None else []


# Example
# wooden_sword = Item("Wooden Sword", "A simple wooden sword.", value=10)
# player = Character("Hero", 100, inventory=[wooden_sword], location="Town Square")
# town_square = Location("Town Square", "A bustling town square.", exits={"north": "Market"}, items=[wooden_sword])
