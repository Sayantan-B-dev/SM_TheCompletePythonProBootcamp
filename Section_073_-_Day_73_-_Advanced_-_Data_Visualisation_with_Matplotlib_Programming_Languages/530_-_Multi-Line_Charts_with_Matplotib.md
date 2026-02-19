## Multi-Line Charts with Matplotlib

After successfully plotting individual languages and comparing two on the same chart, the next logical step is to visualize all programming languages together. This allows us to see relative trends, identify which languages are gaining or losing popularity, and observe the overall landscape of Stack Overflow discussions. Manually calling `plt.plot()` for each of the 14 languages would be repetitive and error-prone. Instead, we leverage Python's looping capabilities to automate the process. This section covers:

- Plotting all languages using a `for` loop.
- Adding a legend to distinguish the lines.
- Adjusting line thickness and labels for better readability.
- Interpreting the resulting multi-line chart.

### Why Plot All Languages?

Plotting all languages on a single chart provides a comprehensive view of the data. It highlights:

- **Dominant languages**: Which languages consistently have high post counts.
- **Rising stars**: Languages that show rapid growth (e.g., Python in recent years).
- **Declining trends**: Languages that are losing popularity (e.g., Perl, Delphi).
- **Comparative trajectories**: How different languages evolve relative to each other.

However, a chart with many overlapping lines can become cluttered. Therefore, careful styling (line widths, colors, legends) is essential to maintain readability.

### Plotting All Languages with a For Loop

The reshaped DataFrame `reshaped_df` has 14 columns, each representing a programming language. We can iterate over these columns and call `plt.plot()` for each one. The loop will generate a line for every language using Matplotlib's default color cycle (which automatically assigns distinct colors).

```python
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)

for column in reshaped_df.columns:
    plt.plot(reshaped_df.index, reshaped_df[column])
```

This code produces a chart with 14 lines, all on the same axes. However, without labels or a legend, it is impossible to know which line corresponds to which language. The colors alone are not sufficient for identification.

### Adding a Legend

To make the chart interpretable, we need a legend. Matplotlib's legend is built from the `label` parameter provided in each `plot()` call. We can set the label to the column name (the language). Then, after the loop, we call `plt.legend()` to display the legend.

Additionally, we can make the lines thicker using the `linewidth` parameter (or `lw` for short) to improve visibility, especially when many lines are present.

```python
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts', fontsize=14)
plt.ylim(0, 35000)

for column in reshaped_df.columns:
    plt.plot(reshaped_df.index, reshaped_df[column], 
             linewidth=3, label=reshaped_df[column].name)

plt.legend(fontsize=16)
```

Now the chart includes a legend in the default position (usually Matplotlib tries to place it where it least obstructs the data). The `fontsize` for the legend is increased to 16 for readability.

#### Explanation of Parameters

- `linewidth=3`: Sets the thickness of the line. The default is around 1.5; increasing to 3 makes lines stand out.
- `label=reshaped_df[column].name`: Assigns the column name as the label. Since `reshaped_df[column]` is a Series, its `name` attribute holds the column name (e.g., 'python', 'java').
- `plt.legend(fontsize=16)`: Creates the legend with the specified font size. The legend automatically collects all labels from previous `plot()` calls.

### Resulting Chart

After running the above code, we see a chart similar to the one in the notebook. It reveals that:

- **JavaScript**, **Java**, **Python**, **C#**, and **PHP** have the highest post volumes.
- **Python** shows a steep upward trend, especially after 2012, overtaking others.
- **Java** and **C#** remain strong but have plateaued or slightly declined.
- **Perl**, **Delphi**, and **Assembly** have very low counts, indicating niche usage.
- Newer languages like **Go** and **Swift** appear later in the timeline and show growth.

The legend, placed in the upper left, lists all languages with their corresponding line colors. However, with 14 entries, the legend can be large and may cover part of the chart. In such cases, you can adjust its location using the `loc` parameter (e.g., `loc='upper right'`, `loc='center left'`, `loc='best'`). You can also split the legend into multiple columns using `ncol` (e.g., `plt.legend(fontsize=12, ncol=2)`).

### Potential Issues and Refinements

- **Overlapping lines**: With many lines, some may be hidden behind others. You can control the order of plotting: languages plotted later appear on top. In the loop, the order is the column order in `reshaped_df`. To highlight a particular language, you could plot it last.
- **Color cycling**: Matplotlib cycles through a default color list. If you want specific colors for certain languages, you can pass a `color` parameter (e.g., `color='red'`) inside the loop.
- **Legend placement**: If the legend covers important data, try `loc='center left'` and use `bbox_to_anchor=(1, 0.5)` to place it outside the plot area.

### Next Steps: Smoothing Time-Series Data

While the multi-line chart provides a comprehensive view, the raw data can be noisy, with many short-term fluctuations. This noise can obscure long-term trends. The next file (531) introduces **rolling averages** (also called moving averages) to smooth the data. By averaging over a window of months (e.g., 6 or 12 months), we can reduce the noise and make trends more apparent. Pandas' `rolling()` and `mean()` methods make this easy, and we will apply them to our reshaped DataFrame before plotting again.

---

*Note: In the notebook, after plotting, you may see the legend object printed as output (e.g., `<matplotlib.legend.Legend at 0x...>`). This is normal; to suppress it, you can add a semicolon at the end of the last line or use `plt.show()`. The plot itself is still displayed.*