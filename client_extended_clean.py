import socket
import time
import sys
import random

# Function to get user input with validation
def get_user_input(prompt, default, min_val=None, max_val=None, dtype=str):
    """
    Helper function to get user input with validation.

    Parameters:
    - prompt (str): Message to display to the user
    - default: Default value if user provides no input
    - min_val, max_val: Range of acceptable values (optional)
    - dtype: Expected data type (int, float, str)

    Returns:
    - Validated user input of specified type
    """
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

# Display available test modes
print("\nSelect test mode:")
print("1 - One-time test (Fixed packets)")
print("2 - Continuous test until packet loss exceeds the limit")
print("3 - Maximum speed test (Fixed duration, Random packet sizes)")
print("4 - Continuous speed test (Fixed packet size, Manual stop)")

# Get the test mode selection from the user
TEST_MODE = get_user_input("Enter your choice (1, 2, 3, or 4)", 1, 1, 4, int)

# Get common user-defined values
SERVER_IP = get_user_input("Enter server IP address", "192.168.0.60")
SERVER_PORT = 5005
NETWORK_TIMEOUT = get_user_input("Enter network timeout duration (seconds)", 2, 1, 10, int)

# Mode-specific user inputs
if TEST_MODE == 3:
    SPEED_TEST_DURATION = get_user_input("Enter speed test duration (seconds)", 10, 1, 60, int)
    MIN_PACKET_SIZE = int(get_user_input("Enter minimum packet size (bytes)", 64, 1, 1472, int))
    MAX_PACKET_SIZE = int(get_user_input("Enter maximum packet size (bytes)", 1472, MIN_PACKET_SIZE, 1472, int))

elif TEST_MODE == 4:
    PAYLOAD_SIZE = int(get_user_input("Enter packet size for speed test (bytes)", 1472, 1, 1472, int))
    PACKET_INTERVAL = get_user_input("Enter packet interval (seconds)", 0.005, 0.0001, 1.0, float)

elif TEST_MODE == 1:
    NUM_PACKETS = int(get_user_input("Enter number of packets per test", 1000, 1, 100000, int))
    PACKET_SIZE = int(get_user_input("Enter packet size (bytes)", 128, 1, 1472, int))
    PACKET_INTERVAL = get_user_input("Enter packet interval (seconds)", 0.005, 0.0001, 1.0, float)

elif TEST_MODE == 2:
    PACKET_SIZE = int(get_user_input("Enter packet size (bytes)", 128, 1, 1472, int))
    PACKET_INTERVAL = get_user_input("Enter packet interval (seconds)", 0.005, 0.0001, 1.0, float)
    PACKET_LOSS_LIMIT = get_user_input("Enter maximum allowed packet loss (%)", 2.0, 0.1, 100.0, float)

# Create UDP socket for packet transmission
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)  # Set timeout for waiting on responses

# Function to execute the test with live results and final stats
def run_test(packet_size, num_packets=None, duration=None, loss_limit=None, packet_interval=0):
    packets_sent = 0
    packets_received = 0
    latencies = []
    max_pps = 0
    pps_counter = 0
    last_pps_update = time.time()
    start_time = time.time()
    last_received_time = start_time

    try:
        while (num_packets is None or packets_sent < num_packets) and (duration is None or time.time() - start_time < duration):
            send_time = time.time()
            payload = b"x" * packet_size

            try:
                sock.sendto(payload, (SERVER_IP, SERVER_PORT))
                packets_sent += 1
                pps_counter += 1

                data, _ = sock.recvfrom(1024)
                recv_time = time.time()
                packets_received += 1
                latencies.append((recv_time - send_time) * 1000)
                last_received_time = time.time()

            except socket.timeout:
                pass

            if time.time() - last_pps_update >= 1:
                max_pps = max(max_pps, pps_counter)
                pps_counter = 0
                last_pps_update = time.time()

            if time.time() - last_received_time > NETWORK_TIMEOUT:
                raise Exception(f"Server unreachable for {NETWORK_TIMEOUT}+ seconds")

            packet_loss = ((packets_sent - packets_received) / packets_sent) * 100 if packets_sent > 0 else 0

            elapsed_time = time.time() - start_time
            total_bytes_sent = packets_sent * packet_size
            throughput_kbps = (total_bytes_sent * 8) / (elapsed_time * 1000) if elapsed_time > 0 else 0
            throughput_kbytes = (total_bytes_sent) / elapsed_time / 1000 if elapsed_time > 0 else 0

            # Live results update
            sys.stdout.write(f"\r📡 Elapsed Time: {elapsed_time:.2f} sec | Sent: {packets_sent} | ✅ Received: {packets_received} | 🚫 Loss: {packet_loss:.2f}% | 🔄 Max PPS: {max_pps} | 📊 Speed: {throughput_kbps:.2f} kbit/s ({throughput_kbytes:.2f} kB/s) ")
            sys.stdout.flush()

            time.sleep(packet_interval if num_packets else 0)

    except KeyboardInterrupt:
        print("\n\n🛑 Test stopped by user.")

    except Exception as e:
        print(f"\n\n❌ ERROR: Connection lost during test. Reason: {e}")

    # Final Stats Calculation
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    min_latency = min(latencies) if latencies else 0
    max_latency = max(latencies) if latencies else 0

    # Print Final Results
    print("\n\n📊 Final Results:")
    print(f" - Server IP: {SERVER_IP}")
    print(f" - Packets sent: {packets_sent}")
    print(f" - Packets received: {packets_received}")
    print(f" - Packet loss: {packet_loss:.2f}%")
    if packets_received > 0:
        print(f" - Latency (min/avg/max): {min_latency:.2f} / {avg_latency:.2f} / {max_latency:.2f} ms")
    else:
        print(" - No packets received.")
    print(f" - Throughput: {throughput_kbps:.2f} kbit/s ({throughput_kbytes:.2f} kB/s)")

# Run selected test mode
if TEST_MODE == 1:
    run_test(PACKET_SIZE, num_packets=NUM_PACKETS, packet_interval=PACKET_INTERVAL)
elif TEST_MODE == 2:
    print("\n🚀 Running continuous test until packet loss exceeds the threshold...")
    run_test(PACKET_SIZE, loss_limit=PACKET_LOSS_LIMIT, packet_interval=PACKET_INTERVAL)
elif TEST_MODE == 3:
    run_test(random.randint(MIN_PACKET_SIZE, MAX_PACKET_SIZE), duration=SPEED_TEST_DURATION)
elif TEST_MODE == 4:
    print("\n🚀 Running continuous test. Press Ctrl + C to stop.")
    run_test(PAYLOAD_SIZE, packet_interval=PACKET_INTERVAL)
