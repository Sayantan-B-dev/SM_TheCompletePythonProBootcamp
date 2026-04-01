## Step 3: Display and Interaction (UI Layer)

In this final step, we examine how the data is presented to the user, how the interface enables interaction (viewing, adding, deleting), and how the custom styling creates a cohesive user experience.

### 3.1 Overview of the UI Layer

The user interface is built with **HTML templates** rendered by Flask using the **Jinja2** templating engine. All pages share a common base template that includes Bootstrap 5 and a custom CSS file. The main pages are:

- **Home page** (`index.html`) – a hero section inviting the user to explore.
- **Add cafe page** (`add.html`) – contains the form for adding a new cafe.
- **Cafes listing page** (`cafes.html`) – displays all cafes in a table, with a delete button per row and links to the location.

The design follows a **Tron‑like aesthetic** with a black background, white text, cyan links, and sharp‑edged buttons, achieved through custom CSS.

### 3.2 Template Inheritance and Base Structure

All templates extend `base.html`, which sets up the HTML skeleton and loads Bootstrap and the custom CSS.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />

    {% block styles %}
      {{ bootstrap.load_css() }}
      <link rel="stylesheet" href="{{ url_for('static', filename='css/styles.css') }}">
    {% endblock %}

    <title>{% block title %}{% endblock %}</title>
  </head>
  <body>
    {% block content %}{% endblock %}
  </body>
</html>
```

- `bootstrap.load_css()` loads Bootstrap 5 CSS from a CDN (provided by the Bootstrap-Flask extension).
- The custom `styles.css` is linked using `url_for('static', filename='css/styles.css')`.
- The `title` and `content` blocks are overridden in child templates.

### 3.3 Home Page (`index.html`)

The home page is simple: a full‑height centered hero unit with a call‑to‑action button.

```html
{% extends 'base.html' %}
{% block title %}Coffee and Wifi{% endblock %}

{% block content %}
<div class="jumbotron text-center">
  <div class="container">
    <h1 class="display-4">☕️ Coffee & Wifi 💻</h1>
    <p class="lead">Want to work in a cafe but need power and wifi?</p>
    <hr class="my-4">
    <p>You've found the right place! Checkout my collection of cafes with data on power socket availability, wifi speed and coffee quality.</p>
    <a class="btn btn-warning btn-lg" href="{{ url_for('cafes') }}" role="button">Show Me!</a>
  </div>
</div>
{% endblock %}
```

- The `jumbotron` class is custom‑styled in `styles.css` to be full viewport height and centered.
- The button links to the `cafes` route using `url_for('cafes')`.

### 3.4 Cafes Listing Page (`cafes.html`)

This is the core page where all data is displayed. The route `/cafes` passes the CSV data as a list of rows (`cafes` variable) to the template.

#### 3.4.1 Passing Data from the Route

```python
@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]
    return render_template('cafes.html', cafes=list_of_rows)
