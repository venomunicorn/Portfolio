import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt

def main():
    print("--- Simple Machine Learning Model (Linear Regression) ---")
    
    # 1. Generate synthetic data
    # Let's simulate House Prices based on Size (sq ft)
    print("Generating synthetic data...")
    np.random.seed(42)
    X = 2000 * np.random.rand(100, 1) # Size between 0 and 2000 sq ft
    # True relationship: Price = 300 * Size + 50000 + Noise
    y = 300 * X + 50000 + np.random.randn(100, 1) * 50000
    
    # 2. Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set size: {X_train.shape[0]}")
    print(f"Testing set size: {X_test.shape[0]}")
    
    # 3. Train Model
    print("Training Linear Regression model...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    print(f"Model Coefficient (Price per sqft): ${model.coef_[0][0]:.2f}")
    print(f"Model Intercept (Base Price): ${model.intercept_[0]:.2f}")
    
    # 4. Predict
    y_pred = model.predict(X_test)
    
    # 5. Evaluate
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print("\n[Evaluation]")
    print(f"Mean Squared Error: {mse:.2f}")
    print(f"R2 Score: {r2:.2f}")
    
    # 6. Visualize
    try:
        plt.figure(figsize=(10, 6))
        plt.scatter(X_test, y_test, color='black', label='Actual Data')
        plt.plot(X_test, y_pred, color='blue', linewidth=3, label='Prediction')
        plt.title('House Price Prediction (Linear Regression)')
        plt.xlabel('Size (sq ft)')
        plt.ylabel('Price ($)')
        plt.legend()
        output_file = 'ml_result.png'
        plt.savefig(output_file)
        print(f"\nGraph saved to {output_file}")
    except Exception as e:
        print("Could not save plot:", e)

    # 7. Interactive Prediction
    print("\n--- Try it out ---")
    try:
        size = float(input("Enter house size (sq ft): "))
        pred_price = model.predict([[size]])
        print(f"Predicted Price: ${pred_price[0][0]:,.2f}")
    except:
        print("Invalid input.")

if __name__ == "__main__":
    main()
