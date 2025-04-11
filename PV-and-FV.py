import streamlit as st
import numpy as np
import pandas as pd
import uuid
import altair as alt

def main():
    st.title("Future Value / Present Value Visualizer (Comparison Mode)")

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
        interest_rate_percent = st.slider("Interest/Discount rate (%)", 0, 20, 5)
        interest_rate = interest_rate_percent / 100.0

        st.subheader("Chart Controls")
        reset_button = st.button("Reset Chart")

        # Reset logic
        if reset_button:
            st.session_state["curves"] = {}
        if st.session_state["prev_years"] is not None and years != st.session_state["prev_years"]:
            st.session_state["curves"] = {}
        if st.session_state["prev_calc_type"] is not None and calculation_type != st.session_state["prev_calc_type"]:
            st.session_state["curves"] = {}

        # Update stored params
        st.session_state["prev_years"] = years
        st.session_state["prev_calc_type"] = calculation_type

        # Compute current curve
        year_range = np.arange(0, years + 1)
        if calculation_type == "Future Value":
            values = 100 * (1 + interest_rate)**year_range
            calc_label = "Future Value"
        else:
            values = 100 / ((1 + interest_rate)**year_range)
            calc_label = "Present Value"

        curve_series = pd.Series(data=values.round(2), index=year_range)
        curve_label = f"{calc_label} @ {interest_rate_percent}% for {years}y"

        # Auto-add the new curve
        key = f"{uuid.uuid4().hex[:5]}"
        st.session_state["curves"][key] = (curve_label, curve_series)

        # Show table for current curve
        df_current = pd.DataFrame({"Year": year_range, "Value": curve_series.values})
        st.subheader(f"Current {calc_label} @ {interest_rate_percent}% for {years} year(s)")
        st.dataframe(df_current.style.format({"Value": "{:.2f}"}))

    with col2:
        st.subheader("Comparison Chart")

        # Combine all stored curves
        df_plot = pd.DataFrame()
        for _, (label, series) in st.session_state["curves"].items():
            df_plot[label] = series

        # Move from wide to long format for Altair
        df_long = df_plot.reset_index().melt(
            id_vars="index", 
            var_name="Curve", 
            value_name="Value"
        )
        df_long.rename(columns={"index": "Year"}, inplace=True)

        # Build Altair chart
        chart = (
            alt.Chart(df_long)
            .mark_line(point=True)       # Show data points, optional
            .encode(
                x=alt.X("Year:Q", title="Year"),
                y=alt.Y("Value:Q", title="Value"),
                color="Curve:N",
                tooltip=["Year", "Value", "Curve"]
            )
            .interactive()  # Allows zoom/pan if desired
        )

        st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
    main()
