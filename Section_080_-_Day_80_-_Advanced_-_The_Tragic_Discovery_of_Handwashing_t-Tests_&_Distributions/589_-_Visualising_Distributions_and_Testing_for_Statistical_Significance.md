isualising Distributions and Testing for Statistical Significance
There are even more powerful arguments we can make to convince our fellow doctors in clinic 1 of the virtues of handwashing. The first are statistics regarding the mean monthly death rate. The second are compelling visualisations to accompany the statistics.

Challenge 1: Calculate the Difference in the Average Monthly Death Rate
What was the average percentage of monthly deaths before handwashing (i.e., before June 1847)?

What was the average percentage of monthly deaths after handwashing was made obligatory?

By how much did handwashing reduce the average chance of dying in childbirth in percentage terms?

How do these numbers compare to the average for all the 1840s that we calculated earlier?

How many times lower are the chances of dying after handwashing compared to before?



.

.

..

...

..

.

.



Solution to Challenge 1

A lot of statistical tests rely on comparing features of distributions, like the mean. We see that the average death rate before handwashing was 10.5%. After handwashing was made obligatory, the average death rate was 2.11%. The difference is massive. Handwashing decreased the average death rate by 8.4%, a 5x improvement. 😮

avg_prob_before = before_washing.pct_deaths.mean() * 100
print(f'Chance of death during childbirth before handwashing: {avg_prob_before:.3}%.')
 
avg_prob_after = after_washing.pct_deaths.mean() * 100
print(f'Chance of death during childbirth AFTER handwashing: {avg_prob_after:.3}%.')
 
mean_diff = avg_prob_before - avg_prob_after
print(f'Handwashing reduced the monthly proportion of deaths by {mean_diff:.3}%!')
 
times = avg_prob_before / avg_prob_after
print(f'This is a {times:.2}x improvement!')


Challenge 2: Using Box Plots to Show How the Death Rate Changed Before and After Handwashing
The statistic above is impressive, but how do we show it graphically? With a box plot we can show how the quartiles, minimum, and maximum values changed in addition to the mean.

Use NumPy's .where() function to add a column to df_monthly that shows if a particular date was before or after the start of handwashing.

Then use plotly to create box plot of the data before and after handwashing.

How did key statistics like the mean, max, min, 1st and 3rd quartile changed as a result of the new policy



.

.

..

...

..

.

.



Solution to Challenge 2

The easiest way to create a box plot is to have a column in our DataFrame that shows the rows' "category" (i.e., was it before or after obligatory handwashing). NumPy allows us to easily test for a condition and add a column of data.

df_monthly['washing_hands'] = np.where(df_monthly.date < handwashing_start, 'No', 'Yes')
Now we can use plotly:

box = px.box(df_monthly, 
             x='washing_hands', 
             y='pct_deaths',
             color='washing_hands',
             title='How Have the Stats Changed with Handwashing?')
 
box.update_layout(xaxis_title='Washing Hands?',
                  yaxis_title='Percentage of Monthly Deaths',)
 
box.show()

The plot shows us the same data as our Matplotlib chart, but from a different perspective. Here we also see the massive spike in deaths in late 1842. Over 30% of women who gave birth that month died in hospital. What we also see in the box plot is how not only did the average death rate come down, but so did the overall range - we have a lower max and 3rd quartile too. Let's take a look at a histogram to get a better sense of the distribution.



Challenge 3: Use Histograms to Visualise the Monthly Distribution of Outcomes
Create a plotly histogram to show the monthly percentage of deaths.

Use docs to check out the available parameters. Use the color parameter to display two overlapping histograms.

The time period of handwashing is shorter than not handwashing. Change histnorm to percent to make the time periods comparable.

Make the histograms slightly transparent

Experiment with the number of bins on the histogram. Which number works well in communicating the range of outcomes?

Just for fun, display your box plot on the top of the histogram using the marginal parameter





.

.

..

...

..

.

.



Solution to Challenge 3

To create our histogram, we once again make use of the color parameter. This creates two separate histograms for us. When we set the opacity to 0.6 or so we can clearly see how the histograms overlap. The trick to getting a sensible-looking histogram when you have a very different number of observations is to set the histnorm to 'percent'. That way the histogram with more observations won't completely overshadow the shorter series.

hist = px.histogram(df_monthly, 
                   x='pct_deaths', 
                   color='washing_hands',
                   nbins=30,
                   opacity=0.6,
                   barmode='overlay',
                   histnorm='percent',
                   marginal='box',)
 
hist.update_layout(xaxis_title='Proportion of Monthly Deaths',
                   yaxis_title='Count',)
 
hist.show()
I quite like how in plotly we can display our box plot from earlier at the top.


Now, we have only about 98 data points or so, so our histogram looks a bit jagged. It's not a smooth bell-shaped curve. However, we can estimate what the distribution would look like with a Kernel Density Estimate (KDE).



Challenge 4: Use a Kernel Density Estimate (KDE) to visualise a smooth distribution
Use Seaborn's .kdeplot() to create two kernel density estimates of the pct_deaths, one for before handwashing and one for after.

Use the fill parameter to give your two distributions different colours.

What weakness in the chart do you see when you just use the default parameters?

Use the clip parameter to address the problem.



.

.

..

...

..

.

.



Solution to Challenge 4

To create two bell-shaped curves of the estimated distributions of the death rates we just call .kdeplot() twice.

plt.figure(dpi=200)
# By default the distribution estimate includes a negative death rate!
sns.kdeplot(before_washing.pct_deaths, fill=True)
sns.kdeplot(after_washing.pct_deaths, fill=True)
plt.title('Est. Distribution of Monthly Death Rate Before and After Handwashing')
plt.show()
However, the problem is that we end up with a negative monthly death rate on the left tail. The doctors would be very surprised indeed if a corpse came back to life after an autopsy! 🧟‍♀️


The solution is to specify a lower bound of 0 for the death rate.

plt.figure(dpi=200)
sns.kdeplot(before_washing.pct_deaths, 
            fill=True,
            clip=(0,1))
sns.kdeplot(after_washing.pct_deaths, 
            fill=True,
            clip=(0,1))
plt.title('Est. Distribution of Monthly Death Rate Before and After Handwashing')
plt.xlim(0, 0.40)
plt.show()

Now that we have an idea of what the two distributions look like, we can further strengthen our argument for handwashing by using a statistical test. We can test whether our distributions ended up looking so different purely by chance (i.e., the lower death rate is just an accident) or if the 8.4% difference in the average death rate is statistically significant.





Challenge 5: Use a T-Test to Show Statistical Significance
Use a t-test to determine if the differences in the means are statistically significant or purely due to chance.

If the p-value is less than 1% then we can be 99% certain that handwashing has made a difference to the average monthly death rate.

Import stats from scipy

Use the .ttest_ind() function to calculate the t-statistic and the p-value

Is the difference in the average proportion of monthly deaths statistically significant at the 99% level?



.

.

..

...

..

.

.



Solution to Challenge 5

The first step is to import stats from scipy

import scipy.stats as stats
When we calculate the p_value we see that it is 0.0000002985 or .00002985% which is far below even 1%. In other words, the difference in means is highly statistically significant and we can go ahead on publish our research paper 😊

t_stat, p_value = stats.ttest_ind(a=before_washing.pct_deaths, 
                                  b=after_washing.pct_deaths)
print(f'p-palue is {p_value:.10f}')
print(f't-statstic is {t_stat:.4}')
