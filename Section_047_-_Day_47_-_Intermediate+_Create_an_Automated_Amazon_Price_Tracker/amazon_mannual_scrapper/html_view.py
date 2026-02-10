import os
import webbrowser
import pandas as pd
from html import escape

def generate_html_from_csv(csv_path, output_html):
    df = pd.read_csv(csv_path)

    rows = []

    for _, row in df.iterrows():
        rows.append(f"""
        <tr>
            <td class="image">
                <img src="{row['image_url']}" loading="lazy" alt="Product image">
            </td>
            <td class="title">{escape(str(row['title']))}</td>
            <td class="subtitle">{escape(str(row['subtitle']))}</td>
            <td class="price" data-value="{str(row['price']).replace('₹','').replace(',','')}">{row['price']}</td>
            <td class="rating" data-value="{str(row['rating']).split('/')[0] if pd.notna(row['rating']) else 0}">
                <span class="rating-value">{row['rating']}</span>
            </td>
            <td class="sponsored" data-value="{1 if row['is_sponsored'] else 0}">
                <span class="sponsored-badge {'sponsored-yes' if row['is_sponsored'] else 'sponsored-no'}">
                    {'Sponsored' if row['is_sponsored'] else 'Organic'}
                </span>
            </td>
            <td class="link">
                <a href="{row['product_url']}" target="_blank" class="link-button">View</a>
            </td>
        </tr>
        """)

    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Product Analytics Dashboard</title>

<style>
:root {{
    --bg: #0e1117;
    --panel: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --muted: #8b949e;
    --accent: #58a6ff;
    --accent-hover: #79c0ff;
    --success: #238636;
    --warning: #daaa3b;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}}

* {{
    box-sizing: border-box;
}}

body {{
    margin: 0;
    padding: 24px;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    line-height: 1.5;
}}

h1 {{
    font-size: 24px;
    margin: 0 0 20px 0;
    font-weight: 600;
    color: var(--text);
}}

.container {{
    max-width: 1400px;
    margin: 0 auto;
}}

.controls {{
    margin-bottom: 20px;
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}}

.sort-select {{
    background: var(--panel);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 14px;
    cursor: pointer;
    transition: var(--transition);
    min-width: 180px;
}}

.sort-select:hover {{
    border-color: var(--accent);
}}

.sort-select:focus {{
    outline: none;
    border-color: var(--accent);
    box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.2);
}}

.sort-info {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    background: var(--panel);
    border-radius: 8px;
    border: 1px solid transparent;
    font-size: 14px;
    color: var(--muted);
}}

.dashboard {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    transition: var(--transition);
}}

table {{
    width: 100%;
    border-collapse: collapse;
    min-width: 1000px;
}}

thead {{
    background: rgba(22, 27, 34, 0.95);
    backdrop-filter: blur(10px);
    position: sticky;
    top: 0;
    z-index: 10;
}}

th {{
    padding: 16px;
    text-align: left;
    color: var(--muted);
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    border-bottom: 2px solid var(--border);
    user-select: none;
    white-space: nowrap;
    transition: var(--transition);
}}

th:hover {{
    color: var(--accent);
}}

tbody tr {{
    transition: var(--transition);
    animation: fadeIn 0.5s ease-out;
}}

