import json

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