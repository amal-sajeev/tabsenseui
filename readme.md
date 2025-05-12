# TabSense

![[tabsense logo (Custom).png]]

TabSense is a system for automated table and surface cleanliness monitoring using computer vision. This system detects stains and other cleanliness issues by comparing control (clean) images with current images of surfaces.

## Components

The TabSense system consists of the following components:

1. **FastAPI Backend**: Handles image processing, detection, scheduling, and database operations
2. **Streamlit UI**: Provides a user-friendly interface for interacting with the system
3. **Capture Scheduler**: Background process that manages scheduled image captures and detections
4. **MongoDB Database**: Stores all configuration and detection results

## Getting Started

### Prerequisites

- Python 3.7+
- MongoDB
- OpenCV
- Required Python packages: `fastapi`, `streamlit`, `pymongo`, `schedule`, `requests`, `Pillow`, `pandas`

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/tabsense.git
   cd tabsense
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Configure MongoDB connection:
   ```
   export mongocred="username:password"
   ```

### Running the System

1. Start the FastAPI server:
   ```
   uvicorn detectapi:app --reload
   ```

2. Start the Streamlit UI:
   ```
   streamlit run tabsense_ui.py
   ```

3. Launch the scheduler from the Streamlit UI or manually:
   ```
   python capture.py
   ```

## System Usage

### Client Setup

1. Start by setting a client name in the sidebar of the Streamlit UI
2. Set up rooms and cameras for the client
3. Configure capture schedules for each room

### Camera Setup

1. Go to the "Camera Management" page in the UI
2. Add cameras for each room and sector
3. Provide camera links (URL for IP cameras or device number for local cameras)

### Schedule Setup

1. Navigate to the "Schedule" page
2. Create schedule entries for each room
3. Define when control and current images should be captured
4. Specify which sectors to include

### Detection

1. Go to the "Detection" page to manually run detections
2. Alternatively, let the scheduler handle automatic detections based on your schedule

### Reports

1. Use the "Reports" page to view detection history
2. Filter reports by date range and room
3. Export reports as CSV files

## Directory Structure

- `imagedata/control`: Storage for clean/control images
- `imagedata/captures`: Storage for current captured images
- `capture.log`: Log file for the scheduler

## Troubleshooting

If you encounter issues:

1. Check the `capture.log` file for scheduler errors
2. Verify MongoDB connection settings
3. Ensure cameras are accessible through the provided links
4. Make sure all directories exist and are writable
5. Check API responses for detailed error messages

## Extending the System

- Add email or SMS notifications for stain detections
- Implement user authentication
- Add support for different types of detection algorithms
- Create custom reporting dashboards
