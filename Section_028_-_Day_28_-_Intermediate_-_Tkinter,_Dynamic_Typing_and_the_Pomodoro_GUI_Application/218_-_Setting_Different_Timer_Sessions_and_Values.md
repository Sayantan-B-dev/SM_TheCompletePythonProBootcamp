## Pomodoro Control Flow — Complete Mechanism-Level Explanation

---

## 1. High-Level Mental Model (Before Code)

The Pomodoro system here is a **state machine driven by time**.

There are only **three states**:

* **Work**
* **Short Break**
* **Long Break**

The system advances states automatically based on a counter called `reps`.

```
Start → Work → Short Break → Work → Short Break
      → Work → Short Break → Work → Long Break
      → repeat
```

No manual switching. Time completion triggers state transitions.

---

## 2. `reps` — The State Counter (Core Variable)

```python
global reps
reps += 1
```

### What `reps` represents

| `reps` value | Meaning            |
| ------------ | ------------------ |
| 1            | First work session |
| 2            | First short break  |
| 3            | Second work        |
| 4            | Second short break |
| 8            | Long break         |

`reps` is **not time-based**, it is **cycle-based**.

---

## 3. `start_timer()` — State Decision Engine

```python
def start_timer():
    global reps
    reps += 1
```

This function:

* Increments the session count
* Decides **which session comes next**
* Initializes the correct countdown

---

## 4. Long Break Condition (Highest Priority)

```python
if reps % 8 == 0:
    count_down_timer = LONG_BREAK_MIN * SECONDS_PER_MIN
    title_label.config(text="Long Break", fg=GREEN)
```

### Why `% 8`

* One full Pomodoro cycle = **8 reps**

  * 4 work sessions
  * 3 short breaks
  * 1 long break

`reps % 8 == 0` means:

* Every 8th session
* Always a **long break**

This condition is checked **first** because it is the most specific.

---

## 5. Short Break Condition

```python
elif reps % 2 == 0:
    count_down_timer = SHORT_BREAK_MIN * SECONDS_PER_MIN
    title_label.config(text="Short Break", fg=PINK)
```

### Why `% 2 == 0`

* Every **even rep** is a break
* Except those already caught by `% 8`

This captures:

* reps = 2, 4, 6

---

## 6. Work Session (Default Case)

```python
else:
    count_down_timer = WORK_MIN * SECONDS_PER_MIN
```

### Why `else`

* All **odd reps**
* Always work sessions
* Clean and predictable

---

## 7. Countdown Initialization

```python
countdown(count_down_timer)
```

At this point:

* Session type is decided
* Duration is calculated
* Countdown engine is started

`start_timer()` **never loops**, it only initializes.

---

## 8. `countdown(count)` — Time Engine

```python
def countdown(count):
```

This function:

* Receives remaining seconds
* Updates UI
* Reschedules itself
* Detects completion

---

## 9. Time Breakdown Logic

```python
count_min = count // 60
count_sec = count % 60
```

### Purpose

Convert raw seconds into display-friendly format.

---

## 10. Leading Zero Formatting (UI Precision)

```python
if count_min < 10:
    count_min = f"0{count_min}"
if count_sec < 10:
    count_sec = f"0{count_sec}"
```

Ensures:

```
05:09 instead of 5:9
```

This is **purely visual**, not logical.

---

## 11. Canvas Text Mutation (Live Update)

```python
canvas.itemconfig(
    canvas_timer_text,
    text=f"{count_min}:{count_sec}"
)
```

Key points:

* No new canvas items created
* Existing text object is modified
* Efficient and flicker-free

---

## 12. The Event Loop Recursion (Heartbeat)

```python
if count > 0:
    window.after(1000, countdown, count - 1)
```

### What actually happens

* Tkinter schedules the next call
* UI thread remains free
* Countdown continues asynchronously

This is **event-driven recursion**, not a loop.

---

## 13. Countdown Completion (Critical Moment)

```python
else:
    start_timer()
```

### Why `start_timer()` is called here

This is the **most important design decision**.

When `count == 0`:

* Current session is finished
* Control must move to the **next session**
* `start_timer()` decides *what comes next*

Without this call:

* Timer would stop permanently
* No state transition
* No automation

---

## 14. Session Reset UI Update

```python
title_label.config(text="Work", fg=RED)
```

This line:

* Prepares UI for upcoming work session
* Visual reset after break
* Does **not** affect logic

---

## 15. Control Flow Timeline (Exact Sequence)

### Example: First Work Session

```
Start button pressed
↓
start_timer() → reps = 1
↓
WORK session chosen
↓
countdown(1500)
↓
...
↓
countdown(0)
↓
start_timer() → reps = 2
↓
SHORT BREAK chosen
↓
countdown(300)
```

This loop continues **indefinitely**.

---

## 16. Why This Design Is Correct

| Design Choice             | Reason                      |
| ------------------------- | --------------------------- |
| `reps` counter            | Single source of truth      |
| `%` logic                 | Predictable session cycling |
| `after()`                 | Non-blocking UI             |
| `start_timer()` recursion | Automatic session chaining  |
| Canvas updates            | Efficient rendering         |

---

## 17. What Each Component Is Responsible For

| Component       | Responsibility   |
| --------------- | ---------------- |
| `start_timer()` | Session decision |
| `reps`          | State tracking   |
| `countdown()`   | Time flow        |
| `after()`       | Scheduling       |
| `canvas`        | Display          |
| `title_label`   | State indication |

No overlaps. No redundancy.

---

## 18. One Critical Insight (Mental Model)

> `countdown()` handles **time**
> `start_timer()` handles **state**

The app works because **time completion triggers state transition**, and state transition triggers a new time cycle.

This separation is what makes the Pomodoro logic clean, scalable, and bug-resistant.
