import os
import logging
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from email_service import EmailService
import email_validator  # optional, for email validation

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Email service instance
email_service = EmailService(
    smtp_server=os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
    smtp_port=int(os.getenv('SMTP_PORT', 587)),
    username=os.getenv('EMAIL_ADDRESS'),
    password=os.getenv('EMAIL_PASSWORD'),
    recipient=os.getenv('RECIPIENT_EMAIL')
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send-message', methods=['POST'])
def send_message():
    # Get form data (JSON or form-urlencoded)
    if request.is_json:
        data = request.json
    else:
        data = request.form

    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    phone = data.get('phone', '').strip()
    project_type = data.get('project_type', '').strip()
    budget = data.get('budget', '').strip()
    message = data.get('message', '').strip()

    # Basic validation
    if not name or not email or not message or not project_type or not budget:
        return jsonify({'success': False, 'message': 'Please fill in all required fields.'}), 400

    # Optional email format validation
    try:
        email_validator.validate_email(email)
    except Exception:
        return jsonify({'success': False, 'message': 'Please enter a valid email address.'}), 400

    # Send email
    success, msg = email_service.send_contact_email(name, email, phone, project_type, budget, message)

    if success:
        return jsonify({'success': True, 'message': msg})
    else:
        return jsonify({'success': False, 'message': msg}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)