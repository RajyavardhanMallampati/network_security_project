import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib
import os

# Load dataset
df = pd.read_csv("synthetic_network_traffic_augmented.csv")

# Debug: Check how many parts each label splits into
split_counts = df['label'].apply(lambda x: len(str(x).split('_')))
print("Label split counts:\n", split_counts.value_counts())

# Filter rows where label splits into exactly 2 parts and reset index
df = df[df['label'].apply(lambda x: len(str(x).split('_')) == 2)].reset_index(drop=True)

# Now split safely into two columns
df[['traffic_category', 'threat_level']] = df['label'].str.split('_', expand=True)

# Encode categorical features
feature_encoders = {}
for col in ['traffic_type', 'protocol', 'flag']:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    feature_encoders[col] = le

# Encode target labels
traffic_encoder = LabelEncoder()
df['traffic_category'] = traffic_encoder.fit_transform(df['traffic_category'])

threat_encoder = LabelEncoder()
df['threat_level'] = threat_encoder.fit_transform(df['threat_level'])

# Prepare features and targets
X = df.drop(['label', 'traffic_category', 'threat_level'], axis=1)

# ===== Model 1: Predict Traffic Category =====
y1 = df['traffic_category']
X_train1, X_test1, y_train1, y_test1 = train_test_split(X, y1, test_size=0.2, random_state=42)
clf_traffic = RandomForestClassifier(n_estimators=100, random_state=42)
clf_traffic.fit(X_train1, y_train1)
print("✅ Traffic Classification Report:")
print(classification_report(y_test1, clf_traffic.predict(X_test1)))

# ===== Model 2: Predict Threat Level =====
y2 = df['threat_level']
X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y2, test_size=0.2, random_state=42)
clf_threat = RandomForestClassifier(n_estimators=100, random_state=42)
clf_threat.fit(X_train2, y_train2)
print("✅ Threat Detection Report:")
print(classification_report(y_test2, clf_threat.predict(X_test2)))

# Save models and encoders
os.makedirs("../model", exist_ok=True)
joblib.dump(clf_traffic, "../model/traffic_model.joblib")
joblib.dump(clf_threat, "../model/threat_model.joblib")
joblib.dump(traffic_encoder, "../model/traffic_encoder.joblib")
joblib.dump(threat_encoder, "../model/threat_encoder.joblib")

# Save feature encoders
for col, le in feature_encoders.items():
    joblib.dump(le, f"../model/{col}_encoder.joblib")

print("✅ Models & encoders saved successfully.")
