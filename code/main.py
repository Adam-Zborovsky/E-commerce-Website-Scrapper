import requests
from bs4 import BeautifulSoup
import csv
import os
import re

# Base URL and settings
print("Hello Mr.Weiss")
base_url = input("Please Enter Your Desired Url And Press Enter:  ")
num_of_pages = int(
    input("How Many Pages Dose Your Url Have? And Press Enter:  "))
confirm = ""
while confirm != "y":
    confirm = input(f"Is This The Correct Url and Number Of Pages?:\n{
                    base_url}\n{num_of_pages}\ny/n?: ")
    if confirm != "y":
        base_url = input("Please Enter Your Desired Url And Press Enter:")
        num_of_pages = int(
            input("How Many Pages Dose Your Url Have? And Press Enter:  "))


product_data = []  # To store product names and prices
product_images = []  # To store (product_name, image_url) pairs

# Scrape all pages
for i in range(1, num_of_pages + 1):
    url = f"{base_url}page/{i}/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "lxml")

    # Find product name, price, and images
    p_tags = soup.find_all("p", class_="product-name txt-color")
    span_tags = soup.find_all("span", class_="woocommerce-Price-amount amount")
    thumbnail_divs = soup.find_all("div", class_="product-thumbnail")

    for p_tag, span_tag, thumbnail_div in zip(p_tags, span_tags, thumbnail_divs):
        # Extract product name
        name_tag = p_tag.find("a")
        name = name_tag.text.strip() if name_tag else None

        # Extract price
        price_tag = span_tag.find("bdi")
        price = price_tag.text.strip() if price_tag else None

        # Extract image URL
        img_tag = thumbnail_div.find("img")
        img_url = img_tag.get(
            "data-lazy-src") or img_tag.get("src") if img_tag else None
        # Append data if name and image exist
        if name and img_url:
            product_data.append([name, price])
            # Pair product name with image URL
            product_images.append([name, img_url])


# Save product names and prices to CSV
csv_filename = "Result/product_data.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(["Product Name", "Product Price"])  # Write headers
    for data in product_data:
        csv_writer.writerow(data)


# Create 'images' directory, overwriting if exists
if os.path.exists("Result/images"):
    for filename in os.listdir("Result/images"):
        file_path = os.path.join("Result/images", filename)
        os.remove(file_path)
else:
    os.makedirs("Result/images")


def sanitize_filename(name):
    # Replace invalid characters with an underscore
    name = re.sub(r'[\/:*?"<>|]', '_', name)
    # Trim extra whitespace
    return name.strip()


# Download images and name them after the product
print(i)
for i, (product_name, img_url) in enumerate(product_images):
    # Sanitize product name for use as a file name
    sanitized_name = sanitize_filename(product_name)
    img_filename = f"Result/images/{i+1}{sanitized_name}.jpg"
    try:
        img_data = requests.get(img_url).content
        with open(img_filename, 'wb') as img_file:
            img_file.write(img_data)
        print(f"{i+1}.download image {img_url}")
        print()
    except Exception as e:
        print(f"Failed to download image {img_url}: {e}")

print(f"Data successfully scraped and saved to {csv_filename}")
