#include <iostream>
#include <string>

// C++ Mad Libs Generator
// demonstrates string manipulation and user I/O

int main() {
    std::string noun1, adj1, noun2, verb1, adj2;
    
    std::cout << "--- Mad Libs Generator ---" << std::endl;
    std::cout << "Please enter the words as requested.\n" << std::endl;
    
    std::cout << "Enter a noun (person/place/thing): ";
    std::getline(std::cin, noun1);
    
    std::cout << "Enter an adjective (descriptive word): ";
    std::getline(std::cin, adj1);
    
    std::cout << "Enter another noun: ";
    std::getline(std::cin, noun2);
    
    std::cout << "Enter a verb ending in 'ing': ";
    std::getline(std::cin, verb1);
    
    std::cout << "Enter another adjective: ";
    std::getline(std::cin, adj2);
    
    std::cout << "\nHere is your story:\n" << std::endl;
    std::cout << "One day, a " << adj1 << " " << noun1 << " decided to go " << verb1 << "." << std::endl;
    std::cout << "Suddenly, it saw a giant " << noun2 << "!" << std::endl;
    std::cout << "It was a very " << adj2 << " experience." << std::endl;
    std::cout << "The end." << std::endl;
    
    return 0;
}
