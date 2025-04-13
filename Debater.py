import openai
import random

class Debater:
    def __init__(self, api_key, model="gpt-4"):
        openai.api_key = api_key
        self.model = model

    def generate_debate_topic(self):
        topics = [
            "Does free will exist?",
            "Is morality objective or subjective?",
            "Can science fully explain the universe?",
            "Is consciousness purely physical?",
            "Do humans have an inherent purpose?"
        ]
        return random.choice(topics)

    def generate_argument(self, topic):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a philosophical debater presenting nuanced arguments."},
                {"role": "user", "content": f"Debate the topic: {topic}. Provide arguments both for and against."}
            ],
            temperature=0.8,
            max_tokens=400
        )
        return response.choices[0].message["content"]
