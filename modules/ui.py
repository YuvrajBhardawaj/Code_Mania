import customtkinter as ctk
from tkcode import CodeEditor
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
    def __init__(self,parent):
        super().__init__()
        self.state('zoomed')
        self.parent = parent
        self.resizable(False, False)  # Disable resizing

        questionLabel = ctk.CTkLabel(self,text="Text find palindrome")
        questionLabel.pack()

        frame = ctk.CTkFrame(self)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Create the CodeEditor widget inside the frame
        editor = CodeEditor(
            frame,  # Place the editor inside the frame
            language="python",  # Language (Python, Java, C++, etc.)
            highlighter="dracula",  # Syntax highlighting theme
            background="black",
            font=("Arial", 18)
        )
        # Make the editor take all the available space, like "flex: 1"
        editor.grid(row=0,column=0,sticky="nsew")  # Flex behavior for the editor

        test_frame = ctk.CTkFrame(frame)
        test_frame.grid(row=0,column=1)
        # Create the label inside the frame, alongside the editor
        for i in range(10):
            label = ctk.CTkLabel(test_frame, text="Test Case : " + str(i+1))
            label.grid(row=i+1, column=1, sticky="w", padx=10, pady=5)  # Align labels in their own row

        frame.grid_columnconfigure(0, weight=1)  # Make the first column (editor) expand
        frame.grid_columnconfigure(1, weight=0) 
        frame.grid_rowconfigure(0, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.close_window)

    def close_window(self):
        """Closes the current window and brings back the main window."""
        self.parent.quit()  # Quit the application
        self.destroy()  # Close the new window