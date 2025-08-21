# Psychology Clinic Triage Tool - Requirements Document

## Overview
This document outlines the requirements for a web-based triage tool for a psychology clinic. The tool will be used by admin staff to handle cold calls and match potential clients with suitable clinicians based on various criteria.

## User Roles
1. **Triage Admin** - Regular staff who handle cold calls and use the tool to find matching clinicians
2. **Super Admin** - Clinic manager who can upload the master clinician spreadsheet and adjust clinician availability

## Authentication
- Secure login screen for both user roles
- Different access levels based on role

## Main Features

### Triage Interface
- Input fields:
  - Age (selection from different age groups)
  - Presentation (type-ahead search, not dropdown)
  - Funding Source (selection from options including MHCP and Private)
  - Location (two specific locations plus flexible choice)

### Search and Matching
- Search through the master spreadsheet (121 columns)
- Match clinicians based on:
  - Age groups they treat
  - Presentations they handle
  - Funding sources they accept
  - Locations they work from
- Display accurate matches showing clinicians who treat the specific presentation and age group at the selected location

### Admin Interface
- Upload facility for the master clinician spreadsheet
- Ability to adjust clinician availability
- Option to set future availability dates for clinicians

## Technical Requirements
- Web-based application accessible via URL from different clinic locations
- Secure authentication system
- Database based on the master spreadsheet structure
- Responsive design following the provided wireframes
- Branding with the clinic logo

## Design
- Follow the provided wireframes for UI/UX design
- Incorporate the clinic's branding and logo
- Ensure responsive design for different devices

## Data Structure
Based on the analysis of the master spreadsheet, the key data elements include:

### Clinician Information
- Name, gender, profession, employment type
- Primary location
- Availability status and dates

### Treatment Capabilities
- Age groups (0-6, 6-12, 12-18, 18+, 70+)
- Various presentations (anxiety, depression, PTSD, etc.)
- Service types for each presentation (assessment, therapy, both)

### Funding Options
- MHCP (Mental Health Care Plan)
- NDIS
- DVA
- Workers Compensation
- QPS
- EAP
- Private

## Search Algorithm Requirements
- Must search through specific columns in the spreadsheet
- Must match all selected criteria (age, presentation, funding, location)
- Results should show accurate matches of clinicians who can treat the specific presentation and age group
- Results should be sorted by relevance/match percentage

