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
    # Lock to the correct channel
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return

    # Process .ask and .auth commands
    await bot.process_commands(message)

    # Ignore self
    if message.author.id == bot.user.id:
        return

    # Check if the person talking is allowed to use the AI
    if message.author.id in authorized_users:
        
        # TRIGGER 1: Direct Mention (@) OR TRIGGER 2: Reply to the bot
        is_reply_to_bot = False
        if message.reference:
            try:
                ref = await message.channel.fetch_message(message.reference.message_id)
                if ref.author.id == bot.user.id:
                    is_reply_to_bot = True
            except:
                pass

        # If mentioned OR replied to
        if bot.user.mentioned_in(message) or is_reply_to_bot:
            async with message.channel.typing():
                # Random "thinking" delay to look human
                await asyncio.sleep(random.uniform(3.0, 5.5))
                
                # Remove the mention from the text so the AI doesn't get confused
                clean_content = message.content.replace(f'<@{bot.user.id}>', '').replace(f'<@!{bot.user.id}>', '').strip()
                
                if not clean_content:
                    response = "yea what's up"
                else:
                    try:
                        api_url = f"https://api.simsimi.vn/v1/simtalk"
                        payload = {"text": clean_content, "lc": "en"}
                        r = requests.get(api_url, params=payload)
                        # Keep it casual: lowercase, no dots/commas
                        response = r.json().get('message', 'idk man brain lag').lower().replace('.', '').replace(',', '')
                    except:
                        response = "my bad bro lost my train of thought what was that again"

                # Use a reply but turn off the ping in the response to stay lowkey
                await message.reply(response, mention_author=False)

bot.run(TOKEN)
