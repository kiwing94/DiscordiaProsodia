from Debater import Debater
from Philosopher import Philosopher
from Treatment_Therapist import Therapist
from Poet import Poet
from Artistic_creative_musician import CreativeMusician
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Log output to a file
def log_output(category, content):
    with open("output_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}] {category}:\n{content}\n")

# Main function
def main():
    print("Welcome to your versatile AI bot!")

    # Initialize all modules with GPT-4
    debater = Debater(api_key, model="gpt-4")
    philosopher = Philosopher(api_key, model="gpt-4")
    therapist = Therapist(api_key, model="gpt-4")
    poet = Poet(api_key, model="gpt-4")
    musician = CreativeMusician(api_key, model="gpt-4")

    while True:
        print("\nWhat would you like to do?")
        print("1. Start a debate")
        print("2. Get a philosophical reflection")
        print("3. Receive therapeutic advice")
        print("4. Generate poetry")
        print("5. Generate music lyrics")
        print("6. Exit")
        print("7. Freestyle rap battle")

        choice = input("Pick an option (1-7): ")

        if choice == '1':
            topic = debater.generate_debate_topic()
            arguments = debater.generate_argument(topic)
            print(f"\nDebate Topic: {topic}\n{arguments}")
            log_output("Debate", f"{topic}\n{arguments}")

        elif choice == '2':
            theme = input("Enter a philosophical theme: ")
            philosophical_text = philosopher.generate_philosophical_text(theme)
            print(f"\nPhilosophical Reflection:\n{philosophical_text}")
            log_output("Philosophy", philosophical_text)

        elif choice == '3':
            issue = input("Describe your issue: ")
            therapy_advice = therapist.offer_therapy(issue)
            print(f"\nTherapeutic Advice:\n{therapy_advice}")
            log_output("Therapy", therapy_advice)

        elif choice == '4':
            theme = input("Poem theme: ")
            style = input("Poem style (e.g., haiku, free verse): ")
            poetry = poet.generate_poetry(theme, style)
            print(f"\nPoetry:\n{poetry}")
            log_output("Poetry", poetry)

        elif choice == '5':
            theme = input("Song theme: ")
            genre = input("Song genre (e.g., rock, pop, rap): ")
            song = musician.generate_song(theme, genre)
            print(f"\nSong Lyrics:\n{song}")
            log_output("Music", song)

        elif choice == '6':
            print("Exiting the program. Thank you for using the AI bot!")
            break

        elif choice == '7':
            prompt = input("What's your rap about? ")
            rap = musician.generate_song(prompt, genre="rap")
            print(f"\nFreestyle Rap:\n{rap}")
            log_output("Rap", rap)

        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
