from typing import List, Dict, Optional
from dataclasses import dataclass, field

from core.models import Character


@dataclass
class GameState:
    """Represents the current state of the game."""

    player: Optional[Character] = None
    messages: List[Dict] = field(default_factory=list)

    def is_initialized(self) -> bool:
        """Checks if the game state has a player character."""
        return self.player is not None

    def clear(self):
        """Resets the game state."""
        self.player = None
        self.messages = []
