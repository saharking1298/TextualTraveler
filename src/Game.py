import random


database = {
    "maleFirstNames": open("src/resources/lists/modern/male-first-names.txt", "r").read().split("\n"),
    "femaleFirstNames": open("src/resources/lists/modern/female-first-names.txt", "r").read().split("\n"),
    "lastNames": open("src/resources/lists/modern/last-names.txt", "r").read().split("\n"),
    "professions": open("src/resources/lists/modern/professions.txt", "r").read().split("\n"),
    "traits": open("src/resources/lists/traits.txt", "r").read().split("\n"),
}


class NPC:
    def __init__(self, name: str, gender: str, profession: str, traits: list):
        self.name = name
        self.gender = gender
        self.profession = profession
        self.traits = traits

    def dialog_prompt(self, question: str) -> str:
        return f"Simulate a conversation with an NPC called {self.name}.\n" \
               f"This character works as a {self.profession}, and is known to be: {', '.join(self.traits)}.\n" \
               f"Player says: '{question}'. NPC says: "

    def make_description(self):
        gender_words = {"male": "He", "female": "She"}
        return f"You are facing {self.name}, a {self.profession} at heart.\n" \
               f"{gender_words[self.gender]} is known to be: {', '.join(self.traits)}."

    def __str__(self):
        return f"NPC Name: {self.name}\n" \
               f"NPC job: {self.profession}\n" \
               f"NPC traits: {', '.join(self.traits)}"

    def __repr__(self):
        return self.__str__()


def generate_npc():
    gender = random.choice(("male", "female"))
    if gender == "male":
        first_name = random.choice(database["maleFirstNames"])
    else:
        first_name = random.choice(database["femaleFirstNames"])
    last_name = random.choice(database["lastNames"])
    profession = random.choice(database["professions"])
    traits = random.choices(database["traits"], k=2)
    return NPC(first_name + " " + last_name, gender, profession, traits)
