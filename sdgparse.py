import os
import json
import platform
import re

# Detect the operating system
os_name = platform.system()

if os_name == 'Darwin' or os_name == 'Linux':  # macOS or Linux
    home_directory = os.path.expanduser("~")
else:
    raise OSError("Unsupported operating system: Only macOS and Linux are supported.")

def process_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    print(f"Processing file: {file_path}")
    
    try:
        with open(file_path, 'r') as file:
            for line in file:
                try:
                    entry = json.loads(line)
                    if 'messages' in entry:
                        for msg in entry['messages']:
                            if 'content' in msg:
                                content = msg['content']
                                question_match = re.search(r'(.*?)\n<\|assistant\|>', content, re.DOTALL)
                                answer_match = re.search(r'<\|assistant\|>\n(.*?)\n\[End\]', content, re.DOTALL)
                                
                                if question_match and answer_match:
                                    question = question_match.group(1).strip().split('\n')[-1]
                                    answer = answer_match.group(1).strip()
                                    print(f"Question: {question}\nAnswer: {answer}\n")
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python sdgparse.py <file_path>")
    else:
        input_file = sys.argv[1]
        process_file(input_file)
