import tkinter as tk
from tkinter import scrolledtext, messagebox
from controller.error_controller import ErrorController
from config import APP_TITLE, WINDOW_SIZE

class MainWindow:

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)

        self.controller = ErrorController()

        self._build_ui()

    def _build_ui(self):
        # Insert error message
        tk.Label(self.root, text="SAP error message:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=5)

        self.input_text = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD)
        self.input_text.pack(fill="both", expand=False, padx=10)

        # Button - start analyse
        self.send_button = tk.Button(self.root,text="Analyse", command=self._on_analyse_clicked)
        self.send_button.pack(pady=10)

        # Result
        tk.Label(self.root, text="LLM answer:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10)

        self.output_text = scrolledtext.ScrolledText(self.root, height=15, wrap=tk.WORD)
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _on_analyse_clicked(self):
        error_message = self.input_text.get("1.0", tk.END)

        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "Analysis in progress...\n")

        try:
            answer = self.controller.handle_error(error_message)

            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, answer)

        except ValueError as ve:
            messagebox.showwarning("Hinweiß", str(ve))

        except Exception as e:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(
                tk.END,
                f"An error occured:\n{e}"
            )