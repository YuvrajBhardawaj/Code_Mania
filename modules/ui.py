import customtkinter as ctk
import json
import os
import random
from time import sleep
from modules.complier import Compiler
import threading
from tkcode import CodeEditor
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
        self.question = random.sample(self.data['questions'], min(10, len(self.data['questions'])))
        self.score = {q['id']: False for q in self.question}
        # Question Title & Content Frame
        questionFrame = ctk.CTkFrame(self)
        questionFrame.pack(fill="x", padx=10, pady=5)

        self.questionTitle = ctk.CTkLabel(questionFrame, text=f"{self.question[self.index]['title']}", font=("Arial", 18, 'bold'))
        self.questionTitle.pack(anchor="w", padx=5, pady=2)

        self.questionLabel = ctk.CTkLabel(questionFrame, text=self.question[self.index]['question'], font=("Arial", 16), wraplength=1200)
        self.questionLabel.pack(anchor="w", padx=5, pady=2)

        self.finish_btn = ctk.CTkButton(self, text="Finish", width=100, font=('Arial', 12, 'bold'), command=self.show_final_score)
        self.finish_btn.place(relx=0.9, rely=0.05, anchor='ne')

        # Main Frame (Editor + Test Cases)
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Language Dropdown
        self.language_var = ctk.StringVar(value="python")
        self.language_dropdown = ctk.CTkComboBox(
            main_frame, values=["python", "java", "cpp"],
            command=self.change_language, variable=self.language_var
        )
        self.language_dropdown.grid(row=0, column=0, sticky="nw", padx=5, pady=5)

        # **Syntax Highlighting Code Editor**
        self.editor = CodeEditor(
            main_frame,
            language="python",
            highlighter="dracula",
            background="black",
            font=("Arial", 21),
            height=20,
            width=80
        )
        self.editor.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Test Case Panel
        test_case_frame = ctk.CTkScrollableFrame(main_frame)
        test_case_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Test Cases Display
        self.test_cases_labels = []
        for i in range(5):
            label = ctk.CTkLabel(test_case_frame, text=f"Test Case {i+1}:", font=("Arial", 18, 'bold'))
            testcase_label = ctk.CTkLabel(test_case_frame, text=f"Input: {self.question[self.index]['test_cases'][i]['input']}", font=("Arial", 15))
            output_label = ctk.CTkLabel(test_case_frame, text=f"Expected Output: {self.question[self.index]['test_cases'][i]['output']}", font=("Arial", 15))
            your_output_label = ctk.CTkLabel(test_case_frame, text="Your Output: ", font=("Arial", 15))

            label.pack(anchor="w", padx=5, pady=2)
            testcase_label.pack(anchor="w", padx=5, pady=2)
            output_label.pack(anchor="w", padx=5, pady=2)
            your_output_label.pack(anchor="w", padx=5, pady=5)

            self.test_cases_labels.append({ 'input':testcase_label, 'expectedOutput':output_label,'output' :your_output_label})
        # Layout Configuration
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)

        # Submit Buttons
        submit_frame = ctk.CTkFrame(self)
        submit_frame.pack(pady=10)

        self.previous_btn = ctk.CTkButton(submit_frame, text="Previous", state='disabled', width=100,font=('Arial',12,'bold'), command=self.prev_question)
        self.submit_btn = ctk.CTkButton(submit_frame, text="Submit", width=100,font=('Arial',12,'bold'), command=self.run_code_thread)
        self.next_btn = ctk.CTkButton(submit_frame, text="Next", width=100,font=('Arial',12,'bold'), command=self.next_question)

        self.previous_btn.grid(row=0, column=0, padx=5, pady=5)
        self.submit_btn.grid(row=0, column=1, padx=5, pady=5)
        self.next_btn.grid(row=0, column=2, padx=5, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def change_language(self, selected_lang):
        """Updates syntax highlighting when the user selects a new language."""
        self.editor.language=selected_lang  # Update editor language
        self.editor.delete("1.0", "end")  # ✅ Correct

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
            self.editor.delete("1.0", "end")
            self.update_test_cases()
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
            self.editor.delete("1.0", "end")
            self.update_test_cases()
            # Disable "Previous" if it's the first question
            if self.index == 0:
                self.previous_btn.configure(state='disabled')
        else:
            self.previous_btn.configure(state='disabled')

    def update_test_cases(self):
        """Updates the test case labels when switching questions."""
        test_cases = self.question[self.index]['test_cases']

        for i in range(5):  # Assuming max 5 test cases
            if i < len(test_cases):  # If test case exists
                input_text = f"Input: {test_cases[i]['input']}"
                output_text = f"Expected Output: {test_cases[i]['output']}"
                your_output_text = "Your Output: "  # Reset user output

                # Update test case labels dynamically
                self.test_cases_labels[i]['input'].configure(text=input_text)
                self.test_cases_labels[i]['expectedOutput'].configure(text=output_text)
                self.test_cases_labels[i]['output'].configure(text=your_output_text)
            else:
                # Hide unused test cases
                self.test_cases_labels[i]['input'].configure(text="Input: N/A")
                self.test_cases_labels[i]['expectedOutput'].configure(text="Expected Output: N/A")
                self.test_cases_labels[i]['output'].configure(text="Your Output: N/A")

    def run_code_thread(self):
        """Runs the code execution in a separate thread to prevent UI freezing."""
        thread = threading.Thread(target=self.run_code, daemon=True)
        thread.start()

    def run_code(self):
        """Passes the selected language & user input to the compiler."""
        language = self.language_var.get()
        code = self.editor.get("1.0", "end-1c")  # Get user code
        test_cases = self.question[self.index]['test_cases']  # Get current question's test cases
        passed_tests = 0
        for i, test_case in enumerate(test_cases):
            sleep(2)  # Simulating execution delay
            
            input_data = str(test_case['input']).strip()  # Ensure input is a string
            expected_output = str(test_case['output']).strip()  # Ensure output is a string
            
            # Execute code using the selected language
            if language == "python":
                output = self.compiler.python_compiler(code, input_data)
            elif language == "cpp":
                output = self.compiler.cpp_compiler(code, input_data)
            elif language == "java":
                output = self.compiler.java_compiler(code, input_data)
            else:
                output = "Unsupported language"

            output = output.strip()  # Remove extra newlines/spaces
            
            # Compare output with expected output
            if output == expected_output:
                self.test_cases_labels[i]['output'].configure(text=f"Your Output: {output} ✅")
                passed_tests+=1
            else:
                self.test_cases_labels[i]['output'].configure(text=f"Your Output: {output} ❌")
        if(passed_tests==5):
            self.score[self.question[self.index]['id']] = True
    
    def show_final_score(self):
        total_questions = len(self.score)
        solved_questions = sum(self.score.values())
        score_text = f"Final Score: {solved_questions}/{total_questions}"
        self.withdraw()
        self.score_window = ScoreWindow(self, score_text)

class ScoreWindow(ctk.CTkToplevel):
    def __init__(self, parent, score_text):
        super().__init__(parent)

        # Set window size and center it
        window_width = 300
        window_height = 200
        x_position = (self.winfo_screenwidth() - window_width) // 2
        y_position = (self.winfo_screenheight() - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        self.title("Your Score")

        # Configure grid to center content
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Score label, centered
        score_label = ctk.CTkLabel(self, text=score_text, font=("Arial", 24, 'bold'))
        score_label.grid(row=0, column=0, pady=20)

        # Exit button — closes everything
        close_btn = ctk.CTkButton(self, text="Exit", command=parent.close_window)
        close_btn.grid(row=1, column=0, pady=10)

        # Ensure "X" button also closes everything
        self.protocol("WM_DELETE_WINDOW", parent.close_window)