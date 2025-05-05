import logging
import sys
import customtkinter as ctk

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MainMenuGUI(ctk.CTk):
    """Main menu window for the FrameTale game."""

    def __init__(self):
        super().__init__()

        # --- Configuration ---
        ctk.DrawEngine.preferred_drawing_method = "circle_shapes"
        ctk.set_appearance_mode("Dark")
        self.title("FrameTale")
        self.geometry("600x500")  # Larger window

        # Consistent styling from previous GameScreen
        self.border_thickness = 3
        self.panel_corner_radius = 8
        self.widget_corner_radius = 8
        self.font_size_normal = 16
        self.font_size_large = 24
        self.button_width = 250  # Consistent button width
        self.button_height = 50  # Consistent button height

        # --- Grid Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)  # Main panel takes full weight

        # --- Create Panels ---
        self._create_main_panel()

        # Tracking user choice
        self.choice = None

    def _create_main_panel(self):
        """Creates the main menu panel with game options."""
        main_panel = ctk.CTkFrame(
            self,
            corner_radius=self.panel_corner_radius,
            border_width=self.border_thickness,
        )
        main_panel.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")

        # Configure panel grid
        main_panel.grid_columnconfigure(0, weight=1)
        main_panel.grid_rowconfigure((0, 1, 2, 3, 4), weight=1)

        # Title Label
        title_label = ctk.CTkLabel(
            main_panel,
            text="FrameTale",
            font=ctk.CTkFont(size=self.font_size_large, weight="bold"),
        )
        title_label.grid(row=0, column=0, padx=20, pady=20)

        # Buttons with consistent styling
        button_font = ctk.CTkFont(size=self.font_size_normal)

        # New Game Button
        new_game_button = ctk.CTkButton(
            main_panel,
            text="New Game",
            command=self.new_game,
            width=self.button_width,
            height=self.button_height,
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
            font=button_font,
        )
        new_game_button.grid(row=1, column=0, padx=20, pady=10)

        # Continue Game Button
        continue_game_button = ctk.CTkButton(
            main_panel,
            text="Continue Game",
            command=self.continue_game,
            width=self.button_width,
            height=self.button_height,
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
            font=button_font,
        )
        continue_game_button.grid(row=2, column=0, padx=20, pady=10)

        # Settings Button
        settings_button = ctk.CTkButton(
            main_panel,
            text="Settings",
            command=self.open_settings,
            width=self.button_width,
            height=self.button_height,
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
            font=button_font,
        )
        settings_button.grid(row=3, column=0, padx=20, pady=10)

        # Exit Button inside the main panel
        exit_button = ctk.CTkButton(
            main_panel,
            text="Exit",
            command=self.exit_game,
            height=40,
            width=80,
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
            font=ctk.CTkFont(size=self.font_size_normal - 2),
            fg_color=("#E74C3C", "#C0392B"),
            hover_color=("#C0392B", "#A93226"),
        )
        exit_button.grid(row=4, column=0, padx=20, pady=20, sticky="se")

    # --- Menu Action Handlers ---

    def new_game(self):
        """Handle new game selection."""
        logger.info("New Game selected")
        self.choice = "1"
        self.destroy()

    def continue_game(self):
        """Handle continue game selection."""
        logger.info("Continue Game selected")
        self.choice = "2"
        self.destroy()

    def open_settings(self):
        """Placeholder for settings menu."""
        logger.info("Settings selected")
        self.choice = "3"
        # TODO: Implement settings menu
        # For now, it just logs and closes

    def exit_game(self):
        """Handle game exit."""
        logger.info("Exit selected")
        self.choice = "4"
        self.destroy()

    def get_choice(self):
        """Run the main loop and return user's choice."""
        logger.info("Entering main menu loop")
        self.mainloop()
        return self.choice
