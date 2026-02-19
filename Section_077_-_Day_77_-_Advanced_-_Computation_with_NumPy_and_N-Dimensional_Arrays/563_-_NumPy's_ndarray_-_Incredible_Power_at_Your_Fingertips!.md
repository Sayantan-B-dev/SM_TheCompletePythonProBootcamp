# NumPy ndarray: The Foundation of Scientific Computing in Python

## Overview

NumPy (Numerical Python) is the fundamental package for numerical computation in Python. Its core data structure is the **ndarray** (n‑dimensional array), a fast and flexible container for large datasets in Python. The ndarray enables efficient vectorized operations, which are essential for data science, machine learning, and scientific computing.

This guide provides a thorough exploration of the ndarray, including its properties, creation, indexing, and slicing across different dimensions. You will learn how to think in terms of axes and how to access and manipulate data in 1‑dimensional, 2‑dimensional, and higher‑dimensional arrays.

---

## 1. Importing NumPy

By convention, NumPy is imported under the alias `np`:

```python
import numpy as np
```

This gives you access to all NumPy functions and the `ndarray` type.

---

## 2. What is an ndarray?

An `ndarray` is a **homogeneous**, **n‑dimensional** container:

- **Homogeneous** means all elements are of the same data type (e.g., all floats, all integers, all booleans). This allows NumPy to store data in contiguous memory blocks, enabling fast operations.
- **n‑dimensional** means the array can have any number of dimensions:
  - 1‑dimensional (a vector)
  - 2‑dimensional (a matrix)
  - 3‑dimensional (a tensor) – the fundamental data structure in deep learning frameworks like TensorFlow.
  - Higher dimensions (e.g., for video data or multi‑channel images).

---

## 3. 1‑Dimensional Arrays (Vectors)

### 3.1 Creating a 1D Array

The simplest way to create an ndarray is to pass a Python list to `np.array()`:

```python
vector = np.array([1.1, 9.2, 8.1, 4.7])
```

### 3.2 Basic Attributes

- `shape`: returns a tuple of the array’s dimensions. For a 1D array, it is `(n,)` where `n` is the number of elements.
- `ndim`: returns the number of dimensions (axes).

```python
print(vector.shape)   # (4,)
print(vector.ndim)    # 1
```

### 3.3 Indexing and Slicing

Indexing works exactly like Python lists:

```python
print(vector[2])      # 8.1  (third element, index 2)
print(vector[-1])     # 4.7  (last element)
```

Slicing with the colon `:` selects a range of elements:

```python
print(vector[1:3])    # [9.2 8.1] (elements at indices 1 and 2)
print(vector[:2])     # [1.1 9.2] (first two elements)
print(vector[::2])    # [1.1 8.1] (every second element)
```

---

## 4. 2‑Dimensional Arrays (Matrices)

### 4.1 Creating a 2D Array

Pass a list of lists to `np.array()`. Each inner list becomes a row.

```python
matrix = np.array([[1, 2, 3, 9],
                   [5, 6, 7, 8]])
```

### 4.2 Axes and Shape

In a 2D array, the first axis (axis 0) corresponds to rows, the second axis (axis 1) to columns.

```python
print(matrix.ndim)           # 2
print(matrix.shape)          # (2, 4)  → 2 rows, 4 columns
print(f"Rows: {matrix.shape[0]}, Columns: {matrix.shape[1]}")
```

### 4.3 Indexing

To access a specific element, provide indices for both axes: `[row, column]`.

```python
# Element at row 1 (second row), column 2 (third column)
print(matrix[1, 2])          # 7
```

To select an entire row or column, use the colon `:` to indicate “all elements along that axis”:

```python
# Entire first row
print(matrix[0, :])          # [1 2 3 9]

# Entire second column
print(matrix[:, 1])          # [2 6]
```

You can also combine slicing on both axes:

