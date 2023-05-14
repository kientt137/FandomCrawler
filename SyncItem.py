import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
#PRODUCTION
# cred = credentials.Certificate('src/Public/tears-of-the-kingdom-companion-firebase-adminsdk-dljty-8df1eba20e.json')

#DEVELOPMENT
cred = credentials.Certificate('src/Public/totk-companion-dev-firebase-adminsdk-kee1u-a4ac96060a.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

list_item_file = [
    "data/armor_list.json",
    "data/weapon_list.json",
    "data/zonai_devices_list.json",
    "data/enemies_list.json",
    "data/location.json"
]

for file in list_item_file:
    with open(file, 'r') as f:
        print("Sync file " + file)
        items = json.loads(f.read())
        for key, item in items.items():
            doc_ref = db.collection(u'items').document(item['item_id'])
            doc_ref.set(item)
            print("sync 1 item successfully")
