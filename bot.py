import os
import discord
import openai
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime

from Debater import Debater
from Philosopher import Philosopher
from Treatment_Therapist import Therapist
from Poet import Poet
from Artistic_creative_musician import CreativeMusician

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Bot setup
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)
tree = client.tree  # Use the existing tree from the bot

# AI modules
debater = Debater(OPENAI_API_KEY, model="gpt-4")
philosopher = Philosopher(OPENAI_API_KEY, model="gpt-4")
therapist = Therapist(OPENAI_API_KEY, model="gpt-4")
poet = Poet(OPENAI_API_KEY, model="gpt-4")
musician = CreativeMusician(OPENAI_API_KEY, model="gpt-4")

# Logging
def log_output(category, content):
    with open("output_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}] {category}:\n{content}\n")

@client.event
async def on_ready():
    await tree.sync()
    print(f"Logged in as {client.user}")

# Slash commands
@tree.command(name="debate", description="Generate a debate topic with arguments.")
async def debate(interaction: discord.Interaction):
    topic = debater.generate_debate_topic()
    arguments = debater.generate_argument(topic)
    await interaction.response.send_message(f"**Debate Topic:** {topic}\n{arguments}")
    log_output("Debate", f"{topic}\n{arguments}")

@tree.command(name="philosophy", description="Generate a philosophical reflection.")
@app_commands.describe(theme="The theme to reflect on.")
async def philosophy(interaction: discord.Interaction, theme: str):
    text = philosopher.generate_philosophical_text(theme)
    await interaction.response.send_message(f"**Philosophical Reflection on {theme}:**\n{text}")
    log_output("Philosophy", text)

@tree.command(name="therapy", description="Get therapeutic advice on an issue.")
@app_commands.describe(issue="The issue you're dealing with.")
async def therapy(interaction: discord.Interaction, issue: str):
    advice = therapist.offer_therapy(issue)
    await interaction.response.send_message(f"**Therapy Advice for '{issue}':**\n{advice}")
    log_output("Therapy", advice)

@tree.command(name="poem", description="Generate a poem.")
@app_commands.describe(theme="Poem theme", style="Poem style (e.g., haiku, free verse)")
async def poem(interaction: discord.Interaction, theme: str, style: str):
    poetry = poet.generate_poetry(theme, style)
    await interaction.response.send_message(f"**Poem ({style}) on {theme}:**\n{poetry}")
    log_output("Poetry", poetry)

@tree.command(name="song", description="Generate a song.")
@app_commands.describe(theme="Song theme", genre="Genre (e.g., rock, pop, rap)")
async def song(interaction: discord.Interaction, theme: str, genre: str):
    lyrics = musician.generate_song(theme, genre)
    await interaction.response.send_message(f"**{genre.capitalize()} Song about '{theme}':**\n{lyrics}")
    log_output("Music", lyrics)

@tree.command(name="rap", description="Freestyle rap on a topic.")
@app_commands.describe(theme="Rap topic")
async def rap(interaction: discord.Interaction, theme: str):
    bars = musician.generate_song(theme, genre="rap")
    await interaction.response.send_message(f"**Freestyle Rap about '{theme}':**\n{bars}")
    log_output("Rap", bars)

@tree.command(name="mentalhealth", description="Get a reflective mental health support message.")
@app_commands.describe(prompt="Your mental health concern")
async def mentalhealth(interaction: discord.Interaction, prompt: str):
    message = therapist.offer_therapy(prompt)
    await interaction.response.send_message(f"**Mental Health Support:**\n{message}")
    log_output("MentalHealth", message)

client.run(DISCORD_TOKEN)





# Autocomplete language choices
async def language_autocomplete(interaction: discord.Interaction, current: str):
    supported = ["Latin", "Greek", "Koine Greek", "English", "Arabic", "Spanish", "Italian", "Tagalog"]
    return [
        app_commands.Choice(name=lang, value=lang)
        for lang in supported if current.lower() in lang.lower()
    ][:25]

@tree.command(name="translate", description="Translate a phrase to a supported language.")
@app_commands.describe(
    text="The text you want to translate.",
    target_language="The target language"
)
@app_commands.autocomplete(target_language=language_autocomplete)
async def translate(interaction: discord.Interaction, text: str, target_language: str):
    supported_languages = ["Latin", "Greek", "Koine Greek", "English", "Arabic", "Spanish", "Italian", "Tagalog"]
    if target_language not in supported_languages:
        await interaction.response.send_message(
            f"❌ Unsupported language. Please choose from: {', '.join(supported_languages)}",
            ephemeral=True
        )
        return

@tree.command(name="backtranslate", description="Translate a phrase and then back to English to check meaning preservation.")
@app_commands.describe(
    original_text="Original phrase to translate",
    target_language="Target language to test"
)
@app_commands.autocomplete(target_language=language_autocomplete)
async def backtranslate(interaction: discord.Interaction, original_text: str, target_language: str):
    supported_languages = ["Latin", "Greek", "Koine Greek", "English", "Arabic", "Spanish", "Italian", "Tagalog"]
    if target_language not in supported_languages:
        await interaction.response.send_message(
            f"❌ Unsupported language. Choose from: {', '.join(supported_languages)}",
            ephemeral=True
        )
        return

    first_translation_prompt = f"Translate this to {target_language}:\n{original_text}"
    back_translation_prompt = f"Now translate that back into English and explain if anything was lost in the process."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a bilingual translator checking fidelity between languages."},
            {"role": "user", "content": first_translation_prompt},
            {"role": "assistant", "content": "(translated text)"},
            {"role": "user", "content": back_translation_prompt}
        ],
        temperature=0.5,
        max_tokens=350
    )
    backtranslated = response.choices[0].message["content"]
    await interaction.response.send_message(f"**Backtranslation Check from {target_language} to English:**\n{backtranslated}")
    log_output("Backtranslate", f"From {target_language}: {backtranslated}")
