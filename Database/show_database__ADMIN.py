import tabulate
import sqlite3

connection = None

def show_data_formatted():
    global connection
    try:
        connection = sqlite3.connect(r"B:\Computer Science and Engineering\ImageClassificationDesktopApp\Database\medical_database.db")
        cursor = connection.cursor()

        # Fetch data from the "users" table
        cursor.execute("SELECT * FROM patient_image_vector")
        rows = cursor.fetchall()

        # Fetch column names
        column_names = [description[0] for description in cursor.description]

        # Format and display the data as a table
        formatted_data = tabulate.tabulate(rows, headers=column_names, tablefmt="grid")
        print(formatted_data)

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if connection:
            connection.close()

show_data_formatted()
