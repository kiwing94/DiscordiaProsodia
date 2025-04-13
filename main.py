from dotenv import load_dotenv
import os
from Debater import Debater
from Philosopher import Philosopher
from Treatment_Therapist import Therapist
from Poet import Poet
from Artistic_creative_musician import CreativeMusician

# Ladda miljövariabler från .env-filen
load_dotenv()

# Hämta API-nyckeln från miljövariabler
api_key = os.getenv("OPENAI_API_KEY")

# Funktion för att starta huvudprogrammet
def main():
    print("Bot awakened!")

    # Skapa instanser av varje modul
    debater = Debater(api_key)
    philosopher = Philosopher(api_key)
    therapist = Therapist(api_key)
    poet = Poet(api_key)
    musician = CreativeMusician(api_key)

    while True:
        print("\nYour wish is my command?")
        print("1. Debate")
        print("2. Generate philosophical texts")
        print("3. Get mental health advice")
        print("4. Create poetry")
        print("5. Create songs in music")
        print("6. Terminate operations")

        choice = input("Pick an alternative from 1 to 6 (1-6): ")

        if choice == '1':
            topic = debater.generate_debate_topic()
            arguments = debater.generate_argument(topic)
            print(f"\nDebattämnet: {topic}\n{arguments}")

        elif choice == '2':
            philosophical_text = philosopher.generate_philosophical_text("consciousness")
            print(f"\nFilosofisk text:\n{philosophical_text}")

        elif choice == '3':
            therapy_advice = therapist.offer_therapy("anxiety")
            print(f"\nTerapiråd:\n{therapy_advice}")

        elif choice == '4':
            poetry = poet.generate_poetry("love and nature")
            print(f"\nPoesi:\n{poetry}")

        elif choice == '5':
            song = musician.generate_song("freedom and peace", genre="rock")
            print(f"\nLåttext:\n{song}")

        elif choice == '6':
            print("Avslutar programmet. Thanks for interacting with CitizenBot!")
            break

        else:
            print("Bad choice! Try once again.")


if __name__ == "__main__":
    main()
