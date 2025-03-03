import socket
import time

# Server settings
UDP_IP = "0.0.0.0"  # Listen on all interfaces
UDP_PORT = 5005  # Port to listen on

def start_server():
    while True:  # Keep restarting the server on failure or END signal
        try:
            # Create UDP socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((UDP_IP, UDP_PORT))
            print(f"Server started on {UDP_PORT}, waiting for packets...")

            while True:
                data, addr = sock.recvfrom(65507)  # Max UDP packet size

                if data == b"END":
                    print(f"Received END signal from {addr}. Restarting server...")
                    break  # Breaks the inner loop, restarting the server

                timestamp = time.time()
                sock.sendto(str(timestamp).encode(), addr)  # Send response

        except Exception as e:
            print(f"Error: {e}. Restarting server...")
            time.sleep(2)  # Prevent immediate crash loops

# Start the server
start_server()
