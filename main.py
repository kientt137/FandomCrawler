import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.
cred = credentials.Certificate('src/Public/tears-of-the-kingdom-companion-firebase-adminsdk-dljty-8df1eba20e.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

enemies = db.collection(u'enemies')
docs = enemies.stream()

for doc in docs:

    dic = doc.to_dict()
    print(dic['name'])
    for item in dic['on_death']:
        dic_item = item.get().to_dict()
        print(dic_item['name'])
    # for item in doc.on_death:
    #     print(item.name)

for doc in docs:
    print(f'{doc.id} => {doc.to_dict()}')
