import logging
import customtkinter as ctk

from game.engine import GameEngine

from .narrative_typer import NarrativeTyper

logger = logging.getLogger(__name__)


class GameScreen(ctk.CTk):
    """Main application window for the FrameTale game."""

    def __init__(self, engine: GameEngine):
        super().__init__()

        self.engine = engine

        # --- Configuration ---
        ctk.DrawEngine.preferred_drawing_method = "circle_shapes"
        ctk.set_appearance_mode("Dark")
        self.title("FrameTale")
        self.geometry("1200x1000")  # Adjust size as needed

        # Consistent border thickness
        self.border_thickness = 3
        self.panel_corner_radius = 8
        self.widget_corner_radius = 8
        self.font_size_normal = 16
        self.font_size_large = 24

        # --- Grid Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Header
        self.grid_rowconfigure(1, weight=0)  # Status Panels (New Position)
        self.grid_rowconfigure(2, weight=1)  # Narrative content
        self.grid_rowconfigure(3, weight=0)  # Input
        self.grid_rowconfigure(4, weight=0)  # Bottom Buttons (Quit)

        # --- UI Element Creation ---
        self._create_header()
        self._create_status_panels()  # Create status panels before narrative
        self._create_narrative_panel()
        self._create_input_panel()
        self._create_bottom_panel()

        # --- Narrative Typer ---
        self.narrative_typer = NarrativeTyper(self.narrative_textbox, self)

        # --- Initial State Update ---
        self.update_player_status()  # Update status immediately
        # Start initial narrative typing
        initial_narrative = self.engine.get_last_message_content()
        if initial_narrative:
            self.narrative_typer.type_out(initial_narrative)
        else:
            self.narrative_typer.type_out("Welcome! Your story awaits...")

        # --- Bind Close Event ---
        self.protocol(
            "WM_DELETE_WINDOW", self.quit_game
        )  # Handle window close ('X') button

    # --- UI Creation Methods ---

    def _create_header(self):
        """Creates the header panel and label."""
        header_panel = ctk.CTkFrame(
            self,
            corner_radius=self.panel_corner_radius,
            height=80,
            border_width=self.border_thickness,
        )
        header_panel.grid(
            row=0, column=0, padx=30, pady=(30, 10), sticky="ew"
        )  # Reduced bottom padding
        header_panel.grid_columnconfigure(0, weight=1)

        header_label = ctk.CTkLabel(
            header_panel,
            text="FrameTale",
            font=ctk.CTkFont(size=self.font_size_large, weight="bold"),
        )
        header_label.grid(row=0, column=0, padx=30, pady=20)

    def _create_status_panels(self):
        """Creates the container for player status indicators."""
        self.status_container = ctk.CTkFrame(
            self,
            corner_radius=self.panel_corner_radius,
            border_width=self.border_thickness,
        )
        self.status_container.grid(
            row=1, column=0, padx=30, pady=(10, 10), sticky="ew"
        )  # Positioned above narrative

        # Configure grid columns within the status container to space out panels
        self.status_container.grid_columnconfigure(
            0, weight=1
        )  # Player Name (takes available space)
        self.status_container.grid_columnconfigure(1, weight=0)  # Health
        self.status_container.grid_columnconfigure(2, weight=0)  # Stamina
        self.status_container.grid_columnconfigure(3, weight=0)  # Money

        # Create individual status labels/panels (using Labels for simplicity here)
        # You could make these CTkFrames if you want borders around each stat
        self.status_labels = {}  # Dictionary to hold status labels

        common_font = ctk.CTkFont(size=self.font_size_normal)
        label_pady = 10
        label_padx = 15

        # Player Name (aligned left)
        # Player Name (aligned left)
        name_frame = ctk.CTkFrame(
            self.status_container,
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
        )
        name_frame.grid(
            row=0,
            column=0,
            padx=(label_padx * 2, label_padx),
            pady=label_pady,
            sticky="nsew",  # Make frame fill available space
        )
        name_frame.grid_columnconfigure(0, weight=1)  # Allow label to expand

        self.status_labels["name"] = ctk.CTkLabel(
            name_frame, text="Name: -", font=common_font, anchor="w"
        )
        self.status_labels["name"].grid(
            row=0,
            column=0,
            padx=label_padx,  # Add internal padding
            pady=label_pady,  # Add internal padding
            sticky="nsew",  # Make label fill available space within frame
        )

        # Health (aligned right)
        # Health (aligned right)
        health_frame = ctk.CTkFrame(
            self.status_container,
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
        )
        health_frame.grid(
            row=0, column=1, padx=label_padx, pady=label_pady, sticky="nsew"
        )  # Make frame fill available space
        health_frame.grid_columnconfigure(0, weight=1)  # Allow label to expand

        self.status_labels["health"] = ctk.CTkLabel(
            health_frame, text="HP: -", font=common_font, anchor="e"
        )
        self.status_labels["health"].grid(
            row=0,
            column=0,
            padx=label_padx,
            pady=label_pady,
            sticky="nsew",  # Make label fill available space within frame
        )

        # Stamina (aligned right)
        # Stamina (aligned right)
        stamina_frame = ctk.CTkFrame(
            self.status_container,
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
        )
        stamina_frame.grid(
            row=0,
            column=2,
            padx=label_padx,
            pady=label_pady,
            sticky="nsew",  # Make frame fill available space
        )
        stamina_frame.grid_columnconfigure(0, weight=1)  # Allow label to expand

        self.status_labels["stamina"] = ctk.CTkLabel(
            stamina_frame, text="Stamina: -", font=common_font, anchor="e"
        )
        self.status_labels["stamina"].grid(
            row=0,
            column=0,
            padx=label_padx,
            pady=label_pady,
            sticky="nsew",  # Make label fill available space within frame
        )

        # Money (aligned right)
        # Money (aligned right)
        money_frame = ctk.CTkFrame(
            self.status_container,
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
        )
        money_frame.grid(
            row=0,
            column=3,
            padx=(label_padx, label_padx * 2),
            pady=label_pady,
            sticky="nsew",  # Make frame fill available space
        )
        money_frame.grid_columnconfigure(0, weight=1)  # Allow label to expand

        self.status_labels["money"] = ctk.CTkLabel(
            money_frame, text="Money: -", font=common_font, anchor="e"
        )
        self.status_labels["money"].grid(
            row=0,
            column=0,
            padx=label_padx,
            pady=label_pady,
            sticky="nsew",  # Make label fill available space within frame
        )

    def _create_narrative_panel(self):
        """Creates the main panel for displaying the story narrative."""
        narrative_panel = ctk.CTkFrame(
            self,
            corner_radius=self.panel_corner_radius,
            border_width=self.border_thickness,
        )
        narrative_panel.grid(
            row=2, column=0, padx=30, pady=10, sticky="nsew"
        )  # Adjusted padding
        narrative_panel.grid_columnconfigure(0, weight=1)
        narrative_panel.grid_rowconfigure(0, weight=1)

        self.narrative_textbox = ctk.CTkTextbox(
            narrative_panel,
            wrap="word",
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
            font=ctk.CTkFont(size=self.font_size_normal),
            state="disabled",  # Start disabled
        )
        self.narrative_textbox.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

    def _create_input_panel(self):
        """Creates the panel for player action input."""
        input_panel = ctk.CTkFrame(
            self,
            corner_radius=self.panel_corner_radius,
            border_width=self.border_thickness,
        )
        input_panel.grid(
            row=3, column=0, padx=30, pady=10, sticky="ew"
        )  # Adjusted padding
        input_panel.grid_columnconfigure(0, weight=0)  # Special button
        input_panel.grid_columnconfigure(
            1, weight=1
        )  # Input Entry (takes available space)
        input_panel.grid_columnconfigure(2, weight=0)  # Send button

        button_height = 50
        button_font = ctk.CTkFont(size=self.font_size_normal)

        # Special Button (New)
        special_button = ctk.CTkButton(
            input_panel,
            text="Special",
            command=self.handle_special_action,  # Add a handler function
            height=button_height,
            width=100,  # Fixed width for special button
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
            font=button_font,
            # Optional: different color for special button
            # fg_color=("#DBAE58", "#C19A6B"),
            # hover_color=("#C19A6B", "#A47E54"),
        )
        special_button.grid(row=0, column=0, sticky="w", padx=(20, 10), pady=20)

        # Input Entry
        self.action_entry = ctk.CTkEntry(
            input_panel,
            placeholder_text="Enter your action...",
            height=button_height,
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
            font=ctk.CTkFont(size=self.font_size_normal),
        )
        self.action_entry.grid(
            row=0, column=1, sticky="ew", padx=0, pady=20
        )  # No internal padx
        self.action_entry.bind("<Return>", self.process_action_event)  # Bind Enter key

        # Send Button
        send_button = ctk.CTkButton(
            input_panel,
            text="Send",
            command=self.process_action_event,  # Trigger same logic as Enter
            height=button_height,
            width=100,  # Fixed width for send button
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
            font=button_font,
        )
        send_button.grid(row=0, column=2, sticky="e", padx=(10, 20), pady=20)

    def _create_bottom_panel(self):
        """Creates the bottom panel, now only containing the Quit button."""
        bottom_panel = ctk.CTkFrame(
            self,
            corner_radius=self.panel_corner_radius,
            border_width=self.border_thickness,
            fg_color="transparent",  # Make panel transparent if only holding one button
        )
        # Align the panel itself to the bottom-right
        bottom_panel.grid(row=4, column=0, padx=30, pady=(10, 30), sticky="se")
        # No need to configure columns if only one widget

        # Quit Button (Smaller and in the corner)
        quit_button = ctk.CTkButton(
            bottom_panel,
            text="Quit",  # Shorter text
            command=self.quit_game,
            height=40,  # Smaller height
            width=80,  # Smaller width
            corner_radius=self.widget_corner_radius,
            border_width=self.border_thickness,
            font=ctk.CTkFont(size=self.font_size_normal - 2),  # Slightly smaller font
            fg_color=("#E74C3C", "#C0392B"),  # Keep danger colors
            hover_color=("#C0392B", "#A93226"),
        )
        # Pack it inside its panel to keep it tight
        quit_button.pack(padx=0, pady=0)  # No padding within its own frame

    # --- Action Handling ---

    def process_action_event(self, event=None):
        """Handles the 'Send' button click or Enter key press."""
        action = self.action_entry.get().strip()
        if not action:
            logger.warning("Attempted to send empty action.")
            return

        logger.info(f"Player action received: '{action}'")
        # Stop any ongoing narrative typing before processing new action
        self.narrative_typer.stop()

        # Clear the entry immediately
        self.action_entry.delete(0, "end")

        try:
            # Process the action through the game engine
            # This call might take time if the engine involves API calls etc.
            # Consider running this in a thread if it blocks the GUI significantly
            narrative, _ = self.engine.process_player_action(action)

            # Update player status immediately
            self.update_player_status()

            # Start typing out the new narrative
            self.narrative_typer.type_out(
                narrative or "..."
            )  # Use "..." if narrative is empty

            # Note: Auto-saving now happens only on quit

        except Exception as e:
            logger.exception(f"Error processing action: {e}")
            # Display error message directly (no typing effect for errors)
            self.narrative_textbox.configure(state="normal")
            self.narrative_textbox.delete("0.0", "end")
            self.narrative_textbox.insert(
                "0.0", f"⚠️ An error occurred: {e}\nPlease try a different action."
            )
            self.narrative_textbox.configure(state="disabled")
            # Still update status in case of partial success or relevant error state
            self.update_player_status()

    def handle_special_action(self):
        """Placeholder for the 'Special' button action."""
        logger.info("'Special' button clicked.")
        # Stop any ongoing narrative typing
        self.narrative_typer.stop()

        # Implement special action logic here
        # For now, just display a message
        special_message = "You triggered a *Special* action! (Implementation pending)"

        # Update player status immediately (if special action affects it)
        # self.update_player_status() # Example if stats change

        # Start typing out the message
        self.narrative_typer.type_out(special_message)

        # Optionally clear the input field or add specific text
        # self.action_entry.delete(0, "end")

    # --- State Update ---

    def update_player_status(self):
        """Updates the player status labels instantly."""
        try:
            player_status = self.engine.get_player_status()  # Fetch latest status
            logger.debug(f"Updating status display with: {player_status}")

            if (
                "name" in self.status_labels
                and self.status_labels["name"].winfo_exists()
            ):
                self.status_labels["name"].configure(
                    text=(
                        f"Name: {player_status.get('name', '-')}"
                        if isinstance(player_status, dict)
                        else "Name: Error"
                    )
                )
            if (
                "health" in self.status_labels
                and self.status_labels["health"].winfo_exists()
            ):
                self.status_labels["health"].configure(
                    text=(
                        f"Health: {player_status.get('health', '-')}"
                        if isinstance(player_status, dict)
                        else "Health: Error"
                    )
                )
            if (
                "stamina" in self.status_labels
                and self.status_labels["stamina"].winfo_exists()
            ):
                self.status_labels["stamina"].configure(
                    text=(
                        f"Stamina: {player_status.get('stamina', '-')}"
                        if isinstance(player_status, dict)
                        else "Stamina: Error"
                    )
                )
            if (
                "money" in self.status_labels
                and self.status_labels["money"].winfo_exists()
            ):
                self.status_labels["money"].configure(
                    text=(
                        f"Money: {player_status.get('money', '-')}"
                        if isinstance(player_status, dict)
                        else "Money: Error"
                    )
                )

        except Exception as e:
            logger.exception(f"Error updating player status display: {e}")
            # Update a label to show status error
            if (
                "name" in self.status_labels
                and self.status_labels["name"].winfo_exists()
            ):
                self.status_labels["name"].configure(text="Status Error")

    # --- Game Lifecycle ---

    def save_and_quit(self):
        """Saves the game state and then quits the application."""
        logger.info("Save and quit initiated.")
        try:
            logger.info("Attempting final save...")
            if self.engine.save_game():
                logger.info("Final save successful.")
            else:
                # Handle save failure? Maybe log it is enough as we are quitting anyway.
                logger.warning("Final save failed before quitting.")
        except Exception as e:
            logger.exception(f"Error saving game on quit: {e}")
        finally:
            # Ensure the application quits regardless of save success/failure
            logger.info("Quitting application.")
            self.quit()  # Stop the Tkinter main loop
            self.destroy()  # Destroy the window and widgets

    def quit_game(self):
        """Handles the quit action, triggering save_and_quit."""
        # Stop any background tasks like typing
        self.narrative_typer.stop()
        # Proceed with saving and quitting
        self.save_and_quit()


def run_game_loop(
    engine: GameEngine,
) -> None:
    """
    Initializes and runs the game loop using the CustomTkinter GUI.

    Args:
        engine: The initialized GameEngine instance.
    """

    logger.info("Initializing GameScreen...")
    app = GameScreen(engine)
    logger.info("Starting main loop...")
    app.mainloop()
    logger.info("Main loop finished.")
