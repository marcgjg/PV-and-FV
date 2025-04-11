import streamlit as st
import numpy as np
import pandas as pd

def main():
    st.title("Future Value / Present Value Visualizer (Comparison Mode)")

    # Session state to hold all the curves the user adds
    # and to track the previously selected number of years
    if "curves" not in st.session_state:
        st.session_state["curves"] = {}
    if "prev_years" not in st.session_state:
        # We initialize this once; it will be updated whenever the slider is moved
        st.session_state["prev_years"] = None

    # ------------------------
    # Layout: Two Columns
    # ------------------------
    col1, col2 = st.columns(2)

    with col1:
        # Radio button: FV vs PV
        calculation_type = st.radio(
            "Select Calculation Type:",
            ("Future Value", "Present Value")
        )

        # Slider: Number of years
        years = st.slider("Number of years", min_value=0, max_value=50, value=10)

        # If the user changes the years from its last known value, clear curves
        if st.session_state["prev_years"] is not None and years != st.session_state["prev_years"]:
            st.session_state["curves"] = {}

        # Update stored 'prev_years' to the new value
        st.session_state["prev_years"] = years

        # Slider: interest/discount rate in percentage
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

        # Create a range of years from 0 up to the chosen value
        year_range = np.arange(0, years + 1)

        # Calculate the corresponding values
        if calculation_type == "Future Value":
            values = 100 * (1 + interest_rate) ** year_range
        else:
            values = 100 / ((1 + interest_rate) ** year_range)

        # Turn into a Pandas Series (indexed by year), rounded to two decimals
        curve_series = pd.Series(data=values.round(2), index=year_range)

        # ------------------------
        # Buttons to Add or Reset
        # ------------------------
        st.subheader("Comparison Controls")
        add_button = st.button("Add to Chart")
        reset_button = st.button("Reset Chart")

        if add_button:
            # Add this new curve to the session
            st.session_state["curves"][curve_label] = curve_series

        if reset_button:
            # Clear out any saved curves
            st.session_state["curves"] = {}

        # ------------------------
        # Show table of current parameters
        # ------------------------
        df_current = pd.DataFrame({
            "Year": year_range,
            "Value": values.round(2)
        })
        st.subheader(f"Current {calc_label} at {interest_rate_percent}% for {years} year(s)")
        st.dataframe(df_current.style.format({"Value": "{:.2f}"}))

    # ------------------------
    # Right Column: Chart
    # ------------------------
    with col2:
        st.subheader("Comparison Chart")

        if len(st.session_state["curves"]) == 0:
            # No curves saved, just show the current one
            df_plot = df_current.copy()
            df_plot.set_index("Year", inplace=True)
            df_plot.rename(columns={"Value": curve_label}, inplace=True)
        else:
            # Combine all saved curves into a single DataFrame
            all_curves_df = pd.DataFrame()
            for label, series in st.session_state["curves"].items():
                all_curves_df[label] = series

            # Also include the current (unsaved) curve for real-time preview
            all_curves_df[curve_label + " (unsaved)"] = curve_series
            df_plot = all_curves_df

        st.line_chart(df_plot)

if __name__ == "__main__":
    main()
