import time
import os
import json
import platform
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# Detect the operating system
os_name = platform.system()

# Set the directory to watch based on the OS
if os_name == 'Darwin':  # macOS
    home_directory = os.path.expanduser("~")
    watch_directory = os.path.join(home_directory, 'Library/Application Support/instructlab/datasets/')
elif os_name == 'Linux':  # Linux
    home_directory = os.path.expanduser("~")
    watch_directory = os.path.join(home_directory, '.local/share/instructlab/datasets/')
else:
    raise OSError("Unsupported operating system: Only macOS and Linux are supported.")

print(f"Watching directory: {watch_directory}")

file_pattern = 'knowledge_train_msgs*'

# Store file pointers to track the last read position for each file
file_positions = {}

# Define an event handler class
class FileChangeHandler(PatternMatchingEventHandler):
    def __init__(self):
        super().__init__(patterns=[os.path.join(watch_directory, file_pattern)])

    def process_new_lines(self, file_path):
        # Open the file and seek to the last known position
        with open(file_path, 'r') as file:
            if file_path not in file_positions:
                file_positions[file_path] = 0  # Initialize if we haven't seen this file before

            # Move to the last read position
            file.seek(file_positions[file_path])

            # Read new lines
            new_lines = file.readlines()

            # Update the file position
            file_positions[file_path] = file.tell()

            # Process each new line
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

    def on_modified(self, event):
        if not event.is_directory:
            self.process_new_lines(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self.process_new_lines(event.src_path)

# Set up the observer
observer = Observer()
event_handler = FileChangeHandler()
observer.schedule(event_handler, path=watch_directory, recursive=False)

# Start watching the directory
observer.start()

print("Observer started. Watching for changes...")

try:
    while True:
        time.sleep(1)  # Keep the script running
except KeyboardInterrupt:
    observer.stop()

observer.join()
