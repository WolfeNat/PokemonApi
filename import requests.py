import requests
import random

def list_first_gen_pokemon():
    response = requests.get('https://pokeapi.co/api/v2/generation/1/')
    
    if response.status_code == 200:
        data = response.json()
        pokemon_species = data['pokemon_species']

        for i, pokemon in enumerate(pokemon_species, 1):
            print(f"{pokemon['name']:<15}", end=" ")
            if i % 4 == 0:  
                print()
        if len(pokemon_species) % 4 != 0:
            print()
    else:
        print("Failed to retrieve data from PokéAPI")

def get_evolution_chain(pokemon_name):
    species_url = f"https://pokeapi.co/api/v2/pokemon-species/{pokemon_name.lower()}/"
    response_species = requests.get(species_url)
    
    if response_species.status_code == 200:
        species_data = response_species.json()
        
        evolution_chain_url = species_data['evolution_chain']['url']
        response_evolution = requests.get(evolution_chain_url)
        
        if response_evolution.status_code == 200:
            evolution_data = response_evolution.json()
            chain = evolution_data['chain']
            
            evolutions = []
            current_evolution = chain
            while current_evolution:
                evolutions.append(current_evolution['species']['name'])
                if current_evolution['evolves_to']:
                    current_evolution = current_evolution['evolves_to'][0]
                else:
                    current_evolution = None
            
            print(f"Evolution chain for {pokemon_name}: {' -> '.join(evolutions)}")
        else:
            print("Failed to retrieve evolution chain.")
    else:
        print(f"Failed to retrieve species data for {pokemon_name}.")

def get_pokemon_stats(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}/"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        stats = {stat['stat']['name']: stat['base_stat'] for stat in data['stats']}
        
        pokemon_type = data['types'][0]['type']['name']
        stats['type'] = pokemon_type  
        
        moves = [move['move']['name'] for move in data['moves'][:4]]  
        return stats, moves
    else:
        print(f"Failed to retrieve stats for {pokemon_name}")
        return None, None
    
def get_move_details(move_name):
    move_url = f"https://pokeapi.co/api/v2/move/{move_name.lower()}/"
    response = requests.get(move_url)
    
    if response.status_code == 200:
        data = response.json()
        move_type = data['type']['name']
        move_power = data.get('power', 50)  
        accuracy = data.get('accuracy', 100)  
        return move_type, move_power, accuracy
    else:
        print(f"Failed to retrieve details for move {move_name}")
        return None, 50, 100

type_effectiveness = {
    'fire': {'grass': 2.0, 'water': 0.5, 'fire': 1.0},
    'water': {'fire': 2.0, 'grass': 0.5, 'water': 1.0},
    'grass': {'water': 2.0, 'fire': 0.5, 'grass': 1.0}
}

def calculate_effectiveness(move_type, defender_type):
    return type_effectiveness.get(move_type, {}).get(defender_type, 1.0)

def calculate_damage(attacker, defender, move_name):
    move_type, move_power, accuracy = get_move_details(move_name)
    
    if random.randint(1, 100) > accuracy:
        print(f"{move_name} missed!")
        return 0
    
    attacker_type = attacker['type'] 
    defender_type = defender['type']  

    effectiveness = calculate_effectiveness(move_type, defender_type)
    base_damage = (move_power * (attacker['attack'] / defender['defense'])) * random.uniform(0.85, 1.0)
    
    return base_damage * effectiveness


def battle(pokemon1_name, pokemon2_name):
    pokemon1_stats, pokemon1_moves = get_pokemon_stats(pokemon1_name)
    pokemon2_stats, pokemon2_moves = get_pokemon_stats(pokemon2_name)
    
    if not pokemon1_stats or not pokemon2_stats:
        return

    print(f"Battle between {pokemon1_name} and {pokemon2_name}!")
    
    pokemon1_hp = pokemon1_stats['hp']
    pokemon2_hp = pokemon2_stats['hp']

    while pokemon1_hp > 0 and pokemon2_hp > 0:
        move = random.choice(pokemon1_moves)
        damage = calculate_damage(pokemon1_stats, pokemon2_stats, move)
        pokemon2_hp -= damage
        print(f"{pokemon1_name} used {move}, dealt {damage:.2f} damage!")
        if pokemon2_hp <= 0:
            print(f"{pokemon2_name} fainted! {pokemon1_name} wins!")
            break

        move = random.choice(pokemon2_moves)
        damage = calculate_damage(pokemon2_stats, pokemon1_stats, move)
        pokemon1_hp -= damage
        print(f"{pokemon2_name} used {move}, dealt {damage:.2f} damage!")
        if pokemon1_hp <= 0:
            print(f"{pokemon1_name} fainted! {pokemon2_name} wins!")
            break

def menu():
    while True:
        print("\nMenu:")
        print("1. List first-gen Pokémon")
        print("2. Enter a Pokémon name to get evolution chain")
        print("3. Start a battle between two first-gen Pokémon")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            list_first_gen_pokemon()
        elif choice == '2':
            pokemon_name = input("Enter the name of a 1st-gen Pokémon: ")
            get_evolution_chain(pokemon_name)
        elif choice == '3':
            pokemon1 = input("Enter the name of the first Pokémon: ")
            pokemon2 = input("Enter the name of the second Pokémon: ")
            battle(pokemon1, pokemon2)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select again.")

menu()
