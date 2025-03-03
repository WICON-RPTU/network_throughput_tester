import socket
import time
import sys

# CLI Input Function
def get_user_input(prompt, default, min_val=None, max_val=None, dtype=str):
    while True:
        try:
            value = input(f"{prompt} (default {default}): ") or default
            value = dtype(value)
            if min_val is not None and max_val is not None and not (min_val <= value <= max_val):
                print(f"⚠️ Value must be between {min_val} and {max_val}. Try again.")
            else:
                return value
        except ValueError:
            print("⚠️ Invalid input. Please enter a valid value.")

# Get user-defined values
SERVER_IP = get_user_input("Enter server IP address", "192.168.1.100")
SERVER_PORT = 5005
NUM_PACKETS = int(get_user_input("Enter number of packets", 1000, 1, 100000, int))
PAYLOAD_SIZE = int(get_user_input("Enter packet size (bytes)", 128, 1, 1472, int))
PACKET_INTERVAL = get_user_input("Enter packet interval (seconds)", 0.005, 0.0001, 1.0, float)

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)  # 2 seconds timeout for responses

latencies = []
successful_packets = 0
lost_packets = 0
start_time = time.time()

print(f"\n🚀 Sending {NUM_PACKETS} packets to {SERVER_IP}:{SERVER_PORT} with {PAYLOAD_SIZE} bytes each, every {PACKET_INTERVAL:.4f} seconds...\n")

for i in range(NUM_PACKETS):
    send_time = time.time()
    payload = b"x" * PAYLOAD_SIZE  # Create dummy payload

    try:
        # Send packet
        sock.sendto(payload, (SERVER_IP, SERVER_PORT))
        
        # Receive timestamp from server
        data, _ = sock.recvfrom(1024)
        recv_time = time.time()
        
        server_time = float(data.decode())
        latency = (recv_time - send_time) * 1000  # Convert to ms
        latencies.append(latency)
        successful_packets += 1

    except socket.timeout:
        lost_packets += 1
        latencies.append(None)

    # Live stats
    avg_latency = sum(filter(None, latencies)) / successful_packets if successful_packets else 0
    packet_loss = (lost_packets / (successful_packets + lost_packets)) * 100

    sys.stdout.write(f"\r📡 Sent: {i+1}/{NUM_PACKETS} | ✅ Received: {successful_packets} | ❌ Lost: {lost_packets} | 📊 Latency: {avg_latency:.2f} ms | 🚫 Loss: {packet_loss:.2f}% ")
    sys.stdout.flush()

    time.sleep(PACKET_INTERVAL)  # Delay between packets

# Send END signal to stop the server
sock.sendto(b"END", (SERVER_IP, SERVER_PORT))

end_time = time.time()
elapsed_time = end_time - start_time

# Calculate throughput
total_bytes_sent = successful_packets * PAYLOAD_SIZE
throughput_mbps = (total_bytes_sent * 8) / (elapsed_time * 1e6)

# Final Stats
print("\n\n📊 Final Results:")
print(f" - Server IP: {SERVER_IP}")
print(f" - Packets sent: {NUM_PACKETS}")
print(f" - Packets received: {successful_packets}")
print(f" - Packet loss: {packet_loss:.2f}%")
if successful_packets:
    print(f" - Average latency: {avg_latency:.2f} ms")
else:
    print(" - No packets received.")
print(f" - Throughput: {throughput_mbps:.2f} Mbps")

sock.close()
