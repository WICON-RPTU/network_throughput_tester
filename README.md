# Network Performance Test (UDP Latency & Throughput)

This script measures **latency**, **packet loss**, and **throughput** between two Raspberry Pi devices (or any networked computers) using **UDP packets**. It provides **real-time performance monitoring** and logs the final results.

## How to Use

### 1. Setup the Server (Receiving Side)
Run the following command on the **first Raspberry Pi** (server):
```bash
python3 server.py
```
The server will listen for incoming UDP packets and automatically restart when it receives an **"END"** signal.

### 2. Run the Client (Sending Side)
On the **second Raspberry Pi** (client), run:
```bash
python3 client.py
```
The script will prompt you to enter the following parameters:

| Parameter          | Description                                       | Default Value       |
|--------------------|---------------------------------------------------|---------------------|
| **Server IP**      | IP address of the receiving device                | `192.168.1.100`    |
| **Number of Packets** | Total number of packets to send               | `1000`              |
| **Packet Size**    | Size of each packet in bytes (1-1472)             | `128`               |
| **Packet Interval** | Time delay between packets in seconds (0.0001 - 1.0) | `0.005`          |

Press **Enter** to accept the default values or type your own.

---

### 3. Example Configuration for Low-Throughput, Low-Latency Network
For a **low-bandwidth but ultra-low-latency connection**, use:
```
Enter server IP address (default 192.168.1.100): 192.168.1.50
Enter number of packets (default 1000): 5000
Enter packet size (bytes) (default 128): 64
Enter packet interval (seconds) (default 0.005): 0.001
```
#### Recommended settings explanation:
- **Small packet size (64 bytes)** → Reduces serialization delay
- **Short packet interval (1ms)** → Ensures rapid updates without flooding
- **5000 packets** → Enough data for accurate latency measurement
- **Low bandwidth usage** → Keeps throughput below **1 Mbps**

---

### 4. Live Performance Analysis
While packets are being sent, real-time stats will be displayed:
```bash
Sent: 100/5000 | Received: 98 | Lost: 2 | Latency: 1.25 ms | Loss: 0.40%
```
- **Sent**: Total packets sent  
- **Received**: Successfully received packets  
- **Lost**: Packets that were dropped  
- **Latency**: Average round-trip time in milliseconds  
- **Loss**: Percentage of packets lost  

---

### 5. Final Results
Once the test completes, the script will display:
```bash
Final Results:
 - Server IP: 192.168.1.50
 - Packets sent: 5000
 - Packets received: 4998
 - Packet loss: 0.04%
 - Average latency: 1.15 ms
 - Throughput: 0.41 Mbps
```
