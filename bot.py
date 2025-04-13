import os
import discord
import openai
import asyncio
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

intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)
tree = client.tree

debater = Debater(OPENAI_API_KEY)
philosopher = Philosopher(OPENAI_API_KEY)
therapist = Therapist(OPENAI_API_KEY)
poet = Poet(OPENAI_API_KEY)
musician = CreativeMusician(OPENAI_API_KEY)

def log_output(category, content):
    with open("output_log.txt", "a", encoding="utf-8") as f:
        f.write(f"\n[{datetime.now()}] {category}:\n{content}\n")

@client.event
async def on_ready():
    await tree.sync()
    client.loop.create_task(keep_alive_loop())
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower() == "ping":
        await message.channel.send("Pong!")
    await client.process_commands(message)

async def keep_alive_loop():
    while True:
        print("✅ Bot is still alive...")
        await asyncio.sleep(300)

@tree.command(name="ping", description="Check if the bot is online.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@tree.command(name="persona", description="Change the bot's personality style for responses.")
@app_commands.describe(type="Choose a persona style: oracle, philosopher, child, bard, therapist")
async def persona(interaction: discord.Interaction, type: str):
    personas = {
        "oracle": "You are an enigmatic oracle who speaks in poetic riddles and timeless wisdom.",
        "philosopher": "You are a deep philosopher who reflects on consciousness and reality.",
        "child": "You are a playful, innocent child who responds with joy and imagination.",
        "bard": "You are a medieval bard who tells stories in lyrical, musical form.",
        "therapist": "You are a gentle, professional therapist providing comforting insights."
    }

    if type not in personas:
        await interaction.response.send_message(
            f"❌ Unknown persona. Choose from: {', '.join(personas.keys())}", ephemeral=True
        )
        return

    prompt = f"Respond in the style of a {type}. Say a greeting to the user as that persona."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": personas[type]},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=150
    )

    output = response.choices[0].message["content"]
    await interaction.response.send_message(f"**{type.capitalize()} persona activated:**\n{output}")
    log_output("Persona", f"{type}: {output}")



@tree.command(name="soulweave", description="Generate a poetic soul-stanza from your name, mood, and chosen language.")
@app_commands.describe(
    name="Your name or symbolic identity",
    mood="How you feel right now",
    language="Language to weave your soul in: English, Latin, Greek, Tagalog"
)
async def soulweave(interaction: discord.Interaction, name: str, mood: str, language: str):
    supported_languages = ["English", "Latin", "Greek", "Tagalog"]
    if language not in supported_languages:
        await interaction.response.send_message(
            f"❌ Unsupported language. Please choose from: {', '.join(supported_languages)}",
            ephemeral=True
        )
        return

    time_signature = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    prompt = (
        f"Create a beautiful, mystical, poetic stanza inspired by the following details:
"
        f"- Name: {name}
"
        f"- Mood: {mood}
"
        f"- Timestamp: {time_signature}
"
        f"- Language: {language}
"
        f"Make it feel personal and eternal, like an incantation or spell, with internal rhythm and subtle rhyme.
"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are a divine poetic oracle writing incantations in {language}."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=200
    )

    verse = response.choices[0].message["content"]
    await interaction.response.send_message(f"🪶 **Soulweave for {name} ({language})**

{verse}")
    log_output("Soulweave", f"{name} ({language}) / {mood}:
{verse}")



@tree.command(name="oracle", description="Receive cryptic poetic wisdom from the oracle.")
async def oracle(interaction: discord.Interaction):
    prompt = "Speak a poetic truth or cryptic wisdom as if from an ancient oracle. Keep it short, profound, and symbolic."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an ancient oracle who speaks in poetic truths and cryptic symbols."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.95,
        max_tokens=100
    )
    quote = response.choices[0].message["content"]
    await interaction.response.send_message(f"🔮 **Oracle speaks:**
{quote}")
    log_output("Oracle", quote)

@tree.command(name="myth", description="Generate a short myth or fable based on a theme.")
@app_commands.describe(theme="The central theme (e.g., betrayal, love, time)")
async def myth(interaction: discord.Interaction, theme: str):
    prompt = f"Create a short myth or fable based on the theme '{theme}'. It should feel ancient, symbolic, and meaningful."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a cosmic mythmaker who invents ancient stories to explain the world."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
        max_tokens=250
    )
    story = response.choices[0].message["content"]
    await interaction.response.send_message(f"📜 **Myth of {theme.capitalize()}**
{story}")
    log_output("Myth", f"{theme}:
{story}")

@tree.command(name="spell", description="Spell a word phonetically or mystically.")
@app_commands.describe(word="The word to spell out", style="Style: phonetic or magical")
async def spell(interaction: discord.Interaction, word: str, style: str):
    if style not in ["phonetic", "magical"]:
        await interaction.response.send_message("❌ Style must be 'phonetic' or 'magical'", ephemeral=True)
        return
    prompt = f"Spell the word '{word}' in a {style} style. Phonetic should be clear and IPA-like, magical should be creative and symbolic."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You spell words based on their sound and symbolism."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=100
    )
    result = response.choices[0].message["content"]
    await interaction.response.send_message(f"🔤 **{style.capitalize()} Spelling of '{word}':**
{result}")
    log_output("Spell", f"{word} / {style}: {result}")

@tree.command(name="etymology", description="Reveal the origin and evolution of a word.")
@app_commands.describe(word="The word to analyze")
async def etymology(interaction: discord.Interaction, word: str):
    prompt = f"Explain the etymology of the word '{word}'. Include original language, roots, and meaning evolution."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a linguistic historian who explains etymologies in a clear and elegant way."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=200
    )
    history = response.choices[0].message["content"]
    await interaction.response.send_message(f"📖 **Etymology of '{word}':**
{history}")
    log_output("Etymology", f"{word}: {history}")



@tree.command(name="divine", description="Receive a sacred answer from a mystic or spiritual guide.")
@app_commands.describe(
    reflection="A doubt, feeling, or spiritual question",
    tone="The tone of response: gentle, fierce, poetic, absolute, mystic"
)
async def divine(interaction: discord.Interaction, reflection: str, tone: str):
    tones = {
        "gentle": "You are a nurturing spiritual guide, like a priestess, who speaks with compassion and light.",
        "fierce": "You are a fiery prophet who declares divine truth with passion and intensity.",
        "poetic": "You are a scripture-singer who speaks in lyrical verses and metaphor.",
        "absolute": "You are a confident oracle, speaking eternal truths with certainty.",
        "mystic": "You are a mystic who sees beyond the veil and answers with dreamlike riddles."
    }

    if tone not in tones:
        await interaction.response.send_message(
            f"❌ Unknown tone. Choose from: {', '.join(tones.keys())}",
            ephemeral=True
        )
        return

    prompt = f"A person shares the reflection: '{reflection}'. Respond as a divine spiritual leader with the tone: {tone}."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": tones[tone]},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
        max_tokens=250
    )

    answer = response.choices[0].message["content"]
    await interaction.response.send_message(f"🕊️ **Divine Insight ({tone.capitalize()}):**
{answer}")
    log_output("Divine", f"{tone} / {reflection}:
{answer}")

client.run(DISCORD_TOKEN)
