### Python Strings, Data Types, Indexing & Type Conversion

**Practice Quizzes (with Answers)**

---

## **Quiz 1: Data Types**

What is the data type of each value?

1. `x = 10`
2. `x = "10"`
3. `x = 10.5`
4. `x = True`
5. `x = [1, 2, 3]`

**Answers:**

1. `int`
2. `str`
3. `float`
4. `bool`
5. `list`

---

## **Quiz 2: `len()` Function**

What will be the output?

```python
print(len("Python"))
print(len([1, 2, 3, 4]))
print(len({"a": 1, "b": 2}))
```

**Answer:**

```
6
4
2
```

---

## **Quiz 3: String Indexing**

What is the output?

```python
text = "Python"
print(text[1])
print(text[-1])
print(text[2:5])
```

**Answer:**

```
y
n
tho
```

---

## **Quiz 4: Step & Reverse Indexing**

What will this print?

```python
word = "abcdef"
print(word[::2])
print(word[::-1])
```

**Answer:**

```
ace
fedcba
```

---

## **Quiz 5: String Methods**

What is the output?

```python
text = " hello world "
print(text.strip().title())
```

**Answer:**

```
Hello World
```

---

## **Quiz 6: Type Conversion**

What happens here?

```python
age = input("Age: ")
print(age + 5)
```

**Answer:**
❌ `TypeError` — input is a string.

✔ Correct version:

```python
age = int(input("Age: "))
print(age + 5)
```

---

## **Quiz 7: Casting Results**

What is printed?

```python
print(int(3.9))
print(float(5))
print(str(100))
```

**Answer:**

```
3
5.0
100
```

---

## **Quiz 8: Boolean Conversion**

What are the results?

```python
print(bool(""))
print(bool("Python"))
print(bool(0))
print(bool(1))
```

**Answer:**

```
False
True
False
True
```

---

## **Quiz 9: Membership Operator**

What will be printed?

```python
print("a" in "cat")
print("z" in "cat")
```

**Answer:**

```
True
False
```

---

## **Quiz 10: Error Identification**

Which line causes an error?

```python
name = "Sam"
age = "25"
print(name + age)
print(age + 5)
```

**Answer:**
❌ `print(age + 5)` → `TypeError`
✔ Fix:

```python
print(int(age) + 5)
```

---

## **Quiz 11: Multiple Data Types**

What is the output?

```python
data = [10, "20", 30]
print(len(data))
```

**Answer:**

```
3
```

---

## **Quiz 12: Dictionary Length**

What does this print?

```python
info = {"name": "Alex", "age": 25, "city": "Delhi"}
print(len(info))
```

**Answer:**

```
3
```

---

## **Quiz 13: Slicing Edge Case**

What happens?

```python
word = "Hi"
print(word[5:])
```

**Answer:**

```
(empty string)
```

No error is raised.

---

## **Quiz 14: Replace & Count**

What is the output?

```python
text = "banana"
print(text.replace("a", "o"))
print(text.count("a"))
```

**Answer:**

```
bonono
3
```

---

## **Quiz 15: Best Practice Question**

Which is the **best** way to combine variables?

A. `"Age: " + age`
B. `"Age: {}".format(age)`
C. `f"Age: {age}"`

**Answer:**
✅ **C. `f"Age: {age}"`**

---
