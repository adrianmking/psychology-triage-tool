# Psychology Clinic Triage Tool

A web-based triage tool for psychology clinics to match clients with suitable clinicians based on various criteria.

## Features

- Secure login for admin and staff users
- Upload and manage clinician database via Excel spreadsheet
- Search for matching clinicians based on:
  - Age group
  - Presentation
  - Funding source
  - Location
- Manage clinician availability
- Type-ahead search for presentations
- Responsive design for all devices

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd psychology-triage-tool
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create an uploads directory:
   ```
   mkdir uploads
   ```

## Running the Application

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Access the application in your web browser at:
   ```
   http://localhost:5000
   ```

## Default Login Credentials

- Super Admin:
  - Username: admin
  - Password: admin123

- Triage Staff:
  - Username: staff
  - Password: staff123

## Usage

1. Log in using the provided credentials
2. Super Admin:
   - Upload the clinician spreadsheet
   - Manage clinician availability
3. Triage Staff:
   - Use the triage tool to find matching clinicians
   - Enter client details and search for matches

## Spreadsheet Format

The clinician spreadsheet should follow the format of the provided master spreadsheet, with columns for:
- Clinician information (name, profession, gender, etc.)
- Age groups treated
- Presentations treated
- Funding sources accepted
- Location information

## Deployment

For production deployment:

1. Set up a production WSGI server (e.g., Gunicorn):
   ```
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. Consider using a reverse proxy like Nginx for better performance and security

3. Update the secret key in app.py with a secure random key

4. Implement proper user authentication with a database instead of the mock users

