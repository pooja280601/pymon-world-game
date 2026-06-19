'''
Student Name: Pooja Bommashettihalli Rangadhamaiah
Student Number: S4110034
Highest Part attempted: HD Level
'''

'''
DESIGN PROCESS:

PASS LEVEL:
Designing the PASS level for this assignment was straightforward. I defined core classes to handle basic 
gameplay functionality, such as creating locations, Pymon creatures, and allowing simple player interactions.
The initial setup involved basic movement, Pymon and location inspection, and core interactions, which were easy
to implement. This level formed the foundation for the entire game, setting up essential structures that I would 
expand upon in later levels.

CREDIT LEVEL:
For the CREDIT level, I added additional functionalities on top of the PASS level, such as handling inventory and
enabling Pymon switching. The validations became more extensive here, ensuring that item interactions and 
creature challenges worked smoothly. Overall, implementing this level was a straightforward 
extension of the PASS level, enhancing the gameplay experience without significantly increasing complexity.

DI LEVEL:
The DI level added a layer of complexity beyond the CREDIT level. This stage required me to introduce more options, 
including additional classes and methods to handle these functionalities. Managing Pymon energy and introducing 
validations for extra features. Although the design was more challenging compared to the previous levels, 
I was able to work out the logic and structure needed to implement these added functionalities.

HD LEVEL:
The HD level was the most challenging part of this assignment. This stage involved advanced features such as 
tracking battle statistics, saving/loading game progress, and supporting customizable gameplay elements.
. Generating key statistics and saving them to a file added complexity to the overall design. 
This level demanded more effort compared to the earlier ones, but I successfully implemented the features, 
creating a richer, more immersive experience.

FLOW OF CODE:
To ensure a smooth flow for the entire program, I designed a main function with a central menu that lets 
users choose between PASS, CREDIT, DI, and HD levels. When a level is selected, it initializes the 
corresponding features and displays relevant options. Within each level, actions are executed based on user input, 
allowing the player to seamlessly progress from basic to advanced gameplay. This approach organizes the code 
logically, guiding users through each level's functionalities and ensuring a cohesive gaming experience.
'''

#Importing necessary libraries
import random
import os
import datetime
import sys

'''
The Location class represents a place in the Pymon game world, characterized by its name, description, and 
connected pathways. Each location may have creatures, items, and directional doors to connect with other locations. 
The class provides methods to add creatures and items, establish connections with neighboring locations in specific 
directions, and retrieve various attributes like name, description, doors, creatures, and items. Additionally, 
it allows setting the name and description as needed.
'''
class Location:
    def __init__(self, name="New room", description=""):
        self.name = name
        self.description = description
        self.doors = {"west": None, "north": None, "east": None, "south": None}
        self.creatures = []
        self.items = []

    def add_creature(self, creature):
        self.creatures.append(creature)

    def add_item(self, item):
        self.items.append(item)

    def connect(self, direction, other_location):
        self.doors[direction] = other_location
        opposite_direction = {"west": "east", "north": "south", "east": "west", "south": "north"}[direction]
        other_location.doors[opposite_direction] = self

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_doors(self):
        return self.doors

    def get_creatures(self):
        return self.creatures

    def get_items(self):
        return self.items

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description


"""
The Creature class defines a creature within the Pymon game world, characterized by a nickname, description, 
and current location. This class provides methods to retrieve the creature's nickname, description, and 
location. Additionally, it includes a method to update the creature's location, supporting its movement 
throughout the Pymon game world.
"""
class Creature:
    def __init__(self, nickname, description, location):
        self.nickname = nickname
        self.description = description
        self.location = location

    def get_nickname(self):
        return self.nickname

    def get_description(self):
        return self.description

    def get_location(self):
        return self.location

    def set_location(self, location):
        self.location = location


"""
The Pymon class represents a playable creature within the Pymon game, inheriting from the Creature class 
and introducing additional attributes like energy, inventory, immunity status, and movement tracking. 
This class includes methods to manage the Pymon's inventory, use items, gain immunity, and challenge 
other Pymon creatures in the game world. It also supports movement across locations and energy management, 
allowing the player to interact dynamically with other creatures and objects within the Pymon environment.
"""
class Pymon(Creature):
    def __init__(self, nickname, description, location, energy=3):
        super().__init__(nickname, description, location)
        self.energy = energy
        self.inventory = []
        self.has_immunity = False
        self.last_location = location
        self.move_counter = 0

    def add_to_inventory(self, item):
        if item.is_pickable():
            self.inventory.append(item)
            print(f"{item.get_name()} has been added to your inventory")

    def use_item(self, item_name):
        for item in self.inventory:
            if item.get_name().lower() == item_name.lower():
                if item.use(self):
                    self.inventory.remove(item)
                return
        print(f"{item_name} is not in your inventory or cannot be used")

    def give_immunity(self):
        self.has_immunity = True

    def challenge(self, opponent):
        if not isinstance(opponent, Pymon) or opponent == self:
            print(f"{opponent.get_nickname()} just ignored you")
            return
        print(f"Challenging {opponent.get_nickname()} to a battle!")

    def challenge_creature(self):
        location = self.pymon.get_location()
        opponent = next((c for c in location.get_creatures() if isinstance(c, Pymon) and c != self.pymon), None)
        
        if opponent:
            self.pymon.challenge(opponent)
            self.battle(opponent)
        else:
            print("No Pymon here to challenge.")

    def get_energy(self):
        return self.energy

    def set_energy(self, energy):
        self.energy = max(0,energy)
        if self.energy ==0:
            print("Energy is zero. Cannot go further down")
    
    def move(self, direction):
        if self.location is not None and direction in self.location.doors:
            new_location = self.location.doors[direction]
            if new_location is not None:
                if self in self.location.creatures:
                    self.location.creatures.remove(self)
                new_location.add_creature(self)
                self.location = new_location
                print(f"{self.nickname} moved to {new_location.get_name()}.")
                self.move_counter += 1
                return True  
            else:
                print("No access to " + direction)
                return False  
        else:
            print("Invalid direction or no current location.")
            return False  


