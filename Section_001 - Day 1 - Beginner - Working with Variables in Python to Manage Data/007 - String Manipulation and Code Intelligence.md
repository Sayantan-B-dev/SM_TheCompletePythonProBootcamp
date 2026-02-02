### Working with Strings in Python: New Lines, Tabs, Concatenation, Spaces, and Common Errors

---

### New Lines (`\n`)

```python
print("Line 1\nLine 2\nLine 3")
```

Each `\n` moves the cursor to a new line.

---

### Tabs (`\t`)

```python
print("Name\tAge\tCity")
print("Alex\t24\tDelhi")
```

`\t` inserts horizontal spacing, useful for simple alignment.

---

### Backslash and Quotes

```python
print("This is a backslash: \\")
print("She said, \"Python is fun\"")
```

---

### Raw Strings (Ignore Escape Characters)

```python
print(r"C:\new_folder\test.py")
```

Raw strings are useful for file paths and regex patterns.

---

### String Concatenation

```python
first = "Hello"
second = "World"

print(first + " " + second)
```

Strings can be joined using `+`.
Always add spaces manually when concatenating.

---

### Concatenation with Variables (Best Practice)

```python
name = "Sam"
age = 22

print(f"My name is {name} and I am {age} years old")
```

`f-strings` are cleaner and safer than `+`.

---

### Automatic Spacing with `print`

```python
print("Hello", "World", "Python")
```

Output:

```
Hello World Python
```

`print()` inserts spaces automatically between comma-separated values.

---

### Multi-line Strings

```python
message = """This is line one
This is line two
This is line three"""
print(message)
```

Useful for long text blocks and templates.

---

### Indentation and Spacing Errors (Very Important)

```python
if True:
print("Hello")
```

❌ **IndentationError**

Correct version:

```python
if True:
    print("Hello")
```

Python uses indentation to define blocks.
Missing or inconsistent spacing breaks execution.

---

### Mixing Tabs and Spaces (Common Mistake)

```python
if True:
\tprint("Hello")
```

❌ Avoid mixing tabs and spaces.

Best practice:

* Use **4 spaces per indentation level**
* Let your editor handle indentation

---

### Trailing and Leading Spaces

```python
text = "   hello world   "
print(text.strip())
```

Removes unnecessary whitespace.

---

### Common Beginner Mistakes

* Forgetting spaces when concatenating strings
* Using `+` with non-string types
* Misaligned indentation
* Overusing escape characters instead of raw strings

---

### Professional Tip

* Prefer **f-strings**
* Keep indentation consistent
* Use multi-line strings for readable output
* Let formatters handle spacing

Mastering strings early prevents a large class of bugs and readability issues later in real-world Python projects.
