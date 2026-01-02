import csv
import os

def create_sample_csv():
    with open('data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Month', 'Sales', 'Expenses'])
        writer.writerow(['Jan', '1000', '800'])
        writer.writerow(['Feb', '1200', '900'])
        writer.writerow(['Mar', '1500', '1000'])
        writer.writerow(['Apr', '1300', '850'])
    print("Created 'data.csv' sample file.")

def plot_data(x_data, y_data, x_label, y_label):
    print("\n--- Generating Plot ---")
    try:
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        plt.bar(x_data, y_data, color='skyblue')
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(f"{y_label} vs {x_label}")
        plt.savefig('plot_output.png')
        print("Plot saved to 'plot_output.png'")
        plt.show()
    except ImportError:
        print("[Simulated Plot]")
        print(f"X: {x_data}")
        print(f"Y: {y_data}")
        print("Matplotlib not found. Graphical plot skipped.")

def main():
    print("--- Simple Data Viz Tool ---")
    
    if not os.path.exists('data.csv'):
        create_sample_csv()
    
    filename = input("Enter CSV filename (default: data.csv): ").strip()
    if not filename: filename = 'data.csv'
    
    x_col_idx = 0 # Simple defaults
    y_col_idx = 1
    
    x_vals = []
    y_vals = []
    
    try:
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            header = next(reader)
            print(f"Columns: {header}")
            
            for row in reader:
                x_vals.append(row[x_col_idx])
                y_vals.append(float(row[y_col_idx]))
                
        plot_data(x_vals, y_vals, header[x_col_idx], header[y_col_idx])
        
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    main()
