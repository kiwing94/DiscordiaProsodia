import openai

class Philosopher:
    def __init__(self, api_key):
        openai.api_key = api_key
    
    def generate_philosophical_text(self, theme):
        prompt = f"Write a philosophical text that explores the concept of {theme}. Address existential questions, abstract reasoning, and paradoxes."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300
        )
        return response.choices[0].text.strip()
