import streamlit as st
import pandas as pd
import joblib
import time
import matplotlib.pyplot as plt
import numpy as np
import io

# Load model and scaler
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# Sidebar upload
st.sidebar.title("📁 Upload Packet CSV")
uploaded_file = st.sidebar.file_uploader("Choose a packet CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ File uploaded successfully.")
else:
    df = pd.read_csv("data/DDos.csv")
    st.sidebar.info("Using default DDos.csv")

df.columns = df.columns.str.strip()
df = df.dropna()
if 'Label' not in df.columns:
    st.error("❌ 'Label' column missing in CSV.")
    st.stop()

# Shuffle the data for randomness
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

X = df.drop(['Label'], axis=1)
y = df['Label']
X_scaled = scaler.transform(X)

# Simulate Hosts: Just generate fake IP addresses for source and destination
def generate_ip():
    return ".".join(str(np.random.randint(1, 255)) for _ in range(4))

# UI Title and description
st.title("🛡️ Real-time DDoS Packet Simulation with Hosts")
st.markdown("""
Simulates incoming packets from Hosts to a server, classifies packets live, shows dynamic stats with bar charts,
and allows exporting the simulation log.
""")

num_packets = st.slider("Number of packets to simulate", 10, min(200, len(df)), 50)
start = st.button("🚦 Start Simulation")

# Placeholders for live UI update
packet_info = st.empty()
packet_table = st.empty()
progress_bar = st.progress(0)
bar_chart_placeholder = st.empty()
download_button_placeholder = st.empty()

attack_count = 0
normal_count = 0
results = []

if start:
    st.info("Simulation started! Please wait...")
    for i in range(num_packets):
        # Prepare packet data
        packet_features = X_scaled[i].reshape(1, -1)
        prediction = model.predict(packet_features)[0]
        true_label = y.iloc[i]

        # ✅ Correct interpretation
        if prediction.upper() == "BENIGN":
            status_text = "✅ Normal"
            normal_count += 1
        else:
            status_text = "🚨 Attack"
            attack_count += 1

        # Simulate host IPs
        src_ip = generate_ip()
        dest_ip = "192.168.1.1"  # Assume all go to one server IP

        results.append({
            "Packet #": i + 1,
            "Source IP": src_ip,
            "Destination IP": dest_ip,
            "Prediction": prediction,
            "True Label": true_label,
            "Status": status_text
        })

        # Update live packet info with “traveling” text
        packet_info.markdown(
            f"**Packet #{i+1} traveling from `{src_ip}` to `{dest_ip}`**\n\n"
            f"**Prediction:** {status_text}"
        )

        # Show last 5 packets in a table
        packet_table.dataframe(pd.DataFrame(results).tail(5), use_container_width=True)

        # Update progress bar
        progress_bar.progress((i + 1) / num_packets)

        # Update live bar chart
        data_for_chart = pd.DataFrame({
            'Type': ['Normal', 'Attack'],
            'Count': [normal_count, attack_count]
        })
        fig, ax = plt.subplots()
        ax.bar(data_for_chart['Type'], data_for_chart['Count'], color=['green', 'red'])
        ax.set_ylabel("Number of Packets")
        ax.set_title("Packet Classification Counts")
        bar_chart_placeholder.pyplot(fig)

        time.sleep(0.3)

    st.success(f"✅ Simulation complete! ✅ Normal: {normal_count} | 🚨 Attacks: {attack_count}")

    # Prepare CSV download
    df_results = pd.DataFrame(results)
    csv_buffer = io.StringIO()
    df_results.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode()

    download_button_placeholder.download_button(
        label="📥 Download Simulation Log as CSV",
        data=csv_bytes,
        file_name="simulation_log.csv",
        mime="text/csv"
    )
else:
    st.info("Press the button above to start the real-time packet simulation.")
