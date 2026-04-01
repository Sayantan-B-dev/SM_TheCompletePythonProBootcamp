## How different programs talk to each other (even if written in different languages)

Programs do **not** talk directly.
They communicate through **well-defined system-level communication mechanisms** provided by the operating system, network stack, or standardized protocols.

Think of it as:

> *Programs don’t understand each other — they agree on a **language + channel***.

---

## 1. The core idea

Every inter-program communication needs **three things**:

| Component       | Meaning                            |
| --------------- | ---------------------------------- |
| **Channel**     | *How* data is transported          |
| **Protocol**    | *Rules* for sending/receiving data |
| **Data Format** | *Structure* of the data            |

As long as both programs agree on these, **language does not matter**.

---

## 2. Main communication methods (most to least common)

### 2.1 File-based communication

Programs communicate by **reading and writing files**.

```
Program A → writes file → Program B reads file
```

#### Why it works

* Files are OS-level objects
* Every language can read/write files

#### Example

* Python writes a JSON file
* Java reads the same JSON file

#### Data format usually used

* `JSON`
* `CSV`
* `XML`
* plain text

#### Python example

```python
# write_data.py
# Writes structured data to a file that any program can read

import json

data = {
    "user": "Alice",
    "score": 95
}

# Write data to file
with open("data.json", "w") as file:
    json.dump(data, file)
```

```python
# read_data.py
# Reads the same file written by another program

import json

with open("data.json", "r") as file:
    data = json.load(file)

print(data["user"], data["score"])
```

**Expected output**

```
Alice 95
```

---

### 2.2 Command-line (stdin / stdout)

Programs talk using **standard input/output streams**.

```
Program A → stdout → Program B stdin
```

Used heavily in:

* Linux pipelines
* Automation
* DevOps tooling

#### Example

```
python script.py | node consumer.js
```

#### Python example (producer)

```python
# producer.py
# Sends data through stdout

print("42")
```

#### Python example (consumer)

```python
# consumer.py
# Receives data from stdin

import sys

value = sys.stdin.read().strip()
print(int(value) * 2)
```

**Expected output**

```
84
```

---

### 2.3 Sockets (most powerful and common)

Programs communicate over **TCP/UDP** using sockets.

```
Program A ←→ Network Socket ←→ Program B
```

This is how:

* Browsers talk to servers
* Microservices communicate
* Games sync players

#### Why language doesn’t matter

Sockets send **bytes**, not Python or Java objects.

---

### 2.4 Client–Server example (Python ↔ any language)

#### Server (Python)

```python
# server.py
# TCP server that listens and responds

import socket

server = socket.socket()
server.bind(("localhost", 5000))
server.listen(1)

conn, addr = server.accept()

data = conn.recv(1024).decode()
print("Received:", data)

conn.send("Hello from Python".encode())
conn.close()
```

#### Client (could be Java, C++, JS, Python)

```python
# client.py
# TCP client that connects to server

import socket

client = socket.socket()
client.connect(("localhost", 5000))

client.send("Hello Server".encode())
response = client.recv(1024).decode()

print(response)
client.close()
```

**Expected output (client)**

```
Hello from Python
```

**Expected output (server)**

```
Received: Hello Server
```

---

### 2.5 HTTP / REST APIs (most common today)

Programs expose **endpoints**, others send requests.

```
Client → HTTP request → Server → HTTP response
```

Used by:

* Web apps
* Mobile apps
* Cloud systems

#### Universal rule

Every language can:

* Send HTTP requests
* Parse HTTP responses

---

### 2.6 Example: Python API server

```python
# api.py
# Minimal HTTP server using Flask

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/data")
def data():
    return jsonify({"message": "Hello world"})

app.run(port=5000)
```

#### Any language can do:

```
GET http://localhost:5000/data
```

**Expected response**

```json
{
  "message": "Hello world"
}
```

---

## 3. Data formats that enable communication

| Format      | Why used                  |
| ----------- | ------------------------- |
| JSON        | Human-readable, universal |
| XML         | Verbose but structured    |
| Protobuf    | Compact, fast             |
| MessagePack | Binary JSON               |
| Plain text  | Simplicity                |

---

## 4. How programs “understand” each other

They **don’t** understand logic — only structure.

Example:

```
{ "age": 25 }
```

Python sees → `dict`
Java sees → `Map`
C sees → raw bytes

**Meaning comes from agreement, not language**.

---

## 5. OS-level mechanisms

| Mechanism      | Used for               |
| -------------- | ---------------------- |
| Pipes          | Parent-child processes |
| Shared Memory  | High-speed IPC         |
| Message Queues | Async communication    |
| Signals        | Process control        |

---

## 6. Real-world analogy

| Program world | Human world     |
| ------------- | --------------- |
| Protocol      | Grammar         |
| Data format   | Language        |
| Socket        | Telephone       |
| HTTP          | Postal system   |
| File          | Shared notebook |

Two people don’t need the same brain —
they need the **same language and medium**.

---

## 7. One-sentence truth

> Programs don’t communicate by language — they communicate by **protocols, data formats, and shared channels**.
