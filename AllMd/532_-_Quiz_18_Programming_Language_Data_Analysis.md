## Quiz 18: Programming Language Data Analysis

This quiz tests your understanding of the concepts covered in the Stack Overflow programming language popularity analysis project. Questions span data loading, cleaning, manipulation with Pandas, and visualization with Matplotlib. Each question includes the correct answer and a detailed explanation.

---

### Question 1

What is the purpose of the `header=0` parameter in `pd.read_csv('QueryResults.csv', names=['DATE', 'TAG', 'POSTS'], header=0)`?

A. It tells Pandas to skip the first 0 rows.  
B. It indicates that the first row of the CSV contains the column names that we want to replace.  
C. It sets the first column as the index.  
D. It ensures that missing values are filled with 0.

**Answer:** B  
**Explanation:** The `header=0` parameter means that the first row of the CSV file (row 0) is currently the header row. By providing `names`, we override that header with our own column names. Without `header=0`, Pandas might treat the first row as data.

---

### Question 2

After loading the DataFrame, you want to check its dimensions. Which attribute or method do you use?

A. `df.size`  
B. `df.shape`  
C. `df.len()`  
D. `df.count()`

**Answer:** B  
**Explanation:** `df.shape` returns a tuple (number of rows, number of columns). `df.size` returns the total number of elements (rows * columns). `df.count()` returns the number of non-null entries per column, not the dimensions.

---

### Question 3

You run `df.groupby('TAG').sum()`. What does the result's index represent?

A. The dates of each post.  
B. The programming language names.  
C. The total number of posts per language.  
D. The number of months each language has been active.

**Answer:** B  
**Explanation:** After grouping by 'TAG', the unique values in the 'TAG' column become the index of the resulting DataFrame. The `sum()` then aggregates the 'POSTS' column for each group, giving total posts per language.

---

### Question 4

How can you count the number of months for which each programming language has at least one post?

A. `df.groupby('TAG').sum()`  
B. `df.groupby('TAG').count()`  
C. `df.groupby('DATE').count()`  
D. `df.groupby('TAG').size()`

**Answer:** B  
**Explanation:** `df.groupby('TAG').count()` returns the number of non-null entries in each column for each language. Since there are no nulls initially, this counts the rows per language, i.e., the number of months each language appears in the dataset.

---

### Question 5

Why do we convert the 'DATE' column to datetime using `pd.to_datetime()`?

A. To remove the time portion (00:00:00).  
B. To enable time-based operations like resampling and proper axis formatting in plots.  
C. To sort the dates alphabetically.  
D. To fill missing dates with the current date.

**Answer:** B  
**Explanation:** Converting to datetime objects allows Pandas and Matplotlib to treat the column as actual dates. This enables time-series operations (e.g., `.resample`), date arithmetic, and correct spacing on plot axes. Removing the time portion is a side effect, not the main purpose.

---

### Question 6

What does the `pivot()` method do in Pandas?

A. It aggregates data by applying a function.  
B. It reshapes data from long format to wide format by specifying index, columns, and values.  
C. It transposes the DataFrame.  
D. It merges two DataFrames on a common column.

**Answer:** B  
**Explanation:** `pivot()` is used to reshape data. You provide an index (rows), columns (new column names), and values (cell contents). It transforms the data so that each combination of index and column becomes a single cell.

---

### Question 7

After pivoting our DataFrame, we get many `NaN` values. Why?

A. Because the original data had missing posts for some months.  
B. Because `pivot()` automatically inserts `NaN` for missing combinations of index and column.  
C. Because we forgot to fill missing values before pivoting.  
D. Both A and B.

**Answer:** D  
**Explanation:** The original data only contains rows for months where a language had at least one post. After pivoting, every date–language combination that does not exist in the original data becomes `NaN`. This includes months before a language existed (e.g., Swift in 2008) and months where a language had zero posts (which were not recorded). So both A and B are correct.

---

### Question 8

How do we replace all `NaN` values in a DataFrame `reshaped_df` with 0, modifying the original DataFrame?

A. `reshaped_df.replace(NaN, 0, inplace=True)`  
B. `reshaped_df.fillna(0, inplace=True)`  
C. `reshaped_df = reshaped_df.fillna(0)`  
D. Both B and C are correct, but B modifies the original.

**Answer:** D  
**Explanation:** `fillna(0)` returns a new DataFrame with `NaN` replaced by 0. Using `inplace=True` modifies the existing DataFrame. Both approaches are valid; B modifies the original, while C reassigns. The question asks for modifying the original, so B is the direct answer, but C also effectively changes it by reassignment. The best single answer is B.

---

### Question 9

What does `reshaped_df.isna().values.any()` check?

A. Whether any column contains `NaN`.  
B. Whether any row contains `NaN`.  
C. Whether any element in the entire DataFrame is `NaN`.  
D. Whether the DataFrame has any missing values in the index.

**Answer:** C  
**Explanation:** `.isna()` returns a Boolean DataFrame of the same shape. `.values` extracts the underlying NumPy array, and `.any()` returns `True` if any element in that array is `True`. Thus, it checks if there is at least one `NaN` anywhere in the DataFrame.

---

### Question 10

When plotting with Matplotlib, what does `plt.figure(figsize=(16,10))` do?

A. It sets the size of the plot to 16 inches wide by 10 inches tall.  
B. It creates a new figure with the specified size.  
C. It scales the data to fit within 16 by 10 units.  
D. Both A and B.

**Answer:** D  
**Explanation:** `plt.figure()` creates a new figure (if not already existing) and the `figsize` argument sets its dimensions in inches. So both A and B are accurate descriptions.

---

