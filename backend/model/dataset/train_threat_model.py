import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os

# Load dataset
df = pd.read_csv("synthetic_network_traffic_augmented.csv")

# Encode features
for col in ['traffic_type', 'protocol', 'flag']:
    df[col] = LabelEncoder().fit_transform(df[col])

# Derive threat level based on label
def get_threat_level(label):
    if label in ["Anomaly", "Malware"]:
        return label
    else:
        return "Normal"

df['threat'] = df['label'].apply(get_threat_level)

# Encode target
threat_encoder = LabelEncoder()
df['threat_encoded'] = threat_encoder.fit_transform(df['threat'])

# Split
X = df.drop(columns=['label', 'threat', 'threat_encoded'])
y = df['threat_encoded']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print("✅ Threat Classification Report:")
print(classification_report(y_test, y_pred, target_names=threat_encoder.classes_))

# Save model & encoder
os.makedirs("model", exist_ok=True)
joblib.dump(clf, "model/threat_model.joblib")
joblib.dump(threat_encoder, "model/threat_encoder.joblib")

print("✅ threat_model.joblib saved!")
print("✅ threat_encoder.joblib saved!")
