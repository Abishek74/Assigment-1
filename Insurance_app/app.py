import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
from models.policyholder import Policyholder
from models.claim import Claim
from models.risk_analysis import *
from utils.reports import *
import datetime 


# File paths
PH_FILE = "data/policyholders.json"
CL_FILE = "data/claims.json"

# Load or initialize data
def load_data(file):
    return json.load(open(file)) if os.path.exists(file) else []

def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

policyholders = load_data(PH_FILE)
claims = load_data(CL_FILE)

st.title("Insurance Claims Management System")
menu = st.sidebar.radio("Choose Module", [
    "Register Policyholder",
    "Add Claim",
    "Update Claim Status",
    "Risk Analysis",
    "Report"
])

if menu == "Register Policyholder":
    st.header("Register Policyholder")
    name = st.text_input("Name")
    age = st.number_input("Age", 18, 100)
    policy_type = st.selectbox("Policy Type", ["Select Option","Health", "Vehicle", "Life"])
    sum_insured = st.number_input("Sum Insured",1000)
    registration_date = st.date_input("Registration Date", value=datetime.date.today())

    if st.button("Register"):
        # Validation
        if not name.strip():
            st.error("Name cannot be empty.")
        elif not name.replace(" ", "").isalpha():
            st.error("Name must contain only letters and spaces, no speacial symbols.")
        elif registration_date > datetime.date.today():
            st.error("Registration date cannot be in the future.")
        else:
            pid = len(policyholders) + 1
            new_ph = Policyholder(pid, name, age, policy_type, sum_insured, registration_date.strftime('%Y-%m-%d'))
            policyholders.append(new_ph.to_dict())
            save_data(PH_FILE, policyholders)
            st.success(f"Policyholder {name} registered with ID {pid}")#

elif menu == "Add Claim":
    st.header("Add Claim")
    pid = st.number_input("Policyholder ID",min_value=1)
    amount = st.number_input("Claim Amount", min_value=1000)
    reason = st.text_input("Reason for Claim")
    status = st.selectbox("Claim Status", ["Select option","Pending", "Approved", "Rejected"])
    claim_date = st.date_input("Claim Date (optional)", value=None)

    if st.button("Submit Claim"):
        ph_ids = [p["policyholder_id"] for p in policyholders]
        # Validations
        if pid not in ph_ids:
            st.error(f"Policyholder ID {pid} not found.")
        elif claim_date and claim_date > datetime.date.today():
            st.error("Claim date cannot be in the future.")
        elif not reason.strip():
            st.error("Reason for claim cannot be empty.")
        else:
            cid = len(claims) + 1
            date_str = claim_date.strftime('%Y-%m-%d') if claim_date else None
            new_claim = Claim(cid, pid, amount, reason, status, date_str)
            claims.append(new_claim.to_dict())
            save_data(CL_FILE, claims)
            st.success(f"Claim ID {cid} added for Policyholder {pid}")
#Update claim status
elif menu == "Update Claim Status":
    st.header("Update Claim Status")
    cid = st.number_input("Enter Claim ID", min_value=1)
    claim = next((c for c in claims if c['claim_id'] == cid), None)#

    if claim:
        st.write(f"Current Status: **{claim['status']}**")
        new_status = st.selectbox("New Status", ["Pending", "Approved", "Rejected"],index=["Pending", "Approved", "Rejected"].index(claim["status"]))
        if st.button("Update Status"):
            claim['status'] = new_status
            save_data(CL_FILE, claims)
            st.success(f"Claim ID {cid} status updated to {new_status}")
    else:
        st.warning("Claim not found.")
#risk Analysing
elif menu == "Risk Analysis":
    st.header("High-Risk Policyholders")
    for p in policyholders:
        if is_high_risk(claims, p):
            st.warning(f"{p['name']} (ID: {p['policyholder_id']}) is HIGH RISK")

    st.subheader(" Claims by Policy Type")
    st.json(aggregate_by_policy_type(claims, policyholders))
#Report
elif menu == "Report":
    st.header("Report")

    # Average Claim per Policy Type
    st.subheader(" Average Claim per Policy Type")
    if claims and policyholders:
        df_claims = pd.DataFrame(claims)
        df_ph = pd.DataFrame(policyholders)
        merged = df_claims.merge(df_ph, on="policyholder_id")
        avg_by_type = merged.groupby("policy_type")["amount"].mean().reset_index()
        cols = st.columns(len(avg_by_type))
        for i, row in avg_by_type.iterrows():
            with cols[i]:
                st.metric(label=row["policy_type"], value=f"₹ {row['amount']:.2f}")
    else:
        st.info("Not enough data to show average claims.")

    # Filtering
    st.subheader(" Filter by Policy Type")
    all_policy_types = list(set([p["policy_type"] for p in policyholders])) if policyholders else []
    selected_policy_type = st.selectbox("Select Policy Type", ["All"] + all_policy_types)

    #Policy Registrations per Month , Claims Per Month
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("Policy Registrations per Month")
        if policyholders:
            df_ph = pd.DataFrame(policyholders)
            if selected_policy_type != "All":
                df_ph = df_ph[df_ph["policy_type"] == selected_policy_type]
            if "registration_date" in df_ph.columns:
                df_ph["registration_month"] = pd.to_datetime(df_ph["registration_date"]).dt.strftime('%b %Y')
            else:
                df_ph["registration_month"] = pd.Timestamp.today().strftime('%b %Y')
            reg_counts = df_ph.groupby("registration_month").size().reset_index(name="count")
            st.bar_chart(reg_counts.set_index("registration_month"))
        else:
            st.info("No policyholders registered yet.")

    with col2:
        st.markdown("Claims Per Month")
        if claims:
            df_cl = pd.DataFrame(claims)
            df_ph = pd.DataFrame(policyholders)
            if selected_policy_type != "All":
                df_ph = df_ph[df_ph["policy_type"] == selected_policy_type]
            merged = df_cl.merge(df_ph, on="policyholder_id")
            if "claim_date" in merged.columns:
                merged["month"] = pd.to_datetime(merged["claim_date"]).dt.strftime('%b %Y')
                claims_by_month = merged.groupby("month").size().reset_index(name="claims")
                st.line_chart(claims_by_month.set_index("month"))
            else:
                st.info("Claim dates are missing.")
        else:
            st.info("No claims submitted yet.")
