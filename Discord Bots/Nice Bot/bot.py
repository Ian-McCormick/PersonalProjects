#token invite link: https://discord.com/api/oauth2/authorize?client_id=1121309588260659360&permissions=274877922304&scope=bot

import discord, random, asyncio, os
import random
import datetime
from discord.ext import commands, tasks

def run_discord_bot():
    #set permissions
    INTENTS = discord.Intents.default()
    INTENTS.message_content = True
    INTENTS.members = True

    CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    TOKEN_FILE = open(CURRENT_DIRECTORY + "/token.txt")
    TOKEN = TOKEN_FILE.read()
    TOKEN_FILE.close()

    CLIENT = discord.Client(intents=INTENTS)

    @CLIENT.event
    async def on_ready():
        print(f'{CLIENT.user} is now running')
        
    
    
    @CLIENT.event
    async def on_message(message):
        #prevents infinite loops, 
        if message.author == CLIENT.user:
            return
        user = message.author
        user_message = str(message.content)
        channel = str(message.channel)
        if("69" in user_message):
            await message.channel.send(f"<@{int(user.id)}> nice")
        if("nice" in user_message):
            if(random.randint(1,10) == 1):
                await message.channel.send(f"<@{int(user.id)}> 69")
        
    @CLIENT.event
    async def on_message_edit(before, after):
        print(str(after.content))

    CLIENT.run(TOKEN)

run_discord_bot()
