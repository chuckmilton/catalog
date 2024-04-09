import requests
from bs4 import BeautifulSoup
import json

url = "https://minecraft.wiki/w/Mob"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find all tables with mobs
mob_tables = soup.find_all("table", style="margin:auto;text-align:center")

mobs_data = []

for table in mob_tables:
    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        for cell in cells:
            link_tag = cell.find("a")
            if link_tag:
                mob_name = link_tag.get("title", "").strip()
                mob_link = "https://minecraft.wiki" + link_tag["href"]
                
                # Visit the mob's page to extract the image URL
                mob_page_response = requests.get(mob_link)
                mob_page_soup = BeautifulSoup(mob_page_response.text, "html.parser")
                infobox_image = mob_page_soup.find("div", class_="infobox-imagearea")
                img_tag = infobox_image.find("img") if infobox_image else None
                mob_image = img_tag["src"] if img_tag else ""

                # Check if the mob is already in the list
                if not any(mob["name"] == mob_name for mob in mobs_data):
                    mobs_data.append({"name": mob_name, "link": mob_link, "image_url": mob_image})

# Save the data to a JSON file
with open('./data/mobs_data.json', 'w') as json_file:
    json.dump(mobs_data, json_file, indent=4)
