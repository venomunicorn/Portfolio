#include <iostream>
#include <cstdlib>
#include <ctime>
#include <string>

// C++ Rock Paper Scissors
// demonstrates conditionals and random AI choice

std::string getChoiceString(int choice) {
    switch (choice) {
        case 1: return "Rock";
        case 2: return "Paper";
        case 3: return "Scissors";
        default: return "Unknown";
    }
}

int main() {
    std::srand(static_cast<unsigned int>(std::time(nullptr)));
    int userChoice, computerChoice;
    
    while (true) {
        std::cout << "\n--- Rock, Paper, Scissors ---" << std::endl;
        std::cout << "1. Rock" << std::endl;
        std::cout << "2. Paper" << std::endl;
        std::cout << "3. Scissors" << std::endl;
        std::cout << "4. Quit" << std::endl;
        std::cout << "Enter your choice (1-4): ";
        
        std::cin >> userChoice;
        
        if (userChoice == 4) break;
        if (userChoice < 1 || userChoice > 3) {
            std::cout << "Invalid choice. Please try again." << std::endl;
            continue;
        }
        
        computerChoice = std::rand() % 3 + 1; // 1 to 3
        
        std::cout << "You chose: " << getChoiceString(userChoice) << std::endl;
        std::cout << "Computer chose: " << getChoiceString(computerChoice) << std::endl;
        
        if (userChoice == computerChoice) {
            std::cout << "It's a Tie!" << std::endl;
        } else if ((userChoice == 1 && computerChoice == 3) || // Rock beats Scissors
                   (userChoice == 2 && computerChoice == 1) || // Paper beats Rock
                   (userChoice == 3 && computerChoice == 2)) { // Scissors beats Paper
            std::cout << "You Win!" << std::endl;
        } else {
            std::cout << "Computer Wins!" << std::endl;
        }
    }
    
    return 0;
}
