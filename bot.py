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



@tree.command(name="reconstruct", description="Reconstruct the ancestral root form of a word.")
@app_commands.describe(word="The modern word to trace", language="Choose PIE, Sumerian, or Akkadian")
async def reconstruct(interaction: discord.Interaction, word: str, language: str):
    ancient_langs = ["PIE", "Sumerian", "Akkadian"]
    if language not in ancient_langs:
        await interaction.response.send_message(
            f"❌ Language not supported. Choose from: {', '.join(ancient_langs)}", ephemeral=True
        )
        return

    prompt = f"Reconstruct the ancient form of the word '{word}' in {language}. Include the root, meaning, and how it evolved into modern terms."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"You are an expert historical linguist and etymologist specializing in {language}."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=300
    )

    result = response.choices[0].message["content"]
    await interaction.response.send_message(f"🗿 **Reconstructed Root in {language}:**
{result}")
    log_output("Reconstruct", f"{word} ({language}): {result}")

@tree.command(name="languageflow", description="Trace a word's path through ancient languages.")
@app_commands.describe(concept="The concept to trace (e.g. soul, star, light)")
async def languageflow(interaction: discord.Interaction, concept: str):
    prompt = (
        f"Trace the linguistic evolution of the concept '{concept}' through at least 4 ancient languages: "
        "Proto-Indo-European (PIE), Sanskrit, Ancient Greek, Latin, and optionally Old English or Sumerian. "
        "Include the word forms, meanings, and phonetic transitions."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a historical linguist specializing in Indo-European and Mesopotamian roots."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.65,
        max_tokens=400
    )

    flow = response.choices[0].message["content"]
    await interaction.response.send_message(f"🌐 **Language Flow for '{concept}':**
{flow}")
    log_output("LanguageFlow", f"{concept}:
{flow}")



@tree.command(name="sacredword", description="Reveal the sacred or symbolic use of a word in ancient rites or languages.")
@app_commands.describe(word="The word you want analyzed symbolically")
async def sacredword(interaction: discord.Interaction, word: str):
    prompt = (
        f"Explain the mythic, religious, or symbolic significance of the word '{word}' "
        f"as used in ancient civilizations — especially Sumerian if applicable. "
        f"Describe how it was used in ritual, cosmology, or magic."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a priest-scholar of ancient languages, especially Sumerian and Akkadian. You explain sacred symbols."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.75,
        max_tokens=300
    )

    meaning = response.choices[0].message["content"]
    await interaction.response.send_message(f"🔺 **Sacred Meaning of '{word}':**
{meaning}")
    log_output("SacredWord", f"{word}: {meaning}")



@tree.command(name="ritual", description="Generate a symbolic ritual ceremony based on a theme and type.")
@app_commands.describe(theme="The intent or energy of the ritual", type="Type: spoken, silent, poetic")
async def ritual(interaction: discord.Interaction, theme: str, type: str):
    if type not in ["spoken", "silent", "poetic"]:
        await interaction.response.send_message("❌ Type must be one of: spoken, silent, poetic", ephemeral=True)
        return

    prompt = (
        f"Design a ritual around the theme '{theme}' in the style '{type}'. "
        f"Include symbolic elements, gestures, materials, space, and purpose. Keep it sacred and meaningful."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a sacred ritualist designing ceremonies with poetic and mystical elements."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.85,
        max_tokens=450
    )

    ritual_text = response.choices[0].message["content"]
    await interaction.response.send_message(f"🕯️ **Ritual for '{theme}' ({type})**
{ritual_text}")
    log_output("Ritual", f"{theme} / {type}:
{ritual_text}")

@tree.command(name="summon", description="Summon an archetypal entity or symbol and let it speak.")
@app_commands.describe(entity="The being or archetype to summon (e.g., Hope, Trickster, Oracle)")
async def summon(interaction: discord.Interaction, entity: str):
    prompt = f"Summon the symbolic entity '{entity}' and let it speak to the user in its true voice."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are the voice of summoned symbolic entities — poetic, strange, powerful."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.95,
        max_tokens=250
    )

    speech = response.choices[0].message["content"]
    await interaction.response.send_message(f"🔺 **{entity.upper()} Appears:**
{speech}")
    log_output("Summon", f"{entity}: {speech}")

@tree.command(name="temple", description="Construct a symbolic sacred space in language.")
@app_commands.describe(purpose="Purpose of the temple", style="Style: ancient Greek, dreamlike, minimal, cosmic, personal")
async def temple(interaction: discord.Interaction, purpose: str, style: str):
    prompt = (
        f"Describe a sacred temple created for the purpose of '{purpose}' in a '{style}' style. "
        "Make it poetic, visual, and spiritually resonant."
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a sacred architect of inner and cosmic temples."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.9,
        max_tokens=350
    )

    description = response.choices[0].message["content"]
    await interaction.response.send_message(f"🏛️ **Temple for {purpose.capitalize()} ({style})**
{description}")
    log_output("Temple", f"{purpose} / {style}:
{description}")

client.run(DISCORD_TOKEN)
