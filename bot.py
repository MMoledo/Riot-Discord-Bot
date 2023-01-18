import discord
from func_disc import *
from TFT import TFT
from senha_discord import senha
from LOL import LOL
import asyncio
from listagem import *

print("Ligando...")

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    channel = client.get_channel(1062498678717284445)
    
    #Confirmacao que esta funcionando
    print("Liguei!")
    await channel.send("Liguei!")
    
    #Loop de Historico
    Error = True
    while Error:
        Error = await loop(channel) 
        
    print("Sai Da Execucao, gerando data...")
    gen_axt()
    
client.run(senha)