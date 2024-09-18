import os
import subprocess
from datetime import datetime

import pandas as pd


# 定义调用编译器的函数
def compile_code(code, language="cpp"):
    if language == "cpp":
        return compile_cpp_code(code)
    elif language == "python":
        return run_python_code(code)
    else:
        raise ValueError("Unsupported language. Choose 'cpp' or 'python'.")


# 编译并运行C++代码
def compile_cpp_code(code):
    try:
        # 保存代码到临时文件
        with open("temp_code.cpp", "w") as file:
            file.write(code)

        # 编译C++代码
        subprocess.run(["g++", "temp_code.cpp", "-o", "temp_code"], check=True)

        # 运行编译后的程序并捕获输出
        result = subprocess.run("./temp_code", capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    finally:
        # 清理临时文件
        os.remove("temp_code.cpp")
        if os.path.exists("temp_code"):
            os.remove("temp_code")


# 运行Python代码
def run_python_code(code):
    try:
        # 保存代码到临时文件
        with open("temp_code.py", "w") as file:
            file.write(code)

        # 运行Python代码并捕获输出
        result = subprocess.run(["python", "temp_code.py"], capture_output=True, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    finally:
        # 清理临时文件
        os.remove("temp_code.py")


# 读取Excel文件并处理每一行
def process_excel(file_path, language="cpp"):
    df = pd.read_excel(file_path)

    # 定义列名列表
    columns_to_process = ['QMR1', 'QMR2', 'QMR3', 'QMR4', 'AMR1', 'AMR2']

    for column in columns_to_process:
        if column in df:
            for index, row in df.iterrows():
                code = row[column]
                output = compile_code(code, language)
                df.at[index, f"{column}_output"] = output

    output_path = f"compiled_output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    df.to_excel(output_path, index=False)
    return output_path


# 主函数
if __name__ == "__main__":
    input_file_path = 'path_to_main_output.xlsx'  # main.py输出的文件路径
    language = "cpp"  # 或 "python"
    compiled_file_path = process_excel(input_file_path, language)
    print(f"Compiled data saved to {compiled_file_path}")
