import pandas as pd
import math
import numpy as np

def generate_multiplication_tables():
    """Generate multiplication tables from 1 to 50"""
    # Create headers for multiplication table (1 x 1, 1 x 2, ..., 1 x 12, etc.)
    data = []
    headers = ['Number'] + [f'x{i}' for i in range(1, 13)]  # Up to 12 times table
    
    for num in range(1, 51):
        row = [num] + [num * i for i in range(1, 13)]
        data.append(row)
    
    return pd.DataFrame(data, columns=headers)

def generate_squares():
    """Generate squares of numbers from 1 to 100"""
    data = []
    for num in range(1, 101):
        data.append([num, num**2])
    
    return pd.DataFrame(data, columns=['Number', 'Square'])

def generate_cubes():
    """Generate cubes of numbers from 1 to 100"""
    data = []
    for num in range(1, 101):
        data.append([num, num**3])
    
    return pd.DataFrame(data, columns=['Number', 'Cube'])

def generate_perfect_squares_with_roots():
    """Generate first 50 perfect squares with their square roots"""
    data = []
    for num in range(1, 51):
        perfect_square = num**2
        square_root = math.sqrt(perfect_square)
        data.append([num, perfect_square, square_root])
    
    return pd.DataFrame(data, columns=['Base Number', 'Perfect Square', 'Square Root'])

def generate_perfect_cubes_with_roots():
    """Generate first 50 perfect cubes with their cube roots"""
    data = []
    for num in range(1, 51):
        perfect_cube = num**3
        cube_root = round(perfect_cube**(1/3), 6)  # Round to 6 decimal places
        data.append([num, perfect_cube, cube_root])
    
    return pd.DataFrame(data, columns=['Base Number', 'Perfect Cube', 'Cube Root'])

def create_section_header(title):
    """Create a section header row"""
    return pd.DataFrame([[title] + [''] * 11], columns=['Section'] + [f'Col{i}' for i in range(1, 12)])

def main():
    """Main function to generate all data and save to CSV"""
    print("Generating mathematical data...")
    
    # Generate all datasets
    print("- Generating multiplication tables (1 to 50)...")
    mult_tables = generate_multiplication_tables()
    
    print("- Calculating squares (1 to 100)...")
    squares = generate_squares()
    
    print("- Calculating cubes (1 to 100)...")
    cubes = generate_cubes()
    
    print("- Generating perfect squares with roots (1 to 50)...")
    perfect_squares = generate_perfect_squares_with_roots()
    
    print("- Generating perfect cubes with roots (1 to 50)...")
    perfect_cubes = generate_perfect_cubes_with_roots()
    
    # Create the final CSV file with all sections
    print("- Compiling data into CSV format...")
    
    with open('mathematical_data.csv', 'w', newline='', encoding='utf-8') as f:
        # Write multiplication tables section
        f.write("MULTIPLICATION TABLES (1 to 50)\n")
        f.write("=" * 50 + "\n")
        mult_tables.to_csv(f, index=False, lineterminator='\n')
        f.write("\n\n")
        
        # Write squares section
        f.write("SQUARES OF NUMBERS (1 to 100)\n")
        f.write("=" * 50 + "\n")
        squares.to_csv(f, index=False, lineterminator='\n')
        f.write("\n\n")
        
        # Write cubes section
        f.write("CUBES OF NUMBERS (1 to 100)\n")
        f.write("=" * 50 + "\n")
        cubes.to_csv(f, index=False, lineterminator='\n')
        f.write("\n\n")
        
        # Write perfect squares section
        f.write("PERFECT SQUARES WITH SQUARE ROOTS (1 to 50)\n")
        f.write("=" * 50 + "\n")
        perfect_squares.to_csv(f, index=False, lineterminator='\n')
        f.write("\n\n")
        
        # Write perfect cubes section
        f.write("PERFECT CUBES WITH CUBE ROOTS (1 to 50)\n")
        f.write("=" * 50 + "\n")
        perfect_cubes.to_csv(f, index=False, lineterminator='\n')
    
    print("\n" + "="*60)
    print("DATA GENERATION COMPLETE!")
    print("="*60)
    print(f"File saved as: mathematical_data.csv")
    print(f"Total sections: 5")
    print(f"- Multiplication tables: {len(mult_tables)} rows")
    print(f"- Squares: {len(squares)} rows")
    print(f"- Cubes: {len(cubes)} rows")
    print(f"- Perfect squares with roots: {len(perfect_squares)} rows")
    print(f"- Perfect cubes with roots: {len(perfect_cubes)} rows")
    
    # Display sample data from each section
    print("\n" + "="*60)
    print("SAMPLE DATA PREVIEW:")
    print("="*60)
    
    print("\n1. MULTIPLICATION TABLES (First 5 rows):")
    print(mult_tables.head().to_string(index=False))
    
    print("\n2. SQUARES (First 10 rows):")
    print(squares.head(10).to_string(index=False))
    
    print("\n3. CUBES (First 10 rows):")
    print(cubes.head(10).to_string(index=False))
    
    print("\n4. PERFECT SQUARES WITH ROOTS (First 10 rows):")
    print(perfect_squares.head(10).to_string(index=False))
    
    print("\n5. PERFECT CUBES WITH ROOTS (First 10 rows):")
    print(perfect_cubes.head(10).to_string(index=False))

if __name__ == "__main__":
    main()
