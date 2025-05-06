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
st.sidebar.image("tabsense logo (Custom).png")
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
            # These would be replaced with actual API calls in a real implementation
            with col1:
                st.metric("Total Rooms", "5")
            with col2:
                st.metric("Active Cameras", "12")
            with col3:
                st.metric("Detections Today", "3", delta="2")
        except:
            st.warning("Could not fetch client statistics")

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
            room = st.text_input("Room")
            sectors = st.text_input("Sectors (comma separated numbers)", "1,2,3")
            
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
                    sector_list = [int(s.strip()) for s in sectors.split(",")]
                    
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
                room = st.text_input("Room")
                label = st.text_input("Label")
                
                col1, col2 = st.columns(2)
                with col1:
                    start_hour = st.number_input("Start Hour", min_value=0, max_value=23, value=8)
                    start_minute = st.number_input("Start Minute", min_value=0, max_value=59, value=0)
                with col2:
                    end_hour = st.number_input("End Hour", min_value=0, max_value=23, value=17)
                    end_minute = st.number_input("End Minute", min_value=0, max_value=59, value=0)
                
                sectors = st.text_input("Sectors (comma separated numbers)", "1,2,3")
                
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
                        
                        # Parse sectors
                        sector_list = [int(s.strip()) for s in sectors.split(",")]
                        
                        # Prepare payload
                        payload = {
                            "client": st.session_state.client,
                            "room": room,
                            "label": label,
                            "start": start_time.isoformat(),
                            "end": end_time.isoformat(),
                            "sectors": sector_list,
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
        tabs = st.tabs(["View Cameras", "Add Camera", "Update Camera", "Delete Camera"])
        
        with tabs[0]:
            st.subheader("Camera List")
            
            # Here we would fetch camera data from the API
            # This is a placeholder implementation
            try:
                response = requests.get(f"{API_URL}/cam")
                # In a real implementation, we would make an API call to get all cameras
                # Since there's no direct endpoint for that, we'll display a message
                st.info("Use the other tabs to manage cameras. View functionality would need custom API endpoint.")
                
                # Example of how this might look with a real API endpoint
                room_filter = st.text_input("Filter by Room")
                if room_filter and st.button("Search Cameras"):
                    st.text("This would show cameras for the specified room")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        with tabs[1]:
            st.subheader("Add Camera")
            
            with st.form("add_camera_form"):
                room = st.text_input("Room")
                sector = st.number_input("Sector", min_value=1, value=1)
                link = st.text_input("Camera Link")
                
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
                room = st.text_input("Room")
                sector = st.number_input("Sector", min_value=1, value=1)
                
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
                    start_datetime = datetime.combine(start_date, time.min)
                    end_datetime = datetime.combine(end_date, time.max)
                    
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