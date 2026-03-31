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
    ALLOWED_CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
except:
    OWNER_ID = 0
    ALLOWED_CHANNEL_ID = 0

# Setup Gemini
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

authorized_users = [OWNER_ID]
bot = commands.Bot(command_prefix=".", self_bot=True, help_command=None)

@bot.event
async def on_ready():
    print(f"gemini ghost active as {bot.user}")

@bot.command()
async def auth(ctx, user_id: int):
    if ctx.channel.id != ALLOWED_CHANNEL_ID or ctx.author.id != OWNER_ID:
        return
    if user_id not in authorized_users:
        authorized_users.append(user_id)
        async with ctx.typing():
            await asyncio.sleep(random.uniform(1.0, 1.5))
            await ctx.send("bet i got u they can use it now")

@bot.event
async def on_message(message):
    if message.channel.id != ALLOWED_CHANNEL_ID:
        return

    await bot.process_commands(message)

    if message.author.id == bot.user.id:
        return

    if message.author.id in authorized_users:
        is_mention = bot.user.mentioned_in(message)
        is_reply = False
        if message.reference:
            try:
                ref = await message.channel.fetch_message(message.reference.message_id)
                if ref.author.id == bot.user.id:
                    is_reply = True
            except: pass

        if is_mention or is_reply:
            async with message.channel.typing():
                # Realistic human typing delay
                await asyncio.sleep(random.uniform(4.0, 7.0))
                
                clean_content = message.content
                for mention in message.mentions:
                    clean_content = clean_content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
                clean_content = clean_content.strip()

                if not clean_content:
                    clean_content = "yo"

                try:
                    # THE GEMINI SYSTEM PROMPT: 
                    # This tells Gemini how to act so it doesn't sound like a robot.
                    prompt = f"Answer this short and casual like a 13yo pro gamer. No periods, no commas, all lowercase. Be an expert coach but talk normal: {clean_content}"
                    
                    response_data = model.generate_content(prompt)
                    ai_text = response_data.text.lower().replace('.', '').replace(',', '').strip()
                    
                    if not ai_text:
                        ai_text = "idk man my brain is fried"
                        
                    await message.reply(ai_text, mention_author=False)
                except Exception as e:
                    print(f"Gemini Error: {e}")
                    await message.reply("api is lagging bro hold on", mention_author=False)

bot.run(TOKEN)
