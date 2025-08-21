"""
Authentication routes for the Psychology Clinic Triage Tool
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import functools

# Create blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Mock user database - in a real application, this would be stored in a database
users = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'role': 'super_admin',
        'name': 'Super Admin'
    },
    'staff': {
        'password': generate_password_hash('staff123'),
        'role': 'triage_admin',
        'name': 'Triage Staff'
    }
}

# Login required decorator
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

# Super admin required decorator
def super_admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        if session.get('user_role') != 'super_admin':
            flash('You do not have permission to access this page.', 'error')
            return redirect(url_for('triage.index'))
        return view(**kwargs)
    return wrapped_view

# Login route
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if username not in users:
            error = 'Invalid username.'
        elif not check_password_hash(users[username]['password'], password):
            error = 'Invalid password.'

        if error is None:
            # Store user info in session
            session.clear()
            session['user_id'] = username
            session['user_role'] = users[username]['role']
            session['user_name'] = users[username]['name']
            
            # Redirect based on role
            if users[username]['role'] == 'super_admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('triage.index'))

        flash(error, 'error')

    return render_template('auth/login.html')

# Logout route
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

