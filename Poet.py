import openai

class Poet:
    def __init__(self, api_key):
        openai.api_key = api_key
    
    def generate_poetry(self, theme, style="free verse"):
        prompt = f"Write a {style} poem about '{theme}', using vivid imagery, metaphors, and deep emotions."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        )
        return response.choices[0].text.strip()
