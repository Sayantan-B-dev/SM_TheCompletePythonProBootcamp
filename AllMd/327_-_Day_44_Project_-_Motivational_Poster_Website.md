# COMPLETE CSS KNOWLEDGE TREE — ADVICE, BEST PRACTICES, HABITS, AND FULL PROPERTY MAP

## 1. PROFESSIONAL CSS MINDSET AND ENGINEERING HABITS

### 1.1 Core Mental Models (How Professionals Think About CSS)

* CSS is a **constraint-based layout and rendering engine**, not a painting tool.
* CSS is resolved through **cascade → specificity → inheritance → computed values → layout → paint → composite**.
* Every CSS change must be evaluated for **scope, side effects, and long-term maintainability**.
* CSS should behave like **configuration**, not ad-hoc styling.

### 1.2 Non-Negotiable Professional Habits

* Never style without inspecting computed values in DevTools.
* Never hardcode values that should be tokens.
* Never fight the cascade; understand and design it.
* Never rely on visual coincidence; rely on rules.
* Never guess layout behavior; always verify box model resolution.
* Never mix concerns between layout, typography, color, and interaction.
* Never overuse `!important`; treat it as a design failure indicator.
* Always design for accessibility first, aesthetics second.
* Always expect CSS to scale to hundreds of components.

---

## 2. GLOBAL CSS ARCHITECTURE BEST PRACTICES

### 2.1 Foundational Setup (Must Exist in Every Project)

```css
*,
*::before,
*::after {
  box-sizing: border-box;
}

:root {
  font-size: 100%;
}
```

* Guarantees predictable sizing behavior.
* Respects user accessibility preferences.
* Prevents cumulative layout bugs.

---

### 2.2 Token-Based Design System (Mandatory at Scale)

```css
:root {
  --color-primary: hsl(220, 90%, 55%);
  --font-size-base: 1rem;
  --space-md: 1rem;
}
```

* All colors, fonts, spacing, and motion must originate from tokens.
* Components must **consume**, never **define**, core values.

---

## 3. COMPLETE CSS PROPERTY TREE (WITH EXAMPLES)

