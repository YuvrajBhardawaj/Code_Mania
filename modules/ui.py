import customtkinter as ctk
import json
import os
from time import sleep
from modules.complier import Compiler
import threading
# Main Application Class
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("400x300")
        self.title("Main Window")

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
        self.title("Code Mania")
        self.compiler = Compiler()
        # Load questions
        file_path = os.path.join(os.path.dirname(__file__), "questions.json")
        with open(file_path, "r") as file:
            self.data = json.load(file)
        self.index = 0
        self.question = self.data['questions']

        # Frame for Question Title & Content
        questionFrame = ctk.CTkFrame(self)
        questionFrame.pack(fill="x", padx=10, pady=5)

        self.questionTitle = ctk.CTkLabel(questionFrame, text=f"{self.question[self.index]['title']}", font=("Arial", 18, 'bold'))
        self.questionTitle.pack(anchor="w", padx=5, pady=2)

        self.questionLabel = ctk.CTkLabel(questionFrame, text=self.question[self.index]['question'], font=("Arial", 16),wraplength=1200)
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
        self.code_input = ctk.CTkTextbox(main_frame, font=("Arial", 25), wrap="word")
        self.code_input.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # 🔹 Scrollable Test Case Panel (Right Side)
        test_case_frame = ctk.CTkScrollableFrame(main_frame)
        test_case_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Test Cases
        for i in range(5):
            label = ctk.CTkLabel(test_case_frame, text=f"Test Case {i+1}:", font=("Arial", 18, 'bold'))
            testcase_label = ctk.CTkLabel(test_case_frame, text=f"Input: {self.question[self.index]['test_cases'][i]['input']}", font=("Arial", 15))
            output_label = ctk.CTkLabel(test_case_frame, text=f"Expected Output: {self.question[self.index]['test_cases'][i]['output']}", font=("Arial", 15))
            your_output_label = ctk.CTkLabel(test_case_frame, text="Your Output: ", font=("Arial", 15))

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

        self.previous_btn = ctk.CTkButton(submit_frame, text="Previous", state='disabled', width=100, command=self.prev_question)
        self.submit_btn = ctk.CTkButton(submit_frame, text="Submit", width=100, command=self.run_code_thread)
        self.next_btn = ctk.CTkButton(submit_frame, text="Next", width=100, command=self.next_question)

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

    def next_question(self):
        if self.index < len(self.question) - 1:
            self.index += 1
            self.previous_btn.configure(state='active')  # Ensure previous button is active
            self.questionTitle.configure(text=self.question[self.index]['title'])
            self.questionLabel.configure(text=self.question[self.index]['question'])

            # Disable "Next" if it's the last question
            if self.index == len(self.question) - 1:
                self.next_btn.configure(state='disabled')
        else:
            self.next_btn.configure(state='disabled')

    def prev_question(self):
        if self.index > 0:
            self.index -= 1
            self.next_btn.configure(state='active')  # Ensure next button is active
            self.questionTitle.configure(text=self.question[self.index]['title'])
            self.questionLabel.configure(text=self.question[self.index]['question'])

            # Disable "Previous" if it's the first question
            if self.index == 0:
                self.previous_btn.configure(state='disabled')
        else:
            self.previous_btn.configure(state='disabled')

    def run_code_thread(self):
        """Runs the code execution in a separate thread to prevent UI freezing."""
        thread = threading.Thread(target=self.run_code, daemon=True)
        thread.start()

    def run_code(self):
        """Passes the selected language & user input to the compiler."""
        language = self.language_var.get()
        code = self.code_input.get("1.0", "end-1c")  # Get user input code
        
        test_cases = self.question[self.index]['test_cases']  # Get current question's test cases
        
        for i, test_case in enumerate(test_cases):
            sleep(2)
            input_data = test_case['input']
            #print(input_data)
            expected_output = test_case['output']
            
            # Pass code and input to the compiler (Assuming your compiler takes input as an argument)
            output = self.compiler.python_compiler(code, input_data) 
            #print(output)
            #Compare output with expected output
            result = "Passed" if output.strip() == str(expected_output) else f"Failed (Expected: {expected_output}, Got: {output})"
            print(result)   