```

- `list_of_rows` contains all rows, including the header at index 0 and data rows from index 1 onward.
- This list is passed to the template as `cafes`.

#### 3.4.2 Building the Table

The template constructs a table dynamically:

```html
<table class="table table-dark table-striped table-hover">
  <thead>
    <tr>
      {% for header in cafes[0] %}
        <th scope="col">{{ header }}</th>
      {% endfor %}
    </tr>
  </thead>
  <tbody>
    {% for row in cafes[1:] %}
      <tr>
        {% for item in row %}
          <td>
            {% if loop.index0 == 1 %}  {# location URL #}
              <a href="{{ item }}" target="_blank">Maps Link</a>
            {% else %}
              {{ item }}
            {% endif %}
          </td>
        {% endfor %}
        <td>
          <form action="{{ url_for('delete_cafe', cafe_id=loop.index0) }}" method="POST">
            <button type="submit" class="btn btn-danger">Delete</button>
          </form>
        </td>
      </tr>
    {% endfor %}
  </tbody>
</table>
```

- **Header row**: Iterates over `cafes[0]` (the first row) to create table headers. This ensures that if the CSV structure changes, the table headers automatically update.
- **Data rows**: `for row in cafes[1:]` loops over all rows after the header.
- **Cells**: An inner loop iterates over each item in the row. The special Jinja2 variable `loop.index0` gives the zero‑based index of the current iteration.
  - If the index is 1 (the second column, which is the location URL), the cell content is rendered as a clickable link (`<a href="{{ item }}" target="_blank">Maps Link</a>`).
  - Otherwise, the raw item text is displayed (this includes cafe name, times, and emoji ratings).
- **Delete button**: After displaying all data columns, an extra table cell is added containing a form with a POST method and a delete button. The form action points to `url_for('delete_cafe', cafe_id=loop.index0)`. Here, `loop.index0` refers to the current row’s index within the `cafes[1:]` loop, i.e., the zero‑based position of the cafe **among the data rows**. This value is passed as `cafe_id` to the delete route.

#### 3.4.3 Understanding `cafe_id` and Row Indexing

The `cafe_id` passed to the delete route is **not** the row number in the CSV file (which would include the header) but the index **within the data rows**. For example, the first data row (Lighthaus) has `loop.index0 = 0`, the second (Esters) has `1`, etc.

In the delete route, we must map this back to the actual row index in the full CSV list (including header). The code does:

```python
list_of_rows.pop(cafe_id + 1)
```

Because the header is at index 0, adding 1 shifts the data row index to its correct position in the full list.

### 3.5 The Delete Route and Its Interaction

When the delete button is clicked, the form submits a POST request to `/delete/<cafe_id>`. The route handles it as described in Step 1.

```python
@app.route('/delete/<int:cafe_id>', methods=['POST'])
def delete_cafe(cafe_id):
    # read all rows
    # pop the row at cafe_id+1
    # write back
    return redirect(url_for('cafes'))
```

- The `methods=['POST']` ensures that the route only accepts POST requests, preventing accidental deletion via a simple GET link.
- After deletion, the user is redirected back to the cafes page, where the updated list is shown.

### 3.6 Custom CSS Styling (`styles.css`)

The custom CSS creates a distinct visual theme:

- **Body**: Black background (`#000`), white text.
- **Links**: Cyan color (`#0ff`) with no underline until hover.
- **Buttons**: Transparent background, white border, sharp corners. On hover, background becomes white and text black.
- **Tables**: Borders and text in white, using Bootstrap’s `table-dark` class but overriding background to pure black.
- **Form controls**: Black background, white border, no border‑radius. Focus state removes the default Bootstrap glow and uses a subtle cyan border.
- **Jumbotron**: Full viewport height, flexbox centering.

```css
body {
  background-color: #000;
  color: #fff;
  font-family: 'Helvetica', 'Arial', sans-serif;
}

a {
  color: #0ff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.btn {
  border: 1px solid #fff;
  background-color: transparent;
  color: #fff;
  border-radius: 0;
}

.btn:hover {
  background-color: #fff;
  color: #000;
}

.table-dark {
  --bs-table-bg: #000;
  --bs-table-border-color: #fff;
  color: #fff;
}

/* etc. */
```

This CSS is loaded after Bootstrap, so it overrides Bootstrap’s default colors.

### 3.7 Navigation Between Pages

The user can navigate through:

- **Home page** → click “Show Me!” → cafes page.
- **Cafes page** → “Add a new cafe” link → add page.
- **Cafes page** → “Return to index page” → home page.
- **Add page** → “See all cafes” → cafes page.

These links use `url_for` to generate URLs, ensuring they remain correct even if routes change.

### 3.8 Summary of UI Data Flow

1. **Display**: The `/cafes` route reads the CSV and passes a list of rows to the template.
2. **Template rendering**:
   - Header row is generated from the first list element.
   - Data rows are looped; each cell is inspected – if it’s the second column, it becomes a clickable link.
   - A delete form is added with the row’s index as `cafe_id`.
3. **Delete action**: Submitting the form sends a POST request to `/delete/<cafe_id>`. The route manipulates the CSV and redirects back to `/cafes`.
4. **Add action**: The form on `/add` submits data, which is validated, transformed, and appended to the CSV. The user is redirected to `/cafes` to see the new entry.

The entire application follows a classic **Model‑View‑Controller** (MVC) pattern, where the CSV acts as the model, the Flask routes serve as controllers, and the Jinja2 templates are the views.

---

## Conclusion

This three‑step breakdown has covered:

1. **Data Layer** – storing, reading, and writing cafe data in a CSV file.
2. **Form Handling** – capturing user input with Flask-WTF, validating it, and transforming ratings into emojis.
3. **Display and Interaction** – rendering the data in a table with clickable links and delete functionality, all styled with a custom Tron theme.

