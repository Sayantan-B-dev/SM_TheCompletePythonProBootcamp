# Requirement 5: Be Able to Sort and Rank the Movies By Rating

## 1. Introduction

The final requirement brings the Top 10 Movies website to its full functionality: automatic ranking of movies based on their ratings. Currently, the front of each movie card displays “None” in large letters because the `ranking` field in the database is not assigned. The goal is to compute a ranking for each movie whenever the home page is loaded. The movie with the highest rating should receive rank 1, the second‑highest rank 2, and so on. If ratings change (through editing) or new movies are added, the rankings must adjust accordingly.

This requirement is implemented entirely in the home route function, without any changes to the HTML templates. The logic involves fetching all movies, sorting them by rating in descending order, assigning a sequential rank, updating the database, and finally passing the sorted list to the template.

---

## 2. Problem Statement

- The `ranking` column in the `Movie` table is currently empty (NULL) for all movies.
- The home page template (`index.html`) displays `movie.ranking` on the front of each card. Because the value is `None`, it shows “None”.
- We need to compute a ranking based on the `rating` column:
  - The highest rated movie gets rank 1.
  - The second highest gets rank 2, and so on.
  - If two movies have the same rating, the order among them is not critical, but they should receive consecutive ranks (e.g., both could share a rank or be assigned different ranks arbitrarily; for simplicity we assign distinct ranks based on the order they appear after sorting by rating and then by title or ID).
- The ranking must be stored in the database so that it persists and can be displayed immediately. However, because ratings may change, we should recalculate the rankings every time the home page is visited.

---

## 3. Solution Overview

The solution consists of modifying the `home()` function to:

1. Retrieve all movies from the database.
2. Sort them by rating in descending order. Movies without a rating (if any) can be placed at the end; we will treat `rating = None` as having a value of 0 or simply exclude them from ranking (keep their `ranking` as `None`).
3. Iterate over the sorted list and assign a rank (starting from 1) to each movie that has a rating.
4. Update each movie’s `ranking` attribute and commit the changes to the database.
5. Pass the sorted list (or a fresh query) to the template for rendering.

Because the rankings are stored, the template will display the correct number on the front of each card. The `index.html` template already contains the necessary conditional logic to show the ranking if it exists, otherwise “None”.

---

## 4. Step-by-Step Implementation

### 4.1. Understanding the Data Flow

When a user navigates to the home page (`/`), the `home()` function is called. Inside it, we have access to the database session. The current code might look like:

```python
@app.route("/")
def home():
    movies = db.session.execute(db.select(Movie).order_by(Movie.title)).scalars().all()
    return render_template("index.html", movies=movies)
```

This simply fetches all movies ordered by title. We will replace this with the ranking logic.

### 4.2. Sorting by Rating

To sort by rating descending, we modify the query:

```python
movies = db.session.execute(db.select(Movie).order_by(Movie.rating.desc())).scalars().all()
```

However, movies with `NULL` ratings will appear at the end when using `.desc()` because `NULL` is considered lower than any value. This is acceptable; we will later assign ranks only to those with a non‑`NULL` rating.

### 4.3. Assigning Ranks

After obtaining the sorted list, we need to assign a rank to each movie that has a rating. We will iterate over the list with an index (starting from 1). For each movie, if `movie.rating` is not `None`, we set `movie.ranking` to the current index and increment the index. Movies with `NULL` rating retain their `ranking` as `None` (or we could set them to `None` explicitly).

```python
rank = 1
for movie in movies:
    if movie.rating is not None:
        movie.ranking = rank
        rank += 1
    else:
        movie.ranking = None   # ensure it's None (though it might already be)
```

### 4.4. Committing Changes to the Database

After updating the ranking attributes, we must commit the session to persist the changes:

```python
db.session.commit()
```

**Important:** If we only need the rankings for display and don’t care about storing them, we could skip the commit and just assign ranks in memory, then pass the list to the template. However, the template expects `movie.ranking` to be the stored value. If we don’t commit, the database still has old (or `NULL`) values. The next time the page is loaded, the rankings would be recalculated, but the stored values would not reflect the current ranking. For consistency, it’s best to store them. That way, even if the application restarts, the latest rankings are preserved.

### 4.5. Returning the Sorted List to the Template

We already have the sorted list `movies`. We can pass it directly to `render_template`. The template will loop over it in the order we provide (which is already sorted by rating descending). Alternatively, we could re‑query after the update, but that’s unnecessary.

### 4.6. Complete `home()` Function

Putting it all together:

```python
@app.route("/")
def home():
    # Fetch all movies sorted by rating descending (NULLs last)
    movies = db.session.execute(
        db.select(Movie).order_by(Movie.rating.desc())
    ).scalars().all()
    
    # Assign ranking based on rating
    rank = 1
    for movie in movies:
        if movie.rating is not None:
            movie.ranking = rank
            rank += 1
        else:
            movie.ranking = None  # optional, ensures NULL for unrated
    
    # Commit the updated rankings to the database
    db.session.commit()
    
    return render_template("index.html", movies=movies)
```

### 4.7. Handling Ties (Optional)

If two movies have the same rating, they will appear consecutively in the sorted list. The above code assigns distinct ranks (e.g., if ratings are equal, one gets rank 3, the next gets rank 4). This is a simple and acceptable approach. If you prefer to give them the same rank (e.g., both 3rd place), you would need to detect equal ratings and adjust the ranking logic accordingly. However, the requirement does not specify tie‑breaking, so distinct consecutive ranks are fine.

---

## 5. Code Explanation

### 5.1. The Query

```python
db.select(Movie).order_by(Movie.rating.desc())
```

