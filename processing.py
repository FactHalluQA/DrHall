from datetime import datetime

import pandas as pd

from util import chat_with_chatgpt

# Define the processing function
def process_question_and_answer(question, answer):
    prompt = f"Question: {question}\nAnswer: {answer}\nTry to summarize the answer into one word or one phrase. Please be as concise as possible."
    response = chat_with_chatgpt(prompt)
    return response

# Read the Excel file and process each row
def process_excel(file_path):
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Define the list of columns to process
    columns_to_process = ['QMR1', 'QMR2', 'QMR3', 'QMR4', 'AMR1', 'AMR2', 'Source_Answer', 'CMR1', 'CMR2', 'CMR3']

    # Process each column
    for column in columns_to_process:
        if column in df:
            for index, row in df.iterrows():
                question = row['question']
                answer = row[column]
                summary = process_question_and_answer(question, answer)
                df.at[index, column + '_summary'] = summary  # Add the summary to a new column

    # Save the processed data to a new Excel file
    output_path = f"processed_output_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx"
    df.to_excel(output_path, index=False)
    return output_path

# Main function
if __name__ == "__main__":
    input_file_path = 'path_to_main_output.xlsx'  # The file path output by main.py
    processed_file_path = process_excel(input_file_path)
    print(f"Processed data saved to {processed_file_path}")
