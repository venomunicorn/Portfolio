#include <iostream>
#include <vector>

// C++ Sudoku Solver
// Uses Backtracking Algorithm

const int N = 9;

void printGrid(int grid[N][N]) {
    for (int row = 0; row < N; row++) {
        for (int col = 0; col < N; col++)
            std::cout << grid[row][col] << " ";
        std::cout << std::endl;
    }
}

bool isSafe(int grid[N][N], int row, int col, int num) {
    // Check row
    for (int x = 0; x <= 8; x++)
        if (grid[row][x] == num)
            return false;
            
    // Check col
    for (int x = 0; x <= 8; x++)
        if (grid[x][col] == num)
            return false;
            
    // Check 3x3 box
    int startRow = row - row % 3;
    int startCol = col - col % 3;
    
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (grid[i + startRow][j + startCol] == num)
                return false;
                
    return true;
}

bool solveSudoku(int grid[N][N], int row, int col) {
    if (row == N - 1 && col == N)
        return true;
        
    if (col == N) {
        row++;
        col = 0;
    }
    
    if (grid[row][col] > 0)
        return solveSudoku(grid, row, col + 1);
        
    for (int num = 1; num <= N; num++) {
        if (isSafe(grid, row, col, num)) {
            grid[row][col] = num;
            if (solveSudoku(grid, row, col + 1))
                return true;
        }
        grid[row][col] = 0; // Backtrack
    }
    return false;
}

int main() {
    int grid[N][N] = { 
        { 3, 0, 6, 5, 0, 8, 4, 0, 0 },
        { 5, 2, 0, 0, 0, 0, 0, 0, 0 },
        { 0, 8, 7, 0, 0, 0, 0, 3, 1 },
        { 0, 0, 3, 0, 1, 0, 0, 8, 0 },
        { 9, 0, 0, 8, 6, 3, 0, 0, 5 },
        { 0, 5, 0, 0, 9, 0, 6, 0, 0 },
        { 1, 3, 0, 0, 0, 0, 2, 5, 0 },
        { 0, 0, 0, 0, 0, 0, 0, 7, 4 },
        { 0, 0, 5, 2, 0, 6, 3, 0, 0 } 
    };

    std::cout << "--- Sudoku Solver ---" << std::endl;
    std::cout << "Original Grid:" << std::endl;
    printGrid(grid);
    
    if (solveSudoku(grid, 0, 0)) {
        std::cout << "\nSolved Grid:" << std::endl;
        printGrid(grid);
    } else {
        std::cout << "No solution exists." << std::endl;
    }
    
    return 0;
}
