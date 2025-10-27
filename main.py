import discord
from discord import app_commands
from discord.ext import commands
import requests
import os

TOKEN = os.getenv("DISCORD_TOKEN")
FONT_API_KEY = os.getenv("FONT_API_KEY")
HELPER_ROLE_ID = 123456789012345678  # Replace with your helper role ID

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="for /findfont 🎨"))
        synced = await bot.tree.sync()
        print(f"📘 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Sync error: {e}")

@bot.tree.command(name="findfont", description="Find the font used in an uploaded image")
@app_commands.describe(image="Upload an image to identify the font")
async def findfont(interaction: discord.Interaction, image: discord.Attachment):
    await interaction.response.defer(thinking=True)
    await interaction.followup.send("🔍 **Analyzing font...** Please wait 2–5 minutes ⏳")

    try:
        api_url = "https://www.whatfontis.com/api2/"
        payload = {
            "API_KEY": FONT_API_KEY,
            "IMAGEBASE64": 0,
            "urlimage": image.url,
            "limit": 1,
            "FREEFONTS": 0
        }

        res = requests.post(api_url, json=payload, timeout=180)
        data = res.json()

        if isinstance(data, list) and len(data) > 0 and "title" in data[0]:
            font = data[0]["title"]
            link = data[0]["url"]
            await interaction.followup.send(f"✅ **Font Found:** **{font}**\n🔗 [View Font Here]({link})")
        else:
            await interaction.followup.send(f"⚠️ Could not detect the font. Please <@&{HELPER_ROLE_ID}> for manual help.")
    except Exception as e:
        print(e)
        await interaction.followup.send(f"❌ Something went wrong. Please <@&{HELPER_ROLE_ID}> for assistance.")

bot.run(TOKEN)
