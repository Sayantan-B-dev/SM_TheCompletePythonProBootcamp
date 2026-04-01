# Broadcasting, Scalars, and Matrix Multiplication in NumPy

## 1. Introduction

NumPy is designed for efficient numerical computations. One of its key strengths is the ability to perform vectorized operations on entire arrays without writing explicit loops. This includes arithmetic operations, comparisons, and more. This section covers:

- How NumPy handles element‑wise operations between vectors and matrices.
- The concept of **broadcasting**, which allows operations between arrays of different shapes.
- **Scalar operations** (a special case of broadcasting).
- **Matrix multiplication** (the dot product), a fundamental linear algebra operation that differs from element‑wise multiplication.

We also highlight the critical difference between NumPy’s behaviour and that of standard Python lists.

---

## 2. Element‑wise Operations on Vectors

### 2.1 NumPy Arrays vs Python Lists

Consider two NumPy vectors:

```python
import numpy as np

v1 = np.array([4, 5, 2, 7])
v2 = np.array([2, 1, 3, 3])
```

In NumPy, the `+` operator performs **element‑wise addition**:

```python
print(v1 + v2)   # [6 6 5 10]
```

Similarly, `*` performs element‑wise multiplication:

```python
print(v1 * v2)   # [ 8  5  6 21]
```

This behaviour is exactly what you would expect in mathematical vector arithmetic.

Contrast this with ordinary Python lists:

```python
list1 = [4, 5, 2, 7]
list2 = [2, 1, 3, 3]

print(list1 + list2)   # [4, 5, 2, 7, 2, 1, 3, 3]  (concatenation)
# print(list1 * list2) would raise a TypeError
```

Lists do not support element‑wise arithmetic; `+` concatenates and `*` repeats (for integer multiplication). NumPy’s design intentionally aligns with mathematical conventions.

---

## 3. Broadcasting

### 3.1 Definition

**Broadcasting** is a powerful mechanism that allows NumPy to perform operations on arrays of different shapes. The smaller array is “broadcast” across the larger array so that they have compatible shapes. The result is a new array with the shape of the larger one.

The most common case is **scalar broadcasting**, where a single number (scalar) operates with every element of an array.

### 3.2 Scalar Broadcasting

When you combine a scalar with an ndarray, NumPy “stretches” the scalar to match the array’s shape, performing the operation element‑wise.

#### Example with a 1D Array

```python
a = np.array([1, 2, 3, 4])
print(a + 10)      # [11 12 13 14]
print(a * 5)       # [ 5 10 15 20]
```

#### Example with a 2D Array

```python
matrix = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8]])

print(matrix + 10)
# [[11 12 13 14]
#  [15 16 17 18]]

print(matrix * 5)
# [[ 5 10 15 20]
#  [25 30 35 40]]
```

The scalar is conceptually replicated to match the shape of the matrix, but NumPy does this without actually creating a full copy, making it memory‑efficient.

### 3.3 Broadcasting Rules

Broadcasting is not limited to scalars. It follows a set of rules to determine whether two arrays are compatible:

1. **If the arrays have different numbers of dimensions**, the shape of the smaller array is padded with ones on its left side.
2. **Two dimensions are compatible if**:
   - they are equal, or
   - one of them is 1.
3. After broadcasting, each array behaves as if its shape were the element‑wise maximum of the two shapes.

If these conditions cannot be met, NumPy raises a `ValueError`.

#### Example: Adding a 1D Array to a 2D Array

```python
A = np.array([[1, 2, 3],
              [4, 5, 6]])          # shape (2,3)
b = np.array([10, 20, 30])         # shape (3,)

C = A + b
print(C)
# [[11 22 33]
#  [14 25 36]]
```

Here, `b` is broadcast across the rows of `A`. The rules: `A` has shape (2,3), `b` has shape (3,). The shapes are compared from the right: both have 3 in the last dimension; the missing dimension of `b` is treated as 1, and that 1 is stretched to match the 2 rows.

### 3.4 Visualising Broadcasting

The NumPy documentation provides several illustrations of broadcasting. The most important takeaway is that broadcasting avoids unnecessary data duplication and makes code both concise and fast.

