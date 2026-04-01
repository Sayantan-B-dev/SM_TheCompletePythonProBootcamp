## Detailed Line-by-Line Breakdown of the Watermarking Application

This document provides an exhaustive explanation of every line of code in the provided Python script. The script creates a desktop GUI application using `tkinter` and `Pillow` (PIL) that allows users to add text and/or logo watermarks to images. The explanation covers the purpose, functionality, and underlying concepts of each part.

---

### 1. Import Statements

```python
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, font
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
```

- **`import tkinter as tk`**: Imports the main Tkinter module and gives it the alias `tk`. Tkinter is Python's standard GUI library; it provides tools to create windows, widgets, and handle events. Using `tk` as a prefix (e.g., `tk.Tk()`, `tk.Button`) keeps the code concise and avoids naming conflicts.

- **`from tkinter import filedialog, messagebox, colorchooser, font`**: Imports specific submodules from `tkinter`:
  - `filedialog`: Provides dialogs for opening and saving files (`askopenfilename`, `asksaveasfilename`).
  - `messagebox`: Displays message boxes for information, warnings, errors (`showinfo`, `showwarning`, `showerror`).
  - `colorchooser`: Opens a color selection dialog (`askcolor`).
  - `font`: Although imported, it's not explicitly used in this script; it might be intended for font selection but remains unused (the script uses `PIL.ImageFont` instead). This import is redundant but harmless.

- **`from PIL import Image, ImageTk, ImageDraw, ImageFont`**: Imports essential classes from the Python Imaging Library (Pillow):
  - `Image`: The core class for opening, manipulating, and saving images.
  - `ImageTk`: Provides a bridge to convert PIL images into Tkinter-compatible photo images that can be displayed in Tkinter widgets (like `Label` or `Canvas`).
  - `ImageDraw`: Allows drawing on images (text, shapes) by creating a drawing context.
  - `ImageFont`: Handles font loading and text rendering on images.

- **`import os`**: Imports Python's operating system interface module. It's used here for extracting the base filename from a full path (e.g., `os.path.basename(file_path)`) to display in the status bar.

---

### 2. Class Definition: `WatermarkApp`

```python
class WatermarkApp:
```

Defines a new class named `WatermarkApp`. This class encapsulates all the data and behavior of the watermarking application. Using a class makes the code organized, reusable, and easier to manage.

---

### 3. `__init__` Method: Constructor

```python
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark Your Images")
        self.root.geometry("800x600")
```

- `def __init__(self, root):` The constructor method is called automatically when a new instance of `WatermarkApp` is created. It takes `root` as an argument, which is the main Tkinter window (an instance of `tk.Tk()`).
- `self.root = root`: Stores the root window as an instance variable so other methods can access it.
- `self.root.title("Watermark Your Images")`: Sets the title of the main window.
- `self.root.geometry("800x600")`: Sets the initial size of the window to 800 pixels wide and 600 pixels tall.

```python
        # Variables to store images and paths
        self.main_image = None          # PIL Image object (original)
        self.main_image_tk = None       # ImageTk for display
        self.logo_image = None           # PIL Image object (logo)
        self.watermarked_image = None    # PIL Image after watermarking
        self.current_preview = None       # ImageTk for preview
```

These are instance variables initialized to `None`. They will hold the actual image data:
- `main_image`: The original loaded main image as a PIL `Image` object.
- `main_image_tk`: A Tkinter-compatible photo image of the main image (used for display on the canvas). This variable is necessary to prevent the image from being garbage-collected by Tkinter.
- `logo_image`: The loaded logo image as a PIL `Image` object.
- `watermarked_image`: The final image after applying the watermark(s), stored as a PIL `Image`.
- `current_preview`: The Tkinter photo image currently displayed on the canvas (the preview after watermarking or loading).

```python
        self.watermark_pos = (0.8, 0.9)  # default relative position (bottom-right)
```

Defines the default position of the watermark. It's a tuple of two floats representing relative coordinates from the top-left corner: (0.8, 0.9) means 80% from the left and 90% from the top, which places the watermark near the bottom-right corner. This can later be changed by user click (absolute coordinates) or remain relative.

```python
        self.watermark_text = tk.StringVar()
        self.watermark_text.set("© YourWebsite.com")
```

