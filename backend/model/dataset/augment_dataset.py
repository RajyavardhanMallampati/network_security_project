import pandas as pd
import random

# Load your existing synthetic dataset
df = pd.read_csv("synthetic_network_traffic.csv")

# Ensure we have a 'label' column
if 'label' not in df.columns:
    df['label'] = 'Normal'

# Inject Anomalies
num_anomalies = 10
anomaly_indices = random.sample(range(len(df)), num_anomalies)
df.loc[anomaly_indices, 'label'] = 'Anomaly'

# Inject Malware
num_malware = 10
malware_indices = random.sample([i for i in range(len(df)) if i not in anomaly_indices], num_malware)
df.loc[malware_indices, 'label'] = 'Malware'

# Save to new CSV
df.to_csv("synthetic_network_traffic_augmented.csv", index=False)

print("✅ Augmented dataset saved as 'synthetic_network_traffic_augmented.csv'")
print("📌 Injected:")
print(f"   - Anomaly: {num_anomalies} rows")
print(f"   - Malware: {num_malware} rows")
