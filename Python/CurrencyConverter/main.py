class CurrencyConverter:
    def __init__(self):
        # Base currency is USD
        self.rates = {
            'USD': 1.0,
            'EUR': 0.92,
            'GBP': 0.79,
            'INR': 83.50,
            'JPY': 150.25,
            'AUD': 1.52,
            'CAD': 1.36
        }

    def convert(self, amount, from_currency, to_currency):
        if from_currency not in self.rates or to_currency not in self.rates:
            raise ValueError("Currency not supported")
        
        # Convert to USD first (Base)
        amount_in_usd = amount / self.rates[from_currency]
        
        # Convert from USD to Target
        final_amount = amount_in_usd * self.rates[to_currency]
        return round(final_amount, 2)

    def show_rates(self):
        print("\nCurrent Exchange Rates (Base: USD):")
        for curr, rate in self.rates.items():
            print(f"1 USD = {rate} {curr}")
        print()

def main():
    converter = CurrencyConverter()
    print("Welcome to the Currency Converter!")
    print(f"Supported Currencies: {', '.join(converter.rates.keys())}")

    while True:
        print("\nMenu:")
        print("1. Convert Currency")
        print("2. View Exchange Rates")
        print("0. Exit")
        
        choice = input("Enter option: ")
        
        if choice == '1':
            try:
                from_curr = input("Convert FROM (e.g. USD): ").upper()
                to_curr = input("Convert TO (e.g. INR): ").upper()
                
                if from_curr not in converter.rates or to_curr not in converter.rates:
                    print(f"Error: Invalid currency code. Supported: {list(converter.rates.keys())}")
                    continue

                amount = float(input(f"Enter amount in {from_curr}: "))
                if amount < 0:
                    print("Amount cannot be negative.")
                    continue
                
                result = converter.convert(amount, from_curr, to_curr)
                print(f"\n✅ {amount} {from_curr} = {result} {to_curr}")
            
            except ValueError:
                print("Invalid input format.")

        elif choice == '2':
            converter.show_rates()
        
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
