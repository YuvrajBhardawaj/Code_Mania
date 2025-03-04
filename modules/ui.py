import customtkinter as ctk
import json
import os
# Main Application Class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("400x300")
        self.title("Main Window")

        self.new_window = None  # To track the new window

        # Button to Open New Window
        open_button = ctk.CTkButton(self, text="Open New Window", command=self.open_new_window)
        open_button.pack(pady=20)

    def open_new_window(self):
        """Opens a new window and hides the main app window."""
        self.withdraw()  # Hide main window
        self.new_window = Questions(self)

class Questions(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__()
        self.state('zoomed')
        self.parent = parent

        # Load questions
        file_path = os.path.join(os.path.dirname(__file__), "questions.json")
        with open(file_path, "r") as file:
            self.data = json.load(file)
        self.index = 0
        self.question = self.data['questions']

        # Frame for Question Title & Content
        questionFrame = ctk.CTkFrame(self)
        questionFrame.pack(fill="x", padx=10, pady=5)

        questionTitle = ctk.CTkLabel(questionFrame, text=f"{self.question[self.index]['title']}", font=("Arial", 18, 'bold'))
        questionTitle.pack(anchor="w", padx=5, pady=2)

        self.questionLabel = ctk.CTkLabel(questionFrame, text=self.question[self.index]['question'], font=("Arial", 16), wraplength=900)
        self.questionLabel.pack(anchor="w", padx=5, pady=2)

        # 🔹 Main Frame (Code Editor + Test Cases)
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # 🔹 Language Selection Dropdown
        self.language_var = ctk.StringVar(value="python")  # Default Language: Python
        self.language_dropdown = ctk.CTkComboBox(
            main_frame, values=["python", "java", "cpp"], 
            command=self.change_language, variable=self.language_var
        )
        self.language_dropdown.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        # 🔹 Code Editor (Left Side)
        self.code_input = ctk.CTkTextbox(main_frame, font=("Arial", 14), wrap="word")
        self.code_input.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # 🔹 Scrollable Test Case Panel (Right Side)
        test_case_frame = ctk.CTkScrollableFrame(main_frame)
        test_case_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Test Cases
        for i in range(5):
            label = ctk.CTkLabel(test_case_frame, text=f"Test Case {i+1}:", font=("Arial", 14, 'bold'))
            testcase_label = ctk.CTkLabel(test_case_frame, text=f"Input: {self.question[self.index]['test_cases'][i]['input']}", font=("Arial", 12))
            output_label = ctk.CTkLabel(test_case_frame, text=f"Expected Output: {self.question[self.index]['test_cases'][i]['output']}", font=("Arial", 12))
            your_output_label = ctk.CTkLabel(test_case_frame, text="Your Output: ", font=("Arial", 12))

            label.pack(anchor="w", padx=5, pady=2)
            testcase_label.pack(anchor="w", padx=5, pady=2)
            output_label.pack(anchor="w", padx=5, pady=2)
            your_output_label.pack(anchor="w", padx=5, pady=5)

        # 🔹 Adjust Size Distribution (Editor: 2 parts, Test Cases: 1 part)
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # 🔹 Submit Buttons
        submit_frame = ctk.CTkFrame(self)
        submit_frame.pack(pady=10)

        self.previous_btn = ctk.CTkButton(submit_frame, text="Previous", state='disabled', width=100)
        self.submit_btn = ctk.CTkButton(submit_frame, text="Submit", width=100)
        self.next_btn = ctk.CTkButton(submit_frame, text="Next", width=100)

        self.previous_btn.grid(row=0, column=0, padx=5, pady=5)
        self.submit_btn.grid(row=0, column=1, padx=5, pady=5)
        self.next_btn.grid(row=0, column=2, padx=5, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def change_language(self, selected_lang):
        """Updates syntax highlighting when the user selects a new language."""
        self.editor.set_language(selected_lang)  # Update editor language
        self.editor.clear()  # Optional: Clear editor when switching languages

    def close_window(self):
        """Closes the question window and returns to the main app."""
        self.parent.quit()
        self.destroy()