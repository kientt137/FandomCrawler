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

fandom_link = "https://zelda.fandom.com/wiki/Enemies_in_Tears_of_the_Kingdom"

with open("data/enemies_list.json", "r") as f:
    dict_item = json.loads(f.read())

req = Request(fandom_link)
html = urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')

enemies_type_id = ['normal_enemies', 'traps', 'overworld_bosses', 'bosses']

enemies_ref = "categories/enemies" # parent enemies

all_enemy_category = soup.find_all('ul', {"class": "gallery mw-gallery-traditional"})

for i in range(0, 4):
    ref = f"categories/{enemies_type_id[i]}"
    category_ref = [enemies_ref, ref]
    enemies_category = all_enemy_category[i]
    enemies = enemies_category.find_all('li')
    for enemy in enemies:
        name = enemy.find('p').text.strip()
        image_url = Utils.get_image_url(enemy.find('img'))
        url = None
        try:
            url = enemy.find('p').find('a')['href']
            item_id = Utils.link_to_id(url)
            item_url = 'https://zelda.fandom.com' + url
            attributes = {}
            if item_url is not None:
                req = Request(item_url)
                html = urlopen(req).read()
                soup = BeautifulSoup(html, 'html.parser')
                asides = soup.find_all('aside')
                if len(asides) > 0:
                    aside = asides[0]
                    divs = aside.findChildren("div")
                    for div in divs:
                        try:
                            title = div.h3.text
                            div_value = div.div
                            if div_value.ul is not None:
                                lis = div_value.ul.find_all('li')
                                value = []
                                for li in lis:
                                    value.append(li.text)
                                attributes[title] = '\n'.join(value)
                            else:
                                attributes[title] = div_value.text
                        except Exception as e:
                            pass
            if item_id not in dict_item:
                data = {
                    "item_id": item_id,
                    "name": name,
                    "description": None,
                    "image_url": image_url,
                    "category_ref": category_ref,
                    "item_url": item_url,
                    "attributes": attributes,
                    "additional": {}
                }
                dict_item[item_id] = data
            else:
                dict_item[item_id]["name"] = name
                dict_item[item_id]["description"] = None
                dict_item[item_id]["image_url"] = image_url
                dict_item[item_id]["item_url"] = item_url
            print("Update item " + name)
        except Exception as e:
            continue


with open("data/enemies_list.json", 'w') as f:
    json.dump(dict_item, f, indent=True)
