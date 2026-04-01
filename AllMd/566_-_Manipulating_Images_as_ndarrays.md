# Manipulating Images as ndarrays: A Comprehensive Guide

Images are, at their core, collections of pixels. Each pixel is represented by one or more numerical values that define its colour. In digital imaging, the most common representation is the **RGB colour model**, where a colour is expressed as a combination of red, green, and blue intensities. Typically, each intensity is stored as an 8‑bit integer, ranging from 0 to 255.

In NumPy, an image is simply an **n‑dimensional array** (ndarray). A colour image is a 3‑dimensional array with dimensions:

- **height** (number of rows of pixels)
- **width** (number of columns of pixels)
- **channels** (usually 3 for RGB: red, green, blue)

Grayscale images are 2‑dimensional (height × width) because only one intensity value per pixel is needed.

This guide explores how to load, inspect, and manipulate images using NumPy, treating them as ndarrays. You will learn how to convert colour images to grayscale, flip, rotate, and invert them, and how to work with your own images.

---

## 1. Importing Required Libraries

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy import misc
from PIL import Image
```

- `numpy` provides the ndarray and all array operations.
- `matplotlib.pyplot` is used to display images.
- `scipy.misc` contains a sample image (a raccoon) for quick experimentation.
- `PIL` (Python Imaging Library, now `Pillow`) allows loading of custom image files.

---

## 2. Loading an Image as an ndarray

### 2.1 Using a Built‑in Sample Image

The `scipy.misc` module includes a colour image of a raccoon, accessible via `misc.face()`.

```python
img = misc.face()
```

`img` is now a NumPy ndarray. You can display it immediately with Matplotlib:

```python
plt.imshow(img)
plt.show()
```

### 2.2 Examining the Array

To understand the structure of the image, inspect its attributes:

```python
print(type(img))          # <class 'numpy.ndarray'>
print(img.shape)          # (768, 1024, 3)
print(img.ndim)           # 3
print(img.dtype)          # uint8
```

- `shape` tells us the image has 768 rows (height), 1024 columns (width), and 3 colour channels.
- `ndim = 3` confirms it is a 3‑dimensional tensor.
- `dtype = uint8` means each colour value is an unsigned 8‑bit integer (0–255).

### 2.3 Visualising the Raw Data

Printing a small portion of the array reveals the pixel values:

```python
print(img)
```

The output shows a 3D array where each inner list of three numbers represents the RGB values of a single pixel. For example, `[121, 112, 131]` might be the red=121, green=112, blue=131 of the top‑left pixel.

---

## 3. Understanding RGB Channels

The three channels can be thought of as three stacked 2D matrices:

- Channel 0: red intensities (shape 768×1024)
- Channel 1: green intensities (shape 768×1024)
- Channel 2: blue intensities (shape 768×1024)

You can access a single channel using slicing:

```python
red_channel = img[:, :, 0]
green_channel = img[:, :, 1]
blue_channel = img[:, :, 2]
```

Each of these is a 2D array (grayscale representation of that colour’s contribution). Displaying a single channel with `plt.imshow()` will show it in false colour unless you specify a colormap.

---

## 4. Converting a Colour Image to Grayscale

### 4.1 The Luminance Formula

Grayscale conversion combines the three colour channels into one intensity value per pixel. The human eye perceives different colours with different sensitivity; therefore a weighted sum is used. The standard **luminance formula** for sRGB (standard RGB) is:

```
Y_linear = 0.2126 * R + 0.7152 * G + 0.0722 * B
```

Where `R`, `G`, `B` are the red, green, and blue components **normalised to the range [0, 1]** (i.e., divided by 255).

### 4.2 Steps in NumPy

1. **Normalise the pixel values** to the [0, 1] range by dividing by 255.
2. **Multiply** the normalised array by the luminance coefficients.
3. The result is a 2D array of grayscale intensities.

```python
# Luminance coefficients
grey_vals = np.array([0.2126, 0.7152, 0.0722])

# Step 1: normalise to [0,1]
sRGB_array = img / 255.0

# Step 2: matrix multiplication (dot product) along the colour axis
# Each pixel (a 3‑element vector) is multiplied by the coefficients.
# Using @ or np.matmul() with appropriate dimensions.
img_gray = sRGB_array @ grey_vals   # shape becomes (768, 1024)
```

**Why `@` works here:**  
`sRGB_array` has shape (768, 1024, 3). `grey_vals` has shape (3,). In NumPy, when you use `@` between a 3D array and a 1D array, it performs a dot product on the last axis of the first array and the only axis of the second, effectively computing the weighted sum for each pixel. The result is a 2D array.

Alternatively:

```python
img_gray = np.matmul(sRGB_array, grey_vals)
```

### 4.3 Displaying the Grayscale Image

```python
plt.imshow(img_gray, cmap='gray')
plt.show()
```

The `cmap='gray'` argument tells Matplotlib to use a grayscale colour map. Without it, the default colour map (viridis) would be applied, giving a false‑colour representation.

**Comparison:**  
Running `plt.imshow(img_gray)` without `cmap` will display the image in false colours, which can be confusing.

---

## 5. Image Transformations Using NumPy

Because an image is an ndarray, any NumPy function that operates on arrays can be applied. Here we explore three common transformations: flipping (upside down), rotating, and inverting colours.

### 5.1 Flipping Upside Down (Vertical Flip)

Flipping an image vertically means reversing the order of rows. This can be done with `np.flip()`.

```python
flipped_gray = np.flip(img_gray)          # flips along all axes; for 2D, this flips rows and columns
# To flip only rows (vertical flip), specify axis=0:
flipped_gray = np.flip(img_gray, axis=0)

