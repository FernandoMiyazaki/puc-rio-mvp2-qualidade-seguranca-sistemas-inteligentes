import streamlit as st
import requests
import pandas as pd

# Backend API URLs
API_BASE_URL = "http://127.0.0.1:5000"
GET_PATIENTS_URL = f"{API_BASE_URL}/patients"
ADD_PATIENT_URL = f"{API_BASE_URL}/patient"

# Function to fetch all patients from the backend
def fetch_patients():
    response = requests.get(GET_PATIENTS_URL)
    if response.status_code == 200:
        data = response.json()
        return data['patients']
    else:
        st.error("Error fetching patients")
        return []

# Function to add a new patient
def add_patient(patient_data):
    response = requests.post(ADD_PATIENT_URL, json=patient_data)

    # Check response status and content
    st.write("Response status code:", response.status_code)
    st.write("Response content:", response.text)  # This prints the actual response text

    if response.status_code == 200:
        st.success("Patient added successfully!")
    else:
        st.error(f"Error adding patient: {response.json().get('message')}")

# Main Streamlit App
def main():
    st.title("Breast Cancer Diagnosis")

    # Input form to add a new patient
    with st.form(key='patient_form'):
        st.header("Add New Patient")

        name = st.text_input("Name")
        concave_points_worst = st.number_input("Concave Points Worst", min_value=0.0)
        perimeter_worst = st.number_input("Perimeter Worst", min_value=0.0)
        concave_points_mean = st.number_input("Concave Points Mean", min_value=0.0)
        radius_worst = st.number_input("Radius Worst", min_value=0.0)
        perimeter_mean = st.number_input("Perimeter Mean", min_value=0.0)
        area_worst = st.number_input("Area Worst", min_value=0.0)
        radius_mean = st.number_input("Radius Mean", min_value=0.0)
        area_mean = st.number_input("Area Mean", min_value=0.0)

        submit_button = st.form_submit_button("Submit")

        if submit_button:
            # Create a patient dictionary
            patient_data = {
                "name": name,
                "concave_points_worst": concave_points_worst,
                "perimeter_worst": perimeter_worst,
                "concave_points_mean": concave_points_mean,
                "radius_worst": radius_worst,
                "perimeter_mean": perimeter_mean,
                "area_worst": area_worst,
                "radius_mean": radius_mean,
                "area_mean": area_mean
            }

            print(patient_data)

            # Add patient to the backend
            add_patient(patient_data)

    # Display the list of patients
    st.header("Patient List")
    patients = fetch_patients()

    if patients:
        df = pd.DataFrame(patients)
        st.dataframe(df)
    else:
        st.write("No patients found")

if __name__ == "__main__":
    main()