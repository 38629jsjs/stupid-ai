import discord
from discord.ext import commands
import asyncio
import random
import os

# --- CONFIG FROM KOYEB ---
TOKEN = os.getenv("DISCORD_TOKEN")
try:
    OWNER_ID = int(os.getenv("OWNER_ID"))
    # Lock the bot to a specific channel
    ALLOWED_CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
except:
    OWNER_ID = 0
    ALLOWED_CHANNEL_ID = 0

authorized_users = [OWNER_ID]

bot = commands.Bot(command_prefix=".", self_bot=True, help_command=None)

@bot.event
async def on_ready():
    print(f"ghost coach active as {bot.user} | locked to channel {ALLOWED_CHANNEL_ID}")

# --- OWNER ONLY: AUTHORIZE OTHERS ---
@bot.command()
async def auth(ctx, user_id: int):
    # Only work in the allowed channel and only for the owner
    if ctx.channel.id != ALLOWED_CHANNEL_ID or ctx.author.id != OWNER_ID:
        return
    
    if user_id not in authorized_users:
        authorized_users.append(user_id)
        async with ctx.typing():
            await asyncio.sleep(random.uniform(1.0, 1.5))
            await ctx.send("bet i got u they can use it now")

# --- AUTHORIZED USERS: ACTIVATE THE AI ---
@bot.command()
async def ask(ctx):
    # Only work in the allowed channel and for authorized users
    if ctx.channel.id != ALLOWED_CHANNEL_ID or ctx.author.id not in authorized_users:
        return
    
    async with ctx.typing():
        await asyncio.sleep(random.uniform(1.0, 2.0))
        await ctx.send("sup what u need help with")

@bot.event
async def on_message(message):
    # 1. Ignore everything outside the allowed channel
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return

    # 2. Process commands (.ask, .auth)
    await bot.process_commands(message)

    # 3. Ignore self
    if message.author.id == bot.user.id:
        return

    # 4. Handle Expert Replies
    if message.reference:
        try:
            if message.author.id in authorized_users:
                referenced_msg = await message.channel.fetch_message(message.reference.message_id)
                
                if referenced_msg.author.id == bot.user.id:
                    async with message.channel.typing():
                        await asyncio.sleep(random.uniform(3.0, 5.0))
                        
                        query = message.content.lower()
                        
                        # --- CASUAL EXPERT RESPONSES (NO PUNCTUATION) ---
                        if "game" in query or "mlbb" in query:
                            response = "bro just focus on map awareness and stop chasing kills if u want mythical immortal focus on the lord and push towers dont overstay"
                        elif "money" in query or "grind" in query:
                            response = "keep the alts staggered and dont burst commands or automod will catch u again stay lowkey and secure the bank every hour"
                        elif "fitness" in query or "gym" in query:
                            response = "focus on form over heavy weight man consistency is everything if u want results do it every single night without fail"
                        else:
                            response = "u just gotta stay focused and keep grinding thats the only secret to being a pro for real"

                        await message.reply(response, mention_author=False)
        except:
            pass

bot.run(TOKEN)
