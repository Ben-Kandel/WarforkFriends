from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re

BOT_NAMES = {"NightBot", "dummy_player", "Fraggle", "Biscuit", "Salem", "Butter", "Luke",
"Maddie", "Clover", "Dino", "Wallie", "Tootsie", "Mama", "Scruffy", "Rocky", 
"Marzipan", "Angus", "Brownie", "Nico", "Clara", "Oscar", "Fred", "Pogo", 
"Maggie", "Bridgette", "Missy", "Dyllan"}

def remove_number_suffixes(player_list):
    return [re.sub(r'\([0-9]+\)$', "", x) for x in player_list]

def remove_bots(player_list):
    diff = set(player_list) - BOT_NAMES
    return [o for o in player_list if o in diff] #preserve the original order, for testing purposes.


class Server:
    def __init__(self, name, player_count, player_list, mapgamemode="map - gm"):
        self.name = name
        self.player_count = player_count
        self.player_list = player_list
        mapgamemode = mapgamemode.split("-")
        self.map = mapgamemode[0].strip()
        self.gamemode = mapgamemode[1].strip()

    def __str__(self):
        string = "players"
        if self.player_count == 1: string = "player"
        bot_count = self.get_bot_count()
        if bot_count != 0:
            string2 = "bots"
            if bot_count == 1: string2 = "bot"
            return "{} has {} {} online, with {} {}.".format(self.name, self.player_count-bot_count, string, bot_count, string2)
        else:
            return "{} has {} {} online.".format(self.name, self.player_count, string)        

    def is_only_bots(self):
        cleaned_list = remove_number_suffixes(self.player_list) #get rid of number suffixes first
        if len(remove_bots(cleaned_list)) == 0:
            return True
        return False

    def is_empty(self):
        if self.player_count == 0 or len(self.player_list) == 0:
            return True
        return False

    def get_bot_count(self):
        answer = 0
        cleaned_list = remove_number_suffixes(self.player_list)
        for player in cleaned_list:
            if player in BOT_NAMES:
                answer += 1
        return answer

    def update_player_list(self, new_player_list):
        self.player_count = len(new_player_list)
        self.player_list = new_player_list
        
class Scraper:
    def __init__(self):
        self._session = HTMLSession()
        #self.load_page()
        # self._resp = self._session.get("http://livesow.net/livefork")
        # self._resp.html.render(timeout=0, sleep=8) #wait some time for things to load
        # self._soup = BeautifulSoup(self._resp.html.html, "html.parser")
    
    def load_page(self):
        self._resp = self._session.get("http://livesow.net/livefork")
        self._resp.html.render(timeout=0, sleep=6) #wait some time for things to load
        self._soup = BeautifulSoup(self._resp.html.html, "html.parser")

    def clean_server_list(self, server_list):
        new_list = []
        for server in server_list:
            if server.is_only_bots() or server.is_empty(): continue #skip this server.
            new_list.append(server)
        return new_list

    def scrape_servers(self):
        answer = []
        server_list = self._soup.find_all("section", class_="server")
        for server in server_list:
            serv_name = server.header.h1.a.text
            serv_description = server.find("div", class_="description").text
            serv_clients = server.find("div", class_="clients").text
            serv_clients = int(serv_clients[0:serv_clients.find("/")]) #just get how many players are here
            #now for the players in the teams...
            serv_players = []
            teams = server.find_all("div", class_="team")
            for team in teams:
                table = team.table
                for row in table.find_all("tr")[1:]:
                    player_name = row.find("td").text
                    serv_players.append(player_name)
            
            #now add it to our final list.
            answer.append(Server(serv_name, serv_clients, serv_players, serv_description))
        return answer
