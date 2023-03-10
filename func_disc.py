import discord
from discord import app_commands
import random
import requests
import senha
import os
import time
import asyncio
import pandas as pd
from LOL import LOL
from TFT import TFT

api_key = senha.api_key
client = discord.Client(intents=discord.Intents.all())
channel = client.get_channel(1062498678717284445)

def get_info(nick):
    api_url = "https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/"+nick+"?api_key="+api_key
    request = requests.get(api_url)
    request = request.json()
    return request["name"],request["puuid"],request["summonerLevel"]

def check_nick(nick,x):
    try:
        oficial,puuid,level = get_info(nick)
    except:
        print("Nick nao existente")
        return None,None,None
    tb = pd.read_excel(x)
    linhas = tb.shape[0]
    achei = False
    
    for i in range(0,linhas):
        if tb["Nick"][i] == oficial:
            achei = True

    if not achei:
        print(f"Adicionando - {oficial}")
        tb.loc[linhas] = [oficial,puuid,0,0]

    tb.to_excel(x,index=False)
    return oficial,level,achei

async def read_LOL(x):
    tb = pd.read_excel(x)
    linhas = tb.shape[0]
    listagem = []
    for i in range(0,linhas):
        print("Consegui")
        adicionando = LOL(tb.Puuid[i],tb.Wins[i],tb.Loses[i])

        listagem.append(adicionando)
        await asyncio.sleep(0.5)
    return listagem

"""
async def read_TFT():
    tb = pd.read_excel("testando_TFT.xlsx")
    linhas = tb.shape[0]
    listagem = []
    for i in range(0,linhas):
        print("Consegui")
        adicionando = TFT(tb.Puuid[i])
        listagem.append(adicionando)
        await asyncio.sleep(1)
    return listagem
"""

async def loop(channel,listagem_LOL):

    """
    for tft in listagem_TFT:
        try:
            print(tft.nick)
            if tft.check_last_match_TFT():
                embed = printa_tft(tft)
                await channel.send(embed=embed)
                print("Printei:",tft)
        except Exception as error:
            print("NAO CONSEGUI TFT")
            print("Erro Apresentado:\n"+str(error)+"\n"+repr(error))
            return False
        await asyncio.sleep(1)
    """

    for lol in listagem_LOL:
        try:
            print(lol.nick)
            if lol.check_last_match():
                embed = printa_lol(lol)
                await channel.send(embed=embed)
                print("Printei:",lol)
        except Exception as error:
            print("NAO CONSEGUI LOL")
            print("Erro Apresentado:\n"+str(error)+"\n"+repr(error))
            return False
        await asyncio.sleep(1)
    await asyncio.sleep(5)
    print("| Resetando... |")
    return True

def printa_tft(account):
    embed = discord.Embed(
        title = "Teamfight Tactics",
        colour = discord.Colour.dark_purple(),
        type="rich"
    )
    embed.set_author(name="O Espectador",icon_url="https://static.wikia.nocookie.net/leagueoflegends/images/6/60/Reckoning_TFT_set_icon.png/revision/latest?cb=20210430004941")
    embed.set_image(url="https://cdnportal.mobalytics.gg/production/2022/11/58fe35e6-tft_set822_art_keyart-nologo_3840x2160_final_v005.jpg")
    embed.set_thumbnail(url="https://static.wikia.nocookie.net/leagueoflegends/images/8/83/Teamfight_Tactics_2019_hover_icon.png/revision/latest/scale-to-width-down/250?cb=20190612160130")
    embed.add_field(name="Nick:",value=account.nick,inline=False)
    embed.add_field(name="Modo de Jogo",value=account.tft_game_type,inline=True)
    embed.add_field(name="Dura????o",value=account.game_length)
    embed.add_field(name="Posi????o",value=account.placement,inline=True)
    embed.add_field(name="Level",value=account.level)
    embed.add_field(name="Elimina????es",value=account.players_eliminated)
    return embed

