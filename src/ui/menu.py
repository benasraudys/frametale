def display_main_menu() -> str:
    """Displays the main menu using stdin/stdout and returns the user's choice."""
    print("╔══════════════════════════════╗")
    print("║       ✨ FrameTale ✨        ║")
    print("╠══════════════════════════════╣")
    print("║  1. 🗡️   New Game             ║")
    print("║  2. 💾  Continue Game        ║")
    print("║  3. ❌  Exit                 ║")
    print("╚══════════════════════════════╝")

    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