```
CSS
├── Layout & Box Model
│   ├── display
│   │   ├── display(block)
│   │   ├── display(inline)
│   │   ├── display(inline-block)
│   │   ├── display(flex)
│   │   ├── display(grid)
│   │   └── display(none)
│   │
│   ├── box-sizing
│   │   ├── box-sizing(content-box)
│   │   └── box-sizing(border-box)
│   │
│   ├── width / height
│   │   ├── width(300px)
│   │   ├── width(50%)
│   │   ├── min-width(320px)
│   │   ├── max-width(1200px)
│   │   ├── height(auto)
│   │   └── aspect-ratio(16 / 9)
│   │
│   ├── margin
│   │   ├── margin(16px)
│   │   ├── margin(16px 32px)
│   │   ├── margin-top(8px)
│   │   ├── margin-inline(auto)
│   │   └── margin-block(1rem)
│   │
│   ├── padding
│   │   ├── padding(12px)
│   │   ├── padding(8px 16px)
│   │   ├── padding-inline(1rem)
│   │   └── padding-block(0.75rem)
│   │
│   ├── border
│   │   ├── border(1px solid red)
│   │   ├── border-width(2px 4px)
│   │   ├── border-style(dashed)
│   │   ├── border-color(#333)
│   │   └── border-radius(8px)
│   │
│   ├── outline
│   │   ├── outline(2px solid blue)
│   │   └── outline-offset(2px)
│   │
│   └── overflow
│       ├── overflow(hidden)
│       ├── overflow-x(auto)
│       └── overflow-y(scroll)
│
├── Positioning
│   ├── position
│   │   ├── position(static)
│   │   ├── position(relative)
│   │   ├── position(absolute)
│   │   ├── position(fixed)
│   │   └── position(sticky)
│   │
│   ├── inset
│   │   ├── top(0)
│   │   ├── right(0)
│   │   ├── bottom(0)
│   │   ├── left(0)
│   │   └── inset(0)
│   │
│   └── z-index
│       ├── z-index(1)
│       └── z-index(auto)
│
├── Flexbox
│   ├── flex-direction(row | column)
│   ├── flex-wrap(wrap)
│   ├── justify-content(space-between)
│   ├── align-items(center)
│   ├── gap(1rem)
│   ├── flex-grow(1)
│   ├── flex-shrink(0)
│   └── flex-basis(auto)
│
├── Grid
│   ├── grid-template-columns(1fr 2fr)
│   ├── grid-template-rows(auto)
│   ├── grid-template-areas("a b")
│   ├── grid-column(1 / 3)
│   ├── grid-row(2 / 4)
│   ├── place-items(center)
│   └── gap(16px)
│
├── Typography
│   ├── font-family("Inter", system-ui)
│   ├── font-size(1rem)
│   ├── font-weight(400 | 700)
│   ├── font-style(italic)
│   ├── font-stretch(condensed)
│   ├── line-height(1.6)
│   ├── letter-spacing(0.05em)
│   ├── word-spacing(0.1em)
│   ├── text-align(center)
│   ├── text-transform(uppercase)
│   ├── text-decoration(underline)
│   ├── text-overflow(ellipsis)
│   ├── white-space(nowrap)
│   └── caret-color(currentColor)
│
├── Color & Painting
│   ├── color(var(--color-text))
│   ├── background-color(#fff)
│   ├── background-image(linear-gradient)
│   ├── background-size(cover)
│   ├── background-position(center)
│   ├── opacity(0.8)
│   ├── box-shadow(0 4px 12px rgba)
│   └── filter(blur(4px))
│
├── Interaction & States
│   ├── cursor(pointer)
│   ├── pointer-events(none)
│   ├── user-select(none)
│   ├── accent-color(var(--color-primary))
│   └── appearance(none)
│
├── Transforms & Motion
│   ├── transform(translateX)
│   ├── transform(scale)
│   ├── transform(rotate)
│   ├── transition(all 200ms ease)
│   ├── animation(slide-in)
│   ├── animation-duration(300ms)
│   └── will-change(transform)
│
├── Visibility & Rendering
│   ├── visibility(hidden)
│   ├── display(none)
│   ├── content-visibility(auto)
│   ├── contain(layout)
│   └── isolation(isolate)
│
├── Lists & Tables
│   ├── list-style(none)
│   ├── list-style-position(inside)
│   ├── border-collapse(collapse)
│   └── table-layout(fixed)
│
├── Pseudo-Classes
│   ├── :hover
│   ├── :focus
│   ├── :focus-visible
│   ├── :active
│   ├── :disabled
│   └── :nth-child(2n)
│
├── Pseudo-Elements
│   ├── ::before
│   ├── ::after
│   ├── ::placeholder
│   └── ::selection
│
└── Media & Queries
    ├── @media (min-width: 768px)
    ├── @media (prefers-color-scheme: dark)
    ├── @supports (display: grid)
    └── @container (min-width: 400px)
```

---

## 4. UNIVERSAL CSS DO AND DO NOT RULES

### Always Do

* Use `rem` for font sizes and spacing.
* Use `em` only for component-relative scaling.
* Use `border-box` everywhere.
* Use semantic HTML before styling.
* Use DevTools for every layout decision.
* Use tokens and variables for every repeated value.
* Use `outline` for focus, not border.

### Never Do

* Never fix layout bugs with `!important`.
* Never hardcode colors, fonts, or spacing inside components.
* Never rely on pixel-perfect coincidence.
* Never style semantic meaning visually only.
* Never use fixed heights for text containers.
* Never mix layout systems randomly.

---

## 5. FINAL PROFESSIONAL PRINCIPLE

CSS mastery is achieved when every property you write is intentional, scoped, inspectable, and reversible. When CSS is structured as a system of rules instead of scattered declarations, layouts become predictable, accessible, performant, and resilient at any scale without breaking under future change.
