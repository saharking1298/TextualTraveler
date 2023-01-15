from Game import generate_npc
import openai

openai.api_key = open('src/resources/auth.txt', "r").read()


def main():
    npc = generate_npc()
    print(npc.make_description() + "\n")
    while True:
        question = input("Say: ").strip()
        if question == "":
            npc = generate_npc()
            print(npc.make_description() + "\n")
            continue
        prompt = npc.dialog_prompt(question)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        print(response.choices[0].text)


if __name__ == '__main__':
    main()