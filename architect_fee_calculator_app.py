
import streamlit as st
import pandas as pd

st.title("🏗️ Architect Fee Calculator")

# Input: Construction details
st.header("Project Info")
construction_cost = st.number_input("Estimated Construction Cost ($)", min_value=0, value=1_000_000)
base_fee_percent = st.number_input("Base Fee % of Construction Cost", min_value=0.0, value=0.08)
complexity_factor = st.number_input("Complexity Factor", min_value=0.5, value=1.1)
location_factor = st.number_input("Location Factor", min_value=0.5, value=1.0)
risk_factor = st.number_input("Risk Factor", min_value=0.5, value=1.05)
firm_multiplier = st.number_input("Firm Multiplier (Overhead + Profit)", min_value=1.0, value=3.0)

# Input: Hourly rates
st.header("Hourly Rates ($)")
rates = {
    "Principal": st.number_input("Principal", value=200),
    "Project Manager": st.number_input("Project Manager", value=150),
    "Architect": st.number_input("Architect", value=100),
    "Drafter": st.number_input("Drafter", value=75)
}

# Input: Hours per phase
st.header("Estimated Hours per Phase and Role")
phases = ['Pre-Design', 'Schematic Design', 'Design Development', 
          'Construction Documents', 'Bidding/Negotiation', 'Construction Administration']
roles = list(rates.keys())

hours_data = {}
for phase in phases:
    st.subheader(phase)
    hours_data[phase] = {role: st.number_input(f"{phase} - {role}", min_value=0, value=10) for role in roles}

# Calculate total raw labor cost
total_raw_labor_cost = sum(hours_data[phase][role] * rates[role] for phase in phases for role in roles)

# Workplan Method Fee
workplan_fee = total_raw_labor_cost * firm_multiplier

# Construction Cost % Fee
adjusted_fee_percent = base_fee_percent * complexity_factor * location_factor * risk_factor
construction_cost_fee = construction_cost * adjusted_fee_percent

# Output
st.header("💰 Fee Summary")
st.write(f"**Total Raw Labor Cost:** ${total_raw_labor_cost:,.2f}")
st.write(f"**Workplan Method Fee:** ${workplan_fee:,.2f}")
st.write(f"**Construction Cost % Method Fee:** ${construction_cost_fee:,.2f}")

# Display data table
if st.checkbox("Show Detailed Hours Table"):
    df = pd.DataFrame.from_dict(hours_data, orient="index")
    st.dataframe(df)
