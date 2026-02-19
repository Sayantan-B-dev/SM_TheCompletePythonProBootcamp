Preliminary Data Exploration and Visualising Births & Deaths at Vienna Hospital
You (aka Dr Semmelweis) are working at Vienna General Hospital. Let's take a closer look at the data you've been collecting on the number of births and maternal deaths throughout the 1840s.




Challenge 1: Preliminary Data Exploration
What is the shape of df_yearly and df_monthly? How many rows and columns?

What are the column names?

Which years are included in the dataset?

Are there any NaN values or duplicates?

What were the average number of births that took place per month?

What were the average number of deaths that took place per month?



.

.

..

...

..

.

.



Solution to Challenge 1

Using .shape, .head(), .tail() we see that the dataset covers the years 1841 to 1849. The two tables report the total number of births and the total number of deaths. Interestingly, the yearly data breaks the number of birthds and deaths down by clinic.


We see that there are no NaN values in either of the DataFrames. We can verify this either with using .info() or using .isna().values.any().


There are also no duplicate entries. In other words, the dataset appears to be clean.


Using .describe() allows us to view some interesting statistics at a glance. We see that on average there were about 267 births and 22.47 deaths per month.



Challenge 2: Percentage of Women Dying in Childbirth
How dangerous was childbirth in the 1840s in Vienna?

Using the annual data, calculate the percentage of women giving birth who died throughout the 1840s at the hospital.

In comparison, the United States recorded 18.5 maternal deaths per 100,000 or 0.018% in 2013 (source).



.

.

..

...

..

.

.





Solution to Challenge 2

Childbirth was very risky! About 7.08% of women died 💀 in the 1840s (compared to 0.018% in the US in 2013).

prob = df_yearly.deaths.sum() / df_yearly.births.sum() * 100
print(f'Chances of dying in the 1840s in Vienna: {prob:.3}%')
If someone gave me a bag of 100 M&Ms and told me that 7 of them would kill me, I'd (probably) pass on those M&Ms 🤭. Just saying.



Challenge 3: Visualise the Total Number of Births 🤱 and Deaths 💀 over Time
Create a Matplotlib chart with twin y-axes. It should look something like this:


Format the x-axis using locators for the years and months (Hint: we did this in the Google Trends notebook)

Set the range on the x-axis so that the chart lines touch the y-axes

Add gridlines

Use skyblue and crimson for the line colours

Use a dashed line style for the number of deaths

Change the line thickness to 3 and 2 for the births and deaths respectively.

Do you notice anything in the late 1840s?



.

.

..

...

..

.

.



Solution to Challenge 3

Just as in previous notebooks we can use .twinx() to create to y-axes. Then it's just a matter of adding a gird with .grid() and configuring the look of our plots with the color, linewidth, and linestyle parameters.

plt.figure(figsize=(14,8), dpi=200)
plt.title('Total Number of Monthly Births and Deaths', fontsize=18)
 
ax1 = plt.gca()
ax2 = ax1.twinx()
 
ax1.grid(color='grey', linestyle='--')
 
ax1.plot(df_monthly.date, 
         df_monthly.births, 
         color='skyblue', 
         linewidth=3)
 
ax2.plot(df_monthly.date, 
         df_monthly.deaths, 
         color='crimson', 
         linewidth=2, 
         linestyle='--')
 
plt.show()

To get the tickmarks showing up on the x-axis, we need to use mdates and Matplotlib's locators.

# Create locators for ticks on the time axis
years = mdates.YearLocator()
months = mdates.MonthLocator()
years_fmt = mdates.DateFormatter('%Y') 
We can then use the locators in our chart:

plt.figure(figsize=(14,8), dpi=200)
plt.title('Total Number of Monthly Births and Deaths', fontsize=18)
plt.yticks(fontsize=14)
plt.xticks(fontsize=14, rotation=45)
 
ax1 = plt.gca()
ax2 = ax1.twinx()
 
ax1.set_ylabel('Births', color='skyblue', fontsize=18)
ax2.set_ylabel('Deaths', color='crimson', fontsize=18)
 
# Use Locators
ax1.set_xlim([df_monthly.date.min(), df_monthly.date.max()])
ax1.xaxis.set_major_locator(years)
ax1.xaxis.set_major_formatter(years_fmt)
ax1.xaxis.set_minor_locator(months)
 
ax1.grid(color='grey', linestyle='--')
 
ax1.plot(df_monthly.date, 
         df_monthly.births, 
         color='skyblue', 
         linewidth=3)
 
ax2.plot(df_monthly.date, 
         df_monthly.deaths, 
         color='crimson', 
         linewidth=2, 
         linestyle='--')
 
plt.show()

What we see is that something happened after 1847. The total number of deaths seems to have dropped, despite an increasing number of births! 🤔

