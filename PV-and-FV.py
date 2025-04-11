import streamlit as st
import numpy as np
import pandas as pd

def main():
    st.title("Future Value / Present Value Visualizer")

    # --- Radio button to select Future Value vs Present Value ---
    calculation_type = st.radio(
        "Select Calculation Type:",
        ("Future Value", "Present Value")
    )

    # --- Sliders to choose the number of years and the interest/discount rate ---
    years = st.slider("Number of years", min_value=0, max_value=50, value=10)
    interest_rate = st.slider("Interest/Discount rate (as a decimal)", 
                              min_value=0.00, max_value=0.20, step=0.01, value=0.05)
    
    # --- Create a range of years from 0 up to the chosen value ---
    year_range = np.arange(0, years + 1)

    # --- Calculate the corresponding amount for each year ---
    if calculation_type == "Future Value":
        # FV = PV * (1 + r)^n
        values = 100 * (1 + interest_rate) ** year_range
        st.subheader(f"Future Value of €100 at {interest_rate*100:.2f}% for up to {years} years")
    else:
        # PV = FV / (1 + r)^n
        values = 100 / ((1 + interest_rate) ** year_range)
        st.subheader(f"Present Value of €100 at {interest_rate*100:.2f}% for up to {years} years")

    # --- Prepare data for chart ---
    df = pd.DataFrame({
        "Year": year_range,
        "Value": values
    })

    # --- Show the numeric results in a table ---
    st.dataframe(df)

    # --- Plot the results ---
    st.line_chart(df, x="Year", y="Value")

if __name__ == "__main__":
    main()
