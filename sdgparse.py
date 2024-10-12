
import os
import json
import platform

# Detect the operating system (this might still be useful depending on where the file is stored)
os_name = platform.system()

if os_name == 'Darwin':  # macOS
    home_directory = os.path.expanduser("~")
elif os_name == 'Linux':  # Linux
    home_directory = os.path.expanduser("~")
else:
    raise OSError("Unsupported operating system: Only macOS and Linux are supported.")

# Function to process a single file
def process_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    
    print(f"Processing file: {file_path}")
    
    try:
        with open(file_path, 'r') as file:
            # Assuming the file contains JSON data
            new_lines = file.readlines()
            for line in new_lines:
                try:
                    entry = json.loads(line)
                    if 'messages' in entry:
                        messages = entry['messages']
                        question = None
                        answer = None

                        for msg in messages:
                            if 'content' in msg and 'role' in msg:
                                if msg['role'] == 'pretraining':
                                    # Extract the last sentence of the question
                                    if '<|assistant|>' in msg['content']:
                                        full_question = msg['content'].split('<|assistant|>')[0].strip()
                                        question = full_question.split('.')[-1].strip() + '.'

                                    # Extract the answer content after <|assistant|> and before "role"
                                    if '<|assistant|>' in msg['content']:
                                        answer = msg['content'].split('<|assistant|>')[1].split('","role":"pretraining"')[0].strip()

                        if question and answer:
                            print(f"Question: {question}\nAnswer: {answer}\n")
                except json.JSONDecodeError:
                    # Handle invalid JSON lines, which might happen in partially written lines
                    continue
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python sdgparse.py <file_path>")
    else:
        input_file = sys.argv[1]
        process_file(input_file)
