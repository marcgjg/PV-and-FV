import streamlit as st
import numpy as np
import pandas as pd
import uuid
import matplotlib.pyplot as plt
import io

# Set the page layout to wide so there's more space
st.set_page_config(layout="wide")

# Increase Matplotlib's default font sizes for better readability.
plt.rcParams.update({
    "font.size": 14,        # Base text
    "axes.titlesize": 18,   # Title size
    "axes.labelsize": 16,   # Axis labels
    "legend.fontsize": 14,  # Legend text
    "xtick.labelsize": 14,  # X tick labels
    "ytick.labelsize": 14   # Y tick labels
})

def main():
    st.title("Future Value / Present Value Visualizer")

    # Initialize session state to store curves and previous parameters.
    if "curves" not in st.session_state:
        st.session_state["curves"] = {}  # To store curves (key: unique, value: (label, series))
    if "prev_years" not in st.session_state:
        st.session_state["prev_years"] = None
    if "prev_calc_type" not in st.session_state:
        st.session_state["prev_calc_type"] = None

    # Use two columns. Here, the right column gets more space.
    col1, col2 = st.columns([1, 3])

    with col1:
        # Control section for calculation options.
        calculation_type = st.radio(
            "Select Calculation Type:",
            ("Future Value", "Present Value")
        )

        years = st.slider("Number of years", min_value=0, max_value=50, value=10)
        interest_rate_percent = st.slider("Interest/Discount rate (%)", 0, 20, 5)
        interest_rate = interest_rate_percent / 100.0

        st.subheader("Chart Controls")
        reset_button = st.button("Reset Chart")

        # Reset curves on button click.
        if reset_button:
            st.session_state["curves"] = {}

        # Clear curves automatically when number of years changes.
        if st.session_state["prev_years"] is not None and years != st.session_state["prev_years"]:
            st.session_state["curves"] = {}

        # Clear curves automatically when switching FV/PV.
        if st.session_state["prev_calc_type"] is not None and calculation_type != st.session_state["prev_calc_type"]:
            st.session_state["curves"] = {}

        # Update the stored previous parameters.
        st.session_state["prev_years"] = years
        st.session_state["prev_calc_type"] = calculation_type

        # Calculate the current curve.
        year_range = np.arange(0, years + 1)
        if calculation_type == "Future Value":
            # FV = 100 * (1 + r)^n with a principal of €100.
            values = 100 * (1 + interest_rate)**year_range
            calc_label = "Future Value"
        else:
            # PV = 100 / (1 + r)^n with a future value of €100.
            values = 100 / ((1 + interest_rate)**year_range)
            calc_label = "Present Value"

        # Create a Pandas Series for easy plotting.
        curve_series = pd.Series(data=values.round(2), index=year_range)
        curve_label = f"{calc_label} at {interest_rate_percent}% for {years}y"
        # Use a unique key so similar curves don't overwrite each other.
        curve_key = f"{uuid.uuid4().hex[:5]}"
        st.session_state["curves"][curve_key] = (curve_label, curve_series)

        # Display the current calculation table.
        df_current = pd.DataFrame({"Year": year_range, "Value": curve_series.values})
        st.subheader(f"Current {calc_label} @ {interest_rate_percent}% for {years} year(s)")
        st.dataframe(df_current.style.format({"Value": "{:.2f}"}))

    with col2:
        # st.subheader("Comparison Chart")

        # Combine all stored curves into a single DataFrame.
        df_plot = pd.DataFrame()
        for _, (label, series) in st.session_state["curves"].items():
            df_plot[label] = series

        # Create a Matplotlib figure. The figsize here sets resolution and clarity.
        fig, ax = plt.subplots(figsize=(10, 6))
        for col in df_plot.columns:
            ax.plot(df_plot.index, df_plot[col], marker='o', label=col)

        # ax.set_title("Comparison Chart", fontsize=18)
        ax.set_xlabel("Year", fontsize=16)
        ax.set_ylabel("Value (€)", fontsize=16)
        ax.legend(loc='best', fontsize=14)
        fig.tight_layout()

        # Save the figure to a bytes buffer and then display with st.image.
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        st.image(buf, use_container_width=True)

if __name__ == "__main__":
    main()
