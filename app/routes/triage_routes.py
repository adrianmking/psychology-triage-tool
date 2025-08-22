from flask import Blueprint, render_template, request, jsonify, current_app
import json
import os

bp = Blueprint("triage", __name__, url_prefix="/triage")

def get_all_presentations():
    json_path = os.path.join(current_app.config["UPLOAD_FOLDER"], "clinicians.json")
    if not os.path.exists(json_path):
        return []
    try:
        with open(json_path, "r") as f:
            clinicians = json.load(f)
        presentation_columns = [col for col in clinicians[0].keys() if col.endswith("_treats")]
        presentations = [col.replace("_treats", "").replace("_", " ").title() for col in presentation_columns]
        return sorted(presentations)
    except:
        return []

def get_all_age_groups():
    json_path = os.path.join(current_app.config["UPLOAD_FOLDER"], "clinicians.json")
    if not os.path.exists(json_path):
        return []
    try:
        with open(json_path, "r") as f:
            clinicians = json.load(f)
        age_group_columns = [col for col in clinicians[0].keys() if col.startswith("age_")]
        age_groups = []
        for col in age_group_columns:
            if col == "age_0_6":
                age_groups.append("0-6 years")
            elif col == "age_6_12":
                age_groups.append("6-12 years")
            elif col == "age_12_18":
                age_groups.append("12-18 years")
            elif col == "age_18_plus":
                age_groups.append("18+ years")
            elif col == "age_70_plus":
                age_groups.append("70+ years")
        return sorted(age_groups)
    except:
        return []

def get_all_funding_sources():
    json_path = os.path.join(current_app.config["UPLOAD_FOLDER"], "clinicians.json")
    if not os.path.exists(json_path):
        return []
    try:
        with open(json_path, "r") as f:
            clinicians = json.load(f)
        
        # Look for individual funding columns in your spreadsheet
        funding_columns = ["mhcp", "ndis", "dva", "wc", "qps", "eap", "private"]
        available_funding = []
        
        # Check which funding columns exist and have data
        for funding_col in funding_columns:
            if funding_col in clinicians[0]:
                if funding_col == "mhcp":
                    available_funding.append("MHCP")
                elif funding_col == "ndis":
                    available_funding.append("NDIS")
                elif funding_col == "dva":
                    available_funding.append("DVA")
                elif funding_col == "wc":
                    available_funding.append("WorkCover")
                elif funding_col == "qps":
                    available_funding.append("QPS")
                elif funding_col == "eap":
                    available_funding.append("EAP")
                elif funding_col == "private":
                    available_funding.append("Private")
        
        return sorted(available_funding)
    except:
        return []

@bp.route("/")
def index():
    presentations = get_all_presentations()
    age_groups = get_all_age_groups()
    funding_sources = get_all_funding_sources()
    locations = ["Sippy Downs", "North Lakes", "Flexible"]
    return render_template(
        "triage/index.html",
        presentations=presentations,
        age_groups=age_groups,
        funding_sources=funding_sources,
        locations=locations,
    )

@bp.route("/search", methods=["POST"])
def search():
    age_group = request.form.get("age_group")
    presentation = request.form.get("presentation")
    funding_source = request.form.get("funding_source")
    location = request.form.get("location")

    json_path = os.path.join(current_app.config["UPLOAD_FOLDER"], "clinicians.json")
    if not os.path.exists(json_path):
        return jsonify([])

    with open(json_path, "r") as f:
        clinicians = json.load(f)

    matches = []

    for clinician in clinicians:
        # Skip if clinician is closed (using original spreadsheet data only)
        if clinician.get("availability_status") == "Unavailable" or clinician.get("availability_status") == "Closed":
            continue

        # Location matching
        if location != "Flexible" and clinician.get("primary_location") != location:
            continue

        # Presentation matching
        presentation_matched = False
        if presentation:
            presentation_col = presentation.lower().replace(" ", "_") + "_treats"
            if clinician.get(presentation_col) == "Y":
                presentation_matched = True
        else:
            presentation_matched = True

        if not presentation_matched:
            continue

        # Age group matching - using your actual column names
        age_group_matched = False
        if age_group:
            if age_group == "0-6 years" and clinician.get("age_0_6") == "Y":
                age_group_matched = True
            elif age_group == "6-12 years" and clinician.get("age_6_12") == "Y":
                age_group_matched = True
            elif age_group == "12-18 years" and clinician.get("age_12_18") == "Y":
                age_group_matched = True
            elif age_group == "18+ years" and clinician.get("age_18_plus") == "Y":
                age_group_matched = True
            elif age_group == "70+ years" and clinician.get("age_70_plus") == "Y":
                age_group_matched = True
        else:
            age_group_matched = True

        if not age_group_matched:
            continue

        # Funding source matching - using your individual funding columns
        funding_source_matched = False
        if funding_source:
            if funding_source == "MHCP" and clinician.get("mhcp") == "Y":
                funding_source_matched = True
            elif funding_source == "NDIS" and clinician.get("ndis") == "Y":
                funding_source_matched = True
            elif funding_source == "DVA" and clinician.get("dva") == "Y":
                funding_source_matched = True
            elif funding_source == "WorkCover" and clinician.get("wc") == "Y":
                funding_source_matched = True
            elif funding_source == "QPS" and clinician.get("qps") == "Y":
                funding_source_matched = True
            elif funding_source == "EAP" and clinician.get("eap") == "Y":
                funding_source_matched = True
            elif funding_source == "Private" and clinician.get("private") == "Y":
                funding_source_matched = True
        else:
            funding_source_matched = True

        if not funding_source_matched:
            continue

        matches.append(clinician)

    return jsonify(matches)

