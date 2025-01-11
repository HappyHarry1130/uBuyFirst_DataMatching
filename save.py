import csv
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)


db = firestore.client()

def upload_excel_to_firestore(excel_file_path, collection_name):

    df = pd.read_excel(excel_file_path)

    for index, row in df.iterrows():
        row_dict = row.to_dict()
        db.collection(collection_name).add(row_dict)
        print(f"Added {row_dict} to Firestore")

if __name__ == "__main__":
    excel_file_path = 'watchbase rolex final.xlsx'  # Use absolute path
    collection_name = 'rorex'
    upload_excel_to_firestore(excel_file_path, collection_name)