---

## 4. Matrix Multiplication

Element‑wise multiplication (using `*`) is not the same as matrix multiplication (the dot product). In linear algebra, multiplying two matrices follows the rule:

\[
(C)_{ij} = \sum_{k} (A)_{ik} (B)_{kj}
\]

That is, the element in row i, column j of the product is the dot product of row i of the first matrix and column j of the second.

NumPy provides two equivalent ways to perform matrix multiplication:

- The `@` operator (introduced in Python 3.5)
- The `np.matmul()` function

Both require that the inner dimensions match: for `A` of shape `(m, n)` and `B` of shape `(n, p)`, the result has shape `(m, p)`.

### 4.1 Example

```python
A = np.array([[1, 3],
              [0, 1],
              [6, 2],
              [9, 7]])          # shape (4, 2)

B = np.array([[4, 1, 3],
              [5, 8, 5]])        # shape (2, 3)

C = A @ B                        # or np.matmul(A, B)
print(C.shape)                   # (4, 3)
print(C)
```

The output matrix `C` is:

```
[[19 25 18]
 [ 5  8  5]
 [34 22 28]
 [71 65 62]]
```

### 4.2 Manual Computation of Selected Elements

Let’s verify two entries:

- **`C[0, 1]`** (row 0, column 1, often denoted `c12` in 1‑based indexing):  
  Row 0 of A: `[1, 3]`  
  Column 1 of B: `[1, 8]`  
  Dot product: `1*1 + 3*8 = 1 + 24 = 25`

- **`C[2, 2]`** (row 2, column 2, `c33` in 1‑based indexing):  
  Row 2 of A: `[6, 2]`  
  Column 2 of B: `[3, 5]`  
  Dot product: `6*3 + 2*5 = 18 + 10 = 28`

These match the computed values.

### 4.3 When to Use `@` vs `np.matmul()`

- `@` is an operator, making expressions like `A @ B` concise and readable.
- `np.matmul(A, B)` is a function call; it can be useful when you need to pass an optional `out` argument or when working with older Python versions (pre‑3.5).
- For higher‑dimensional arrays, both behave similarly, performing matrix multiplication on the last two axes while broadcasting over the others. For more details, refer to the [NumPy matmul documentation](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html).

### 4.4 Important Distinction: `*` vs `@`

- `*` performs **element‑wise** multiplication. If you multiply two 2D arrays of the same shape with `*`, you get the Hadamard product (each element multiplied individually), not the matrix product.
- `@` (or `matmul`) performs the true **matrix multiplication** (dot product) according to linear algebra rules.

This distinction is crucial in scientific computing and machine learning.

---

## 5. Challenge: Matrix Multiplication Verification

**Task**: Using the matrices `a1` and `b1` provided, compute the matrix product manually for the elements `c12` and `c33`, then verify with NumPy.

```python
a1 = np.array([[1, 3],
               [0, 1],
               [6, 2],
               [9, 7]])

b1 = np.array([[4, 1, 3],
               [5, 8, 5]])
```

**Solution**:

```python
c = a1 @ b1
print(c[0, 1])   # 25
print(c[2, 2])   # 28
```

The manual calculations confirm these values.

---

## 6. Summary

- **Element‑wise operations** are the default in NumPy (`+`, `-`, `*`, `/`, etc.) and are applied positionally.
- **Broadcasting** extends this to arrays of different shapes, following strict rules. Scalar operations are the simplest form of broadcasting.
- **Matrix multiplication** is a distinct operation, performed with `@` or `np.matmul()`, and follows linear algebra rules.
- Always choose the right operator: `*` for element‑wise, `@` for matrix multiplication.

Understanding these concepts is essential for effective use of NumPy in data science, image processing, simulations, and machine learning.

---

## 7. Further Reading

- [NumPy Broadcasting Documentation](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [NumPy Linear Algebra](https://numpy.org/doc/stable/reference/routines.linalg.html)
- [PEP 465 – A dedicated infix operator for matrix multiplication](https://peps.python.org/pep-0465/)
