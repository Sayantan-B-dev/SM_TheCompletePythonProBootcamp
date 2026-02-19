# NumPy for Scientific Computing: A Comprehensive Guide

## Overview

NumPy (Numerical Python) is the foundational library for scientific computing in Python. It provides高性能 multidimensional array objects and tools for working with these arrays. This guide covers the essential features of NumPy through practical examples, including array creation, manipulation, linear algebra, and image processing.

---

## 1. Introduction to NumPy and ndarrays

NumPy’s primary data structure is the `ndarray` (n-dimensional array). It is a homogeneous container (all elements of the same data type) that allows efficient vectorized operations. Pandas, which you may already know, is built on top of NumPy; while Pandas excels at data manipulation (grouping, joining, missing data), NumPy shines in low-level mathematical computations.

### Key Concepts

- **Homogeneous**: All elements must have the same data type (e.g., all floats, all integers).
- **N-dimensional**: Can represent vectors (1D), matrices (2D), and tensors (3D or higher).
- **Vectorization**: Operations apply element-wise without explicit loops, leveraging optimized C code.

---

## 2. Creating ndarrays

### 2.1 Manual Creation with `np.array()`

You can create an array from a Python list:

```python
import numpy as np

# 1-dimensional array (vector)
vector = np.array([1.1, 9.2, 8.1, 4.7])
print(vector)
# Output: [1.1 9.2 8.1 4.7]

# 2-dimensional array (matrix)
matrix = np.array([[1, 2, 3, 9],
                   [5, 6, 7, 8]])
print(matrix)
# Output:
# [[1 2 3 9]
#  [5 6 7 8]]
```

### 2.2 Using `np.arange()`

`arange([start,] stop[, step])` generates evenly spaced values within a given interval.

```python
# Values from 10 to 29 (stop is exclusive)
a = np.arange(10, 30)
print(a)
# Output: [10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29]

# With step
b = np.arange(0, 10, 2)   # [0 2 4 6 8]
```

### 2.3 Using `np.linspace()`

`linspace(start, stop, num)` generates `num` evenly spaced numbers over the interval [`start`, `stop`], including both endpoints.

```python
# 9 values from 0 to 100 (inclusive)
x = np.linspace(0, 100, num=9)
print(x)
# Output: [  0.   12.5  25.   37.5  50.   62.5  75.   87.5 100. ]

# 9 values from -3 to 3
y = np.linspace(-3, 3, 9)
print(y)
# Output: [-3.   -2.25 -1.5  -0.75  0.    0.75  1.5   2.25  3.  ]
```

### 2.4 Random Arrays with `np.random.random()`

Generate arrays filled with random floats in the half-open interval [0.0, 1.0).

```python
# 3x3x3 array of random numbers
random_tensor = np.random.random((3, 3, 3))
print(random_tensor.shape)   # (3, 3, 3)
```

---

## 3. Array Attributes

- `ndarray.shape`: tuple of array dimensions.
- `ndarray.ndim`: number of dimensions (axes).
- `ndarray.dtype`: data type of elements.
- `ndarray.size`: total number of elements.

```python
print(vector.shape)    # (4,)
print(vector.ndim)     # 1

print(matrix.shape)    # (2, 4)
print(matrix.ndim)     # 2

print(random_tensor.shape)  # (3, 3, 3)
print(random_tensor.ndim)   # 3
```

---

## 4. Indexing and Slicing

NumPy indexing follows Python list conventions but extends to multiple dimensions.

### 1D Array

```python
a = np.arange(10, 30)
print(a[2])        # 12 (third element)
print(a[-3:])      # [27 28 29] (last three)
print(a[3:6])      # [13 14 15]
print(a[12:])      # [22 23 24 25 26 27 28 29]
print(a[::2])      # [10 12 14 16 18 20 22 24 26 28] (every second)
```

### 2D Array

Use `[row, column]` indexing. The colon `:` selects all elements along that axis.

```python
matrix = np.array([[1, 2, 3, 9],
                   [5, 6, 7, 8]])

# Element at row 1, column 2 (0‑based)
print(matrix[1, 2])   # 7

# Entire first row
print(matrix[0, :])   # [1 2 3 9]

# Entire second column
print(matrix[:, 1])   # [2 6]
```

### 3D Array (Tensors)

Higher dimensions require an index for each axis.

**Example array** (shape (3,2,4)):

```python
mystery_array = np.array([[[0, 1, 2, 3],
                           [4, 5, 6, 7]],
                          [[7, 86, 6, 98],
                           [5, 1, 0, 4]],
                          [[5, 36, 32, 48],
                           [97, 0, 27, 18]]])
```

- **Access value 18**: It is at axis0=2, axis1=1, axis2=3 → `mystery_array[2, 1, 3]`.
- **Retrieve [97, 0, 27, 18]**: All elements at axis2 (third axis) for axis0=2, axis1=1 → `mystery_array[2, 1, :]`.
- **Retrieve 3x2 matrix of first elements along axis2**: `mystery_array[:, :, 0]` gives:
  ```
  [[ 0  4]
   [ 7  5]
   [ 5 97]]
  ```

---

## 5. Useful Array Manipulation Functions

### 5.1 Reversing an Array

```python
a = np.arange(10, 30)
reversed_a = np.flip(a)          # or a[::-1]
print(reversed_a)
# [29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10]
```

