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

fandom_link = "https://zelda.fandom.com/wiki/Weapon#Breath_of_the_Wild"

with open("data/weapon_list.json", "r") as f:
    dict_item = json.loads(f.read())

req = Request(fandom_link)
html = urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')

category_ref = ["categories/items", "categories/weapons"]

table = soup.find('table')

items = table.find_all('tr')
for item in items:
    item_data = item.find_all('td')
    if len(item_data) == 8:
        name = item_data[0].text.strip()
        image_url = Utils.get_image_url(item_data[0].find('img'))
        item_id = Utils.string_to_id(item_data[0].text)
        description = item_data[7].text.strip()
        a = item_data[0].find('b').find('a')
        if a is not None:
            item_id = Utils.link_to_id(a['href'])
            item_url = "https://zelda.fandom.com" + a["href"]
        else:
            item_id = Utils.string_to_id(name)
            item_url = None
        attributes = {
            "Compendium No.": item_data[1].text.strip(),
            "Archetype": item_data[2].text.strip(),
            "Category": item_data[3].text.strip(),
            "Can use a shield simultaneously": item_data[4].text.strip(),
            "Attack": item_data[5].text.strip(),
            "Durability": item_data[6].text.strip(),
        }
        if item_id not in dict_item:
            data = {
                "item_id": item_id,
                "name": name,
                "description": description,
                "image_url": image_url,
                "category_ref": category_ref,
                "item_url": item_url,
                "attributes": attributes,
                "additional": {}
            }
            dict_item[item_id] = data
        else:
            dict_item[item_id]["name"] = name
            dict_item[item_id]["description"] = description
            dict_item[item_id]["image_url"] = image_url
            dict_item[item_id]["item_url"] = item_url
            dict_item[item_id]["attributes"] = attributes
        print("Update item " + name)
with open("data/weapon_list.json", 'w') as f:
    json.dump(dict_item, f, indent=True)