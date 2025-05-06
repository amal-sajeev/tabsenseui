import streamlit as st
import requests
import json
import subprocess
import pandas as pd
from datetime import datetime, time
import os
from typing import List, Dict, Any

# Configure page
st.set_page_config(
    page_title="TabSense Dashboard",
    page_icon="🔍",
    layout="wide",
)

# Define API URL
API_URL = "http://localhost:8000"

# Define sidebar navigation
st.sidebar.title("TabSense Dashboard")
page = st.sidebar.selectbox(
    "Navigation", 
    ["Home", "Detection", "Schedule", "Camera Management", "Reports"]
)

# Initialize client state
if "client" not in st.session_state:
    st.session_state.client = ""

# Client selection in sidebar
st.sidebar.subheader("Client Selection")
st.session_state.client = st.sidebar.text_input("Client", st.session_state.client)

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
    st.image("https://via.placeholder.com/800x200?text=TabSense+Dashboard", use_column_width=True)
    
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
                        room = st.selectbox("Room", [""] + list(unique_rooms) + ["New Room..."])
                        
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
            try:
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
                        
                        # Display camera previews
                        st.subheader("Camera Previews")
                        preview_columns = st.columns(3)
                        
                        for i, camera in enumerate(cameras):
                            col_idx = i % 3
                            with preview_columns[col_idx]:
                                st.subheader(f"Room: {camera['room']}, Sector: {camera['sector']}")
                                # Check if link is an image URL
                                if camera['link'].lower().endswith(('.png', '.jpg', '.jpeg')):
                                    st.image(camera['link'], caption=f"Camera ID: {camera['id']}", use_column_width=True)
                                else:
                                    st.write(f"Camera Link: {camera['link']}")
                                    st.write("Preview not available (not an image URL)")
                    else:
                        st.info("No cameras found matching the criteria")
                else:
                    st.error(f"Error fetching cameras: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with tabs[1]:
            st.subheader("Add Camera")
            
            with st.form("add_camera_form"):
                # Get existing rooms from API to populate dropdown
                try:
                    response = requests.get(f"{API_URL}/entry", params={"client": st.session_state.client})
                    if response.status_code == 200:
                        entries = response.json()
                        unique_rooms = sorted(set(entry.get("room", "") for entry in entries if "room" in entry))
                        room = st.selectbox("Room", [""] + list(unique_rooms) + ["New Room..."])
                        
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
                # Get existing rooms from API to populate dropdown
                try:
                    response = requests.get(f"{API_URL}/entry", params={"client": st.session_state.client})
                    if response.status_code == 200:
                        entries = response.json()
                        unique_rooms = sorted(set(entry.get("room", "") for entry in entries if "room" in entry))
                        room = st.selectbox("Room", [""] + list(unique_rooms))
                    else:
                        room = st.text_input("Room")
                except:
                    room = st.text_input("Room")
                
                # Get sectors for this room
                if room:
                    try:
                        cam_response =