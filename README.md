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
| **Test Mode**      | Choose between different test types               | `1` (One-time test) |
| **Server IP**      | IP address of the receiving device                | `192.168.100.4`    |
| **Network Timeout**| Time to wait before assuming disconnection (sec) | `2`                 |
| **Packet Size**    | Size of each packet in bytes (1-1472)             | `128` (varies)      |
| **Packet Interval**| Time delay between packets (0.0001 - 1.0 sec)     | `0.005`             |
| **Max Packet Loss**| Packet loss threshold for stopping tests (%)      | `2.0`               |
| **Test Duration**  | For speed tests, total runtime (seconds)          | `10`                |

Press **Enter** to accept the default values or type your own.

---

### 3. Test Modes
The script supports **four different test modes**:

#### **Mode 1 - One-Time Test**
Sends a **fixed number of packets** and reports **latency, throughput, and packet loss**.

#### **Mode 2 - Continuous Test (Stops at Packet Loss Limit)**
- Runs tests continuously until **packet loss exceeds the user-defined limit**.
- **Packet size increases** after each test cycle.

#### **Mode 3 - Maximum Speed Test (Fixed Duration)**
- Runs for a **set duration** and measures **maximum possible throughput**.
- Uses **large packet sizes** to push network performance.

#### **Mode 4 - Continuous Speed Test (Fixed Packet Size)**
- Sends packets **indefinitely** at a **fixed size** until **manually stopped**.
- Reports **real-time speed, packet loss, and latency**.
- **Stops when the user presses** `Ctrl + C`.

---

### 4. Live Performance Analysis
During the test, real-time statistics will be displayed:
```bash
📡 Sent: 1000 | ✅ Received: 998 | 🚫 Loss: 0.20% | 📊 Speed: 15.45 Mbps
```
- **Sent**: Total packets sent  
- **Received**: Successfully received packets  
- **Lost**: Packets that were dropped  
- **Latency**: Min, Avg, Max values displayed at the end  
- **Speed**: Current network throughput in Mbps  

---

### 5. Automatic Disconnection Detection
If **no response from the server** is received within the **user-defined timeout (e.g., 2 seconds)**, the test will stop and display final results.

Example error message:
```
❌ ERROR: Connection lost during test. Reason: Server unreachable for 2+ seconds
📊 Speed Test Results:
 - Server IP: 192.168.100.4
 - Test duration: 14.32 seconds
 - Packets sent: 5000
 - Packets received: 4320
 - Packet loss: 13.60%
 - Throughput: 12.84 Mbps
 - Latency (ms): Min = 1.22, Avg = 2.45, Max = 5.67
```

---

## Why Use This?
- **Measure real-time latency & packet loss**  
- **Analyze throughput for low-latency networks**  
- **Test Wi-Fi vs Ethernet stability**  
- **Detect network failures automatically**  
- **Monitor network performance live**  

---
