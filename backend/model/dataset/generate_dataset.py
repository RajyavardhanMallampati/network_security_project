import pandas as pd
import numpy as np
import random

np.random.seed(42)

traffic_types = ['Web', 'Video', 'Messaging', 'File Transfer', 'Database']
protocols = ['TCP', 'UDP', 'ICMP']
labels = ['Normal', 'Anomaly', 'Malware', 'Encrypted']

def random_flag():
    return random.choice(['SYN', 'ACK', 'PSH', 'FIN', 'URG', 'RST'])

data = []

for _ in range(500):
    traffic_type = random.choice(traffic_types)
    protocol = random.choice(protocols)
    duration = round(np.random.exponential(scale=1.5), 2)
    packet_count = np.random.randint(5, 200)
    avg_packet_size = np.random.randint(40, 1500)
    total_bytes = packet_count * avg_packet_size
    bytes_per_sec = round(total_bytes / duration, 2) if duration > 0 else 0
    flag = random_flag()
    label = random.choices(labels, weights=[0.7, 0.15, 0.1, 0.05])[0]

    data.append([
        traffic_type, protocol, duration, packet_count,
        avg_packet_size, bytes_per_sec, flag, label
    ])

df = pd.DataFrame(data, columns=[
    'traffic_type', 'protocol', 'duration', 'packet_count',
    'avg_packet_size', 'bytes_per_sec', 'flag', 'label'
])

df.to_csv("synthetic_network_traffic.csv", index=False)
print("✅ Dataset saved as 'synthetic_network_traffic.csv'")
