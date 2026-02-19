# NumPy Learning Points and Summary

## 1. Introduction

This lesson provided a comprehensive introduction to NumPy, the fundamental library for numerical computing in Python. The key takeaway is the **ndarray** – a homogeneous, n‑dimensional array that enables fast, vectorized operations. By working through practical challenges, you gained hands‑on experience with array creation, manipulation, linear algebra, and even image processing. This summary consolidates all the essential concepts and techniques covered.

---

## 2. Creating Arrays Manually with `np.array()`

The most direct way to create an ndarray is to pass a Python list (or nested list) to `np.array()`.

```python
import numpy as np

# 1‑dimensional array (vector)
vector = np.array([1.1, 9.2, 8.1, 4.7])

# 2‑dimensional array (matrix)
matrix = np.array([[1, 2, 3, 9],
                   [5, 6, 7, 8]])

# 3‑dimensional array (tensor)
tensor = np.array([[[0, 1, 2, 3],
                    [4, 5, 6, 7]],
                   [[7, 86, 6, 98],
                    [5, 1, 0, 4]]])
```

**Key points:**
- All elements must have the same data type (homogeneous).
- The shape is inferred from the nesting structure.

---

## 3. Generating Arrays Using Built‑in Functions

NumPy provides several convenient functions to create arrays without manually listing every element.

### 3.1 `np.arange()`
Generates evenly spaced values within a given interval (half‑open, like Python’s `range`).

```python
a = np.arange(10, 30)          # [10 11 12 ... 29]
```

### 3.2 `np.linspace()`
Generates a specified number of evenly spaced values over a closed interval.

```python
x = np.linspace(0, 100, num=9) # [0. 12.5 25. ... 100.]
y = np.linspace(-3, 3, 9)      # [-3. -2.25 ... 3.]
```

### 3.3 `np.random.random()`
Creates an array of a given shape filled with random floats in [0.0, 1.0).

```python
noise = np.random.random((128, 128, 3))   # a 128×128 RGB image of random noise
```

---

## 4. Analysing Array Attributes

Every ndarray has several important attributes that describe its structure.

- `ndarray.shape` : a tuple of axis lengths.
- `ndarray.ndim`   : the number of dimensions (axes).
- `ndarray.dtype`  : the data type of the elements.
- `ndarray.size`   : the total number of elements.

```python
print(vector.shape)   # (4,)
print(matrix.ndim)    # 2
print(tensor.shape)   # (2, 2, 4)   (if using the tensor above)
print(noise.dtype)    # float64
```

Understanding these attributes is essential for manipulating arrays correctly.

---

## 5. Slicing and Subsetting

NumPy’s indexing and slicing syntax extends Python’s list notation to multiple dimensions.

### 5.1 1D Slicing
```python
a = np.arange(10, 30)
a[-3:]      # last three elements
a[3:6]      # elements at indices 3,4,5
a[12:]      # from index 12 to the end
a[::2]      # every second element
```

### 5.2 2D Slicing
```python
matrix = np.array([[1, 2, 3, 9],
                   [5, 6, 7, 8]])
matrix[1, 2]      # element at row 1, column 2 → 7
matrix[0, :]      # entire first row
matrix[:, 1]      # entire second column
matrix[:2, 1:3]   # submatrix: rows 0‑1, columns 1‑2
```

### 5.3 Higher‑Dimensional Slicing
For a 3D array, you need three indices (or slices). For example, given a tensor of shape `(3,2,4)`:

```python
tensor[2, 1, 3]      # single element
tensor[2, 1, :]      # 1D vector from that slice
tensor[:, :, 0]      # 2D matrix of all first elements of the last axis
```

**Rule:** The colon `:` selects all elements along that axis.

---

## 6. Linear Algebra Operations

NumPy supports both element‑wise arithmetic and true matrix multiplication.

### 6.1 Element‑wise Operations
```python
v1 = np.array([4, 5, 2, 7])
v2 = np.array([2, 1, 3, 3])
v1 + v2        # [6 6 5 10]
v1 * v2        # [8 5 6 21]
```

### 6.2 Scalar Operations and Broadcasting
A scalar can operate on every element of an array.

```python
matrix = np.array([[1, 2, 3, 4],
                   [5, 6, 7, 8]])
matrix + 10    # [[11 12 13 14]
               #  [15 16 17 18]]
```

Broadcasting extends this to arrays of different shapes, following strict rules. For example, adding a 1D array to a 2D array:

```python
A = np.array([[1, 2, 3],
              [4, 5, 6]])       # shape (2,3)
b = np.array([10, 20, 30])       # shape (3,)
A + b                            # [[11 22 33]
                                 #  [14 25 36]]
```

### 6.3 Matrix Multiplication
Use the `@` operator or `np.matmul()` for true matrix multiplication (dot product).

```python
A = np.array([[1, 3],
              [0, 1],
              [6, 2],
              [9, 7]])          # shape (4,2)
B = np.array([[4, 1, 3],
              [5, 8, 5]])        # shape (2,3)
C = A @ B                        # shape (4,3)
```

The element at row i, column j is the dot product of row i of A and column j of B.

---

## 7. Manipulating Images as ndarrays

An image is just a 3D array: height × width × colour channels (RGB). Grayscale images are 2D.

### 7.1 Loading and Inspecting an Image
```python
from scipy import misc
img = misc.face()                 # built‑in raccoon image
print(img.shape)                  # (768, 1024, 3)
print(img.ndim)                   # 3
print(img.dtype)                  # uint8
```

### 7.2 Converting to Grayscale
Normalise to [0, 1], then apply the luminance formula:

```python
grey_vals = np.array([0.2126, 0.7152, 0.0722])
sRGB = img / 255.0
gray = sRGB @ grey_vals            # shape (768, 1024)
plt.imshow(gray, cmap='gray')
```

### 7.3 Image Transformations
Because an image is an ndarray, any NumPy function works.

- **Flip upside down:** `np.flip(img, axis=0)`
- **Rotate 90°:** `np.rot90(img)`
- **Invert colours:** `255 - img`

```python
plt.imshow(np.flip(img, axis=0))
plt.imshow(np.rot90(img))
plt.imshow(255 - img)
```

### 7.4 Using Your Own Images
Load any image with PIL and convert to a NumPy array:

```python
from PIL import Image
my_img = Image.open('yummy_macarons.jpg')
img_array = np.array(my_img)
```

Now you can apply the same manipulations.

---

## 8. Completed Code

All the code examples and challenges from this lesson are available in the accompanying Jupyter notebook. You can download it and run it in Google Colab or your local environment to experiment further.

---

## 9. Conclusion

Congratulations on completing this mathematically intensive lesson! You have acquired the core NumPy skills that underpin data science, machine learning, and scientific computing. With these tools, you can efficiently handle numerical data, perform linear algebra, and even process images. The next steps are to apply these techniques in real‑world projects and to explore more advanced topics like broadcasting rules, universal functions, and integration with other libraries.

---

## 10. Further Resources

- [NumPy Quickstart Tutorial](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy: The Absolute Basics for Beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [Broadcasting Documentation](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [Linear Algebra in NumPy](https://numpy.org/doc/stable/reference/routines.linalg.html)
- [Matplotlib `imshow` Documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html)