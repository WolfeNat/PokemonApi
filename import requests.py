import requests

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

def menu():
    while True:
        print("\nMenu:")
        print("1. Enter a Pokémon name")
        print("2. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            pokemon_name = input("Enter the name of a 1st-gen Pokémon: ")
            get_evolution_chain(pokemon_name)
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select again.")

menu()