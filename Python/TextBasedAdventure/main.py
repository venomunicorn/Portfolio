import time
import os

class GameState:
    def __init__(self):
        self.inventory = []
        self.location = 'start'
        self.alive = True

    def add_item(self, item):
        self.inventory.append(item)
        print(f"\n🌟 Acquired: {item}")

    def has_item(self, item):
        return item in self.inventory

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_slow(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print()

def scene_start(state):
    clear_screen()
    print_slow("You wake up in a cold, damp cave. It's dark.")
    print_slow("To your NORTH is a faint light. To your EAST is a strange humming sound.")
    
    while True:
        choice = input("\nWhat do you do? (north/east/check inventory): ").lower().strip()
        
        if choice == 'north':
            return 'forest_clearing'
        elif choice == 'east':
            return 'machine_room'
        elif choice == 'check inventory':
            print(f"Inventory: {state.inventory if state.inventory else 'Empty'}")
        else:
            print("I don't understand that.")

def scene_forest_clearing(state):
    clear_screen()
    print_slow("You emerge into a moonlit forest clearing.")
    print_slow("There is a rusty KEY lying on a stump.")
    print_slow("A path leads back into the CAVE (south) or towards a creepy CASTLE (north).")
    
    while True:
        choice = input("\nWhat do you do? (take key/south/north): ").lower().strip()
        
        if choice == 'take key':
            if not state.has_item('Rusty Key'):
                state.add_item('Rusty Key')
            else:
                print("You already have the key.")
        elif choice == 'south':
            return 'start'
        elif choice == 'north':
            return 'castle_gate'
        elif choice == 'check inventory':
            print(f"Inventory: {state.inventory if state.inventory else 'Empty'}")
        else:
            print("I don't understand that.")

def scene_machine_room(state):
    clear_screen()
    print_slow("You find a room with a strange, humming metal box.")
    print_slow("There is a button. And a path back WEST.")
    
    while True:
        choice = input("\nWhat do you do? (push button/west): ").lower().strip()
        
        if choice == 'push button':
            if state.has_item('Golden Gear'):
                print_slow("The machine whirs to life! A secret compartment opens.")
                print_slow("Found: DIAMOND. You win this path!")
                if not state.has_item('Diamond'):
                    state.add_item('Diamond')
            else:
                print_slow("The machine sputters. It seems to miss a part.")
        elif choice == 'west':
            return 'start'
        else:
            print("I don't understand that.")

def scene_castle_gate(state):
    clear_screen()
    print_slow("You stand before a massive iron gate leading to the Castle.")
    print_slow("It is locked.")
    
    while True:
        choice = input("\nWhat do you do? (open gate/south): ").lower().strip()
        
        if choice == 'open gate':
            if state.has_item('Rusty Key'):
                print_slow("The key turns! The gate creaks open...")
                return 'castle_hall'
            else:
                print_slow("It's locked tight. You need a key.")
        elif choice == 'south':
            return 'forest_clearing'
        else:
            print("I don't understand that.")

def scene_castle_hall(state):
    clear_screen()
    print_slow("You are in the Castle Hall. It's magnificent.")
    print_slow("There is a shiny GOLDEN GEAR on a pedestal.")
    print_slow("You can leave SOUTH.")

    while True:
        choice = input("\nWhat do you do? (take gear/south): ").lower().strip()
        
        if choice == 'take gear':
            if not state.has_item('Golden Gear'):
                state.add_item('Golden Gear')
                print_slow("This looks like it belongs in a machine...")
            else:
                print("You already have it.")
        elif choice == 'south':
            return 'castle_gate'
        else:
            print("I don't understand that.")

def main():
    state = GameState()
    
    scenes = {
        'start': scene_start,
        'forest_clearing': scene_forest_clearing,
        'machine_room': scene_machine_room,
        'castle_gate': scene_castle_gate,
        'castle_hall': scene_castle_hall
    }
    
    while state.alive:
        if state.location in scenes:
            next_scene = scenes[state.location](state)
            state.location = next_scene
        else:
            print("Error: Unknown location.")
            break

if __name__ == "__main__":
    main()
