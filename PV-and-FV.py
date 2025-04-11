import streamlit as st
import numpy as np
import pandas as pd

def main():
    st.title("Future Value / Present Value Visualizer")

    # Create two columns
    col1, col2 = st.columns(2)

    # --- Column 1: Inputs and Table ---
    with col1:
        calculation_type = st.radio(
            "Select Calculation Type:",
            ("Future Value", "Present Value")
        )

        years = st.slider("Number of years", min_value=0, max_value=50, value=10)

        # Using an integer slider for the interest/discount rate in percentages
        interest_rate_percent = st.slider(
            "Interest/Discount rate (%)",
            min_value=0,
            max_value=20,
            value=5
        )
        interest_rate = interest_rate_percent / 100.0

        # Create a range of years from 0 up to the chosen value
        year_range = np.arange(0, years + 1)

        # Calculate the corresponding amount for each year
        if calculation_type == "Future Value":
            # FV = 100 * (1 + r)^n
            values = 100 * (1 + interest_rate) ** year_range
            st.subheader(f"Future Value of €100 at {interest_rate_percent}% for up to {years} year(s)")
        else:
            # PV = 100 / (1 + r)^n
            values = 100 / ((1 + interest_rate) ** year_range)
            st.subheader(f"Present Value of €100 at {interest_rate_percent}% for up to {years} year(s)")

        # Prepare data for display and formatting
        df = pd.DataFrame({
            "Year": year_range,
            "Value": values.round(2)
        })

        # Show the numeric results in a table with 2 decimal places
        st.dataframe(df.style.format({"Value": "{:.2f}"}))

    # --- Column 2: Chart ---
    with col2:
        st.line_chart(df, x="Year", y="Value")

if __name__ == "__main__":
    main()