plt.imshow(flipped_gray, cmap='gray')
```

For a colour image, `np.flip(img, axis=0)` flips the rows, keeping the colour channels intact.

**How it works:**  
`np.flip` reverses the order of elements along the specified axis. For axis=0 (rows), the first row becomes the last, and so on.

### 5.2 Rotating the Image

`np.rot90()` rotates an array by 90 degrees counter‑clockwise. You can specify the number of rotations with the `k` parameter.

```python
rotated_color = np.rot90(img)          # 90° CCW
plt.imshow(rotated_color)

# Rotate 180° (two 90° rotations)
rotated_180 = np.rot90(img, k=2)
```

**Note:** After rotation, the shape changes: a (768, 1024, 3) image becomes (1024, 768, 3).

### 5.3 Inverting Colours (Solarisation)

Inverting an image means each colour value `v` becomes `255 - v`. This is a simple element‑wise subtraction using broadcasting.

```python
solarized = 255 - img
plt.imshow(solarized)
```

**Explanation:**  
`img` is a uint8 array with values 0–255. Subtracting it from 255 yields the complementary colour: black (0) becomes white (255), white becomes black, and all other colours are inverted.

---

## 6. Working with Your Own Images

The same principles apply to any image you load. However, you must ensure the image is in a format that NumPy can interpret as an array of RGB values.

### 6.1 Loading a Custom Image with PIL

```python
from PIL import Image

# Open the image file (supports many formats: JPEG, PNG, etc.)
my_image = Image.open('yummy_macarons.jpg')

# Convert to a NumPy array
img_array = np.array(my_image)
```

### 6.2 Verifying the Array Structure

```python
print(img_array.shape)      # e.g., (533, 799, 3)
print(img_array.ndim)       # 3
print(img_array.dtype)      # uint8 (most common for JPEG)
```

If your image is a PNG with transparency, it may have 4 channels (RGBA). In that case, you can either drop the alpha channel or convert to RGB first:

```python
my_image = Image.open('transparent.png').convert('RGB')
img_array = np.array(my_image)
```

### 6.3 Applying Transformations

You can now use all the techniques described above:

```python
# Grayscale conversion (if desired)
grey_vals = np.array([0.2126, 0.7152, 0.0722])
sRGB = img_array / 255.0
gray = sRGB @ grey_vals
plt.imshow(gray, cmap='gray')

# Flip
flipped = np.flip(img_array, axis=0)
plt.imshow(flipped)

# Rotate
rotated = np.rot90(img_array)
plt.imshow(rotated)

# Invert
inverted = 255 - img_array
plt.imshow(inverted)
```

---

## 7. Important Considerations and Pitfalls

- **Data Type Range:** When performing arithmetic on uint8 arrays, be aware of overflow. For example, `img_array + 50` could wrap around values above 255. It is safer to convert to a float type (e.g., `float32`) before operations and then clip or convert back.
- **Normalisation for Grayscale:** The luminance formula expects values in [0, 1]. Always divide by the maximum value (255 for 8‑bit images). If you have 16‑bit images, divide by 65535.
- **PNG with Alpha Channel:** Some PNGs have four channels (RGBA). If you try to apply the 3‑element luminance vector, you will get a broadcasting error. Either drop the alpha channel (`img_array[:, :, :3]`) or convert the image to RGB before conversion.
- **Matplotlib’s `imshow` Behaviour:** By default, `imshow` uses a colormap for 2D data. For 3D data with shape (M, N, 3) or (M, N, 4), it assumes RGB/RGBA data and displays correctly without a colormap. For grayscale (2D), always specify `cmap='gray'` to avoid false colours.

---

## 8. Summary

- An image is just a NumPy ndarray: a 3D array (height, width, channels) for colour, and a 2D array for grayscale.
- You can load built‑in images (`scipy.misc.face`) or any image using PIL.
- The array’s `shape`, `ndim`, and `dtype` reveal its dimensions and data format.
- Grayscale conversion uses the luminance formula and matrix multiplication with normalised values.
- NumPy functions like `flip`, `rot90`, and simple arithmetic (`255 - img`) enable powerful image manipulations.
- Working with custom images follows the same principles; be mindful of extra channels (alpha) and data type ranges.

These techniques are the foundation for more advanced image processing, computer vision, and deep learning applications, where images are routinely treated as tensors.

---

## 9. Further Reading and Resources

- [NumPy Quickstart Tutorial](https://numpy.org/doc/stable/user/quickstart.html)
- [Pillow (PIL) Documentation](https://pillow.readthedocs.io/)
- [Matplotlib `imshow` documentation](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html)
- [Luminance formula reference](https://en.wikipedia.org/wiki/Grayscale#Luma_coding_in_video_systems)

