## What You Learned – A Complete Summary

### 1. **Quickly spot relationships using Seaborn's `.pairplot()`**
- `.pairplot()` creates a grid of scatterplots for every pair of features, with histograms on the diagonal.  
- It gives an instant overview of correlations, trends, and potential outliers across your dataset.  
- **Example:** You saw that `NOX` (pollution) and `DIS` (distance to employment) have a negative correlation, while `RM` (rooms) and `PRICE` have a positive one.

### 2. **Split data into training and testing sets with `train_test_split()`**
- This function randomly divides your data into two parts: one for training the model and one for testing its performance on unseen data.  
- The `test_size=0.2` parameter means 20% of data is held out for testing.  
- `random_state=10` ensures you get the same split every time (reproducibility).

### 3. **Run a multivariable regression using `LinearRegression` from scikit‑learn**
- You created a model: `regr = LinearRegression()`  
- Then trained it: `regr.fit(X_train, y_train)`  
- This finds the best‑fit line (hyperplane) that minimises the sum of squared errors between predicted and actual values.

### 4. **Evaluate the model by checking the sign of coefficients**
- The coefficients (`.coef_`) tell you how much the target changes when a feature increases by one unit, holding all other features constant.  
- A positive sign means the feature increases the price; a negative sign means it decreases the price.  
- You verified that all signs matched your intuition (e.g., `RM` positive, `LSTAT` negative).

### 5. **Analyse residuals to detect patterns**
- Residuals = actual values – predicted values.  
- You plotted residuals vs predicted values and looked for randomness.  
- Patterns in residuals suggest the model might be missing something (e.g., non‑linear relationships).  
- You also checked the distribution of residuals (mean near zero, skewness close to zero for a good model).

### 6. **Improve the model with a log transformation**
- Because the target `PRICE` was right‑skewed, you applied `np.log()` to create `log(PRICE)`.  
- This made the distribution more normal and improved both R² and residual behaviour.  
- After transformation, the model became: `log(PRICE) = θ₀ + θ₁·RM + …`

### 7. **Make predictions with custom feature values**
- You created a new data point (e.g., 8 rooms, next to river, low poverty) and used `log_regr.predict()` to estimate its log price.  
- Then you reversed the log transformation with `np.exp()` to get a dollar value.

---

## 🔍 Explaining the “Weird” Function Names

Many function names come from statistics or mathematics and are abbreviated. Here's a breakdown of the most important ones:

### **`train_test_split`**
- **What it does:** Splits a dataset into random train and test subsets.  
- **Why the name:** It's literally “train‑test split”. The function comes from scikit‑learn’s `model_selection` module.  
- **Parameters:**  
  - `*arrays` – your features and target.  
  - `test_size` – fraction of data to put in test set.  
  - `random_state` – seed for random number generator (so you get the same split each time).

### **`LinearRegression`**
- **What it does:** Implements ordinary least squares linear regression.  
- **Why the name:** “Linear” because it models a linear relationship, “Regression” because it predicts a continuous value.  
- **Key methods:**  
  - `.fit(X, y)` – estimates the coefficients.  
  - `.predict(X)` – uses the fitted model to make predictions.  
  - `.score(X, y)` – returns the R² (coefficient of determination).  
  - `.coef_` – the estimated coefficients (one per feature).  
  - `.intercept_` – the bias term (θ₀).

### **`.fit()`**
- **What it does:** Trains the model on given data.  
- **Why the name:** In machine learning, “fitting” means adjusting the model parameters to best match the training data.

### **`.predict()`**
- **What it does:** Uses the trained model to generate predictions for new data.  
- **Why the name:** It literally predicts the output.

### **`.score()`**
- **What it does:** Returns the coefficient of determination R² for the given data.  
- **Why the name:** It “scores” the model’s performance. For regression, the default score is R².

### **`.coef_` and `.intercept_`**
- **`.coef_`** : an array of the coefficients (weights) for each feature.  
- **`.intercept_`** : the bias term (θ₀).  
- The trailing underscore is a scikit‑learn convention: attributes that are learned from data (like coefficients) have an underscore.

### **Seaborn functions**

#### **`sns.pairplot()`**
- **What it does:** Plots pairwise relationships in a dataset.  
- **Why the name:** “Pair” because it plots every pair of variables, “plot” because it's a plot.  
- **Parameters:** `data` – a DataFrame; you can also add `kind='reg'` to include regression lines.

#### **`sns.displot()`**
- **What it does:** Creates a distribution plot (histogram + optional KDE).  
- **Why the name:** “Dis” stands for distribution, “plot” for plot. It’s a figure‑level function introduced in newer seaborn versions.  
- **Parameters:** `bins`, `kde`, `aspect`, `color`, etc.

