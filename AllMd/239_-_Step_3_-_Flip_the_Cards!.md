## 1. What “Window” Means in Tkinter (Exact Scope)

In Tkinter, the **window** usually refers to an instance of:

```python
tk.Tk()        # main application window
tk.Toplevel() # secondary windows
```

Both inherit from the same **Tk / Wm (Window Manager)** API.
Below is a **complete, practical catalog** of window-level methods and variables you actually use in real applications.

---

## 2. Window Creation & Identity

| Method / Variable     | Parameters | Returns         | Purpose                | Real Case Usage         |
| --------------------- | ---------- | --------------- | ---------------------- | ----------------------- |
| `tk.Tk()`             | none       | Tk object       | Create main app window | App entry point         |
| `tk.Toplevel(master)` | parent     | Toplevel object | Create child window    | Settings, dialogs       |
| `window.winfo_id()`   | none       | int             | OS window ID           | Advanced OS integration |
| `window.winfo_name()` | none       | str             | Tk internal name       | Debugging               |

---

## 3. Title, Icon, Visibility

| Method         | Parameters     | Returns | Meaning          | Real Usage            |
| -------------- | -------------- | ------- | ---------------- | --------------------- |
| `title()`      | `str`          | None    | Set window title | App branding          |
| `iconbitmap()` | path           | None    | Set window icon  | Professional look     |
| `iconphoto()`  | default, image | None    | PNG icon support | Cross-platform icons  |
| `deiconify()`  | none           | None    | Show window      | Restore minimized app |
| `iconify()`    | none           | None    | Minimize window  | Background mode       |
| `withdraw()`   | none           | None    | Hide window      | Splash screens        |

---

## 4. Size, Position, Geometry (Critical)

### `geometry()` (Most Important)

| Usage               | Meaning         |
| ------------------- | --------------- |
| `"800x600"`         | Width × height  |
| `"+200+100"`        | Position only   |
| `"800x600+200+100"` | Size + position |

### Table

| Method           | Parameters | Returns | Purpose            | Real Usage       |
| ---------------- | ---------- | ------- | ------------------ | ---------------- |
| `geometry()`     | string     | None    | Set/get size & pos | Initial layout   |
| `winfo_width()`  | none       | int     | Current width      | Responsive UI    |
| `winfo_height()` | none       | int     | Current height     | Canvas scaling   |
| `winfo_x()`      | none       | int     | X screen pos       | Custom centering |
| `winfo_y()`      | none       | int     | Y screen pos       | Multi-monitor    |

---

## 5. Window Resizing & Constraints

| Method        | Parameters                     | Returns | Meaning       | Usage            |
| ------------- | ------------------------------ | ------- | ------------- | ---------------- |
| `resizable()` | bool, bool                     | None    | Enable resize | Lock dialogs     |
| `minsize()`   | w, h                           | None    | Minimum size  | Prevent UI break |
| `maxsize()`   | w, h                           | None    | Maximum size  | Kiosk apps       |
| `aspect()`    | minNum, minDen, maxNum, maxDen | None    | Aspect ratio  | Media viewers    |

---

## 6. Window Focus & Stacking (Z-Order)

| Method                         | Parameters | Returns | Purpose        | Real Case        |
| ------------------------------ | ---------- | ------- | -------------- | ---------------- |
| `focus()`                      | none       | None    | Focus window   | Keyboard input   |
| `focus_force()`                | none       | None    | Force focus    | Modal dialogs    |
| `lift()`                       | none       | None    | Bring to front | Alerts           |
| `lower()`                      | none       | None    | Send back      | Background tools |
| `attributes("-topmost", bool)` | flag, bool | None    | Always on top  | Floating tools   |

---

## 7. Background, Cursor, Appearance

| Method            | Parameters  | Returns | Meaning           | Usage           |
| ----------------- | ----------- | ------- | ----------------- | --------------- |
| `configure(bg=)`  | color       | None    | Window background | Theme           |
| `cget("bg")`      | option      | value   | Read config       | Dynamic styling |
| `config(cursor=)` | cursor name | None    | Mouse cursor      | Drawing apps    |

---

## 8. Event Loop & Scheduling (Behavior Control)

