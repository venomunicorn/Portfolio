import math

class Calculator:
    def __init__(self):
        self.history = []

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, a, b):
        return math.pow(a, b)

    def sqrt(self, a):
        if a < 0:
            raise ValueError("Cannot take square root of negative number")
        return math.sqrt(a)

    def sin(self, a):
        return math.sin(math.radians(a))

    def cos(self, a):
        return math.cos(math.radians(a))

    def tan(self, a):
        return math.tan(math.radians(a))

    def log(self, a):
        if a <= 0:
            raise ValueError("Logarithm valid only for positive numbers")
        return math.log10(a)

    def add_to_history(self, operation, result):
        entry = f"{operation} = {result}"
        self.history.append(entry)
        if len(self.history) > 5:
            self.history.pop(0)

    def show_history(self):
        print("\n--- History (Last 5) ---")
        if not self.history:
            print("Empty")
        else:
            for item in self.history:
                print(item)
        print("------------------------\n")

def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    calc = Calculator()
    print("Welcome to the Advanced Python Calculator!")
    print("Features: Arithmetic, Power, Sqrt, Log, Trigonometry (degrees), History")

    while True:
        print("\nOptions:")
        print("1. Add (+)")
        print("2. Subtract (-)")
        print("3. Multiply (*)")
        print("4. Divide (/)")
        print("5. Power (^)")
        print("6. Square Root (sqrt)")
        print("7. Sin")
        print("8. Cos")
        print("9. Tan")
        print("10. Log (base 10)")
        print("11. Show History")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == '0':
            print("Goodbye!")
            break
        
        elif choice == '11':
            calc.show_history()
            continue

        try:
            if choice in ['1', '2', '3', '4', '5']:
                n1 = get_number("Enter first number: ")
                n2 = get_number("Enter second number: ")
                
                if choice == '1':
                    res = calc.add(n1, n2)
                    op = f"{n1} + {n2}"
                elif choice == '2':
                    res = calc.subtract(n1, n2)
                    op = f"{n1} - {n2}"
                elif choice == '3':
                    res = calc.multiply(n1, n2)
                    op = f"{n1} * {n2}"
                elif choice == '4':
                    res = calc.divide(n1, n2)
                    op = f"{n1} / {n2}"
                elif choice == '5':
                    res = calc.power(n1, n2)
                    op = f"{n1} ^ {n2}"
                
                print(f"Result: {res}")
                calc.add_to_history(op, res)

            elif choice in ['6', '7', '8', '9', '10']:
                n1 = get_number("Enter number: ")
                
                if choice == '6':
                    res = calc.sqrt(n1)
                    op = f"sqrt({n1})"
                elif choice == '7':
                    res = calc.sin(n1)
                    op = f"sin({n1})"
                elif choice == '8':
                    res = calc.cos(n1)
                    op = f"cos({n1})"
                elif choice == '9':
                    res = calc.tan(n1)
                    op = f"tan({n1})"
                elif choice == '10':
                    res = calc.log(n1)
                    op = f"log({n1})"

                print(f"Result: {res}")
                calc.add_to_history(op, res)

            else:
                print("Invalid choice, please try again.")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
