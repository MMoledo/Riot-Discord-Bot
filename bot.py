import discord
from func_disc import *
from senha_discord import senha

print("Ligando...")
tabela = "testando_LOL.xlsx"
id_do_servidor = 871544237458595910

class Client(discord.Client):

    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False #Nós usamos isso para o bot não sincronizar os comandos mais de uma vez
        
    @client.event
    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #Checar se os comandos slash foram sincronizados 
            await tree.sync(guild = discord.Object(id=id_do_servidor)) # Você também pode deixar o id do servidor em branco para aplicar em todos servidores, mas isso fará com que demore de 1~24 horas para funcionar.
            self.synced = True

        print(f"Entramos como {self.user}.")
        channel = client.get_channel(978479957418311700)

        #Confirmacao que esta funcionando
        print("Liguei!")
        await channel.send("Liguei!")

        #Loop de Historico
        Error = True
        listagem_LOL = await read_LOL(tabela)
        tb = pd.read_excel(tabela)
        linhas = tb.shape[0]

        while Error:
            tb = pd.read_excel(tabela)
            linhas = tb.shape[0]
            print(linhas)
            print(len(listagem_LOL))
            if linhas > len(listagem_LOL):
                listagem_LOL = await read_LOL(tabela)
            Error = await loop(channel,listagem_LOL) 
            
        print("Sai Da Execucao, gerando data...")

client = Client()
tree = app_commands.CommandTree(client)

@tree.command(guild = discord.Object(id=id_do_servidor), name = 'cadastro', description='Escolhe o nick que deseja cadastrar') #Comando específico para seu servidor
async def Cadastro(interaction: discord.Interaction, nick: str):    
    nome,level,achei = check_nick(nick,tabela)
    if achei == None:
        await interaction.response.send_message(f'**Esse usuário não existe**', ephemeral = True)    
    elif not achei:
        await interaction.response.send_message(f'**Adicionando o {nome} - Level: {level}**', ephemeral = True)
    elif achei:
        await interaction.response.send_message(f'**Usuario: {nome} - Level: {level}, já é cadastrado**', ephemeral = True)
"""
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    channel = client.get_channel(978479957418311700)
    
    #Confirmacao que esta funcionando
    print("Liguei!")
    await channel.send("Liguei!")

    #Loop de Historico
    Error = True
    listagem_LOL = await read_LOL()
    listagem_TFT = await read_TFT()

    while Error:
        Error = await loop(channel,listagem_TFT,listagem_LOL) 
        
    print("Sai Da Execucao, gerando data...")
    gen_axt()
"""
client.run(senha)