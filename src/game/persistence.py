import os
import json
import logging
from typing import Optional, List, Dict, Tuple

from core.models import Character
from core import config

logger = logging.getLogger(__name__)


def save_game_state(
    player: Character, messages: List[Dict], save_path: str = config.SAVE_FILE_PATH
):
    """Saves the current game state (player and messages) to a JSON file."""
    try:
        game_state = {"player": player.to_dict(), "messages": messages}
        save_dir = os.path.dirname(save_path)
        if save_dir and not os.path.exists(save_dir):
            os.makedirs(save_dir)
            logger.info(f"Created save directory: {save_dir}")

        with open(save_path, "w") as f:
            json.dump(game_state, f, indent=4)
        logger.info(f"Game state saved successfully to {save_path}")
    except IOError as e:
        logger.error(f"Error saving game state to {save_path}: {e}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred during saving: {e}")


def load_game_state(
    save_path: str = config.SAVE_FILE_PATH,
) -> Tuple[Optional[Character], Optional[List[Dict]]]:
    """Loads the game state from a JSON file."""
    if not os.path.exists(save_path):
        logger.info(f"No save file found at {save_path}. Cannot load game.")
        return None, None
    try:
        with open(save_path, "r") as f:
            game_state = json.load(f)
        player_data = game_state.get("player")
        messages = game_state.get("messages")
        if not player_data or not isinstance(messages, list):
            logger.error(
                f"Invalid save file format in {save_path}. Missing 'player' or 'messages' (must be a list)."
            )
            return None, None

        player = Character.from_dict(player_data)
        logger.info(f"Game state loaded successfully from {save_path}")
        return player, messages
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from save file {save_path}: {e}")
        return None, None
    except IOError as e:
        logger.error(f"Error reading save file {save_path}: {e}")
        return None, None
    except Exception as e:
        logger.exception(f"An unexpected error occurred during loading: {e}")
        return None, None
