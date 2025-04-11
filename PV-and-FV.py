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

        # Create a Series with index = year_range
        # Round the values to 2 decimals for clarity
        curve_series = pd.Series(data=values.round(2), index=year_range)

        # ------------------------
        # Buttons to Add/Reset Curves
        # ------------------------
        st.subheader("Comparison Controls")

        add_button = st.button("Add to Chart")
        reset_button = st.button("Reset Chart")

        if add_button:
            # Add this new curve to session_state
            st.session_state["curves"][curve_label] = curve_series

        if reset_button:
            # Clear out any saved curves
            st.session_state["curves"] = {}

        # ------------------------
        # Current (Latest) Results Table
        # ------------------------
        # Show the numeric results for the *current* parameters
        df_current = pd.DataFrame({
            "Year": year_range,
            "Value": values.round(2)
        })
        st.subheader(f"Current {calc_label} at {interest_rate_percent}% for {years} year(s)")
        st.dataframe(df_current.style.format({"Value": "{:.2f}"}))

    # ------------------------
    # Column 2: Chart
    # ------------------------
    with col2:
        st.subheader("Comparison Chart")

        # Build a DataFrame combining all the stored curves
        # If no curves are stored yet, we'll just show the current one
        if len(st.session_state["curves"]) == 0:
            # Plot only the current curve
            df_plot = df_current.copy()
            df_plot.set_index("Year", inplace=True)
            df_plot.rename(columns={"Value": curve_label}, inplace=True)

        else:
            # Combine all curves, aligning on the year index
            # We'll expand out to the max year range among all curves
            all_curves_df = pd.DataFrame()

            for label, series in st.session_state["curves"].items():
                all_curves_df[label] = series

            # Additionally, also include the *current* unsaved curve
            # so user can see the effect of changing sliders in real time
            all_curves_df[curve_label + " (unsaved)"] = curve_series

            df_plot = all_curves_df

        # Plot the combined DataFrame
        st.line_chart(df_plot)

        # Optionally show a table of all stored curves to help compare
        # (Comment out if you only want the chart)
        # st.write("All Saved Curves:")
        # st.dataframe(df_plot.style.format("{:.2f}"))

if __name__ == "__main__":
    main()
