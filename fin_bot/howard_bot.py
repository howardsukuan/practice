#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import discord
from intern_finbot import Result as finchatbot

DISCORD_TOKEN=""
DISCORD_GUILD=""
BOT_NAME = ""

# Documention
# https://discordpy.readthedocs.io/en/latest/api.html#client

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == DISCORD_GUILD:
            break
    print(f'{BOT_NAME}bot has connected to Discord!')
    print(f'{guild.name}(id:{guild.id})')

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@client.event
async def on_message(message):
    if "<@!{}>".format(client.user.id) in message.content:
        if message.author == client.user:
            return() 
        print("message.content", message.content)
        
        if "hi!" in message.content:
            response = "我知道這很辛苦但你要加油"
            await message.channel.send(response)
    
        if 'test' in message.content:
            response = "Send message."
            await message.channel.send(response)
        
        else:
            msgSTR = message.content.replace("<@!{}> ".format(client.user.id), "")
            response = finchatbot(msgSTR)
            await message.channel.send(response)
            
        
    elif "bot 點名" in message.content:
        response = "有!"
        await message.channel.send(response)
    


client.run(DISCORD_TOKEN)
