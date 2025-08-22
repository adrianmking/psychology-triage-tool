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
def get_age_groups():
    return [
        {"id": "age_0_6", "label": "0-6 years"},
        {"id": "age_6_12", "label": "6-12 years"},
        {"id": "age_12_18", "label": "12-18 years"},
        {"id": "age_18_plus", "label": "18+ years"},
        {"id": "age_70_plus", "label": "70+ years"}
    ]

# Helper function to get all funding sources
def get_funding_sources():
    return [
        {"id": "mhcp", "label": "MHCP"},
        {"id": "ndis", "label": "NDIS"},
        {"id": "dva", "label": "DVA"},
        {"id": "wc", "label": "Workers Compensation"},
        {"id": "qps", "label": "QPS"},
        {"id": "eap", "label": "EAP"},
        {"id": "private", "label": "Private"}
    ]

# Helper function to get all locations
def get_locations():
    locations = ["Maroochydore", "Sippy Downs", "Flexible"]
    
    json_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'clinicians.json')
    
    if not os.path.exists(json_path):
        return locations
    
    try:
        with open(json_path, 'r') as f:
            clinicians = json.load(f)
        
        # Extract all unique locations
        db_locations = set()
        for clinician in clinicians:
            if clinician.get('primary_location'):
                db_locations.add(clinician['primary_location'])
        
        # Make sure Maroochydore, Sippy Downs, and Flexible are always included
        for loc in locations:
            if loc in db_locations:
                db_locations.remove(loc)
        
        # Combine the standard locations with any additional ones from the database
        all_locations = locations + sorted(list(db_locations))
        
        return all_locations
    except:
        return locations

# Helper function to search for matching clinicians
def search_clinicians(age_group, presentation, funding_source, location):
    json_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'clinicians.json')
    
    if not os.path.exists(json_path):
        return []
    
    try:
        with open(json_path, 'r') as f:
            clinicians = json.load(f)
        
        # Convert presentation to column name format
        presentation_column = presentation.lower().replace(' ', '_') + '_treats'
        
        # Filter clinicians based on criteria
        matches = []
        
        for clinician in clinicians:
            # Skip if clinician is closed (marked as Unavailable or Closed)
            if clinician.get('availability_status') == 'Unavailable' or clinician.get('availability_status') == 'Closed':
                continue
            
            # STRICT LOCATION MATCHING: If a specific location is selected, only show clinicians from that location
            if location != "Flexible" and clinician.get('primary_location') != location:
                continue
            
            # STRICT PRESENTATION MATCHING: Only include clinicians who definitely treat this presentation
            if clinician.get(presentation_column) != 'Y':
                continue
            
            # Check age group match - must be exact
            if clinician.get(age_group) != 'Y':
                continue
            
            # Check funding source match
            # Special case: if MHCP is selected, all clinicians are considered to accept it
            if funding_source != 'mhcp' and clinician.get(funding_source) != 'Y':
                continue
            
            # Calculate match score - now all included clinicians meet the basic requirements
            match_score = 100  # Start with 100% match
            match_details = []
            
            # Reduce score for conditional matches (though we're now filtering these out)
            if clinician.get(presentation_column) == 'Conditional':
                match_score -= 10
                match_details.append("Conditional treatment for this presentation")
            
            if funding_source != 'mhcp' and clinician.get(funding_source) == 'Conditional':
                match_score -= 10
                match_details.append("Conditional acceptance of this funding")
            
            # Get service type for the presentation
            service_type_column = presentation.lower().replace(' ', '_') + '_service_type'
            service_type = clinician.get(service_type_column, 'Unknown')
            
            # Get notes for the presentation
            notes_column = presentation.lower().replace(' ', '_') + '_notes'
            notes = clinician.get(notes_column)
            
            matches.append({
                'name': clinician.get('clinician_name', 'Unknown'),
                'profession': clinician.get('profession', 'Unknown'),
                'gender': clinician.get('gender', 'Unknown'),
                'location': clinician.get('primary_location', 'Unknown'),
                'service_type': service_type,
                'notes': notes,
                'match_score': match_score,
                'match_percentage': match_score,
                'match_details': match_details,
                'availability_status': clinician.get('availability_status', 'Unknown'),
                'available_from_date': clinician.get('available_from_date'),
                'availability_notes': clinician.get('availability_notes')
            })
        
        # Sort by match score (descending) and availability
        matches.sort(key=lambda x: (
            0 if x['availability_status'] == 'Available' else 1,  # Available first
            -x['match_score']  # Higher score first
        ))
        
        return matches
    except Exception as e:
        print(f"Error searching clinicians: {str(e)}")
        return []

# Triage index page
@bp.route('/')
@login_required
def index():
    age_groups = get_age_groups()
    presentations = get_all_presentations()
    funding_sources = get_funding_sources()
    locations = get_locations()
    
    return render_template('triage/index.html',
                          age_groups=age_groups,
                          presentations=presentations,
                          funding_sources=funding_sources,
                          locations=locations)

# Search for matching clinicians
@bp.route('/search', methods=['POST'])
@login_required
def search():
    age_group = request.form.get('age_group')
    presentation = request.form.get('presentation')
    funding_source = request.form.get('funding_source')
    location = request.form.get('location')
    
    # Validate inputs
    if not all([age_group, presentation, funding_source, location]):
        flash('Please fill in all fields', 'error')
        return redirect(url_for('triage.index'))
    
    # Search for matching clinicians
    matches = search_clinicians(age_group, presentation, funding_source, location)
    
    # Store search parameters in session for reference
    session['last_search'] = {
        'age_group': age_group,
        'presentation': presentation,
        'funding_source': funding_source,
        'location': location
    }
    
    # Get the labels for display
    age_groups = get_age_groups()
    age_group_label = next((g['label'] for g in age_groups if g['id'] == age_group), age_group)
    
    funding_sources = get_funding_sources()
    funding_source_label = next((f['label'] for f in funding_sources if f['id'] == funding_source), funding_source)
    
    return render_template('triage/results.html',
                          matches=matches,
                          age_group=age_group_label,
                          presentation=presentation,
                          funding_source=funding_source_label,
                          location=location)

# API endpoint for presentation autocomplete
@bp.route('/api/presentations')
@login_required
def api_presentations():
    query = request.args.get('q', '').lower()
    presentations = get_all_presentations()
    
    # Filter presentations based on query
    filtered = [p for p in presentations if query in p.lower()]
    
    return jsonify(filtered)

