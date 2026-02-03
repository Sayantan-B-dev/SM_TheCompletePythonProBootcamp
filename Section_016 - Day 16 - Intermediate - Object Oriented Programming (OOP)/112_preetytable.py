from rich.console import Console
from rich.table import Table
from rich import box
from faker import Faker
import random
from datetime import datetime

"""NOT USING PREETYTABLE HERE"""

# Initialize
console = Console()
fake = Faker()

def generate_sales_data(num=12):
    """Generate monthly sales data"""
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    regions = ["North America", "Europe", "Asia", "South America", "Australia"]
    products = ["Product A", "Product B", "Product C", "Product D", "Product E"]
    
    data = []
    for i in range(num):
        region = random.choice(regions)
        product = random.choice(products)
        units = random.randint(100, 5000)
        price = round(random.uniform(10, 500), 2)
        revenue = units * price
        growth = random.uniform(-15, 25)
        
        data.append({
            "month": months[i % 12],
            "region": region,
            "product": product,
            "units": units,
            "price": price,
            "revenue": revenue,
            "growth": growth,
            "status": "✅ Above Target" if revenue > 50000 else "⚠️ Below Target"
        })
    return data

# Generate data
sales_data = generate_sales_data(15)

# Create a beautiful table
console.print("\n")
console.rule("[bold blue]📈 QUARTERLY SALES REPORT[/bold blue]", style="blue")

# Table 1: Sales Performance
table1 = Table(title="Sales Performance Q1 2024", 
               box=box.ROUNDED,
               header_style="bold magenta",
               title_style="bold white on blue")

table1.add_column("Month", style="cyan", justify="center")
table1.add_column("Region", style="green")
table1.add_column("Product", style="yellow")
table1.add_column("Units", justify="right", style="white")
table1.add_column("Price", justify="right", style="white")
table1.add_column("Revenue", justify="right", style="bold green")
table1.add_column("Growth %", justify="right")
table1.add_column("Status", justify="center")

for sale in sales_data[:8]:
    # Color code growth
    growth_color = "red" if sale["growth"] < 0 else "green"
    growth_text = f"[{growth_color}]{sale['growth']:+.1f}%[/{growth_color}]"
    
    table1.add_row(
        sale["month"],
        sale["region"],
        sale["product"],
        f"{sale['units']:,}",
        f"${sale['price']:.2f}",
        f"[bold]${sale['revenue']:,.2f}[/bold]",
        growth_text,
        sale["status"]
    )

console.print(table1)

# Table 2: Regional Summary
console.print("\n")
table2 = Table(title="Regional Performance Summary", 
               box=box.DOUBLE_EDGE,
               show_header=True,
               header_style="bold white on dark_blue")

table2.add_column("Region", style="bold cyan")
table2.add_column("Total Revenue", justify="right", style="bold green")
table2.add_column("Avg Growth", justify="right")
table2.add_column("Market Share", justify="right")
table2.add_column("Trend", justify="center")

region_stats = {}
for sale in sales_data:
    region = sale["region"]
    if region not in region_stats:
        region_stats[region] = {"revenue": 0, "growth": [], "count": 0}
    region_stats[region]["revenue"] += sale["revenue"]
    region_stats[region]["growth"].append(sale["growth"])
    region_stats[region]["count"] += 1

for region, stats in region_stats.items():
    avg_growth = sum(stats["growth"]) / len(stats["growth"])
    market_share = random.randint(15, 40)
    
    # Trend indicator
    if avg_growth > 10:
        trend = "📈 [bold green]Strong Growth[/bold green]"
    elif avg_growth > 0:
        trend = "↗️ [yellow]Moderate Growth[/yellow]"
    else:
        trend = "📉 [red]Declining[/red]"
    
    table2.add_row(
        region,
        f"${stats['revenue']:,.0f}",
        f"[green]{avg_growth:+.1f}%[/green]" if avg_growth >= 0 else f"[red]{avg_growth:+.1f}%[/red]",
        f"{market_share}%",
        trend
    )

console.print(table2)

# Table 3: Product Performance (Compact)
console.print("\n")
table3 = Table(title="Product Analysis", 
               box=box.SIMPLE,
               show_lines=True)

table3.add_column("Product", style="bold")
table3.add_column("Q1 Revenue", justify="right")
table3.add_column("Q2 Forecast", justify="right")
table3.add_column("YoY Growth", justify="right")
table3.add_column("Rating", justify="center")

products = {}
for sale in sales_data:
    product = sale["product"]
    if product not in products:
        products[product] = {"revenue": 0, "count": 0}
    products[product]["revenue"] += sale["revenue"]
    products[product]["count"] += 1

for product, stats in products.items():
    forecast = stats["revenue"] * random.uniform(0.9, 1.3)
    yoy_growth = random.uniform(-5, 30)
    rating = random.randint(1, 5)
    
    # Star rating
    stars = "⭐" * rating + "☆" * (5 - rating)
    
    table3.add_row(
        product,
        f"${stats['revenue']:,.0f}",
        f"${forecast:,.0f}",
        f"[green]{yoy_growth:+.1f}%[/green]" if yoy_growth > 0 else f"[red]{yoy_growth:+.1f}%[/red]",
        f"[yellow]{stars}[/yellow]"
    )

console.print(table3)

# Key Metrics Panel
console.print("\n")
console.rule("[bold]🎯 KEY METRICS[/bold]")

metrics = Table(box=box.HEAVY, show_header=False, pad_edge=False)
metrics.add_column("Metric", style="bold cyan", width=25)
metrics.add_column("Value", style="bold white", justify="right")
metrics.add_column("Change", style="bold", justify="center")
metrics.add_column("Status", style="bold", justify="center")

metrics_data = [
    ["Total Revenue", "$4,825,350", "+12.5%", "✅ On Track"],
    ["Units Sold", "28,450", "+8.2%", "✅ On Track"],
    ["Avg. Price", "$169.50", "+3.1%", "⚠️ Monitor"],
    ["Customer Growth", "1,245", "+15.3%", "✅ On Track"],
    ["Market Share", "23.5%", "+2.1%", "✅ On Track"],
    ["Profit Margin", "34.2%", "+1.8%", "✅ On Track"]
]

for metric in metrics_data:
    metrics.add_row(*metric)

console.print(metrics)