- `db.select(Movie)` creates a SELECT statement for the entire `Movie` table.
- `.order_by(Movie.rating.desc())` orders the results by the `rating` column in descending order. Because SQLite treats `NULL` as lower than any non‑`NULL` value, movies without a rating appear at the end.

### 5.2. Executing and Retrieving Objects

```python
db.session.execute(...).scalars().all()
```

- `db.session.execute()` runs the query and returns a `Result` object.
- `.scalars()` returns a `ScalarResult` that yields each row as a `Movie` instance (rather than a tuple).
- `.all()` collects all results into a Python list.

### 5.3. Ranking Assignment

```python
rank = 1
for movie in movies:
    if movie.rating is not None:
        movie.ranking = rank
        rank += 1
    else:
        movie.ranking = None
```

- We initialize `rank` to 1.
- For each movie in the sorted list, we check if it has a rating.
- If yes, we assign the current rank and increment the rank counter.
- If not, we explicitly set `ranking` to `None` (this step is optional because it might already be `None`, but it ensures consistency).
- The loop modifies the `Movie` objects in memory; these changes are tracked by SQLAlchemy.

### 5.4. Committing Changes

```python
db.session.commit()
```

- This saves all modified `Movie` objects to the database. Without this, the rankings would not persist.

---

## 6. Testing the Ranking Functionality

### 6.1. Initial State

Assume the database contains two movies:

- Phone Booth: rating 7.3, ranking `None`
- Avatar The Way of Water: rating 7.3, ranking `None`

### 6.2. First Visit to Home Page

- The query returns both movies. They have the same rating, so their order is arbitrary (could be based on primary key or insertion order). Let’s say Phone Booth comes first.
- Ranking assignment:
  - Phone Booth gets rank 1.
  - Avatar gets rank 2.
- Commit updates the database.
- The home page displays:
  - Phone Booth card with "1" on the front.
  - Avatar card with "2" on the front.

### 6.3. Editing a Rating

- Suppose we edit Avatar and change its rating to 9.0 (via the edit form). After submission, the database now has Avatar (rating 9.0) and Phone Booth (rating 7.3). The rankings are still 1 and 2 respectively.
- Navigate to the home page again:
  - The query returns Avatar first (rating 9.0), then Phone Booth (7.3).
  - Ranking assignment:
    - Avatar gets rank 1.
    - Phone Booth gets rank 2.
  - Commit updates the rankings.
- The home page now shows Avatar with rank 1, Phone Booth with rank 2.

### 6.4. Adding a New Movie

- Add a new movie (e.g., “Inception”) via the add flow. Initially it has no rating (rating `None`). The home page will display it with rank `None` (since rating is `None`, it appears last and gets no rank). After editing it to give it a rating, say 8.5, the next home page visit will recalculate:
  - Sorted order: Avatar (9.0), Inception (8.5), Phone Booth (7.3)
  - Rankings: Avatar = 1, Inception = 2, Phone Booth = 3
- Commit updates the database.

### 6.5. Edge Cases

- If all movies have `NULL` ratings, the loop never assigns any ranks. The front of each card will show “None”, which is correct.
- If a movie’s rating is deleted (set to `NULL`) via some unforeseen means, it will lose its rank.

---

## 7. Why Not Use SQL Window Functions?

An alternative approach would be to use SQL window functions like `RANK()` or `ROW_NUMBER()` to compute rankings on the fly without storing them. However, the template expects a stored `ranking` attribute, and the requirement explicitly says to assign the ranking in the home route. Storing the ranking also simplifies the template and ensures that the ranking persists across sessions, even if the server restarts and we forget to recalculate (though we always recalculate on home).

---

## 8. Complete Code for `main.py` (Relevant Section)

Here is the final version of the home route incorporating the ranking logic:

```python
@app.route("/")
def home():
    # Fetch all movies sorted by rating descending (NULLs last)
    movies = db.session.execute(
        db.select(Movie).order_by(Movie.rating.desc())
    ).scalars().all()
    
    # Assign ranking based on rating
    rank = 1
    for movie in movies:
        if movie.rating is not None:
            movie.ranking = rank
            rank += 1
        else:
            movie.ranking = None   # optional, but ensures NULL
    
    # Commit the updated rankings to the database
    db.session.commit()
    
    return render_template("index.html", movies=movies)
```

All other routes (`edit`, `delete`, `add`, `find`) remain unchanged.

---

## 9. Testing Checklist

- [ ] Home page initially shows “None” for all movies (if no ratings exist).
- [ ] After editing a movie to set a rating, the home page displays the correct rank for that movie.
- [ ] After adding a new movie and then editing it to set a rating, the home page recalculates ranks correctly.
- [ ] If two movies have the same rating, they receive consecutive ranks (e.g., 3 and 4) in the order they appear.
- [ ] Movies without a rating always show “None” and do not affect the ranking count.
- [ ] Refreshing the home page does not change the ranks unless ratings have been modified (because ranks are recomputed each time based on current ratings).

---

## 10. Conclusion

With the addition of the ranking logic, the Top 10 Movies website now fully meets the project requirements. Users can view their movies ranked by personal rating, edit ratings and reviews, delete movies, and add new movies via the TMDB API. The ranking is automatically updated every time the home page is loaded, ensuring that the list always reflects the current order.

This project demonstrates a complete CRUD (Create, Read, Update, Delete) application with external API integration, form handling, and database management using Flask and SQLAlchemy. The final result is a polished, functional web application that can be further extended (e.g., with user authentication, more detailed movie info, or sharing features).

---

## 11. Additional Resources

- [Flask-SQLAlchemy Query Guide](https://flask-sqlalchemy.palletsprojects.com/en/3.1.x/quickstart/#query-the-data)
- [SQLAlchemy ORDER BY Documentation](https://docs.sqlalchemy.org/en/20/core/selectable.html#sqlalchemy.sql.expression.Select.order_by)
