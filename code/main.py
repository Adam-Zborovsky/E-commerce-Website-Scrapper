import requests
from bs4 import BeautifulSoup
import csv
import os
import re


print("Hello Mr.Weiss")
base_url = input("Please Enter Your Desired Url And Press Enter:  ")
num_of_pages = int(input("How Many Pages Dose Your Url Have? And Press Enter:  "))
confirm = ""
while confirm != "y":
    confirm = input(f"Is This The Correct Url and Number Of Pages?:\n{base_url} \n {num_of_pages} \n y/n?: ")
    if confirm != "y":
        base_url = input("Please Enter Your Desired Url And Press Enter:")
        num_of_pages = int(input("How Many Pages Dose Your Url Have? And Press Enter:  "))


urls =[]

# Scrape all pages
for i in range(1, num_of_pages + 1):
    url = f"{base_url}page/{i}/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")
    
    thumbnail_divs = soup.find_all("div", class_="product-thumbnail")
    for thumbnail_div in thumbnail_divs:
            a_tag = thumbnail_div.find("a")
            url = a_tag.get("href")
            # Append data if name and image exist
            if a_tag and url:
                urls.append(url)



for url in urls:
    
    product_data = []
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

    
    product_data = [[name,price,' '.join(description),' '.join(content)]]

    base_path =f"Result/{name}"
    if os.path.exists(base_path):
        pass
    else:
        os.makedirs(base_path)
            
    csv_filename = base_path + "/product_data.csv"
    with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Product Name", "Product Price", "Quick View", "Big Description"])
        for data in product_data:
            csv_writer.writerow(data)

    
    
    
    product_images = []
    img_tags = soup.find_all("img", class_="wp-post-image")
    for img_tag in img_tags[1:]:
        src = img_tag.get("data-large_image")
        if src:
            product_images.append(src)
    
    

    if os.path.exists(base_path+"/images"):
        for filename in os.listdir(base_path+"/images"):
            file_path = os.path.join(base_path+"/images", filename)
            os.remove(file_path)
    else:
        os.makedirs(base_path+"/images")
    
    for i, img_url in enumerate(product_images):
        # Sanitize product name for use as a file name
        sanitized_name = re.sub(r'[\/:*?"<>|]', '_', name)
        img_filename = f"{base_path}/images/{i+1}.jpg"
        try:
            img_data = requests.get(img_url).content
            with open(img_filename, 'wb') as img_file:
                img_file.write(img_data)
            print(f"{i+1}.download image {img_url}")
            print()
        except Exception as e:
            print(f"Failed to download image {img_url}: {e}")


# # Create 'images' directory, overwriting if exists
# if os.path.exists("Result/images"):
#     for filename in os.listdir("Result/images"):
#         file_path = os.path.join("Result/images", filename)
#         os.remove(file_path)
# else:
#     os.makedirs("Result/images")





print(f"Data successfully scraped and saved to {csv_filename}")
