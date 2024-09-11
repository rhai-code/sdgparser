import json

file_path = '/Users/gshipley/Library/Application Support/instructlab/datasets/knowledge_train_msgs_2024-08-27T19_24_34.jsonl'

# Open and process the JSONL file
qa_pairs = []
with open(file_path, 'r') as file:
    for line in file:
        entry = json.loads(line)
        if 'messages' in entry:
            messages = entry['messages']
            question = None
            answer = None
            
            for msg in messages:
                if 'content' in msg and 'role' in msg:
                    if msg['role'] == 'pretraining':
                        # Extract the question content before <|assistant|>
                        if '<|assistant|>' in msg['content']:
                            full_question = msg['content'].split('<|assistant|>')[0].strip()
                            # Extract the last sentence of the question
                            question = full_question.split('.')[-1].strip() + '.'
                            
                        # Extract the answer content after <|assistant|> and before "role"
                        if '<|assistant|>' in msg['content']:
                            answer = msg['content'].split('<|assistant|>')[1].split('","role":"pretraining"')[0].strip()

            if question and answer:
                qa_pairs.append((question, answer))

# Print extracted question-answer pairs (with last sentence of the question only)
for q, a in qa_pairs:
    print(f"Question: {q}\nAnswer: {a}\n")

