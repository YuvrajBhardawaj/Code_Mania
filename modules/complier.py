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

    def cpp_compiler(self, code, input_data):
        """Compiles and runs C++ code using g++ and subprocess."""
        file_path = "temp/temp.cpp"
        executable = "temp/temp.out"
        os.makedirs("temp", exist_ok=True)  # Ensure temp directory exists

        with open(file_path, "w") as f:
            f.write(code)

        # Compile the C++ code
        compile_result = subprocess.run(
            ["g++", file_path, "-o", executable],
            capture_output=True,
            text=True
        )

        if compile_result.returncode != 0:
            return f"Compilation failed:\n{compile_result.stderr}"

        # Run the compiled executable and pass input data
        run_result = subprocess.run(
            [executable],
            capture_output=True,
            text=True,
            input=str(input_data)
        )

        return run_result.stdout + run_result.stderr

    def java_compiler(self, code, input_data):
        """Compiles and runs Java code using javac and java subprocess."""
        file_path = "temp/Solution.java"
        class_file = "temp"  # Directory to store compiled Java class
        os.makedirs("temp", exist_ok=True)  # Ensure temp directory exists

        with open(file_path, "w") as f:
            f.write(code)

        # Compile the Java code
        compile_result = subprocess.run(
            ["javac", "-d", class_file, file_path],
            capture_output=True,
            text=True
        )

        if compile_result.returncode != 0:
            return f"Compilation failed:\n{compile_result.stderr}"

        # Run the Java program
        run_result = subprocess.run(
            ["java", "-cp", class_file, "Solution"],
            capture_output=True,
            text=True,
            input=str(input_data)
        )

        return run_result.stdout + run_result.stderr
