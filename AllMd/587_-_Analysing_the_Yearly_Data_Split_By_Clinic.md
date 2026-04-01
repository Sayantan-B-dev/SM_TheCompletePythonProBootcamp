## Analysing the Yearly Data Split by Clinic

The yearly data provides a breakdown by clinic, allowing a direct comparison between the two maternity wards. Clinic 1 was staffed by male doctors and medical students, while Clinic 2 was staffed by female midwives. This section explores how the number of births and deaths differed between the clinics and calculates the proportion of deaths to account for different patient volumes. The analysis uses Plotly Express to create interactive line charts.

### Dataset

The yearly data is stored in `df_yearly` with columns: `year`, `births`, `deaths`, `clinic`. It covers the years 1841 to 1846 for both clinics.

```python
import pandas as pd
import plotly.express as px

df_yearly = pd.read_csv('annual_deaths_by_clinic.csv')
```

---

### Challenge 1: The Yearly Data Split by Clinic

#### Births by Clinic

We create a line chart of yearly births, colored by clinic, to see how each clinic’s patient volume changed over time.

```python
line = px.line(df_yearly, 
               x='year', 
               y='births',
               color='clinic',
               title='Total Yearly Births by Clinic')
line.show()
```

**Interpretation**:

- Both clinics experienced an increase in births from 1841 to 1846, indicating the hospital became busier.
- Clinic 1 consistently had more births than Clinic 2. This suggests Clinic 1 was either larger or more popular.
- The gap between the two clinics widened over the years.

#### Deaths by Clinic

Similarly, we plot the total yearly deaths.

```python
line = px.line(df_yearly, 
               x='year', 
               y='deaths',
               color='clinic',
               title='Total Yearly Deaths by Clinic')
line.show()
```

**Interpretation**:

- Clinic 1 also recorded many more deaths than Clinic 2.
- The highest number of deaths in Clinic 1 occurred in 1842 (518 deaths), while Clinic 2 peaked in 1842 as well (202 deaths).
- Although deaths fluctuate, the raw numbers cannot be directly compared because the number of patients differs.

#### Key Findings from Challenge 1

- **Which clinic is bigger?** Clinic 1, based on the number of births.
- **Has the hospital had more patients over time?** Yes, births increased steadily.
- **Highest recorded deaths:** Clinic 1: 518 (1842); Clinic 2: 202 (1842).

---

### Challenge 2: Calculate the Proportion of Deaths at Each Clinic

To compare the risk of dying in childbirth between the clinics, we must account for the different patient volumes. We compute the death proportion for each clinic each year.

#### Adding a Percentage Column

```python
df_yearly['pct_deaths'] = df_yearly.deaths / df_yearly.births
df_yearly
```

This column represents the fraction of women who died in that clinic that year.

#### Average Death Rate for Each Clinic (Entire Period)

```python
clinic_1 = df_yearly[df_yearly.clinic == 'clinic 1']
avg_c1 = clinic_1.deaths.sum() / clinic_1.births.sum() * 100
print(f'Average death rate in clinic 1 is {avg_c1:.3}%.')   # 9.92%

clinic_2 = df_yearly[df_yearly.clinic == 'clinic 2']
avg_c2 = clinic_2.deaths.sum() / clinic_2.births.sum() * 100
print(f'Average death rate in clinic 2 is {avg_c2:.3}%.')   # 3.88%
```

**Interpretation**:

- Clinic 1 had an average death rate of 9.92% – nearly 1 in 10 women died.
- Clinic 2 had an average death rate of 3.88% – about 1 in 26.
- The death rate in Clinic 1 was more than 2.5 times higher than in Clinic 2.

#### Visualising Yearly Death Proportions

A line chart of the death proportion over time reveals the year‑by‑year comparison.

```python
line = px.line(df_yearly, 
               x='year', 
               y='pct_deaths',
               color='clinic',
               title='Proportion of Yearly Deaths by Clinic')
line.show()
```

**Observations**:

- In every year, Clinic 1 had a higher death proportion than Clinic 2.
- The worst year was 1842, when Clinic 1’s death rate reached approximately 16%, while Clinic 2’s peaked at about 7.6%.
- Although both clinics show a general decline after 1842, Clinic 1 remained consistently more dangerous.

#### Highest Monthly Death Rates

The question asks for the highest monthly death rate in each clinic. However, the yearly data only gives annual rates. To answer precisely, we would need monthly data broken down by clinic (which is not provided). Based on the yearly proportions, the highest for Clinic 1 was 16% (1842) and for Clinic 2 was 7.6% (1842). The true monthly peaks could be higher, but the yearly data gives a lower bound.

---

### The Story Continues: Hypotheses and Breakthrough

Dr. Semmelweis was puzzled by the persistent difference between the clinics. He tested several hypotheses:

1. **Position during childbirth**: In Clinic 2, women gave birth on their sides; in Clinic 1, on their backs. Changing the position in Clinic 1 had no effect.
2. **Psychological impact of the priest**: A priest walked through Clinic 1 ringing a bell after a death, possibly terrifying new mothers. Changing the route and stopping the bell had no effect.

Frustrated, Semmelweis took a holiday to Venice. Upon his return, he learned that a colleague, a pathologist, had died after pricking his finger during an autopsy on a woman who had died of childbed fever. The pathologist’s symptoms mirrored those of the fever.

**Breakthrough insight**: The disease was not confined to pregnant women; anyone could contract it. This led Semmelweis to hypothesise that “cadaverous particles” from autopsies were being carried on the hands of doctors and medical students to the women in Clinic 1, causing infection. Midwives in Clinic 2 did not perform autopsies, so they were not transmitting these particles.

This hypothesis directly explained the higher death rate in Clinic 1 and set the stage for the handwashing intervention.

---

### Summary of Yearly Clinic Analysis

- Clinic 1, staffed by doctors, had consistently higher birth and death numbers.
- When comparing proportions, Clinic 1’s death rate was more than double that of Clinic 2.
- The difference persisted year after year, ruling out chance.
- The pathologist’s death provided the crucial clue that the infection could be transmitted from corpses to living patients via contaminated hands.
- This realisation led to the handwashing policy in June 1847, which we analyse next using the monthly data.