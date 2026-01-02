import random

def story_1():
    print("\n--- Story: The Magical Forest ---")
    adj1 = input("Enter an adjective: ")
    noun1 = input("Enter a noun: ")
    verb1 = input("Enter a verb (past tense): ")
    adj2 = input("Enter an adjective: ")
    noun2 = input("Enter a noun (plural): ")
    
    story = f"\nOne day, a {adj1} wizard walked into a {noun1}. He {verb1} loudly, causing all the {adj2} {noun2} to scatter in fear!"
    print(story)

def story_2():
    print("\n--- Story: The Space Mission ---")
    name = input("Enter a name: ")
    noun1 = input("Enter a noun: ")
    number = input("Enter a number: ")
    verb1 = input("Enter a verb: ")
    adj = input("Enter an adjective: ")
    
    story = f"\nCaptain {name} looked out the window of the {noun1}. 'We have {number} seconds to {verb1}!' she shouted. It was a {adj} day in space."
    print(story)

def story_3():
    print("\n--- Story: Creating a Pizza ---")
    adj1 = input("Enter an adjective: ")
    food = input("Enter a food item: ")
    noun1 = input("Enter a noun: ")
    verb1 = input("Enter a verb: ")
    
    story = f"\nTo make the most {adj1} pizza, first you need dough made of {food}. Then, add a {noun1} on top and {verb1} it for 20 minutes."
    print(story)

def main():
    print("Welcome to the Ultimate Mad Libs Generator!")
    
    stories = [story_1, story_2, story_3]
    
    while True:
        print("\nMenu:")
        print("1. Play Random Story")
        print("2. Choose Story")
        print("0. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            selected_story = random.choice(stories)
            selected_story()
        elif choice == '2':
            print("1. The Magical Forest")
            print("2. The Space Mission")
            print("3. Creating a Pizza")
            c = input("Select (1-3): ")
            if c == '1': story_1()
            elif c == '2': story_2()
            elif c == '3': story_3()
            else: print("Invalid selection")
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print("Invalid Option")

if __name__ == "__main__":
    main()
