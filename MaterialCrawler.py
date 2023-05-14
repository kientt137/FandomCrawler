import json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from Utilities import Utilities as Utils

fandom_link = "https://zelda.fandom.com/wiki/Materials_in_Tears_of_the_Kingdom"

with open("data/material.json", "r") as f:
    dict_item = json.loads(f.read())

req = Request(fandom_link)
html = urlopen(req).read()
soup = BeautifulSoup(html, 'html.parser')

category_ref = ["categories/materials"]

table = soup.find('table')

items = table.find_all('tr')
for item in items:
    item_data = item.find_all('td')
    if len(item_data) == 4:

        name = item_data[0].text.strip()
        image_url = Utils.get_image_url(item_data[0].find('img'))

        item_id = Utils.string_to_id(item_data[0].text)
        description = item_data[1].text.strip()

        a = item_data[0].find('b').find('a')
        if a is not None:
            item_id = Utils.link_to_id(a['href'])
            item_url = "https://zelda.fandom.com" + a["href"]
        else:
            item_id = Utils.string_to_id(name)
            item_url = None
        icons = item_data[3].find_all('img')
        for icon in icons:
            if icon['alt'] == 'BotW Heart Icon':
                icon.replaceWith("%full_heart%")
            elif icon['alt'] == 'BotW Half-Heart Icon':
                icon.replaceWith("%half_heart%")
            elif icon['alt'] == 'BotW Quarter Heart Icon':
                icon.replaceWith("%quarter_heart%")
            else:
                icon.replaceWith("")
        break_lines = item_data[3].find_all('br')
        for break_line in break_lines:
            break_line.replaceWith("\n")
        attributes = {
            "Value": item_data[2].text.strip() + " %rupee%",
            "Additional uses": item_data[3].text.strip()
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
with open("data/material.json", 'w') as f:
    json.dump(dict_item, f, indent=True)
