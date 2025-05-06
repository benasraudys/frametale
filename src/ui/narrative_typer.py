import logging
import time
import random
import threading
import customtkinter as ctk

logger = logging.getLogger(__name__)


class NarrativeTyper:
    """Handles the threaded typing effect for the narrative textbox."""

    def __init__(self, textbox: ctk.CTkTextbox, app: ctk.CTk):
        self.textbox = textbox
        self.app = app
        self._stop_event = threading.Event()
        self._thread = None

    def type_out(self, text: str):
        """Starts the typing effect in a separate thread."""
        # Stop any existing typing thread
        self.stop()

        # Clear the stop event for the new thread
        self._stop_event.clear()

        # Disable textbox during typing, clear it
        self.textbox.configure(state="normal")
        self.textbox.delete("0.0", "end")
        self.textbox.configure(state="disabled")

        # Start the new typing thread
        self._thread = threading.Thread(
            target=self._type_worker, args=(text,), daemon=True
        )
        self._thread.start()

    def _type_worker(self, text: str):
        """The worker function that performs typing simulation."""
        try:
            # Re-enable textbox safely using app.after
            self.app.after(0, lambda: self.textbox.configure(state="normal"))

            for char in text:
                # Check if stop was requested
                if self._stop_event.is_set():
                    logger.info("Typing thread stopped.")
                    break

                # Schedule character insertion on the main thread
                self.app.after(0, lambda c=char: self._insert_char(c))

                # Calculate delay
                if char == "\n":
                    delay = 0.5  # Slightly faster newline
                elif char in [".", "!", "?"]:
                    delay = 0.3  # Faster punctuation
                elif char == ",":
                    delay = 0.1
                elif char == " ":
                    delay = 0.01
                else:
                    # Variable delay for other characters
                    delay = random.uniform(0.01, 0.05)

                time.sleep(delay)

            # Ensure the final state is disabled, scheduled after the last char
            self.app.after(10, self._finalize_typing)

        except Exception as e:
            logger.exception(f"Error in typing thread: {e}")
            # Ensure textbox is disabled even if error occurs
            self.app.after(0, lambda: self.textbox.configure(state="disabled"))

    def _insert_char(self, char: str):
        """Inserts a character and scrolls (runs on main thread via app.after)."""
        if self.textbox.winfo_exists():  # Check if widget still exists
            self.textbox.insert("end", char)
            self.textbox.see("end")

    def _finalize_typing(self):
        """Finalizes typing state (runs on main thread via app.after)."""
        if self.textbox.winfo_exists():
            # Only disable if no stop was requested during the final delay
            if not self._stop_event.is_set():
                self.textbox.configure(state="disabled")
            logger.info("Typing finished.")

    def stop(self):
        """Signals the typing thread to stop."""
        if self._thread and self._thread.is_alive():
            self._stop_event.set()
            # Optionally wait for the thread to finish
            # self._thread.join(timeout=0.1)
            logger.info("Stop signal sent to typing thread.")
        # Re-enable textbox immediately upon stopping if it was disabled
        # self.app.after(0, lambda: self.textbox.configure(state="normal"))