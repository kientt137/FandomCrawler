import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('src/Public/tears-of-the-kingdom-companion-firebase-adminsdk-dljty-8df1eba20e.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()


with open("data/category_list.json", 'r') as f:
    list_category = json.load(f)
    for key, value in list_category.items():
        doc_ref = db.collection(u'categories').document(key)
        doc_ref.set(value)