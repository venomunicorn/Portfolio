#include <iostream>
#include <vector>
#include <string>

// C++ Chess Engine (Lite)
// Board representation and display

class ChessBoard {
    std::string board[8][8];
    
public:
    ChessBoard() {
        setupBoard();
    }
    
    void setupBoard() {
        // Init empty
        for (int i = 0; i < 8; i++)
            for (int j = 0; j < 8; j++)
                board[i][j] = " . ";
                
        // Pawns
        for (int j = 0; j < 8; j++) {
            board[1][j] = "BP ";
            board[6][j] = "WP ";
        }
        
        // Pieces
        std::string pieces = "RNBQKBNR";
        for (int j = 0; j < 8; j++) {
            board[0][j] = std::string("B") + pieces[j] + " ";
            board[7][j] = std::string("W") + pieces[j] + " ";
        }
    }
    
    void printBoard() {
        std::cout << "  a  b  c  d  e  f  g  h" << std::endl;
        std::cout << " +-----------------------+" << std::endl;
        for (int i = 0; i < 8; i++) {
            std::cout << 8 - i << "|";
            for (int j = 0; j < 8; j++) {
                std::cout << board[i][j];
            }
            std::cout << "|" << 8 - i << std::endl;
        }
        std::cout << " +-----------------------+" << std::endl;
        std::cout << "  a  b  c  d  e  f  g  h" << std::endl;
    }
    
    void makeMove(std::string from, std::string to) {
        // Simplified move logic (Input: "e2", "e4")
        int fromRow = 8 - (from[1] - '0');
        int fromCol = from[0] - 'a';
        int toRow = 8 - (to[1] - '0');
        int toCol = to[0] - 'a';
        
        board[toRow][toCol] = board[fromRow][fromCol];
        board[fromRow][fromCol] = " . ";
        
        std::cout << "Move: " << from << " -> " << to << std::endl;
    }
};

int main() {
    std::cout << "--- C++ Chess Engine v1.0 ---" << std::endl;
    ChessBoard cb;
    cb.printBoard();
    
    std::cout << "\nExecuting opening e2 -> e4..." << std::endl;
    cb.makeMove("e2", "e4");
    cb.printBoard();
    
    return 0;
}
