import subprocess
import os
class Compiler:
    def python_compiler(self, code, input_data):
        """Executes Python code using subprocess with test case input."""
        file_path = "temp/temp.py"
        os.makedirs("temp", exist_ok=True)  # Ensure temp directory exists

        with open(file_path, "w") as f:
            f.write(code)

        # Run the Python script and pass input data
        result = subprocess.run(
            ["python", file_path],  # Use "python" or "python3" based on OS
            capture_output=True,
            text=True,
            input=str(input_data)  # Pass formatted input
        )

        return result.stdout + result.stderr    
    def cpp_compiler(self):
        pass

    def java_compiler(self):
        command = ['javac', 'HelloWorld.java']
        
        result = subprocess.run(command, capture_output=True, text=True)

        # Check the result
        if result.returncode == 0:
            print("Compilation successful!")
        else:
            print("Compilation failed!")
            print(result.stderr)