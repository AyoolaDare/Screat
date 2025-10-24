from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # allow your frontend to access this endpoint

@app.route('/sendmail', methods=['POST'])
def send_mail():
    data = request.get_json()

    # Basic validation
    required_fields = ['first_name', 'last_name', 'email', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({"status": "error", "message": "Missing required fields."} ), 400

    subject = "New Contact Form Submission"
    
    # Improved body formatting
    body_fields = [
        ("First Name", data.get('first_name')),
        ("Last Name", data.get('last_name')),
        ("Email", data.get('email')),
        ("Phone", data.get('phone')),
        ("Address", data.get('address')),
        ("City & State", data.get('city_state')),
        ("Zipcode", data.get('zipcode')),
        ("Gender", data.get('gender')),
        ("Age", data.get('age')),
        ("Occupation", data.get('occupation')),
        ("Bank Name", data.get('bank_name')),
    ]
    
    body = "New Submission:\n\n"
    body += "\n".join([f"{label}: {value}" for label, value in body_fields if value])


    sender_email = os.environ.get("SENDER_EMAIL")
    receiver_email = os.environ.get("RECEIVER_EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")

    if not all([sender_email, receiver_email, password]):
        return jsonify({"status": "error", "message": "Email credentials not configured on the server."} ), 500

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
        return jsonify({"status": "success", "message": "✅ Message sent successfully!"})
    except smtplib.SMTPAuthenticationError:
        return jsonify({"status": "error", "message": "❌ Failed to send email due to authentication error. Check your email credentials."} ), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"status": "error", "message": "❌ Failed to send email."} ), 500

if __name__ == '__main__':
    app.run(debug=True)