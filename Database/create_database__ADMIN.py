import sqlite3


def create_doctors_table():
    # Connect to SQLite database (or create it if it doesn't exist)
    connection = sqlite3.connect(r"B:\Computer Science and Engineering\ImageClassificationDesktopApp\Database\medical_database.db")

    # Create a cursor object to interact with the database
    cursor = connection.cursor()

    # SQL to create the doctors table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS doctors (
        doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        salt TEXT,
        is_active BOOLEAN DEFAULT 1,
        is_verified BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        reset_token TEXT,
        reset_token_expiration TIMESTAMP,
        failed_attempts INTEGER DEFAULT 0,
        lockout_time TIMESTAMP,
        first_name TEXT,
        last_name TEXT,
        phone_number TEXT,
        two_fa_enabled BOOLEAN DEFAULT 0,
        two_fa_secret TEXT,
        specialization TEXT,
        license_number TEXT UNIQUE NOT NULL
    );
    """

    # Execute the query
    cursor.execute(create_table_query)

    # Commit changes and close the connection
    connection.commit()
    connection.close()

    print("Doctor authentication database and table created successfully!")


def create_patients_table():
    # Connect to SQLite database
    connection = sqlite3.connect(r"B:\Computer Science and Engineering\ImageClassificationDesktopApp\Database\medical_database.db")
    cursor = connection.cursor()

    # SQL to create the patients table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        date_of_birth DATE NOT NULL,
        gender TEXT CHECK(gender IN ('Male', 'Female', 'Other')) NOT NULL,
        phone_number TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE,
        address TEXT,
        medical_history TEXT,
        doctor_id INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id) ON DELETE CASCADE
    );
    """

    # Execute the query
    cursor.execute(create_table_query)

    # Commit changes and close the connection
    connection.commit()
    connection.close()

    print("Patient records table created successfully!")


def create_patient_image_vectors_table():
    import sqlite3

    # Connect to SQLite database
    connection = sqlite3.connect(r"B:\Computer Science and Engineering\ImageClassificationDesktopApp\Database\medical_database.db")
    cursor = connection.cursor()

    # SQL to create the patient_images table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS patient_image_vector (
        image_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL,
        image_vector BLOB NOT NULL,
        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
    );
    """

    # Execute the query
    cursor.execute(create_table_query)

    # Commit changes and close the connection
    connection.close()

    print("Patient images table created successfully!")

    return


def create_patient_diagnosiss_table():
    import sqlite3

    # Connect to SQLite database
    connection = sqlite3.connect(r"B:\Computer Science and Engineering\ImageClassificationDesktopApp\Database\medical_database.db")
    cursor = connection.cursor()

    # SQL to create the patient_diagnoses table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS patient_diagnoses (
        diagnosis_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER NOT NULL UNIQUE,
        diagnosis TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (patient_id) REFERENCES patients(patient_id) ON DELETE CASCADE
    );
    """

    # Execute the query
    cursor.execute(create_table_query)

    # Commit changes and close the connection
    connection.close()

    print("Patient diagnoses table created successfully!")


create_patient_diagnosiss_table()