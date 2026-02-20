from pathlib import Path


def read_file(file_path: str) -> str:
    """
    Reads a text file and returns its contents as a string.
    
    Args:
        file_path (str): Path to the instructions file.
    
    Returns:
        str: File contents.
    
    Raises:
        FileNotFoundError: If file does not exist.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Instructions file not found: {file_path}")

    return path.read_text(encoding="utf-8").strip()