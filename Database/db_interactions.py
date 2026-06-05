import hashlib
import sqlite3

from Database.salting import generate_salt

connection = None

def hash_password_using_sha3_and_scrypt(password, salt: tuple) -> str:
    """
    Hashes a given password using the provided salt and returns the hash value.

    This function combines the password with a salt and uses the SHA-512 algorithm
    to generate a secure hash. The salt should be a tuple of characters that will
    be joined into a string if not already in that form.

    Parameters:
    password (str): The plaintext password to be hashed.
    salt (tuple): A tuple of characters to be used as the salt for hashing.
                  If the salt is not a string, it will be converted into one.

    Returns:
    str: The resulting hash value as a hexadecimal string.

    Example:
    >>> hash_password_using_sha3_and_scrypt('myPassword123', ('s', 'a', 'l', 't'))
    'f54a9f...'
    """
    if type(salt) != str:
        salt = "".join(salt)

    sha3_512_hash: bytes = hashlib.sha3_512((password + salt).encode()).digest()

    scrypt_hash: bytes = hashlib.scrypt(sha3_512_hash, salt=salt.encode(), n=2**14, r=8, p=1, dklen=128)

    return scrypt_hash.hex()



# Insert a new user into the database
def add_user(username, email, password, first_name, last_name, specialization, license_, PATH_):
    """
    Adds a new user to the database.

    This function connects to the SQLite database specified by PATH_ and adds a new
    user with the provided details to the 'doctors' table. It hashes the password using
    a generated salt and handles potential database errors. The connection is properly closed
    after the operation.

    Parameters:
    username (str): The username of the new user.
    email (str): The email address of the new user.
    password (str): The plaintext password of the new user.
    first_name (str): The first name of the new user.
    last_name (str): The last name of the new user.
    specialization (str): The specialization of the new user.
    license_ (str): The license number of the new user.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    bool: True if the user is added successfully, False otherwise.

    Example:
    >>> add_user('DrSmith', 'drsmith@example.com', 'password123', 'John', 'Smith', 'Cardiology', 'XYZ123', 'path/to/database.db')
    True
    """
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # Generate a salt and hash the password
        SALT = generate_salt(512)
        password_hash = hash_password_using_sha3_and_scrypt(password, SALT)

        # SQL query to insert the new user
        insert_query = """
        INSERT INTO doctors (username, email, password_hash, salt, first_name, last_name, specialization, license_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor.execute(insert_query, (username, email, password_hash, SALT, first_name, last_name, specialization, license_))

        connection.commit()
        print(f"User {username} added successfully!")

        return True

    except sqlite3.IntegrityError as e:
        # Handle case where the user already exists
        print(f"Error: {e}")
        return False  # User already exists

    except sqlite3.Error as e:
        # Handle general SQLite errors
        print(f"Error: {e}")
        return False

    except Exception as e:
        # Handle any other exceptions
        print(f"Error: {e}")
        return False

    finally:
        # Ensure that the database connection is closed
        connection.close()



def authenticate_user(username, password, salt, PATH_):
    """
    Authenticates a user based on the provided username, password, and salt.

    This function connects to the SQLite database specified by PATH_ and retrieves
    the user details associated with the provided username from the 'doctors' table.
    It hashes the provided password using the given salt and compares it to the stored
    hash to authenticate the user. It handles potential database errors and ensures the
    connection is properly closed.

    Parameters:
    username (str): The username of the user to be authenticated.
    password (str): The plaintext password of the user to be authenticated.
    salt (tuple): The salt value to be used for hashing the password.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    bool: True if the authentication is successful, False otherwise.

    Example:
    >>> authenticate_user('DrSmith', 'password123', ('s', 'a', 'l', 't'), 'path/to/database.db')
    True
    """
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # SQL query to select the user by username
        select_query = "SELECT * FROM doctors WHERE username = ?;"
        cursor.execute(select_query, (username,))

        # Fetch the first result from the executed query
        user = cursor.fetchone()

        if user:
            # Hash the provided password and compare with the stored hash
            provided_password_hash = hash_password_using_sha3_and_scrypt(password, salt)
            if provided_password_hash == user[3]:
                print("Authentication successful!")
                return True  # Authentication successful
            else:
                return False  # Incorrect password
        else:
            return False  # User not found

    except sqlite3.Error as e:
        # Print the error message if an SQLite error occurs
        print(f"Error: {e}")
        return False

    finally:
        # Ensure that the database connection is closed
        connection.close()



def remove_user(identifier, PATH_, by="username"):
    """
    Removes a user from the database by username or user_id.

    This function connects to the SQLite database specified by PATH_ and removes the
    user identified by the provided identifier, which can be a username or user_id,
    from the 'doctors' table. It handles potential database errors and ensures the
    connection is properly closed.

    Parameters:
    identifier (str): The value of the username or user_id to identify the user.
    by (str): The column to use for identification ("username" or "user_id").
    PATH_ (str): The file path to the SQLite database.

    Returns:
    None

    Example:
    >>> remove_user('DrSmith', 'path/to/database.db', by="username")
    >>> remove_user('12345', 'path/to/database.db', by="user_id")
    """
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # Determine the column to use for identification
        if by == "doctor_id":
            delete_query = "DELETE FROM doctors WHERE doctor_id = ?;"
        elif by == "username":
            delete_query = "DELETE FROM doctors WHERE username = ?;"
        else:
            print("Error: Invalid identifier type. Use 'username' or 'doctor_id'.")
            return

        # Execute the delete query
        cursor.execute(delete_query, (identifier,))
        connection.commit()

        # Check the number of affected rows and print the result
        if cursor.rowcount > 0:
            print(f"User with {by} '{identifier}' removed successfully.")
        else:
            print(f"No user found with {by} '{identifier}'.")

    except sqlite3.Error as e:
        # Print the error message if an SQLite error occurs
        print(f"Error: {e}")

    finally:
        # Ensure that the database connection is closed
        connection.close()



def check_username_unique(username, PATH_):
    """
    Checks whether a given username is unique in the database.

    This function connects to the SQLite database specified by PATH_ and retrieves
    the user details associated with the provided username from the 'doctors' table.
    It handles potential database errors and ensures the connection is properly closed.

    Parameters:
    username (str): The username to be checked for uniqueness.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    bool: True if the username is unique, False otherwise.

    Example:
    >>> check_username_unique('DrSmith', 'path/to/database.db')
    True
    """
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # SQL query to select the user by username
        select_query = "SELECT * FROM doctors WHERE username = ?;"
        cursor.execute(select_query, (username,))

        # Fetch the first result from the executed query
        user = cursor.fetchone()

        # Check if the username is unique and return the result
        if user:
            return False  # Username already exists
        else:
            return True  # Username is unique

    except sqlite3.Error as e:
        # Print the error message if an SQLite error occurs
        print(f"Error: {e}")
        return False

    finally:
        # Ensure that the database connection is closed
        connection.close()



def check_license_unique(license_, PATH_):
    """
    Checks whether a given license number is unique in the database.

    This function connects to the SQLite database specified by PATH_ and retrieves
    the user details associated with the provided license number from the 'doctors' table.
    It handles potential database errors and ensures the connection is properly closed.

    Parameters:
    license_ (str): The license number to be checked for uniqueness.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    bool: True if the license number is unique, False otherwise.

    Example:
    >>> check_license_unique('XYZ123', 'path/to/database.db')
    True
    """
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # SQL query to select the user by license number
        select_query = "SELECT * FROM doctors WHERE license_number = ?;"
        cursor.execute(select_query, (license_,))

        # Fetch the first result from the executed query
        user = cursor.fetchone()

        # Check if the license number is unique and return the result
        if user:
            return False  # License already exists
        else:
            return True  # License is unique

    except sqlite3.Error as e:
        # Print the error message if an SQLite error occurs
        print(f"Error: {e}")
        return False

    finally:
        # Ensure that the database connection is closed
        connection.close()



def check_email_unique(email, PATH_):
    """
    Checks whether a given email is unique in the database.

    This function connects to the SQLite database specified by PATH_ and retrieves
    the user details associated with the provided email from the 'doctors' table.
    It handles potential database errors and ensures the connection is properly closed.

    Parameters:
    email (str): The email to be checked for uniqueness.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    bool: True if the email is unique, False otherwise.

    Example:
    >>> check_email_unique('example@example.com', 'path/to/database.db')
    True
    """
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # SQL query to select the user by email
        select_query = "SELECT * FROM doctors WHERE email = ?;"
        cursor.execute(select_query, (email,))

        # Fetch the first result from the executed query
        user = cursor.fetchone()

        # Check if the email is unique and return the result
        if user:
            return False  # Email already exists
        else:
            return True  # Email is unique

    except sqlite3.Error as e:
        # Print the error message if an SQLite error occurs
        print(f"Error: {e}")
        return False

    finally:
        # Ensure that the database connection is closed
        connection.close()



def username_exists(username, PATH_):
    """
    Checks whether a given username exists in the database.

    This function connects to the SQLite database specified by PATH_ and retrieves
    the user details associated with the provided username from the 'doctors' table.
    It handles potential database errors and ensures the connection is properly closed.

    Parameters:
    username (str): The username to be checked for existence.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    bool: True if the username exists, False otherwise.

    Example:
    >>> username_exists('DrSmith', 'path/to/database.db')
    True
    """
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # SQL query to select the user by username
        select_query = "SELECT * FROM doctors WHERE username = ?;"
        cursor.execute(select_query, (username,))

        # Fetch the first result from the executed query
        user = cursor.fetchone()

        # Check if the user exists and return the result
        if user:
            return True  # Username exists
        else:
            return False  # Username does not exist

    except sqlite3.Error as e:
        # Print the error message if an SQLite error occurs
        print(f"Error: {e}")
        return False

    finally:
        # Ensure that the database connection is closed
        connection.close()



def get_user_details(username, PATH_):
    """
    Retrieves detailed information for a given user from the database.

    This function connects to the SQLite database specified by PATH_ and retrieves
    all details associated with the provided username from the 'doctors' table. It
    handles potential database errors and ensures the connection is properly closed.

    Parameters:
    username (str): The username of the user whose details are to be retrieved.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    tuple: A tuple containing all details of the specified user if found, otherwise None.

    Example:
    >>> get_user_details('DrSmith', 'path/to/database.db')
    ('DrSmith', 'John Smith', 'Cardiology', 'drsmith@example.com', ...)
    """
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # SQL query to select all details for the given username
        select_query = "SELECT * FROM doctors WHERE username = ?;"
        cursor.execute(select_query, (username,))

        # Fetch the first result from the executed query
        user = cursor.fetchone()

        # Return the user details
        return user

    except sqlite3.Error as e:
        # Print the error message if an SQLite error occurs
        print(f"Error: {e}")
        return None

    finally:
        # Ensure that the database connection is closed
        connection.close()


def _DOCTOR_ID(username, PATH_):
    """
    Retrieves the ID for a given user from the database.

    This function connects to the SQLite database specified by PATH_ and retrieves
    the ID associated with the provided username from the 'doctors' table. It
    handles potential database errors and ensures the connection is properly closed.

    Parameters:
    username (str): The username of the user whose ID is to be retrieved.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    tuple: The ID for the specified user if found, otherwise None.

    Example:
    >>> _DOCTOR_ID('DrSmith', 'path/to/database.db')
    ('12345',)
    """
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # SQL query to select the ID for the given username
        select_query = "SELECT doctor_id FROM doctors WHERE username = ?;"
        cursor.execute(select_query, (username,))

        # Fetch the first result from the executed query
        ID = cursor.fetchone()

        # Return the ID value
        return ID

    except sqlite3.Error as e:
        # Print the error message if an SQLite error occurs
        print(f"Error: {e}")
        return None

    finally:
        # Ensure that the database connection is closed
        connection.close()



def get_salt_user(username, PATH_):
    """
    Retrieves the salt value for a given user from the database.

    This function connects to the SQLite database specified by PATH_ and retrieves
    the salt associated with the provided username from the 'doctors' table. It
    handles potential database errors and ensures the connection is properly closed.

    Parameters:
    username (str): The username of the user whose salt is to be retrieved.
    PATH_ (str): The file path to the SQLite database.

    Returns:
    tuple: The salt value for the specified user if found, otherwise None.

    Example:
    >>> get_salt_user('DrSmith', 'path/to/database.db')
    ('random_salt_value',)
    """
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # SQL query to select the salt for the given username
        select_query = "SELECT salt FROM doctors WHERE username = ?;"
        cursor.execute(select_query, (username,))

        # Fetch the first result from the executed query
        salt = cursor.fetchone()

        # Return the salt value
        return salt

    except sqlite3.Error as e:
        # Print the error message if an SQLite error occurs
        print(f"Error: {e}")
        return None

    finally:
        # Ensure that the database connection is closed
        connection.close()


def _PATIENT_DATA(search_value, criteria, PATH_):
    """Fetch patient record from the database and return as a dictionary."""
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # Ensure criteria is valid to prevent SQL injection
        valid_criteria = {"patient_id", "email", "phone_number"}
        if criteria not in valid_criteria:
            print("Invalid search criteria")
            return None

        # SQL query to select the patient record based on search criteria
        select_query = f"""
            SELECT patient_id, first_name, last_name, date_of_birth, gender, phone_number, email 
            FROM patients WHERE {criteria} = ?;
            """
        cursor.execute(select_query, (search_value,))

        # Fetch the first result from the executed query
        patient = cursor.fetchone()

        # Return patient data as a dictionary
        if patient:
            return {
                "patient_id": patient[0],
                "first_name": patient[1],
                "last_name": patient[2],
                "date_of_birth": patient[3],
                "gender": patient[4],
                "phone_number": patient[5],
                "email": patient[6],
            }
        return None

    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return None

    finally:
        if connection:
            connection.close()


def _GET_TUMOR_IMAGE(patient_id, PATH_):
    """Fetch tumor image vector for a given patient_id from the database."""
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # SQL query to fetch the image vector for the given patient ID
        select_query = """
        SELECT image_vector FROM patient_image_vector WHERE patient_id = ? ORDER BY uploaded_at DESC LIMIT 1;
        """
        cursor.execute(select_query, (patient_id,))

        # Fetch the first image vector result
        image_vector = cursor.fetchone()

        # Return the image vector if found, otherwise None
        return image_vector[0] if image_vector else None

    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return None

    finally:
        if connection:
            connection.close()


def _MAKE_TUMOR_DIAGNOSIS(patient_id, tumor_type, PATH_):
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # SQL query to insert a new diagnosis record
        insert_query = """
        INSERT INTO patient_diagnoses (patient_id, diagnosis)
        VALUES (?, ?);
        """
        cursor.execute(insert_query, (patient_id, tumor_type))

        # Commit the changes to the database
        connection.commit()

        return True

    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return False

    finally:
        if connection:
            connection.close()

def _GET_TUMOR_DIAGNOSIS_DETAILS(patient_id, PATH_):
    # return only one
    global connection
    try:
        # Establish a connection to the SQLite database
        connection = sqlite3.connect(PATH_)
        cursor = connection.cursor()

        # SQL query to fetch the image vector for the given patient ID
        select_query = """
        SELECT diagnosis_id, diagnosis, created_at FROM patient_diagnoses WHERE patient_id = ?;
        """
        cursor.execute(select_query, (patient_id,))

        # Fetch the first image vector result
        diagnosis = cursor.fetchone()

        # Return the image vector if found, otherwise None
        return diagnosis

    except sqlite3.Error as e:
        print(f"Database Error: {e}")
        return None

    finally:
        if connection:
            connection.close()
