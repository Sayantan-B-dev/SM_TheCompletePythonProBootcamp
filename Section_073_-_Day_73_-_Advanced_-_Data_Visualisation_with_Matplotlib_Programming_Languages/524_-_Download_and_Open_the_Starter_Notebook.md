## Setting Up the Starter Notebook and Initial Data Import

Before diving into analysis, the first practical step is to obtain the starter notebook and the dataset. The starter notebook provides a structured template with predefined sections and challenges, which helps maintain focus and ensures all necessary steps are covered. This documentation walks through downloading the notebook, preparing the environment in Google Colab, importing the data, and performing preliminary inspections to understand the dataset's structure.

### Obtaining the Starter Notebook

The starter notebook is provided as a compressed (ZIP) file in the course resources. To begin:

1. **Download the ZIP file** from the designated lesson resources.
2. **Extract its contents** to a folder on your local machine. The extracted folder contains the notebook file (with a `.ipynb` extension) and possibly other assets.
3. **Upload the notebook to Google Drive**:
   - Navigate to your Google Drive in a web browser.
   - Drag and drop the extracted notebook file into a suitable folder (e.g., a "Colab Notebooks" folder).
   - Right-click the file and select "Open with" → "Google Colaboratory". If Colab is not listed, you may need to install the Colab add-on from the Google Workspace Marketplace.
4. **Alternative**: You can also upload the notebook directly to Colab by going to [colab.research.google.com](https://colab.research.google.com) and choosing "File" → "Upload notebook".

Using Google Colab offers several advantages: no local setup required, free access to computational resources, and easy sharing. However, any code written can also be executed in a local Jupyter environment if preferred.

### Importing the Dataset

The analysis relies on a CSV file containing Stack Overflow post counts per language per month. Two options are available:

#### Option A: Use the Provided `QueryResults.csv`

The file `QueryResults.csv` is included in the same ZIP archive as the starter notebook. After unzipping, you will have this file alongside the notebook. To use it in Colab:

- In the Colab interface, click the folder icon on the left sidebar to open the file browser.
- Click the "Upload" icon and select `QueryResults.csv` from your local machine.
- The file will be uploaded to the Colab runtime's temporary storage. You can then read it using Pandas.

#### Option B: Fetch Fresh Data via StackExchange Query

For the most up-to-date information, you can run a SQL query on the StackExchange Data Explorer. The query (provided in the notebook) retrieves monthly post counts for a predefined set of programming languages. The SQL code is:

```sql
select dateadd(month, datediff(month, 0, q.CreationDate), 0) m, TagName, count(*)
from PostTags pt
join Posts q on q.Id=pt.PostId
join Tags t on t.Id=pt.TagId
where TagName in ('java','c','c++','python','c#','javascript','assembly','php','perl','ruby','visual basic','swift','r','object-c','scratch','go','swift','delphi')
and q.CreationDate < dateadd(month, datediff(month, 0, getdate()), 0)
group by dateadd(month, datediff(month, 0, q.CreationDate), 0), TagName
order by dateadd(month, datediff(month, 0, q.CreationDate), 0)
```

To execute this query:

- Visit [StackExchange Data Explorer](https://data.stackexchange.com/stackoverflow/query/new).
- Paste the query into the editor.
- Run the query (may take a few seconds).
- Export the results as a CSV file by clicking the "Export" button and selecting "CSV".
- Download the CSV and upload it to Colab as described above.

The query groups posts by the first day of each month (`dateadd(month, datediff(month, 0, q.CreationDate), 0)`) and by tag name, counting the number of posts. The `where` clause filters for a specific list of languages and ensures data only up to the current month is included.

### Reading the CSV into a Pandas DataFrame

Once the CSV file is accessible in the Colab environment, we read it using `pandas.read_csv()`. To make the data easier to work with, we assign custom column names instead of relying on the original headers. The `names` parameter accepts a list of new column names, and `header=0` tells Pandas to treat the first row of the CSV as the original header (which we then replace).

```python
import pandas as pd

df = pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)
```

This creates a DataFrame `df` with three columns:

- **DATE**: The month and year of the posts, originally formatted as a string like `2008-07-01 00:00:00`.
- **TAG**: The programming language name (e.g., 'python', 'java').
- **POSTS**: The number of posts during that month for that language.

### Preliminary Data Exploration Challenges

The starter notebook poses several challenges to familiarize yourself with the data. These steps are essential for verifying the import and understanding the dataset's dimensions and content.

#### Challenge 1: Examine the First and Last Five Rows

Use `.head()` and `.tail()` to view the beginning and end of the DataFrame. This helps confirm that the column renaming worked and gives a glimpse of the data range.

```python
df.head()
```

Expected output (first five rows):

|    | DATE                 | TAG        | POSTS |
|----|----------------------|------------|-------|
| 0  | 2008-07-01 00:00:00  | c#         | 3     |
| 1  | 2008-08-01 00:00:00  | assembly   | 8     |
| 2  | 2008-08-01 00:00:00  | javascript | 162   |
| 3  | 2008-08-01 00:00:00  | c          | 85    |
| 4  | 2008-08-01 00:00:00  | python     | 124   |

```python
df.tail()
```

Expected output (last five rows, depending on data freshness):

|      | DATE                 | TAG    | POSTS |
|------|----------------------|--------|-------|
| 1986 | 2020-07-01 00:00:00  | r      | 5694  |
| 1987 | 2020-07-01 00:00:00  | go     | 743   |
| 1988 | 2020-07-01 00:00:00  | ruby   | 775   |
| 1989 | 2020-07-01 00:00:00  | perl   | 182   |
| 1990 | 2020-07-01 00:00:00  | swift  | 3607  |

#### Challenge 2: Determine the Dimensions of the DataFrame

The `.shape` attribute returns a tuple (number of rows, number of columns). This tells us how many records we have and confirms that all three columns are present.

```python
df.shape
```

Output: `(1991, 3)` (the exact number may vary with fresh data).

#### Challenge 3: Count Non-Null Entries per Column

The `.count()` method returns the number of non-null values in each column. Since we just imported the data and there are no missing values initially, all counts should be equal to the total number of rows.

```python
df.count()
```

Output:

```
DATE     1991
TAG      1991
POSTS    1991
dtype: int64
```

This confirms that every row has valid entries in all columns. Note that missing values will appear later after reshaping, when languages with no posts in certain months are introduced.

### Summary of Initial Steps

By completing these challenges, you have successfully:

- Loaded the dataset into a Pandas DataFrame.
- Verified the data's structure and content.
- Confirmed that the data is complete (no missing values at this stage).

These preliminary checks are crucial before moving on to more complex manipulations like grouping, pivoting, and visualization. The next steps will involve converting the date strings to proper datetime objects, grouping by language to explore total posts, and reshaping the data to a wide format for easier plotting.

---

*Note: The exact code and outputs may vary slightly depending on the version of the dataset used. Always refer to the notebook's actual outputs for your specific data.*