import streamlit as st
from PA28Performance import PA28Plot  # if PA28Plot is in another file

st.title("PA-28 Performance Calculator")

Weight = st.number_input("Weight (lb)", min_value=1000, max_value=3000, value=2325)
OAT_C = st.number_input("Outside Air Temperature (°C)", value=15.0)
Elevation = st.number_input("Elevation (ft)", value=1000)
Altimeter = st.number_input("Altimeter Setting (in Hg)", value=29.92)

if st.button("Calculate"):
    fig = PA28Plot(Weight, OAT_C, Elevation, Altimeter)
    st.plotly_chart(fig)