`tk.StringVar()` is a Tkinter variable class that holds a string and can be linked to widgets (like `Entry`) for automatic updates. Here, it holds the watermark text, initially set to "© YourWebsite.com". Using a `StringVar` allows easy retrieval and modification of the entry content.

```python
        # Watermark type: "text", "logo", or "both"
        self.watermark_type = tk.StringVar(value="text")
```

Another `StringVar` to store the selected watermark type. It is initialized with `value="text"`, meaning the default selection is text-only. This variable will be linked to radio buttons.

```python
        # Font settings
        self.font_path = None
        self.font_size = 36
        self.font_color = (255, 255, 255, 128)  # white with 50% opacity
```

- `font_path`: Stores the path to a TrueType font file selected by the user. If `None`, the default PIL font will be used.
- `font_size`: An integer for the font size (in points). Default is 36.
- `font_color`: A tuple representing RGBA color. Here, (255,255,255,128) is white with 128/255 ≈ 50% opacity. This allows the text to be semi-transparent.

```python
        # Build UI
        self.create_widgets()
```

Calls the method `create_widgets` which constructs all the GUI elements.

---

### 4. `create_widgets` Method: Building the Interface

```python
    def create_widgets(self):
        # Control frame
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
```

- Creates a `Frame` widget as a child of the main window. Frames are used to group related widgets.
- `pack()` is a geometry manager that places the frame at the top (`side=tk.TOP`), fills the horizontal space (`fill=tk.X`), and adds padding of 10 pixels horizontally and 5 pixels vertically around the frame.

```python
        # Buttons for loading images
        tk.Button(control_frame, text="Load Main Image", command=self.load_main_image).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Load Logo", command=self.load_logo).pack(side=tk.LEFT, padx=5)
```

- Creates two buttons inside `control_frame`.
- `text` sets the label on the button.
- `command` specifies the function to call when the button is clicked (`self.load_main_image` and `self.load_logo`).
- `pack(side=tk.LEFT, padx=5)` places them left-to-right with 5 pixels horizontal padding.

```python
        # Watermark text entry
        tk.Label(control_frame, text="Watermark Text:").pack(side=tk.LEFT, padx=5)
        tk.Entry(control_frame, textvariable=self.watermark_text, width=30).pack(side=tk.LEFT, padx=5)
```

- A `Label` with descriptive text.
- An `Entry` widget where the user can type the watermark text. The `textvariable` option links it to `self.watermark_text`, so changes in the entry automatically update the `StringVar` and vice versa. Width is set to 30 characters.

```python
        # Watermark type selection
        tk.Radiobutton(control_frame, text="Text", variable=self.watermark_type, value="text").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Logo", variable=self.watermark_type, value="logo").pack(side=tk.LEFT)
        tk.Radiobutton(control_frame, text="Both", variable=self.watermark_type, value="both").pack(side=tk.LEFT)
```

Three radio buttons, all sharing the same `variable=self.watermark_type`. When a radio button is selected, the variable is set to the corresponding `value` ("text", "logo", or "both"). Only one can be selected at a time.

```python
        # Buttons for actions
        tk.Button(control_frame, text="Add Watermark", command=self.add_watermark).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Save Image", command=self.save_image).pack(side=tk.LEFT, padx=5)
```

Two more buttons: one triggers watermark addition, the other saves the result.

```python
        # Font customization (optional)
        tk.Button(control_frame, text="Choose Font", command=self.choose_font).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="Font Color", command=self.choose_color).pack(side=tk.LEFT, padx=5)
```

Buttons to customize font: choose a font file and choose a color.

```python
        # Canvas for image preview
        self.canvas = tk.Canvas(self.root, bg='gray')
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.set_watermark_position)
```

- Creates a `Canvas` widget where images will be displayed. The background is set to gray.
- `pack(fill=tk.BOTH, expand=True)` makes the canvas expand to fill any remaining space in the window (both horizontally and vertically) and resizes with the window.
- `bind("<Button-1>", self.set_watermark_position)` binds the left mouse button click event to the `set_watermark_position` method. When the user clicks on the canvas, that method is called with an event object containing click coordinates.

```python
        # Status bar
        self.status = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
```