@keyframes fadeIn {{
    from {{
        opacity: 0;
        transform: translateY(10px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

td {{
    padding: 16px;
    border-bottom: 1px solid var(--border);
    font-size: 14px;
    vertical-align: middle;
    transition: var(--transition);
}}

tbody tr:hover {{
    background: rgba(88, 166, 255, 0.08);
}}

tbody tr:last-child td {{
    border-bottom: none;
}}

/* Column specific styles */
.image {{
    width: 80px;
    padding: 16px !important;
}}

.image img {{
    width: 64px;
    height: 64px;
    object-fit: contain;
    border-radius: 8px;
    background: var(--bg);
    padding: 4px;
    transition: var(--transition);
}}

.image img:hover {{
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}}

.title {{
    font-weight: 600;
    color: var(--text);
    min-width: 200px;
    max-width: 250px;
}}

.subtitle {{
    color: var(--muted);
    min-width: 300px;
    max-width: 400px;
    line-height: 1.4;
}}

.price {{
    font-weight: 600;
    font-size: 16px;
    color: #2ea043;
    min-width: 120px;
}}

.rating {{
    min-width: 120px;
}}

.rating-value {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    background: rgba(35, 134, 54, 0.15);
    border-radius: 6px;
    color: #2ea043;
    font-weight: 500;
}}

.sponsored {{
    min-width: 120px;
}}

.sponsored-badge {{
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}}

.sponsored-yes {{
    background: rgba(218, 170, 59, 0.15);
    color: var(--warning);
}}

.sponsored-no {{
    background: rgba(35, 134, 54, 0.15);
    color: var(--success);
}}

.link {{
    min-width: 100px;
}}

.link-button {{
    display: inline-block;
    padding: 6px 16px;
    background: var(--accent);
    color: white;
    text-decoration: none;
    border-radius: 6px;
    font-size: 13px;
    font-weight: 500;
    transition: var(--transition);
    text-align: center;
    min-width: 70px;
}}

.link-button:hover {{
    background: var(--accent-hover);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(88, 166, 255, 0.3);
}}

/* Sorting indicators */
.sort-indicator {{
    display: inline-block;
    margin-left: 4px;
    transition: var(--transition);
    opacity: 0;
}}

.sort-asc .sort-indicator {{
    opacity: 1;
    transform: rotate(180deg);
}}

.sort-desc .sort-indicator {{
    opacity: 1;
    transform: rotate(0deg);
}}

/* Responsive */
@media (max-width: 1200px) {{
    body {{
        padding: 16px;
    }}
    
    .dashboard {{
        border-radius: 8px;
    }}
    
    th, td {{
        padding: 12px;
    }}
}}

@media (max-width: 768px) {{
    .container {{
        padding: 0 8px;
    }}
    
    .controls {{
        flex-direction: column;
        gap: 8px;
    }}
    
    .sort-select {{
        width: 100%;
    }}
}}
</style>

<script>
let currentSort = {{column: '', direction: 1}};
let rowsData = [];

function initTable() {{
    const tbody = document.querySelector("tbody");
    const rows = Array.from(tbody.querySelectorAll("tr"));
    rowsData = rows.map(row => {{
        return {{
            element: row,
            price: parseFloat(row.querySelector('.price').dataset.value) || 0,
            rating: parseFloat(row.querySelector('.rating').dataset.value) || 0,
            title: row.querySelector('.title').textContent.toLowerCase(),
            sponsored: parseInt(row.querySelector('.sponsored').dataset.value) || 0
        }};
    }});
    
    updateSortInfo();
}}

function sortTable(columnClass) {{
    if (!columnClass) return;
    
    // Reset previous sort indicators
    document.querySelectorAll('th').forEach(th => {{
        th.classList.remove('sort-asc', 'sort-desc');
    }});
    
    // Set new sort indicator
    const headerCell = document.querySelector(`th[data-sort="${{columnClass}}"]`);
    if (headerCell) {{
        if (currentSort.column === columnClass) {{
            currentSort.direction *= -1;
        }} else {{
            currentSort.column = columnClass;
            currentSort.direction = 1;
        }}
        
        headerCell.classList.add(currentSort.direction === 1 ? 'sort-desc' : 'sort-asc');
    }}
    
    const tbody = document.querySelector("tbody");
    
    // Animate rows out
    const rows = Array.from(tbody.querySelectorAll("tr"));
    rows.forEach((row, index) => {{
        row.style.opacity = '0';
        row.style.transform = 'translateX(-20px)';
        row.style.transition = 'all 0.3s ease';
    }});
    
    // Sort and re-insert rows
    setTimeout(() => {{
        rows.sort((a, b) => {{
            const aCell = a.querySelector("." + columnClass);
            const bCell = b.querySelector("." + columnClass);
            
            let aVal, bVal;
            
            if (columnClass === 'price' || columnClass === 'rating') {{
                aVal = parseFloat(aCell.dataset.value) || 0;
                bVal = parseFloat(bCell.dataset.value) || 0;
            }} else if (columnClass === 'sponsored') {{
                aVal = parseInt(aCell.dataset.value) || 0;
                bVal = parseInt(bCell.dataset.value) || 0;
            }} else {{
                aVal = aCell.textContent.toLowerCase();
                bVal = bCell.textContent.toLowerCase();
            }}
            
            if (aVal < bVal) return -1 * currentSort.direction;
            if (aVal > bVal) return 1 * currentSort.direction;
            return 0;
        }});
        
        // Clear and append sorted rows
        tbody.innerHTML = '';
        rows.forEach((row, index) => {{
            row.style.opacity = '0';
            row.style.transform = 'translateX(20px)';
            tbody.appendChild(row);
            
            // Animate rows in with staggered delay
            setTimeout(() => {{
                row.style.opacity = '1';
                row.style.transform = 'translateX(0)';
            }}, index * 20);
        }});
        
        updateSortInfo();
    }}, 300);
}}

function updateSortInfo() {{
    const infoElement = document.getElementById('sortInfo');
    if (infoElement && currentSort.column) {{
        const columnNames = {{
            'price': 'Price',
            'rating': 'Rating',
            'title': 'Brand',
            'sponsored': 'Sponsored'
        }};
        
        const direction = currentSort.direction === 1 ? '↑' : '↓';
        infoElement.textContent = `Sorted by: ${{columnNames[currentSort.column]}} ${{direction}}`;
        infoElement.style.display = 'flex';
    }} else if (infoElement) {{
        infoElement.style.display = 'none';
    }}
}}
</script>
</head>

<body>
<div class="container">
    <h1>Amazon Product Analytics Dashboard</h1>
    
    <div class="controls">
        <select class="sort-select" onchange="sortTable(this.value)">
            <option value="">Sort products by...</option>
            <option value="price">Price (Low to High)</option>
            <option value="price">Price (High to Low)</option>
            <option value="rating">Rating (Best First)</option>
            <option value="rating">Rating (Worst First)</option>
            <option value="title">Brand (A-Z)</option>
            <option value="title">Brand (Z-A)</option>
            <option value="sponsored">Sponsored First</option>
            <option value="sponsored">Organic First</option>
        </select>
        
        <div class="sort-info" id="sortInfo" style="display: none;">
            <span>Sorted by: Price ↑</span>
        </div>
    </div>
    
    <div class="dashboard">
        <table>
            <thead>
                <tr>
                    <th data-sort="image">Image</th>
                    <th data-sort="title" onclick="sortTable('title')" style="cursor: pointer;">
                        Brand
                        <span class="sort-indicator">↓</span>
                    </th>
                    <th data-sort="subtitle">Description</th>
                    <th data-sort="price" onclick="sortTable('price')" style="cursor: pointer;">
                        Price
                        <span class="sort-indicator">↓</span>
                    </th>
                    <th data-sort="rating" onclick="sortTable('rating')" style="cursor: pointer;">
                        Rating
                        <span class="sort-indicator">↓</span>
                    </th>
                    <th data-sort="sponsored" onclick="sortTable('sponsored')" style="cursor: pointer;">
                        Sponsored
                        <span class="sort-indicator">↓</span>
                    </th>
                    <th>Link</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
    </div>
</div>

<script>
// Initialize table on load
document.addEventListener('DOMContentLoaded', initTable);
</script>
</body>
</html>
"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)

    webbrowser.open("file://" + os.path.abspath(output_html))