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

fandom_link = "https://zelda.fandom.com/wiki/Armor_in_Tears_of_the_Kingdom"

with open("data/armor_list.json", "r") as f:
    dict_item = json.loads(f.read())

req = Request(fandom_link)
html = urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')

armor_type = ['Head Gear', 'Body Gear', 'Leg Gear']
armor_type_id = ['head_gear', 'body_gear', 'leg_gear']

items_ref = "categories/items"
armor_ref = "categories/armor"

all_table = soup.find_all('table')
for i in range(0, 3):
    armor_type_ref = f"categories/{armor_type_id[i]}"
    category_ref = [items_ref, armor_ref, armor_type_ref]
    table = all_table[i]
    items = table.find_all('tr')
    for item in items:
        item_data = item.find_all('td')
        '''
        Table with 4 column:
        1. Image + name
        2. Defense
        3. Effect
        4. Description
        '''
        if len(item_data) == 4:
            image_url = Utils.get_image_url(item_data[0].find('img'))
            item_id = Utils.string_to_id(item_data[0].text)
            name_html = item_data[0].find('b')
            name = name_html.text.strip()
            item_url = None
            a = name_html.find('a')
            if a is not None:
                item_url = 'https://zelda.fandom.com' + a['href']
                item_id = Utils.link_to_id(a['href'])
            description = item_data[3].text.strip()
            # Item detail
            attributes = {
                "Defense": item_data[1].text.strip(),
                "Effect": item_data[2].text.strip()
            }
            if item_url is not None:
                req = Request(item_url)
                html = urlopen(req).read()
                soup = BeautifulSoup(html, 'html.parser')
                aside = soup.find('aside')
                if aside is not None:
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
            print("Update item " + name)

    # break
with open("data/armor_list.json", 'w') as f:
    json.dump(dict_item, f, indent=True)
