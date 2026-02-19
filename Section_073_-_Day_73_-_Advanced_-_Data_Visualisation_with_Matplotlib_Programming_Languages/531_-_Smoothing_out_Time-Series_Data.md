## Smoothing out Time-Series Data

Time-series data, such as the monthly post counts on Stack Overflow, often contains significant short-term fluctuations or "noise." These variations can obscure the underlying long-term trends—for instance, a language might show a temporary spike due to a new release or a seasonal effect, but the overall direction of its popularity may be more stable. To reveal these trends more clearly, we apply a technique called **rolling averages** (also known as moving averages). This section covers:

- The concept of rolling averages and why they are useful.
- How to compute rolling averages using Pandas' `rolling()` and `mean()` methods.
- Plotting the smoothed data alongside the original or as a replacement.
- Choosing an appropriate window size and observing its effect.
- Interpreting the smoothed chart to identify trends.

### Why Smooth Time-Series Data?

Raw time-series data can be "noisy" due to many factors:

- **Seasonality**: Certain times of the year (e.g., summer, holidays) may see more or fewer posts.
- **Random fluctuations**: Day-to-day or month-to-month variations that are not indicative of a lasting change.
- **Transient events**: A sudden surge of interest in a language due to a new framework release, a conference, or a viral project.

A rolling average smooths out these short-term irregularities by averaging the values over a consecutive window of time. The result is a smoother curve that highlights the underlying trend.

For example, a 6-month rolling average at month `t` is the average of the post counts from months `t-5` to `t`. As we move forward one month, the window shifts, dropping the oldest month and including the newest. This produces a series of averages that track the general direction without being overly influenced by single-month anomalies.

### Computing Rolling Averages with Pandas

Pandas provides a convenient `rolling()` method that creates a windowed view of a DataFrame or Series. It can be chained with various aggregation functions, most commonly `mean()` for averages.

The basic syntax is:

```python
roll_df = reshaped_df.rolling(window=n).mean()
```

where `n` is the size of the moving window (number of observations). The result `roll_df` is a DataFrame of the same shape as the original, but each cell contains the rolling average for that language at that time point. For the first `n-1` rows, where a full window is not available, the values are `NaN` by default. However, when plotting, Matplotlib will simply not connect those points, or you can choose to drop them.

#### Example with a 6-Month Window

```python
roll_df = reshaped_df.rolling(window=6).mean()
```

After this operation, `roll_df` contains the smoothed values. For instance, the value for Python in January 2009 would be the average of Python posts from August 2008 through January 2009 (six months).

### Plotting the Smoothed Data

We can then plot `roll_df` using the same styling as before. The code from the previous section is easily adapted:

```python
plt.figure(figsize=(16,10))
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Number of Posts (6-month rolling average)', fontsize=14)
plt.ylim(0, 35000)

for column in roll_df.columns:
    plt.plot(roll_df.index, roll_df[column], 
             linewidth=3, label=roll_df[column].name)

plt.legend(fontsize=16)
```

Notice we changed the y-axis label to reflect that we are now showing a rolling average. The chart now displays much smoother lines, making it easier to compare long-term trends.

### Interpreting the Smoothed Chart

The resulting smoothed chart (as shown in the notebook) reveals several insights that were less obvious in the raw data:

- **Python's ascent**: The smoothed line for Python shows a steady and accelerating increase, confirming its rise as a dominant language.
- **Java's plateau**: After a peak around 2013-2014, Java's smoothed line levels off and even declines slightly, suggesting a stabilization or gradual loss of share.
- **C# and JavaScript**: Both maintain high levels but show more fluctuation; the smoothing clarifies their relative positions.
- **Newer languages (Go, Swift)**: Their smoothed lines start later and show growth trajectories, though they remain far below the leaders.
- **Legacy languages (Perl, Delphi)**: Their smoothed lines are consistently low, indicating sustained low interest.

The smoothing also helps to compare the "momentum" of different languages. For instance, Python's line has a steeper slope than Java's in recent years, indicating faster growth.

### Choosing the Window Size

The choice of window size significantly affects the smoothness and responsiveness of the averaged line:

- **Small window (e.g., 3 months)**: Retains more of the original fluctuation but still reduces some noise. It reacts quickly to changes.
- **Large window (e.g., 12 months)**: Produces a very smooth line but may lag behind real trends and obscure short-term shifts. It is better for identifying multi-year trends.
- **Medium window (e.g., 6 months)**: A compromise that balances smoothness and responsiveness.

The notebook encourages experimenting with the `window` argument (e.g., 3 or 12) to see how the chart changes. This is an important exploratory step: different windows can reveal different aspects of the data.

#### Visual Comparison

If you set `window=3`, the lines will be more wiggly, still showing some seasonal patterns. With `window=12`, the lines become much smoother, potentially smoothing out even significant year-long trends. The choice depends on the question you are trying to answer. For identifying general popularity trends over the entire history, a 6- or 12-month window is appropriate.

### Important Considerations

- **Edge effects**: The first `window-1` rows of `roll_df` will contain `NaN` because there aren't enough preceding observations to form a full window. When plotting, these points are either omitted or cause the line to start later. In our case, with a 6-month window, the smoothed lines begin in January 2009 (six months after July 2008). This is acceptable because we are interested in the overall trend, and the early months are less critical.
- **Data frequency**: Our data is monthly, so a window of 6 means averaging over half a year. If the data were daily, the same window would represent 6 days. Always interpret the window in the context of the data's time unit.
- **Other smoothing methods**: Rolling averages are simple and intuitive, but other techniques like exponentially weighted moving averages (using `ewm()`) or LOESS smoothing exist. Rolling averages are often sufficient for exploratory analysis.

### Next Steps

With the smoothed chart, we have completed the core analysis of programming language popularity over time. The final file (532) summarizes the key learning points and provides a quiz to reinforce the concepts. However, the notebook also includes some additional code cells that are empty—these are placeholders for further exploration, such as experimenting with different languages or time ranges.

---

*Note: The code and chart in the notebook use a 6-month rolling average. To see the effect of a different window, simply change the number in `rolling(window=...)` and re-run the plotting cell.*