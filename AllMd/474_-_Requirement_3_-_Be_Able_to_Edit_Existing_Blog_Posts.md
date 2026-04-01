## Requirement 3 – Be Able to Edit Existing Blog Posts

### Overview

Requirement 3 adds the ability to modify existing blog posts. This involves:

- Activating the "Edit Post" button on each post's individual page to navigate to a pre-populated edit form.
- Creating a new route `/edit-post/<post_id>` that handles both GET (display form) and POST (process updates) requests.
- Modifying the `make-post.html` template to conditionally display "Edit Post" as the heading and to work with the same form used for creation.
- Auto-populating all form fields (title, subtitle, author, img_url, body) with the existing post's data when the user arrives in edit mode.
- Handling the form submission: updating the corresponding database record with the new data, while preserving the original publication date.
- Redirecting the user back to the individual post page (`post.html`) after a successful update.

This requirement corresponds to the "Update" operation in RESTful terms (PUT or PATCH). However, because HTML forms only support GET and POST, the update is implemented as a POST request to the same endpoint that renders the form. The route distinguishes between rendering and updating based on the request method.

### Prerequisites

Before implementing this requirement, ensure that:

- The application can successfully display individual posts (`/post/<post_id>`) as implemented in Requirement 1.
- The new post creation (Requirement 2) is fully functional, including the `CreatePostForm` and the `make-post.html` template.
- The database contains some posts to edit (either the sample posts or ones you've created).
- The "Edit Post" button is present in `post.html` (provided in the starting project) but currently lacks a proper `href` or points to a placeholder route.

### Step 1: Create the Edit Route

Define a new route `/edit-post/<int:post_id>` that accepts both GET and POST methods. The GET method should retrieve the post from the database and render the `make-post.html` template with a form pre-populated with the post's data. The POST method should update the post and redirect.

**Code Example – main.py**

```python
@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    # Fetch the post from the database or return 404
    post = db.get_or_404(BlogPost, post_id)
    
    # Create a form instance and pre-populate with the post's data
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    
    if edit_form.validate_on_submit():
        # Update the post object with form data
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = edit_form.author.data
        post.body = edit_form.body.data
        # Note: date is intentionally NOT updated to preserve original publication date
        db.session.commit()
        # Redirect to the individual post page
        return redirect(url_for('show_post', post_id=post.id))
    
    # For GET request, render the form with pre-populated data
    return render_template("make-post.html", form=edit_form, is_edit=True)
```

**Explanation:**

- The route captures `post_id` from the URL.
- `db.get_or_404(BlogPost, post_id)` retrieves the post or raises a 404 error if it doesn't exist.
- `CreatePostForm` is instantiated with keyword arguments corresponding to the post's current attributes. This pre-populates the form fields when the template is rendered.
- `edit_form.validate_on_submit()` works the same as before: returns `True` only for POST requests with valid data.
- On valid submission, each field of the `post` object is updated with the new data from the form. The `date` field is deliberately left untouched.
- The session is committed, and the user is redirected to the individual post page (`show_post` route) with the same `post_id`.
- For a GET request (or if validation fails), the template is rendered with the form. The additional `is_edit=True` is passed to the template so we can conditionally change the heading to "Edit Post".

### Step 2: Update the "Edit Post" Button in `post.html`

The button at the bottom of each individual post page must link to the edit route with the correct post ID.

**Code Example – in post.html**

```html
<!-- Existing content above -->
<a href="{{ url_for('edit_post', post_id=post.id) }}" class="btn btn-primary">Edit Post</a>
```

If the button was previously a placeholder or linked to a static route, this change dynamically generates the correct URL for each post.

### Step 3: Modify `make-post.html` to Display Appropriate Heading

The same template is used for both creating a new post and editing an existing one. We need to distinguish between the two modes in the user interface. This can be done by checking the `is_edit` variable passed from the route, or by inspecting the endpoint name.

**Code Example – in make-post.html (partial)**

```html
{% extends "layout.html" %}
{% from "bootstrap5/form.html" import render_form %}

{% block content %}
<div class="container">
    <div class="row">
        <div class="col-lg-8 col-md-10 mx-auto">
            <h1>{% if is_edit %}Edit Post{% else %}New Post{% endif %}</h1>
            {{ render_form(form, novalidate=True) }}
            {{ ckeditor.load() }}
            {{ ckeditor.config(name='body') }}
        </div>
    </div>
</div>
{% endblock %}
```

**Explanation:**

- The `is_edit` variable is passed from the `edit_post` route as `True`. For the `add_new_post` route, it is not passed (or you could pass `False`). The template checks for its existence and truthiness.
- If `is_edit` is true, the heading reads "Edit Post"; otherwise, "New Post". This provides clear context to the user.

Alternatively, you could check `request.endpoint` to determine the current route, but passing an explicit variable is more straightforward and less error-prone.

### Step 4: Understanding the Update Logic

#### Preserving the Publication Date

One subtle but important point: the original publication date should not change when a post is edited. In the sample blog, the date represents when the post was first created, not when it was last modified. Therefore, the `date` field is not included in the form and is not updated. If you wanted to track modification dates, you would need an additional `last_modified` field and update it accordingly, but that is beyond the current requirement.

#### Form Re-population

When the `CreatePostForm` is instantiated with keyword arguments matching the field names, WTForms automatically sets the initial values of those fields. This is why `edit_form = CreatePostForm(title=post.title, ...)` results in a form where all inputs are filled with the existing post's data. The user sees the current content and can modify it.

#### Handling Validation Errors

If the user submits the form with invalid data (e.g., missing required fields), `validate_on_submit()` returns `False`. The template is rendered again with the same form object (which now contains the submitted data and error messages). The `is_edit` variable remains `True`, so the heading stays "Edit Post". The user can correct the errors and resubmit. The post is not updated until validation passes.

#### Redirect After Update

After a successful update, the user is redirected to the individual post page. This follows the Post/Redirect/Get (PRG) pattern, which prevents duplicate form submissions if the user refreshes the page. The redirect also provides immediate visual feedback that the edit was successful.

### Step 5: Testing the Edit Functionality

1. Run the Flask application.
2. Navigate to the home page and click on any post title to view it.
3. At the bottom of the post, click the **Edit Post** button. You should be taken to `/edit-post/<post_id>` and see the form pre-filled with the post's current data.
4. Modify some fields (e.g., change the title, add text to the body). Ensure the CKEditor works as expected.
5. Click **Submit Post**. After submission, you should be redirected to the updated post page, and the changes should be visible.
6. Return to the home page and verify that the post's title/subtitle have been updated in the list (if those fields were changed).
7. Test validation by leaving a required field (e.g., title) empty and submitting. The form should reappear with error messages, and no changes should be saved.

### Detailed Explanation of Key Concepts

#### Why Not Use PUT/PATCH?

RESTful API design suggests using PUT or PATCH for updates. However, HTML forms only support GET and POST. To adhere strictly to REST, some developers use a hidden `_method` field or JavaScript to override the method. In this project, we keep it simple and use POST for the update. The route accepts both GET and POST, with GET for displaying the form and POST for processing the update. This is a common pattern in Flask applications.

#### Difference Between Creating and Editing

Although both creation and editing use the same form class, the logic differs:

- **Creation**: A new `BlogPost` object is instantiated, populated with form data (plus the current date), added to the session, and committed. The post gets a new auto-incremented ID.
- **Editing**: An existing `BlogPost` object is retrieved from the database, its attributes are updated with form data (excluding date), and the session is committed. The ID remains the same.

#### Data Persistence and Sessions

Flask-SQLAlchemy tracks changes to objects that are added to the session. When we modify the `post` object's attributes (e.g., `post.title = edit_form.title.data`), the session knows that this object has been changed. Calling `db.session.commit()` persists those changes to the database. There is no need to re-add the object to the session because it was already retrieved from the database and is already being tracked.

#### Security Considerations

- **Authorization**: In a production blog, you would want to ensure that only the author (or an admin) can edit a post. This project does not implement user authentication, so any visitor can edit any post. That is acceptable for a learning exercise but should be noted.
- **CSRF Protection**: The form includes a CSRF token (handled automatically by Flask-WTF), which protects against cross-site request forgery attacks. This is especially important for update operations.

### Troubleshooting Common Issues

| Issue | Possible Cause | Solution |
|-------|----------------|----------|
| Form does not pre-populate with existing data. | The form is instantiated without keyword arguments, or the argument names do not match the field names. | Ensure `CreatePostForm(title=post.title, ...)` uses the exact field names (`title`, `subtitle`, etc.) as defined in the form class. |
| After submission, the post is not updated. | The database session may not be committed, or the form validation failed. | Check that `db.session.commit()` is called after updating the post. Add print statements or use a debugger to verify `validate_on_submit()` returns `True`. Also check for validation errors in the form. |
| The date changes after editing. | The date field might be inadvertently updated. | Verify that the `date` attribute of the `post` object is not modified. Do not include a date field in the form, and do not assign a new date. |
| The heading still says "New Post" when editing. | The `is_edit` variable is not passed correctly, or the template condition is wrong. | In the `edit_post` route, ensure `render_template("make-post.html", form=edit_form, is_edit=True)` includes `is_edit=True`. In the template, check `{% if is_edit %}`. |
| The CKEditor does not show the existing body content. | The pre-population may not work for CKEditorField because it expects HTML. | The `body=post.body` argument should work; CKEditorField is a subclass of TextAreaField and accepts initial data. Verify that `post.body` contains the HTML content. |
| Redirect after edit goes to wrong page. | The `url_for('show_post', post_id=post.id)` may be using an incorrect function name. | Ensure the function name for the individual post route is `show_post` (or whatever you named it). Check the route definition. |

### Next Steps

With editing now implemented, the blog application supports Create, Read, and Update operations. The final requirement will add the ability to delete posts, completing the full CRUD cycle.

### Conclusion

Requirement 3 successfully extends the blog with editing capabilities. By reusing the same form template and form class, and by intelligently pre-populating fields and preserving the original date, the application provides a seamless editing experience. The pattern of a single route handling both display and update via GET and POST is a practical compromise given the limitations of HTML forms, and it keeps the code clean and maintainable.