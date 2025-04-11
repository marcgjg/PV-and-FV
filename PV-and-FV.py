import streamlit as st
import numpy as np
import pandas as pd

def main():
    st.title("Future Value / Present Value Visualizer (Comparison Mode)")

    # Session state to hold all the curves the user adds
    if "curves" not in st.session_state:
        # We'll store curves in a dict with the key as a label, 
        # and the value as a Pandas Series (indexed by year)
        st.session_state["curves"] = {}

    # ------------------------
    # Column Layout
    # ------------------------
    col1, col2 = st.columns(2)

    with col1:
        # Radio button to choose Future Value vs Present Value
        calculation_type = st.radio(
            "Select Calculation Type:",
            ("Future Value", "Present Value")
        )

        # Slider for the number of years
        years = st.slider("Number of years", min_value=0, max_value=50, value=10)

        # Slider for the interest/discount rate in percentage
        interest_rate_percent = st.slider(
            "Interest/Discount rate (%)",
            min_value=0,
            max_value=20,
            value=5
        )
        interest_rate = interest_rate_percent / 100.0

        # Define a label for the curve
        calc_label = "FV" if calculation_type == "Future Value" else "PV"
        curve_label = f"{calc_label} {interest_rate_percent}% {years}y"

        # Compute the values
        year_range = np.arange(0, years + 1)
        if calculation_type == "Future Value":
            values = 100 * (1 + interest_rate) ** year_range
        else:
            # Present Value
            values = 100 / ((1 + interest_rate) ** year_range)

        # Create a Series with index =
