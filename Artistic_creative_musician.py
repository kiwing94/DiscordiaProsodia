import openai

class CreativeMusician:
    def __init__(self, api_key, model="gpt-4"):
        openai.api_key = api_key
        self.model = model

    def generate_song(self, theme, genre="pop"):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": f"You are a creative songwriter in the {genre} genre."},
                {"role": "user", "content": f"Write a {genre} song about '{theme}' with verses and a catchy chorus."}
            ],
            temperature=0.85,
            max_tokens=300
        )
        return response.choices[0].message["content"]
