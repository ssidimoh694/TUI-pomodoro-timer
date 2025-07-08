def print_debug(message: str, filepath: str = "debug.txt") -> None:
    """
    Appends the given message to the debug file on the next free line.
    """
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(f"{message}\n")