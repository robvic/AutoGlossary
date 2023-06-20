# Import dependencies
import pandas as pd
from io import BytesIO
from google.cloud import storage
from google.cloud import firestore

# Read from bucket
def read_bucket(data, context):
    file_name = data['name']
    bucket_name = data['bucket']

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)

    byte_stream = BytesIO()
    blob.download_to_file(byte_stream)
    byte_stream.seek(0)
    list = pd.read_excel(byte_stream, engine='openpyxl')

# Connect to Firebase
db = firestore.Client()

# Iterate each line
LIMIT = 5
for index, row in list.iterrows():
    if index == LIMIT: break
    # Save to Firebase
    doc_ref = db.collection('concepts').document(row['ID'])

    # Set data with document reference
    doc_ref.set({
        'Mnemonic': row['mnemonic'],
        'Concept': row['concept'],
        'Definition': row['definition'],
        'Field': row['field'],
        'Subfield': row['subfield']
    })