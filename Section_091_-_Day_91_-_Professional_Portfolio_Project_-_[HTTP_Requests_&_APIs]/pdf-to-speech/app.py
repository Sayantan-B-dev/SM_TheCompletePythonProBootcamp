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

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-this')

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

tasks = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_file_size(size_bytes):
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes/1024:.1f} KB"
    else:
        return f"{size_bytes/(1024*1024):.1f} MB"

def format_duration(seconds):
    if seconds < 60:
        return f"{seconds:.0f} sec"
    elif seconds < 3600:
        return f"{seconds/60:.1f} min"
    else:
        return f"{seconds/3600:.1f} hours"

def extract_text_from_pdf(pdf_path, task_id):
    text = ""
    reader = PdfReader(pdf_path)
    total_pages = len(reader.pages)
    tasks[task_id]['total_pages'] = total_pages
    tasks[task_id]['total_bytes'] = os.path.getsize(pdf_path)

    for i, page in enumerate(reader.pages):
        if tasks[task_id].get('cancel_requested'):
            return None  # cancelled
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
            tasks[task_id]['text_length'] = len(text)
            tasks[task_id]['pages_processed'] = i + 1
            tasks[task_id]['est_duration'] = len(text) / 15
            tasks[task_id]['progress'] = int((i + 1) / total_pages * 40)
            tasks[task_id]['status'] = f"Extracting page {i+1}/{total_pages}..."
        time.sleep(0.05)  # small delay to make progress visible
    return text

def text_to_speech(text, output_filename):
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save(output_filename)

def process_pdf_task(task_id, pdf_path, original_filename):
    try:
        tasks[task_id]['progress'] = 5
        tasks[task_id]['status'] = "Starting..."

        # Step 1: Extract text
        text = extract_text_from_pdf(pdf_path, task_id)
        if text is None:  # cancelled
            tasks[task_id]['error'] = "Cancelled by user"
            tasks[task_id]['progress'] = 100
            tasks[task_id]['completed'] = True
            os.remove(pdf_path)
            return
        if not text.strip():
            tasks[task_id]['error'] = 'No text could be extracted. The PDF might be scanned or image-based.'
            tasks[task_id]['progress'] = 100
            tasks[task_id]['completed'] = True
            return

        # Prepare output filename
        base = os.path.splitext(original_filename)[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        audio_filename = f"{base}_{timestamp}.mp3"
        audio_path = os.path.join(app.config['OUTPUT_FOLDER'], audio_filename)

        # Step 2: TTS in background thread
        tts_done = threading.Event()
        tts_error = None

        def do_tts():
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
        progress_messages = [
            "Processing audio waveform...",
            "Applying voice modulation...",
            "Adding natural pauses...",
            "Finalizing audio stream...",
            "Encoding MP3..."
        ]
        msg_index = 0
        while not tts_done.is_set():
            if tasks[task_id].get('cancel_requested'):
                tasks[task_id]['error'] = "Cancelled by user"
                tasks[task_id]['progress'] = 100
                tasks[task_id]['completed'] = True
                # Optionally delete partial audio file
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                return

            # Increment progress slowly
            current = tasks[task_id]['progress']
            if current < 89:
                tasks[task_id]['progress'] = min(current + 1, 89)
                # Update status with varied messages
                tasks[task_id]['status'] = progress_messages[msg_index % len(progress_messages)]
                msg_index += 1
            time.sleep(0.8)  # adjust for desired animation speed

        # TTS finished
        if tts_error:
            tasks[task_id]['error'] = f"TTS failed: {tts_error}"
            tasks[task_id]['progress'] = 100
            tasks[task_id]['completed'] = True
            return

        if tasks[task_id].get('cancel_requested'):
            return

        # Get final file info
        audio_size = os.path.getsize(audio_path)
        try:
            audio = MP3(audio_path)
            actual_duration = audio.info.length
        except:
            actual_duration = tasks[task_id]['est_duration']

        tasks[task_id]['audio_file'] = audio_filename
        tasks[task_id]['audio_size'] = audio_size
        tasks[task_id]['actual_duration'] = actual_duration
        tasks[task_id]['progress'] = 100
        tasks[task_id]['status'] = "Done!"

        # Cleanup
        os.remove(pdf_path)

    except Exception as e:
        tasks[task_id]['error'] = str(e)
    finally:
        tasks[task_id]['completed'] = True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'pdf_file' not in request.files:
        flash('No file part')
        return redirect(url_for('index'))
    file = request.files['pdf_file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        task_id = uuid.uuid4().hex
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

        filename = secure_filename(file.filename)
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{task_id}_{filename}")
        file.save(pdf_path)

        thread = threading.Thread(target=process_pdf_task, args=(task_id, pdf_path, filename))
        thread.daemon = True
        thread.start()

        return redirect(url_for('progress', task_id=task_id))
    else:
        flash('Allowed file type is PDF')
        return redirect(url_for('index'))

@app.route('/progress/<task_id>')
def progress(task_id):
    if task_id not in tasks:
        flash('Invalid task ID')
        return redirect(url_for('index'))
    return render_template('progress.html', task_id=task_id)

@app.route('/api/progress/<task_id>')
def api_progress(task_id):
    if task_id not in tasks:
        return jsonify({'error': 'Task not found'}), 404
    task = tasks[task_id]
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
    if task_id in tasks:
        tasks[task_id]['cancel_requested'] = True
        return jsonify({'success': True})
    return jsonify({'error': 'Task not found'}), 404

@app.route('/result/<task_id>')
def result(task_id):
    if task_id not in tasks:
        flash('Task not found')
        return redirect(url_for('index'))
    task = tasks[task_id]
    if task['error']:
        flash(f"Conversion failed: {task['error']}")
        return redirect(url_for('index'))
    if not task['audio_file']:
        flash('Conversion not completed yet')
        return redirect(url_for('progress', task_id=task_id))
    return render_template('result.html', task=task, task_id=task_id)

@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, threaded=True)