import openai

class Poet:
    def __init__(self, api_key, model="gpt-4"):
        openai.api_key = api_key
        self.model = model

    def generate_poetry(self, theme, style="free verse"):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a skilled poet."},
                {"role": "user", "content": f"Write a {style} poem about {theme}."}
            ],
            temperature=0.9,
            max_tokens=250
        )
        return response.choices[0].message["content"]
