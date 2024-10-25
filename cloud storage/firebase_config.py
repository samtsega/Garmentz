import firebase_admin
from firebase_admin import credentials,storage

def initialize_firebase():
        cred = credentials.Certificate("path/to/your/firebase-key.json")
        firebase_admin.initialize_app(cred, { 'storageBucket': 'your-app.appspot.com' })
        def upload_to_firebase(file_path, destination_path):
            bucket = storage.bucket()
            blob = bucket.blob(destination_path)
            blob.upload_from_filename(file_path)