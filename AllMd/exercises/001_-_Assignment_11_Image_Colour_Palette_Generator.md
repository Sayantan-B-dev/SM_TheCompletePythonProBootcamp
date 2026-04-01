# Color Extractor - Documentation

## 1. Introduction
Color Extractor is a web application built with Flask that allows users to upload an image and extract all distinct colors present in it. The application quantizes the image to a 32‑color palette using the median cut algorithm, counts pixel frequencies, and displays each color with its HEX code and percentage of the image. The interface is styled with Tailwind CSS and includes live preview, copy-to-clipboard functionality, and a simulated progress bar during processing.

## 2. Technologies Used
- **Backend:** Python 3, Flask, Pillow (PIL), NumPy
- **Frontend:** HTML5, Tailwind CSS, JavaScript
- **Development Tools:** Werkzeug (secure file handling)

## 3. Installation and Setup

### Prerequisites
- Python 3.7 or higher installed on your system.
- pip (Python package installer).

### Steps

1. **Clone or download the project** (if using version control). Otherwise create a project folder with the provided files.

2. **Navigate to the project directory** in your terminal.

3. **Create a virtual environment** (recommended):
   ```
   python -m venv venv
   ```
   Activate it:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. **Install required packages**:
   Create a `requirements.txt` file with the following content:
   ```
   Flask==2.3.3
   numpy==1.24.3
   Pillow==10.0.0
   ```
   Then run:
   ```
   pip install -r requirements.txt
   ```

5. **Ensure the upload folder exists**:
   The application automatically creates `static/uploads/` when it runs. You can also create it manually.

6. **Run the application**:
   ```
   python app.py
   ```

7. **Open your browser** and go to `http://127.0.0.1:5000/`.

## 4. Application Workflow

1. User accesses the home page (GET `/`).
2. User selects an image file using the upload form.
3. The browser shows a live preview of the selected image.
4. Upon form submission (POST `/`), the file is validated and saved to the `static/uploads/` folder.
5. The saved image is processed by the `get_colors()` function:
   - Image is opened and converted to RGB.
   - Quantized to a 32‑color palette using median cut.
   - Palette colors are extracted.
   - Pixel indices are counted using NumPy and `collections.Counter`.
   - For each used color, the count, percentage, and HEX code are computed.
6. The extracted colors are passed to the template (`index.html`) along with the uploaded image filename.
7. The template renders the color swatches in a responsive grid.
8. User can copy any HEX code by clicking the copy button.

## 5. Data Flow Diagram (Mermaid)

The following Mermaid flowchart illustrates the data flow from upload to result display.

```mermaid
flowchart TD
    A[User selects image file] --> B[Browser shows live preview]
    B --> C[User submits form]
    C --> D[Flask route index() POST]
    D --> E{File present and allowed?}
    E -- No --> F[Flash error, redirect to GET]
    E -- Yes --> G[Save file with secure_filename]
    G --> H[Call get_colors(filepath)]
    
    subgraph get_colors
        H --> I[Open image with PIL, convert to RGB]
        I --> J[Quantize to 32 colors using median cut]
        J --> K[Extract palette colors as list of RGB tuples]
        K --> L[Convert quantized image to numpy array of indices]
        L --> M[Count frequencies of each index with Counter]
        M --> N[For each used index, compute RGB, count, percentage, hex]
    end
    
    N --> O[Return list of color dictionaries]
    O --> P[Render index.html with colors and uploaded_image]
    P --> Q[Browser displays color swatches grid]
    Q --> R[User copies HEX code via JavaScript]
```

## 6. Function Explanations

### 6.1 `allowed_file(filename)`
- **Purpose:** Validate that the uploaded file has an allowed extension.
- **Parameters:** `filename` – name of the uploaded file.
- **Logic:** Checks if the filename contains a dot and if the extension (lowercase) is in the set `{'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}`.
- **Returns:** `True` if allowed, otherwise `False`.

### 6.2 `get_colors(image_path)`
- **Purpose:** Extract all distinct colors from the image by quantizing to a 32‑color palette.
- **Parameters:** `image_path` – filesystem path to the uploaded image.
- **Algorithm steps:**
  1. **Open image:** Use `PIL.Image.open()` and convert to RGB mode to ensure consistent color representation.
  2. **Quantization:** `img.quantize(colors=32, method=Image.MEDIANCUT)` reduces the number of colors to 32 using the median cut algorithm. The result is a palette image (mode 'P').
  3. **Palette extraction:** `quantized.getpalette()` returns a list of 768 integers (256 colors * 3 channels). We take only the first `32*3` entries to build a list of RGB tuples for the actual palette colors.
  4. **Pixel index array:** Convert the quantized image to a numpy array (`np.array(quantized)`) and flatten it to a 1D array of palette indices.
  5. **Count frequencies:** Use `collections.Counter` to count occurrences of each index.
  6. **Build result list:** Iterate over the most common indices. For each:
     - Retrieve the RGB tuple from the palette.
     - Calculate percentage: `(count / total_pixels) * 100`, rounded to 2 decimals.
     - Convert RGB to HEX: `'#{:02x}{:02x}{:02x}'`.
     - Append a dictionary with keys `rgb`, `count`, `percentage`, `hex`.
  7. **Return** the list of color dictionaries, sorted by frequency (most common first).
- **Time complexity:** O(pixels) for counting, O(colors) for building result.

### 6.3 `index()` (route `/`)
- **Methods:** GET, POST
- **GET request:** Renders `index.html` with `colors=None` (no results).
- **POST request:**
  1. Retrieve file from `request.files`.
  2. Validate: check if file part exists, filename not empty, and extension allowed.
  3. Save the file securely using `secure_filename` to `app.config['UPLOAD_FOLDER']`.
  4. Call `get_colors(filepath)` to extract colors.
  5. If successful, render template with `colors` and `uploaded_image`.
  6. If an exception occurs (e.g., corrupted image), flash an error message and redirect to GET.
- **Security:** The app sets a maximum content length (16MB) and only allows specific image extensions. The filename is sanitized with `secure_filename`.

## 7. Frontend Features

- **Live Preview:** JavaScript reads the selected file and displays a thumbnail using `FileReader`.
- **Copy HEX to Clipboard:** When the copy button is clicked, the HEX code is written to the clipboard using the Clipboard API. A temporary checkmark icon provides feedback.
- **Simulated Progress Bar:** On form submission, a loading overlay appears with a progress bar that fills in steps (uploading, analyzing, quantizing, etc.). This is purely visual; the actual processing time depends on the backend. The progress steps are hardcoded and the bar updates every 600ms until the form is submitted.
- **Responsive Grid:** Tailwind CSS classes create a grid that adapts to different screen sizes.

## 8. Important Notes

- **Maximum Image Size:** The server limits uploads to 16MB. Larger files are rejected.
- **Color Count:** The extraction is limited to 32 distinct colors due to the quantization step. This is sufficient for most images and keeps processing fast.
- **Decompression Bomb Protection:** PIL's maximum image pixel limit is disabled (`Image.MAX_IMAGE_PIXELS = None`) to allow large images, but this may expose the server to DoS attacks. In production, consider setting a reasonable limit.
- **Truncated Images:** `LOAD_TRUNCATED_IMAGES = True` allows loading of partially corrupted images, but may lead to unexpected results.

## 9. Running in Production

For production deployment:
- Use a production WSGI server like Gunicorn.
- Set `debug=False` and use a strong `secret_key`.
- Consider using a CDN for static files.
- Implement proper error logging.

## 10. License
This project is open-source and available under the MIT License. See the LICENSE file for details.