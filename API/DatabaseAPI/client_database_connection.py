from Database.db_interactions import (add_user, authenticate_user, check_username_unique,
                                      check_email_unique, username_exists, get_user_details,
                                      get_salt_user, check_license_unique, _PATIENT_DATA, _GET_TUMOR_IMAGE,
                                      _DOCTOR_ID, _MAKE_TUMOR_DIAGNOSIS, _GET_TUMOR_DIAGNOSIS_DETAILS)


def register_user(username, email, password, first_name, last_name, specialization, licence, PATH_):
    """
    Registers a new user by adding their details to the database.

    This function calls the add_user function to add the specified user details to the
    SQLite database. It returns a dictionary with the status, message, and a boolean
    indicating the success of the registration process.

    Parameters:
    username (str): The username of the new user.
    email (str): The email address of the new user.
    password (str): The plaintext password of the new user.
    first_name (str): The first name of the new user.
    last_name (str): The last name of the new user.
    specialization (str): The specialization of the new user.
    licence (str): The licence number of the new user.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    dict: A dictionary containing:
          - status (str): 'success' if the user is added successfully, 'error' otherwise.
          - message (str): A message indicating the registration status.
          - boolean (bool): True if the user is added successfully, False otherwise.

    Example:
    >>> register_user('DrSmith', 'drsmith@example.com', 'password123', 'John', 'Smith', 'Cardiology', 'XYZ123', 'path/to/database.db')
    {'status': 'success', 'message': 'User DrSmith added successfully!', 'boolean': True}
    """
    # Call the add_user function to add the user details to the database
    boolean = add_user(username=username,
                       email=email,
                       password=password,
                       first_name=first_name,
                       last_name=last_name,
                       specialization=specialization,
                       license_=licence,
                       PATH_=PATH_)

    # Return a dictionary with the result and a message
    if boolean:
        return {"status": "success", "message": f"User {username} added successfully!", "boolean": True}
    else:
        return {"status": "error", "message": f"User {username} already exists!", "boolean": False}


def authenticate(username, password, PATH_):
    """
    Authenticates a user based on the provided username and password.

    This function first retrieves the salt value for the specified username by calling
    the get_salt function. It then calls the authenticate_user function to verify the
    username and password using the retrieved salt. The function returns a dictionary
    with the status, message, and a boolean indicating the success of the authentication.

    Parameters:
    username (str): The username of the user to be authenticated.
    password (str): The plaintext password of the user to be authenticated.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    dict: A dictionary containing:
          - status (str): 'success' if the authentication is successful, 'error' otherwise.
          - message (str): A message indicating the authentication status.
          - boolean (bool): True if the user is authenticated, False otherwise.

    Example:
    >>> authenticate('DrSmith', 'password123', 'path/to/database.db')
    {'status': 'success', 'message': 'User DrSmith authenticated successfully!', 'boolean': True}
    """
    # Retrieve the salt value for the specified username
    salt = get_salt(username=username,
                    PATH_=PATH_)

    # Call the authenticate_user function to verify the username and password
    boolean = authenticate_user(username=username,
                                password=password,
                                salt=salt,
                                PATH_=PATH_)

    # Return a dictionary with the result and a message
    if boolean:
        return {"status": "success", "message": f"User {username} authenticated successfully!", "boolean": True}
    else:
        return {"status": "error", "message": f"User {username} not authenticated!", "boolean": False}


def logout_user(username):
    # Perform logout logic here
    return {"status": "success", "message": f"User {username} logged out successfully!"}


def check_username_uniqueness(username, PATH_):
    """
    Checks whether a given username is unique in the database.

    This function calls the check_username_unique function to determine if the specified
    username is unique in the SQLite database. It prints the result to the console and
    returns a dictionary with the status, message, and a boolean indicating uniqueness.

    Parameters:
    username (str): The username to be checked for uniqueness.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    dict: A dictionary containing:
          - status (str): 'success' if the username is unique, 'error' otherwise.
          - message (str): A message indicating the uniqueness of the username.
          - boolean (bool): True if the username is unique, False otherwise.

    Example:
    >>> check_username_uniqueness('DrSmith', 'path/to/database.db')
    {'status': 'success', 'message': 'Username DrSmith is unique!', 'boolean': True}
    """
    # Call the check_username_unique function to check if the username is unique
    boolean = check_username_unique(username=username,
                                    PATH_=PATH_)

    # Print the result to the console
    print("USERNAME IS UNIQUE:", boolean)

    # Return a dictionary with the result and a message
    if boolean:
        return {"status": "success", "message": f"Username {username} is unique!", "boolean": True}
    else:
        return {"status": "error", "message": f"Username {username} is not unique!", "boolean": False}


def check_licence_uniqueness(licence, PATH_):
    """
    Checks whether a given licence is unique in the database.

    This function calls the check_license_unique function to determine if the specified
    licence is unique in the SQLite database. It prints the result to the console and
    returns a dictionary with the status, message, and a boolean indicating uniqueness.

    Parameters:
    licence (str): The licence to be checked for uniqueness.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    dict: A dictionary containing:
          - status (str): 'success' if the licence is unique, 'error' otherwise.
          - message (str): A message indicating the uniqueness of the licence.
          - boolean (bool): True if the licence is unique, False otherwise.

    Example:
    >>> check_licence_uniqueness('XYZ123', 'path/to/database.db')
    {'status': 'success', 'message': 'Licence XYZ123 is unique!', 'boolean': True}
    """
    # Call the check_license_unique function to check if the licence is unique
    boolean = check_license_unique(license_=licence,
                                   PATH_=PATH_)

    # Print the result to the console
    print("LICENCE IS UNIQUE:", boolean)

    # Return a dictionary with the result and a message
    if boolean:
        return {"status": "success", "message": f"Licence {licence} is unique!", "boolean": True}
    else:
        return {"status": "error", "message": f"Licence {licence} is not unique!", "boolean": False}


