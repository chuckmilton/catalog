import requests
from bs4 import BeautifulSoup
import json

url = "https://minecraft.wiki/w/Item"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find the "List of items" section
items_section = soup.find("span", id="List_of_items")

items_data = []

# Check if the section was found
if items_section:
    print("Section found:")
    # Find all the divs containing the items following the "List of items" section
    items_divs = items_section.find_all_next("div", class_="div-col columns column-width")
    for div in items_divs:
        # Extract the list items
        items_list = div.find_all("li")
        # Extract the item's name, image, and link
        for item in items_list:
            item_name = item.text.strip()
            item_link = "https://minecraft.wiki" + item.find("a")["href"]
            items_data.append({
                "name": item_name,
                "link": item_link,
                "image_url": ""  # Initialize the image URL to an empty string
            })

    # Print the extracted data
    for item_data in items_data:
        print(item_data)
else:
    print("Section not found")

# Iterate through the items and extract the image URL for each item
for item in items_data:
    item_url = item['link']
    response = requests.get(item_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # First method: Find all img tags
    img_tags = soup.find_all('img')
    image_found = False

    # Find the img tag where the alt attribute contains the item's name
    for img_tag in img_tags:
        if img_tag.has_attr('alt') and item['name'].lower() in img_tag['alt'].lower():
            image_url = img_tag['src']
            item['image_url'] = image_url
            image_found = True
            break  # Stop searching once the image URL is found

    # Second method: Use tabbertab if the image was not found in the first method
    if not image_found:
        img_elements = soup.find_all('div', class_='tabbertab')
        if img_elements:
            for img_element in img_elements:
                data_title = img_element['data-title']
                if data_title.lower() in item['name'].lower():
                    img_tag = img_element.find('img')
                    if img_tag:
                        image_url = img_tag['src']
                        item['image_url'] = image_url
                        break  # Stop searching once the image URL is found
        else:
            print(f"No image found for {item['name']}")

# Save the updated items_data back to the JSON file
with open('./data/items_data.json', 'w') as json_file:
    json.dump(items_data, json_file, indent=4)
