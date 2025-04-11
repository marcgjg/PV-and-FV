import streamlit as st
import numpy as np
import pandas as pd
import uuid

def main():
    st.title("Future Value / Present Value Visualizer (Comparison Mode)")

    # -- Session State Setup --
    if "curves" not in st.session_state:
        # Dictionary: {some_key: (label_string, pandas.Series)}
        st.session_state["curves"] = {}
    if "prev_years" not in st.session_state:
        st.session_state["prev_years"] = None
    if "prev_calc_type" not in st.session_state:
        st.session_state["prev_calc_type"] = None

    # -- Two-column layout for controls and chart --
    col1, col2 = st.columns(2)

    with col1:
        # Select Future Value vs Present Value
        calculation_type = st.radio(
            "Select Calculation Type:",
            ("Future Value", "Present Value")
        )

        # Slider for number of years
        years = st.slider("Number of years", min_value=0, max_value=50, value=10)

        # Slider for interest/discount rate (in %)
        interest_rate_percent = st.slider(
            "Interest/Discount rate (%)",
            min_value=0,
            max_value=20,
            value=5
        )
        interest_rate = interest_rate_percent / 100.0

        # Button to reset the chart manually
        st.subheader("Chart Controls")
        reset_button = st.button("Reset Chart")

        # -- Logic to reset chart based on user actions --

        # 1. Manual reset button
        if reset_button:
            st.session_state["curves"] = {}

        # 2. Changing the "Number of years"
        if (st.session_state["prev_years"] is not None) and (years != st.session_state["prev_years"]):
            st.session_state["curves"] = {}

        # 3. Changing Calculation Type (FV <-> PV)
        if (st.session_state["prev_calc_type"] is not None) and (calculation_type != st.session_state["prev_calc_type"]):
            st.session_state["curves"] = {}

        # Update stored 'previous' parameters
        st.session_state["prev_years"] = years
        st.session_state["prev_calc_type"] = calculation_type

        # -- Compute the current curve --
        year_range = np.arange(0, years + 1)
        if calculation_type == "Future Value":
            # FV = 100 * (1 + r)^n
            values = 100 * (1 + interest_rate)**year_range
        else:
            # PV = 100 / (1 + r)^n
            values = 100 / ((1 + interest_rate)**year_range)

        curve_series = pd.Series(data=values.round(2), index=year_range)

        # Label that shows the meaning of each curve in the legend
        calc_label = "Future Value" if calculation_type == "Future Value" else "Present Value"
        curve_label = f"{calc_label} at {interest_rate_percent}% for {years}y"

        # -- AUTO-ADD the new curve to session_state so we keep all prior curves --
        # We'll use a short UUID as the dict key so multiple lines of the same label won't overwrite each other.
        curve_key = f"{uuid.uuid4().hex[:5]}"  
        st.session_state["curves"][curve_key] = (curve_label, curve_series)

        # -- Show the current curve results in a small table --
        df_current = pd.DataFrame({"Year": year_range, "Value": curve_series.values})
        st.subheader(f"Current {calc_label} @ {interest_rate_percent}% for {years} year(s)")
        st.dataframe(df_current.style.format({"Value": "{:.2f}"}))

    # -- Right Column: Comparison Chart --
    with col2:
        st.subheader("Comparison Chart")

        # Build a DataFrame combining all stored curves
        df_plot = pd.DataFrame()
        for _, (label, series) in st.session_state["curves"].items():
            df_plot[label] = series

        # Plot them all
        st.line_chart(df_plot)

        # Optional: Show a combined table for all lines
        # st.write("All Curves (for debugging):")
        # st.dataframe(df_plot.round(2))

if __name__ == "__main__":
    main()
