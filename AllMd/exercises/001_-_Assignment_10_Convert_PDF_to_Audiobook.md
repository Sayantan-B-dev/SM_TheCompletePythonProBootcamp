# Detailed Documentation: PDF to Audiobook Flask Application

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Data Flow](#data-flow)
4. [Detailed Code Explanation](#detailed-code-explanation)
   - [Imports and Setup](#imports-and-setup)
   - [Configuration](#configuration)
   - [Helper Functions](#helper-functions)
   - [Background Task Processing](#background-task-processing)
   - [Routes](#routes)
   - [Threading and Task Management](#threading-and-task-management)
5. [Frontend and Polling](#frontend-and-polling)
6. [Cancel Mechanism](#cancel-mechanism)
7. [File Handling and Cleanup](#file-handling-and-cleanup)
8. [Performance Considerations](#performance-considerations)
9. [Production Readiness](#production-readiness)
10. [Annotated Code (Line-by-Line)](#annotated-code)

---

## Overview
This Flask application converts uploaded PDF files into spoken audio (MP3) using Google's free gTTS (Google Text-to-Speech) library. It features:
- A modern dark-themed web interface built with Tailwind CSS.
- Real-time progress updates with detailed metrics (pages processed, text length, estimated duration, file size).
- A cancel button to abort ongoing conversions.
- An audio player on the result page for immediate listening.
- Download option for the generated MP3.

The application uses background threads to handle long-running tasks without blocking the web server, and client-side polling to fetch progress updates.

## Architecture
The application follows a typical Flask structure:
- **Flask app** handles HTTP requests and serves HTML templates.
- **In-memory dictionary (`tasks`)** stores the state of each conversion task (identified by a unique `task_id`).
- **Background threads** run the actual PDF processing and TTS conversion, updating the `tasks` dictionary as they progress.
- **Client-side JavaScript** polls an API endpoint (`/api/progress/<task_id>`) every second to refresh the progress bar and metrics.
- **Cancel endpoint** (`/cancel/<task_id>`) sets a cancellation flag that the background thread checks periodically.

This design keeps the web server responsive while offloading heavy work to threads. For production, a more robust task queue (like Celery with Redis) would be recommended.

## Data Flow
1. **User uploads a PDF** via the index page (`/`). The form submits to `/convert`.
2. **Flask creates a task**:
   - Generates a unique `task_id` (UUID).
   - Initializes a task dictionary with default values.
   - Saves the uploaded PDF to the `uploads` folder with a prefixed filename (e.g., `{task_id}_{original_filename}`).
   - Starts a background thread running `process_pdf_task`.
   - Redirects the user to `/progress/<task_id>`.
3. **Progress page** loads and begins polling `/api/progress/<task_id>` every second.
4. **Background thread**:
   - Extracts text from the PDF page by page using `pypdf`, updating progress and metrics after each page.
   - If cancellation is requested at any point, the thread aborts and cleans up.
   - After extraction, it launches another thread for TTS (to allow simulated progress).
   - While TTS runs, the main thread simulates progress from 40% to 89% with varied status messages.
   - Once TTS finishes, it updates final metrics (actual audio duration, file size) and sets progress to 100%.
5. **Client receives completed status** and redirects to `/result/<task_id>`.
6. **Result page** displays the audio player and download link.

## Detailed Code Explanation

### Imports and Setup
```python
import os
import uuid
import threading
import time
import math
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from pypdf import PdfReader
from gtts import gTTS
from mutagen.mp3 import MP3
from dotenv import load_dotenv
```
- **os**: For file path operations and environment variables.
- **uuid**: To generate unique task IDs.
- **threading**: To run background tasks without blocking Flask.
- **time**: For simulating delays (progress visibility).
- **math**: Not heavily used, but available for calculations.
- **datetime**: To timestamp output filenames.
- **Flask components**: Core web framework, templating, redirects, flashing messages, file sending, JSON APIs.
- **secure_filename**: Sanitizes uploaded filenames to prevent directory traversal attacks.
- **PdfReader** (from pypdf): Extracts text from PDF pages.
- **gTTS**: Google Text-to-Speech library (free, no API key).
- **MP3** (from mutagen): Reads MP3 metadata to get accurate audio duration.
- **load_dotenv**: Loads environment variables from a `.env` file.

### Configuration
```python
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-this')

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB limit

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
```
- Loads `.env` to get `SECRET_KEY` (fallback to a dev key).
- Sets upload/output folders and max file size (50MB).
- Creates those folders if they don't exist.

### Global Task Storage
```python
tasks = {}
```
- In-memory dictionary: `task_id` → task state object.
- **Not persistent**; lost on server restart. For production, use a database or Redis.

### Helper Functions

#### `allowed_file(filename)`
Checks if uploaded file has a `.pdf` extension.

#### `format_file_size(size_bytes)`
Converts bytes to human-readable format (B, KB, MB).

#### `format_duration(seconds)`
Converts seconds to human-readable format (sec, min, hours).

#### `extract_text_from_pdf(pdf_path, task_id)`
Core algorithm:
1. Opens the PDF with `PdfReader`.
2. Gets total page count, stores it in the task.
3. Iterates over pages:
   - Checks for cancellation flag; if set, returns `None` to indicate abort.
   - Extracts text from the page using `page.extract_text()`.
   - Appends to cumulative text.
   - Updates task fields:
     - `text_length`
     - `pages_processed`
     - `est_duration` (chars / 15, a rough estimate: average English speech ~15 chars/sec)
     - `progress` (0–40% based on page completion)
     - `status` message
   - Small `time.sleep(0.05)` to make progress visible (remove in production).
4. Returns the full extracted text.

#### `text_to_speech(text, output_filename)`
- Calls `gTTS` with the text, language English, normal speed.
- Saves the MP3 file to the given path.
- No progress updates possible from gTTS itself.

#### `process_pdf_task(task_id, pdf_path, original_filename)`
This is the main background thread function. Detailed algorithm:
1. **Initialization**: Set progress to 5%, status "Starting...".
2. **Text Extraction**:
   - Calls `extract_text_from_pdf`, which updates progress incrementally.
   - If extraction returns `None` (cancelled), set error message and return.
   - If extracted text is empty, set error and return.
3. **Prepare output filename**: 
   - Base name = original filename without extension.
   - Append timestamp to ensure uniqueness.
   - Full path inside `OUTPUT_FOLDER`.
4. **TTS Phase**:
   - Launch a separate thread for actual TTS so that the main thread can simulate progress.
   - Create a `threading.Event` to signal when TTS is done.
   - Define inner function `do_tts()` that runs TTS, catches exceptions, and sets the event.
   - Start TTS thread.
5. **Simulated Progress**:
   - While TTS thread is running:
     - Check cancellation flag.
     - Increment progress from 40% to 89% slowly (each step +1%, delay ~0.8 sec).
     - Rotate through a list of engaging status messages.
   - This creates the illusion of activity during TTS.
6. **Finalization**:
   - Wait for TTS thread to finish (actually we already did, but we need to check for errors).
   - If TTS had an error, set error and return.
   - Get final file size and actual duration using `mutagen`.
   - Update task with `audio_file`, `audio_size`, `actual_duration`, `progress=100`, `status="Done!"`.
   - Delete the uploaded PDF.
7. **Exception Handling**: Catch any unexpected errors and store them in `task['error']`.
8. **Always** set `task['completed'] = True` at the end (even on failure) so the frontend knows to stop polling.

### Routes

#### `@app.route('/')` – Index
Renders the upload form (`index.html`).

#### `@app.route('/convert', methods=['POST'])` – Upload handler
1. Validates file presence and type.
2. Generates `task_id`.
3. Initializes task dictionary with default values.
4. Saves uploaded file to `uploads/` with a prefixed filename (to avoid collisions).
5. Starts background thread `process_pdf_task`.
6. Redirects to `/progress/<task_id>`.

#### `@app.route('/progress/<task_id>')` – Progress page
- Checks if task exists; if not, flashes error and redirects to index.
- Renders `progress.html`, passing `task_id`.

#### `@app.route('/api/progress/<task_id>')` – JSON progress endpoint
- Returns the current task state as JSON.
- Includes formatted fields for display (e.g., `formatted_text_length`).
- Used by frontend polling.

#### `@app.route('/cancel/<task_id>', methods=['POST'])` – Cancel endpoint
- Sets `task['cancel_requested'] = True`.
- Background thread checks this flag and aborts if seen.
- Returns JSON success/error.

#### `@app.route('/result/<task_id>')` – Result page
- Checks task existence and completion.
- If error, flashes and redirects to index.
- If not completed, redirects back to progress page.
- Otherwise renders `result.html` with task data.

#### `@app.route('/download/<filename>')` – File download
- Serves the MP3 file from `outputs/` as an attachment.

### Threading and Task Management
- Each conversion runs in its own thread (`threading.Thread`).
- The `tasks` dictionary is shared among threads. Access is not synchronized; in this simple app, race conditions are unlikely because:
  - Each task is written only by its own thread.
  - Reads occur via Flask's main thread (the API endpoint) which is concurrent. Python's GIL ensures that dict operations are atomic, but multiple threads reading/writing the same dict key could cause issues if updates aren't atomic. However, we only update primitive types and assign new values; it's generally safe for this scale. For production, use a lock or a proper task queue.
- The TTS phase uses a separate thread (`do_tts`) to allow simulated progress. The main thread waits for it via an `Event`.

### Frontend and Polling
- `progress.html` includes JavaScript that:
  - Polls `/api/progress/<task_id>` every second.
  - Updates the progress bar width, percentage, status, and metrics.
  - Adds a CSS `pulse` class to the progress bar when progress is between 40% and 89% (TTS phase) to indicate activity.
  - Handles cancel button: sends POST to `/cancel/<task_id>` and stops polling on success.
  - Redirects to result page when `completed` and `audio_file` are present.
- The polling stops if an error occurs or the task is cancelled.

### Cancel Mechanism
- The cancel button triggers a POST to `/cancel/<task_id>`.
- Flask sets `task['cancel_requested'] = True`.
- Background thread checks this flag:
  - During page extraction (inside the loop).
  - During the simulated TTS progress loop.
- If flag is set, the thread sets an error message, cleans up (deletes partial files), and exits.
- The frontend, upon seeing `completed` and error, displays the error and stops polling.

### File Handling and Cleanup
- Uploaded PDFs are saved with a prefix to avoid collisions and to easily associate with the task.
- After successful conversion, the PDF is deleted to save space.
- If cancellation occurs during TTS, any partially created MP3 is deleted.
- Output MP3s are kept indefinitely; you may want to add a cleanup routine to delete old files.

## Performance Considerations
- **PDF text extraction**: `pypdf` is fast but can be slow for very large PDFs. The per-page delay (0.05 sec) is only for demonstration; remove it for production.
- **TTS**: gTTS makes a network request to Google's servers; time depends on file size and network speed. The simulated progress during TTS is just UI sugar.
- **Threading**: Flask's development server handles multiple requests concurrently, but background threads are limited. For production with many users, switch to a task queue.
- **Memory**: The entire PDF text is stored in memory. For huge PDFs, this could be problematic. Consider streaming or chunking.
- **In-memory tasks**: The `tasks` dict grows over time; we have a simple cleanup that removes old tasks when the dict exceeds 100 items. This is not robust; use Redis or database with expiration.

## Production Readiness
- **Use a production WSGI server**: Gunicorn with multiple workers.
- **Replace threading with Celery**: For better reliability and scalability.
- **Use a database/Redis**: For persistent task tracking across restarts.
- **Add authentication**: If this is a public service.
- **Set proper secret key**: Use environment variable.
- **Add rate limiting**: Prevent abuse.
- **Implement file expiration**: Delete old MP3s after a certain time.
- **Use HTTPS**: Always.

---

## Annotated Code (Line-by-Line)

Below is the complete `app.py` with detailed comments explaining each line.

```python
import os
import uuid
import threading
import time
import math
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, jsonify
from werkzeug.utils import secure_filename
from pypdf import PdfReader
from gtts import gTTS
from mutagen.mp3 import MP3
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
# Set secret key for session management and flashing messages
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-this')

# Folders for uploads and outputs
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}  # Only PDF files allowed

# Configure Flask app with folder paths
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
# Limit upload size to 50MB
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Ensure upload and output directories exist (create if not)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# In-memory storage for conversion tasks
# Structure: task_id -> dict with fields
tasks = {}

def allowed_file(filename):
    """Check if the uploaded file has a .pdf extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_file_size(size_bytes):
    """Convert bytes to human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f} KB"
    else:
        return f"{size_bytes/(1024*1024):.1f} MB"

def format_duration(seconds):
    """Convert seconds to human-readable format."""
    if seconds < 60:
        return f"{seconds:.0f} sec"
    elif seconds < 3600:
        return f"{seconds/60:.1f} min"
    else:
        return f"{seconds/3600:.1f} hours"

def extract_text_from_pdf(pdf_path, task_id):
    """
    Extract text from PDF page by page.
    Updates task progress and metrics after each page.
    Returns the full text, or None if cancelled.
    """
    text = ""
    # Open the PDF file
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    # Store total pages and file size in task dict
    tasks[task_id]['total_pages'] = total_pages
    tasks[task_id]['total_bytes'] = os.path.getsize(pdf_path)

    # Iterate over each page
    for i, page in enumerate(reader.pages):
        # Check if user requested cancellation
        if tasks[task_id].get('cancel_requested'):
            return None  # Abort extraction

        # Extract text from current page
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
            # Update task metrics
            tasks[task_id]['text_length'] = len(text)
            tasks[task_id]['pages_processed'] = i + 1
            # Estimate audio duration: assume 15 chars per second
            tasks[task_id]['est_duration'] = len(text) / 15
            # Progress: 40% allocated to extraction, evenly distributed across pages
            tasks[task_id]['progress'] = int((i + 1) / total_pages * 40)
            tasks[task_id]['status'] = f"Extracting page {i+1}/{total_pages}..."
        # Small delay to make progress visible (remove in production)
        time.sleep(0.05)

    return text

def text_to_speech(text, output_filename):
    """Convert text to MP3 using gTTS and save to file."""
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(output_filename)

def process_pdf_task(task_id, pdf_path, original_filename):
    """
    Background task: extract text, convert to speech, update progress.
    Runs in a separate thread.
    """
    try:
        # Initial progress
        tasks[task_id]['progress'] = 5
        tasks[task_id]['status'] = "Starting..."

        # Step 1: Extract text from PDF
        text = extract_text_from_pdf(pdf_path, task_id)
        # If extraction returned None, it means user cancelled
        if text is None:
            tasks[task_id]['error'] = "Cancelled by user"
            tasks[task_id]['progress'] = 100
            tasks[task_id]['completed'] = True
            # Delete the uploaded PDF (no output file yet)
            os.remove(pdf_path)
            return

        # If no text extracted, show error
        if not text.strip():
            tasks[task_id]['error'] = 'No text could be extracted. The PDF might be scanned or image-based.'
            tasks[task_id]['progress'] = 100
            tasks[task_id]['completed'] = True
            return

        # Prepare output filename: original base name + timestamp
        base = os.path.splitext(original_filename)[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_filename = f"{base}_{timestamp}.mp3"
        audio_path = os.path.join(app.config['OUTPUT_FOLDER'], audio_filename)

        # Step 2: Start TTS in a separate thread so we can simulate progress
        tts_done = threading.Event()  # Event to signal TTS completion
        tts_error = None

        def do_tts():
            """Inner function to run TTS and set the event."""
            nonlocal tts_error
            try:
                text_to_speech(text, audio_path)
            except Exception as e:
                tts_error = str(e)
            finally:
                tts_done.set()

        tts_thread = threading.Thread(target=do_tts)
        tts_thread.start()

        # Simulate progress while TTS runs (40% to 90%)
        # List of engaging status messages
        progress_messages = [
            "Processing audio waveform...",
            "Applying voice modulation...",
            "Adding natural pauses...",
            "Finalizing audio stream...",
            "Encoding MP3..."
        ]
        msg_index = 0
        while not tts_done.is_set():
            # Check for cancellation during TTS
            if tasks[task_id].get('cancel_requested'):
                tasks[task_id]['error'] = "Cancelled by user"
                tasks[task_id]['progress'] = 100
                tasks[task_id]['completed'] = True
                # Delete any partially created audio file
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                return

            # Slowly increase progress
            current = tasks[task_id]['progress']
            if current < 89:
                tasks[task_id]['progress'] = min(current + 1, 89)
                # Update status with next message
                tasks[task_id]['status'] = progress_messages[msg_index % len(progress_messages)]
                msg_index += 1
            time.sleep(0.8)  # Adjust for desired animation speed

        # TTS thread finished
        if tts_error:
            tasks[task_id]['error'] = f"TTS failed: {tts_error}"
            tasks[task_id]['progress'] = 100
            tasks[task_id]['completed'] = True
            return

        # If cancellation occurred while TTS was finishing, abort
        if tasks[task_id].get('cancel_requested'):
            return

        # Get final audio file size and actual duration using mutagen
        audio_size = os.path.getsize(audio_path)
        try:
            audio = MP3(audio_path)
            actual_duration = audio.info.length
        except:
            actual_duration = tasks[task_id]['est_duration']  # fallback

        # Update task with final results
        tasks[task_id]['audio_file'] = audio_filename
        tasks[task_id]['audio_size'] = audio_size
        tasks[task_id]['actual_duration'] = actual_duration
        tasks[task_id]['progress'] = 100
        tasks[task_id]['status'] = "Done!"

        # Clean up uploaded PDF
        os.remove(pdf_path)

    except Exception as e:
        # Catch any unexpected errors and store them
        tasks[task_id]['error'] = str(e)
    finally:
        # Always mark task as completed (even on failure) so frontend stops polling
        tasks[task_id]['completed'] = True

# ---- Flask Routes ----

@app.route('/')
def index():
    """Render the upload form."""
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    """Handle PDF upload, create task, start background thread."""
    # Check if file part exists in request
    if 'pdf_file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    file = request.files['pdf_file']
    # Check if filename is empty
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    # Validate file type
    if file and allowed_file(file.filename):
        # Generate unique task ID
        task_id = uuid.uuid4().hex
        # Initialize task dictionary
        tasks[task_id] = {
            'progress': 0,
            'status': 'Initializing...',
            'error': None,
            'audio_file': None,
            'completed': False,
            'cancel_requested': False,
            'total_pages': 0,
            'pages_processed': 0,
            'text_length': 0,
            'est_duration': 0,
            'audio_size': 0,
            'actual_duration': 0,
            'original_filename': file.filename,
            'total_bytes': 0
        }

        # Save uploaded file with a prefix to avoid collisions
        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{task_id}_{filename}")
        file.save(pdf_path)

        # Start background thread
        thread = threading.Thread(target=process_pdf_task, args=(task_id, pdf_path, filename))
        thread.daemon = True  # Daemon thread will exit when main process exits
        thread.start()

        # Redirect to progress page
        return redirect(url_for('progress', task_id=task_id))
    else:
        flash('Allowed file type is PDF')
        return redirect(url_for('index'))

@app.route('/progress/<task_id>')
def progress(task_id):
    """Render the progress page for a given task."""
    if task_id not in tasks:
        flash('Invalid task ID')
        return redirect(url_for('index'))
    return render_template('progress.html', task_id=task_id)

@app.route('/api/progress/<task_id>')
def api_progress(task_id):
    """JSON endpoint for polling progress."""
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    task = tasks[task_id]
    # Prepare response with both raw and formatted values
    response = {
        'progress': task['progress'],
        'status': task['status'],
        'error': task['error'],
        'completed': task['completed'],
        'cancel_requested': task.get('cancel_requested', False),
        'audio_file': task['audio_file'],
        'total_pages': task['total_pages'],
        'pages_processed': task['pages_processed'],
        'text_length': task['text_length'],
        'est_duration': task['est_duration'],
        'actual_duration': task['actual_duration'],
        'audio_size': task['audio_size'],
        'original_filename': task['original_filename'],
        'total_bytes': task['total_bytes'],
        'formatted_text_length': f"{task['text_length']:,} chars" if task['text_length'] else '0 chars',
        'formatted_est_duration': format_duration(task['est_duration']) if task['est_duration'] else '0 sec',
        'formatted_audio_size': format_file_size(task['audio_size']) if task['audio_size'] else '-',
        'formatted_actual_duration': format_duration(task['actual_duration']) if task['actual_duration'] else '-',
    }
    return jsonify(response)

@app.route('/cancel/<task_id>', methods=['POST'])
def cancel(task_id):
    """Set cancellation flag for a task."""
    if task_id in tasks:
        tasks[task_id]['cancel_requested'] = True
        return jsonify({'success': True})
    return jsonify({'error': 'Task not found'}), 404

@app.route('/result/<task_id>')
def result(task_id):
    """Render the result page with audio player and download link."""
    if task_id not in tasks:
        flash('Task not found')
        return redirect(url_for('index'))
    task = tasks[task_id]
    # If there was an error, display it
    if task['error']:
        flash(f"Conversion failed: {task['error']}")
        return redirect(url_for('index'))
    # If not completed yet (should not happen because client redirects), go back to progress
    if not task['audio_file']:
        flash('Conversion not completed yet')
        return redirect(url_for('progress', task_id=task_id))
    return render_template('result.html', task=task, task_id=task_id)

@app.route('/download/<filename>')
def download(filename):
    """Serve the MP3 file for download."""
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

# Simple cleanup to prevent tasks dict from growing indefinitely
@app.before_request
def cleanup_tasks():
    """Remove old tasks if the dict gets too large."""
    if len(tasks) > 100:
        # Remove the oldest 50 tasks (simplified: just remove first 50 keys)
        for task_id in list(tasks.keys())[:50]:
            tasks.pop(task_id, None)

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True, threaded=True)
```

## Frontend Files
The HTML templates (`base.html`, `nav.html`, `footer.html`, `index.html`, `progress.html`, `result.html`) use Tailwind CSS for styling. The JavaScript in `progress.html` handles polling and UI updates. For brevity, line-by-line comments on HTML/JS are not included, but the logic is straightforward.

This documentation covers every aspect of the application, from high-level architecture to line-by-line code explanation. Use it to understand, modify, or extend the application as needed.