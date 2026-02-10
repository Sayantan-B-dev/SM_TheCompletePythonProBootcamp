from bs4 import BeautifulSoup
import lxml
import requests
import os
import rich
import time 
import json


# Main site call
url="https://books.toscrape.com"
if os.path.exists("website.html"):
    with open("website.html", "r") as file:
        contents = file.read()
else:
    with requests.get(url+"/index.html") as response:
        response.raise_for_status()
        contents = response.text
        with open("website.html", "w") as file:
            file.write(contents)
soup = BeautifulSoup(contents, "lxml")



def get_products(soup):
    available_products={}
    soup_article=soup.find_all("article")
    for article in soup_article:
        title=article.h3.a.text.strip()
        link=article.h3.a["href"].strip()
        price=article.find("p", class_="price_color").text.strip()
        stock=article.find("p", class_="instock availability").text.strip()
    
        available_products[title] = {
            "link": url+"/"+link,
            "price": price,
            "stock": stock
        }
    return available_products


def get_product_by_category(soup):
    all_categories={}
    filtered_products={}

    categories=soup.find("ul", class_="nav nav-list")
    total_categories=len(categories.ul.find_all("li"))
    for category in categories.ul.find_all("li"):
        all_categories[category.a.text.strip()] = category.a["href"].strip()
    for category in all_categories:
        category_url=url+"/"+all_categories[category]
        with requests.get(category_url) as response:
            response.raise_for_status()
            contents = response.text
            soup=BeautifulSoup(contents, "lxml")
            filtered_products[category]=get_products(soup)
        rich.print(f"Fetched {category}.json")
        rich.print(f"Fetched {len(filtered_products)}/{total_categories} categories")
        time.sleep(5)
    with open(f"all_products_by_category.json", "w") as file:
        json.dump(filtered_products, file, indent=4)
        rich.print("Saved all_products_by_category.json")
    return filtered_products
        
def get_all_products():
    all_products={}
    page_url=url+"/catalogue/category/books_1/"
    page_no=1
    while True:
        if page_no==1:
            final_page_url=page_url+"index.html"
        else:
            final_page_url=page_url+"page-"+str(page_no)+".html"
        if final_page_url==url+"/catalogue/category/books_1/page-51.html":
            break
        with requests.get(final_page_url) as response:
            response.raise_for_status()
            contents = response.text
            soup=BeautifulSoup(contents, "lxml")
            all_products[page_no]=get_products(soup)
        rich.print(f"Fetched {page_no}.json")
        rich.print(f"Fetched {len(all_products)}/50 categories")
        page_no+=1
        time.sleep(5)
    with open(f"all_products.json", "w") as file:
        json.dump(all_products, file, indent=4)
        rich.print("Saved all_products.json")
    return all_products


choice=input("Enter 1 for all products by category, 2 for all products: ")
if choice=="1":
    get_product_by_category(soup)
elif choice=="2":
    get_all_products()
else:
    rich.print("Invalid choice try again")