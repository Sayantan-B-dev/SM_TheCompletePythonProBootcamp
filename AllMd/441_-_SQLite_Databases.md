# SQLite Databases: Persistent Storage for Python Applications

## 1. Overview of SQLite

SQLite is a self-contained, serverless, zero‑configuration, transactional SQL database engine. It is the most widely deployed database in the world – it is embedded in virtually every smartphone, many desktop applications, and is included by default in all Python installations. Unlike client‑server databases (e.g., PostgreSQL, MySQL), SQLite does not require a separate server process; it reads and writes directly to ordinary disk files. A complete SQL database is stored in a single cross‑platform file, making it ideal for desktop applications, embedded systems, and small to medium‑sized websites.

**Key characteristics:**

- **Serverless** – no separate server process to install, configure, or maintain.
- **Zero configuration** – no setup or administration required.
- **File‑based** – the entire database is a single file; copying it backs up the entire database.
- **ACID compliant** – transactions are atomic, consistent, isolated, and durable.
- **Lightweight** – small code footprint and low memory usage.
- **Cross‑platform** – database files are portable across different architectures.
- **Included in Python** – the `sqlite3` module is part of the standard library, so you can use it immediately without installing anything extra.

In this project, we will use SQLite to store our book collection so that data persists across server restarts.

## 2. Prerequisites

Before starting, ensure you have:

- Python installed (version 3.x). SQLite support is built‑in.
- A text editor or IDE (PyCharm recommended) to write and run Python scripts.
- (Optional) **DB Browser for SQLite** – a visual tool to inspect and manipulate SQLite database files. We will use it to verify our database contents. Download it from [https://sqlitebrowser.org/dl/](https://sqlitebrowser.org/dl/) (choose the appropriate installer for your operating system).

## 3. Creating an SQLite Database with Python

We will create a new SQLite database named `books-collection.db` and define a table `books` to store our book entries. The entire interaction with the database will be done using Python’s built‑in `sqlite3` module.

### 3.1 Importing the Module

Create a new Python file (e.g., `main.py`) and start by importing `sqlite3`:

```python
import sqlite3
```

### 3.2 Connecting to a Database

To work with an SQLite database, you must first establish a connection. The `connect()` function takes the database filename as an argument. If the file does not exist, it will be created automatically.

```python
db = sqlite3.connect("books-collection.db")
```

After this line executes, you will see a new file `books-collection.db` appear in your project directory (you may need to refresh the file tree). **Do not attempt to open this file with a text editor** – it is a binary file. We will use DB Browser to inspect it later.

### 3.3 Creating a Cursor

A cursor is an object that allows you to execute SQL commands and fetch results. Think of it as a “mouse pointer” that navigates and manipulates the database.

```python
cursor = db.cursor()
```

All subsequent database operations will be performed through this cursor.

### 3.4 Creating a Table

We need a table to hold our book data. The table will have four columns:

- `id` – a unique identifier for each book (integer, primary key).
- `title` – the book’s title (variable‑length string, maximum 250 characters, must be unique and cannot be empty).
- `author` – the author’s name (variable‑length string, maximum 250 characters, cannot be empty).
- `rating` – the user’s rating (floating‑point number, cannot be empty).

The SQL command to create such a table is:

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title VARCHAR(250) NOT NULL UNIQUE,
    author VARCHAR(250) NOT NULL,
    rating FLOAT NOT NULL
)
```

We execute this command using the cursor’s `execute()` method:

```python
cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
```

**Explanation of the SQL syntax:**

- `CREATE TABLE books` – creates a new table named `books`.
- The parentheses contain the column definitions separated by commas.
- `id INTEGER PRIMARY KEY` – defines an integer column `id` that serves as the primary key. The primary key uniquely identifies each row. SQLite automatically enforces uniqueness and creates an index for fast lookups. For `INTEGER PRIMARY KEY` columns, SQLite will auto‑increment the value if you omit it when inserting.
- `title VARCHAR(250) NOT NULL UNIQUE` – `VARCHAR(250)` means a variable‑length string up to 250 characters. `NOT NULL` ensures that a value must be provided. `UNIQUE` guarantees that no two rows can have the same title.
- `author VARCHAR(250) NOT NULL` – similar to title, but without the uniqueness constraint.
- `rating FLOAT NOT NULL` – a floating‑point number column that cannot be null.

**Note:** SQL keywords are conventionally written in uppercase, but SQLite is case‑insensitive. However, using uppercase improves readability.

### 3.5 Running the Code

After adding the above lines, run the Python script. If there are no errors, nothing will appear in the console – the table has been created silently. To verify, we need to inspect the database file using an external tool.

### 3.6 Inspecting the Database with DB Browser

1. **Download and install DB Browser for SQLite** from the link provided above.
2. Launch DB Browser.
3. Click **“Open Database”** and navigate to your project folder. Select `books-collection.db` and click **Open**.
4. You should see a window with several tabs. Click the **“Database Structure”** tab.
5. You will see a table named `books` listed. Expand it to view the columns: `id`, `title`, `author`, `rating`. This confirms that your table was created successfully.

![DB Browser showing books table structure](placeholder_for_image – describe that the user should see the table and columns)

### 3.7 Inserting Data into the Table

Now let’s add a book record. We use the `INSERT INTO` SQL command. The basic syntax is:

```sql
INSERT INTO table_name VALUES (value1, value2, ...)
```

The values must be provided in the same order as the columns were defined. For our `books` table, the order is `id`, `title`, `author`, `rating`.

To insert the book “Harry Potter” with id 1, author “J. K. Rowling”, and rating 9.3, we execute:

```python
cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', 9.3)")
```

**Important:** After any modification (INSERT, UPDATE, DELETE), you must **commit** the transaction to make the changes permanent. Otherwise, they will be lost when the connection is closed.

```python
db.commit()
```

**Complete code snippet for insertion:**

```python
cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', 9.3)")
db.commit()
```

### 3.8 Avoiding the “Table Already Exists” Error

If you run the entire script again (including the `CREATE TABLE` command), you will get an error:

```
sqlite3.OperationalError: table books already exists
```

Because the table was already created during the first run. To prevent this, **comment out the `CREATE TABLE` line** after the first execution, or restructure your code to check for existence (but for learning purposes, simply commenting it out is fine). Your final script might look like this:

```python
import sqlite3