- A `Label` at the bottom to display status messages. `bd=1` gives a border width of 1 pixel, `relief=tk.SUNKEN` makes it appear sunken (like a status bar), and `anchor=tk.W` aligns text to the west (left).
- `pack(side=tk.BOTTOM, fill=tk.X)` places it at the bottom, filling the horizontal space.

---

### 5. `load_main_image` Method

```python
    def load_main_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Main Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
```

- Opens a file open dialog using `filedialog.askopenfilename`. The dialog title is set, and only files with the specified extensions are shown (though the user can select "All files" if they wish). Returns the selected file path as a string, or an empty string if cancelled.

```python
        if file_path:
            try:
                self.main_image = Image.open(file_path).convert("RGBA")
                self.show_image_on_canvas(self.main_image)
                self.status.config(text=f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")
```

- If a file was selected (`if file_path:`), attempt to open it with `Image.open()`. The image is then converted to RGBA mode using `.convert("RGBA")` to ensure it has an alpha channel (transparency) for consistent handling. This is important because later operations (drawing, compositing) assume RGBA.
- Calls `self.show_image_on_canvas` to display the loaded image on the canvas.
- Updates the status bar with the filename (using `os.path.basename` to extract just the name).
- If any exception occurs (e.g., file not an image, corrupted), an error message box is shown with the exception details.

---

### 6. `load_logo` Method

```python
    def load_logo(self):
        file_path = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            try:
                self.logo_image = Image.open(file_path).convert("RGBA")
                self.status.config(text=f"Logo loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open logo: {e}")
```

Analogous to `load_main_image`, but stores the logo in `self.logo_image` and does not display it on the canvas (only updates status). Again converts to RGBA for transparency handling.

---

### 7. `show_image_on_canvas` Method

```python
    def show_image_on_canvas(self, pil_image):
        """Resize image to fit canvas and display it."""
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width <= 1:  # canvas not yet realized
            canvas_width, canvas_height = 700, 400
```

- Retrieves the current width and height of the canvas widget using `winfo_width()` and `winfo_height()`. These values might be 1 if the canvas hasn't been fully drawn yet (e.g., immediately after startup). In that case, fallback dimensions (700x400) are used as a reasonable default.

```python
        # Maintain aspect ratio
        pil_image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
        self.current_preview = ImageTk.PhotoImage(pil_image)
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.current_preview, anchor=tk.CENTER)
```

- `pil_image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)`: Resizes the image **in place** to fit within the given bounding box while preserving aspect ratio. `LANCZOS` is a high-quality resampling filter. Note: `thumbnail` modifies the image object; if we need the original later, we should work on a copy (but here we only display a thumbnail for preview; the original `self.main_image` remains untouched).
- `self.current_preview = ImageTk.PhotoImage(pil_image)`: Converts the PIL image to a Tkinter-compatible photo image. Storing it as an instance variable prevents garbage collection.
- `self.canvas.delete("all")`: Clears any existing drawings on the canvas.
- `self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.current_preview, anchor=tk.CENTER)`: Places the image at the center of the canvas. The `anchor=tk.CENTER` means the image's center is positioned at the given coordinates.

---

### 8. `set_watermark_position` Method

```python
    def set_watermark_position(self, event):
        """Capture click position on canvas for watermark placement."""
        if self.current_preview and self.main_image:
```

- This method is called when the user clicks on the canvas. It checks that there is a preview image and a main image loaded (otherwise, clicking is meaningless).

```python
            # Convert canvas coordinates to image coordinates
            canvas_bbox = self.canvas.bbox("all")
            if canvas_bbox:
                img_x, img_y = event.x - canvas_bbox[0], event.y - canvas_bbox[1]
```

- `self.canvas.bbox("all")` returns the bounding box of all items on the canvas as a tuple (x1, y1, x2, y2). Since the image is the only item (after `delete("all")` and `create_image`), this gives the area occupied by the image. This is necessary because the image might not fill the entire canvas; it's centered.
- The click coordinates `event.x` and `event.y` are relative to the canvas's top-left corner. By subtracting the top-left of the image bounding box (`canvas_bbox[0]`, `canvas_bbox[1]`), we get coordinates relative to the image's top-left corner (`img_x`, `img_y`).

