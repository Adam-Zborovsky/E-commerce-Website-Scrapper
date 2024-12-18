import requests
from bs4 import BeautifulSoup
import csv
import os
import re
import shutil


print("Hello Mr.Weiss")
base_url = input("Please Enter Your Desired Url And Press Enter:  ")
num_of_pages = int(input("How Many Pages Dose Your Url Have? And Press Enter:  "))
confirm = ""
while confirm != "y":
    confirm = input(f"Is This The Correct Url and Number Of Pages?:\n{base_url} \n {num_of_pages} \n y/n?: ")
    if confirm != "y":
        base_url = input("Please Enter Your Desired Url And Press Enter:")
        num_of_pages = int(input("How Many Pages Dose Your Url Have? And Press Enter:  "))


shutil.rmtree("Result", ignore_errors=True)
os.makedirs("Result")
urls =[]

for i in range(1, num_of_pages + 1):
    url = f"{base_url}page/{i}/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    
    thumbnail_divs = soup.find_all("div", class_="product-thumbnail")
    for thumbnail_div in thumbnail_divs:
            a_tag = thumbnail_div.find("a")
            url = a_tag.get("href")
            if a_tag and url:
                urls.append(url)



product_data = []
for url in urls:
    dupes = 1
    name = ""
    price = ""
    content = []
    description = []
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    
    
    h1_tags = soup.find_all("h1", class_="product_title entry-title h2") 
    for h1_tag in h1_tags:
        name = h1_tag.text.strip()
    
    active_li_tag = soup.find("li", class_="active")
    if active_li_tag:
        content_div_tags = active_li_tag.find_all("div", class_="tab-content")
        for content_div_tag in content_div_tags:
            for child in content_div_tag.find_all(["p", "ul", "li", "h3"]):
                text = child.text.strip() 
                if text:
                    text = text.replace(",",".")
                    content.append(text)
    else:
        content_div_tags = soup.find_all("div", class_="tab-content")
        for content_div_tag in content_div_tags:
            for child in content_div_tag.find_all("p"):
                text = child.text.strip() 
                if text:
                    text = text.replace(",",".")
                    content.append(text)
                    
                    
    description_div_tags = soup.find_all("div", class_="row description")
    
    for description_div_tag in description_div_tags:
        description_p = description_div_tag.find("p")
        if  description_p:
            text = description_p.text.strip()
            description.append(text) 
        
    
    price_p_tags = soup.find_all("p", class_="price prm-color")
        
    for price_p_tag in price_p_tags:
        span_tag = price_p_tag.find("span", class_="woocommerce-Price-amount amount")
        if span_tag:
            price = span_tag.text.strip() 

    
    product_data.append([name,price,' '.join(description),' '.join(content)])

    

    
    product_images = []
    img_tags = soup.find_all("img", class_="wp-post-image")
    for img_tag in img_tags[1:]:
        src = img_tag.get("data-large_image")
        if src:
            product_images.append(src)
    

    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    
    base_path =f"Result/{name}"
    if os.path.exists(base_path):
        os.mkdir(base_path + str(dupes))
        dupes =+ 1
    else:
        os.mkdir(base_path)
    
    
    print(f"Downloading {name}")
    for i, img_url in enumerate(product_images):
        # Sanitize product name for use as a file name
        
        img_filename = f"{base_path}/{i+1}.jpg"
        try:
            img_data = requests.get(img_url).content
            with open(img_filename, 'wb') as img_file:
                img_file.write(img_data)
        except Exception as e:
            print(f"Failed to download image {img_url}: {e}")
            input()





csv_filename = "Result/product_data.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Product Name", "Product Price", "Quick View", "Big Description"])
    for data in product_data:
        csv_writer.writerow(data)
print(f"Data successfully scraped and saved to {csv_filename}")
input()