| Method               | Parameters      | Returns | Purpose            | Usage            |
| -------------------- | --------------- | ------- | ------------------ | ---------------- |
| `mainloop()`         | none            | None    | Start app loop     | Required         |
| `update()`           | none            | None    | Force redraw       | Rare (dangerous) |
| `update_idletasks()` | none            | None    | Layout update only | Geometry calc    |
| `after()`            | ms, func, *args | id      | Schedule task      | Timers           |
| `after_cancel()`     | id              | None    | Cancel task        | Stop timers      |
| `after_idle()`       | func            | id      | Run when idle      | Deferred UI      |

---

## 9. Screen & System Information

| Method                 | Returns | Meaning              | Usage            |
| ---------------------- | ------- | -------------------- | ---------------- |
| `winfo_screenwidth()`  | int     | Screen width         | Center window    |
| `winfo_screenheight()` | int     | Screen height        | Fullscreen apps  |
| `winfo_fpixels()`      | float   | Pixels per unit      | DPI scaling      |
| `winfo_pixels()`       | int     | Pixels from distance | Precision layout |

---

## 10. Window State & Attributes

| Method                        | Parameters                         | Returns | Purpose            | Usage         |
| ----------------------------- | ---------------------------------- | ------- | ------------------ | ------------- |
| `state()`                     | `"normal"`, `"iconic"`, `"zoomed"` | None    | Window state       | Maximize      |
| `attributes()`                | key, value                         | None    | OS-level flags     | Transparency  |
| `attributes("-alpha", float)` | 0.0–1.0                            | None    | Opacity            | Fade effects  |
| `overrideredirect()`          | bool                               | None    | Remove decorations | Custom chrome |

---

## 11. Protocols (OS Events)

### `protocol()` (Extremely Important)

| Event                | Meaning      |
| -------------------- | ------------ |
| `"WM_DELETE_WINDOW"` | Close button |
| `"WM_TAKE_FOCUS"`    | Focus change |

### Example

```python
def on_close():
    print("Cleaning up")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
```

| Why | Prevent crashes, cancel timers, save data |

---

## 12. Clipboard & Selection

| Method               | Parameters | Returns | Usage           |
| -------------------- | ---------- | ------- | --------------- |
| `clipboard_clear()`  | none       | None    | Clear clipboard |
| `clipboard_append()` | text       | None    | Copy text       |
| `clipboard_get()`    | none       | str     | Paste           |

---

## 13. Variables Bound to Window (`tk.Variable`)

| Variable     | Type  | Use        |
| ------------ | ----- | ---------- |
| `StringVar`  | str   | Text state |
| `IntVar`     | int   | Counters   |
| `BooleanVar` | bool  | Toggles    |
| `DoubleVar`  | float | Sliders    |

### Example

```python
status = tk.StringVar(value="Ready")
label.config(textvariable=status)
```

---

## 14. Window Binding & Input

| Method       | Parameters  | Returns | Use              |
| ------------ | ----------- | ------- | ---------------- |
| `bind()`     | event, func | id      | Keyboard/mouse   |
| `unbind()`   | event       | None    | Remove binding   |
| `bind_all()` | event, func | id      | Global shortcuts |

---

## 15. Fullscreen & Kiosk Mode

| Method                            | Parameters | Use Case         |
| --------------------------------- | ---------- | ---------------- |
| `attributes("-fullscreen", True)` | bool       | Presentations    |
| `state("zoomed")`                 | none       | Desktop maximize |
| `overrideredirect(True)`          | none       | Kiosk terminals  |

---

## 16. Real-World Usage Mapping

| App Type      | Window Methods Used                |
| ------------- | ---------------------------------- |
| Desktop tool  | `geometry`, `minsize`, `after`     |
| Game          | `after`, `bind`, `attributes`      |
| Dashboard     | `state`, `lift`, `focus_force`     |
| Media app     | `aspect`, `fullscreen`, `alpha`    |
| Utility popup | `topmost`, `withdraw`, `deiconify` |

---

## 17. Critical Rules to Remember

* `Tk()` → one per app
* `Toplevel()` → many allowed
* Always cancel `after()` on close
* Avoid `update()` unless you know why
* Geometry + grid weights define behavior
* OS window manager ≠ Tk layout manager

---

## 18. Mental Model (Final)

> The window controls **existence, behavior, and time**.
> Widgets control **content**.
> Layout managers control **space**.

Mastering window methods is what turns a Tkinter script into a **real desktop application**.
