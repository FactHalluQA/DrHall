import os
import subprocess
from datetime import datetime

import pandas as pd

# Define the function to call the compiler
def compile_code(code, language="cpp"):
    if language == "cpp":
        return compile_cpp_code(code)
    elif language == "python":
        return run_python_code(code)
    else:
        raise ValueError("Unsupported language. Choose 'cpp' or 'python'.")

# Compile and run C++ code
def compile_cpp_code(code):
    try:
        # Save the code to a temporary file
        with open("temp_code.cpp", "w") as file:
            file.write(code)

        # Compile the C++ code
        subprocess.run(["g++", "temp_code.cpp", "-o", "temp_code"], check=True)

        # Run the compiled program and capture the output
        result = subprocess.run("./temp_code", capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    finally:
        # Clean up temporary files
        os.remove("temp_code.cpp")
        if os.path.exists("temp_code"):
            os.remove("temp_code")

# Run Python code
def run_python_code(code):
    try:
        # Save the code to a temporary file
        with open("temp_code.py", "w") as file:
            file.write(code)

        # Run the Python code and capture the output
        result = subprocess.run(["python", "temp_code.py"], capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    finally:
        # Clean up temporary files
        os.remove("temp_code.py")

# Read the Excel file and process each row
def process_excel(file_path, language="cpp"):
    df = pd.read_excel(file_path)

    # Define the list of columns to process
    columns_to_process = ['QMR1', 'QMR2', 'QMR3', 'QMR4', 'AMR1', 'AMR2', 'Source_Answer', 'CMR1', 'CMR2', 'CMR3']

    for column in columns_to_process:
        if column in df:
            for index, row in df.iterrows():
                code = row[column]
                output = compile_code(code, language)
                df.at[index, f"{column}_output"] = output

    output_path = f"compiled_output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    df.to_excel(output_path, index=False)
    return output_path

# Main function
if __name__ == "__main__":
    input_file_path = 'path_to_main_output.xlsx'  # The file path output by main.py
    language = "cpp"  # or "python"
    compiled_file_path = process_excel(input_file_path, language)
    print(f"Compiled data saved to {compiled_file_path}")
