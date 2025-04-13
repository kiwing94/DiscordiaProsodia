import random
import openai

class Debater:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_debate_topic(self):
        topics = [
            "Does free will exist?",
            "Is morality objective or subjective?",
            "Can the universe be explained by science alone?",
            "Is consciousness purely physical?",
            "Do humans have an inherent purpose?"
        ]
        return random.choice(topics)
    
    def generate_argument(self, topic):
        prompt = f"Generate a strong argument for and against the topic '{topic}', providing contradictions and complex reasoning."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300
        )
        return response.choices[0].text.strip()

    def debate(self):
        topic = self.generate_debate_topic()
        arguments = self.generate_argument(topic)
        return topic, arguments