```python
# Submatrix: rows 0 and 1, columns 1 to 3 (exclusive of 3 means columns 1 and 2)
print(matrix[0:2, 1:3])      # [[2 3]
                              #  [6 7]]
```

---

## 5. N‑Dimensional Arrays (Tensors)

Arrays with three or more dimensions are often called **tensors**. They are common in deep learning (e.g., batches of images, video frames) and scientific computing.

### 5.1 Creating a 3D Array

A 3D array can be thought of as a stack of 2D matrices. The creation uses nested lists accordingly.

```python
tensor = np.array([[[0, 1, 2, 3],
                    [4, 5, 6, 7]],
                   
                   [[7, 86, 6, 98],
                    [5, 1, 0, 4]],
                   
                   [[5, 36, 32, 48],
                    [97, 0, 27, 18]]])
```

### 5.2 Understanding Axes

- **Axis 0** (first axis): the outermost dimension – in this case, 3 elements (the three 2D slices).
- **Axis 1** (second axis): the next dimension – each slice has 2 rows.
- **Axis 2** (third axis): the innermost dimension – each row has 4 columns.

Thus the shape is `(3, 2, 4)`.

```python
print(tensor.ndim)            # 3
print(tensor.shape)           # (3, 2, 4)
```

### 5.3 Indexing in 3D

To access a specific element, you must provide an index for each axis: `[axis0_index, axis1_index, axis2_index]`.

**Example: retrieving the value 18**

Looking at the array, `18` is in:
- axis 0: third slice (index 2)
- axis 1: second row of that slice (index 1)
- axis 2: fourth column (index 3)

```python
print(tensor[2, 1, 3])        # 18
```

### 5.4 Slicing in Higher Dimensions

The colon `:` selects all elements along a given axis.

**Retrieve a 1D vector** – for instance, the entire third row of the third slice (`[97, 0, 27, 18]`):

```python
# axis0=2, axis1=1, all of axis2
print(tensor[2, 1, :])        # [97  0 27 18]
```

**Retrieve a 2D matrix** – for example, a 3×2 matrix composed of all first elements along axis2:

```python
# All along axis0 and axis1, but only the first element (index 0) of axis2
print(tensor[:, :, 0])
# Output:
# [[ 0  4]
#  [ 7  5]
#  [ 5 97]]
```

**Explanation**: The expression `[:, :, 0]` keeps axis0 and axis1 unchanged, but takes only index 0 of axis2, producing a 3×2 matrix.

### 5.5 Visualising Axes

When working with higher dimensions, it helps to think of the indices as coordinates. For a 3D array, you can imagine a cube where each cell is defined by three coordinates (depth, row, column). The colon acts as a wildcard, selecting an entire slice along that dimension.

---

## 6. Why Homogeneity Matters

All elements in an ndarray must have the same data type. This constraint allows NumPy to:

- Store data in contiguous memory, leading to faster access and vectorized operations.
- Perform operations without type checking each element, crucial for performance in large datasets.
- Enable broadcasting (see later sections) where operations between arrays of different shapes become possible.

You can check the data type with the `dtype` attribute:

```python
print(vector.dtype)   # float64 (or similar, depending on your system)
print(matrix.dtype)   # int64
```

---

## 7. Summary of Key Concepts

- **ndarray**: homogeneous, n‑dimensional container.
- **shape**: tuple of axis lengths.
- **ndim**: number of axes.
- **Indexing**: `[axis0, axis1, ...]`.
- **Slicing**: `:` selects all elements along an axis.
- **Axes**: dimensions are numbered from 0 (outermost) to n‑1 (innermost).

Mastering these fundamentals is essential for effectively using NumPy in data analysis, image processing, linear algebra, and machine learning.

---

## 8. Further Reading

- [NumPy Quickstart Tutorial](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [TensorFlow and tensors](https://www.tensorflow.org/guide/tensor) – shows how deep learning frameworks build on these concepts.
