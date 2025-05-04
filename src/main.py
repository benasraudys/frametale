import logging
import os
from ui.menu import display_main_menu
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


def main():
    """Main function to run the game menu and handle choices."""
    engine = GameEngine()
    os.system("clear")
    try:
        while True:
            choice = display_main_menu()

            if choice == "1":
                logger.info("Starting new game...")
                os.system("clear")
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
                    os.system("clear")
                    print(
                        "[red]Failed to initialize new game state. Returning to menu.[/red]"
                    )

            elif choice == "2":
                logger.info("Attempting to continue game...")
                if engine.load_game():
                    os.system("clear")
                    logger.info("Loaded game state successfully.")
                    run_game_loop(engine)
                else:
                    logger.warning(
                        "Could not load game. No save file found or file is invalid."
                    )
                    os.system("clear")
                    print("\n[yellow]No game save available.[/yellow]")

            elif choice == "3":
                os.system("clear")
                print("Exiting game. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    except KeyboardInterrupt:
        logger.info("Game interrupted by user (Ctrl+C). Exiting gracefully.")
        os.system("clear")
        print("\nExiting game. Goodbye!")


if __name__ == "__main__":
    logger.info("Starting game application.")
    try:
        main()
    except Exception as e:
        logger.exception("An unhandled exception occurred.")
    logger.info("Exiting game application.")
