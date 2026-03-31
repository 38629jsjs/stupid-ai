import discord
from discord.ext import commands
import asyncio
import random
import os
from google import genai

# --- CONFIG FROM KOYEB ---
TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

try:
    OWNER_ID = int(os.getenv("OWNER_ID"))
except:
    OWNER_ID = 0

# Setup the NEW Gemini Client
client = genai.Client(api_key=GEMINI_KEY)

authorized_users = [OWNER_ID]
bot = commands.Bot(command_prefix=".", self_bot=True, help_command=None)

@bot.event
async def on_ready():
    print(f"global normal egirl ghost active as {bot.user}")

@bot.command()
async def auth(ctx, user_id: int):
    # Only you can authorize others to use the AI
    if ctx.author.id != OWNER_ID:
        return
    if user_id not in authorized_users:
        authorized_users.append(user_id)
        async with ctx.typing():
            await asyncio.sleep(random.uniform(1.0, 1.5))
            await ctx.send("got u they can use it now")

@bot.event
async def on_message(message):
    # 1. Process commands (.auth)
    await bot.process_commands(message)

    # 2. Ignore messages from the bot itself
    if message.author.id == bot.user.id:
        return

    # 3. Check if the user is authorized (You or friends)
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
                # Random human-like delay (3.5 to 6.5 seconds)
                await asyncio.sleep(random.uniform(3.5, 6.5))
                
                # Clean up the mention from the message
                clean_content = message.content
                for mention in message.mentions:
                    clean_content = clean_content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
                clean_content = clean_content.strip() or "hi"

                try:
                    # THE NORMAL EGIRL PERSONA
                    persona = (
                        "respond like a normal chill 13yo egirl on discord. "
                        "don't act like an expert. stay lowkey. "
                        "no periods, no commas, all lowercase. "
                        "don't be sassy, don't be a pickme, just be helpful and cool. "
                        "use casual slang like 'fr', 'lowkey', 'literally', 'lol', or 'rn' occasionally. "
                        "never use 'bro', 'man', or 'dude'."
                    )
                    
                    # Generate with the NEW Gemini library
                    response = client.models.generate_content(
                        model="gemini-1.5-flash",
                        contents=f"{persona}\n\nUser says: {clean_content}"
                    )
                    
                    # Force clean formatting (all lowercase, no dots or commas)
                    ai_text = response.text.lower().replace('.', '').replace(',', '').strip()
                    
                    if not ai_text:
                        ai_text = "idk honestly my brain is lagging lol"
                        
                    await message.reply(ai_text, mention_author=False)
                except Exception as e:
                    print(f"Gemini Error: {e}")
                    await message.reply("api is trippin fr wait a sec", mention_author=False)

bot.run(TOKEN)
