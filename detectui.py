import streamlit as st
import requests
import json
import subprocess
import pandas as pd
from datetime import datetime, time
import os, cv2
from typing import List, Dict, Any
from PIL import Image
import time as timmytime

# Configure page
st.set_page_config(
    page_title="TabSense Dashboard",
    page_icon="🔍",
    layout="wide",
)

# Define API URL
API_URL = "http://localhost:8000"

# Define sidebar navigation
# st.sidebar.title("TabSense Dashboard")

st.sidebar.image("tabsense logo (Custom).png", use_container_width=True)
page = st.sidebar.selectbox(
    "Navigation", 
    ["Home", "Detection", "Schedule", "Camera Management", "Reports"]
)

# Initialize client state
if "client" not in st.session_state:
    st.session_state.client = ""

# Client selection in sidebar
st.sidebar.subheader("Client Selection")
st.session_state.client = st.sidebar.text_input("Client", st.session_state.client, key = "cliententry")

# Scheduler control section in sidebar
st.sidebar.subheader("Scheduler Control")
if st.sidebar.button("Launch Scheduler"):
    try:
        # Launch the capture.py script
        process = subprocess.Popen(["python", "capture.py"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
        st.sidebar.success("Scheduler launched successfully!")
    except Exception as e:
        st.sidebar.error(f"Failed to launch scheduler: {str(e)}")

if st.sidebar.button("Relaunch Scheduler"):
    try:
        # Kill existing process (simplified approach)
        os.system("pkill -f capture.py")
        # Relaunch the script
        process = subprocess.Popen(["python", "capture.py"], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
        st.sidebar.success("Scheduler relaunched successfully!")
    except Exception as e:
        st.sidebar.error(f"Failed to relaunch scheduler: {str(e)}")

# Home page
if page == "Home":
    st.title("TabSense Dashboard")
    
    st.write("""
    ## Welcome to TabSense
    
    TabSense helps you monitor surfaces for cleanliness through automated image analysis.
    
    ### Features:
    - Stain detection through image comparison
    - Scheduled monitoring
    - Camera management
    - Detailed reporting
    
    Use the sidebar to navigate through different features.
    """)
    
    # Quick stats if a client is selected
    if st.session_state.client:
        st.subheader(f"Quick Stats for {st.session_state.client}")
        col1, col2, col3 = st.columns(3)
        
        try:
            # Get room count
            rooms_response = requests.get(f"{API_URL}/entry", params={"client": st.session_state.client})
            if rooms_response.status_code == 200:
                entries = rooms_response.json()
                unique_rooms = set(entry.get("room", "") for entry in entries)
                room_count = len(unique_rooms)
            else:
                room_count = "N/A"
                
            # Get camera count
            try:
                cameras_response = requests.get(f"{API_URL}/cam", params={"client": st.session_state.client})
                if cameras_response.status_code == 200:
                    cameras = cameras_response.json()
                    if isinstance(cameras, list):
                        camera_count = len(cameras)
                    else:
                        camera_count = 1  # Single camera returned
                else:
                    camera_count = "N/A"
            except:
                camera_count = "N/A"
                
            # For detection count, we'd need to query each room's collection or have a summary endpoint
            # This is a placeholder
            detections_count = "N/A"
            
            with col1:
                st.metric("Total Rooms", room_count)
            with col2:
                st.metric("Active Cameras", camera_count)
            with col3:
                st.metric("Detections Today", detections_count)
        except Exception as e:
            st.warning(f"Could not fetch client statistics: {str(e)}")

# Detection Page
elif page == "Detection":
    st.title("Stain Detection")
    
    if not st.session_state.client:
        st.warning("Please select a client in the sidebar")
    else:
        with st.form("detection_form"):
            st.subheader("Run Detection")
            
            # Form fields
            control = st.text_input("Control Image UUID")
            current = st.text_input("Current Image UUID")
            
            # Get rooms from schedule entries
            try:
                response = requests.get(f"{API_URL}/entry", params={"client": st.session_state.client})
                if response.status_code == 200:
                    entries = response.json()
                    unique_rooms = sorted(set(entry.get("room", "") for entry in entries))
                    room = st.selectbox("Room", [""] + list(unique_rooms))
                else:
                    room = st.text_input("Room")
            except:
                room = st.text_input("Room")
            
            # If a room is selected, try to get camera sectors for that room
            sectors = []
            if room:
                try:
                    cam_response = requests.get(f"{API_URL}/cam", 
                                               params={"client": st.session_state.client, "room": room})
                    if cam_response.status_code == 200:
                        cameras = cam_response.json()
                        if isinstance(cameras, list):
                            sectors = sorted(set(cam.get("sector", 1) for cam in cameras))
                        elif isinstance(cameras, dict):
                            sectors = [cameras.get("sector", 1)]
                except:
                    pass
            
            if sectors:
                selected_sectors = st.multiselect("Sectors", sectors, default=sectors)
                sectors_str = ",".join(map(str, selected_sectors))
            else:
                sectors_str = st.text_input("Sectors (comma separated numbers)", "1,2,3")
            
            col1, col2 = st.columns(2)
            with col1:
                crop = st.checkbox("Crop Images", value=True)
                shape = st.selectbox("Shape", ["auto", "rectangle", "circle", "oval"])
            with col2:
                color = st.selectbox("Border Color", ["blue", "red", "green", "yellow"])
                format = st.selectbox("Image Format", ["png", "jpg", "jpeg"])
            
            # Submit button
            submitted = st.form_submit_button("Run Detection")
            
            if submitted:
                try:
                    # Parse sectors from string to list of integers
                    if isinstance(sectors_str, str):
                        sector_list = [int(s.strip()) for s in sectors_str.split(",")]
                    else:
                        sector_list = sectors_str
                    
                    # Prepare request payload
                    payload = {
                        "control": control,
                        "current": current,
                        "sectors": sector_list,
                        "client": st.session_state.client,
                        "room": room,
                        "crop": crop,
                        "color": color,
                        "shape": shape,
                        "format": format
                    }
                    
                    # Make API request
                    response = requests.get(f"{API_URL}/detect", params=payload)
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        if result:
                            st.success(f"Detection completed! Found stains in {len(result)} sectors.")
                            
                            # Display results
                            for sector, data in result.items():
                                st.subheader(f"Sector {sector}")
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.image(f"imagedata/control/{data['control']}", caption="Control Image", width=300)
                                with col2:
                                    st.image(f"{data['highlight']}", caption="Highlighted Stains", width=300)
                        else:
                            st.info("No stains detected!")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Schedule Page
elif page == "Schedule":
    st.title("Schedule Management")
    
    if not st.session_state.client:
        st.warning("Please select a client in the sidebar")
    else:
        tabs = st.tabs(["View Schedule", "Add Entry", "Update Entry", "Delete Entry"])
        
        with tabs[0]:
            st.subheader("Current Schedule")
            
            # Fetch schedule entries
            try:
                response = requests.get(f"{API_URL}/entry", params={"client": st.session_state.client})
                
                if response.status_code == 200:
                    entries = response.json()
                    
                    if entries:
                        # Convert to DataFrame for better display
                        df = pd.DataFrame(entries)
                        
                        # Process time columns for better display
                        if 'start' in df.columns:
                            df['start_time'] = df['start'].apply(lambda x: x.split('T')[-1] if 'T' in str(x) else x)
                        if 'end' in df.columns:
                            df['end_time'] = df['end'].apply(lambda x: x.split('T')[-1] if 'T' in str(x) else x)
                        
                        # Display the schedule
                        st.dataframe(df, use_container_width=True)
                        
                        # Additional filters
                        with st.expander("Filter Results"):
                            room_filter = st.text_input("Filter by Room")
                            if room_filter:
                                filtered_df = df[df['room'].str.contains(room_filter, case=False)]
                                st.dataframe(filtered_df, use_container_width=True)
                    else:
                        st.info("No schedule entries found")
                else:
                    st.error(f"Error fetching schedule: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with tabs[1]:
            st.subheader("Add Schedule Entry")
            
            with st.form("add_schedule_form"):
                # Get existing rooms from API to populate dropdown
                try:
                    response = requests.get(f"{API_URL}/entry", params={"client": st.session_state.client})
                    if response.status_code == 200:
                        entries = response.json()
                        unique_rooms = sorted(set(entry.get("room", "") for entry in entries if "room" in entry))
                        room = st.selectbox("Room", [""] + list(unique_rooms) + ["New Room..."], accept_new_options = True)
                        
                        if room == "New Room...":
                            room = st.text_input("Enter New Room Name")
                    else:
                        room = st.text_input("Room")
                except:
                    room = st.text_input("Room")
                
                label = st.text_input("Label")
                
                col1, col2 = st.columns(2)
                with col1:
                    start_hour = st.number_input("Start Hour", min_value=0, max_value=23, value=8)
                    start_minute = st.number_input("Start Minute", min_value=0, max_value=59, value=0)
                with col2:
                    end_hour = st.number_input("End Hour", min_value=0, max_value=23, value=17)
                    end_minute = st.number_input("End Minute", min_value=0, max_value=59, value=0)
                
                # If room is selected, try to get camera sectors for that room
                sectors = []
                if room and room != "New Room...":
                    try:
                        cam_response = requests.get(f"{API_URL}/cam", 
                                                   params={"client": st.session_state.client, "room": room})
                        if cam_response.status_code == 200:
                            cameras = cam_response.json()
                            if isinstance(cameras, list):
                                sectors = sorted(set(cam.get("sector", 1) for cam in cameras))
                            elif isinstance(cameras, dict):
                                sectors = [cameras.get("sector", 1)]
                    except:
                        pass
                
                if sectors:
                    selected_sectors = st.multiselect("Sectors", sectors, default=sectors)
                else:
                    sectors_str = st.text_input("Sectors (comma separated numbers)", "1,2,3")
                    selected_sectors = [int(s.strip()) for s in sectors_str.split(",")]
                
                days = st.multiselect(
                    "Days",
                    ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    default=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                )
                
                submitted = st.form_submit_button("Add Schedule Entry")
                
                if submitted:
                    try:
                        # Create time objects
                        start_time = time(hour=start_hour, minute=start_minute)
                        end_time = time(hour=end_hour, minute=end_minute)
                        
                        # Prepare payload
                        payload = {
                            "client": st.session_state.client,
                            "room": room,
                            "label": label,
                            "start": start_time.isoformat(),
                            "end": end_time.isoformat(),
                            "sectors": selected_sectors,
                            "days": days
                        }
                        
                        # Make API request
                        response = requests.post(f"{API_URL}/entry/add", json=payload)
                        
                        if response.status_code == 200:
                            st.success("Schedule entry added successfully!")
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with tabs[2]:
            st.subheader("Update Schedule Entry")
            
            # First, fetch all entries to let user select one
            try:
                response = requests.get(f"{API_URL}/entry", params={"client": st.session_state.client})
                
                if response.status_code == 200:
                    entries = response.json()
                    
                    if entries:
                        # Create selection options
                        entry_options = {f"{e['id']} - {e['label']} ({e['room']})": e for e in entries}
                        selected_entry_key = st.selectbox("Select Entry to Update", list(entry_options.keys()))
                        selected_entry = entry_options[selected_entry_key]
                        
                        with st.form("update_schedule_form"):
                            # Pre-fill form with current values
                            room = st.text_input("Room", value=selected_entry["room"])
                            label = st.text_input("Label", value=selected_entry["label"])
                            
                            # Parse time values
                            current_start = time.fromisoformat(selected_entry["start"])
                            current_end = time.fromisoformat(selected_entry["end"])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                start_hour = st.number_input("Start Hour", min_value=0, max_value=23, value=current_start.hour)
                                start_minute = st.number_input("Start Minute", min_value=0, max_value=59, value=current_start.minute)
                            with col2:
                                end_hour = st.number_input("End Hour", min_value=0, max_value=23, value=current_end.hour)
                                end_minute = st.number_input("End Minute", min_value=0, max_value=59, value=current_end.minute)
                            
                            # Get sectors for this room
                            try:
                                cam_response = requests.get(f"{API_URL}/cam", 
                                                         params={"client": st.session_state.client, "room": room})
                                if cam_response.status_code == 200:
                                    cameras = cam_response.json()
                                    if isinstance(cameras, list):
                                        available_sectors = sorted(set(cam.get("sector", 1) for cam in cameras))
                                    elif isinstance(cameras, dict):
                                        available_sectors = [cameras.get("sector", 1)]
                                    
                                    current_sectors = selected_entry.get("sectors", [])
                                    sectors = st.multiselect("Sectors", available_sectors, default=current_sectors)
                                else:
                                    current_sectors_str = ",".join(map(str, selected_entry.get("sectors", [])))
                                    sectors_str = st.text_input("Sectors (comma separated numbers)", current_sectors_str)
                                    sectors = [int(s.strip()) for s in sectors_str.split(",")]
                            except:
                                current_sectors_str = ",".join(map(str, selected_entry.get("sectors", [])))
                                sectors_str = st.text_input("Sectors (comma separated numbers)", current_sectors_str)
                                sectors = [int(s.strip()) for s in sectors_str.split(",")]
                            
                            days = st.multiselect(
                                "Days",
                                ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                default=selected_entry.get("days", [])
                            )
                            
                            submitted = st.form_submit_button("Update Schedule Entry")
                            
                            if submitted:
                                try:
                                    # Create time objects
                                    start_time = time(hour=start_hour, minute=start_minute)
                                    end_time = time(hour=end_hour, minute=end_minute)
                                    
                                    # Prepare payload
                                    payload = {
                                        "room": room,
                                        "label": label,
                                        "start": start_time.isoformat(),
                                        "end": end_time.isoformat(),
                                        "sectors": sectors,
                                        "days": days
                                    }
                                    
                                    # Make API request
                                    response = requests.post(
                                        f"{API_URL}/entry/update",
                                        params={"client": st.session_state.client, "id": selected_entry["id"]},
                                        json=payload
                                    )
                                    
                                    if response.status_code == 200:
                                        st.success("Schedule entry updated successfully!")
                                    else:
                                        st.error(f"Error: {response.status_code} - {response.text}")
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
                    else:
                        st.info("No schedule entries found to update")
                else:
                    st.error(f"Error fetching schedule: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with tabs[3]:
            st.subheader("Delete Schedule Entry")
            
            delete_option = st.radio("Delete by", ["Single Entry", "Room", "Multiple Entries"])
            
            if delete_option == "Single Entry":
                # Fetch entries for selection
                try:
                    response = requests.get(f"{API_URL}/entry", params={"client": st.session_state.client})
                    
                    if response.status_code == 200:
                        entries = response.json()
                        
                        if entries:
                            # Create selection options
                            entry_options = {f"{e['id']} - {e['label']} ({e['room']})": e["id"] for e in entries}
                            selected_entry_id = st.selectbox("Select Entry to Delete", list(entry_options.keys()))
                            entry_id = entry_options[selected_entry_id]
                            
                            if st.button("Delete Entry"):
                                response = requests.post(
                                    f"{API_URL}/entry/deleteone",
                                    params={"id": entry_id, "client": st.session_state.client, "room": ""}
                                )
                                
                                if response.status_code == 200:
                                    st.success("Entry deleted successfully!")
                                else:
                                    st.error(f"Error: {response.status_code} - {response.text}")
                        else:
                            st.info("No entries found")
                    else:
                        st.error(f"Error fetching entries: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            elif delete_option == "Room":
                # Get room list
                try:
                    response = requests.get(f"{API_URL}/entry", params={"client": st.session_state.client})
                    
                    if response.status_code == 200:
                        entries = response.json()
                        
                        if entries:
                            # Extract unique rooms
                            rooms = list(set(e["room"] for e in entries if "room" in e))
                            selected_room = st.selectbox("Select Room", rooms)
                            
                            if st.button("Delete All Entries for Room"):
                                response = requests.post(
                                    f"{API_URL}/entry/delete",
                                    params={"client": st.session_state.client, "room": selected_room}
                                )
                                
                                if response.status_code == 200:
                                    st.success(f"All entries for room '{selected_room}' deleted!")
                                else:
                                    st.error(f"Error: {response.status_code} - {response.text}")
                        else:
                            st.info("No entries found")
                    else:
                        st.error(f"Error fetching entries: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
            
            elif delete_option == "Multiple Entries":
                # Fetch entries for selection
                try:
                    response = requests.get(f"{API_URL}/entry", params={"client": st.session_state.client})
                    
                    if response.status_code == 200:
                        entries = response.json()
                        
                        if entries:
                            # Create selection options
                            entry_options = {f"{e['id']} - {e['label']} ({e['room']})": e["id"] for e in entries}
                            selected_entries = st.multiselect("Select Entries to Delete", list(entry_options.keys()))
                            entry_ids = [entry_options[entry] for entry in selected_entries]
                            
                            if st.button("Delete Selected Entries"):
                                response = requests.post(
                                    f"{API_URL}/entry/delete",
                                    params={"client": st.session_state.client},
                                    json={"id": entry_ids}
                                )
                                
                                if response.status_code == 200:
                                    st.success(f"{len(entry_ids)} entries deleted successfully!")
                                else:
                                    st.error(f"Error: {response.status_code} - {response.text}")
                        else:
                            st.info("No entries found")
                    else:
                        st.error(f"Error fetching entries: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

# Camera Management Page
elif page == "Camera Management":
    st.title("Camera Management")
    
    if not st.session_state.client:
        st.warning("Please select a client in the sidebar")
    else:
        tabs = st.tabs(["View Cameras", "Add Camera", "Update Camera", "Delete Camera", "Bulk Import"])
        
        with tabs[0]:
            st.subheader("Camera List")
            
            # Create filters for viewing cameras
            col1, col2 = st.columns(2)
            with col1:
                # Get rooms from schedule entries to populate filter
                try:
                    response = requests.get(f"{API_URL}/entry", params={"client": st.session_state.client})
                    if response.status_code == 200:
                        entries = response.json()
                        unique_rooms = sorted(set(entry.get("room", "") for entry in entries if "room" in entry))
                        room_filter = st.selectbox("Filter by Room", ["All Rooms"] + list(unique_rooms))
                    else:
                        room_filter = st.text_input("Filter by Room")
                except:
                    room_filter = st.text_input("Filter by Room")
            
            with col2:
                sector_filter = st.number_input("Filter by Sector", min_value=0, value=0, 
                                               help="Enter 0 to show all sectors")
            
            # Fetch camera data based on filters
            # try:
            if room_filter and room_filter != "All Rooms":
                if sector_filter > 0:
                    # Get specific room and sector
                    response = requests.get(
                        f"{API_URL}/cam",
                        params={
                            "client": st.session_state.client,
                            "room": room_filter,
                            "sector": sector_filter
                        }
                    )
                else:
                    # Get all cameras in a room
                    response = requests.get(
                        f"{API_URL}/cam",
                        params={
                            "client": st.session_state.client,
                            "room": room_filter
                        }
                    )
            else:
                # Get all cameras for client
                response = requests.get(
                    f"{API_URL}/cam",
                    params={"client": st.session_state.client}
                )
            
            if response.status_code == 200:
                cameras = response.json()
                
                # Convert to list if single camera returned
                if isinstance(cameras, dict):
                    cameras = [cameras]
                
                if cameras and len(cameras) > 0:
                    # Convert to DataFrame for display
                    df = pd.DataFrame(cameras)
                    st.dataframe(df, use_container_width=True)
                    
                    def camcapture(rtsp_url: str) -> Image.Image:
                        """
                        Capture a single frame from an RTSP stream and return it as a PIL Image.

                        Args:
                            rtsp_url (str): The RTSP URL of the IP camera.

                        Returns:
                            PIL.Image.Image: A PIL Image of the current frame.
                        """
                        cap = cv2.VideoCapture(rtsp_url)
                        if not cap.isOpened():
                            raise ValueError(f"Unable to open RTSP stream: {rtsp_url}")

                        ret, frame = cap.read()
                        cap.release()

                        if not ret:
                            raise RuntimeError("Failed to read frame from stream.")

                        # Convert from BGR (OpenCV) to RGB (PIL)
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        return Image.fromarray(frame_rgb)

                    # Display camera previews
                    st.subheader("Camera Previews")
                    preview_columns = st.columns(3)
                    
                    for i, camera in enumerate(cameras):
                        col_idx = i % 3
                        
                        with preview_columns[col_idx]:
                            if st.button(f" Room: {camera['room']}, Sector: {camera['sector']}"):
                                with st.expander(f"Room: {camera['room']}, Sector: {camera['sector']}",True):
                                    # st.write(type(camcapture(camera["link"])))
                                    st.image(camcapture(camera["link"]))
                else:
                    st.info("No cameras found matching the criteria")
            else:
                st.error(f"Error fetching cameras: {response.status_code} - {response.text}")
            # except Exception as e:
            #     st.error(f"Error: {str(e.with_traceback())}")
        
        with tabs[1]:
            st.subheader("Add Camera")
            
            with st.form("add_camera_form"):
                # Get existing rooms from API to populate dropdown
                try:
                    response = requests.get(f"{API_URL}/entry", params={"client": st.session_state.client})
                    if response.status_code == 200:
                        entries = response.json()
                        unique_rooms = sorted(set(entry.get("room", "") for entry in entries if "room" in entry))
                        room = st.selectbox("Room", [""] + list(unique_rooms) + ["New Room..."], accept_new_options =True)
                        
                        if room == "New Room...":
                            room = st.text_input("Enter New Room Name")
                    else:
                        room = st.text_input("Room")
                except:
                    room = st.text_input("Room")
                
                sector = st.number_input("Sector", min_value=1, value=1)
                link = st.text_input("Camera Link")
                
                # Preview link if it's an image
                if link and link.lower().endswith(('.png', '.jpg', '.jpeg')):
                    st.image(link, caption="Link Preview", width=300)
                
                submitted = st.form_submit_button("Add Camera")
                
                if submitted:
                    try:
                        # Prepare payload
                        payload = {
                            "id": "",  # API will generate UUID
                            "client": st.session_state.client,
                            "room": room,
                            "sector": sector,
                            "link": link
                        }
                        
                        # Make API request
                        response = requests.post(f"{API_URL}/cam", json=payload)
                        
                        if response.status_code == 200:
                            st.success("Camera added successfully!")
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with tabs[2]:
            st.subheader("Update Camera")
            
            search_option = st.radio("Search by", ["Room & Sector", "Camera ID"])
            
            if search_option == "Room & Sector":
                room = st.text_input("Room")
                sector = st.number_input("Sector", min_value=1, value=1)
                
                if st.button("Find Camera"):
                    try:
                        # Make API request
                        response = requests.get(
                            f"{API_URL}/cam",
                            params={
                                "client": st.session_state.client,
                                "room": room,
                                "sector": sector
                            }
                        )
                        
                        if response.status_code == 200:
                            camera = response.json()
                            
                            st.session_state.camera_id = camera["id"]
                            st.session_state.camera_data = camera
                            
                            # Show update form
                            with st.form("update_camera_form"):
                                new_room = st.text_input("New Room", value=camera["room"])
                                new_sector = st.number_input("New Sector", min_value=1, value=camera["sector"])
                                new_link = st.text_input("New Camera Link", value=camera["link"])
                                
                                update_submitted = st.form_submit_button("Update Camera")
                                
                                if update_submitted:
                                    # Prepare payload
                                    payload = {
                                        "room": new_room,
                                        "sector": new_sector,
                                        "link": new_link
                                    }
                                    
                                    # Make update request
                                    update_response = requests.post(
                                        f"{API_URL}/cam/update",
                                        params={
                                            "client": st.session_state.client,
                                            "id": camera["id"]
                                        },
                                        json=payload
                                    )
                                    
                                    if update_response.status_code == 200:
                                        st.success("Camera updated successfully!")
                                    else:
                                        st.error(f"Error: {update_response.status_code} - {update_response.text}")
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            elif search_option == "Camera ID":
                camera_id = st.text_input("Camera ID")
                
                if st.button("Find Camera"):
                    try:
                        # Make API request
                        response = requests.get(
                            f"{API_URL}/cam",
                            params={
                                "client": st.session_state.client,
                                "id": camera_id
                            }
                        )
                        
                        if response.status_code == 200:
                            camera = response.json()
                            
                            # Show update form
                            with st.form("update_camera_form_by_id"):
                                new_room = st.text_input("New Room", value=camera["room"])
                                new_sector = st.number_input("New Sector", min_value=1, value=camera["sector"])
                                new_link = st.text_input("New Camera Link", value=camera["link"])
                                
                                update_submitted = st.form_submit_button("Update Camera")
                                
                                if update_submitted:
                                    # Prepare payload
                                    payload = {
                                        "room": new_room,
                                        "sector": new_sector,
                                        "link": new_link
                                    }
                                    
                                    # Make update request
                                    update_response = requests.post(
                                        f"{API_URL}/cam/update",
                                        params={
                                            "client": st.session_state.client,
                                            "id": camera_id
                                        },
                                        json=payload
                                    )
                                    
                                    if update_response.status_code == 200:
                                        st.success("Camera updated successfully!")
                                    else:
                                        st.error(f"Error: {update_response.status_code} - {update_response.text}")
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with tabs[3]:
            st.subheader("Delete Camera")
            
            delete_option = st.radio("Delete by", ["Room & Sector", "Camera ID", "All in Room"])
            
            if delete_option == "Room & Sector":
                room = st.text_input("Room", key = "roomenter")
                sector = st.number_input("Sector", min_value=1, value=1, key = "keyentry")
                
                if st.button("Delete Camera"):
                    try:
                        # Make API request
                        response = requests.post(
                            f"{API_URL}/cam/delete",
                            params={
                                "client": st.session_state.client,
                                "room": room,
                                "sector": sector
                            }
                        )
                        
                        if response.status_code == 200:
                            st.success(f"Camera in room '{room}', sector {sector} deleted successfully!")
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            elif delete_option == "Camera ID":
                camera_id = st.text_input("Camera ID")
                
                if st.button("Delete Camera"):
                    try:
                        # Make API request
                        response = requests.post(
                            f"{API_URL}/cam/delete",
                            params={
                                "client": st.session_state.client,
                                "id": camera_id
                            }
                        )
                        
                        if response.status_code == 200:
                            st.success(f"Camera with ID '{camera_id}' deleted successfully!")
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            elif delete_option == "All in Room":
                room = st.text_input("Room")
                
                if st.button("Delete All Cameras in Room"):
                    try:
                        # Make API request
                        response = requests.post(
                            f"{API_URL}/cam/delete",
                            params={
                                "client": st.session_state.client,
                                "room": room
                            }
                        )
                        
                        if response.status_code == 200:
                            st.success(f"All cameras in room '{room}' deleted successfully!")
                        else:
                            st.error(f"Error: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with tabs[4]:
            st.subheader("Bulk Import Cameras")
            
            st.write("Upload a CSV file with camera data. Required columns: room, sector, link")
            
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            
            if uploaded_file is not None:
                try:
                    # Read the CSV file
                    df = pd.read_csv(uploaded_file)
                    
                    # Validate required columns
                    required_columns = ["room", "sector", "link"]
                    if not all(col in df.columns for col in required_columns):
                        st.error(f"CSV file must contain these columns: {', '.join(required_columns)}")
                    else:
                        # Display preview
                        st.write("Preview of uploaded data:")
                        st.dataframe(df.head())
                        
                        if st.button("Import Cameras"):
                            progress_bar = st.progress(0)
                            success_count = 0
                            error_count = 0
                            error_messages = []
                            
                            for i, row in df.iterrows():
                                try:
                                    # Prepare payload
                                    payload = {
                                        "id": "",  # API will generate UUID
                                        "client": st.session_state.client,
                                        "room": str(row["room"]),
                                        "sector": int(row["sector"]),
                                        "link": str(row["link"])
                                    }
                                    
                                    # Make API request
                                    response = requests.post(f"{API_URL}/cam", json=payload)
                                    
                                    if response.status_code == 200:
                                        success_count += 1
                                    else:
                                        error_count += 1
                                        error_messages.append(f"Row {i+1}: {response.text}")
                                except Exception as e:
                                    error_count += 1
                                    error_messages.append(f"Row {i+1}: {str(e)}")
                                
                                # Update progress
                                progress_bar.progress((i + 1) / len(df))
                            
                            # Show results
                            st.success(f"Successfully imported {success_count} cameras")
                            if error_count > 0:
                                st.error(f"Failed to import {error_count} cameras")
                                with st.expander("Error Details"):
                                    for msg in error_messages:
                                        st.write(msg)
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")

# Reports Page
elif page == "Reports":
    st.title("Reports")
    
    if not st.session_state.client:
        st.warning("Please select a client in the sidebar")
    else:
        st.subheader("Generate Reports")
        
        # Room selection
        room = st.text_input("Room")
        
        # Date range selection
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", datetime.now().replace(day=1))
        with col2:
            end_date = st.date_input("End Date", datetime.now())
        
        # Button to generate report
        if st.button("Generate Report"):
            if not room:
                st.error("Please enter a room name")
            else:
                try:
                    # Convert date to datetime with time set to beginning/end of day
                    start_datetime = datetime.combine(start_date, datetime.min.time())
                    end_datetime = datetime.combine(end_date, datetime.max.time())
                    
                    # Make API request
                    response = requests.post(
                        f"{API_URL}/report",
                        params={
                            "room": room,
                            "client": st.session_state.client
                        },
                        json={
                            "start": start_datetime.isoformat(),
                            "end": end_datetime.isoformat()
                        }
                    )
                    
                    if response.status_code == 200:
                        report_data = response.json()
                        
                        if report_data:
                            # Convert to DataFrame for better display
                            df = pd.DataFrame(report_data)
                            
                            # Basic stats
                            total_detections = sum(item.get("detections", 0) for item in report_data)
                            
                            st.success(f"Report generated successfully! Found {total_detections} detections.")
                            
                            # Display metrics
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Detections", total_detections)
                            with col2:
                                st.metric("Date Range", f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d')}")
                            with col3:
                                st.metric("Number of Records", len(report_data))
                            
                            # Display detailed data
                            st.subheader("Detection Records")
                            st.dataframe(df, use_container_width=True)
                            
                            # Option to download as CSV
                            csv = df.to_csv(index=False)
                            st.download_button(
                                label="Download CSV",
                                data=csv,
                                file_name=f"tabsense_report_{room}_{start_date}_{end_date}.csv",
                                mime="text/csv"
                            )
                            
                            # Visualization section
                            st.subheader("Visualization")
                            
                            # Convert timestamp to date for grouping
                            if 'timestamp' in df.columns:
                                df['date'] = pd.to_datetime(df['timestamp']).dt.date
                                
                                # Group by date and count detections
                                detections_by_date = df.groupby('date')['detections'].sum().reset_index()
                                
                                # Plot
                                st.line_chart(detections_by_date.set_index('date'))
                        else:
                            st.info("No detection data found for the selected criteria")
                    else:
                        st.error(f"Error: {response.status_code} - {response.text}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Example of custom report
        with st.expander("Custom Reports"):
            st.write("Here you can define and run custom reports based on specific criteria.")