def printa_lol(account):
    embed = discord.Embed(
        title = "League Of Legends",
        colour = discord.Colour.dark_blue()
    )
    if account.penta == 0:
        embed.set_author(name="O Espectador",icon_url="https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/f/f6/Worlds_2014.png/revision/latest?cb=20190910232343")
        embed.set_image(url="https://files.tecnoblog.net/wp-content/uploads/2021/08/league-of-legends.jpg")
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/1200px-LoL_icon.svg.png")
        embed.add_field(name="Nick:",value=account.nick)
        embed.add_field(name="Resultado",value=account.win)
        embed.add_field(name="Campe??o",value=account.champion)
        embed.add_field(name="Modo De Jogo",value=account.gamemod)
        embed.add_field(name="Dura????o",value=account.gameduration)
        embed.add_field(name="Win Rate",value=account.win_rate)
        embed.add_field(name="Kills",value=account.kills)
        embed.add_field(name="Deaths",value=account.death)
        embed.add_field(name="Assists",value=account.assists)
    else:
        embed.set_author(name="O Espectador",icon_url="https://static.wikia.nocookie.net/lolesports_gamepedia_en/images/f/f6/Worlds_2014.png/revision/latest?cb=20190910232343")
        embed.set_image(url="https://files.tecnoblog.net/wp-content/uploads/2021/08/league-of-legends.jpg")
        embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/LoL_icon.svg/1200px-LoL_icon.svg.png")
        embed.add_field(name="Nick:",value=account.nick)
        embed.add_field(name="Resultado",value=account.win)
        embed.add_field(name="Campe??o",value=account.champion)
        embed.add_field(name="Modo De Jogo",value=account.gamemod)
        embed.add_field(name="Dura????o",value=account.gameduration)
        embed.add_field(name="Win Rate",value=account.win_rate)
        embed.add_field(name="Kills",value=account.kills)
        embed.add_field(name="Deaths",value=account.death)
        embed.add_field(name="Assists",value=account.assists)
        embed.set_footer(text="KRLLL DEU PENTA KILL !!!!!!")
    return embed

""""def gen_axt(x):

    listagem_TFT = read_TFT()

    listagem_LOL = read_LOL(x)
    i = random.randint(1,1000)
    name = "listagem"+str(i)+".py"
    file = open(name,"w")

    file.write("from TFT import TFT\n")

    file.write("from LOL import LOL\n")
    listagem_lol = []

    listagem_tft = []

    for pessoa in listagem_LOL:
        nick = pessoa.nick
        nick = nick.replace(" ","")
        nick = nick.lower()
        nick_lol = nick
        nick_lol = nick_lol+"_LOL"

        nick = nick+"_TFT"
        listagem_tft.append(nick_lol)
 
        file.write(nick_lol+" = LOL(""'"+pessoa.puid+"'"+","+str(pessoa.count_win)+","+str(pessoa.count_lose)+")\n")

        listagem_lol.append(nick)

        file.write(nick+" = TFT(""'"+pessoa.puid+"'"")\n")

    
    file.write("listagem1 = [")
    count = 0
    for i in listagem_lol:
        tamanho = len(listagem_lol)
        file.write(i)
        if count < tamanho-1:
            file.write(",")
        count = count+1
    file.write("]\n")
    file.write("listagem2 = [")
    count = 0
    print(listagem_lol)
    for i in listagem_tft:
        tamanho = len(listagem_tft)
        file.write(i)
        if count < tamanho-1:
            file.write(",")
        count = count+1
    file.write("]\n")
    print(listagem_tft)
    file.close()
    if os.path.exists("listagem.py"):
        os.remove("listagem.py")
    else:
        print("The file does not exist - 1")
    if os.path.exists(name):
        os.rename(name, "listagem.py")
    else:
        print("The file does not exist - 2")"""