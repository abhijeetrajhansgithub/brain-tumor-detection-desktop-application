import sqlite3

connection = None

def remove_all():
    global connection
    try:
        connection = sqlite3.connect(r"B:\Computer Science and Engineering\ImageClassificationDesktopApp\Database\medical_database.db")
        cursor = connection.cursor()

        # SQL to delete all users
        delete_query = "DELETE FROM patient_image_vector;"
        cursor.execute(delete_query)

        connection.commit()
        print("All users removed successfully!")

    except sqlite3.Error as e:
        print(f"Error: {e}")

    finally:
        if connection:
            connection.close()

    return

remove_all()