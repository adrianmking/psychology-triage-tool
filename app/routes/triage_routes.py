"""
Triage routes for the Psychology Clinic Triage Tool
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
import os
import json
from app.routes.auth_routes import login_required
import pandas as pd

# Create blueprint
bp = Blueprint('triage', __name__, url_prefix='/triage')

# Helper function to get all unique presentations from the clinicians data
def get_all_presentations():
    json_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'clinicians.json')
    
    if not os.path.exists(json_path):
        return []
    
    try:
        with open(json_path, 'r') as f:
            clinicians = json.load(f)
        
        # Extract all presentation columns
        presentation_columns = [col for col in clinicians[0].keys() if col.endswith('_treats')]
        
        # Remove the '_treats' suffix and replace underscores with spaces
        presentations = [col.replace('_treats', '').replace('_', ' ').title() for col in presentation_columns]
        
        return sorted(presentations)
    except:
        return []

# Helper function to get all age groups
def get_all_age_groups():
    return ['0-5 years', '6-12 years', '13-17 years', '18+ years']

# Helper function to get all funding sources
def get_all_funding_sources():
    return ['Private', 'MHCP', 'EAP', 'DVA', 'WorkCover', 'Other']

# Helper function to get all locations
def get_all_locations():
    return ['Sippy Downs', 'Caloundra', 'Flexible']

@bp.route('/')
@login_required
def index():
    presentations = get_all_presentations()
    age_groups = get_all_age_groups()
    funding_sources = get_all_funding_sources()
    locations = get_all_locations()
    
    return render_template('triage/index.html', 
                         presentations=presentations,
                         age_groups=age_groups,
                         funding_sources=funding_sources,
                         locations=locations)

@bp.route('/search', methods=['POST'])
@login_required
def search_clinicians(age_group, presentation, funding_source, location):
    json_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'clinicians.json')
    
    if not os.path.exists(json_path):
        flash('No clinician data available. Please upload the spreadsheet first.', 'error')
        return redirect(url_for('triage.index'))
    
    try:
        with open(json_path, 'r') as f:
            clinicians = json.load(f)
        
        # Convert presentation to column name format
        presentation_column = presentation.lower().replace(' ', '_') + '_treats'
        
        # Filter clinicians based on criteria
        matches = []
        
        # Load saved availability settings
        availability_settings = {}
        availability_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'availability.json')
        if os.path.exists(availability_path):
            try:
                with open(availability_path, 'r') as f:
                    availability_settings = json.load(f)
            except:
                pass  # If there's an error loading the file, just use empty settings
        
        for clinician in clinicians:
            # Skip if clinician is closed (marked as Unavailable or Closed)
            clinician_name = clinician.get('clinician_name')
            
            # Check if we have saved availability settings for this clinician
            if clinician_name in availability_settings:
                # Use the saved availability setting
                if availability_settings[clinician_name]['status'] == 'Closed':
                    continue
            else:
                # Fall back to spreadsheet availability if no saved setting
                if clinician.get('availability_status') == 'Unavailable' or clinician.get('availability_status') == 'Closed':
                    continue
            
            # STRICT LOCATION MATCHING: If a specific location is selected, only show clinicians from that location
            if location != "Flexible" and clinician.get('primary_location') != location:
                continue
            
            # STRICT PRESENTATION MATCHING: Check if clinician treats this specific presentation
            if presentation_column in clinician and clinician.get(presentation_column) != 'Y':
                continue
            
            # STRICT AGE GROUP MATCHING: Check if clinician treats this age group
            age_match = False
            if age_group == '0-5 years' and clinician.get('age_0_5') == 'Y':
                age_match = True
            elif age_group == '6-12 years' and clinician.get('age_6_12') == 'Y':
                age_match = True
            elif age_group == '13-17 years' and clinician.get('age_13_17') == 'Y':
                age_match = True
            elif age_group == '18+ years' and clinician.get('age_18_plus') == 'Y':
                age_match = True
            
            if not age_match:
                continue
            
            # STRICT FUNDING SOURCE MATCHING: Check if clinician accepts this funding source
            funding_match = False
            if funding_source == 'Private' and clinician.get('private_funding') == 'Y':
                funding_match = True
            elif funding_source == 'MHCP' and clinician.get('mhcp_funding') == 'Y':
                funding_match = True
            elif funding_source == 'EAP' and clinician.get('eap_funding') == 'Y':
                funding_match = True
            elif funding_source == 'DVA' and clinician.get('dva_funding') == 'Y':
                funding_match = True
            elif funding_source == 'WorkCover' and clinician.get('workcover_funding') == 'Y':
                funding_match = True
            elif funding_source == 'Other' and clinician.get('other_funding') == 'Y':
                funding_match = True
            
            if not funding_match:
                continue
            
            # If all criteria match, add to results
            matches.append(clinician)
        
        # Sort matches by availability percentage (highest first)
        matches.sort(key=lambda x: float(x.get('availability_percentage', 0)), reverse=True)
        
        return render_template('triage/results.html', 
                             matches=matches,
                             search_criteria={
                                 'age_group': age_group,
                                 'presentation': presentation,
                                 'funding_source': funding_source,
                                 'location': location
                             })
    
    except Exception as e:
        flash(f'Error searching clinicians: {str(e)}', 'error')
        return redirect(url_for('triage.index'))

@bp.route('/search', methods=['POST'])
@login_required
def search():
    age_group = request.form.get('age_group')
    presentation = request.form.get('presentation')
    funding_source = request.form.get('funding_source')
    location = request.form.get('location')
    
    return search_clinicians(age_group, presentation, funding_source, location)

@bp.route('/api/presentations')
@login_required
def api_presentations():
    presentations = get_all_presentations()
    return jsonify(presentations)

