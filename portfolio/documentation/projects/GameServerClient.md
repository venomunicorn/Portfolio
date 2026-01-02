# Game Server & Client Documentation

**Category**: C++ Systems
**Path**: `C++/GameServerClient`
**Version**: 1.0 Simulation

## Overview
The **Game Server Client** project is a simulation of a multiplayer architecture. It demonstrates the fundamental concepts of concurrent execution using multithreading in C++. The C++ console application simulates a server listening for connections and a client initiating a handshake, running on separate threads to mimic asynchronous network behavior.

## Key Features

### 1. Concurrent Execution (C++)
- **Multithreading**: Uses `std::thread` to run the server and client logic simultaneously.
- **Synchronization**: Uses `std::this_thread::sleep_for` to simulate network latency (RRT) and processing time.
- **Handshake Simulation**: Modeled sequence:
  1. Server Start & Listen.
  2. Client Connect.
  3. Connection Established.
  4. Authentication Token Exchange.

### 2. Dashboard Interface (Web Demo)
The web demo provides a graphical admin panel to visualize the server-client relationship:
- **Server Control**: Start/Stop the virtual server.
- **Real-time Metrics**: Displays simulated packet rates (Packets/sec) and connected client count.
- **Latency Monitoring**: Randomly fluctuates simulated ping (ms) for each connected client to mimic network instability.
- **Console Log**: A scrolling terminal window showing system events, errors, and status updates timestamps.

### 3. Usage Logic
- **Server Side**: Maintains a list of connected users and broadcasts simulated state updates.
- **Client Side**: Connects to the server address (default: `localhost:8080`), performs a handshake, and enters the "Ready" state.

## Architecture

### Directory Structure
```
GameServerClient/
├── main.cpp    # Multithreaded C++ simulation
└── demo.html   # Visual dashboard simulation
```

### Critical Components (`main.cpp`)
- **`serverThread()`**: Represents the host process. Starts, listens, and accepts the client.
- **`clientThread()`**: Represents the player. Waits for server startup, connects, and sends credentials.
- **`main()`**: Spawns both threads and waits for them to complete using `.join()`.

## Setup & Compilation

### Prerequisites
- C++11 compliant compiler (for `<thread>` and `<chrono>`)

### Build Instructions
1.  **Navigate directly**:
    ```powershell
    cd "C:\Users\kaush\Downloads\ProjectsCode\Startup VAYU\C++\GameServerClient"
    ```
2.  **Compile**:
    ```powershell
    g++ main.cpp -o server_sim
    ```
3.  **Run**:
    ```powershell
    .\server_sim
    ```
    *Note: Output will be interleaved as both threads print to stdout simultaneously.*

## Web Demo Usage
- Open `demo.html` in a versatile web browser.
- **Server**: Click "Start Server". The status indicator will turn green (Online).
- **Client**: Enter a name (or keep "Player1") and click "Connect".
- **Observe**: Watch the console log for the handshake process and the client list for ping updates.