"""
The InvalidDirectionException and InvalidInputFileFormat classes define custom exceptions used within the 
Pymon game to handle specific error scenarios. InvalidDirectionException is raised when a movement attempt 
is made in an unsupported direction, while InvalidInputFileFormat is triggered if the input file format 
does not meet the expected requirements. These custom exceptions help provide more descriptive error 
messages and aid in debugging and handling errors effectively in the game.
"""
class InvalidDirectionException(Exception):
    pass

class InvalidInputFileFormat(Exception):
    pass


"""
The Record class manages the data loading and organization of locations, creatures, and items within the Pymon game. 
It provides methods to load data from files, including creating locations with specific descriptions, connecting 
locations in given directions, and adding creatures and items to random locations in the game. The class supports 
error handling for file operations and ensures data is loaded and linked properly, establishing connections between 
locations and placing creatures and items at random. This structure allows the Pymon game world to be dynamically 
configured from external files.
"""
class Record:
    def __init__(self):
        self.locations = {}
        self.creatures = []
        self.connections = {}
        self.items = {}

    def load_data(self, filename):
        if not os.path.isfile(filename):
            filename = input(f"File '{filename}' not found. Please provide the full path to the file: ").strip().strip('"')
        
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines[1:]:  
                    parts = line.strip().split(',')
                    if len(parts) < 6:
                        continue  
                    location_name = parts[0].strip()
                    description = parts[1].strip()
                    west = parts[2].strip()
                    north = parts[3].strip()
                    east = parts[4].strip()
                    south = parts[5].strip()
                    location = Location(location_name, description)
                    self.locations[location_name] = location
                    self.connections[location_name] = {
                        'west': west,
                        'north': north,
                        'east': east,
                        'south': south
                    }
            self.connect_locations()

            print(f"Data loaded successfully from {filename}")

        except FileNotFoundError:
            print(f"File '{filename}' could not be found or opened.")
        except Exception as e:
            print(f"Error loading data from {filename}: {e}")

    def load_creatures(self, filename):
        if not os.path.isfile(filename):
            filename = input(f"File '{filename}' not found. Please provide the full path to the file: ").strip().strip('"')

        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                
                # Skipping the header line
                for line in lines[1:]:  
                    parts = line.strip().split(',')
                    if len(parts) != 3:
                        continue 
                    nickname = parts[0].strip()
                    description = parts[1].strip()
                    adoptable_value = parts[2].strip().lower()
                    if adoptable_value == 'yes':
                        creature = Pymon(nickname, description, None, energy=3)
                        creature_type = "Pymon"
                    elif adoptable_value == 'no':
                        creature = Creature(nickname, description, None)
                        creature_type = "Creature"
                    else:
                        print(f"Warning: Unrecognized adoptable value '{adoptable_value}' for creature '{nickname}'")
                        continue  
                    self.creatures.append(creature)
                    random_location = random.choice(list(self.locations.values()))
                    random_location.add_creature(creature)
                    
            print(f"Creatures loaded successfully from {filename}")

        except FileNotFoundError:
            print(f"File '{filename}' could not be found or opened.")
        except Exception as e:
            print(f"Error loading creatures from {filename}: {e}")
    
    def load_items(self, filename):
        if not os.path.isfile(filename):
            filename = input(f"File '{filename}' not found, Please enter the full path to the file: ").strip().strip('"')
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
                for line in lines[1:]:
                    parts = line.strip().split(',')
                    if len(parts) != 4:
                        print("Wrong format in items file")
                        continue
                    name = parts[0].strip()
                    description = parts[1].strip()
                    pickable = parts[2].strip().lower() == 'yes'
                    consumable = parts[3].strip().lower() == 'yes'
                    item = Item(name, description, pickable, consumable)
                    self.items[name] = item
                    
                    # Randomly place the item in any available location
                    random_location = random.choice(list(self.locations.values()))
                    random_location.add_item(item)
                    
            print(f"Items loaded successfully from {filename}")
        except FileNotFoundError:
            print(f"File '{filename}' could not be found or opened.")
        except Exception as e:
            print(f"Error loading items from {filename}: {e}")

    def connect_locations(self):
        for location_name, directions in self.connections.items():
            location = self.locations[location_name]
            for direction, connected_location_name in directions.items():
                if connected_location_name != "None" and connected_location_name in self.locations:
                    connected_location = self.locations[connected_location_name]
                    location.connect(direction, connected_location)


