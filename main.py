import discord
from discord.ext import commands
import asyncio
import random
import os

# --- CONFIG FROM KOYEB ---
TOKEN = os.getenv("DISCORD_TOKEN")
# Convert ID to int so the check works
try:
    AUTHORIZED_ID = int(os.getenv("AUTHORIZED_ID"))
except:
    AUTHORIZED_ID = 0

bot = commands.Bot(command_prefix=".", self_bot=True, help_command=None)

@bot.event
async def on_ready():
    print(f"ghost coach active as {bot.user}")

@bot.command()
async def ask(ctx):
    if ctx.author.id != AUTHORIZED_ID:
        return
    await ctx.send("ask me anything")

@bot.event
async def on_message(message):
    if message.author.id == bot.user.id:
        return

    if message.reference and message.author.id == AUTHORIZED_ID:
        try:
            referenced_msg = await message.channel.fetch_message(message.reference.message_id)
            
            if referenced_msg.author.id == bot.user.id:
                async with message.channel.typing():
                    # Random delay so it looks like a real person typing
                    await asyncio.sleep(random.uniform(2.5, 4.5))
                    
                    query = message.content.lower()
                    
                    # --- CASUAL EXPERT RESPONSES (NO PUNCTUATION) ---
                    if "game" in query or "mlbb" in query:
                        response = "bro just focus on map awareness and stop chasing kills if u want mythical immortal focus on the lord and push towers dont overstay"
                    elif "money" in query or "grind" in query:
                        response = "keep the alts staggered and dont burst commands or automod will catch u again stay lowkey and secure the bank every hour"
                    elif "fitness" in query or "gym" in query:
                        response = "focus on form over heavy weight man consistency is everything if u want results do it every single night without fail"
                    elif "help" in query or "how" in query:
                        response = "honestly just stay calm and look at the logic behind it most people rush and fail but if u take it slow u win every time"
                    else:
                        response = "u just gotta stay focused and keep grinding thats the only secret to being a pro for real"

                    await message.reply(response, mention_author=False)
        except:
            pass

    await bot.process_commands(message)

bot.run(TOKEN)
