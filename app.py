"""
Psychology Clinic Triage Tool
Main application entry point
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime

# Create Flask application
app = Flask(__name__, 
            static_folder='app/static',
            template_folder='app/templates')

# Configure application
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import routes after app is created to avoid circular imports
from app.routes import auth_routes, admin_routes, triage_routes

# Register blueprints
app.register_blueprint(auth_routes.bp)
app.register_blueprint(admin_routes.bp)
app.register_blueprint(triage_routes.bp)

# Root route redirects to login
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

