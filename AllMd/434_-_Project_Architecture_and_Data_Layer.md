We'll dive deep into this Flask-based Cafe Catalog application. To keep things clear and comprehensive, we'll break the explanation into three logical steps. Here is **Step 1**, covering the project architecture and the data layer.

---

## Step 1: Project Architecture and Data Layer

In this step, we examine the overall structure of the project, how it is set up, and most importantly, how data is stored and manipulated using a simple CSV file.

### 1.1 Project Overview

The application is a catalog of cafes that provides information about:

- Cafe name
- Location (Google Maps URL)
- Opening and closing times
- Coffee quality rating (represented by coffee cup emojis)
- Wi-Fi strength rating (represented by flexed bicep emojis)
- Power outlet availability rating (represented by plug emojis)

Users can view the list of cafes, add new cafes via a form, and delete existing entries. The entire data set is stored in a single CSV file, making it a lightweight, file‑based solution ideal for learning or small‑scale use.

### 1.2 Project Structure

The project consists of the following files and directories:

```
project/
│
├── main.py                 # Flask application entry point
├── cafe-data.csv           # Data storage (CSV format)
├── requirements.txt        # Python dependencies
│
├── static/                 # Static assets
│   └── css/
│       └── styles.css      # Custom CSS (Tron‑like theme)
│
└── templates/              # Jinja2 HTML templates
    ├── base.html           # Base template with Bootstrap & common structure
    ├── index.html          # Homepage hero section
    ├── add.html            # Form to add a new cafe
    └── cafes.html          # Table displaying all cafes
```

### 1.3 Dependencies and Configuration

The `requirements.txt` file lists the necessary packages:

```
Bootstrap_Flask==2.2.0
Flask==2.3.2
WTForms==3.0.1
Flask_WTF==1.2.1
Werkzeug==3.0.0
```

- **Flask** – the web framework.
- **Flask-WTF** – integrates WTForms with Flask, providing CSRF protection and form handling.
- **WTForms** – for form definition and validation.
- **Bootstrap-Flask** – simplifies the use of Bootstrap 5 in Flask templates.
- **Werkzeug** – a WSGI utility library (Flask depends on it).

In `main.py`, the Flask app is created and configured:

```python
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
```

The secret key is required by Flask-WTF to protect forms against CSRF attacks. `Bootstrap5(app)` initializes the Bootstrap-Flask extension, making Bootstrap 5 resources available in templates.

### 1.4 The Data Schema (CSV Structure)

The file `cafe-data.csv` acts as the database. Its first row is a header, and subsequent rows contain cafe records. The columns are:

| Column        | Description                              | Example                           |
|---------------|------------------------------------------|-----------------------------------|
| Cafe Name     | Name of the cafe                         | Lighthaus                         |
| Location      | Google Maps URL                          | https://goo.gl/maps/...           |
| Open          | Opening time (string)                     | 11AM                              |
| Close         | Closing time (string)                     | 3:30PM                            |
| Coffee        | Coffee rating (emoji string)              | ☕☕☕☕️                            |
| Wifi          | Wi‑Fi rating (emoji string)                | 💪💪                              |
| Power         | Power outlet rating (emoji string)         | 🔌🔌🔌                            |

Here is the actual content of `cafe-data.csv`:

```
Cafe Name,Location,Open,Close,Coffee,Wifi,Power
Lighthaus,https://goo.gl/maps/2EvhB4oq4gyUXKXx9,11AM, 3:30PM,☕☕☕☕️,💪💪,🔌🔌🔌
Esters,https://goo.gl/maps/13Tjc36HuPWLELaSA,8AM,3PM,☕☕☕☕,💪💪💪,🔌
Ginger & White,https://goo.gl/maps/DqMx2g5LiAqv3pJQ9,7:30AM,5:30PM,☕☕☕,✘,🔌
Mare Street Market,https://goo.gl/maps/ALR8iBiNN6tVfuAA8,8AM,1PM,☕☕,💪💪💪,🔌🔌🔌
```

### 1.5 Reading Data from CSV