```python
                # Map to original image size
                orig_w, orig_h = self.main_image.size
                disp_w, disp_h = self.current_preview.width(), self.current_preview.height()
                if disp_w > 0 and disp_h > 0:
                    x = int(img_x * orig_w / disp_w)
                    y = int(img_y * orig_h / disp_h)
                    self.watermark_pos = (x, y)
                    self.status.config(text=f"Watermark position set to ({x}, {y})")
```

- Retrieve original image dimensions (`orig_w`, `orig_h`) and displayed thumbnail dimensions (`disp_w`, `disp_h`).
- Scale the click coordinates proportionally to the original image: `x = img_x * (orig_w / disp_w)`, `y = img_y * (orig_h / disp_h)`. The result is the position in the original image where the watermark should be placed (top-left corner of the watermark? The code currently uses these as the top-left coordinates for text/logo; see later methods).
- Update `self.watermark_pos` with the absolute coordinates (integers) and display in status bar.

---

### 9. `choose_font` Method

```python
    def choose_font(self):
        file_path = filedialog.askopenfilename(
            title="Select TrueType Font",
            filetypes=[("Font files", "*.ttf *.otf")]
        )
        if file_path:
            self.font_path = file_path
            self.status.config(text=f"Font selected: {os.path.basename(file_path)}")
```

Opens a file dialog to select a TrueType or OpenType font file. If selected, stores the path in `self.font_path` and updates status.

---

### 10. `choose_color` Method

```python
    def choose_color(self):
        color = colorchooser.askcolor(title="Choose font color", color='white')
        if color[0]:
            # color[0] is RGB tuple, add alpha (e.g., 255 for opaque)
            self.font_color = (int(color[0][0]), int(color[0][1]), int(color[0][2]), 255)
            self.status.config(text=f"Font color set")
```

