from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import joblib

# Load models
traffic_model = joblib.load("model/traffic_model.joblib")
threat_model = joblib.load("model/threat_model.joblib")

# Load label encoders
traffic_encoder = joblib.load("model/traffic_encoder.joblib")
threat_encoder = joblib.load("model/threat_encoder.joblib")
protocol_encoder = joblib.load("model/protocol_encoder.joblib")
flag_encoder = joblib.load("model/flag_encoder.joblib")
traffic_type_encoder = joblib.load("model/traffic_type_encoder.joblib")

# FastAPI app
app = FastAPI()

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define expected input
class TrafficInput(BaseModel):
    traffic_type: str
    protocol: str
    duration: float
    packet_count: int
    avg_packet_size: int
    bytes_per_sec: float
    flag: str

@app.get("/")
def root():
    return {"message": "Network Traffic Classifier API is running ✅"}

@app.post("/predict")
def predict(input_data: TrafficInput):
    try:
        # Encode categorical string fields
        traffic_type = traffic_type_encoder.transform([input_data.traffic_type])[0]
        protocol = protocol_encoder.transform([input_data.protocol])[0]
        flag = flag_encoder.transform([input_data.flag])[0]
    except Exception as e:
        return {"error": f"Encoding error: {e}"}

    features = [[
        traffic_type,
        protocol,
        input_data.duration,
        input_data.packet_count,
        input_data.avg_packet_size,
        input_data.bytes_per_sec,
    
    ]]

    # Predict traffic category and threat level
    traffic_pred = traffic_model.predict(features)[0]
    threat_pred = threat_model.predict(features)[0]

    # Decode results
    traffic_class = traffic_encoder.inverse_transform([traffic_pred])[0]
    threat_level = threat_encoder.inverse_transform([threat_pred])[0]

    print("➡️ Features received:", features)
    print("🔵 Traffic Class ID:", traffic_pred, "->", traffic_class)
    print("🔴 Threat Level ID:", threat_pred, "->", threat_level)

    return {
        "traffic_class": traffic_class,
        "threat_level": threat_level
    }
