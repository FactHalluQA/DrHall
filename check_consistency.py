from datetime import datetime

import pandas as pd

from util import chat_with_chatgpt


# 定义检查一致性的函数
def check_consistency(question, answer1, answer2):
    prompt = f"Question: {question}\nAnswer1: {answer1}\nAnswer2: {answer2}\nAre the above two answers to the question consistent? Please answer in as few words or phrases as possible. Do not evaluate the rightness or wrongness of the answer itself. Note: Yes and right have the same meaning; No and Wrong have the same meaning."
    response = chat_with_chatgpt(prompt)
    return response


# 读取Excel文件并检查每一行的一致性
def process_excel(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 定义列名列表
    columns_to_process = ['QMR1', 'QMR2', 'QMR3', 'QMR4', 'AMR1', 'AMR2']

    # 处理每一列
    for column in columns_to_process:
        if column in df:
            for index, row in df.iterrows():
                question = row['question']
                source_answer = row['Source Answer']
                answer = row[column]
                consistency = check_consistency(question, source_answer, answer)
                df.at[index, column + '_consistency'] = consistency  # 将一致性检查结果添加到新的列中

    # 保存处理后的数据到新的Excel文件
    output_path = f"consistency_check_output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    df.to_excel(output_path, index=False)
    return output_path


# 主函数
if __name__ == "__main__":
    input_file_path = 'path_to_processed_output.xlsx'  # processing.py输出的文件路径
    consistency_check_file_path = process_excel(input_file_path)
    print(f"Consistency check data saved to {consistency_check_file_path}")
