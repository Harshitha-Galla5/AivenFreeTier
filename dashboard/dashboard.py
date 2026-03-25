import streamlit as st
import requests

st.title(" DevOps Incident Dashboard")

API_URL = "http://localhost:5000"

# fetch logs
logs = requests.get(f"{API_URL}/logs").json()
incidents = requests.get(f"{API_URL}/incidents").json()

st.subheader("Logs")
st.write(logs)

st.subheader("Incidents")
st.write(incidents)