- Opens a color chooser dialog, with initial color set to white. The `askcolor` function returns a tuple `(RGB_tuple, hex_string)`. If the user cancels, it returns `(None, None)`.
- If a color was chosen (`if color[0]:`), we take the RGB tuple and add an alpha value of 255 (fully opaque) to create an RGBA tuple. The default was semi-transparent white (128 alpha), but here we set to opaque. (Note: The initial default had 50% opacity; after choosing color, opacity becomes 100%. The code doesn't provide an opacity slider, but could be enhanced.)

---

### 11. `add_watermark` Method

```python
    def add_watermark(self):
        if not self.main_image:
            messagebox.showwarning("No Image", "Please load a main image first.")
            return
```

Checks if a main image is loaded; if not, shows a warning and exits the method.

```python
        # Work on a copy of the main image
        img = self.main_image.copy()
        draw_type = self.watermark_type.get()
```

- Creates a copy of the main image so that the original remains unchanged. All watermarking operations are performed on this copy.
- Retrieves the selected watermark type from the `StringVar` using `.get()`.

```python
        # Add logo if selected
        if draw_type in ("logo", "both") and self.logo_image:
            img = self.add_logo_watermark(img)
```

If the type includes logo and a logo image is loaded, call `add_logo_watermark` on the image copy. Note: `add_logo_watermark` returns the modified image (which may be a new image or the same). Assigning back to `img` ensures we keep the updated version.

```python
        # Add text if selected
        if draw_type in ("text", "both") and self.watermark_text.get().strip():
            img = self.add_text_watermark(img)
```

Similarly, if text is included and the watermark text is not empty after stripping whitespace, call `add_text_watermark` and update `img`.

```python
        # Update preview and store watermarked image
        self.watermarked_image = img
        self.show_image_on_canvas(img)
        self.status.config(text="Watermark applied. You can save the image now.")
```

- Store the final watermarked image in `self.watermarked_image`.
- Display it on the canvas using `show_image_on_canvas`.
- Update status.

---

### 12. `add_text_watermark` Method

```python
    def add_text_watermark(self, img):
        """Draw text onto the image at self.watermark_pos."""
        draw = ImageDraw.Draw(img, "RGBA")
        text = self.watermark_text.get().strip()
```

- `ImageDraw.Draw(img, "RGBA")` creates a drawing context for the image, with mode RGBA to support transparency.
- Retrieves the watermark text and strips whitespace.

```python
        # Try to load font, fallback to default
        try:
            if self.font_path:
                font = ImageFont.truetype(self.font_path, self.font_size)
            else:
                # Use default font; size can be approximated
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
```

Attempts to load a TrueType font from the specified path with the given size. If that fails (e.g., file not found, invalid font), falls back to PIL's default bitmap font. The default font does not scale well and has a fixed size, but it's better than crashing.

```python
        # Use textbbox to get text size (new in Pillow 8.0.0)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
```

- `draw.textbbox((0,0), text, font=font)` returns the bounding box of the text if placed at (0,0). It returns `(left, top, right, bottom)` coordinates relative to the anchor point. Subtracting gives the width and height of the rendered text. This is necessary for positioning the text correctly.

```python
        # Determine position (absolute or relative)
        if isinstance(self.watermark_pos[0], float):
            # relative coordinates (0-1)
            x = int((img.width - text_width) * self.watermark_pos[0])
            y = int((img.height - text_height) * self.watermark_pos[1])
        else:
            # absolute coordinates from click
            x, y = self.watermark_pos
            # For simplicity, we'll use the click as top-left corner.
```

- Checks whether the first element of `self.watermark_pos` is a float. If it is, the position is interpreted as relative coordinates (0.0 to 1.0) and converted to absolute pixel coordinates such that the text's top-left corner is placed proportionally within the remaining space. For example, if `watermark_pos = (0.8, 0.9)`, then `x = (img.width - text_width) * 0.8`, meaning 80% from the left edge of the available area (so the text will be near the right edge).
- If the first element is not a float (i.e., integer), then it's the absolute coordinates from a previous mouse click, and those are used directly as the top-left corner.

```python
        # Draw the text
        draw.text((x, y), text, font=font, fill=self.font_color)
        return img
```

- `draw.text()` renders the text at (x, y) using the specified font and color.
- Returns the modified image.

---

### 13. `add_logo_watermark` Method

```python
    def add_logo_watermark(self, img):
        """Overlay logo image with transparency."""
        if not self.logo_image:
            return img
```

If no logo is loaded, return the original image unchanged.

```python
        # Resize logo to be a reasonable size (e.g., 20% of main image width)
        base_width = int(img.width * 0.2)
        w_percent = base_width / float(self.logo_image.width)
        new_height = int(self.logo_image.height * w_percent)
        logo_resized = self.logo_image.resize((base_width, new_height), Image.Resampling.LANCZOS)
```

- Sets the logo width to 20% of the main image's width (as an integer). Then computes the scaling factor and resizes the logo proportionally using high-quality `LANCZOS` resampling. This ensures the logo is not too large.

```python
        # Determine position
        if isinstance(self.watermark_pos[0], float):
            # relative
            x = int((img.width - logo_resized.width) * self.watermark_pos[0])
            y = int((img.height - logo_resized.height) * self.watermark_pos[1])
        else:
            x, y = self.watermark_pos
```

Same coordinate logic as for text: if relative floats, compute absolute pixel coordinates so that the logo's top-left corner is placed accordingly; if absolute integers, use them directly.

```python
        # Paste using alpha channel as mask if available
        if logo_resized.mode == 'RGBA':
            # Create a transparent layer the size of the main image
            transparent = Image.new('RGBA', img.size, (0,0,0,0))
            transparent.paste(logo_resized, (x, y), logo_resized)
            img = Image.alpha_composite(img, transparent)
        else:
            # If logo has no alpha, just paste (may lose transparency)
            img.paste(logo_resized, (x, y))
```

- **If the logo has an alpha channel (RGBA)**, we perform alpha compositing to preserve transparency:
  1. Create a new fully transparent image (`transparent`) of the same size as the main image.
  2. Paste the resized logo onto this transparent image using the logo itself as the mask (the third argument). This ensures that the logo's transparency is maintained.
  3. Use `Image.alpha_composite(img, transparent)` to composite the transparent layer onto the main image. This blends the two images using their alpha channels correctly.
- **If the logo does not have an alpha channel** (e.g., a JPG), we simply paste it directly. This will overwrite pixels in the main image without transparency blending, which may look harsh but is a simple fallback.

```python
        return img
```

Returns the modified image.

---

### 14. `save_image` Method

```python
    def save_image(self):
        if not self.watermarked_image:
            messagebox.showwarning("No Watermarked Image", "Please add a watermark first.")
            return
```

Checks if there is a watermarked image to save; if not, shows a warning.

```python
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
```

Opens a **save as** dialog. The `defaultextension=".png"` means if the user doesn't type an extension, `.png` will be appended. The `filetypes` list filters the displayed file types.

```python
        if file_path:
            try:
                # Convert to RGB if saving as JPEG
                if file_path.lower().endswith(('.jpg', '.jpeg')):
                    self.watermarked_image.convert("RGB").save(file_path)
                else:
                    self.watermarked_image.save(file_path)
                self.status.config(text=f"Saved to: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Image saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image: {e}")
```

- If a file path was provided (user didn't cancel), proceed to save.
- JPEG format does not support alpha channels. If the chosen filename ends with `.jpg` or `.jpeg`, convert the image to RGB (dropping alpha) before saving. For other formats (like PNG), save as is (preserving transparency).
- Update status bar and show a success message.
- Catch any exceptions (e.g., permission denied, disk full) and show an error.

---

### 15. Main Execution Block

```python
if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()
```

- `if __name__ == "__main__":` ensures the code runs only when the script is executed directly, not when imported as a module.
- `root = tk.Tk()` creates the main Tkinter window (the root widget). This is the starting point of any Tkinter application.
- `app = WatermarkApp(root)` instantiates our application class, passing the root window. This triggers `__init__` and builds the GUI.
- `root.mainloop()` starts the Tkinter event loop, which waits for user interactions (clicks, key presses) and updates the GUI accordingly. The program remains in this loop until the window is closed.

---

## Overall Workflow Summary

1. **User launches the program** → Main window appears with control buttons and a gray canvas.
2. **User loads a main image** → Image is displayed (scaled to fit) on the canvas. The original image is stored in memory.
3. **User optionally loads a logo** → Logo is stored; no immediate visual change.
4. **User optionally enters watermark text** → Default text is present; can be changed.
5. **User selects watermark type** (Text, Logo, or Both) via radio buttons.
6. **User may customize font** by choosing a font file and/or font color.
7. **User may click on the canvas** to set a custom watermark position. The coordinates are mapped to the original image and stored.
8. **User clicks "Add Watermark"** → The program creates a copy of the main image, applies the selected watermark(s) using the current settings, displays the result on the canvas, and stores it.
9. **User clicks "Save Image"** → Opens a save dialog; the watermarked image is saved in the chosen format (PNG preserves transparency, JPEG discards it).
10. Throughout, the status bar provides feedback, and error/warning dialogs appear for issues.

---

## Key Concepts Explained

- **Tkinter Variables (`StringVar`)**: Used to hold widget values and automatically synchronize between the GUI and code. This simplifies retrieving and updating entry text and radio button selections.
- **Canvas and Image Display**: The canvas is used because it can display images and also capture mouse clicks. The image must be converted to `ImageTk.PhotoImage` and stored as an instance variable to avoid garbage collection.
- **Coordinate Mapping**: Since the displayed image is a scaled thumbnail, mouse clicks are transformed to original image coordinates using the ratio of dimensions. This ensures the watermark is placed correctly on the full-resolution image.
- **Image Modes and Alpha Compositing**: Converting images to RGBA ensures consistent handling of transparency. `Image.alpha_composite` correctly blends two RGBA images, preserving anti-aliasing and partial transparency.
- **Error Handling**: `try-except` blocks around file operations prevent crashes and inform the user via message boxes.

## Potential Improvements (Based on Reflection)

- **Opacity control**: Add a slider for text/logo opacity.
- **Better positioning UI**: Use spinboxes for precise X/Y or allow dragging the watermark.
- **Live preview**: Update the watermark as settings change (without needing to click "Add Watermark").
- **Undo/redo functionality**.
- **Batch processing**.
- **More font options**: Size, style, alignment.
- **Separate GUI from logic** for easier testing and maintenance.

This detailed breakdown should provide a comprehensive understanding of every line of code and how they work together to create a functional watermarking application.