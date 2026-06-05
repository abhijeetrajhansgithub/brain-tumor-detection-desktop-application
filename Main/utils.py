import os

def get_current_system_path():
    """
    Get the current system path of the script.

    This function retrieves the absolute directory path where the current script is located.
    It is particularly useful for determining file paths relative to the script.

    Returns:
        str: The absolute directory path of the current script.
    """
    # Get the absolute path of the current script
    current_script_path = os.path.abspath(__file__)

    # Extract the directory name from the absolute path
    current_directory = os.path.dirname(current_script_path)
    return current_directory


def change_path_to_db(path):
    """
    Modify the provided path to point to the doctor authentication database.

    This function takes a given path, truncates the last four characters, 
    and appends the relative path to the doctor authentication database file.
    It is useful for dynamically constructing paths to database files.

    Args:
        path (str): The original path string that needs to be modified.

    Returns:
        str: The modified path string that points to the doctor authentication database.
    """
    # Remove the last four characters from the path (e.g., a file extension or other suffix)
    main_path_directory = path[:-4]
    print(main_path_directory)

    # Append the relative path to the doctor authentication database file
    # db_path_directory = main_path_directory + r"Database\medical_database.db"
    db_path_directory = r"B:\Computer Science and Engineering\ImageClassificationDesktopApp\Database\medical_database.db"
    return db_path_directory
