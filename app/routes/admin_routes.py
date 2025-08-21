"""
Admin routes for the Psychology Clinic Triage Tool
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
import os
import pandas as pd
import json
from datetime import datetime
from app.routes.auth_routes import super_admin_required, login_required

# Create blueprint
bp = Blueprint('admin', __name__, url_prefix='/admin')

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx', 'xls'}

# Helper function to process spreadsheet
def process_spreadsheet(file_path):
    """Process the uploaded spreadsheet and convert it to a JSON format for the database"""
    try:
        # Read the Excel file
        df = pd.read_excel(file_path)
        
        # Convert to dictionary format
        clinicians = []
        
        for _, row in df.iterrows():
            clinician = {}
            for column in df.columns:
                # Handle NaN values
                if pd.isna(row[column]):
                    clinician[column] = None
                else:
                    clinician[column] = row[column]
            
            clinicians.append(clinician)
        
        # Save to a JSON file
        json_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'clinicians.json')
        with open(json_path, 'w') as f:
            json.dump(clinicians, f, default=str)
        
        return True, f"Successfully processed {len(clinicians)} clinicians"
    
    except Exception as e:
        return False, f"Error processing spreadsheet: {str(e)}"

# Admin dashboard
@bp.route('/')
@super_admin_required
def dashboard():
    # Check if clinicians data exists
    json_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'clinicians.json')
    clinicians_exist = os.path.exists(json_path)
    
    if clinicians_exist:
        try:
            with open(json_path, 'r') as f:
                clinicians = json.load(f)
            last_updated = os.path.getmtime(json_path)
            last_updated = datetime.fromtimestamp(last_updated).strftime('%Y-%m-%d %H:%M:%S')
        except:
            clinicians = []
            last_updated = "Unknown"
    else:
        clinicians = []
        last_updated = "Never"
    
    return render_template('admin/dashboard.html', 
                           clinicians_exist=clinicians_exist,
                           clinician_count=len(clinicians),
                           last_updated=last_updated)

# Upload spreadsheet
@bp.route('/upload', methods=['GET', 'POST'])
@super_admin_required
def upload_spreadsheet():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            
            # Process the spreadsheet
            success, message = process_spreadsheet(file_path)
            
            if success:
                flash(message, 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash(message, 'error')
                return redirect(request.url)
        else:
            flash('Invalid file type. Please upload an Excel file (.xlsx or .xls)', 'error')
            return redirect(request.url)
    
    return render_template('admin/upload.html')

# Manage clinicians
@bp.route('/clinicians')
@super_admin_required
def manage_clinicians():
    # Load clinicians data
    json_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'clinicians.json')
    
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
                clinicians = json.load(f)
                
            # Group clinicians by location
            locations = {}
            for clinician in clinicians:
                location = clinician.get('primary_location', 'Unknown')
                if location not in locations:
                    locations[location] = []
                locations[location].append(clinician)
                
            # Sort locations alphabetically
            sorted_locations = sorted(locations.items())
                
        except Exception as e:
            flash(f"Error loading clinicians: {str(e)}", 'error')
            clinicians = []
            sorted_locations = []
    else:
        clinicians = []
        sorted_locations = []
    
    return render_template('admin/clinicians.html', 
                          clinicians=clinicians,
                          locations=sorted_locations)

# Update clinician availability
@bp.route('/clinicians/update', methods=['POST'])
@super_admin_required
def update_clinician():
    if request.method == 'POST':
        clinician_name = request.form.get('clinician_name')
        availability_status = request.form.get('availability_status')
        available_from_date = request.form.get('available_from_date')
        availability_notes = request.form.get('availability_notes')
        
        # Load clinicians data
        json_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'clinicians.json')
        
        if os.path.exists(json_path):
            try:
                with open(json_path, 'r') as f:
                    clinicians = json.load(f)
                
                # Update the clinician
                for clinician in clinicians:
                    if clinician['clinician_name'] == clinician_name:
                        clinician['availability_status'] = availability_status
                        clinician['available_from_date'] = available_from_date
                        clinician['availability_notes'] = availability_notes
                        break
                
                # Save the updated data
                with open(json_path, 'w') as f:
                    json.dump(clinicians, f, default=str)
                
                flash(f"Successfully updated availability for {clinician_name}", 'success')
            except Exception as e:
                flash(f"Error updating clinician: {str(e)}", 'error')
        else:
            flash("No clinicians data found. Please upload a spreadsheet first.", 'error')
        
        return redirect(url_for('admin.manage_clinicians'))