#### **`sns.jointplot()`**
- **What it does:** Draws a scatter plot of two variables with marginal histograms.  
- **Why the name:** “Joint” because it shows the joint distribution of two variables.  
- **Parameters:** `x`, `y`, `kind` (e.g., 'scatter', 'hex', 'reg'), `height`, `joint_kws` to pass extra arguments to the scatter plot.

#### **`sns.axes_style()`**
- **What it does:** Temporarily sets the aesthetic style of the plots.  
- **Why the name:** “Axes” refers to the matplotlib axes, “style” is the visual theme.  
- **Usage:** `with sns.axes_style('darkgrid'):` to apply a dark grid background only inside the block.

### **Matplotlib functions**

#### **`plt.figure()`**
- **What it does:** Creates a new figure (a blank canvas).  
- **Why the name:** In matplotlib, the top‑level container for all plot elements is called a “figure”.  
- **Parameters:** `figsize` (width, height in inches), `dpi` (dots per inch).

#### **`plt.scatter()`**
- **What it does:** Draws a scatter plot.  
- **Why the name:** “Scatter” because it scatters points.  
- **Parameters:** `x`, `y`, `c` (color), `alpha` (transparency).

#### **`plt.plot()`**
- **What it does:** Draws lines and/or markers.  
- **Why the name:** It “plots” data. Here you used it to draw the diagonal line (perfect predictions).

#### **`plt.hist()`**
- **What it does:** Draws a histogram.  
- **Why the name:** “Hist” for histogram.  
- **Parameters:** `bins`, `ec` (edge color), `rwidth` (relative bar width).

#### **`plt.title()`, `plt.xlabel()`, `plt.ylabel()`**
- Self‑explanatory: set title and axis labels.

#### **`plt.show()`**
- **What it does:** Displays all open figures.  
- **Why the name:** It “shows” the plots.

### **Pandas functions**

#### **`pd.read_csv()`**
- **What it does:** Reads a comma‑separated values file into a DataFrame.  
- **Why the name:** “read” a “csv” file.

#### **`data.describe()`**
- **What it does:** Generates descriptive statistics (count, mean, std, min, quartiles, max).  
- **Why the name:** It “describes” the data.

#### **`data.isna()`**
- **What it does:** Returns a boolean DataFrame where True indicates a missing (NaN) value.  
- **Why the name:** “is na” stands for “is not available” (i.e., missing).

#### **`data.duplicated()`**
- **What it does:** Identifies duplicate rows.  
- **Why the name:** Checks for “duplicated” rows.

#### **`.values`**
- **What it does:** Converts a pandas Series or DataFrame to a NumPy array.  
- **Why the name:** It returns the underlying “values”.

#### **`.reshape()`**
- **What it does:** Changes the shape of a NumPy array without changing its data.  
- **Why the name:** “Re‑shape” the array dimensions.

### **NumPy functions**

#### **`np.log()`**
- **What it does:** Computes the natural logarithm element‑wise.  
- **Why the name:** “log” is the standard mathematical notation for logarithm.

#### **`np.exp()`**
- **What it does:** Computes the exponential (e^x) element‑wise.  
- **Why the name:** “exp” stands for exponential.

#### **`np.e`**
- **What it does:** The mathematical constant e (Euler's number).  
- **Why the name:** “e” is the standard symbol for Euler's number.

### **Plotly Express**

#### **`px.bar()`**
- **What it does:** Creates an interactive bar chart.  
- **Why the name:** “px” is the alias for plotly express, “bar” indicates a bar chart.  
- **Parameters:** `x` (categories), `y` (values), `color` (to colour bars), `title`, etc.

#### **`.update_layout()`**
- **What it does:** Modifies the layout of a plotly figure (axis titles, legend, etc.).  
- **Why the name:** “update” the “layout” of the figure.

#### **`.show()`**
- **What it does:** Displays the interactive plotly figure.  
- **Why the name:** Shows the plot.

---

## Why All Those Underscores and Dots?

- **`_` (underscore) at the end of attributes** (like `.coef_`): In scikit‑learn, this indicates that the attribute is **estimated from the data** during `.fit()`. It's a convention to avoid conflicts with user‑set parameters.  
- **`.` (dot) notation**: Used to access methods and attributes of objects. For example, `regr.fit()` calls the `fit` method of the `regr` object.  
- **`sns` and `plt`**: These are aliases (shortcuts) for the libraries, making code shorter: `import seaborn as sns`, `import matplotlib.pyplot as plt`.

---

## Final Thoughts

You've now built a complete machine learning pipeline: data exploration → preprocessing → model training → evaluation → improvement → prediction. Every function you used has a meaningful name that hints at its purpose. With practice, these names will become second nature.

