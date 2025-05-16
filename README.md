# DDoS Attack Detection and Simulation using Machine Learning

This project demonstrates real-time DDoS attack detection using a machine learning model with an interactive Streamlit dashboard. The simulation classifies incoming network packets as **Normal** or **Attack** and visualizes the live results with host-IP simulation, bar charts, and downloadable logs.

---

## 🔧 Project Structure

DDoS_Detection_App/
├── app.py # Main Streamlit simulation app
├── model.pkl # Trained ML classification model
├── scaler.pkl # Fitted scaler for input features
├── data/
│ └── DDos.csv # Default dataset for simulation
└── README.md # Project documentation


---

## ⚙️ Features

- **Real-time packet simulation** with host-to-server IP generation
- **Live classification** using a pre-trained ML model
- **Dynamic bar chart** showing normal vs. attack packet counts
- **Live packet feed** with details for each simulated packet
- **Downloadable CSV logs** of simulation results
- **Manual CSV upload support for testing custom data**

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/DDoS_Detection_App.git
cd DDoS_Detection_App
