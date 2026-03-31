import discord
from discord.ext import commands
import asyncio
import random
import os
import google.generativeai as genai

# --- CONFIG FROM KOYEB ---
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

try:
    OWNER_ID = int(os.getenv("OWNER_ID"))
except:
    OWNER_ID = 0

# Setup Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

authorized_users = [OWNER_ID]
bot = commands.Bot(command_prefix=".", self_bot=True, help_command=None)

@bot.event
async def on_ready():
    print(f"global gemini ghost active as {bot.user}")

@bot.command()
async def auth(ctx, user_id: int):
    # .auth still works globally for you
    if ctx.author.id != OWNER_ID:
        return
    if user_id not in authorized_users:
        authorized_users.append(user_id)
        async with ctx.typing():
            await asyncio.sleep(random.uniform(1.0, 1.5))
            await ctx.send("bet i got u they can use it now")

@bot.event
async def on_message(message):
    # 1. Process commands (.auth, .ask)
    await bot.process_commands(message)

    # 2. Ignore messages from the bot itself
    if message.author.id == bot.user.id:
        return

    # 3. Check if the user is in your authorized list
    if message.author.id in authorized_users:
        
        # Check for Mention or Reply
        is_mention = bot.user.mentioned_in(message)
        is_reply = False
        if message.reference:
            try:
                ref = await message.channel.fetch_message(message.reference.message_id)
                if ref.author.id == bot.user.id:
                    is_reply = True
            except: pass

        # TRIGGER: If pinged or replied to in ANY channel/server
        if is_mention or is_reply:
            async with message.channel.typing():
                # Random human-like delay
                await asyncio.sleep(random.uniform(3.5, 6.5))
                
                clean_content = message.content
                for mention in message.mentions:
                    clean_content = clean_content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
                clean_content = clean_content.strip()

                if not clean_content:
                    clean_content = "yo"

                try:
                    # System prompt for the persona
                    prompt = f"respond like a casual 13yo pro gamer no periods no commas all lowercase be an expert coach but talk normal: {clean_content}"
                    
                    response_data = model.generate_content(prompt)
                    ai_text = response_data.text.lower().replace('.', '').replace(',', '').strip()
                    
                    if not ai_text:
                        ai_text = "idk man my brain is fried"
                        
                    await message.reply(ai_text, mention_author=False)
                except Exception as e:
                    print(f"Gemini Error: {e}")
                    await message.reply("api is lagging bro wait", mention_author=False)

bot.run(TOKEN)
