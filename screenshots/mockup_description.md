# Psychology Clinic Triage Tool - Interface Mockups

## Login Screen
- Clean, professional login form with the clinic logo
- Fields for username and password
- Login button
- Error messages for invalid credentials

## Admin Dashboard
- Welcome message with user name
- Three main cards:
  1. Clinician Database - Shows status, count, and last updated date
  2. Manage Clinicians - Link to clinician management page
  3. Triage Tool - Link to the triage interface
- Navigation menu at the top

## Spreadsheet Upload
- Form to select and upload Excel file
- Instructions on required format
- Success/error messages
- Cancel button to return to dashboard

## Clinician Management
- Table listing all clinicians with:
  - Name
  - Profession
  - Location
  - Availability status (Available, Waitlist, Unavailable)
  - Available from date
  - Edit button
- Modal dialog for editing clinician availability:
  - Status dropdown (Available, Waitlist, Unavailable)
  - Date picker for future availability
  - Notes text area
  - Save and Cancel buttons

## Triage Form
- Form with four main fields:
  1. Age Group - Dropdown with options (0-6, 6-12, 12-18, 18+, 70+)
  2. Presentation - Text input with type-ahead search
  3. Funding Source - Dropdown with options (MHCP, NDIS, DVA, etc.)
  4. Location - Dropdown with clinic locations
- Search button
- Instructions panel

## Search Results
- Search criteria summary at the top
- Cards for each matching clinician showing:
  - Name, profession, gender
  - Match percentage (color-coded)
  - Location and service type
  - Availability status and dates
  - Match details explaining why not 100% match (if applicable)
  - Notes about the clinician's services
  - "Book Now" button
- "New Search" button to return to the form