### 5.2 Finding Non‑Zero Indices

```python
b = np.array([6, 0, 9, 0, 0, 5, 0])
nonzero_indices = np.nonzero(b)
print(nonzero_indices)   # (array([0, 2, 5]),)  → tuple of arrays
```

### 5.3 Rotating an Array (2D)

```python
matrix = np.array([[1, 3],
                   [0, 1],
                   [6, 2],
                   [9, 7]])
rotated = np.rot90(matrix)
print(rotated)
# [[3 1 2 7]
#  [1 0 6 9]]
```

---

## 6. Broadcasting and Scalar Operations

**Broadcasting** allows NumPy to perform operations between arrays of different shapes by “stretching” the smaller array to match the larger one.

```python
matrix = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8]])

# Add a scalar to every element
print(matrix + 10)
# [[11 12 13 14]
#  [15 16 17 18]]

# Multiply every element by 5
print(matrix * 5)
# [[ 5 10 15 20]
#  [25 30 35 40]]
```

Broadcasting works for any arithmetic operation (+, -, *, /, **, etc.) and also for comparisons.

---

## 7. Linear Algebra with NumPy

### 7.1 Vector Operations

NumPy treats arrays as mathematical vectors/matrices, so operations are element‑wise by default.

```python
v1 = np.array([4, 5, 2, 7])
v2 = np.array([2, 1, 3, 3])

print(v1 + v2)   # [ 6  6  5 10]  (element‑wise addition)
print(v1 * v2)   # [ 8  5  6 21]  (element‑wise multiplication)
```

Contrast with Python lists, which concatenate on `+` and error on `*`.

### 7.2 Matrix Multiplication

For true matrix multiplication (dot product), use `np.matmul()` or the `@` operator.

**Example**:

```python
A = np.array([[1, 3],
              [0, 1],
              [6, 2],
              [9, 7]])          # shape (4,2)

B = np.array([[4, 1, 3],
              [5, 8, 5]])        # shape (2,3)

C = np.matmul(A, B)               # or A @ B
print(C.shape)                    # (4,3)
print(C)
# [[19 25 18]
#  [ 5  8  5]
#  [34 22 28]
#  [71 65 62]]
```

**Manual verification of selected elements**:

- `c12` (row1, col2) = row1 of A dot col2 of B = (1,3) · (1,8) = 1*1 + 3*8 = 25.
- `c33` (row3, col3) = row3 of A dot col3 of B = (6,2) · (3,5) = 6*3 + 2*5 = 28.

---

## 8. Working with Images as ndarrays

Images are essentially 3D arrays: height × width × color channels (RGB). NumPy allows direct manipulation of pixel values.

### 8.1 Loading an Image

Using `scipy.misc.face()` (a built‑in raccoon image) or PIL for custom images.

```python
from scipy import misc
import matplotlib.pyplot as plt

img = misc.face()           # returns a NumPy array
print(type(img))             # <class 'numpy.ndarray'>
print(img.shape)             # (768, 1024, 3)
print(img.ndim)              # 3
plt.imshow(img)
plt.show()
```

The array values are unsigned 8‑bit integers (0–255).

### 8.2 Converting to Grayscale

Grayscale conversion uses the luminance formula:  
`Y = 0.2126 * R + 0.7152 * G + 0.0722 * B`  
But the formula expects RGB values in the range [0,1] (sRGB).

**Steps**:

1. Normalize to [0,1]: `sRGB = img / 255`.
2. Matrix‑multiply with the luminance coefficients.
3. Display with `cmap='gray'`.

```python
grey_vals = np.array([0.2126, 0.7152, 0.0722])
sRGB = img / 255.0
gray_img = sRGB @ grey_vals          # or np.matmul(sRGB, grey_vals)

plt.imshow(gray_img, cmap='gray')
plt.show()
```

Without `cmap='gray'`, Matplotlib uses a false‑color map.

### 8.3 Image Transformations

Because the image is an ndarray, we can use NumPy functions to manipulate it.

**Flip upside down**:

```python
flipped = np.flip(gray_img)          # flips along all axes; for grayscale it works
# For a color image, you may want to flip only the rows:
# flipped_color = np.flip(img, axis=0)
plt.imshow(flipped, cmap='gray')
```

**Rotate 90 degrees**:

```python
rotated = np.rot90(img)               # rotates the whole array
plt.imshow(rotated)
```

**Invert colors (solarize)**:

```python
solarized = 255 - img                 # broadcasting subtraction
plt.imshow(solarized)
```

### 8.4 Using Your Own Images

To load a custom image (e.g., JPEG), use PIL:

```python
from PIL import Image

# Open image file
my_image = Image.open('yummy_macarons.jpg')
img_array = np.array(my_image)

print(img_array.shape)   # (height, width, 3)
plt.imshow(img_array)
```

You can then apply the same transformations.

---

## 9. Summary and Next Steps

After mastering these NumPy fundamentals, you are equipped to:

- Create and manipulate n‑dimensional arrays efficiently.
- Perform element‑wise operations and broadcasting.
- Execute linear algebra computations.
- Treat images as arrays and apply transformations.

**Further Resources**:

- [NumPy Quickstart Tutorial](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy: the absolute basics for beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [Broadcasting documentation](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [Linear algebra with NumPy](https://numpy.org/doc/stable/reference/routines.linalg.html)
