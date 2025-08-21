# Psychology Clinic Triage Tool - User Guide

## Accessing the Application

The triage tool is accessible at the following URL:
```
https://5000-i1rm0nj1aasjqjy8iwz1q-456bd350.manusvm.computer
```

## Login Credentials

### Super Admin
- Username: `admin`
- Password: `admin123`

### Triage Staff
- Username: `staff`
- Password: `staff123`

## User Roles

### Super Admin
The Super Admin role has full access to all features of the application, including:
- Uploading and updating the clinician database
- Managing clinician availability
- Using the triage tool to find matching clinicians

### Triage Staff
The Triage Staff role has limited access to the application, including:
- Using the triage tool to find matching clinicians

## Using the Application

### Super Admin Dashboard

After logging in as a Super Admin, you will be directed to the Admin Dashboard. From here, you can:

1. **Upload Clinician Spreadsheet**
   - Click on "Upload Spreadsheet" button
   - Select the Excel file containing clinician data
   - Click "Upload Spreadsheet" to process the file
   - The spreadsheet must follow the required format with columns for clinician information, age groups, presentations, and funding sources

2. **Manage Clinicians**
   - Click on "Manage Clinicians" button
   - View a list of all clinicians in the database
   - Edit individual clinician availability by clicking the "Edit" button
   - Update availability status (Available, Waitlist, Unavailable)
   - Set future availability dates for clinicians who are temporarily unavailable
   - Add notes about clinician availability

3. **Use Triage Tool**
   - Click on "Go to Triage Tool" button
   - Follow the instructions for using the triage tool (see below)

### Triage Tool

After logging in as Triage Staff (or accessing the triage tool as a Super Admin), you will see the triage form. To find matching clinicians:

1. **Enter Client Information**
   - Select the client's age group from the dropdown
   - Enter the client's presentation (start typing to see suggestions)
   - Select the client's funding source from the dropdown
   - Select the preferred location from the dropdown

2. **Find Matching Clinicians**
   - Click "Find Matching Clinicians" button
   - View the list of matching clinicians sorted by match percentage
   - Each clinician card shows:
     - Name, profession, and gender
     - Location and service type
     - Availability status and dates
     - Match details (if not a 100% match)
     - Notes about the clinician's services

3. **Book an Appointment**
   - Click "Book Now" button to open the booking system in a new tab
   - This will take you to the external booking system (Zanda Health)

## Maintenance and Updates

### Updating Clinician Database
To update the clinician database:
1. Log in as a Super Admin
2. Go to "Upload Spreadsheet"
3. Upload the new Excel file
4. The new data will replace the existing database

### Managing Clinician Availability
To update individual clinician availability:
1. Log in as a Super Admin
2. Go to "Manage Clinicians"
3. Find the clinician you want to update
4. Click "Edit" button
5. Update the availability status, date, and notes
6. Click "Save Changes"

## Troubleshooting

### Common Issues

1. **No matching clinicians found**
   - Try broadening your search criteria
   - Check that the clinician database has been uploaded
   - Verify that clinicians in the database match the selected criteria

2. **Spreadsheet upload errors**
   - Ensure the spreadsheet follows the required format
   - Check for missing or incorrectly named columns
   - Verify that the file is in Excel format (.xlsx or .xls)

3. **Login issues**
   - Verify that you are using the correct username and password
   - Contact the system administrator if you cannot access your account

### Support

For additional support or to report issues, please contact the system administrator.

