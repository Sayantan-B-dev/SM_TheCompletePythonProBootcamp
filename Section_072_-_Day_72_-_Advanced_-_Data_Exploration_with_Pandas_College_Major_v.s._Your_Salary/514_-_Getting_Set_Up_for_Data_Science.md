## Setting Up the Development Environment for Data Science

This document provides a comprehensive guide to setting up a working environment for data science using Python notebooks. Two primary options are covered: **Google Colaboratory (Colab)** , a cloud-based solution, and **Jupyter Notebook** via the Anaconda distribution, a local installation. Both support the interactive notebook format where code, output, and explanatory text can be combined, making them ideal for exploratory data analysis.

---

### 1. Overview of Python Notebooks

A Python notebook is an interactive document divided into cells. Each cell can contain executable code or formatted text (Markdown). When a code cell is executed, the result (output, printed text, or visualizations) appears directly below the cell. This iterative workflow allows for step‑by‑step exploration and documentation of the analysis process.

The notebook format is widely used in data science because it:
- Encourages experimentation and rapid prototyping.
- Preserves the analysis narrative alongside code and results.
- Simplifies sharing and reproducibility.

---

### 2. Google Colab (Cloud‑Based)

Google Colab is a free, cloud‑based service that requires no installation. It provides a Jupyter notebook environment hosted on Google servers, with access to a runtime that includes common data science libraries (e.g., pandas, numpy, matplotlib) pre‑installed.

#### 2.1. Accessing Google Colab

