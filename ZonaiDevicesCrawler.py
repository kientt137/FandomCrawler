import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import validators
from Utilities import Utilities as Utils

# Use a service account.
cred = credentials.Certificate('src/Public/tears-of-the-kingdom-companion-firebase-adminsdk-dljty-8df1eba20e.json')

app = firebase_admin.initialize_app(cred)

db = firestore.client()

fandom_link = "https://zelda.fandom.com/wiki/Zonai_Devices"

dict_item = {}
with open("data/zonai_devices_list.json", "r") as f:
    dict_item = json.loads(f.read())


req = Request(fandom_link)
html = urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')

category_ref = ["categories/items", "categories/zonai_devices"]    # parent enemies

item_table = soup.find('table', {"class": "fandom-table"})
item_tr = item_table.find_all('tr')
for item in item_tr:
    tds = item.find_all('td')
    if len(tds) == 2:
        name = tds[0].text.strip()
        image_url = Utils.get_image_url(tds[0].find('img'))
        description = tds[1].text.strip()
        a = tds[0].find('b').find('a')
        if a is not None:
            item_id = Utils.link_to_id(a['href'])
            link = "https://zelda.fandom.com" + a["href"]
        else:
            item_id = Utils.string_to_id(name)
            link = None

        if item_id not in dict_item:
            data = {
                "item_id": item_id,
                "name": name,
                "description": description,
                "image_url": image_url,
                "category_ref": category_ref,
                "item_url": link,
                "attributes": {},
                "additional": {}
            }
            dict_item[item_id] = data
        else:
            dict_item[item_id]["name"] = name
            dict_item[item_id]["description"] = description
            dict_item[item_id]["image_url"] = image_url
            dict_item[item_id]["item_url"] = link
        print("Update item " + name)

with open("data/zonai_devices_list.json", 'w') as f:
    json.dump(dict_item, f, indent=True)
