#include <iostream>
#include <string>
#include <map>

// C++ Text Adventure Game
// Uses Classes and Switch-Case for state management

class Player {
public:
    std::string name;
    int health;
    bool hasKey;
    
    Player(std::string n) : name(n), health(100), hasKey(false) {}
};

int main() {
    std::string name;
    std::cout << "--- Dungeon Crawler ---" << std::endl;
    std::cout << "Enter your name: ";
    std::cin >> name;
    
    Player player(name);
    int currentRoom = 1;
    bool playing = true;
    
    while (playing && player.health > 0) {
        std::cout << "\n-----------------------" << std::endl;
        
        switch(currentRoom) {
            case 1:
                std::cout << "You are in a dark Entrance Hall." << std::endl;
                std::cout << "There are doors to the NORTH (2) and EAST (3)." << std::endl;
                std::cout << "Where do you go? (2/3): ";
                int choice;
                std::cin >> choice;
                if (choice == 2) currentRoom = 2;
                else if (choice == 3) currentRoom = 3;
                else std::cout << "Invalid direction." << std::endl;
                break;
                
            case 2:
                std::cout << "You are in the Armory." << std::endl;
                std::cout << "You found a Rusty Key on a table!" << std::endl;
                if (!player.hasKey) {
                    player.hasKey = true;
                    std::cout << "* Key Acquired *" << std::endl;
                }
                std::cout << "Return to the Entrance Hall? (1): ";
                std::cin >> choice;
                if (choice == 1) currentRoom = 1;
                break;
                
            case 3:
                std::cout << "You are in a Corridor. There is a huge locked door to the NORTH (4)." << std::endl;
                std::cout << "Or go back WEST (1)." << std::endl;
                std::cin >> choice;
                if (choice == 1) currentRoom = 1;
                else if (choice == 4) {
                    if (player.hasKey) {
                        std::cout << "You unlock the door with the Rusty Key..." << std::endl;
                        currentRoom = 4;
                    } else {
                        std::cout << "The door is locked. You need a key." << std::endl;
                    }
                }
                break;
                
            case 4:
                std::cout << "You entered the Treasure Room!" << std::endl;
                std::cout << "Congratulations " << player.name << "! You found the gold!" << std::endl;
                playing = false;
                break;
        }
    }
    
    return 0;
}
