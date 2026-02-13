# Import Flask framework
from flask import Flask, render_template

# Create Flask app instance
app = Flask(__name__)

# Define route for homepage
@app.route("/")
def homepage():
    """
    This function renders an HTML template.
    Flask automatically searches inside 'templates' folder.
    """
    return render_template("index.html")

@app.route("/about")
def about_page():
    """
    Renders About page.
    """
    return render_template("about.html")


# Entry point of program
if __name__ == "__main__":
    app.run(debug=True)

