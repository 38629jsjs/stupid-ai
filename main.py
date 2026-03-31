import discord
from discord.ext import commands
import asyncio
import random
import os
import requests

# --- CONFIG FROM KOYEB ---
TOKEN = os.getenv("DISCORD_TOKEN")
try:
    OWNER_ID = int(os.getenv("OWNER_ID"))
    ALLOWED_CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
except:
    OWNER_ID = 0
    ALLOWED_CHANNEL_ID = 0

authorized_users = [OWNER_ID]

bot = commands.Bot(command_prefix=".", self_bot=True, help_command=None)

@bot.event
async def on_ready():
    print(f"ghost coach active as {bot.user} | channel {ALLOWED_CHANNEL_ID}")

@bot.command()
async def auth(ctx, user_id: int):
    if ctx.channel.id != ALLOWED_CHANNEL_ID or ctx.author.id != OWNER_ID:
        return
    if user_id not in authorized_users:
        authorized_users.append(user_id)
        async with ctx.typing():
            await asyncio.sleep(random.uniform(1.0, 1.5))
            await ctx.send("bet i got u they can use it now")

@bot.command()
async def ask(ctx):
    if ctx.channel.id != ALLOWED_CHANNEL_ID or ctx.author.id not in authorized_users:
        return
    async with ctx.typing():
        await asyncio.sleep(random.uniform(1.0, 2.0))
        await ctx.send("sup what u need help with")

@bot.event
async def on_message(message):
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return

    await bot.process_commands(message)

    if message.author.id == bot.user.id:
        return

    if message.reference:
        try:
            if message.author.id in authorized_users:
                referenced_msg = await message.channel.fetch_message(message.reference.message_id)
                if referenced_msg.author.id == bot.user.id:
                    async with message.channel.typing():
                        # Thinking delay
                        await asyncio.sleep(random.uniform(3.0, 5.0))
                        
                        # Get real AI response from free API
                        try:
                            api_url = f"https://api.simsimi.vn/v1/simtalk"
                            payload = {"text": message.content, "lc": "en"}
                            r = requests.get(api_url, params=payload)
                            # Force lowercase and remove punctuation to stay lowkey
                            response = r.json().get('message', 'idk man brain lag').lower().replace('.', '').replace(',', '')
                        except:
                            response = "my bad bro lost my train of thought what was that again"

                        await message.reply(response, mention_author=False)
        except:
            pass

bot.run(TOKEN)
