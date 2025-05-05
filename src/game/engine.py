import logging
from typing import Generator, Tuple, Optional, List, Dict

from core.models import Character
from game.state import GameState
from game import persistence
from services import ai_narrator
from core import config

logger = logging.getLogger(__name__)


class GameEngine:
    """Orchestrates the main game flow."""

    def __init__(self):
        """Initializes the GameEngine."""
        self.game_state = GameState()
        logger.info("GameEngine initialized.")

    def start_new_game(self) -> Tuple[str, List[Dict]]:
        """
        Starts a new game, initializes the state, and returns the initial narrative.
        """
        logger.info("Starting new game...")
        self.game_state.clear()
        self.game_state.player = Character(name="Hero", hp=100, inventory=[])
        initial_prompt = "The story is initiated. Please start the story."
        self.game_state.messages = []

        if not config.is_ai_available():
            return (
                "[red]Cannot start game: AI Narrator is unavailable (missing API key).[/red]\n",
                [],
            )

        try:
            narrative, updated_messages = ai_narrator.get_ai_narrative(
                self.game_state.player,
                initial_prompt,
                list(self.game_state.messages),
            )
            self.game_state.messages = updated_messages
            return narrative, self.game_state.messages
        except Exception as e:
            logger.exception("Error during new game initialization narrative.")
            return (
                f"[bold red]Error starting game: {e}[/bold red]\n",
                self.game_state.messages,
            )

    def load_game(self) -> bool:
        """
        Loads the game state from the save file.
        Returns True if successful, False otherwise.
        """
        logger.info("Attempting to load game...")
        player, messages = persistence.load_game_state()
        if player and messages:
            self.game_state.player = player
            self.game_state.messages = messages
            logger.info("Game loaded successfully.")
            return True
        else:
            logger.warning("Failed to load game or no save file found.")
            self.game_state.clear()
            return False

    def save_game(self) -> bool:
        """
        Saves the current game state.
        Returns True if successful, False otherwise.
        """
        if not self.game_state.is_initialized():
            logger.warning("Cannot save game: Game state not initialized.")
            return False

        logger.info("Saving game state...")
        try:
            persistence.save_game_state(
                self.game_state.player, self.game_state.messages
            )
            logger.info("Game saved successfully.")
            return True
        except Exception as e:
            logger.exception("Error saving game state.")
            return False

    def process_player_action(self, action: str) -> Tuple[str, List[Dict]]:
        """
        Processes the player's action using the AI narrator and returns the narrative.
        """
        if not self.game_state.is_initialized():
            logger.error("Cannot process action: Game state not initialized.")
            return "[red]Error: Game not started or loaded.[/red]\n", []

        if not config.is_ai_available():
            return (
                "[red]Cannot process action: AI Narrator is unavailable.[/red]\n",
                self.game_state.messages,
            )

        logger.debug(f"Processing player action: {action}")
        next_prompt = f"The player chose to '{action}'. Describe what happens next."

        try:
            narrative, updated_messages = ai_narrator.get_ai_narrative(
                self.game_state.player,
                next_prompt,
                list(self.game_state.messages),
            )
            self.game_state.messages = updated_messages
            return narrative, self.game_state.messages
        except Exception as e:
            logger.exception(f"Error processing player action: {action}")
            return (
                f"[bold red]Error processing action: {e}[/bold red]\n",
                self.game_state.messages,
            )

    def get_last_message_content(self) -> Optional[str]:
        """Returns the content of the last message, if available."""
        if self.game_state.messages:
            last_msg = self.game_state.messages[-1]
            if last_msg.get("role") == "assistant":
                return last_msg.get("content", "")
            elif last_msg.get("role") == "tool":
                try:
                    content_data = json.loads(last_msg.get("content", "{}"))
                    if content_data.get("success") and content_data.get("message"):
                        return f"[italic yellow]>> {content_data['message']}[/italic yellow]"
                except json.JSONDecodeError:
                    pass
                return f"[italic dim]Tool '{last_msg.get('name', 'unknown')}' executed.[/italic dim]"
        return None

    def get_player_status(self) -> Dict:
        """Returns a dictionary describing the player's current status."""
        if not self.game_state.player:
            return {
                "name": "N/A",
                "health": "-",
                "stamina": "-",
                "money": "-",
                "inventory": [],
            }

        inventory_names = [item.name for item in self.game_state.player.inventory]

        return {
            "name": self.game_state.player.name,
            "health": self.game_state.player.hp,
            "stamina": self.game_state.player.stamina,
            "money": f"{self.game_state.player.money_oz:.2f} oz",
            "inventory": inventory_names,
        }
