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

array_item = []
fandom_link = "https://zelda.fandom.com/wiki/Armor_in_Tears_of_the_Kingdom"

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
        if len(item_data) == 4:
            image_url = None
            img_html = item_data[0].find_all('img')
            if len(img_html) == 1:
                if img_html[0].has_attr('src'):
                    image_url = img_html[0]['src']
                    if not validators.url(image_url):
                        image_url = None
                        if img_html[0].has_attr('data-src'):
                            image_url = img_html[0]['data-src']
                            if not validators.url(image_url):
                                image_url = None

            item_id = Utils.string_to_id(item_data[0].text)
            name_html = item_data[0].find_all('b')
            item_url = None
            if len(name_html) == 1:
                a = name_html[0].find_all('a')
                if len(a) == 1:
                    item_url = 'https://zelda.fandom.com' + a[0]['href']

            # Item detail
            attributes = {
                "Defense": item_data[1].text.strip(),
                "Effect": item_data[2].text.strip()
            }
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
            data = {
                "item_id": item_id,
                "name": item_data[0].text.strip(),
                "description": item_data[3].text.strip(),
                "image_url": image_url,
                "category_ref": category_ref,
                "item_url": item_url,
                "attributes": attributes
            }
            array_item.append(data)
            print(data)
    # break
with open("data/armor_list.json", 'w') as f:
    json.dump(array_item, f, indent=True)