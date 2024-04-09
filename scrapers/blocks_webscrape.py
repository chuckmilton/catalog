import requests
from bs4 import BeautifulSoup
import json

url = "https://minecraft.wiki/w/Block"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find the "List of blocks" section
blocks_section = soup.find("span", id="List_of_blocks")

blocks_data = []

# Check if the section was found
if blocks_section:
    print("Section found:")
    blocks_divs = blocks_section.find_all_next("div", class_="div-col columns column-width")
    for div in blocks_divs:
        blocks_list = div.find_all("li")
        for block in blocks_list:
            block_name = block.text.strip()
            # Find all <a> tags in the block list item
            block_a_tags = block.find_all("a")
            # Use the second <a> tag (if available) to get the block's link
            if len(block_a_tags) > 1:
                block_link = "https://minecraft.wiki" + block_a_tags[1]["href"]
            else:
                block_link = "Link not found"
            blocks_data.append({
                "name": block_name,
                "link": block_link,
                "image_url": ""  # Initialize the image URL to an empty string
            })
else:
    print("Section not found")
# Iterate through the blocks and extract the image URL for each block
for block in blocks_data:
    if block['link'] != "Link not found":
        response = requests.get(block['link'])
        soup = BeautifulSoup(response.text, 'html.parser')

    img_tags = soup.find_all('img')
    image_found = False

    for img_tag in img_tags:
        if img_tag.has_attr('alt') and block['name'].lower() in img_tag['alt'].lower():
            image_url = img_tag['src']
            block['image_url'] = image_url
            image_found = True
            break

    if not image_found:
        img_elements = soup.find_all('div', class_='tabbertab')
        for img_element in img_elements:
            data_title = img_element.get('data-title', '').lower()
            if data_title == block['name'].lower():
                img_tag = img_element.find('img')
                if img_tag:
                    image_url = img_tag['src']
                    block['image_url'] = image_url
                    break

    if not image_found:
        print(f"No image found for {block['name']}")

# Save the updated blocks_data back to the JSON file
with open('./data/blocks_data.json', 'w') as json_file:
    json.dump(blocks_data, json_file, indent=4)
