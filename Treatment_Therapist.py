import openai

class Therapist:
    def __init__(self, api_key):
        openai.api_key = api_key
    
    def offer_therapy(self, issue):
        prompt = f"Offer therapeutic advice on dealing with the issue of '{issue}', using methods like CBT, mindfulness, or positive psychology."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300
        )
        return response.choices[0].text.strip()
