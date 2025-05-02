import os



def create_folder(folder_name: str) -> None:
    """
    Create a new folder.

    Args:
        folder_path (str): Name of the folder to create.
    
    Returns:
        None
    """
    try:
        os.makedirs(folder_name, exist_ok=False)
        print(f'Folder {folder_name} created succesfully.')
    except:
        print(f'Folder {folder_name} already exists.')







def rename_files(folder_path: str, prefix="", start_index=0) -> None:
    """
    Renames all files in the given folder with a specified prefix and index.

    Args:
        folder_path (str): Folder to renamen.
        prefix (str): Prefix of the new files name. Default is `""`.
        start_index (int): Start index for renaming the files. Default is `0`

    Returns:
        None

    """
    if not os.path.isdir(folder_path):
        print(f"Error: {folder_path} is not a valid directory.")
        return

    files = sorted(os.listdir(folder_path))  # Sort to maintain order
    dash = '_' if prefix != '' else ''
    for index, filename in enumerate(files, start=start_index):
        old_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(old_path):  # Ensure it's a file, not a folder
            extension = os.path.splitext(filename)[1]  # Keep the original file extension
            new_name = f"{prefix}{dash}{index}{extension}"
            new_path = os.path.join(folder_path, new_name)
            
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} → {new_name}")








def delete_file(file_path: str) -> None:
    """
    Deletes a file if it exists.
    
    Args:
        file_path (str): File to delete.
    
    Returns
        None
    """
    try:
        os.remove(file_path)
        print(f"File '{file_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except PermissionError:
        print(f"Error: Permission denied for '{file_path}'.")







def delete_folder(folder_path: str) -> None:
    """
    Deletes an empty folder.
    
    Args:
        folder_path (str): Folder to delete.

    Returns:
        None
    """
    try:
        os.rmdir(folder_path)
        print(f"Folder '{folder_path}' deleted successfully.")
    except FileNotFoundError:
        print(f"Error: Folder '{folder_path}' not found.")
    except OSError:
        print(f"Error: Folder '{folder_path}' is not empty.")








def get_all_file_names_in_a_folder(folder_path: str) -> list[str]:
    """
    Get a list of all file names in the specified folder, excluding `.DS_Store`.

    Args:
        folder_path (str): The path to the folder.

    Returns:
        list[str]: A list of file names.
    
    Example:
        >>> get_files_all_files_name("path/to/folder")
        ['file1.txt', 'image.png', 'document.pdf']
    """
    return [f for f in os.listdir(folder_path) 
            if os.path.isfile(os.path.join(folder_path, f)) and f != ".DS_Store"]




