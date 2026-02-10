import os
import requests

from scraper import parse_products, get_each_product_info
from storage import write_products_to_csv
from html_view import generate_html_from_csv

PRODUCT_URL = "https://www.amazon.in/s?k=ram+8gb+ddr4"
CACHE_FILE = "data/input/productpage.html"
CSV_FILE = "data/output/products.csv"
HTML_FILE = "data/output/products.html"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-IN,en;q=0.9",
}

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        html = f.read()
else:
    r = requests.get(PRODUCT_URL, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        raise RuntimeError(r.status_code)
    html = r.text
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        f.write(html)

products = parse_products(html)

write_products_to_csv(
    products=products,
    extractor=get_each_product_info,
    output_file=CSV_FILE
)

generate_html_from_csv(CSV_FILE, HTML_FILE)
