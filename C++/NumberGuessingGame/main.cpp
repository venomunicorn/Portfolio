#include <iostream>
#include <cstdlib>
#include <ctime>

// C++ Number Guessing Game
// demonstrates loops, random numbers, and user input

int main() {
    // Seed random number generator
    std::srand(static_cast<unsigned int>(std::time(nullptr)));
    
    int numberToGuess = std::rand() % 100 + 1; // 1 to 100
    int userGuess = 0;
    int attempts = 0;
    
    std::cout << "--- Welcome to the Number Guessing Game! ---" << std::endl;
    std::cout << "I have chosen a number between 1 and 100." << std::endl;
    std::cout << "Can you guess what it is?" << std::endl;
    
    while (userGuess != numberToGuess) {
        std::cout << "Enter your guess: ";
        if (!(std::cin >> userGuess)) {
            // Error handling for non-numeric input
            std::cout << "Invalid input. Please enter a number." << std::endl;
            std::cin.clear();
            std::cin.ignore(10000, '\n');
            continue;
        }
        
        attempts++;
        
        if (userGuess > numberToGuess) {
            std::cout << "Too high! Try again." << std::endl;
        } else if (userGuess < numberToGuess) {
            std::cout << "Too low! Try again." << std::endl;
        } else {
            std::cout << "\nCongratulations!" << std::endl;
            std::cout << "You guessed the number " << numberToGuess << " in " << attempts << " attempts." << std::endl;
        }
    }
    
    std::cout << "Thanks for playing!" << std::endl;
    return 0;
}
