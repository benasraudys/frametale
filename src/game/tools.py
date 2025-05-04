import logging
from core.models import Character, Item

logger = logging.getLogger(__name__)


def change_player_hp(player: Character, amount: int) -> dict[str, any]:
    """Changes the player's HP by the specified amount."""
    logger.info(f"Tool: Changing player HP by {amount}. Current HP: {player.hp}")
    player.hp += amount
    if player.hp < 0:
        player.hp = 0
    logger.info(f"Tool: New player HP: {player.hp}")
    if amount < 0:
        message = f"You took {abs(amount)} damage!"
    else:
        message = f"You healed {amount} HP."
    return {"success": True, "new_hp": player.hp, "message": message}


def add_item_to_inventory(
    player: Character, item_name: str, item_description: str, item_value: int = 0
) -> dict[str, any]:
    """Adds a new item to the player's inventory."""
    logger.info(f"Tool: Adding item '{item_name}' to player inventory.")
    new_item = Item(name=item_name, description=item_description, value=item_value)
    player.inventory.append(new_item)
    logger.info(
        f"Tool: Player inventory now contains: {[item.name for item in player.inventory]}"
    )
    message = f"You recieved: {item_name}."
    return {"success": True, "item_added": item_name, "message": message}


def change_player_stamina(player: Character, amount: int) -> dict[str, any]:
    """Changes the player's stamina by the specified amount."""
    logger.info(
        f"Tool: Changing player stamina by {amount}. Current Stamina: {player.stamina}"
    )
    player.stamina += amount
    if player.stamina < 0:
        player.stamina = 0
    logger.info(f"Tool: New player stamina: {player.stamina}")
    if amount < 0:
        message = f"You lost {abs(amount)} stamina."
    else:
        message = f"You gained {amount} stamina."
    return {"success": True, "new_stamina": player.stamina, "message": message}


def change_player_money(player: Character, amount: float) -> dict[str, any]:
    """Changes the player's money (in oz) by the specified amount."""
    logger.info(
        f"Tool: Changing player money by {amount} oz. Current Money: {player.money_oz}"
    )
    player.money_oz += amount
    if player.money_oz < 0:
        player.money_oz = 0.0
    logger.info(f"Tool: New player money: {player.money_oz} oz")
    if amount < 0:
        message = f"You lost {abs(amount):.2f} oz of money."
    else:
        message = f"You gained {amount:.2f} oz of money."
    return {"success": True, "new_money_oz": player.money_oz, "message": message}


def remove_item_from_inventory(player: Character, item_name: str) -> dict[str, any]:
    """Removes an item from the player's inventory by name."""
    logger.info(f"Tool: Attempting to remove item '{item_name}' from player inventory.")
    initial_inventory_size = len(player.inventory)
    player.inventory = [
        item for item in player.inventory if item.name.lower() != item_name.lower()
    ]
    if len(player.inventory) < initial_inventory_size:
        logger.info(f"Tool: Item '{item_name}' removed successfully.")
        message = f"'{item_name}' has been removed from your inventory."
        return {"success": True, "item_removed": item_name, "message": message}
    else:
        logger.warning(f"Tool: Item '{item_name}' not found in player inventory.")
        message = f"'{item_name}' was not found in your inventory."
        return {"success": False, "item_removed": None, "message": message}


def modify_item_in_inventory(
    player: Character,
    item_name: str,
    new_description: str = None,
    new_value: int = None,
) -> dict[str, any]:
    """Modifies an item in the player's inventory by name."""
    logger.info(f"Tool: Attempting to modify item '{item_name}' in player inventory.")
    for item in player.inventory:
        if item.name.lower() == item_name.lower():
            if new_description is not None:
                item.description = new_description
                logger.info(f"Tool: Updated description for '{item_name}'.")
            if new_value is not None:
                item.value = new_value
                logger.info(f"Tool: Updated value for '{item_name}'.")
            message = f"'{item_name}' has been updated."
            return {"success": True, "item_modified": item_name, "message": message}
    logger.warning(
        f"Tool: Item '{item_name}' not found in player inventory for modification."
    )
    message = f"'{item_name}' was not found in your inventory."
    return {"success": False, "item_modified": None, "message": message}


TOOL_MAPPING = {
    "change_player_hp": change_player_hp,
    "add_item_to_inventory": add_item_to_inventory,
    "remove_item_from_inventory": remove_item_from_inventory,
    "modify_item_in_inventory": modify_item_in_inventory,
    "change_player_stamina": change_player_stamina,
    "change_player_money": change_player_money,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "change_player_hp",
            "description": "Modify the player character's health points (HP). Use negative values to decrease HP (damage) and positive values to increase HP (healing).",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "integer",
                        "description": "The amount to change the player's HP by (positive for healing, negative for damage).",
                    }
                },
                "required": ["amount"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_item_to_inventory",
            "description": "Add an item to the player character's inventory.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "The name of the item to add.",
                    },
                    "item_description": {
                        "type": "string",
                        "description": "A brief description of the item.",
                    },
                    "item_value": {
                        "type": "integer",
                        "description": "The value of the item (optional, defaults to 0).",
                    },
                },
                "required": ["item_name", "item_description"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_item_from_inventory",
            "description": "Remove an item from the player character's inventory by name.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "The name of the item to remove.",
                    }
                },
                "required": ["item_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "modify_item_in_inventory",
            "description": "Modify an existing item in the player character's inventory by name. You can update its description and/or value.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item_name": {
                        "type": "string",
                        "description": "The name of the item to modify.",
                    },
                    "new_description": {
                        "type": "string",
                        "description": "The new description for the item (optional).",
                    },
                    "new_value": {
                        "type": "integer",
                        "description": "The new value for the item (optional).",
                    },
                },
                "required": ["item_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "change_player_stamina",
            "description": "Modify the player character's stamina. Use negative values to decrease stamina and positive values to increase stamina.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "integer",
                        "description": "The amount to change the player's stamina by (positive for gain, negative for loss).",
                    }
                },
                "required": ["amount"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "change_player_money",
            "description": "Modify the player character's money in ounces (oz). Use negative values to decrease money and positive values to increase money.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {
                        "type": "number",
                        "description": "The amount to change the player's money by in ounces (positive for gain, negative for loss).",
                    }
                },
                "required": ["amount"],
            },
        },
    },
]
