import requests
from bs4 import BeautifulSoup

# Fetch the HTML content from the webpage
r = requests.get("https://www.xwear.co.il/shop/fighting-equipment/mma-gloves/venum-challenger-gloves/")
soup = BeautifulSoup(r.text, "lxml")

# Find the div with the class "tab-content"
text_div_tags = soup.find_all("div", class_="tab-content")
texts = []

for text_div_tag in text_div_tags:
    p_tags = text_div_tag.find_all("p")
    for p in p_tags:
        text = p.text.strip()
        if text:
            texts.append(text)

# Print the extracted texts
for text in texts:
    print(text)
