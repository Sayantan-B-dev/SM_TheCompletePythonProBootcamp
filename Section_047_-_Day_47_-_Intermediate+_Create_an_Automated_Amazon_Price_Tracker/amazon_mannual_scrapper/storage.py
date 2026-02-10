import csv

HEADERS = [
    "title",
    "subtitle",
    "product_url",
    "asin",
    "image_url",
    "is_sponsored",
    "price",
    "rating",
]

def write_products_to_csv(products, extractor, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(HEADERS)
        for product in products:
            writer.writerow(extractor(product))
