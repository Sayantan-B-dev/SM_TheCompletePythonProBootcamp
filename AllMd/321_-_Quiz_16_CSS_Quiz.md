### CSS Professional Competency Quiz

This quiz is designed to test logic, specificity, and modern layout techniques. You can copy this directly into your Markdown files for study or internal training.

---

#### Section 1: The Box Model and Layout Logic

**Q1: What is the total calculated width of the element based on the following code?**

```css
/* Logic: Box-sizing is set to border-box by default in many resets, 
   but the browser default is content-box. */
.container {
    width: 300px;
    padding: 20px;
    border: 5px solid black;
    margin: 10px;
    box-sizing: content-box; 
}

```

* A) 300px
* B) 325px
* C) 350px
* D) 370px

> **Correct Answer: C**
> **Explanation**: Under `content-box`, the total width = `width` + `left padding` + `right padding` + `left border` + `right border`.
> Calculation: . Margins are outside the box and do not affect its width.

---

**Q2: Which Flexbox property is used to align items along the cross-axis?**

* A) `justify-content`
* B) `align-items`
* C) `flex-direction`
* D) `align-content`

> **Correct Answer: B**
> **Explanation**: `justify-content` handles the main-axis (usually horizontal), while `align-items` handles the cross-axis (usually vertical).

---

#### Section 2: Specificity and Cascade

**Q3: Given the following HTML and CSS, what color will the text "Hello World" be?**

**HTML:**

```html
<div id="sidebar" class="widget">
    <p class="text" style="color: green;">Hello World</p>
</div>

```

**CSS:**

```css
#sidebar .text { color: red; }
.widget .text { color: blue; }
p { color: orange !important; }

```

* A) Red
* B) Blue
* C) Green
* D) Orange

> **Correct Answer: D**
> **Explanation**: Although inline styles (Green) usually beat external CSS, the `!important` flag (Orange) overrides everything regardless of specificity or location.

---

#### Section 3: Modern CSS Features

**Q4: What is the primary difference between CSS Grid and Flexbox?**

* A) Grid is for small components, Flexbox is for page layouts.
* B) Grid is 2-dimensional (rows and columns), Flexbox is 1-dimensional (rows or columns).
* C) Flexbox is older and no longer used in professional environments.
* D) Grid requires external libraries like Bootstrap, while Flexbox is native.

> **Correct Answer: B**
> **Explanation**: Flexbox focuses on distributing space along a single axis. Grid allows you to define precise areas across both horizontal and vertical tracks simultaneously.

---

#### Section 4: Units and Responsiveness

**Q5: Which unit is relative to the font-size of the root element (html)?**

* A) `em`
* B) `px`
* C) `rem`
* D) `vh`

> **Correct Answer: C**
> **Explanation**: `rem` stands for "Root EM." Unlike `em`, which is relative to its parent element (leading to compounding issues), `rem` always references the base font size defined in the `<html>` tag.

---

### Professional Code Implementation Example

Use this snippet to demonstrate the **BEM (Block Element Modifier)** methodology and **Custom Variables** mentioned in your previous query.

```css
/* Logic: Using Design Tokens (Variables) for commercial benefit. 
   Allows for instant theme switching.
*/
:root {
    --primary-color: #007bff;
    --border-radius: 8px;
    --transition-speed: 0.3s;
}

/* Block: The Component */
.btn {
    padding: 10px 20px;
    border-radius: var(--border-radius);
    transition: background-color var(--transition-speed);
    border: none;
    cursor: pointer;
}

/* Modifier: A Variation */
.btn--primary {
    background-color: var(--primary-color);
    color: white;
}

/* Hover State Logic */
.btn--primary:hover {
    background-color: #0056b3;
}

/*
Expected Output:
A button with rounded corners and a blue background.
When hovered, it smoothly transitions to a darker blue over 0.3 seconds.
*/

```

---

### Practice Exercise: Specificity Scoring

Rank these selectors from **Lowest (1)** to **Highest (4)** specificity:

| Selector | Rank | Logic |
| --- | --- | --- |
| `div` | 1 | Element selector (lowest) |
| `.menu-item` | 2 | Class selector |
| `#main-nav .link` | 3 | ID + Class combination |
| Inline `style=""` | 4 | Applied directly to DOM node |