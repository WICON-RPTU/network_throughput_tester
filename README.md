# Network Performance Test (UDP Latency & Throughput)

This script measures **latency**, **packet loss**, **throughput**, and **packet rate (PPS)** between two Raspberry Pi devices (or any networked computers) using **UDP packets**. It provides **real-time performance monitoring** and logs the final results.

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
python3 client_extended.py
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
Sends a **fixed number of packets** and reports **latency, throughput, packet loss, and PPS**.

#### **Mode 2 - Continuous Test (Stops at Packet Loss Limit)**
- Runs tests continuously until **packet loss exceeds the user-defined limit**.
- **Packet size increases** after each test cycle.

#### **Mode 3 - Maximum Speed Test (Fixed Duration, Random Packet Sizes)**  
- Runs for a **set duration** and measures **maximum possible throughput**.  
- **User defines a min and max packet size**, and sizes change randomly per packet.  
- Best for **real-world and stress testing**.

#### **Mode 4 - Continuous Speed Test (Fixed Packet Size, Manual Stop)**  
- Sends packets **indefinitely** at a **fixed size** until **manually stopped**.  
- Reports **real-time speed, packet loss, PPS, and latency**.  
- **Stops when the user presses** `Ctrl + C`.

---

### 4. Recommended Packet Sizes for Ethernet Testing

| **Test Type**               | **Recommended Packet Size** | **Reason** |
|----------------------------|----------------------------|------------|
| **Maximum Throughput**      | **1472 bytes** (UDP) / **1500 bytes** (Ethernet MTU) | Maximizes efficiency and reduces overhead |
| **Real-World Traffic**      | **512 - 1024 bytes** | Common packet size in internet traffic |
| **Low-Latency Networks**    | **64 - 128 bytes** | Used in VoIP, gaming, and real-time systems |
| **Stress Testing (Varied)** | **64 - 1472 bytes (randomized)** | Simulates different network loads |

---

### 5. Live Performance Analysis
During the test, real-time statistics will be displayed:
```bash
📡 Elapsed Time: 5.43 sec | Sent: 2500 | ✅ Received: 2495 | 🚫 Loss: 0.20% | 📊 Speed: 15.45 Mbps | 🔄 Max PPS: 8000
```
- **Sent**: Total packets sent  
- **Received**: Successfully received packets  
- **Lost**: Packets that were dropped  
- **Latency**: Min, Avg, Max values displayed at the end  
- **Speed**: Current network throughput in Mbps  
- **Max PPS**: Maximum packet rate per second achieved during the test  

---

### 6. Automatic Disconnection Detection
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
 - 🔄 Max PPS: 10,500 PPS
```
