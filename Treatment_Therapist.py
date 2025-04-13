import openai

class Therapist:
    def __init__(self, api_key, model="gpt-4"):
        openai.api_key = api_key
        self.model = model

    def offer_therapy(self, issue):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a compassionate therapist offering practical advice."},
                {"role": "user", "content": f"I am experiencing {issue}. What therapeutic guidance can you offer?"}
            ],
            temperature=0.8,
            max_tokens=300
        )
        return response.choices[0].message["content"]
