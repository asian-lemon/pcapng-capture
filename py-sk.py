import pyshark
import pandas as pd

# Load the pcapng file
file_path = 'capture.pcapng'  # Replace with your file's path

# Open the capture file
capture = pyshark.FileCapture(file_path, display_filter="ip")

# Dictionary to store connection summaries
connections = {}

print("Analyzing packets...")

# Analyze each packet
for packet in capture:
    try:
        src_ip = packet.ip.src
        dst_ip = packet.ip.dst
        protocol = packet.highest_layer

        # Port information (if available)
        src_port = packet[packet.transport_layer].srcport if hasattr(packet, 'transport_layer') else None
        dst_port = packet[packet.transport_layer].dstport if hasattr(packet, 'transport_layer') else None

        # Create a unique connection identifier
        connection_id = (src_ip, dst_ip, protocol, src_port, dst_port)

        # Update connection data
        if connection_id not in connections:
            connections[connection_id] = {"Count": 0, "Protocols": set()}
        connections[connection_id]["Count"] += 1
        connections[connection_id]["Protocols"].add(protocol)
    except AttributeError:
        # Skip packets without required fields
        continue

# Convert the connection summary to a DataFrame
connection_summary = [
    {
        "Source IP": conn[0],
        "Destination IP": conn[1],
        "Protocol": conn[2],
        "Source Port": conn[3],
        "Destination Port": conn[4],
        "Packet Count": data["Count"],
        "Protocols": list(data["Protocols"]),
    }
    for conn, data in connections.items()
]

df = pd.DataFrame(connection_summary)

# Save the summary as a CSV for further analysis
output_file = "capture_analysis_summary.csv"
df.to_csv(output_file, index=False)

print(f"Analysis complete. Summary saved as {output_file}.")
