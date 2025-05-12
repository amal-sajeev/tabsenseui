# TabSense Dashboard User Manual

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
   - [Accessing the Dashboard](#accessing-the-dashboard)
   - [Understanding the Interface](#understanding-the-interface)
   - [Client Selection](#client-selection)
   - [Navigation](#navigation)
3. [Home Dashboard](#home-dashboard)
   - [Overview](#overview)
   - [Quick Statistics](#quick-statistics)
4. [Detection](#detection)
   - [Understanding Detection](#understanding-detection)
   - [Running a Manual Detection](#running-a-manual-detection)
   - [Interpreting Results](#interpreting-results)
5. [Schedule Management](#schedule-management)
   - [Understanding Schedules](#understanding-schedules)
   - [Viewing the Schedule](#viewing-the-schedule)
   - [Adding Schedule Entries](#adding-schedule-entries)
   - [Updating Schedule Entries](#updating-schedule-entries)
   - [Deleting Schedule Entries](#deleting-schedule-entries)
6. [Camera Management](#camera-management)
   - [Understanding Camera Setup](#understanding-camera-setup)
   - [Viewing Cameras](#viewing-cameras)
   - [Adding Cameras](#adding-cameras)
   - [Updating Cameras](#updating-cameras)
   - [Deleting Cameras](#deleting-cameras)
   - [Bulk Importing Cameras](#bulk-importing-cameras)
7. [Reports](#reports)
   - [Understanding Reports](#understanding-reports)
   - [Generating Reports](#generating-reports)
   - [Analyzing Report Data](#analyzing-report-data)
8. [Scheduler Control](#scheduler-control)
   - [Understanding the Scheduler](#understanding-the-scheduler)
   - [Managing the Scheduler](#managing-the-scheduler)
9. [Extensive Troubleshooting Guide](#extensive-troubleshooting-guide)
   - [Login and Access Issues](#login-and-access-issues)
   - [Client Selection Issues](#client-selection-issues)
   - [Camera Problems](#camera-problems)
   - [Schedule Issues](#schedule-issues)
   - [Detection Problems](#detection-problems)
   - [Report Generation Issues](#report-generation-issues)
   - [System Performance Issues](#system-performance-issues)
   - [Common Error Messages](#common-error-messages)

## Introduction

TabSense is a sophisticated monitoring system designed to help you track surface cleanliness through automated image analysis. This technology uses scheduled image captures and comparison algorithms to detect stains, residue, and other cleanliness issues across multiple locations, rooms, and specific areas (sectors).

For businesses in industries where cleanliness is critical—such as hospitality, healthcare, food service, and manufacturing—TabSense provides an objective, automated way to verify that cleaning procedures are effective and surfaces remain clean between scheduled cleanings.

This user manual will guide you through all features of the TabSense Dashboard, from basic navigation to advanced reporting, ensuring you can effectively monitor your facilities regardless of your technical experience.

## Getting Started

### Accessing the Dashboard

To access the TabSense Dashboard:

1. Open your web browser
2. Navigate to your organization's TabSense URL (typically provided by your IT department)
3. Log in with your provided credentials if prompted

### Understanding the Interface

The TabSense Dashboard has three main sections:

1. **Left Sidebar**: Contains navigation menu, client selection, and scheduler controls
2. **Main Content Area**: Displays the currently selected page content
3. **Top Bar**: Shows the page title and sometimes contains additional controls

### Client Selection

Before using any features of the TabSense Dashboard, you must first select a client. A "client" in TabSense represents an organization or facility being monitored.

1. Locate the **Client Selection** field in the left sidebar
2. Enter your client name exactly as it was configured in the system
3. All subsequent operations will be performed in the context of this client

**Important**: If you're unsure of your client name, contact your system administrator.

### Navigation

The TabSense Dashboard is organized into several main sections accessible via the navigation menu in the sidebar:

- **Home**: Overview and quick statistics
- **Detection**: Manual stain detection tools for on-demand analysis
- **Schedule**: Schedule management for automated monitoring
- **Camera Management**: Configure and manage cameras throughout your facility
- **Reports**: Generate and view detection reports for historical analysis

To navigate, simply click on the desired section in the sidebar menu.

## Home Dashboard

### Overview

The Home page provides a central overview of your TabSense system. For beginners, this is the best place to start as it provides a summary of the system's status and basic statistics.

When you first access the Home page, you'll see:

- A welcome message introducing TabSense
- A summary of main features
- A section for quick statistics (only visible when a client is selected)

### Quick Statistics

Once you've selected a client, the Home page displays quick statistics giving you an at-a-glance view of your monitoring system:

- **Total Rooms**: The number of distinct rooms configured for monitoring
- **Active Cameras**: The total number of cameras currently connected to the system
- **Detections Today**: The number of stain detections recorded today

These statistics help you quickly assess the scope of your monitoring setup and recent cleanliness issues.

## Detection

### Understanding Detection

The Detection feature allows you to manually run stain detection on specific areas. This is useful for:

- Immediate verification of cleanliness
- Testing new camera setups
- Investigating reported cleanliness issues
- Training staff on what constitutes a detection

TabSense detection works by comparing a clean reference image (control image) with a current image to identify differences that may indicate stains or other cleanliness issues.

### Running a Manual Detection

To run a manual detection:

1. Navigate to the **Detection** page from the sidebar
2. Ensure you have selected the correct client
3. Fill in the detection form:
   - **Control Image UUID**: Enter the unique identifier of the clean reference image (this is typically recorded when setting up a camera or can be found in the system logs)
   - **Current Image UUID**: Enter the unique identifier of the image you want to check for stains
   - **Room**: Select the room from the dropdown (this list is populated based on rooms configured in your schedule)
   - **Sectors**: Select which camera sectors to analyze. Sectors are specific areas within a room that are monitored separately
4. Configure detection options:
   - **Crop Images**: When enabled, focuses the analysis on the most relevant parts of the image
   - **Shape**: Determines how the detection algorithm identifies potential stain boundaries:
     - **Auto**: System chooses the best method based on the images
     - **Rectangle**: Identifies stains as rectangular areas
     - **Circle**: Identifies stains as circular areas
     - **Oval**: Identifies stains as oval-shaped areas
   - **Border Color**: Choose the color used to highlight detected stains in the results
   - **Image Format**: Select the output format for the results images
5. Click **Run Detection** to start the analysis

### Interpreting Results

After running a detection, results will be displayed below the form:

- If stains are detected, you'll see a success message indicating how many sectors had detections
- For each sector with detections:
  - The control (clean) image is shown on the left
  - The current image with highlighted stains is shown on the right
  - The highlighted areas indicate where the system detected differences between the two images

If no stains are detected, you'll see an information message stating "No stains detected!"

## Schedule Management

### Understanding Schedules

Schedules in TabSense allow you to automate the monitoring process by defining when and where the system should capture images and run detections. A schedule consists of:

- A specific room to monitor
- One or more sectors within that room
- Time windows when monitoring should occur
- Days of the week when the schedule is active

The scheduler will automatically capture images from the configured cameras during the specified times and run detections to check for cleanliness issues.

### Viewing the Schedule

To view your current schedule:

1. Navigate to **Schedule** > **View Schedule** tab
2. The current schedule will be displayed in a table format with the following information:
   - Room name
   - Schedule label
   - Start and end times
   - Active days
   - Sectors being monitored
   - Schedule ID (useful for technical support)

For large schedules, you can filter the results by expanding the **Filter Results** section and entering a room name.

### Adding Schedule Entries

To add a new schedule entry:

1. Navigate to **Schedule** > **Add Entry** tab
2. Fill in the form:
   - **Room**: Select an existing room from the dropdown or choose "New Room..." to create a new one
   - **Label**: Enter a descriptive name for this schedule entry (e.g., "Morning Check", "Post-Cleaning Verification")
   - **Start Hour/Minute**: Set when monitoring should begin each day
   - **End Hour/Minute**: Set when monitoring should end each day
   - **Sectors**: Select camera sectors to monitor (these correspond to specific cameras in the room)
   - **Days**: Select which days of the week this schedule should be active
3. Click **Add Schedule Entry**

A success message will appear when the entry is added successfully.

### Updating Schedule Entries

To update an existing schedule entry:

1. Navigate to **Schedule** > **Update Entry** tab
2. Select the entry you want to update from the dropdown (entries are listed with their ID, label, and room)
3. The form will be pre-filled with the current settings for this entry
4. Modify any fields as needed
5. Click **Update Schedule Entry**

A success message will appear when the entry is updated successfully.

### Deleting Schedule Entries

To delete schedule entries:

1. Navigate to **Schedule** > **Delete Entry** tab
2. Choose a deletion method:
   - **Single Entry**: Select and delete a specific entry from the dropdown
   - **Room**: Delete all entries for a specific room
   - **Multiple Entries**: Check multiple entries to delete at once
3. Click the corresponding delete button
4. Confirm the deletion when prompted

A success message will appear when the entries are deleted successfully.

## Camera Management

### Understanding Camera Setup

Cameras are the eyes of the TabSense system, capturing images that are used for stain detection. Each camera is associated with:

- A specific room
- A sector number (representing a specific area within the room)
- A link/URL that provides access to the camera feed

TabSense supports various camera types, including IP cameras with RTSP streams and static image URLs.

### Viewing Cameras

To view your configured cameras:

1. Navigate to **Camera Management** > **View Cameras** tab
2. Filter the camera list if needed:
   - **Filter by Room**: Select a specific room from the dropdown
   - **Filter by Sector**: Enter a sector number (use 0 to show all sectors)
3. Camera information will be displayed in a table showing:
   - Camera ID
   - Room name
   - Sector number
   - Camera link
4. Below the table, you'll see **Camera Previews** with buttons for each camera
5. Click on a camera button to expand a live preview of that camera's feed

The preview feature helps verify that cameras are working correctly and positioned appropriately.

### Adding Cameras

To add a new camera:

1. Navigate to **Camera Management** > **Add Camera** tab
2. Fill in the form:
   - **Room**: Select an existing room or enter a new one
   - **Sector**: Enter the sector number (a unique identifier within the room)
   - **Camera Link**: Enter the full URL to access the camera
     - For IP cameras, this is typically an RTSP URL (e.g., `rtsp://username:password@camera-ip:port/stream`)
     - For static images, this can be an HTTP URL
3. Click **Add Camera**

A success message will appear when the camera is added successfully.

### Updating Cameras

To update an existing camera:

1. Navigate to **Camera Management** > **Update Camera** tab
2. Choose a search method:
   - **Room & Sector**: Find a camera by room name and sector number
   - **Camera ID**: Find a camera by its unique system ID
3. Enter the required search information
4. Click **Find Camera**
5. When the camera is found, a form will appear with the current settings
6. Modify any fields as needed:
   - **New Room**: Change the room assignment
   - **New Sector**: Change the sector number
   - **New Camera Link**: Update the camera URL
7. Click **Update Camera**

A success message will appear when the camera is updated successfully.

### Deleting Cameras

To delete cameras:

1. Navigate to **Camera Management** > **Delete Camera** tab
2. Choose a deletion method:
   - **Room & Sector**: Delete a camera by room name and sector number
   - **Camera ID**: Delete a camera by its unique system ID
   - **All in Room**: Delete all cameras in a specific room
3. Enter the required information for your chosen method
4. Click the corresponding delete button
5. Confirm the deletion when prompted

A success message will appear when the camera(s) are deleted successfully.

### Bulk Importing Cameras

For setups with many cameras, TabSense allows bulk importing:

1. Navigate to **Camera Management** > **Bulk Import** tab
2. Prepare a CSV file with three columns:
   - `room`: Room name for each camera
   - `sector`: Sector number for each camera
   - `link`: Camera URL for each camera
3. Click **Choose a CSV file** and select your prepared file
4. Review the preview of the uploaded data to verify it looks correct
5. Click **Import Cameras**
6. A progress bar will show the import status
7. When complete, a summary will show successful and failed imports

If any imports fail, you can expand the "Error Details" section to see what went wrong.

## Reports

### Understanding Reports

The Reports section allows you to generate and view historical detection data. Reports are useful for:

- Tracking cleanliness trends over time
- Identifying problem areas that may need additional attention
- Verifying that cleaning procedures are effective
- Providing documentation for compliance purposes

Reports can be filtered by room and date range to focus on specific areas or time periods.

### Generating Reports

To generate a report:

1. Navigate to the **Reports** page from the sidebar
2. Enter a **Room** name to report on
3. Select a **Start Date** and **End Date** for the report period
4. Click **Generate Report**

The system will retrieve all detection records matching your criteria and display them.

### Analyzing Report Data

Once a report is generated, you'll see:

1. **Summary Metrics**:
   - Total detections found during the period
   - Date range of the report
   - Number of detection records

2. **Detection Records Table**:
   - Detailed information about each detection event
   - Timestamps of when detections occurred
   - Number of stains detected in each event

3. **Visualization**:
   - A line chart showing detections over time
   - Helps identify patterns or trends in cleanliness issues

4. **Export Options**:
   - Click **Download CSV** to save the report data for offline analysis or record-keeping

## Scheduler Control

### Understanding the Scheduler

The Scheduler is the background process that automates image capture and detection according to your configured schedules. It:

- Runs continuously in the background
- Checks the schedule to determine when to capture images
- Automatically runs detections on newly captured images
- Records results for later reporting

For TabSense to perform automated monitoring, the scheduler must be running.

### Managing the Scheduler

The Scheduler Control section in the left sidebar allows you to manage the automated monitoring service:

1. **Launch Scheduler**: Starts the monitoring scheduler if it's not already running
   - Click this button when setting up TabSense for the first time
   - Click this button if the scheduler has been stopped

2. **Relaunch Scheduler**: Force-stops and then restarts the monitoring scheduler
   - Use this if you suspect the scheduler is running but not functioning correctly
   - Use this after making significant changes to your schedule or camera configuration

After clicking either button, a success message will appear if the operation was successful.

## Extensive Troubleshooting Guide

### Login and Access Issues

**Issue**: Unable to access the dashboard
- **Solution**: Verify you're using the correct URL for your TabSense installation
- **Solution**: Check that your network connection is active
- **Solution**: Clear your browser cache and cookies
- **Solution**: Try using a different browser

**Issue**: Dashboard appears but shows errors or doesn't load completely
- **Solution**: Refresh the page
- **Solution**: Try disabling browser extensions that might interfere
- **Solution**: Check with IT that the TabSense server is running correctly

### Client Selection Issues

**Issue**: Cannot find the correct client name
- **Solution**: Check with your administrator for the exact client name
- **Solution**: Client names are case-sensitive; ensure correct capitalization
- **Solution**: Look for possible spaces or special characters in the client name

**Issue**: Client selection doesn't persist between sessions
- **Solution**: Check that your browser allows cookies
- **Solution**: Try selecting the client again and refreshing the page

**Issue**: "Please select a client" warning appears despite entering a client name
- **Solution**: Verify the client name is spelled correctly
- **Solution**: Confirm with administrator that the client exists in the system
- **Solution**: Try logging out and logging back in

### Camera Problems

**Issue**: Cameras not appearing in the camera list
- **Solution**: Verify you've entered the correct client name
- **Solution**: Confirm cameras have been added to the system
- **Solution**: Check the "View Cameras" tab with no filters to see all cameras

**Issue**: Camera preview not loading
- **Solution**: Verify that the camera URL is correct and accessible
- **Solution**: Check network connectivity between the TabSense server and the camera
- **Solution**: Ensure the camera is powered on and connected to the network
- **Solution**: Check if the camera requires authentication and that credentials are correct
- **Solution**: Verify that the camera's RTSP port isn't blocked by a firewall

**Issue**: Camera images are blurry or poorly positioned
- **Solution**: Physically adjust the camera position or focus
- **Solution**: Check camera settings for resolution and quality
- **Solution**: Clean the camera lens if dusty or dirty

**Issue**: Error when adding a new camera
- **Solution**: Check that all required fields are completed
- **Solution**: Verify the URL format is correct (e.g., RTSP URLs should start with `rtsp://`)
- **Solution**: Ensure the sector number is unique within the selected room

### Schedule Issues

**Issue**: Schedule entries not appearing
- **Solution**: Check that you've selected the correct client
- **Solution**: Verify schedule entries have been created
- **Solution**: Try refreshing the page

**Issue**: Automated detections not running according to schedule
- **Solution**: Verify the scheduler is running (see Scheduler Control section)
- **Solution**: Check that the schedule times are correct (24-hour format)
- **Solution**: Ensure the current day is selected in the schedule's "Days" field
- **Solution**: Verify cameras are properly configured for the scheduled room/sectors

**Issue**: Error when adding or updating schedule entries
- **Solution**: Check that all required fields are completed
- **Solution**: Verify end time is later than start time
- **Solution**: Ensure at least one day is selected
- **Solution**: Check that the sectors specified have corresponding cameras

### Detection Problems

**Issue**: Manual detection shows "Error" message
- **Solution**: Verify that the control and current image UUIDs are correct
- **Solution**: Check that the room and sectors are properly configured
- **Solution**: Ensure the images exist and are accessible to the system

**Issue**: No stains detected when there should be
- **Solution**: Check that the control image is truly clean
- **Solution**: Verify that the lighting conditions are similar between control and current images
- **Solution**: Try adjusting the detection sensitivity (contact administrator)
- **Solution**: Ensure the camera is properly focused and positioned

**Issue**: False positives (stains detected when there aren't any)
- **Solution**: Check for lighting changes between control and current images
- **Solution**: Verify that the control image is appropriate for the current setup
- **Solution**: Check for camera movement or focus changes
- **Solution**: Consider updating the control image if conditions have changed

**Issue**: "Image not found" error
- **Solution**: Verify the image UUIDs are correct
- **Solution**: Check that the images haven't been deleted from the system
- **Solution**: Ensure the scheduler is properly capturing images (for automated monitoring)

### Report Generation Issues

**Issue**: No data in generated reports
- **Solution**: Verify you've selected the correct room
- **Solution**: Check that the date range includes periods when detections occurred
- **Solution**: Ensure that scheduled detections have been running properly
- **Solution**: Verify that the client selection is correct

**Issue**: Reports missing expected detection events
- **Solution**: Check that the date range fully covers the period of interest
- **Solution**: Verify that scheduled detections were active during that period
- **Solution**: Ensure the scheduler was running during the period

**Issue**: Error when generating reports
- **Solution**: Try a shorter date range (large date ranges may timeout)
- **Solution**: Check that the room name is spelled correctly
- **Solution**: Verify server connectivity

**Issue**: Cannot download CSV report
- **Solution**: Check browser download settings
- **Solution**: Try using a different browser
- **Solution**: Ensure you have the necessary permissions

### System Performance Issues

**Issue**: Dashboard is slow to respond
- **Solution**: Try refreshing the page
- **Solution**: Check your internet connection speed
- **Solution**: Close unused browser tabs
- **Solution**: If viewing camera previews, close them when not needed

**Issue**: Scheduler running slowly or missing scheduled captures
- **Solution**: Relaunch the scheduler using the sidebar button
- **Solution**: Check that the server has sufficient resources
- **Solution**: Verify that the network can handle the camera traffic
- **Solution**: Consider reducing the number of concurrent scheduled captures

**Issue**: Image processing takes too long
- **Solution**: Check server resources (CPU, memory)
- **Solution**: Consider optimizing image resolution for faster processing
- **Solution**: Stagger schedules to avoid too many simultaneous detections

### Common Error Messages

**Error**: "Failed to fetch" or "Network Error"
- **Cause**: Connection issues between browser and TabSense server
- **Solution**: Check network connectivity
- **Solution**: Verify the server is running
- **Solution**: Try refreshing the page

**Error**: "Error: 404 - Not Found"
- **Cause**: Requested resource doesn't exist
- **Solution**: Check that the client, room, or camera you're trying to access exists
- **Solution**: Verify URLs and IDs are correct

**Error**: "Error: 500 - Internal Server Error"
- **Cause**: Server-side problem processing the request
- **Solution**: Try the operation again
- **Solution**: Check server logs (contact administrator)
- **Solution**: Verify the data you're submitting is valid

**Error**: "Unauthorized" or "Access Denied"
- **Cause**: Insufficient permissions
- **Solution**: Log out and log back in
- **Solution**: Contact administrator to verify your access rights

---

© 2025 TabSense. All rights reserved.