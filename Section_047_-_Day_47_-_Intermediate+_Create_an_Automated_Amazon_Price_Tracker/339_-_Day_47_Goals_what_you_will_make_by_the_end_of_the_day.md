# Amazon Product Scraper & Dashboard Documentation

## 📊 Project Overview
This project is a **practice-oriented web scraping tool** that extracts product information from Amazon search results and presents it in an interactive HTML dashboard. It demonstrates data extraction, processing, and visualization in a local environment.

```
┌─────────────────────────────────────────────────────────────┐
│                    WORKFLOW DIAGRAM                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 1. Manual HTML Copy → 2. Parse & Extract → 3. Store as CSV │
│        ↓                        ↓                 ↓         │
│ 4. Generate HTML Dashboard ← 5. View in Browser            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 🏗️ Project Structure

```
amazon-scraper/
│
├── main.py              # Orchestrates the entire pipeline
├── scraper.py           # HTML parsing and data extraction
├── storage.py           # CSV file handling
├── html_view.py         # HTML dashboard generation
│
├── data/
│   ├── input/           # Manually pasted HTML files
│   │   └── productpage.html
│   └── output/          # Generated files
│       ├── products.csv
│       └── products.html
│
└── README.md           # This documentation
```

## 🛠️ How It Works

### 🔄 Process Flow

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MANUAL STEP   │    │  AUTOMATED STEP │    │    OUTPUT       │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ 1. Search Amazon│    │ 4. Parse HTML   │    │ 7. CSV File     │
│    in Browser   │───→│    with scraper │───→│    Created      │
│                 │    │                 │    │                 │
│ 2. Open DevTools│    │ 5. Extract      │    │ 8. HTML         │
│    (F12)        │    │    Product Data │───→│    Dashboard    │
│                 │    │                 │    │    Generated    │
│ 3. Copy HTML    │    │ 6. Generate     │    │                 │
│    to File      │    │    Dashboard    │    │ 9. Auto-open    │
│                 │    │                 │    │    in Browser   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 📋 Step-by-Step Manual Process

#### Step 1: Search Amazon Manually
```
1. Open browser → 2. Go to amazon.in → 3. Search for products
   Example: "ram 8gb ddr4" or "laptops under 50000"
```

#### Step 2: Copy HTML Content
```
1. Press F12 (Developer Tools)
2. In Elements tab, find <body> element
3. Right-click → Copy → Copy outerHTML
4. Create/Open: data/input/productpage.html
5. Paste entire HTML content
6. Save the file
```

#### Step 3: Run the Program
```
$ python main.py
```

#### Step 4: View Results
```
1. Browser automatically opens products.html
2. If not, manually open: data/output/products.html
3. Interactive table with sorting capabilities
```

## 📁 File Details

### `main.py` - Pipeline Controller
```python
# Purpose: Orchestrates the entire scraping and visualization pipeline
# Flow: Read HTML → Parse → Extract → Save CSV → Generate HTML → Open Browser
# Key Features: Caching mechanism, error handling, sequential execution
```

### `scraper.py` - Data Extractor
```python
# Purpose: Parse HTML and extract structured product information
# Functions:
#   - parse_products(): Finds all product divs in HTML
#   - get_each_product_info(): Extracts 8 data points per product
# Data Points: title, subtitle, URL, ASIN, image, sponsorship, price, rating
```

### `storage.py` - Data Persistence
```python
# Purpose: Save extracted data to CSV format
# Features: UTF-8 encoding, proper headers, row-by-row writing
# Output: CSV with 8 columns matching extracted data structure
```

### `html_view.py` - Visualization Engine
```python
# Purpose: Convert CSV data to interactive HTML dashboard
# Features:
#   - Dark theme modern UI
#   - Interactive sorting (price, rating, brand, sponsorship)
#   - Responsive design
#   - Animated transitions
#   - Direct product links
```

## 🎨 Dashboard Features

### Sorting Capabilities
```
┌─────────────────────────────────────────────────────────┐
│                    SORTING OPTIONS                      │
├──────────────┬──────────────────────────────────────────┤
│ Price        │ Low to High / High to Low                │
│ Rating       │ Best First (4.5/5+) / Worst First        │
│ Brand        │ Alphabetical A-Z / Z-A                   │
│ Sponsored    │ Sponsored First / Organic First          │
└──────────────┴──────────────────────────────────────────┘
```

### Visual Elements
```
┌─────────────────────────────────────────────────────────┐
│                    TABLE COLUMNS                        │
├──────────────┬──────────────────────────────────────────┤
│ Image        │ Product thumbnail (64x64)                │
│ Brand        │ Main product title                       │
│ Description  │ Detailed subtitle                        │
│ Price        │ Green colored, formatted (₹)             │
│ Rating       │ Badge with score (e.g., 4.2/5)           │
│ Sponsored    │ Orange (Sponsored) / Green (Organic)     │
│ Link         │ "View" button (opens Amazon product)     │
└──────────────┴──────────────────────────────────────────┘
```

## 🔧 Technical Implementation

### Data Flow Diagram
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   RAW HTML  │    │  PARSED     │    │  STRUCTURED │    │  VISUAL     │
│   (Manual)  │───→│  Beautiful- │───→│  CSV Data   │───→│  Dashboard  │
│             │    │  Soup Obj   │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
        │                  │                  │                  │
        │             parse_products()   write_products_    generate_html_
        │                                  to_csv()        from_csv()
        │
        │    ┌────────────────────────────────────────────┐
        └───→│  8 Data Points Per Product:                │
             │  1. Title       5. Image URL               │
             │  2. Subtitle    6. Sponsored Flag          │
             │  3. Product URL 7. Price                   │
             │  4. ASIN        8. Rating                  │
             └────────────────────────────────────────────┘
```