### Question 11

How do you add a legend to a Matplotlib plot that distinguishes multiple lines?

A. Use `plt.legend()` after plotting with `label` parameters.  
B. Use `plt.legend()` and pass the line objects manually.  
C. Use `plt.show(legend=True)`.  
D. Both A and B are correct.

**Answer:** D  
**Explanation:** The simplest way is to include a `label` in each `plot()` call and then call `plt.legend()`. Alternatively, you can capture the line objects and pass them to `legend()`. Both work, but A is the most common.

---

### Question 12

In the loop `for column in reshaped_df.columns: plt.plot(reshaped_df.index, reshaped_df[column], linewidth=3, label=column)`, what does `label=column` achieve?

A. It sets the line color.  
B. It assigns the column name as the label for the legend.  
C. It labels the x-axis with the column name.  
D. It adds a title to the plot.

**Answer:** B  
**Explanation:** The `label` parameter in `plot()` provides the text that appears in the legend for that line. Here, `column` is the language name, so the legend will show the language names.

---

### Question 13

Why might we apply a rolling average (e.g., `reshaped_df.rolling(window=6).mean()`) to our data?

A. To reduce the number of data points.  
B. To smooth out short-term fluctuations and highlight long-term trends.  
C. To interpolate missing values.  
D. To convert monthly data to yearly data.

**Answer:** B  
**Explanation:** Rolling averages (moving averages) average values over a sliding window, which reduces noise and makes underlying trends more visible. It does not reduce the number of points (the DataFrame remains the same shape) and is not primarily for interpolation or resampling.

---

### Question 14

What happens to the first `window-1` rows when you compute a rolling mean with `window=6`?

A. They become `NaN` because there aren't enough preceding values to form a full window.  
B. They are dropped from the DataFrame.  
C. They are filled with zeros.  
D. They are calculated using a smaller window.

**Answer:** A  
**Explanation:** By default, rolling operations require a full window. For the first 5 rows (when window=6), there are not enough previous observations, so the result is `NaN`. You can change this behavior with the `min_periods` parameter.

---

### Question 15

Which of the following best describes the trend for Python in the smoothed chart (6-month rolling average)?

A. Steady decline since 2008.  
B. Rapid increase starting around 2012–2013, overtaking other languages.  
C. Flat line with no significant change.  
D. Peaked in 2010 and then decreased.

**Answer:** B  
**Explanation:** The smoothed chart shows Python's popularity growing slowly initially, then accelerating around 2012–2013, eventually surpassing Java and other languages by the end of the dataset.

---

### Question 16

What does the `plt.ylim(0, 35000)` call do?

A. It sets the range of the y-axis from 0 to 35000.  
B. It limits the data to values between 0 and 35000.  
C. It sets the number of ticks on the y-axis to 35000.  
D. It scales the y-axis logarithmically.

**Answer:** A  
**Explanation:** `plt.ylim()` sets the lower and upper bounds of the y-axis display range. It does not filter the data; it only affects the visible portion of the plot.

---

### Question 17

If you wanted to plot only the data from 2010 onwards, how could you do it using the reshaped DataFrame?

A. `plt.plot(reshaped_df.index[2010:], reshaped_df['python'][2010:])`  
B. `plt.plot(reshaped_df.loc['2010':], reshaped_df['python'])`  
C. `plt.plot(reshaped_df.loc['2010':, 'python'])`  
D. Both B and C, but C is more precise.

**Answer:** D  
**Explanation:** With a DatetimeIndex, you can slice using date strings. `reshaped_df.loc['2010':, 'python']` selects rows from 2010 onward and the 'python' column. B also works but would plot all columns if not careful. C is the correct and precise way.

---

### Question 18

What is the purpose of the `linewidth` parameter in `plt.plot()`?

A. It sets the thickness of the plotted line.  
B. It determines the width of the figure.  
C. It controls the spacing between ticks.  
D. It sets the font size of the legend.

**Answer:** A  
**Explanation:** `linewidth` (or `lw`) controls the thickness of the line drawn. Increasing it makes the line more prominent, which is useful when many lines overlap.

---

### Question 19

After pivoting, why does the `c#` column have 145 non-null entries while most others have 144?

A. Because C# had an extra month of data due to a data collection error.  
B. Because C# existed before Stack Overflow started, so it had posts in July 2008.  
C. Because the count includes an extra month at the end.  
D. It's likely that C# had posts in every month from July 2008 to the end, totaling 145 months.

**Answer:** D  
**Explanation:** The dataset starts in July 2008. Most languages appear from August 2008 onward, giving 144 months (August 2008 to July 2020). C# had posts in July 2008 as well, so it has one extra month, totaling 145.

---

### Question 20

Which of the following correctly computes and plots a 12-month rolling average for all languages?

A.  
```python
roll_df = reshaped_df.rolling(12).mean()
plt.plot(roll_df.index, roll_df)
```
B.  
```python
roll_df = reshaped_df.rolling(window=12).mean()
for col in roll_df.columns:
    plt.plot(roll_df.index, roll_df[col], label=col)
plt.legend()
```
C.  
```python
roll_df = reshaped_df.rolling(12).apply(np.mean)
plt.plot(roll_df)
```
D. Both A and B will work, but B includes a legend.

**Answer:** D  
**Explanation:** Option A plots all columns at once, but without a legend you cannot distinguish them. Option B plots each column with a label and legend, making it interpretable. Both compute the rolling average correctly. However, option A's `plt.plot(roll_df.index, roll_df)` will produce multiple lines but no legend. So B is the better practice, but technically A also works. D acknowledges that both are valid, with B adding a legend.

---

**End of Quiz**