def check_email_uniqueness(email, PATH_):
    """
    Checks whether a given email is unique in the database.

    This function calls the check_email_unique function to determine if the specified
    email is unique in the SQLite database. It prints the result to the console and
    returns a dictionary with the status, message, and a boolean indicating uniqueness.

    Parameters:
    email (str): The email to be checked for uniqueness.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    dict: A dictionary containing:
          - status (str): 'success' if the email is unique, 'error' otherwise.
          - message (str): A message indicating the uniqueness of the email.
          - boolean (bool): True if the email is unique, False otherwise.

    Example:
    >>> check_email_uniqueness('example@example.com', 'path/to/database.db')
    {'status': 'success', 'message': 'Email example@example.com is unique!', 'boolean': True}
    """
    # Call the check_email_unique function to check if the email is unique
    boolean = check_email_unique(email=email,
                                 PATH_=PATH_)

    # Print the result to the console
    print("EMAIL IS UNIQUE:", boolean)

    # Return a dictionary with the result and a message
    if boolean:
        return {"status": "success", "message": f"Email {email} is unique!", "boolean": True}
    else:
        return {"status": "error", "message": f"Email {email} is not unique!", "boolean": False}


def check_username_existence(username, PATH_):
    """
    Checks whether a given username exists in the database.

    This function calls the username_exists function to determine if the specified
    username exists in the SQLite database. It prints the result to the console and
    returns a dictionary with the status, message, and a boolean indicating existence.

    Parameters:
    username (str): The username to be checked for existence.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    dict: A dictionary containing:
          - status (str): 'success' if the username exists, 'error' otherwise.
          - message (str): A message indicating the existence of the username.
          - boolean (bool): True if the username exists, False otherwise.

    Example:
    >>> check_username_existence('DrSmith', 'path/to/database.db')
    {'status': 'success', 'message': 'Username DrSmith exists!', 'boolean': True}
    """
    # Call the username_exists function to check if the username exists
    boolean = username_exists(username=username,
                              PATH_=PATH_)

    # Print the result to the console
    print("USERNAME FOUND:", boolean)

    # Return a dictionary with the result and a message
    if boolean:
        return {"status": "success", "message": f"Username {username} exists!", "boolean": True}
    else:
        return {"status": "error", "message": f"Username {username} does not exist!", "boolean": False}


def get_details(username, PATH_):
    """
    Retrieves detailed information for a given user by calling the get_user_details function.

    This function acts as a simple wrapper around the get_user_details function, making
    the call to retrieve detailed information for the provided username from the specified
    database.

    Parameters:
    username (str): The username of the user whose details are to be retrieved.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    tuple: The detailed information for the specified user if found, otherwise None.

    Example:
    >>> get_details('DrSmith', 'path/to/database.db')
    ('DrSmith', 'John Smith', 'random_salt_value', ...)
    """
    # Call the get_user_details function to retrieve the detailed information
    details = get_user_details(username=username,
                               PATH_=PATH_)

    # Return the retrieved detailed information
    return details


def get_salt(username, PATH_):
    """
    Retrieves the salt value for a given user by calling the get_salt_user function.

    This function acts as a simple wrapper around the get_salt_user function, making
    the call to retrieve the salt for the provided username from the specified database.

    Parameters:
    username (str): The username of the user whose salt is to be retrieved.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    tuple: The salt value for the specified user if found, otherwise None.

    Example:
    >>> get_salt('DrSmith', 'path/to/database.db')
    ('random_salt_value',)
    """
    # Call the get_salt_user function to retrieve the salt value
    salt = get_salt_user(username=username,
                         PATH_=PATH_)

    # Return the retrieved salt value
    return salt


def get_patient_details(search_value, criteria, PATH_) -> dict:
    data = _PATIENT_DATA(search_value=search_value,
                  criteria=criteria,
                  PATH_=PATH_)

    return data

def get_tumor_image(patient_id, PATH_):
    print("Fetching tumor image...")
    image = _GET_TUMOR_IMAGE(patient_id=patient_id,
                             PATH_=PATH_)

    return image


def get_doctor_id(username, PATH_):
    id_ = _DOCTOR_ID(username=username,
                        PATH_=PATH_)

    return id_

def make_tumor_diagnosis(patient_id, tumor_type, PATH_):
    return _MAKE_TUMOR_DIAGNOSIS(patient_id=patient_id,
                                 tumor_type=tumor_type,
                                 PATH_=PATH_)

def get_tumor_diagnosis_details(patient_id, PATH_):
    data = get_patient_details(search_value=patient_id, criteria="patient_id", PATH_=PATH_)
    return _GET_TUMOR_DIAGNOSIS_DETAILS(patient_id=patient_id,
                                        PATH_=PATH_), data