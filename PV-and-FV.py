import streamlit as st
import numpy as np
import pandas as pd
import uuid
import matplotlib.pyplot as plt

# Set the page configuration to wide so that the chart has more room
st.set_page_config(layout="wide")

# Increase Matplotlib's default font sizes for better readability
plt.rcParams.update({
    "font.size": 14,        # Base font size for text
    "axes.titlesize": 18,   # Font size for axes titles
    "axes.labelsize": 16,   # Font size for x and y labels
    "legend.fontsize": 14,  # Font size for legend text
    "xtick.labelsize": 14,  # Font size for x tick labels
    "ytick.labelsize": 14   # Font size for y tick labels
})

def main():
    st.title("Future Value / Present Value Visualizer (Comparison Mode)")

    # -- Initialize session state values --
    if "curves" not in st.session_state:
        st.session_state["curves"] = {}  # Dictionary to store curves (key: unique, value: (label, series))
    if "prev_years" not in st.session_state:
        st.session_state["prev_years"] = None  # To detect if the number of years changed
    if "prev_calc_type" not in st.session_state:
        st.session_state["prev_calc_type"] = None  # To detect if FV vs. PV changed

    # Use two columns with custom width ratios (left: controls; right: larger chart)
    col1, col2 = st.columns([1, 3])

    with col1:
        # Future Value vs Present Value radio button
        calculation_type = st.radio(
            "Select Calculation Type:",
            ("Future Value", "Present Value")
        )

        # Slider for the number of years (investment horizon)
        years = st.slider("Number of years", min_value=0, max_value=50, value=10)

        # Slider for interest/discount rate in percentage
        interest_rate_percent = st.slider("Interest/Discount rate (%)", 0, 20, 5)
        interest_rate = interest_rate_percent / 100.0

        st.subheader("Chart Controls")
        reset_button = st.button("Reset Chart")

        # Reset the stored curves if the reset button is clicked
        if reset_button:
            st.session_state["curves"] = {}

        # If the number of years changed from the previous value, clear stored curves
        if st.session_state["prev_years"] is not None and years != st.session_state["prev_years"]:
            st.session_state["curves"] = {}

        # If the calculation type (FV vs. PV) changed from previous value, clear stored curves
        if st.session_state["prev_calc_type"] is not None and calculation_type != st.session_state["prev_calc_type"]:
            st.session_state["curves"] = {}

        # Update the stored previous parameters
        st.session_state["prev_years"] = years
        st.session_state["prev_calc_type"] = calculation_type

        # Calculate the curve for the current parameters
        year_range = np.arange(0, years + 1)
        if calculation_type == "Future Value":
            # Future Value: FV = PV * (1 + r)^n with PV = €100
            values = 100 * (1 + interest_rate) ** year_range
            calc_label = "Future Value"
        else:
            # Present Value: PV = FV / (1 + r)^n with FV = €100
            values = 100 / ((1 + interest_rate) ** year_range)
            calc_label = "Present Value"

        # Convert to a Pandas Series for easy plotting and rounding
        curve_series = pd.Series(data=values.round(2), index=year_range)

        # Create a label that describes this curve
        curve_label = f"{calc_label} at {interest_rate_percent}% for {years}y"

        # Automatically add the new curve to the session state using a unique key
        curve_key = f"{uuid.uuid4().hex[:5]}"
        st.session_state["curves"][curve_key] = (curve_label, curve_series)

        # Display the current curve's data in a table
        df_current = pd.DataFrame({"Year": year_range, "Value": curve_series.values})
        st.subheader(f"Current {calc_label} @ {interest_rate_percent}% for {years} year(s)")
        st.dataframe(df_current.style.format({"Value": "{:.2f}"}))

    with col2:
        st.subheader("Comparison Chart")

        # Combine all stored curves into a DataFrame
        df_plot = pd.DataFrame()
        for _, (label, series) in st.session_state["curves"].items():
            df_plot[label] = series

        # Create a Matplotlib figure with a larger size
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Plot each curve from the DataFrame
        for col in df_plot.columns:
            ax.plot(df_plot.index, df_plot[col], marker='o', label=col)
        
        # Set chart title and axis labels
        ax.set_title("Comparison Chart", fontsize=18)
        ax.set_xlabel("Year", fontsize=16)
        ax.set_ylabel("Value (€)", fontsize=16)
        ax.legend(loc='best', fontsize=14)

        # Ensure a tight layout so labels are not cut off
        fig.tight_layout()
        
        # Render the Matplotlib chart in Streamlit
        st.pyplot(fig)

if __name__ == "__main__":
    main()
