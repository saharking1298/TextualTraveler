from googleplaces import GooglePlaces, Place
from utils import menu, LocationOperations, GPTOperations, NPCOperations, RESOURCES
from pyquest import Engine, Room, Interactive, NPC
import openai
import json


class App:
    def __init__(self, key):
        self.api = GooglePlaces(key)
        self.engine = None

    def ask_starting_location(self) -> Place:
        """
        This function let the user choose a place to start exploring.
        """
        flag = True
        location = None
        while flag:
            # Getting a location name a list of search results
            location = input("Enter a starting location: ").strip()
            response = self.api.text_search(location)
            options = []
            for result in response.places:
                options.append(result.name)
            options.append("None of the above")

            # Letting the user choose a location and confirm
            while True:
                choice = menu("Choose a location:", options, index=True)
                if choice == len(options) - 1:
                    # Letting the user search for a location once again
                    break
                else:
                    # Getting location details and asking user to confirm
                    location = response.places[choice]
                    location.get_details()
                    print(LocationOperations.details(location))
                    answer = input("Is this your location (y/n)? ").strip().lower()
                    if answer.startswith("y"):
                        flag = False
                        break
                    else:
                        print()
                        if len(response.places) == 1:
                            break
        return location

    def generate_room(self, location: Place) -> Room:
        gpt_prompt = LocationOperations.gpt_prompt(location)
        response = GPTOperations.completion(gpt_prompt)
        room = None
        try:
            data = json.loads(response)
            required_keys = ["description", "type", "npcs"]
            for key in required_keys:
                if key not in data:
                    raise KeyError
            room = Room(data["description"].strip("\n"), show_locations=True)
            room.metadata = {
                "name": location.name,
                "type": data["type"],
                "address": location.formatted_address
            }
            if 'editorial_summary' in location.details:
                room.metadata["description"] = location.details['editorial_summary']['overview']
            for i in range(len(data["npcs"])):
                room.npcs.add(NPCOperations.generate(data["npcs"][i]))
        except json.decoder.JSONDecodeError:
            print("Can't parse JSON from GPT-3 response!")
        except KeyError:
            print("JSON response from GPT-3 is invalid!")
        if room is None:
            print(response)
        return room

    def npc_handler(self, npc: NPC, question: str) -> str:
        prompt = NPCOperations.gpt_prompt(npc, question, self.engine.currentRoom)
        return GPTOperations.completion(prompt)

    def start(self):
        starting_place = self.ask_starting_location()
        print("Setting up your adventure...\n")
        room = self.generate_room(starting_place)
        self.engine = Engine(npc_handler=self.npc_handler)
        self.engine.start(room)


def main():
    # Setting OpenAI API key
    auth = json.load(open(RESOURCES + '/auth.json', "r"))
    openai.api_key = auth["OpenAI"]
    # Starting the app
    app = App(auth["GooglePlaces"])
    app.start()


if __name__ == '__main__':
    main()
