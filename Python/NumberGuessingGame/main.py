import random
import time

def get_difficulty():
    print("\nSelect Difficulty:")
    print("1. Easy (1-10, 5 attempts)")
    print("2. Medium (1-50, 7 attempts)")
    print("3. Hard (1-100, 10 attempts)")
    
    while True:
        choice = input("Enter option (1/2/3): ")
        if choice == '1':
            return 10, 5
        elif choice == '2':
            return 50, 7
        elif choice == '3':
            return 100, 10
        else:
            print("Invalid choice.")

def play_game(max_num, max_attempts):
    secret_number = random.randint(1, max_num)
    attempts = 0
    print(f"\nI have selected a number between 1 and {max_num}.")
    print(f"You have {max_attempts} attempts to guess it.")

    while attempts < max_attempts:
        try:
            guess = int(input(f"\nAttempt {attempts + 1}/{max_attempts}: Enter guess: "))
        except ValueError:
            print("Please enter a valid integer.")
            continue
        
        attempts += 1
        
        if guess < secret_number:
            print("Too Low!")
        elif guess > secret_number:
            print("Too High!")
        else:
            print(f"🎉 Congratulations! You guessed the number {secret_number} in {attempts} attempts!")
            return
            
    print(f"\n😞 Game Over! The number was {secret_number}.")

def ai_solve_demo(max_num):
    print(f"\n--- AI Solver Demo (Binary Search) for range 1-{max_num} ---")
    low = 1
    high = max_num
    secret_number = random.randint(1, max_num)
    print(f"Secret Number is: {secret_number} (Hidden from AI)")
    attempts = 0
    
    while low <= high:
        attempts += 1
        guess = (low + high) // 2
        print(f"AI guesses: {guess}")
        time.sleep(0.5) 
        
        if guess < secret_number:
            print("Result: Too Low -> Adjusting range up")
            low = guess + 1
        elif guess > secret_number:
            print("Result: Too High -> Adjusting range down")
            high = guess - 1
        else:
            print(f"AI found {secret_number} in {attempts} attempts!")
            return

def main():
    print("Welcome to the Enhanced Number Guessing Game!")
    
    while True:
        print("\nMain Menu:")
        print("1. Play Game")
        print("2. Watch AI Solve (Demo)")
        print("0. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            max_num, max_attempts = get_difficulty()
            play_game(max_num, max_attempts)
        elif choice == '2':
            print("Select range for AI:")
            print("1. 1-100")
            print("2. 1-1000")
            c = input("Choice: ")
            limit = 1000 if c == '2' else 100
            ai_solve_demo(limit)
        elif choice == '0':
            print("Thanks for playing!")
            break
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
