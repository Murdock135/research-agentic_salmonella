# utils.py

def load_text(file_path):
    """Loads text from a file."""
    with open(file_path, 'r') as f:
        text = f.read()

    return text
