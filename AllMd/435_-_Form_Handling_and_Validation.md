## Step 2: Form Handling and Validation

In this step, we focus on how user input is captured, validated, and transformed using **Flask-WTF** and **WTForms**. The central piece is the `CafeForm` class, which defines the fields and validation rules for adding a new cafe.

### 2.1 Form Definition with Flask-WTF

The form is defined in `main.py` as a class that inherits from `FlaskForm`. Each field corresponds to a column in the CSV file, except that the three rating fields use `SelectField` to let the user choose a rating level, which is later converted to an emoji string.

```python
class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Location URL', validators=[DataRequired(), URL()])
    open_time = StringField('Open Time (e.g., 8AM)', validators=[DataRequired()])
    close_time = StringField('Close Time (e.g., 5PM)', validators=[DataRequired()])
    coffee_rating = SelectField('Coffee Rating', choices=COFFEE_CHOICES, validators=[DataRequired()])
    wifi_rating = SelectField('Wifi Rating', choices=WIFI_CHOICES, validators=[DataRequired()])
    power_rating = SelectField('Power Outlet Rating', choices=POWER_CHOICES, validators=[DataRequired()])
    submit = SubmitField('Add Cafe')
```

- **`StringField`**: Used for cafe name, open time, and close time. The `DataRequired()` validator ensures the field is not empty.
- **`URLField`**: A specialized field that validates that the input is a proper URL (using the `URL()` validator). This ensures the location link is valid.
- **`SelectField`**: Provides a dropdown menu. The `choices` parameter is a list of `(value, label)` tuples. The value is what gets submitted (as a string), and the label is what the user sees. The `DataRequired()` validator ensures an option is selected.
- **`SubmitField`**: Renders as a submit button.

### 2.2 Defining Rating Choices with Emojis

To present the ratings in a visual way (emojis), the form uses predefined choice lists. These are defined at the top of `main.py`:

```python
COFFEE_CHOICES = [('0', '✘'), ('1', '☕️'), ('2', '☕☕'), ('3', '☕☕☕'), ('4', '☕☕☕☕'), ('5', '☕☕☕☕☕')]
WIFI_CHOICES = [('0', '✘'), ('1', '💪'), ('2', '💪💪'), ('3', '💪💪💪'), ('4', '💪💪💪💪'), ('5', '💪💪💪💪💪')]
POWER_CHOICES = [('0', '✘'), ('1', '🔌'), ('2', '🔌🔌'), ('3', '🔌🔌🔌'), ('4', '🔌🔌🔌🔌'), ('5', '🔌🔌🔌🔌🔌')]
```

- Each list contains tuples where the first element is the numeric value as a string (e.g., `'3'`) and the second element is the human‑friendly emoji representation (e.g., `'☕☕☕'`).
- The value `'0'` corresponds to `'✘'` (meaning none/unavailable). The emoji strings are used both in the dropdown options and later when storing the data in the CSV.
- The numeric values are used internally to map the user’s selection to the correct emoji string.

### 2.3 CSRF Protection

Flask-WTF automatically includes CSRF (Cross-Site Request Forgery) protection for all forms. A hidden field with a CSRF token is added to the form when rendered, and the token is validated on submission. This requires a secret key to be set in the app configuration:

```python
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
```

The secret key is used to sign the token. Without a valid token, the form will not validate.

### 2.4 Rendering the Form in the Template

The `add.html` template extends `base.html` and uses Bootstrap-Flask’s `render_form` macro to render the form with Bootstrap styling. This macro automatically handles field labels, error messages, and CSRF token.

```html
{% extends 'base.html' %}
{% from 'bootstrap5/form.html' import render_form %}

{% block content %}
<div class="container">
  <div class="row">
    <div class="col-sm-12 col-md-8">
      <h1>Add a new cafe into the database</h1>
      {{ render_form(form) }}
      <p class="space-above"><a href="{{ url_for('cafes') }}">See all cafes</a></p>
    </div>
  </div>
</div>
{% endblock %}
```

- `{{ render_form(form) }}` generates the complete HTML form, including labels, inputs, validation error messages, and the submit button. It also includes the CSRF token automatically.
- The `form` variable is passed from the route when rendering the template.

### 2.5 Processing the Form in the `add_cafe` Route

The `/add` route handles both GET and POST requests. When the user first visits the page (GET), an empty form is created and rendered. When the form is submitted (POST), the route checks if the data is valid using `form.validate_on_submit()`.

```python
@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Process the data...
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)
```

- `form.validate_on_submit()` does two things: it checks if the request is POST and then runs all validators on the submitted data. If both conditions are true, it returns `True`; otherwise `False`.
- When validation fails (e.g., missing field, invalid URL), the form is re‑rendered with error messages displayed next to the respective fields. The user can correct the errors and resubmit.

### 2.6 Transforming Form Data for CSV Storage

When validation succeeds, the form data is extracted and transformed into a format suitable for writing to the CSV. The three rating fields need to be converted from the selected numeric value to the corresponding emoji string.

```python
cafe_data = [
    form.cafe.data,
    form.location.data,
    form.open_time.data,
    form.close_time.data,
    COFFEE_CHOICES[int(form.coffee_rating.data)][1],
    WIFI_CHOICES[int(form.wifi_rating.data)][1],
    POWER_CHOICES[int(form.power_rating.data)][1]
]
```

- `form.cafe.data`, `form.location.data`, etc., retrieve the raw submitted values.
- For the rating fields, `form.coffee_rating.data` returns the selected **value** (e.g., `'3'`). This is a string, but we need to use it as an index into the `COFFEE_CHOICES` list. We convert it to an integer with `int(...)`.
- Then we index the appropriate choice list: `COFFEE_CHOICES[int_val]` gives the tuple `(value, label)`, and we take the second element `[1]` which is the emoji string (e.g., `'☕☕☕'`). This emoji string is what gets stored in the CSV.
- The resulting `cafe_data` list is a flat list of strings ready to be written as a CSV row.

### 2.7 Example of Data Flow

Let’s trace a submission:

- User selects **Coffee Rating** as `'3'` (the third option, label `☕☕☕`).
- `form.coffee_rating.data` = `'3'`.
- `int('3')` = `3`.
- `COFFEE_CHOICES[3]` = `('3', '☕☕☕')`.
- `COFFEE_CHOICES[3][1]` = `'☕☕☕'`.
- This string is stored in the CSV.

Similarly for Wi‑Fi and power.

### 2.8 Validation in Action

If the user omits the cafe name or enters an invalid URL, `validate_on_submit()` returns `False`, and the form is re‑rendered. The `render_form` macro automatically displays error messages below the problematic fields, styled with Bootstrap’s error classes. This provides immediate feedback without requiring custom code.

For example, if the location field is not a valid URL, the error “Invalid URL.” appears.

### 2.9 Summary of Form Handling

- The form defines fields, validators, and choices.
- Choices are stored as lists of (value, label) tuples, with emoji labels for visual appeal.
- The form is rendered using Bootstrap-Flask for a clean, responsive layout.
- On submission, the data is validated; if valid, it is transformed (numeric values → emoji strings) and then written to the CSV.
- CSRF protection is automatically enabled, securing the form against cross‑site attacks.

