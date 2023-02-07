import requests
import json
import senha
import time
api_key = senha.api_key
class TFT:
    def __init__(self,puid):
        start_time = time.time()
        self.puid = puid
        self.nick = self.get_nick()
        self.last = self.last_match()
        self.gen_all()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print("Tempo de execução:", elapsed_time, "segundos")
        print("Gerei {} TFT".format(self.nick))

    def gen_all(self):
        request = self.gen_json()
        for i in range(0,8):
            if request["info"]["participants"][i]["puuid"] == self.puid:
                self.tft_game_type = request["info"]["tft_game_type"]
                self.placement = request["info"]["participants"][i]["placement"]
                if self.tft_game_type == "pairs":
                    if self.placement == 1 or self.placement == 2:
                        self.placement = 1
                    elif self.placement == 3 or self.placement == 4:
                        self.placement = 2
                    elif self.placement == 5 or self.placement == 6:
                        self.placement = 3
                    else:
                        self.placement = 4
                self.level = request["info"]["participants"][i]["level"]
                self.players_eliminated = request["info"]["participants"][i]["players_eliminated"]

                self.game_length = str(int(request["info"]["game_length"] // 60))+":"+str(int(request["info"]["game_length"] % 60))
        
    def get_nick(self):
        api_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-puuid/"+self.puid+"?api_key="+api_key
        request = requests.get(api_url)
        request = request.json()
        return request["gameName"]
        
    def last_match(self):
        api_url = "https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/"+self.puid+"/ids?start=0&count=20&api_key="+api_key
        request = requests.get(api_url)
        historico = request.json()
        return historico[0]

    def check_last_match_TFT(self):
        if self.last != self.last_match():
            self.last = self.last_match()
            self.gen_all()
            return True
        return False
    
    def gen_json(self):
        api_url = "https://americas.api.riotgames.com/tft/match/v1/matches/"+self.last+"?api_key="+api_key
        get = requests.get(api_url)
        return get.json()
    
    def gen_file(self):
        doc = self.gen_json()
        doc = json.dumps(doc,sort_keys=True,indent=2)
        name = self.nick+self.last + ".json"
        file = open(name,"w")
        file.write(doc)
        file.close
    
    def print_test(self):
        print(self.gen_json())
        
    def __str__(self):
        if self.tft_game_type == "pairs":
            if self.placement == 1 or self.placement == 2:
                aux = 1
            elif self.placement == 3 or self.placement == 4:
                aux = 2
            elif self.placement == 5 or self.placement == 6:
                aux = 3
            else:
                aux = 4
            text = """
Modo de jogo: Duplas
Posicao: {}
Level: {}
Eliminacoes: {}
        """.format(self.nick,aux,self.level,self.players_eliminated)
        else:
            text = """
Modo de jogo: Normal
Posicao: {}
Level: {}
Eliminacoes: {}
        """.format(self.nick,self.placement,self.level,self.players_eliminated)
        return text
        