"""
The Operation class manages player interactions, game mechanics, and data handling within the Pymon game. 
This class facilitates various levels (Credit, DI, and HD), each offering different gameplay options such as 
Pymon inspection, location navigation, inventory management, and creature challenges. Key methods include 
loading and saving game progress, handling Pymon energy and movement, capturing and releasing Pymons, and 
conducting battles. The class also supports additional HD-level functionalities like custom location/creature 
addition, randomized connections, and battle statistics generation, enriching the gameplay experience.
"""
class Operation:
    def __init__(self, pymon, record):
        self.pymon = pymon
        self.benched_pymons = []
        self.record = record
        self.successful_moves = 0
        self.battle_stats = []
        self.all_pymons_lost = False
        self.hd_record = HDRecord()

    def generate_stats(self):
        if not self.battle_stats:
            print("No battles have been recorded.")
            return
        total_wins, total_draws, total_losses = 0, 0, 0
        for i, stat in enumerate(self.battle_stats, start=1):
            print(f"Battle {i}, {stat['timestamp']} Opponent: {stat['opponent']}, W: {stat['wins']}, D: {stat['draws']}, L: {stat['losses']}")
            total_wins += stat['wins']
            total_draws += stat['draws']
            total_losses += stat['losses']
        
        print(f"Total: W: {total_wins} D: {total_draws} L: {total_losses}")

    def display_menu(self):
        print("\nPlease issue a command to your Pymon:")
        print("1) Inspect Pymon")
        print("2) Inspect current location")
        print("3) Move")
        print("4) Exit the program")

    def inspect_pymon(self):
        print(f"\nHi Player, my name is {self.pymon.get_nickname()}.")
        print(f"Description: {self.pymon.get_description()}")
        print(f"My energy level is {self.pymon.get_energy()}/3.")
        print("What can I do to help you?")
    
    def list_benched_pymons(self):
        if not self.benched_pymons:
            print("No benched Pymons available.")
            return

        print("\nBenched Pymons:")
        for index, pymon in enumerate(self.benched_pymons, start=1):
            print(f"{index}) {pymon.get_nickname()} - {pymon.get_description()}")

        try:
            selection = int(input("Select a Pymon by number to make it your current Pymon: ")) - 1
            if 0 <= selection < len(self.benched_pymons):
                selected_pymon = self.benched_pymons.pop(selection)
                selected_pymon.inventory.extend(self.pymon.inventory)
                self.pymon.inventory.clear()

                if self.pymon.location:
                    self.pymon.last_location = self.pymon.location

                self.benched_pymons.append(self.pymon)

                if selected_pymon.last_location:
                    selected_pymon.location = selected_pymon.last_location
                else:
                    print(f"{selected_pymon.get_nickname()} has no last known location.")

                self.pymon = selected_pymon
                print(f"You have switched to {self.pymon.get_nickname()}.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    def inspect_location(self):
        location = self.pymon.location
        if location:
            print(f"\nYou are at {location.get_name()}, {location.get_description()}.")
            if location.creatures:
                print("Creatures here:")
                for creature in location.creatures:
                    if creature == self.pymon:
                        print(f"  - {creature.get_nickname()} - {creature.get_description()} (you)")
                    else:
                        print(f"  - {creature.get_nickname()} - {creature.get_description()}")
            if location.items:
                print("Items here:")
                for item in location.items:
                    print(f"  - {item}")
        else:
            print("Pymon is not located in any specific place.")

    def move(self):
        direction = input("\nMoving to which direction? (north/east/south/west): ").strip().lower()
        try:
            if direction in ["north", "east", "south", "west"]:
                move_successful = self.pymon.move(direction)
                if move_successful:
                    self.successful_moves += 1  
                    print(f"You traveled {direction} and arrived at {self.pymon.location.get_name()}.")

                    if self.successful_moves % 2 == 0:
                        self.pymon.set_energy(self.pymon.get_energy() - 1)
                        print(f"{self.pymon.get_nickname()} lost 1 energy point due to movement.")

                        if self.pymon.get_energy() <= 0:
                            print(f"{self.pymon.get_nickname()}'s energy is depleted.")
                            self.relinquish_pymon()
            else:
                raise InvalidDirectionException("Invalid direction. Please choose north, east, south, or west.")
        except InvalidDirectionException as e:
            print(e)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Choose an option (1-4): ").strip()

            if choice == "1":
                self.inspect_pymon()
            elif choice == "2":
                self.inspect_location()
            elif choice == "3":
                self.move()
            elif choice == "4":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")

    def display_credit_menu(self):
        print("\nPlease issue a command to your Pymon:")
        print("1) Inspect Pymon")
        if self.benched_pymons:
            print("1.1) List and select a benched Pymon to use")
        print("2) Inspect current location")
        print("3) Move")
        print("4) Pick an item")
        print("5) View inventory")
        print("6) challenge a creature")
        print("7) exit the program")

    def pick_item(self):
        location = self.pymon.get_location()
        if location is None:
            print("Pymon is not currently at any location.")
            return

        if not location.get_items():
            print("No items to pick up here.")
            return

        print("Items available to pick:")
        for i, item in enumerate(location.get_items()):
            print(f"{i + 1}) {item.get_name()} - {item.get_description()}")

        try:
            choice = int(input("Pick which item (enter the number): ")) - 1
            if 0 <= choice < len(location.get_items()):
                item = location.get_items()[choice]
                if item.is_pickable():
                    location.items.remove(item)
                    self.pymon.add_to_inventory(item)
                else:
                    print(f"You can't pick up the {item.get_name()}.")
            else:
                print("Invalid item number selected.")
        except ValueError:
            print("Invalid input. Please enter the number corresponding to the item.")

    def view_inventory(self):
        if not self.pymon.inventory:
            print("Your inventory is empty.")
        else:
            print("Your inventory contains:")
            for item in self.pymon.inventory:
                print(f"- {item.get_name()}: {item.get_description()}")

    def challenge_creature(self):
        location = self.pymon.get_location()
        opponent = next((c for c in location.get_creatures() if isinstance(c, Pymon) and c != self.pymon), None)

        if opponent:
            self.pymon.challenge(opponent)
            self.battle(opponent)
        else:
            print("No Pymon here to challenge.")

    def battle(self, opponent):
        pymon_energy = self.pymon.get_energy()
        opponent_energy = 3
        wins, losses, draws = 0, 0, 0

        while wins < 2 and losses < 2 and pymon_energy > 0:
            while True:
                player_choice = input("Your turn (r)ock, (p)aper, or (s)cissor: ").strip().lower()
                if player_choice in ["r", "p", "s"]:
                    break
                else:
                    print("Invalid input. Please enter 'r', 'p', or 's'.")

            opponent_choice = random.choice(["r", "p", "s"])
            print(f"Opponent chose: {opponent_choice}")

            if player_choice == opponent_choice:
                print("Draw! Repeat encounter.")
            elif (player_choice, opponent_choice) in [("r", "s"), ("s", "p"), ("p", "r")]:
                print("You won this round!")
                wins += 1
                opponent_energy -= 1
            else:
                print("You lost this round!")
                losses += 1
                if not self.pymon.has_immunity:
                    pymon_energy -= 1
                    self.pymon.set_energy(pymon_energy)
                else:
                    print("But you are immune!")
                    self.pymon.has_immunity = False

        if wins >= 2:
            print(f"Congrats! You won the battle against {opponent.get_nickname()} and captured them!")
            self.capture_pymon(opponent)
        else:
            print("You lost the battle and your Pymon has been defeated.")
            self.relinquish_pymon()
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %I:%M%p")
        self.battle_stats.append({
            "timestamp": timestamp,
            "opponent": opponent.get_nickname(),
            "wins": wins,
            "draws": draws,
            "losses": losses
        })

    def relinquish_pymon(self):
        print(f"You have lost your Pymon: {self.pymon.get_nickname()}. It will be released into the wild.")

        random_location = random.choice(list(self.record.locations.values()))
        self.pymon.location = random_location
        random_location.add_creature(self.pymon)

        if self.benched_pymons:
            new_pymon = self.benched_pymons.pop(0)
            new_pymon.inventory.extend(self.pymon.inventory)
            self.pymon.inventory.clear()
            self.pymon = new_pymon
            print(f"You have switched to {self.pymon.get_nickname()} and transferred the inventory.")
        else:
            print("No more Pymons left. Game over.")
            print("\n Returning back to level options.")
            self.all_pymons_lost = True

    def run_credit(self):
        while True:
            self.display_credit_menu()
            choice = input("Choose an option (1-7, or 1.1 if available): ").strip()

            if choice == "1":
                self.inspect_pymon()
            elif choice == "1.1" and self.benched_pymons:
                self.list_benched_pymons()
            elif choice == "2":
                self.inspect_location()
            elif choice == "3":
                self.move()
            elif choice == "4":
                self.pick_item()
            elif choice == "5":
                self.view_inventory()
            elif choice == "6":
                self.challenge_creature()
            elif choice == "7":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 7.")

    def capture_pymon(self, new_pymon):
        print(f"You captured a new Pymon: {new_pymon.get_nickname()}!")
        new_pymon.last_location = self.pymon.location
        self.benched_pymons.append(new_pymon)
        if new_pymon in self.pymon.location.creatures:
            self.pymon.location.creatures.remove(new_pymon)

    def display_di_menu(self):
        print("\nPlease issue a command to your Pymon:")
        print("1) Inspect Pymon")
        if self.benched_pymons:
            print("1.1) List and select a benched Pymon to use")
        print("2) Inspect current location")
        print("3) Move")
        print("4) Pick an item")
        print("5) View inventory")
        print("5.1) Select item to use")
        print("6) Challenge a creature")
        print("7) Exit the program")

    def run_DI(self):
        move_counter = 0
        while True:
            self.display_di_menu()
            choice = input("Choose an option (1-7, or 1.1 / 5.1 if available): ").strip()

            if choice == "1":
                self.inspect_pymon()
            elif choice == "1.1" and self.benched_pymons:
                self.list_benched_pymons()
            elif choice == "2":
                self.inspect_location()
            elif choice == "3":
                self.move()
                move_counter += 1
                if move_counter >= 2:
                    self.pymon.set_energy(self.pymon.get_energy() - 1)
                    print(f"{self.pymon.get_nickname()} lost 1 energy point due to movement.")
                    move_counter = 0
                    if self.pymon.get_energy() <= 0:
                        self.relinquish_pymon()
            elif choice == "4":
                self.pick_item()
            elif choice == "5":
                self.view_inventory()
            elif choice == "5.1":
                item_name = input("Enter the name of the item to use: ").strip()
                self.pymon.use_item(item_name)
            elif choice == "6":
                self.challenge_creature()
            elif choice == "7":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 7.")

    def display_hd_menu(self):
        print("\nPlease issue a command to your Pymon:")
        print("1) Inspect Pymon")
        if self.benched_pymons:
            print("1.1) List and select a benched Pymon to use")
        print("2) Inspect current location")
        print("3) Move")
        print("4) Pick an item")
        print("5) View inventory")
        print("5.1) Select item to use")
        print("6) Challenge a creature")
        print("7) Generate stats")
        print("8) Add a custom location")
        print("9) Add custom creature")
        print("10) Randomise location")
        print("11) Save game progress")
        print("12) Load game progress")
        print("13) Exit the program")

    def run_HD(self):
        move_counter = 0
        while True:
            self.display_hd_menu()
            choice = input("Choose an option (1-11, or 1.1 / 5.1 if available): ").strip()

            if choice == "1":
                self.inspect_pymon()
            elif choice == "1.1" and self.benched_pymons:
                self.list_benched_pymons()
            elif choice == "2":
                self.inspect_location()
            elif choice == "3":
                self.move()
                move_counter += 1
                if move_counter >= 2:
                    self.pymon.set_energy(self.pymon.get_energy() - 1)
                    print(f"{self.pymon.get_nickname()} lost 1 energy point due to movement.")
                    move_counter = 0
                    if self.pymon.get_energy() <= 0:
                        self.relinquish_pymon()
            elif choice == "4":
                self.pick_item()
            elif choice == "5":
                self.view_inventory()
            elif choice == "5.1":
                item_name = input("Enter the name of the item to use: ").strip()
                self.pymon.use_item(item_name)
            elif choice == "6":
                self.challenge_creature()
            elif choice == "7":
                self.generate_stats()
            elif choice == "8":
                self.hd_record.add_custom_location()
            elif choice == "9":
                self.hd_record.add_custom_creature()
            elif choice == "10":
                self.randomize_connections()
            elif choice == "11":
                self.save_game()
            elif choice == "12":
                self.load_game()
            elif choice == "13":
                print("Exiting the program. Goodbye!")
                return
            else:
                print("Invalid choice. Please enter a valid option.")

            if self.all_pymons_lost:
                print("You lost all Pymons. Restarting HD Level...\n")
                break

    def randomize_connections(self):
        all_locations = list(self.record.locations.values())
        directions = ["north", "south", "east", "west"]

        for location in all_locations:
            location.doors = {dir: None for dir in directions}

        for location in all_locations:
            for direction in directions:
                if random.choice([True, False]):
                    other_location = random.choice(all_locations)
                    
                    while other_location == location:
                        other_location = random.choice(all_locations)

                    location.connect(direction, other_location)

        print("Connections have been randomized successfully.")

    def save_game(self, filename=None):
        filename = filename or input("Enter save filename (or press Enter to use 'save2024.csv'): ").strip() or "save2024.csv"
        try:
            with open(filename, 'w') as file:
                file.write(f"Pymon,{self.pymon.get_nickname()},{self.pymon.get_location().get_name()},{self.pymon.get_energy()}\n")
                
                for item in self.pymon.inventory:
                    file.write(f"Inventory,{item.get_name()},{item.get_description()},{item.is_pickable()},{item.is_consumable()}\n")
                
                for location_name, location in self.record.locations.items():
                    file.write(f"Location,{location_name},{location.get_description()}\n")
                    
                    for creature in location.get_creatures():
                        file.write(f"Creature,{creature.get_nickname()},{creature.get_description()},{location_name}\n")
                    
                    for item in location.get_items():
                        file.write(f"Item,{item.get_name()},{item.get_description()},{item.is_pickable()},{item.is_consumable()},{location_name}\n")
            
            print(f"Game progress saved successfully to {filename}")
        except Exception as e:
            print(f"An error occurred while saving the game: {e}")

    def load_game(self, filename=None):
        filename = filename or input("Enter load filename (or press Enter to use 'save2024.csv'): ").strip() or "save2024.csv"
        
        try:
            self.pymon.inventory.clear()
            self.record.locations.clear()
            
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if not parts:
                        continue
                    
                    record_type = parts[0]
                    
                    try:
                        if record_type == "Pymon":
                            pymon_name = parts[1]
                            location_name = parts[2]
                            energy = int(parts[3])
                            self.pymon = Pymon(nickname=pymon_name, description="Restored Pymon", location=self.record.locations[location_name], energy=energy)
                            self.record.locations[location_name].add_creature(self.pymon)
                        
                        elif record_type == "Inventory":
                            item_name, description = parts[1], parts[2]
                            pickable = parts[3].lower() == 'true'
                            consumable = parts[4].lower() == 'true'
                            item = Item(item_name, description, pickable, consumable)
                            self.pymon.add_to_inventory(item)
                        
                        elif record_type == "Location":
                            location_name, description = parts[1], parts[2]
                            if location_name not in self.record.locations:
                                location = Location(name=location_name, description=description)
                                self.record.locations[location_name] = location
                            else:
                                self.record.locations[location_name].set_description(description)
                        
                        elif record_type == "Creature":
                            creature_name, description, location_name = parts[1], parts[2], parts[3]
                            creature = Creature(creature_name, description, self.record.locations[location_name])
                            self.record.locations[location_name].add_creature(creature)
                        
                        elif record_type == "Item":
                            item_name, description = parts[1], parts[2]
                            pickable = parts[3].lower() == 'true'
                            consumable = parts[4].lower() == 'true'
                            location_name = parts[5]
                            item = Item(item_name, description, pickable, consumable)
                            self.record.locations[location_name].add_item(item)
                    
                    except IndexError:
                        print(f"Warning: Malformed line in {filename}: {line.strip()} - skipping.")
                    except KeyError:
                        print(f"Warning: Location '{location_name}' not found for record '{line.strip()}' - skipping.")
            
            print(f"Game progress loaded successfully from {filename}")
        
        except FileNotFoundError:
            print(f"File '{filename}' not found. Cannot load game progress.")
        except Exception as e:
            print(f"An error occurred while loading the game: {e}")


"""
The GameController_pass class initializes and manages the gameplay for the Pass level of the Pymon game. 
It sets up the game environment by loading location and creature data, and ensures that a Pymon character 
is assigned a starting location. This class provides the main interface for starting the game, where the 
player can explore the world and interact with their Pymon. The start_game method serves as the entry 
point for gameplay, displaying a welcome message and initiating the main game loop.
"""
class GameController_pass:
    def __init__(self):
        self.record = Record()
        
        self.record.load_data("locations.csv")
        self.record.load_creatures("creatures.csv")

        start_location = self.record.locations.get("Playground")
        if start_location is None and self.record.locations:
            start_location = random.choice(list(self.record.locations.values()))
            print("Warning: 'Playground' not found. Starting at a random location.")

        if start_location:
            self.pymon = Pymon(nickname="Kimimon", description="I am white and yellow with a square face.", location=start_location)
            start_location.add_creature(self.pymon)
        else:
            print("No locations loaded. Exiting the game.")
            return

        self.operation = Operation(self.pymon, self.record)

    def start_game(self):
        print("\n")
        print("\n Welcome to Pymon World \n")
        print("It is just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.\n")
        print(f"You just started at {self.pymon.location.get_name()}")
        self.operation.run()
        print("Returning to the main menu.\n")


"""
The Item class represents items that can be found and interacted with in the Pymon game. 
Each item has properties such as name, description, and flags indicating if it is pickable or consumable. 
The class provides methods for checking if an item is pickable or consumable and to retrieve 
its name and description. The use method handles the item's specific functionality, such as 
restoring energy with an apple, granting immunity with a potion, or providing a directional view 
with binoculars. The __str__ method provides a string representation of the item for easy display.
"""
class Item:
    def __init__(self, name, description, pickable, consumable):
        self.name = name
        self.description = description
        self.pickable = pickable
        self.consumable = consumable

    def is_pickable(self):
        return self.pickable

    def is_consumable(self):
        return self.consumable

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description
    
    def use(self, pymon):
        if self.name.lower() == "apple" and self.is_consumable():
            if pymon.get_energy() < 3:
                pymon.set_energy(pymon.get_energy() + 1)
                print(f"{pymon.get_nickname()} ate the apple and regained some energy!")
            else:
                print(f"{pymon.get_nickname()}'s energy is already at maximum.")
            return True

        elif self.name.lower() == "potion" and self.is_consumable():
            pymon.give_immunity()
            print(f"{pymon.get_nickname()} used the magic potion and is immune for one battle!")
            return True

        elif self.name.lower() == "binocular":
            self.use_binocular(pymon)
            return False

        if not self.is_pickable() and not self.is_consumable():
            print(f"It's just a {self.get_name()}. You can't pick it up or use it.")
            return False

        else:
            print(f"{self.name} cannot be used.")
            return False

    def use_binocular(self, pymon):
        current_location = pymon.get_location()
        if not current_location:
            print("Pymon is not at any specific location to use binoculars.")
            return

        direction = input("Choose view direction (current, north, south, east, west): ").strip().lower()
        
        if direction == "current":
            print(f"Current location: {current_location.get_name()} - {current_location.get_description()}")
            creatures = current_location.get_creatures()
            items = current_location.get_items()

            if creatures:
                for creature in creatures:
                    print(f"  - Creature: {creature.get_nickname()} - {creature.get_description()}")
            else:
                print("  - No creatures here.")

            if items:
                for item in items:
                    print(f"  - Item: {item.get_name()} - {item.get_description()}")
            else:
                print("  - No items here.")

        elif direction in current_location.get_doors():
            location = current_location.get_doors()[direction]
            if location:
                print(f"In the {direction}, you see {location.get_name()} with:")
                creatures = location.get_creatures()
                items = location.get_items()

                if creatures:
                    for creature in creatures:
                        print(f"  - Creature: {creature.get_nickname()} - {creature.get_description()}")
                else:
                    print("  - No creatures in this direction.")

                if items:
                    for item in items:
                        print(f"  - Item: {item.get_name()} - {item.get_description()}")
                else:
                    print("  - No items in this direction.")
            else:
                print(f"This direction ({direction}) leads nowhere.")
        else:
            print("Invalid direction. Please choose from 'current', 'north', 'south', 'east', or 'west'.")

    def __str__(self):
        return f"{self.name} - {self.description}"


"""
The HDRecord class extends the Record class to manage high-definition (HD) level data for locations and creatures 
in the Pymon game. It initializes with default file paths for locations, creatures, and items, and loads data 
from these files. The class includes methods to add custom locations and creatures dynamically. The add_custom_location 
method allows the player to specify a new location with descriptive details and directional connections. 
The add_custom_creature method provides the ability to add new creatures, distinguishing between adoptable 
(Pymon) and non-adoptable (Animal) types, with details saved to their respective files.
"""
class HDRecord(Record):
    def __init__(self, locations_file='locations.csv', creatures_file='creatures.csv', items_file='items.csv'):
        super().__init__()
        
        self.current_locations_file = locations_file.strip('"')
        self.current_creatures_file = creatures_file.strip('"')
        
        self.load_data(self.current_locations_file)
        self.load_creatures(self.current_creatures_file)

    def add_custom_location(self):
        location_name = input("Enter location name: ").strip()
        
        if location_name.lower() in (loc.lower() for loc in self.locations):
            print(f"Location '{location_name}' already exists. No changes made.")
            return

        description = input("Enter location description: ").strip()
        
        directions = {}
        for direction in ['west', 'north', 'east', 'south']:
            while True:
                neighbor = input(f"Enter the location to the {direction} (or 'None'): ").strip()
                neighbor = neighbor.title() if neighbor.lower() != 'none' else 'None'
                if neighbor.lower() == 'none' or neighbor in self.locations:
                    directions[direction] = neighbor
                    break
                else:
                    print(f"Warning: '{neighbor}' is not a valid location. Please enter an existing location name or 'None'.")

        new_location = Location(location_name, description)
        self.locations[location_name] = new_location
        for direction, neighbor in directions.items():
            if neighbor.lower() != 'none':
                new_location.connect(direction, self.locations[neighbor])

        with open(self.current_locations_file, 'a') as file:
            file.write(f"{location_name},{description},{directions['west']},{directions['north']},{directions['east']},{directions['south']}\n")

        print(f"Location '{location_name}' added and saved to {self.current_locations_file} successfully.")

    def add_custom_creature(self):
        creature_name = input("Enter creature name: ").strip()
        
        if creature_name.lower() in (creature.nickname.lower() for creature in self.creatures):
            print(f"Creature '{creature_name}' already exists. No changes made.")
            return

        description = input("Enter creature description: ").strip()
        
        while True:
            adoptable = input("Is the creature adoptable? (yes/no): ").strip().lower()
            if adoptable in {'yes', 'no'}:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if adoptable == 'yes':
            new_creature = Pymon(creature_name, description, None, energy=3)
            creature_type = "Pymon"
        else:
            new_creature = Creature(creature_name, description, None)
            creature_type = "Animal"

        self.creatures.append(new_creature)

        with open(self.current_creatures_file, 'a') as file:
            file.write(f"{creature_name},{description},{adoptable}\n")

        print(f"{creature_type} '{creature_name}' added and saved to {self.current_creatures_file} successfully.")


"""
The GameController_credit class manages the Credit level gameplay for the Pymon game. It initializes 
the game environment by loading data for locations, creatures, and items, and assigns a starting location 
for the player's Pymon. This class provides a looped gameplay interface where the player can explore 
and interact with their Pymon at an advanced level. The start_game method initializes the main gameplay 
loop, allowing the player to restart the level if all Pymons are lost, while handling potential errors 
and unexpected conditions gracefully.
"""
class GameController_credit:
    def __init__(self):
        self.record = Record()
        self.record.load_data("locations.csv")
        self.record.load_creatures("creatures.csv")
        self.record.load_items("items.csv")
        start_location = random.choice(list(self.record.locations.values()))
        self.pymon = Pymon(nickname="Kimimon", description="I am white and yellow with a square face.", location=start_location)
        start_location.add_creature(self.pymon)
        self.operation = Operation(self.pymon, self.record)
        
    def start_game(self):
        while True:
            print("Welcome to Pymon World - Credit Level")
            print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.")
            print(f"You just started at {self.pymon.location.get_name()}")

            self.operation.all_pymons_lost = False

            try:
                self.operation.run_credit()
                print("Returning to main menu.\n")
                break
            except:
                if self.operation.all_pymons_lost:
                    print("You lost all Pymons. Restarting Credit Level...\n")
                    continue
                else:
                    raise


"""
The GameController_DI class manages the DI level gameplay for the Pymon game. It sets up the game 
environment by loading locations, creatures, and items from specified files, and assigns a starting 
location for the player's Pymon. This class provides a looped gameplay interface for the DI level, 
where the player can explore, interact with creatures, and capture new Pymons at an advanced level. 
The start_game method initializes the main gameplay loop, allowing the player to restart if all Pymons 
are lost, and handles exceptions to ensure smooth gameplay.
"""
class GameController_DI:
    def __init__(self):
        self.record = Record()
        self.record.load_data("locations.csv")
        self.record.load_creatures("creatures.csv")
        self.record.load_items("items.csv")
        
        start_location = random.choice(list(self.record.locations.values()))
        self.pymon = Pymon(nickname="Kimimon", description="I am white and yellow with a square face.", location=start_location)
        start_location.add_creature(self.pymon)
        
        self.operation = Operation(self.pymon, self.record)

    def start_game(self):
        while True:
            print("Welcome to Pymon World - HD Level")
            print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.")
            print(f"You just started at {self.pymon.location.get_name()}")

            self.operation.all_pymons_lost = False

            try:
                self.operation.run_DI()
                print("Returning to main menu.\n")
                break
            except:
                if self.operation.all_pymons_lost:
                    print("You lost all Pymons. Restarting HD Level...\n")
                    continue
                else:
                    raise


"""
The GameController_HD class manages the HD level gameplay for the Pymon game, providing advanced features 
for a high-definition experience. It initializes the game environment by loading data for locations, 
creatures, and items, and assigns a starting location for the player's Pymon. This class retrieves file 
paths from command-line arguments or prompts the user if not provided, making it flexible in handling 
various game setups. The start_game method initiates the main gameplay loop, restarting if all Pymons 
are lost, and allows for additional features like adding custom creatures or locations through the 
HDRecord instance. The class delegates advanced gameplay options to the run_HD method of the Operation class.
"""
class GameController_HD:
    def __init__(self):
        locations_file, creatures_file, items_file = self.get_file_arguments()

        self.record = HDRecord(locations_file, creatures_file, items_file)

        start_location = random.choice(list(self.record.locations.values()))
        self.pymon = Pymon(nickname="Kimimon", description="I am white and yellow with a square face.", location=start_location)
        start_location.add_creature(self.pymon)
        self.operation = Operation(self.pymon, self.record)

    def get_file_arguments(self):
        args = sys.argv[1:]
        if len(args) >= 3:
            return args[0], args[1], args[2]
        elif len(args) == 2:
            items_file = input("Enter items file (or press Enter to use 'items.csv'): ").strip() or "items.csv"
            return args[0], args[1], items_file
        elif len(args) == 1:
            creatures_file = input("Enter creatures file (or press Enter to use 'creatures.csv'): ").strip() or "creatures.csv"
            items_file = input("Enter items file (or press Enter to use 'items.csv'): ").strip() or "items.csv"
            return args[0], creatures_file, items_file
        else:
            locations_file = input("Enter locations file (or press Enter to use 'locations.csv'): ").strip() or "locations.csv"
            creatures_file = input("Enter creatures file (or press Enter to use 'creatures.csv'): ").strip() or "creatures.csv"
            items_file = input("Enter items file (or press Enter to use 'items.csv'): ").strip() or "items.csv"
            return locations_file, creatures_file, items_file

    def start_game(self):
        while True:
            print("Welcome to Pymon World - HD Level")
            print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.")
            print(f"You just started at {self.pymon.location.get_name()}")

            self.operation.all_pymons_lost = False

            self.operation.run_HD()

            if self.operation.all_pymons_lost:
                print("You lost all Pymons. Restarting HD Level...\n")
            else:
                print("Exiting the HD Level.")
                break

    def add_custom_creature(self):
        self.record.add_custom_creature()

    def add_custom_location(self):
        self.record.add_custom_location()


"""
The main entry point for the Pymon game. This looped menu system allows the player to choose 
between different levels of gameplay: Pass, Credit, DI, and HD levels. Each level provides 
different features and gameplay complexity. Based on the player's selection, the corresponding 
GameController class is instantiated, and the game begins at the chosen level. The player can 
exit the program by selecting option 5. Invalid inputs prompt the user to enter a valid choice.
"""
if __name__ == "__main__":
    while True:
        print("Welcome to Pymon World")
        print("Select the level you want to play:")
        print("1) Pass Level")
        print("2) Credit Level")
        print("3) DI Level")
        print("4) HD Level")
        print("5) Exit")
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            game = GameController_pass()
            game.start_game()
             
        elif choice == "2":
            game = GameController_credit()  
            game.start_game()
            
        elif choice == "3":
            game = GameController_DI()
            game.start_game()
            
        elif choice == "4":
            game = GameController_HD()
            game.start_game()
            
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

