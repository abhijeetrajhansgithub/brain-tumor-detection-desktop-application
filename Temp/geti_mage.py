from API.DatabaseAPI.client_database_connection import get_tumor_image

image = get_tumor_image(patient_id=1, PATH_='B:\Computer Science and Engineering\ImageClassificationDesktopApp\Database\medical_database.db')

print(image)