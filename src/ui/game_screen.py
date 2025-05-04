# ui/game_screen.py

import os
import sys
import logging
import time
import random
from typing import Generator, List, Dict, Optional, Tuple

from game.engine import GameEngine

logger = logging.getLogger(__name__)


def _type_out(text: str):
    for char in text:
        print(char, end="", flush=True)
        if char == "\n":
            time.sleep(0.7)
        elif char == ".":
            time.sleep(0.5)
        elif char == ",":
            time.sleep(0.2)
        elif char == " ":
            time.sleep(0.01)
        else:
            time.sleep(random.uniform(0.0, random.uniform(0.0, 0.2)))
    print()


def run_game_loop(engine: GameEngine) -> None:
    """
    Runs the main game loop using stdin/stdout, interacting with the GameEngine.

    Args:
        engine: The initialized GameEngine instance.
    """
    if not engine.game_state.is_initialized():
        logger.error("Game loop started with uninitialized engine.")
        print("❌ [red]Error: Game engine not ready. Cannot start loop.[/red]")
        return

    while True:
        try:
            os.system("clear")

            print("\n═══════════════ Narrative ═══════════════")
            print("\033[0m")
            last_narrative = engine.get_last_message_content()
            if last_narrative:
                _type_out(last_narrative.strip())
            else:
                print("❌ Couldn't get narrative.")
            print("\033[0m")
            print("\n═════════════ Player Status ═════════════")
            print(engine.get_player_status())
            print("═══════════════════════════════════════════")
            action = input("\n🎮 Your action (or 'quit'): ").strip()

            if not action:
                continue

            if action.lower() == "quit":
                os.system("clear")
                print("\n💾 Attempting to save game before exiting...")
                if engine.save_game():
                    print("✅ Game saved successfully.")
                else:
                    print("⚠️ [yellow]Warning: Failed to save game state.[/yellow]")
                print("👋 Exiting game.")
                break

            os.system("clear")
            print("\n🧭 Loading...")
            logger.debug(f"Processing action: {action}")
            narrative, _ = engine.process_player_action(action)

            if narrative:
                print(narrative.strip())
            else:
                print("📭 (No narrative generated for this action)")
            print("═══════════════════════════════════════════")

            if engine.save_game():
                logger.info(f"Game state saved after action: '{action}'")
            else:
                logger.warning(f"Failed to save game state after action: '{action}'")
                print(
                    "⚠️ [yellow]Warning: Could not save game progress after last action.[/yellow]"
                )

        except (KeyboardInterrupt, EOFError):
            os.system("clear")
            print("\n🛑 Interrupted. Attempting to save game before exiting...")
            if engine.save_game():
                print("✅ Game saved successfully.")
            else:
                print("⚠️ [yellow]Warning: Failed to save game state on exit.[/yellow]")
            print("👋 Exiting game.")
            break
        except Exception as e:
            logger.exception("An unexpected error occurred in the game loop.")
            print(
                f"\n💥 [bold red]An unexpected error occurred: {e}. Exiting without saving.[/bold red]"
            )
            break
