#include <iostream>
#include <fstream>
#include <string>

// C++ Simple File Encryption (XOR Cipher)

void encryptDecrypt(const std::string& inputFile, const std::string& outputFile, char key) {
    std::ifstream fin(inputFile, std::ios::binary);
    std::ofstream fout(outputFile, std::ios::binary);
    
    if (!fin) {
        std::cout << "Error opening input file!" << std::endl;
        return;
    }
    if (!fout) {
        std::cout << "Error opening output file!" << std::endl;
        return;
    }
    
    char ch;
    while (fin.get(ch)) {
        // Simple XOR encryption/decryption
        fout.put(ch ^ key);
    }
    
    std::cout << "Operation complete. Output saved to " << outputFile << std::endl;
    
    fin.close();
    fout.close();
}

int main() {
    std::string inFile, outFile;
    char key;
    
    std::cout << "--- File Encryptor/Decryptor (XOR) ---" << std::endl;
    
    // Create a dummy file for testing if it doesn't exist
    std::ofstream test("secret.txt");
    test << "This is a secret message used to test the encryption tool.";
    test.close();
    
    std::cout << "Created 'secret.txt' for testing." << std::endl;
    
    std::cout << "Enter input filename (e.g., secret.txt): ";
    std::cin >> inFile;
    
    std::cout << "Enter output filename (e.g., encrypted.dat): ";
    std::cin >> outFile;
    
    std::cout << "Enter encryption key (single character): ";
    std::cin >> key;
    
    encryptDecrypt(inFile, outFile, key);
    
    return 0;
}