When the user visits the `/cafes` route, the application reads all rows from the CSV file and passes them to the template for display. The route handler `cafes()` in `main.py` does:

```python
@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]
    return render_template('cafes.html', cafes=list_of_rows)
```

- `open('cafe-data.csv', ...)` opens the file in read mode. The `newline=''` parameter ensures proper handling of line endings across platforms.
- `csv.reader(csv_file, delimiter=',')` creates a reader object that parses each line into a list of strings.
- A list comprehension collects all rows into `list_of_rows`. The first element is the header row; subsequent elements are data rows.
- The entire list is passed to the template as the variable `cafes`.

This list is then iterated in `cafes.html` to build an HTML table.

### 1.6 Writing Data to CSV (Adding a New Cafe)

When a user submits the form on the `/add` page (POST request), the `add_cafe()` route processes the data and appends a new row to the CSV file.

The relevant part of the route:

```python
if form.validate_on_submit():
    cafe_data = [
        form.cafe.data,
        form.location.data,
        form.open_time.data,
        form.close_time.data,
        COFFEE_CHOICES[int(form.coffee_rating.data)][1],
        WIFI_CHOICES[int(form.wifi_rating.data)][1],
        POWER_CHOICES[int(form.power_rating.data)][1]
    ]
    with open('cafe-data.csv', mode='a', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(cafe_data)
    return redirect(url_for('cafes'))
```

- The form data is extracted. Note that the rating fields store the **index** of the selected choice (e.g., `'3'` for a rating of 3). The code converts that index to an integer and uses it to fetch the corresponding emoji string from the predefined choices (e.g., `COFFEE_CHOICES[3][1]` gives `'☕☕☕☕'`).
- The resulting list `cafe_data` is a flat list of strings matching the CSV columns.
- `open('cafe-data.csv', mode='a', ...)` opens the file in **append** mode. This adds new data to the end without overwriting existing content.
- `csv.writer(csv_file).writerow(cafe_data)` writes the list as a single comma‑separated row.
- After writing, the user is redirected to the `/cafes` page so they can see the updated list.

### 1.7 Deleting Data from CSV

The delete operation is implemented in the `/delete/<int:cafe_id>` route. It receives the index of the cafe to delete (the cafe's position in the data list, **excluding the header**). The logic reads the entire file, removes the specified row, and writes all remaining rows back.

```python
@app.route('/delete/<int:cafe_id>', methods=['POST'])
def delete_cafe(cafe_id):
    with open('cafe-data.csv', mode='r', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]

    # Remove the row at index cafe_id+1 (because row 0 is the header)
    list_of_rows.pop(cafe_id + 1)

    with open('cafe-data.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(list_of_rows)

    return redirect(url_for('cafes'))
```

- First, all rows are read into `list_of_rows`. The header is at index 0.
- The parameter `cafe_id` corresponds to the zero‑based index of the cafe **among the data rows** (as passed from the template). To target the correct row in the full list, we add 1 (skipping the header).
- `list_of_rows.pop(cafe_id + 1)` removes that row.
- The file is then opened in write mode (`'w'`), which truncates the file. `writer.writerows(list_of_rows)` writes all remaining rows back, effectively saving the updated dataset.
- Finally, the user is redirected to the cafes page.

### 1.8 Implications of Using CSV as a Database

- **Simplicity**: No database server setup, no SQL. The code is straightforward.
- **Concurrency**: The application does not handle concurrent writes. If two users try to add or delete at the same time, data corruption could occur.
- **Scalability**: For more than a handful of entries or users, a proper database (like SQLite, PostgreSQL) would be necessary.
- **Data integrity**: There is no validation beyond what the form provides; the CSV format is plain text and could be manually edited.

This file‑based approach is perfectly suitable for a tutorial or a small personal project, which is its intended use.

### 1.9 Data Flow Summary

- **Read**: `/cafes` route → open CSV → read all rows → pass to template.
- **Write (add)**: Form submission → gather form data (convert ratings to emojis) → open CSV in append mode → write one row.
- **Write (delete)**: Delete request → read all rows → remove one row → open CSV in write mode → write all rows back.
