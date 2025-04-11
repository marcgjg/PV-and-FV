import streamlit as st
import numpy as np
import pandas as pd
import uuid
import matplotlib.pyplot as plt

def main():
    st.title("Future Value / Present Value Visualizer")

    # -- Session State Setup --
    if "curves" not in st.session_state:
        st.session_state["curves"] = {}
    if "prev_years" not in st.session_state:
        st.session_state["prev_years"] = None
    if "prev_calc_type" not in st.session_state:
        st.session_state["prev_calc_type"] = None

    col1, col2 = st.columns(2)

    with col1:
        calculation_type = st.radio(
            "Select Calculation Type:",
            ("Future Value", "Present Value")
        )

        years = st.slider("Number of years", min_value=0, max_value=50, value=10)

        interest_rate_percent = st.slider(
            "Interest/Discount rate (%)",
            min_value=0,
            max_value=20,
            value=5
        )
        interest_rate = interest_rate_percent / 100.0

        st.subheader("Chart Controls")
        reset_button = st.button("Reset Chart")

        # Manual reset
        if reset_button:
            st.session_state["curves"] = {}

        # Auto-reset on "years" change
        if (st.session_state["prev_years"] is not None) and (years != st.session_state["prev_years"]):
            st.session_state["curves"] = {}

        # Auto-reset on "calculation_type" change
        if (st.session_state["prev_calc_type"] is not None) and (calculation_type != st.session_state["prev_calc_type"]):
            st.session_state["curves"] = {}

        # Update stored parameters
        st.session_state["prev_years"] = years
        st.session_state["prev_calc_type"] = calculation_type

        # Compute the current curve
        year_range = np.arange(0, years + 1)
        if calculation_type == "Future Value":
            values = 100 * (1 + interest_rate)**year_range
            calc_label = "Future Value"
        else:
            values = 100 / ((1 + interest_rate)**year_range)
            calc_label = "Present Value"

        curve_series = pd.Series(data=values.round(2), index=year_range)

        # Label that appears in the legend
        curve_label = f"{calc_label} at {interest_rate_percent}% for {years}y"

        # AUTO-ADD the new curve to session_state
        curve_key = f"{uuid.uuid4().hex[:5]}"  # short random suffix
        st.session_state["curves"][curve_key] = (curve_label, curve_series)

        # Display the current curve in a table
        df_current = pd.DataFrame({"Year": year_range, "Value": curve_series.values})
        st.subheader(f"Current {calc_label} @ {interest_rate_percent}% for {years} year(s)")
        st.dataframe(df_current.style.format({"Value": "{:.2f}"}))

    with col2:
        st.subheader("Comparison Chart")

        # Build a DataFrame for all stored curves
        df_plot = pd.DataFrame()
        for _, (label, series) in st.session_state["curves"].items():
            df_plot[label] = series

        # --- Matplotlib Plot ---
        # Create a larger figure: width=10 inches, height=6 inches (for example)
        fig, ax = plt.subplots(figsize=(20, 12))
       
        
        for label in df_plot.columns:
            ax.plot(df_plot.index, df_plot[label], label=label)

        ax.set_title("Comparison Chart")
        ax.set_xlabel("Year")
        ax.set_ylabel("Value")
        ax.legend()

        # Display the Matplotlib figure in Streamlit
        st.pyplot(fig)

if __name__ == "__main__":
    main()
