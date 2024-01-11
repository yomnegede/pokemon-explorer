import streamlit as st
import requests
import random


POKEAPI_BASE_URL = "https://pokeapi.co/api/v2/"

def search_pokemon():
    st.header("Search for a Pokémon")
    pokemon_name = st.text_input("Enter Pokémon Name or ID").lower() #NEW

    if st.button("Search"):     #NEW
        response = requests.get(f"{POKEAPI_BASE_URL}pokemon/{pokemon_name}")
        if response.status_code == 200:
            pokemon_data = response.json()
            st.write("Name:", pokemon_data['name'])
            st.write("Weight:", pokemon_data['weight'])
            st.image(pokemon_data['sprites']['front_default'], width=100)
            st.write("Height:", pokemon_data['height'])
            st.write("Base Experience:", pokemon_data['base_experience'])
            types = [t['type']['name'] for t in pokemon_data['types']]
            st.write("Types:", ', '.join(types))
        else:
            st.error("Pokémon not found. Please try a different name or ID.")

def random_pokemon():
    st.header("Discover a Random Pokémon")
    range_min, range_max = st.slider("Select ID Range for Random Pokémon", 1, 898, (1, 898))
    if st.button("Generate Random Pokémon"):
        random_id = random.randint(range_min, range_max)
        response = requests.get(f"{POKEAPI_BASE_URL}pokemon/{random_id}")
        if response.ok:
            pokemon_data = response.json()
            st.write("Name:", pokemon_data['name'])
            st.image(pokemon_data['sprites']['front_default'], width=100)
            st.write("Stats:")
            for stat in pokemon_data['stats']:
                st.write(f"{stat['stat']['name'].capitalize()}: {stat['base_stat']}")
        else:
            st.error("Failed to fetch random Pokémon. Please try again.")

def pokemon_ability_finder():
    st.header("Find Pokémon by Ability")
    ability_name = st.text_input("Enter Ability Name").lower()
    if st.button("Find Pokémon"):
        response = requests.get(f"{POKEAPI_BASE_URL}ability/{ability_name}")
        if response.ok:
            ability_data = response.json()
            pokemons = [pokemon['pokemon']['name'] for pokemon in ability_data['pokemon']]
            st.write(f"Pokémon with the ability '{ability_name}':")
            st.write(", ".join(pokemons))

def main():
    st.title("Pokémon Exploration App")
    st.sidebar.title("Features")
    app_mode = st.sidebar.radio("Choose Feature",
                                ["Search Pokémon", "Random Pokémon Generator", "Pokémon Ability Finder"])
    if app_mode == "Search Pokémon":
        search_pokemon()
    elif app_mode == "Random Pokémon Generator":
        random_pokemon()
    elif app_mode == "Pokémon Ability Finder":
        pokemon_ability_finder()

if __name__ == "__main__":
    main()
