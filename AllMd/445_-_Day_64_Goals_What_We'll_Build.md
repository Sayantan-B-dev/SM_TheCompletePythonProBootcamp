# Day 64: Top 10 Movies Website – Project Overview

## 1. Introduction

Day 64 of the course focuses on building a fully functional web application that allows users to create, manage, and rank their personal list of top movies. This project serves as a practical exercise to integrate several key web development technologies:

- **Flask** as the web framework
- **Flask-SQLAlchemy** for database interactions
- **WTForms** (with Bootstrap-Flask) for form handling
- **SQLite** as the database engine
- **The Movie Database (TMDB) API** to fetch movie data dynamically

The final product will resemble popular list‑building websites such as [List Challenges](https://www.listchallenges.com/) or curated movie lists from [BFI](https://www2.bfi.org.uk/greatest-films-all-time), [Empire](https://www.empireonline.com/movies/features/best-movies-2/), and [The New York Times](https://www.imdb.com/list/ls058705802/). Users will be able to:

- View a collection of their top movies displayed as “cards”.
- Edit the rating and personal review for any movie.
- Delete movies from the list.
- Add new movies by searching the TMDB API.
- Automatically rank movies based on their ratings.

This document outlines the project goals, the technologies involved, and the high‑level requirements that will be implemented in the following lessons.

---

## 2. Project Objectives

By the end of Day 64, you will have built a web application that:

1. **Displays a list of movies** – Each movie is presented as a card showing its title, year, description, rating, ranking, a personal review, and a poster image. The home page renders all movies stored in the database.

2. **Allows editing of ratings and reviews** – Each movie card has an “Edit” button that leads to a form where the user can update the rating and review text.

3. **Supports deletion of movies** – A “Delete” button removes the corresponding movie entry from the database.

4. **Enables adding new movies** – A dedicated “Add Movie” page lets the user enter a movie title. The application queries the TMDB API for matching movies, presents a list of possible matches, and after selection fetches full details (title, poster, year, description) from the API. The new movie is then stored in the database, and the user is redirected to edit its rating and review.

5. **Automatically ranks movies** – Whenever the home page is loaded, all movies are sorted by their rating (descending) and each is assigned a ranking (1 = highest rating). This ranking is displayed on the front of the movie card.

---

## 3. Technology Stack

| Technology       | Purpose                                                                                   |
|------------------|-------------------------------------------------------------------------------------------|
| **Flask**        | Micro web framework to handle routes, requests, and responses.                           |
| **Flask-SQLAlchemy** | ORM (Object Relational Mapper) to interact with the SQLite database using Python objects. |
| **SQLite**       | Lightweight, file‑based database; perfect for development and small projects.            |
| **WTForms**      | Library for building and validating web forms. Used together with Bootstrap‑Flask for styling. |
| **Bootstrap‑Flask** | Simplifies rendering Bootstrap‑styled WTForms in templates.                            |
| **Requests**     | Python library to make HTTP requests to The Movie Database API.                          |
| **Jinja2**       | Templating engine (built into Flask) to dynamically generate HTML pages.                 |
| **The Movie Database (TMDB) API** | External API that provides movie metadata: titles, release years, posters, descriptions, etc. |

All dependencies are listed in the provided `requirements.txt` (or `requirements_3.13.txt`) and can be installed in a virtual environment.

---

## 4. Functional Requirements (in Detail)

The project is broken down into five core requirements, each covered in a separate lesson:

### Requirement 1 – View Movie List Items
- Create a SQLite database with a `Movie` table containing the fields: `id`, `title`, `year`, `description`, `rating`, `ranking`, `review`, `img_url`. The `title` must be unique.
- Populate the database with at least two sample movies using Python code.
- Query all movies when the home page is accessed and pass them to the `index.html` template for rendering.

### Requirement 2 – Edit a Movie’s Rating and Review
- Build a `RateMovieForm` using WTForms with fields for rating (float) and review (text).
- When the “Edit” button on a movie card is clicked, the application displays the `edit.html` page containing this form, pre‑filled with the current values.
- On form submission, update the corresponding movie record in the database with the new rating and review.

### Requirement 3 – Delete Movies from the Database
- Add a “Delete” button on each movie card.
- Clicking the button triggers a route that deletes the movie entry from the database and redirects back to the home page.

### Requirement 4 – Add New Movies via the Add Page
- Create an “Add Movie” page with a single‑field form for the movie title.
- Upon submission, the title is sent to the server, which then queries the TMDB API’s **search/movie** endpoint to retrieve a list of matching movies.
- Display the search results on a `select.html` page, allowing the user to pick the correct movie.
- After selection, fetch the full movie details from the TMDB API’s **movie/{id}** endpoint.
- Create a new `Movie` record with the title, poster URL, year, and description obtained from the API.
- Redirect the user to the edit page for that new movie so they can immediately add a rating and review.

### Requirement 5 – Sort and Rank the Movies by Rating
- When the home route is accessed, retrieve all movies from the database and sort them by rating in descending order.
- Assign a ranking to each movie (starting from 1 for the highest rated) and update the `ranking` field in the database.
- Display the ranking on the front of each movie card.

---

## 5. Expected Outcome

The final application will consist of four main pages:

- **Home page (`/`)** – Shows all movies as cards. Each card displays the ranking, title, year, description, rating, review, and a poster image. Two buttons (Edit, Delete) are available on each card.
- **Edit page (`/edit/<int:id>`)** – Contains a form to update the rating and review for a specific movie.
- **Add page (`/add`)** – Contains a form to enter a movie title.
- **Select page (`/select`)** – Displays the list of movies returned by the TMDB API for the user to choose from.

All interactions (add, edit, delete) will persist changes to the SQLite database, ensuring the list is updated correctly.

---

## 6. Resources

- [BFI Greatest Films of All Time](https://www2.bfi.org.uk/greatest-films-all-time)
- [Empire’s Best Movies](https://www.empireonline.com/movies/features/best-movies-2/)
- [The New York Times’ Top Movies (via IMDb)](https://www.imdb.com/list/ls058705802/)
- [List Challenges](https://www.listchallenges.com/)
- [The Movie Database API Documentation](https://developers.themoviedb.org/3)

---
