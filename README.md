# 🛡️ Network Security Project: AI-Based Traffic Classification & Threat Detection

This project leverages **Machine Learning (ML)** and **AI** to analyze and classify network traffic in real-time, detect anomalies, and identify potential threats. The system consists of a Python-based backend for ML inference and a JavaScript/HTML frontend dashboard for visualization.

## 🚀 Features

- 🎯 Real-time traffic classification (Web, Video, Messaging, File Transfer, Database)
- 🔐 Threat detection using trained ML models
- 📊 Frontend dashboard with charts & data table
- ⚡ FastAPI backend with pre-trained joblib models
- 📁 Synthetic and augmented dataset generators
- 📈 Custom traffic & threat encoders

## 🧠 ML Models Used

- **Random Forest Classifier** for traffic classification
- **Custom encoders** for protocol, traffic type, and flags
- Trained using synthetic datasets (`generate_dataset.py`, `augment_dataset.py`)

## 📂 Project Structure

├── backend/
│ ├── main.py # FastAPI backend server
│ ├── model/
│ │ ├── traffic_model.joblib
│ │ ├── threat_model.joblib
│ │ ├── *_encoder.joblib # Encoders for label, protocol, flag, etc.
│ │ └── dataset/
│ │ ├── generate_dataset.py
│ │ ├── augment_dataset.py
│ │ ├── synthetic_network_traffic.csv
│ │ └── train_model.py
├── frontend/
│ ├── index.html # Input form UI
│ ├── dashboard.html # Dashboard visualization
│ ├── live.html # Live traffic simulation
│ └── *.js # Supporting JS files

bash
Copy
Edit

## 🛠️ How to Run

### 1. Clone the repo

git clone https://github.com/RajyavardhanMallampati/network_security_project.git
cd network_security_project

2. Run Backend

cd backend
pip install -r requirements.txt
uvicorn main:app --reload

3. Open Frontend
Just open frontend/index.html or frontend/dashboard.html in your browser.

👥 Contributors
Rajyavardhan Mallampati – https://github.com/RajyavardhanMallampati

Yasam Durga Harika – https://github.com/DurgaHarika-Yasam