1. Open your web browser and go to [Google Drive](https://drive.google.com).
2. Sign in with your Google account.
3. Click the **New** button (usually on the left side) and select **More** → **Google Colaboratory**.  
   - If **Google Colaboratory** is not listed, click **Connect more apps**, search for “Colaboratory”, and install it. After installation, it will appear in the **More** menu.

Alternatively, you can directly navigate to [colab.research.google.com](https://colab.research.google.com) and create a new notebook from there.

#### 2.2. Creating and Renaming a Notebook

- After clicking **Google Colaboratory**, a new untitled notebook opens in a new browser tab.
- By default, the notebook is named “Untitled0.ipynb”. Click on the notebook name at the top left to rename it (e.g., “Salary_Analysis.ipynb”).
- The notebook is automatically saved in your Google Drive in a folder called “Colab Notebooks”.

#### 2.3. Connecting to a Runtime

Before executing any code, the notebook must connect to a runtime (a virtual machine with CPU/GPU). This happens automatically when you run the first cell, but you can also manually connect via the **Runtime** menu:

- Click **Runtime** → **Run all** or **Connect to hosted runtime**.
- A green checkmark and “Connected” appear in the top right when the runtime is ready.

Google Colab offers free access to a limited set of resources. For most educational datasets, this is sufficient. You can also upgrade to a paid plan for more powerful hardware.

#### 2.4. Uploading Data Files

Data files (e.g., CSV) can be uploaded to the Colab environment:

1. Click the folder icon on the left sidebar to open the file browser.
2. Click the **Upload** icon (a sheet of paper with an upward arrow) and select the file from your local machine.
3. The file appears in the current working directory and can be accessed by its name in code.

**Note:** Uploaded files are temporary and will be lost when the runtime is disconnected. To keep files permanently, store them in Google Drive and mount the drive within the notebook using:

```python
from google.colab import drive
drive.mount('/content/drive')
```

After mounting, you can access files from your Drive using paths like `/content/drive/MyDrive/filename.csv`.

#### 2.5. Installing Additional Libraries

Most common data science libraries are already installed. If you need a library not present, you can install it using `!pip install` directly in a code cell:

```python
!pip install seaborn
```

The exclamation mark tells Colab to run the command as a shell command.

---

### 3. Local Jupyter Notebook with Anaconda

For users who prefer a local environment or need to work offline, installing Anaconda is the recommended approach. Anaconda is a distribution that includes Python, the Jupyter Notebook server, and hundreds of scientific packages.

#### 3.1. Downloading and Installing Anaconda

1. Go to the official Anaconda download page: [https://www.anaconda.com/products/individual](https://www.anaconda.com/products/individual)
2. Choose the installer for your operating system (Windows, macOS, Linux).
3. Run the installer and follow the on‑screen instructions. Accept the default settings unless you have specific preferences.
   - On Windows, you may be asked whether to add Anaconda to your PATH environment variable. The default recommendation is usually sufficient.

#### 3.2. Launching Jupyter Notebook

After installation, you can start the Jupyter Notebook server in several ways:

- **Using Anaconda Navigator:**  
  Open Anaconda Navigator (installed with Anaconda) and click the **Launch** button under the Jupyter Notebook tile. This opens a new tab in your default web browser showing the notebook dashboard.

- **Using the Command Line:**  
  Open a terminal (or Anaconda Prompt on Windows) and type:
  ```bash
  jupyter notebook
  ```
  The server starts and the dashboard opens in your browser.

#### 3.3. Creating a New Notebook

In the Jupyter dashboard, navigate to the folder where you want to store your notebooks. Click the **New** button on the right and select **Python 3** (or your preferred kernel). A new notebook opens in a browser tab.

#### 3.4. Uploading Data Files

To use a data file locally, simply place it in the same directory as your notebook (or any subdirectory). You can then reference it by its relative path, e.g., `'data/salaries.csv'`. The Jupyter dashboard also allows you to upload files via the **Upload** button.

---

### 4. Working with a Python Notebook

Whether using Colab or local Jupyter, the notebook interface is similar.

#### 4.1. Cells and Execution

- A notebook consists of a sequence of cells.
- Cells can be of type **Code** (for Python code) or **Markdown** (for formatted text, headings, images, etc.).
- To execute a code cell, select it and press **Shift+Enter**. The code runs, and any output (printed text, tables, plots) appears directly below the cell. A new cell is automatically created below.
- To execute a cell and stay on the same cell (without creating a new one), use **Ctrl+Enter**.
- To run all cells in order, use the **Run** menu or the double‑play button in the toolbar.

#### 4.2. Markdown Cells

Markdown cells allow you to write rich text using Markdown syntax. Common elements include:

- Headings: `# Heading 1`, `## Heading 2`, etc.
- Bold: `**bold text**`
- Italic: `*italic text*`
- Lists: `- item` for bullet lists, `1. item` for numbered lists.
- Code inline: `code` with backticks.
- Code blocks: triple backticks with optional language name.
- Links: `[text](url)`
- Images: `![alt text](image_path)`

To convert a cell to Markdown, select the cell and choose **Markdown** from the dropdown menu in the toolbar (or press **Esc** then **m**). To render the Markdown, execute the cell (Shift+Enter).

#### 4.3. Keyboard Shortcuts

Familiarity with keyboard shortcuts speeds up notebook navigation:

- **Shift+Enter**: Run cell and move to next cell.
- **Ctrl+Enter**: Run cell and stay.
- **Alt+Enter**: Run cell and insert a new cell below.
- **Esc**: Enter command mode (navigation mode).
- **Enter**: Enter edit mode (for typing in a cell).
- **A**: Insert cell above current cell (command mode).
- **B**: Insert cell below.
- **DD** (press D twice): Delete current cell.
- **Z**: Undo cell deletion.
- **M**: Change cell to Markdown (command mode).
- **Y**: Change cell to Code (command mode).

For a full list, go to **Help** → **Keyboard Shortcuts** in the notebook menu.

#### 4.4. Saving and Exporting

- Notebooks are automatically saved periodically. You can also manually save with **Ctrl+S** (or **Cmd+S** on Mac).
- To download a notebook as a `.ipynb` file, go to **File** → **Download** → **Download .ipynb**.
- In Colab, you can also save a copy to GitHub or Google Drive.

#### 4.5. Example: First Code Cell

To verify that everything is working, enter the following code in a code cell and execute it:

```python
import pandas as pd
print("Hello, data science world!")
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df.head()
```

**Expected Output:**

```
Hello, data science world!
   A  B
0  1  4
1  2  5
2  3  6
```

This confirms that pandas is imported correctly and that the dataframe displays nicely.

---

### 5. Additional Tips and Troubleshooting

#### 5.1. Autocompletion

Both Colab and Jupyter support tab‑based autocompletion. Start typing a variable or function name and press **Tab** to see suggestions. In Colab, you can also press **Ctrl+Space** to trigger autocompletion.

#### 5.2. Documentation Lookup

To view the documentation of a function or method, place the cursor inside the parentheses and press **Shift+Tab**. A popup shows the signature and docstring.

#### 5.3. Handling Kernel Crashes or Disconnections

- In Colab, if the runtime disconnects (e.g., after 90 minutes of inactivity), you may lose unsaved data and variables. Save your notebook frequently and consider using Google Drive mounting for persistent data storage.
- In local Jupyter, if the kernel dies, you can restart it via the **Kernel** menu. Variables will be lost, so re‑run necessary cells.

#### 5.4. Installing Additional Packages Locally

In a local environment, you can install packages using `!pip install` as well, but it’s more common to use the terminal or Anaconda Prompt. For example:

```bash
pip install seaborn
```

Alternatively, use `conda install seaborn` if you prefer conda.

#### 5.5. Sharing Notebooks

- **Colab:** You can share the notebook link with others (they need a Google account to edit). Set permissions to “Viewer” or “Commenter” as needed.
- **Local Jupyter:** You can export the notebook as HTML or PDF for sharing, or upload the `.ipynb` file to a repository like GitHub. GitHub renders notebooks natively.

---

### 6. Summary

Both Google Colab and local Jupyter Notebook provide excellent environments for data analysis with Python. Colab offers convenience and zero setup, while a local installation gives you full control and offline access. The choice depends on your specific needs and preferences.

Now that the environment is ready, you can proceed to load the dataset and begin exploring it with pandas, as described in the subsequent sections.