db = sqlite3.connect("books-collection.db")
cursor = db.cursor()

# cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")

cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', 9.3)")
db.commit()
```

### 3.9 Viewing the Inserted Data

1. **Close the database in DB Browser** (click **“Close Database”**). This releases the file lock; otherwise, you may get a “database is locked” error when trying to access it from Python while DB Browser has it open.
2. Run the Python script again (with the `INSERT` line active).
3. Re‑open the database in DB Browser.
4. Go to the **“Browse Data”** tab. You should see the Harry Potter record displayed in the table.

![DB Browser showing inserted row](placeholder)

### 3.10 The Danger of Typos in SQL

SQL commands are plain strings, and the Python interpreter cannot check their validity. A single typo can cause the entire command to fail silently or raise an error. For example, if you accidentally write:

```python
cursor.execute("INSERT INTO books VALUE(1, 'Harry Potter', 'J. K. Rowling', 9.3)")
```

(note `VALUE` instead of `VALUES`), you will get an `sqlite3.OperationalError`. The error message may not be immediately obvious. This fragility is one of the main reasons developers prefer using an **Object Relational Mapper (ORM)** like SQLAlchemy, which allows you to write Python code instead of raw SQL strings. The ORM handles the correct SQL generation and provides type checking and auto‑completion in your IDE.

## 4. Complete Example Script

Here is a full example that creates the database and inserts one book. It includes a check to avoid re‑creating the table if it already exists (using `try-except`), which is a better practice.

```python
import sqlite3

db = sqlite3.connect("books-collection.db")
cursor = db.cursor()

# Create table if it does not exist
try:
    cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) NOT NULL, rating FLOAT NOT NULL)")
except sqlite3.OperationalError:
    print("Table already exists, skipping creation.")

# Insert a book
cursor.execute("INSERT INTO books VALUES(1, 'Harry Potter', 'J. K. Rowling', 9.3)")
db.commit()

# Verify by selecting all records
cursor.execute("SELECT * FROM books")
rows = cursor.fetchall()
print(rows)  # Should print [(1, 'Harry Potter', 'J. K. Rowling', 9.3)]

db.close()
```

## 5. Key Takeaways

- SQLite databases are simple files; use `sqlite3.connect()` to create or open one.
- A cursor is required to execute SQL commands.
- Tables are defined using the `CREATE TABLE` statement with appropriate column types and constraints.
- Data is inserted with `INSERT INTO` and must be committed with `db.commit()`.
- DB Browser for SQLite is a useful tool to visually inspect your database.
- Raw SQL is error‑prone; typos can cause runtime errors that are hard to debug.

## 6. Next Steps

Now that you understand how to work directly with SQLite, the next lesson will introduce **SQLAlchemy**, an ORM that lets you define tables as Python classes and interact with them using Python objects. This approach is more intuitive, less error‑prone, and integrates seamlessly with Flask applications. We will use SQLAlchemy to add persistent storage to our virtual bookshelf website.
