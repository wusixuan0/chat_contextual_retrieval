import json
# from filelock import FileLock
# TODO: add filelock

# def atomic_write_json(data, file_path):
#     lock_path = f"{file_path}.lock"
#     with FileLock(lock_path):
#         # Write to temp file
#         temp_path = f"{file_path}.temp"
#         with open(temp_path, 'w') as f:
#             json.dump(data, f)
#         # Atomic rename
#         os.replace(temp_path, file_path)

def read_text_file(file_path):
    """Reads the entire content of a text file as a single string."""
    with open(file_path, 'r') as f:
        data = f.read()
    return data

def write_text_file(data, file_path):
    """Writes a string to a text file."""
    with open(file_path, 'w') as f:
        f.write(data)
    print(f"Text data saved to {file_path}")

def write_json_file(data, file_path):
    """Writes a JSON object to a file."""
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"JSON data saved to {file_path}")

def load_json_file(file_path):
    """Loads a JSON object from a file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def messages_array_to_text(history, file_path):
    # turn messages array to plain text (for gemini-2.0-flash-thinking-exp)
    chat_history = ''.join([part for message in history for part in message['parts']])
    write_text_file(chat_history, file_path)