import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('src/Public/tears-of-the-kingdom-companion-firebase-adminsdk-dljty-8df1eba20e.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

list_item_file = [
    "data/armor_list.json",
    "data/weapon_list.json"
]

for file in list_item_file:
    with open(file, 'r') as f:
        items = json.loads(f.read())
        for item in items:
            refs = item['category_ref']
            list_ref = []
            if refs:
                for ref in refs:
                    ref_arr = ref.split('/')
                    items_ref = db.collection(ref_arr[0])
                    for i in range(1, len(ref_arr)):
                        items_ref = items_ref.document(ref_arr[i])
                    list_ref.append(items_ref)
                item['category_ref'] = list_ref
            doc_ref = db.collection(u'items').document(item['item_id'])
            doc_ref.set(item)
            print("sync 1 item successfully")