## Data Visualisation with Matplotlib

With the data cleaned, reshaped, and missing values handled, we are now ready to visualize the popularity trends of programming languages over time. The primary tool for this task is **Matplotlib**, a comprehensive library for creating static, animated, and interactive visualizations in Python. In this section, we will:

- Import Matplotlib's `pyplot` module.
- Create a basic line chart for a single programming language.
- Customize the chart to improve readability (size, axis labels, ticks, limits).
- Add a second line to compare two languages.

These steps lay the foundation for more advanced visualizations, such as plotting all languages together and applying rolling averages.

### Importing Matplotlib

Before plotting, we need to import the `pyplot` module. By convention, it is imported as `plt`:

```python
import matplotlib.pyplot as plt
```

This import is typically placed at the top of the notebook alongside Pandas. The `pyplot` module provides a MATLAB-like interface for creating figures and axes, and it handles the underlying state machine automatically, making it convenient for quick plotting.

### Basic Line Chart for a Single Language

The simplest way to plot a line chart is to call `plt.plot()` with two arguments: the x-axis values and the y-axis values. For our data, the x-axis should be the dates (the index of `reshaped_df`), and the y-axis should be the post counts for a specific language (a column of `reshaped_df`).

For example, to plot the popularity of Java:

```python
plt.plot(reshaped_df.index, reshaped_df['java'])
```

Or using dot notation (since the column name has no spaces):

```python
plt.plot(reshaped_df.index, reshaped_df.java)
```

Both produce the same result. Executing this in a Jupyter cell will display a line chart. However, the default chart is quite small and lacks labels, making it difficult to interpret.

### Customizing the Chart

To make the chart more informative and visually appealing, we can apply several customizations:

1. **Increase figure size**: `plt.figure(figsize=(width, height))` creates a new figure with specified dimensions (in inches). A width of 16 and height of 10 works well for time-series data.
2. **Adjust tick font sizes**: `plt.xticks(fontsize=14)` and `plt.yticks(fontsize=14)` make axis numbers easier to read.
3. **Add axis labels**: `plt.xlabel('Date', fontsize=14)` and `plt.ylabel('Number of Posts', fontsize=14)` describe what the axes represent.
4. **Set y-axis limits**: `plt.ylim(0, 35000)` ensures the y-axis starts at zero and caps at a reasonable maximum, preventing the chart from being distorted by extreme values.

Applying these customizations to the Java plot:

```python
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)

plt.plot(reshaped_df.index, reshaped_df.java)
```

The resulting chart is much clearer: the date axis is properly spaced (Matplotlib automatically formats the dates), the line is visible, and the overall layout is professional.

#### Explanation of Each Customization

- `plt.figure(figsize=(16,10))`: Creates a new figure with the given size. If you call this after other plotting commands, it will start a fresh figure. It's good practice to call it at the beginning of a plotting block.
- `plt.xticks(fontsize=14)`: Sets the font size for tick labels on the x-axis. Similarly for `plt.yticks()`.
- `plt.xlabel()` and `plt.ylabel()`: Add labels to the axes. The `fontsize` parameter controls the label's font size.
- `plt.ylim(0, 35000)`: Sets the lower and upper bounds of the y-axis. Since post counts cannot be negative, zero is a natural lower bound. The upper bound (35000) is chosen based on the maximum number of posts observed (around 30,000 for Python at its peak). This bound can be adjusted if other languages exceed it.

### Challenge: Plotting Two Languages (Java and Python)

The notebook poses a challenge: can you plot both Java and Python on the same chart? The solution is straightforward: simply call `plt.plot()` twice before displaying the chart.

```python
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)

plt.plot(reshaped_df.index, reshaped_df.java)
plt.plot(reshaped_df.index, reshaped_df.python)
```

This overlays two lines on the same axes. However, without a legend, it is impossible to tell which line corresponds to which language. To add a legend, we include the `label` parameter in each `plot()` call and then call `plt.legend()`:

```python
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)

plt.plot(reshaped_df.index, reshaped_df.java, label='Java')
plt.plot(reshaped_df.index, reshaped_df.python, label='Python')
plt.legend(fontsize=14)
```

The legend will appear in the default location (usually the best fit). You can adjust its position with the `loc` parameter (e.g., `loc='upper left'`).

### Under the Hood: How Matplotlib Handles Dates

One of the benefits of having a datetime index is that Matplotlib automatically recognizes it and formats the x-axis appropriately. It chooses a reasonable date format based on the range (e.g., showing years for multi-year spans) and spaces the ticks evenly in time, not just by index position. This ensures that gaps in the data (e.g., missing months) are represented accurately—the line will not connect across a gap if you have `NaN`, but since we filled with zeros, the line will drop to zero for those months.

### Next Steps

Now that we can plot individual and pairs of languages, the next logical step is to visualize all languages simultaneously. Doing this manually with 14 `plot()` calls would be tedious. Instead, we can use a for-loop to iterate over the columns of `reshaped_df`. This approach, along with adding a comprehensive legend, is covered in the next file (530).

---

*Note: In the notebook, you may notice that after plotting, Jupyter displays both the plot and an output like `<matplotlib.lines.Line2D at 0x...>` or the legend object. This is normal; the plot itself is the primary output. If you want to suppress the extra text, you can end the cell with a semicolon after the last plotting command, or use `plt.show()` at the end.*