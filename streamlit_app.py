import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Balaton Surf Wind", layout="wide")

st.title("🌬️ Balaton Széljelentés - Siófok")

# Adatlekérés (ugyanaz az API, amit eddig használtunk)
LAT, LON = 46.91, 18.05
url = f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}&hourly=wind_speed_10m,wind_gusts_10m,wind_direction_10m&current=wind_speed_10m,wind_gusts_10m,wind_direction_10m&timezone=auto"

try:
    res = requests.get(url).json()
    curr = res['current']
    hist = res['hourly']

    # 1. Aktuális adatok (Kártyák)
    col1, col2, col3 = st.columns(3)
    col1.metric("Szélsebesség", f"{curr['wind_speed_10m']} km/h")
    col2.metric("Lökések", f"{curr['wind_gusts_10m']} km/h")
    col3.metric("Irány", f"{curr['wind_direction_10m']}°")

    # 2. Szélirány vizualizáció (Stílusos nyíl)
    st.write(f"### Szélirány: {curr['wind_direction_10m']}°")
    st.markdown(f'<div style="font-size:100px; transform: rotate({curr["wind_direction_10m"]}deg); text-align: center;">↑</div>', unsafe_allow_html=True)

    # 3. Grafikon (Idősoros)
    st.write("### Elmúlt 24 óra")
    df = pd.DataFrame({
        'Idő': [t.split("T")[1] for t in hist['time'][-24:]],
        'Sebesség': hist['wind_speed_10m'][-24:],
        'Lökések': hist['wind_gusts_10m'][-24:]
    })
    
    fig = px.line(df, x='Idő', y=['Sebesség', 'Lökések'], 
                  title="Szél alakulása (km/h)",
                  color_discrete_sequence=["#38bdf8", "#fbbf24"])
    st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.error(f"Hiba az adatok lekérésekor: {e}")
