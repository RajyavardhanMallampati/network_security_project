import pandas as pd
import numpy as np

np.random.seed(42)

# Define possible categories and threat levels
traffic_types = ['Web', 'Video', 'Messaging', 'FileTransfer']
threat_levels = ['Normal', 'Anomaly', 'Threat']

protocols = ['TCP', 'UDP', 'ICMP']
flags = ['SYN', 'ACK', 'FIN', 'RST']

# Number of samples
n_samples = 500

# Generate random features
data = {
    'traffic_type': np.random.choice(traffic_types, n_samples),
    'protocol': np.random.choice(protocols, n_samples),
    'flag': np.random.choice(flags, n_samples),
    'packet_length': np.random.randint(20, 1500, n_samples),
    'duration': np.random.uniform(0.01, 10.0, n_samples),
    'flow_bytes': np.random.randint(100, 100000, n_samples)
}

df = pd.DataFrame(data)

# Create composite label as traffic_threat
df['label'] = df['traffic_type'] + '_' + np.random.choice(threat_levels, n_samples)

# Save to CSV
df.to_csv('synthetic_network_traffic_augmented.csv', index=False)

print("Synthetic dataset with composite labels generated and saved.")
print(df.head())
