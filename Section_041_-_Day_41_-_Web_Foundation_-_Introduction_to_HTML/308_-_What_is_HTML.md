## What HTML Is in Web Development

**HTML (HyperText Markup Language)** is a declarative markup language used to describe the structure, meaning, and hierarchy of content on the World Wide Web. It does not define application logic or behavior, but instead defines **what content exists** and **how that content is semantically organized** so that browsers, search engines, assistive technologies, and other tools can interpret it consistently.

HTML documents are parsed by web browsers into a **Document Object Model (DOM)**, which becomes the foundation upon which styling (CSS) and behavior (JavaScript) are applied.

---

## Meaning of HyperText

**HyperText** refers to text that contains embedded references, called hyperlinks, which allow navigation between documents or different sections within the same document.

Key properties of hypertext systems include:

* Textual content that is non-linear and allows branching navigation paths.
* Embedded references that point to other resources using addresses called URLs.
* User-driven traversal rather than fixed sequential reading order.

In HTML, hypertext is primarily implemented using the `<a>` anchor tag, which connects documents across the web into an interconnected information graph.

---

## Meaning of Markup Language

A **Markup Language** is a system for annotating text with tags that provide metadata about structure, semantics, or presentation, without being part of the text’s actual content.

Core characteristics of markup languages include:

* Tags that surround content to describe its role or meaning.
* Human-readable syntax that can be authored and reviewed easily.
* Machine-readable structure that can be parsed deterministically.

Markup languages describe **what something is**, not **what to do**, which distinguishes them from programming languages.

---

## Why HTML Is a Markup Language and Not a Programming Language

HTML lacks features required for computation or control flow, which defines why it is not a programming language.

| Capability        | HTML Behavior Description                                |
| ----------------- | -------------------------------------------------------- |
| Variables         | Not supported, content is static or externally generated |
| Conditional logic | Not supported natively                                   |
| Loops             | Not supported natively                                   |
| Functions         | Not supported                                            |
| Execution model   | Parsed, not executed                                     |

HTML strictly describes document structure and semantics, leaving logic and computation to JavaScript or server-side languages.

---

## Core Building Blocks of HTML

### HTML Elements

An **HTML element** consists of a start tag, optional content, and an optional end tag, forming a semantic unit.

```html
<p>This paragraph represents a block of textual content.</p>
```

Expected Output in Browser Rendering:

```
This paragraph represents a block of textual content.
```

---

### HTML Tags

**Tags** are syntactic markers enclosed in angle brackets that define the role of content.

* Opening tags define where an element begins.
* Closing tags define where an element ends.
* Void tags represent elements without content.

```html
<img src="photo.jpg" alt="Sample image">
```

Expected Output in Browser Rendering:

```
An image is displayed at the specified location.
```

---

### HTML Attributes

**Attributes** provide additional metadata or configuration for elements.

```html
<a href="https://example.com" target="_blank">Visit Example</a>
```

Expected Output in Browser Rendering:

```
A clickable hyperlink that opens in a new browser tab.
```

---

## Categories of HTML Tags

### Structural and Document-Level Tags

These tags define the global structure of the document.

| Tag       | Purpose Description                        |
| --------- | ------------------------------------------ |
| `<html>`  | Root container of the entire HTML document |
| `<head>`  | Metadata container not rendered visually   |
| `<body>`  | Container for all visible page content     |
| `<title>` | Defines the browser tab title              |

---

### Text and Content Semantics Tags

These tags describe the meaning and role of textual content.

| Tag            | Semantic Meaning                                  |
| -------------- | ------------------------------------------------- |
| `<h1>`–`<h6>`  | Hierarchical headings defining content importance |
| `<p>`          | Paragraph of prose content                        |
| `<strong>`     | Strong importance, not just visual boldness       |
| `<em>`         | Emphasized text with semantic stress              |
| `<blockquote>` | Quoted external content                           |

---

### Grouping and Layout Tags

These tags group content for structure and styling purposes.

| Tag         | Usage Context                                          |
| ----------- | ------------------------------------------------------ |
| `<div>`     | Generic block-level container without semantic meaning |
| `<span>`    | Generic inline container for small content regions     |
| `<section>` | Thematically related content grouping                  |
| `<article>` | Self-contained, reusable content unit                  |
| `<nav>`     | Navigation-related content                             |

---

### Media and Embedded Content Tags

These tags embed external or rich media resources.

| Tag        | Purpose Description                       |
| ---------- | ----------------------------------------- |
| `<img>`    | Embeds images                             |
| `<audio>`  | Embeds audio playback                     |
| `<video>`  | Embeds video playback                     |
| `<iframe>` | Embeds external documents or applications |

---

### Forms and User Input Tags

These tags define interactive data entry interfaces.

| Tag          | Role Description                  |
| ------------ | --------------------------------- |
| `<form>`     | Container for user-submitted data |
| `<input>`    | Single-line input control         |
| `<textarea>` | Multi-line text input             |
| `<select>`   | Dropdown selection input          |
| `<button>`   | Clickable action trigger          |

---

## Examples of Complete HTML Document

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Basic HTML Example</title>
  </head>
  <body>
    <h1>Main Heading</h1>
    <p>This paragraph explains the purpose of the document.</p>
    <a href="https://example.com">Learn more</a>
  </body>
</html>
```

Expected Output in Browser Rendering:

```
A webpage displaying a heading, a paragraph, and a clickable link.
```

---

## Other Markup Languages and Their Purposes

### XML (Extensible Markup Language)

XML focuses on data transport and storage rather than presentation.

```xml
<user>
  <name>Sayantan</name>
  <role>Developer</role>
</user>
```

Expected Output Interpretation:

```
Structured data representation intended for machine processing.
```

---

### XHTML (Extensible HyperText Markup Language)

XHTML enforces strict XML rules on HTML syntax.

```html
<br />
<img src="icon.png" alt="Icon" />
```

Expected Output Interpretation:

```
HTML rendered using XML-compliant syntax rules.
```

---

### SVG (Scalable Vector Graphics)

SVG describes vector-based graphical content using markup.

```xml
<svg width="100" height="100">
  <circle cx="50" cy="50" r="40" />
</svg>
```

Expected Output in Browser Rendering:

```
A scalable circular vector graphic rendered without pixel loss.
```

---

### MathML (Mathematical Markup Language)

MathML encodes mathematical notation for accurate rendering and accessibility.

```xml
<math>
  <mi>x</mi>
  <mo>=</mo>
  <mn>5</mn>
</math>
```

Expected Output Interpretation:

```
Mathematical expression rendered as formatted math notation.
```

---

### Markdown

Markdown is a lightweight markup language optimized for readability and quick authoring.

```markdown
# Heading
This is **bold** text.
```

Expected Output Interpretation:

```
A heading followed by a paragraph with emphasized text.
```

---

## Summary Table of Markup Languages

| Language | Primary Use Case                                | Human Readability | Browser Rendering |
| -------- | ----------------------------------------------- | ----------------- | ----------------- |
| HTML     | Web document structure and semantics            | High              | Native            |
| XML      | Data exchange and configuration                 | Medium            | Indirect          |
| XHTML    | Strict HTML with XML rules                      | Medium            | Native            |
| SVG      | Vector graphics                                 | Medium            | Native            |
| MathML   | Mathematical notation                           | Low               | Native            |
| Markdown | Documentation and lightweight content authoring | Very High         | Converted         |