### Key Dependencies
- `beautifulsoup4`: HTML parsing
- `pandas`: CSV reading for HTML generation
- `lxml`: Fast XML/HTML parser
- Built-in: `csv`, `os`, `webbrowser`, `html`

## ⚠️ Important Notes

### Practice-Only Project
```
⚠️  DISCLAIMER: This is for EDUCATIONAL PURPOSES only
├── Manual HTML copy avoids automated requests
├── No real-time scraping of Amazon
├── No bypassing of Amazon's terms
├── Demonstrates data processing concepts
└── Local file-based workflow only
```

### File Locations
```
Input (Manual):  data/input/productpage.html
Output (Auto):   data/output/products.csv
                 data/output/products.html
```

### Requirements
```txt
beautifulsoup4==4.12.2
pandas==2.1.4
lxml==4.9.3
```

## 🚀 Quick Start Guide

1. **Setup Environment**
   ```bash
   pip install beautifulsoup4 pandas lxml
   ```

2. **Prepare Directory Structure**
   ```bash
   mkdir -p data/input data/output
   ```

3. **Manual Data Collection**
   - Search Amazon in browser
   - Copy HTML from DevTools
   - Save to `data/input/productpage.html`

4. **Run Pipeline**
   ```bash
   python main.py
   ```

5. **Explore Results**
   - Open `data/output/products.html`
   - Sort by different columns
   - Click "View" to visit products

## 📈 Sample Output

After running the pipeline, you'll get:

1. **CSV File** (`products.csv`):
   ```
   title,subtitle,product_url,asin,image_url,is_sponsored,price,rating
   "Corsair Vengeance","DDR4 8GB 3200MHz","https://...","B07...","https://...",False,"₹2,499","4.5/5"
   ```

2. **HTML Dashboard**:
   - Interactive table with all products
   - Sortable columns with visual indicators
   - Responsive design for all screen sizes
   - Direct links to Amazon product pages

## 🔍 Troubleshooting

| Issue | Solution |
|-------|----------|
| `FileNotFoundError` | Create `data/input/` and `data/output/` directories |
| No browser opening | Manually open `data/output/products.html` |
| Empty CSV | Check HTML file contains product divs |
| Encoding issues | Ensure HTML file is UTF-8 encoded |

## 📚 Learning Points

This project demonstrates:
- HTML parsing with BeautifulSoup
- Data extraction patterns
- CSV file handling
- HTML/CSS/JavaScript dashboard creation
- Data visualization techniques
- Project organization and modular code

## 🔄 Extension Ideas (For Practice)

1. Add filtering by price range
2. Implement pagination for multiple HTML files
3. Add charts using Chart.js
4. Export functionality (PDF/Excel)
5. Price comparison across products
6. Rating distribution visualization

---

**Note**: This tool is designed for learning web scraping concepts. Always respect website terms of service and robots.txt files when working with real websites.