import csv
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
# Initialize Firebase Admin SDK
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Function to upload CSV data to Firestore

# ... existing imports ...

def upload_excel_to_firestore(excel_file_path, collection_name):
    # Read the Excel file
    df = pd.read_excel(excel_file_path)

    # Iterate over DataFrame rows as dictionaries
    for index, row in df.iterrows():
        # Convert row to dictionary
        row_dict = row.to_dict()
        # Add each row to Firestore
        db.collection(collection_name).add(row_dict)
        print(f"Added {row_dict} to Firestore")

# Example usage
if __name__ == "__main__":
    excel_file_path = 'watchbase rolex final.xlsx'  # Use absolute path
    collection_name = 'rorex'
    upload_excel_to_firestore(excel_file_path, collection_name)