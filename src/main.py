#!/usr/bin/env python

import logging
import os
from ui.menu import MainMenuGUI
from game.engine import GameEngine
from ui.game_screen import run_game_loop
from core import config

if not os.path.exists(config.LOG_DIR):
    os.makedirs(config.LOG_DIR)

LOG_FILE = os.path.join(config.LOG_DIR, "latest.log")

logging.basicConfig(
    level=logging.DEBUG,  # Capture all debug messages
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w"),  # Log to file
        # If you want some level of logging to console uncomment below
        # logging.StreamHandler() # Log to console (stdout) - default level is WARNING
    ],
)
# Optional: Set console handler to a higher level if uncommented
# console_handler = next((h for h in logging.root.handlers if isinstance(h, logging.StreamHandler)), None)
# if console_handler:
#    console_handler.setLevel(logging.INFO) # Only show INFO and above on console

logger = logging.getLogger(__name__)
logger.info("Initialized logger.")


def main():
    """Main function to run the game menu and handle choices."""
    engine = GameEngine()
    try:
        menu = MainMenuGUI()
        choice = menu.get_choice()

        if choice == "1":
            logger.info("Starting new game...")
            print("\n🧭 Loading...")
            engine.start_new_game()
            if engine.save_game():
                logger.debug("Saved game state after initial narrative.")
            else:
                logger.warning("Failed to save initial game state.")

            if engine.game_state.is_initialized():
                run_game_loop(engine)
            else:
                logger.error("Engine state not initialized after start_new_game.")
                print("Failed to initialize new game state. Returning to menu.")

        elif choice == "2":
            logger.info("Attempting to continue game...")
            if engine.load_game():
                logger.info("Loaded game state successfully.")
                run_game_loop(engine)
            else:
                logger.warning(
                    "Could not load game. No save file found or file is invalid."
                )
                print("\nNo game save available.")

        elif choice == "3":
            print("Exiting game. Goodbye!")
            # No break needed as there's no loop

    except KeyboardInterrupt:
        logger.info("Game interrupted by user (Ctrl+C). Exiting gracefully.")
        print("\nExiting game. Goodbye!")


if __name__ == "__main__":
    logger.info("Starting game application.")
    try:
        main()
    except Exception as e:
        logger.exception("An unhandled exception occurred.")
    logger.info("Exiting game application.")
