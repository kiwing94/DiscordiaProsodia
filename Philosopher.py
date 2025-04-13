import openai

class Philosopher:
    def __init__(self, api_key, model="gpt-4"):
        openai.api_key = api_key
        self.model = model

    def generate_philosophical_text(self, theme):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a philosophical thinker who explores complex ideas."},
                {"role": "user", "content": f"Write a deep philosophical text about {theme}."}
            ],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message["content"]
