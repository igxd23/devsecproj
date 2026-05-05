import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go

st.set_page_config(layout="wide")

pipeline = joblib.load("vehicle_pipeline.pkl")

iso = pipeline["iso_model"]
rf = pipeline["rf_model"]
scaler = pipeline["scaler"]
feature_columns = pipeline["feature_columns"]
le = pipeline["label_encoder"]

df = pd.read_csv("engine_failure_dataset.csv")
df['Time_Stamp'] = pd.to_datetime(df['Time_Stamp'])

st.title("🚗 Real-Time Engine Monitoring Dashboard")

safe_ranges = {
    "RPM": (800, 3000),
    "Temperature (°C)": (30, 90),
    "Vibration": (0, 1.2)
}

st.markdown("### ⚙️ Engine Controls")

col1, col2, col3 = st.columns(3)

rpm = col1.slider(f"RPM (Safe: {safe_ranges['RPM'][0]} - {safe_ranges['RPM'][1]})", 500, 5000, 2000)
temp = col2.slider(f"Temperature °C (Safe: {safe_ranges['Temperature (°C)'][0]} - {safe_ranges['Temperature (°C)'][1]})", 20, 120, 60)
fuel = col3.slider("Fuel Efficiency", 5.0, 25.0, 15.0)

col4, col5, col6 = st.columns(3)

vib_x = col4.slider("Vibration X", 0.0, 5.0, 1.0)
vib_y = col5.slider("Vibration Y", 0.0, 5.0, 1.0)
vib_z = col6.slider("Vibration Z", 0.0, 5.0, 1.0)

col7, col8 = st.columns(2)

torque = col7.slider("Torque", 50.0, 500.0, 200.0)
power = col8.slider("Power Output", 10.0, 200.0, 80.0)

mode_options = df['Operational_Mode'].unique()
mode_selected = st.selectbox("Operational Mode", mode_options)

if isinstance(mode_selected, str):
    mode_encoded = le.transform([mode_selected])[0]
else:
    mode_encoded = mode_selected

colA, colB, colC = st.columns(3)
anomaly_box = colA.empty()
fault_box = colB.empty()
status_box = colC.empty()

chart_placeholder = st.empty()

if "plot_data" not in st.session_state:
    st.session_state.plot_data = pd.DataFrame(
        columns=["Time", "vibration", "anomaly", "fault"]
    )

if "last_input" not in st.session_state:
    st.session_state.last_input = None

row = {}

row['RPM'] = rpm
row['Temperature (°C)'] = temp
row['Fuel_Efficiency'] = fuel
row['Vibration_X'] = vib_x
row['Vibration_Y'] = vib_y
row['Vibration_Z'] = vib_z
row['Torque'] = torque
row['Power_Output (kW)'] = power
row['Operational_Mode'] = mode_encoded
row['Time_Stamp'] = pd.Timestamp.now()

vib_mag = np.sqrt(vib_x**2 + vib_y**2 + vib_z**2)
row['vibration_mag'] = vib_mag

current_input = (
    rpm, temp, fuel,
    vib_x, vib_y, vib_z,
    torque, power,
    mode_encoded
)

if current_input != st.session_state.last_input:

    st.session_state.last_input = current_input

    row['temp_ma'] = temp
    row['rpm_ma'] = rpm
    row['vib_ma'] = vib_mag
    row['hour'] = row['Time_Stamp'].hour

    X = pd.DataFrame([row])

    missing_cols = set(feature_columns) - set(X.columns)
    for col in missing_cols:
        X[col] = 0

    X = X[feature_columns]

    X_scaled = scaler.transform(X)

    anomaly = iso.predict(X_scaled)[0]
    fault = rf.predict(X)[0]

    anomaly_flag = 1 if anomaly == -1 else 0

    safe = (
        safe_ranges["RPM"][0] <= rpm <= safe_ranges["RPM"][1] and
        safe_ranges["Temperature (°C)"][0] <= temp <= safe_ranges["Temperature (°C)"][1] and
        vib_mag <= safe_ranges["Vibration"][1]
    )

    if safe:
        anomaly_flag = 0
        fault = 0

    anomaly_box.metric("Anomaly", anomaly_flag)
    fault_box.metric("Fault", int(fault))

    if safe:
        status_box.success("🟢 Safe Zone")
    elif anomaly_flag == 1:
        status_box.error("🔴 Anomaly Detected")
    elif fault == 1:
        status_box.warning("🟠 Fault Predicted")
    else:
        status_box.info("Normal")

    new_row = {
        "Time": row['Time_Stamp'],
        "vibration": vib_mag,
        "anomaly": anomaly_flag,
        "fault": fault
    }

    st.session_state.plot_data = pd.concat(
        [st.session_state.plot_data, pd.DataFrame([new_row])]
    )

plot_df = st.session_state.plot_data.tail(200)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=plot_df["Time"],
    y=plot_df["vibration"],
    mode='lines',
    name='Vibration'
))

fig.add_trace(go.Scatter(
    x=plot_df[plot_df["anomaly"] == 1]["Time"],
    y=plot_df[plot_df["anomaly"] == 1]["vibration"],
    mode='markers',
    marker=dict(size=8, color='red'),
    name='Anomaly'
))

fig.add_trace(go.Scatter(
    x=plot_df[plot_df["fault"] == 1]["Time"],
    y=plot_df[plot_df["fault"] == 1]["vibration"],
    mode='markers',
    marker=dict(size=8, color='orange'),
    name='Fault'
))

fig.update_layout(
    template="plotly_dark",
    margin=dict(l=20, r=20, t=30, b=20)
)

chart_placeholder.plotly_chart(fig, use_container_width=True)