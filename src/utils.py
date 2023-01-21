from googleplaces import Place
from pyquest import NPC, Room
import openai
import random
import os

RESOURCES = os.path.join(os.path.dirname(__file__), "resources")

database = {
    "maleFirstNames": open(RESOURCES + "/lists/modern/male-first-names.txt", "r").read().split("\n"),
    "femaleFirstNames": open(RESOURCES + "/lists/modern/female-first-names.txt", "r").read().split("\n"),
    "lastNames": open(RESOURCES + "/lists/modern/last-names.txt", "r").read().split("\n"),
    "professions": open(RESOURCES + "/lists/modern/professions.txt", "r").read().split("\n"),
    "traits": open(RESOURCES + "/lists/traits.txt", "r").read().split("\n"),
}


class LocationOperations:
    @staticmethod
    def details(location: Place, prompt: bool = False) -> str:
        text = f"Name: {location.name}.\n" \
               f"Tags: {location.types}.\n"
        if not prompt:
            text += f"Address: {location.formatted_address}.\n"
        if 'editorial_summary' in location.details:
            text += f"Description: {location.details['editorial_summary']['overview']}"
        return text

    @staticmethod
    def gpt_prompt(location: Place) -> str:
        text = "Location data:\n" \
               f"Name: {location.name}.\n" \
               f"Address: {location.formatted_address}.\n" \
               f"Tags: {location.types}.\n"
        if 'editorial_summary' in location.details:
            text += f"Details: {location.details['editorial_summary']['overview']}\n"
        text += "Return a JSON response, representing a location in a text adventure: " \
                '{"description": "<generate a description of the location\'s appearance and contents>", ' \
                '"type": "<location type>", "npcs: ["NPC profession that fits the location"]}'
        return text


class NPCOperations:
    @staticmethod
    def generate(profession: str = None) -> NPC:
        gender = random.choice(("male", "female"))
        if gender == "male":
            first_name = random.choice(database["maleFirstNames"])
        else:
            first_name = random.choice(database["femaleFirstNames"])
        traits = random.choices(database["traits"], k=2)
        return NPC(first_name, gender, profession, traits)

    @staticmethod
    def gpt_prompt(npc: NPC, question: str, location: Room = None) -> str:
        metadata = location.metadata
        if location is None:
            text = f"Simulate a conversation with an NPC called {npc.name}.\n" \
                   f"fThis character is a {npc.gender}, works as a {npc.profession}, " \
                   f"and is known to be: {', '.join(npc.traits)}.\n" \
                   f"Player says: '{question}'. NPC says: "
        else:
            if "description" in metadata:
                description = metadata["description"]
            else:
                description = metadata["type"]
            text = f"Simulate a conversation with an NPC called {npc.name}.\n" \
                   f"This character is a {npc.gender}, works as a {npc.profession}, " \
                   f"in '{metadata['name']}', a {description} located at '{metadata['address']}'." \
                   f"The character is known to be: {', '.join(npc.traits)}.\n" \
                   f'Player says: "{question}". NPC says: '
        return text


class GPTOperations:
    @staticmethod
    def completion(prompt: str, max_tokens: int = 256) -> str:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].text


def menu(title, options, index=False):
    print(title)
    if type(options) == dict:
        choices = tuple(options.keys())
    elif type(options) in (list, tuple):
        choices = options
    else:
        choices = ()
    for i in range(len(choices)):
        print(f"{i+1}. {choices[i]}")
    choice = 0
    while True:
        try:
            choice = int(input())
        except ValueError:
            print("Please enter a number.")
            continue
        if 0 < choice <= len(choices):
            break
        else:
            print("Please choose a valid option.")
    if type(options) == dict:
        tuple(options.values())[choice - 1]()
    else:
        if index:
            return choice - 1
        else:
            return choices[choice - 1]
