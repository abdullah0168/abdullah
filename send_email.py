import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, redirect
import os

app = Flask(__name__)

EMAIL_ADDRESS = "your_email@example.com"  # Replace with your email
EMAIL_PASSWORD = "your_password"  # Replace with your email password

def send_email(name, email, message):
    subject = "New Contact Form Submission"
    body = f"Name: {name}\nEmail: {email}\nMessage: {message}"
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.route('/send_email.py', methods=['POST'])
def handle_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    
    if send_email(name, email, message):
        return redirect('/contact.html?success=true')
    else:
        return redirect('/contact.html?success=false')

@app.route('/list_files', methods=['GET'])
def list_files():
    files = []
    for root, dirs, file_names in os.walk('.'):
        for file_name in file_names:
            if file_name.endswith(('.html', '.css', '.py')):
                files.append(os.path.join(root, file_name))
    return {'files': files}

if __name__ == '__main__':
    app.run(debug=True)