import streamlit as st
import numpy as np
import pandas as pd
import uuid

def main():
    st.title("Future Value / Present Value Visualizer (Comparison Mode)")

    # -- Initialize session state for storing curves and old parameters --
    if "curves" not in st.session_state:
        st.session_state["curves"] = {}
    if "prev_years" not in st.session_state:
        st.session_state["prev_years"] = None
    if "prev_interest_rate_percent" not in st.session_state:
        st.session_state["prev_interest_rate_percent"] = None
    if "prev_calc_type" not in st.session_state:
        st.session_state["prev_calc_type"] = None

    # -- Two-column layout --
    col1, col2 = st.columns(2)

    with col1:
        # Radio: FV or PV
        calculation_type = st.radio(
            "Select Calculation Type:",
            ("Future Value", "Present Value")
        )

        # Slider: Number of years
        years = st.slider("Number of years", min_value=0, max_value=50, value=10)

        # Slider: interest/discount rate in percentage
        interest_rate_percent = st.slider(
            "Interest/Discount rate (%)",
            min_value=0,
            max_value=20,
            value=5
        )
        interest_rate = interest_rate_percent / 100.0

        # Reset button
        st.subheader("Chart Controls")
        reset_button = st.button("Reset Chart")

        # If user clicks "Reset Chart", clear stored curves
        if reset_button:
            st.session_state["curves"] = {}

        # If user changes the years from its last known value, clear curves
        if st.session_state["prev_years"] is not None and years != st.session_state["prev_years"]:
            st.session_state["curves"] = {}

        # Compute the new curve for the current parameters
        year_range = np.arange(0, years + 1)
        if calculation_type == "Future Value":
            # FV = 100 * (1 + r)^n
            values = 100 * (1 + interest_rate) ** year_range
        else:
            # PV = 100 / (1 + r)^n
            values = 100 / ((1 + interest_rate) ** year_range)

        # Round values to 2 decimals
        curve_series = pd.Series(data=values.round(2), index=year_range)

        # Check if either the interest rate or the calc type changed
        # (but years did not, because that already triggers a reset)
        if (
            (st.session_state["prev_interest_rate_percent"] is not None 
             and interest_rate_percent != st.session_state["prev_interest_rate_percent"])
            or
            (st.session_state["prev_calc_type"] is not None
             and calculation_type != st.session_state["prev_calc_type"])
        ):
            # Generate a label for storing the curve
            label = f"{'FV' if calculation_type=='Future Value' else 'PV'} {interest_rate_percent}% {years}y"
            # Use a UUID to ensure uniqueness if the user slides quickly through multiple rates
            unique_key = f"{label}-{uuid.uuid4().hex[:4]}"
            st.session_state["curves"][unique_key] = (label, curve_series)

        # Update stored 'previous' parameters
        st.session_state["prev_years"] = years
        st.session_state["prev_interest_rate_percent"] = interest_rate_percent
        st.session_state["prev_calc_type"] = calculation_type

        # ------------------------
        # Display the *current* results in a small table (optional)
        df_current = pd.DataFrame({"Year": year_range, "Value": curve_series.values})
        st.subheader(f"Current {calculation_type} @ {interest_rate_percent}% for {years} year(s)")
        st.dataframe(df_current.style.format({"Value": "{:.2f}"}))

    with col2:
        st.subheader("Comparison Chart")

        # Build a DataFrame with all stored curves
        # plus the current unsaved curve if we want to see it.
        if len(st.session_state["curves"]) == 0:
            # If no stored curves, just display the current one
            df_plot = pd.DataFrame({"Current": curve_series})
        else:
            # Combine all saved curves
            df_plot = pd.DataFrame()
            for (key, (label, series)) in st.session_state["curves"].items():
                df_plot[label] = series

            # Optionally also show the current curve, if not already added
            # This ensures the chart updates in real time as we move the slider
            # But does not store it unless there's a real parameter change.
            label_current = f"Current ({'FV' if calculation_type=='Future Value' else 'PV'} {interest_rate_percent}% {years}y)"
            df_plot[label_current] = curve_series

        # Plot them all. 
        st.line_chart(df_plot)

        # Optional debug: see the entire DF
        # st.dataframe(df_plot)

if __name__ == "__main__":
    main()
