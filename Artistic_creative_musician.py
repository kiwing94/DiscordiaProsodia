import openai

class CreativeMusician:
    def __init__(self, api_key):
        openai.api_key = api_key
    
    def generate_song(self, theme, genre="pop"):
        prompt = f"Write a {genre} song with verses and a catchy chorus about '{theme}'. Use creative lyrics and rhythm."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        )
        return response.choices[0].text.strip()
