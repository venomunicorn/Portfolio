#include <iostream>
#include <thread>
#include <chrono>

// C++ Simulated Game Server
// Uses threads to simulate concurrent operations

void serverThread() {
    std::cout << "[Server] Started. Listening on port 8080..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(2));
    
    std::cout << "[Server] Client connected from 127.0.0.1" << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(1));
    
    std::cout << "[Server] Received handshake packet." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(1));
    
    std::cout << "[Server] Sending Auth Token..." << std::endl;
}

void clientThread() {
    std::this_thread::sleep_for(std::chrono::seconds(1)); // Wait for server startup
    std::cout << "[Client] Connecting to server..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(2));
    
    std::cout << "[Client] Connection established." << std::endl;
    std::cout << "[Client] Sending login credentials..." << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(1));
    
    std::cout << "[Client] Authenticated! Ready to play." << std::endl;
}

int main() {
    std::cout << "--- Multiplayer System Simulation ---" << std::endl;
    
    std::thread server(serverThread);
    std::thread client(clientThread);
    
    server.join();
    client.join();
    
    std::cout << "\nSimulation Complete. System stable." << std::endl;
    return 0;
}
