#include <iostream>
#include <iomanip>

// C++ Currency Converter
// demonstrates switch-case, formatting, and arithmetic

void displayMenu() {
    std::cout << "\n--- Currency Converter ---" << std::endl;
    std::cout << "1. USD to EUR" << std::endl;
    std::cout << "2. EUR to USD" << std::endl;
    std::cout << "3. USD to INR" << std::endl;
    std::cout << "4. INR to USD" << std::endl;
    std::cout << "5. Exit" << std::endl;
}

int main() {
    int choice;
    double amount, converted;
    
    // Fixed conversion rates (Example rates)
    const double USD_TO_EUR = 0.92;
    const double EUR_TO_USD = 1.09;
    const double USD_TO_INR = 83.50;
    const double INR_TO_USD = 0.012;
    
    while (true) {
        displayMenu();
        std::cout << "Select an option: ";
        std::cin >> choice;
        
        if (choice == 5) {
            std::cout << "Exiting..." << std::endl;
            break;
        }
        
        if (choice < 1 || choice > 5) {
            std::cout << "Invalid option." << std::endl;
            continue;
        }
        
        std::cout << "Enter amount: ";
        std::cin >> amount;
        
        std::cout << std::fixed << std::setprecision(2);
        
        switch (choice) {
            case 1:
                converted = amount * USD_TO_EUR;
                std::cout << "$" << amount << " USD = €" << converted << " EUR" << std::endl;
                break;
            case 2:
                converted = amount * EUR_TO_USD;
                std::cout << "€" << amount << " EUR = $" << converted << " USD" << std::endl;
                break;
            case 3:
                converted = amount * USD_TO_INR;
                std::cout << "$" << amount << " USD = ₹" << converted << " INR" << std::endl;
                break;
            case 4:
                converted = amount * INR_TO_USD;
                std::cout << "₹" << amount << " INR = $" << converted << " USD" << std::endl;
                break;
        }
    }
    
    return 0;
}
