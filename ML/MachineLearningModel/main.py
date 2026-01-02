class LinearRegression:
    def __init__(self, learning_rate=0.01, iterations=1000):
        self.lr = learning_rate
        self.iterations = iterations
        self.weights = 0
        self.bias = 0

    def fit(self, X, y):
        n_samples = len(X)
        print(f"Training on {n_samples} samples...")
        
        for _ in range(self.iterations):
            # Predicted values y_pred = wx + b
            y_pred = [self.weights * x + self.bias for x in X]
            
            # Gradients
            # dw = (2/n) * sum(x * (y_pred - y))
            # db = (2/n) * sum(y_pred - y)
            
            dw = (2 / n_samples) * sum([x * (yp - yi) for x, yp, yi in zip(X, y_pred, y)])
            db = (2 / n_samples) * sum([(yp - yi) for yp, yi in zip(y_pred, y)])
            
            # Update params
            self.weights -= self.lr * dw
            self.bias -= self.lr * db
            
    def predict(self, X):
        return [self.weights * x + self.bias for x in X]

def main():
    print("--- Linear Regression from Scratch (Pure Python) ---")
    
    # Dataset: Years of Experience vs Salary (Approx)
    X = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] # Years
    y = [30000, 35000, 42000, 48000, 55000, 62000, 68000, 75000, 80000, 90000] # Salary
    
    print("Dataset (Experience vs Salary):")
    for i in range(len(X)):
        print(f"  {X[i]} years -> ${y[i]}")

    model = LinearRegression(learning_rate=0.01, iterations=1000)
    model.fit(X, y)
    
    print("\nTraining Complete.")
    print(f"Weight (Slope): {model.weights:.2f}")
    print(f"Bias (Intercept): {model.bias:.2f}")
    
    print("\n--- Prediction Mode ---")
    while True:
        val = input("Enter Years of Experience to predict Salary (or 'exit'): ")
        if val.lower() == 'exit':
            break
        try:
            exp = float(val)
            pred = model.predict([exp])[0]
            print(f"Predicted Salary for {exp} years: ${pred:.2f}")
        except ValueError:
            print("Invalid input.")

if __name__ == "__main__":
    main()
