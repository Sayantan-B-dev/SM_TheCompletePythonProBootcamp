## Uploading the Data and Reading the CSV File

This section covers the essential first step of any data analysis project: loading the dataset into a Pandas DataFrame. The dataset used throughout this analysis is `salaries_by_college_major.csv`, which contains salary information by undergraduate major. By the end of this step, you will have the data loaded and ready for exploration.

---

### 1. Obtaining the Dataset

The dataset is provided in the course resources. Download the file `salaries_by_college_major.csv` to your local machine. Ensure you know its location (e.g., `Downloads` folder) so you can upload it to your notebook environment.

---

### 2. Uploading the File to the Notebook Environment

The method depends on whether you are using **Google Colab** or a **local Jupyter Notebook**.

#### 2.1. In Google Colab

1. In your open Colab notebook, look at the left sidebar. Click the **folder icon** to open the file browser.
2. In the file browser, click the **upload icon** (a sheet of paper with an upward arrow). A file selection dialog appears.
3. Navigate to the location of `salaries_by_college_major.csv` on your computer, select it, and click **Open**.
4. The file appears in the list of files in the Colab environment, typically in the root directory (`/content/`). You should see its name, e.g., `salaries_by_college_major.csv`.

**Note:** Files uploaded this way are temporary and will be lost when the Colab runtime is disconnected. For persistent storage, you can mount Google Drive and read the file from there. However, for this exercise, the temporary upload is sufficient.

#### 2.2. In Local Jupyter Notebook

1. In the Jupyter dashboard (the file browser that opens when you launch Jupyter), navigate to the directory where you want to work.
2. Click the **Upload** button (usually an upward arrow icon) and select the CSV file from your local machine.
3. After uploading, you will see the file listed in the dashboard. It is now available in the same directory as your notebook (or the current working directory of the notebook server).

Alternatively, you can place the file manually in the notebook’s directory before starting the server.

---

### 3. Importing Pandas

Before reading the CSV, you need to import the Pandas library. It is conventional to import it with the alias `pd`.

```python
import pandas as pd
```

If you are using Google Colab, Pandas is pre‑installed. In a local environment, if you installed Anaconda, Pandas is also included. If not, you may need to install it first (`!pip install pandas` in a cell or `pip install pandas` in the terminal).

---

### 4. Reading the CSV File

Use the `pd.read_csv()` function to load the file into a DataFrame. Pass the filename as a string. If the file is in the same directory as the notebook (or the current working directory), simply use the filename.

```python
df = pd.read_csv('salaries_by_college_major.csv')
```

#### Explanation:

- `pd.read_csv()` is a versatile function that reads a comma‑separated values file and returns a DataFrame.
- By default, it assumes the first row contains column headers (which is true for this dataset).
- The DataFrame is assigned to the variable `df` (a common shorthand for DataFrame).

**Handling Different File Paths:**

If the file is in a subfolder, provide the relative path, e.g., `'data/salaries_by_college_major.csv'`. If you mounted Google Drive in Colab, the path might be something like `'/content/drive/MyDrive/salaries_by_college_major.csv'`.

---

### 5. Verifying the Load

It is good practice to immediately inspect the DataFrame to ensure it loaded correctly. The `.head()` method displays the first five rows.

```python
df.head()
```

When you execute this cell (Shift+Enter), the output appears directly below, formatted as a table.

**Expected Output:**

|     | Undergraduate Major   | Group    | Starting Median Salary | Mid-Career Median Salary | Mid-Career 10th Percentile | Mid-Career 90th Percentile |
|-----|-----------------------|----------|------------------------|--------------------------|----------------------------|----------------------------|
| 0   | Accounting            | Business | 46000                   | 77100                    | 43300                      | 124000                     |
| 1   | Aerospace Engineering | STEM     | 57200                   | 104000                   | 60400                      | 143000                     |
| 2   | Agriculture           | STEM     | 42600                   | 69100                    | 42300                      | 101000                     |
| 3   | Anthropology          | HASS     | 37300                   | 61300                    | 35600                      | 88400                      |
| 4   | Architecture          | STEM     | 42300                   | 76400                    | 40400                      | 121000                     |

**Interpretation:**  
The output shows that the DataFrame has columns corresponding to undergraduate major, group category, starting median salary, mid‑career median salary, and the 10th and 90th percentiles for mid‑career earnings. Each row represents a different major.

If you see this table, the data has been loaded successfully.

---

### 6. Using Autocompletion to Speed Up Typing

Notebook environments provide autocompletion to reduce typing errors and speed up coding.

- **In Google Colab:** After typing `df.`, press **Tab** or **Ctrl+Space** to see a list of available methods and attributes.
- **In Jupyter Notebook:** Press **Tab** after the dot to trigger autocompletion.

For example, typing `df.h` and then pressing Tab might suggest `df.head()`, `df.hist()`, etc. This feature is particularly useful when you are not sure of the exact method name or its spelling.

---

### 7. Common Issues and Troubleshooting

#### 7.1. FileNotFoundError

If you receive an error like `FileNotFoundError: [Errno 2] File salaries_by_college_major.csv does not exist`, it means Python cannot find the file in the current working directory.

**Solutions:**

- Check that the file name is spelled exactly as it is on disk (including case sensitivity on some systems).
- Verify the current working directory by running:
  ```python
  import os
  print(os.getcwd())
  ```
  Then ensure the file is located there, or provide the full/relative path.

- In Colab, after uploading, the file appears in the file browser. You can right‑click on it and select “Copy path” to get the exact path to use in `read_csv()`.

#### 7.2. UnicodeDecodeError

If the file contains special characters, you might encounter encoding errors. The default encoding is usually 'utf-8'. You can specify the encoding explicitly:

```python
df = pd.read_csv('salaries_by_college_major.csv', encoding='latin-1')
```

For this dataset, the default encoding should work without issues.

#### 7.3. No Output from .head()

If you run `df.head()` and nothing prints, ensure you are executing the cell (Shift+Enter) and that the cell contains only that line. In a Jupyter notebook, the last expression in a cell is automatically printed. If you have multiple statements, you may need to use `print(df.head())`.

---

### 8. Next Steps

With the data successfully loaded into the DataFrame `df`, you are ready to begin exploring its structure, checking for missing values, and performing initial cleaning. The subsequent sections will guide you through those processes.

---

### 9. Summary of Commands Used

| Step                     | Code                                      |
|--------------------------|-------------------------------------------|
| Import pandas            | `import pandas as pd`                     |
| Read CSV file            | `df = pd.read_csv('filename.csv')`        |
| View first 5 rows        | `df.head()`                               |
| Check current directory  | `import os; print(os.getcwd())`           |
| List files in directory  | `!ls` (in Colab) or `os.listdir('.')`     |

---

**Resource:** The dataset file `salaries_by_college_major.csv` is available in the course materials. Ensure you have downloaded it before proceeding.