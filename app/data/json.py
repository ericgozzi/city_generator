import os
import json




def export_json(data, file_path):
    """
    Exports data to a JSON file.

    Args:
        data (dict or list): The data to be saved in JSON format.
        file_path (str): The path to the JSON file.

    Returns:
        None
    """
    # Write data to the file
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4)






def add_to_json(file_path, new_item):
    """
    Adds a new item to a JSON file. Raises an error if the file does not exist.

    Args:
        file_path (str): The path to the JSON file.
        new_item (dict or list): The item to be added. If the JSON file contains a list, 
                                 the item is appended. If it contains a dictionary, it must be merged.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the JSON structure is not a list or dictionary.

    Returns:
        None
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' does not exist.")

    # Read the existing data
    with open(file_path, "r", encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"Error: The file '{file_path}' contains invalid JSON.")

    # Ensure the JSON structure allows adding new items
    if isinstance(data, list):
        data.append(new_item)
    elif isinstance(data, dict) and isinstance(new_item, dict):
        data.update(new_item)  # Merge dictionaries
    else:
        raise ValueError("Unsupported JSON format. Expected a list or a dictionary.")

    # Write the updated data back to the file
    with open(file_path, "w", encoding='utf-8') as file:
        json.dump(data, file, indent=4)






def read_json(file_path):
    """
    Reads and returns the contents of a JSON file.

    Args:
        file_path (str): The path to the JSON file.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file contains invalid JSON.

    Returns:
        dict or list: The parsed JSON data.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' does not exist.")

    # Read and parse the JSON file
    with open(file_path, "r", encoding='utf-8') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            raise ValueError(f"Error: The file '{file_path}' contains invalid JSON.")