import socket
import time
import sys

# Function to get user input with validation
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

# User chooses the test mode
print("\nSelect test mode:")
print("1 - One-time test")
print("2 - Continuous test until packet loss exceeds the limit")
print("3 - Maximum speed test (fixed duration)")
print("4 - Continuous speed test (fixed packet size, manual stop)")

TEST_MODE = get_user_input("Enter your choice (1, 2, 3, or 4)", 1, 1, 4, int)

# Get user-defined values
SERVER_IP = get_user_input("Enter server IP address", "192.168.100.4")  # Default changed to 192.168.100.4
SERVER_PORT = 5005
NETWORK_TIMEOUT = get_user_input("Enter network timeout duration (seconds)", 2, 1, 10, int)  # Now user-defined

if TEST_MODE in [3, 4]:
    PAYLOAD_SIZE = int(get_user_input("Enter packet size for speed test (bytes)", 1472, 1, 1472, int))

if TEST_MODE == 3:
    SPEED_TEST_DURATION = get_user_input("Enter speed test duration (seconds)", 10, 1, 60, int)
elif TEST_MODE != 4:
    NUM_PACKETS = int(get_user_input("Enter number of packets per test", 1000, 1, 100000, int))
    INITIAL_PACKET_SIZE = int(get_user_input("Enter initial packet size (bytes)", 128, 1, 1472, int))
    PACKET_INTERVAL = get_user_input("Enter packet interval (seconds)", 0.005, 0.0001, 1.0, float)

    if TEST_MODE == 2:
        PACKET_LOSS_LIMIT = get_user_input("Enter maximum allowed packet loss (%)", 2.0, 0.1, 100.0, float)
        PACKET_SIZE_INCREMENT = int(get_user_input("Enter packet size increment per test", 64, 1, 512, int))

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)  # Standard timeout for individual packets

if TEST_MODE in [3, 4]:
    if TEST_MODE == 3:
        print(f"\n🚀 Running maximum speed test to {SERVER_IP}:{SERVER_PORT} for {SPEED_TEST_DURATION} seconds with {PAYLOAD_SIZE} byte packets...\n")
        end_time = time.time() + SPEED_TEST_DURATION
    else:
        print(f"\n🚀 Running continuous speed test to {SERVER_IP}:{SERVER_PORT} with {PAYLOAD_SIZE} byte packets. Press Ctrl + C to stop.\n")

    packets_sent = 0
    packets_received = 0
    latencies = []
    start_time = time.time()
    last_received_time = time.time()  # Track last received packet

    try:
        while TEST_MODE == 4 or time.time() < end_time:
            send_time = time.time()
            payload = b"x" * PAYLOAD_SIZE  # Create dummy payload

            try:
                sock.sendto(payload, (SERVER_IP, SERVER_PORT))
                packets_sent += 1

                # Receive timestamp from server
                data, _ = sock.recvfrom(1024)
                recv_time = time.time()
                latency = (recv_time - send_time) * 1000  # Convert to ms
                latencies.append(latency)
                packets_received += 1
                last_received_time = time.time()  # Update last successful packet reception

            except socket.timeout:
                pass  # Packet was lost

            # Check if the server has been unreachable for the user-defined timeout duration
            if time.time() - last_received_time > NETWORK_TIMEOUT:
                raise Exception(f"Server unreachable for {NETWORK_TIMEOUT}+ seconds")

            # Live stats
            elapsed_time = time.time() - start_time
            total_bytes_sent = packets_sent * PAYLOAD_SIZE
            throughput_mbps = (total_bytes_sent * 8) / (elapsed_time * 1e6) if elapsed_time > 0 else 0
            packet_loss = ((packets_sent - packets_received) / packets_sent) * 100 if packets_sent > 0 else 0

            sys.stdout.write(f"\r📡 Sent: {packets_sent} | ✅ Received: {packets_received} | 🚫 Loss: {packet_loss:.2f}% | 📊 Speed: {throughput_mbps:.2f} Mbps ")
            sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n\n🛑 Speed test stopped by user.")

    except Exception as e:
        print(f"\n\n❌ ERROR: Connection lost during test. Reason: {e}")

    # Calculate min/avg/max latency
    if latencies:
        min_latency = min(latencies)
        avg_latency = sum(latencies) / len(latencies)
        max_latency = max(latencies)
    else:
        min_latency = avg_latency = max_latency = 0

    # Print final results
    elapsed_time = time.time() - start_time
    total_bytes_sent = packets_sent * PAYLOAD_SIZE
    throughput_mbps = (total_bytes_sent * 8) / (elapsed_time * 1e6) if elapsed_time > 0 else 0
    packet_loss = ((packets_sent - packets_received) / packets_sent) * 100 if packets_sent > 0 else 0

    print("\n📊 Speed Test Results:")
    print(f" - Server IP: {SERVER_IP}")
    print(f" - Test duration: {elapsed_time:.2f} seconds")
    print(f" - Packets sent: {packets_sent}")
    print(f" - Packets received: {packets_received}")
    print(f" - Packet loss: {packet_loss:.2f}%")
    print(f" - Throughput: {throughput_mbps:.2f} Mbps")
    print(f" - Latency (ms): Min = {min_latency:.2f}, Avg = {avg_latency:.2f}, Max = {max_latency:.2f}")

else:
    print("\n❌ ERROR: Only modes 3 and 4 support live speed testing.")
    sys.exit(1)

sock.close()
