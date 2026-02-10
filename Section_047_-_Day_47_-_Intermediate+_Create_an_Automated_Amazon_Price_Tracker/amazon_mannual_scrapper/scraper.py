from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote

def parse_products(html):
    soup = BeautifulSoup(html, "lxml")
    return soup.find_all("div", attrs={"data-component-type": "s-search-result"})

def get_each_product_info(product_div):
    title = None
    h2 = product_div.find("h2")
    if h2 and h2.find("span"):
        title = h2.find("span").get_text(strip=True)

    subtitle = None
    long_title_h2 = product_div.find(
        "h2",
        class_="a-size-base-plus a-spacing-none a-color-base a-text-normal"
    )
    if long_title_h2 and long_title_h2.find("span"):
        subtitle = long_title_h2.find("span").get_text(strip=True)

    if title and subtitle and title == subtitle:
        subtitle = "same as title"

    link = None
    asin = None
    a_tag = product_div.find("a", href=True)
    if a_tag:
        href = a_tag["href"]
        if "/sspa/click" in href:
            qs = parse_qs(urlparse(href).query)
            if "url" in qs:
                decoded = unquote(qs["url"][0])
                link = "https://www.amazon.in" + decoded
                parts = decoded.split("/")
        else:
            link = "https://www.amazon.in" + href
            parts = href.split("/")
        if "dp" in parts:
            i = parts.index("dp")
            if i + 1 < len(parts):
                asin = parts[i + 1]

    img = product_div.find("img", class_="s-image")
    image_url = img["src"] if img else None

    sponsored = bool(product_div.find("span", string=lambda x: x and "Sponsored" in x))

    price = None
    price_tag = product_div.find("span", class_="a-offscreen")
    if price_tag:
        price = price_tag.get_text(strip=True)

    rating = None
    rating_tag = product_div.find("span", class_="a-icon-alt")
    if rating_tag:
        rating = rating_tag.get_text(strip=True).replace(" out of 5 stars", "/5")

    return [
        title,
        subtitle,
        link,
        asin,
        image_url,
        sponsored,
        price,
        rating,
    ]
