
def read_txt_file(file_path: str) -> str:
    """
    This function reads the content of a file specified by the given path and returns it as a string.

    Args:
        file_path (str): The path to the file from which content will be read.

    Returns:
        str: The content of the file as a string.

    Example:
        >>> content = read_file("example.txt")
        >>> print(content)
        This will read the content of "example.txt" and print it.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If there is an issue opening or reading from the file.
    
    """
    if not file_path.lower().endswith('.txt'):
            file_path += '.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content
    
      






def write_txt_file(file_path: str, content: any) -> None:
    """
    This function writes the specified content to a file at the given path. If the file already exists, 
    it will be overwritten with the new content. If the file does not exist, it will be created.

    Args:
        file_path (str): The path of the file where content will be written.
        content (any): The content to write to the file. This can be a string, list, or any other type.
                       It will be converted to a string before being written to the file.

    Returns:
        None: This function does not return any value.

    Example:
        >>> write_file("output.txt", "This is the content of the file.")
        This writes the string "This is the content of the file." to the "output.txt" file.

    Raises:
        IOError: If there is an issue opening or writing to the file.
    
    """
    if not file_path.lower().endswith('.txt'):
            file_path += '.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content







def append_to_txt_file(file_path: str, content: any) -> None:
    """
    This function appends the specified content to a file at the given path. If the file does not exist,
    it will be created.

    Args:
        file_path (str): The path of the file to which content will be appended.
        content (any): The content to be appended to the file. This can be a string, list, or any other type.
                       It will be converted to a string before being written to the file.

    Returns:
        None

    """
    if not file_path.lower().endswith('.txt'):
            file_path += '.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        return content