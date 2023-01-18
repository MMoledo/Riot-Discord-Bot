import requests
import json
import senha
api_key = senha.api_key
class LOL:
    def __init__(self,puid,wins,loses):
        self.puid = puid
        self.nick = self.get_nick()
        self.last = self.last_match()
        self.matchs = wins+loses
        self.count_win = wins
        self.count_lose = loses
        self.gen_all()
        
    def get_nick(self):
        api_url = "https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/"+self.puid+"?api_key="+api_key
        request = requests.get(api_url)
        request = request.json()
        return request["name"]
        
    def last_match(self):
        api_url = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/"+self.puid+"/ids?start=0&count=20&api_key="+api_key
        request = requests.get(api_url)
        historico = request.json()
        return historico[0]

    def check_last_match(self):
        if self.last != self.last_match():
            self.last = self.last_match()
            self.gen_all()
            return True
        return False
    
    def gen_all(self):
        request = self.gen_json()
        for i in range(0,10):
            if request["info"]["participants"][i]["puuid"] == self.puid:
                self.gamemod = request["info"]["gameMode"]
                self.gameduration = str(int(request["info"]["gameDuration"] // 60))+":"+str(int(request["info"]["gameDuration"] % 60))
                self.champion = request["info"]["participants"][i]["championName"]
                self.penta = request["info"]["participants"][i]["pentaKills"]
                self.totalDamageDealt = request["info"]["participants"][i]["totalDamageDealt"]
                self.kills = request["info"]["participants"][i]["kills"]
                self.death = request["info"]["participants"][i]["deaths"]
                self.assists = request["info"]["participants"][i]["assists"]
                self.matchs = self.matchs+1
                if request["info"]["participants"][i]["win"]:
                    self.win = "Ganhou"
                    self.count_win = self.count_win+1
                else:
                    self.win = "Perdeu"
                    self.count_lose = self.count_lose+1
                self.kda = str(self.kills)+"/"+str(self.death)+"/"+str(self.assists)
                self.win_rate = str(round((self.count_win/self.matchs)*100))+"%"
        
    
    def gen_json(self):
        api_url = "https://americas.api.riotgames.com/lol/match/v5/matches/"+self.last+"?api_key="+api_key
        get = requests.get(api_url)
        return get.json()
    
    def gen_file(self):
        doc = self.gen_json()
        doc = json.dumps(doc,sort_keys=True,indent=2)
        name = self.nick+self.last + ".json"
        file = open(name,"w")
        file.write(doc)
        file.close
    
    def teste(self):
        self.kills = 100000
        
    def __str__(self):
        if self.penta > 0:
            text = """
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=
League Of Legends
{} - {}
{} - {}
Campeao : {} - Causando: {} de dano
KDA : {}/{}/{}
OLOKO DEU PENTA KILL!!!!!
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=
        """.format(self.nick,self.win,self.gamemod,self.gameduration,self.champion,self.totalDamageDealt,self.kills,self.death,self.assists)
        else:
            text = """
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=
League Of Legends
{} - {}
{} - {}
Campeao : {} - Causando: {} de dano
KDA : {}/{}/{}
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=
        """.format(self.nick,self.win,self.gamemod,self.gameduration,self.champion,self.totalDamageDealt,self.kills,self.death,self.assists)
        return text
        