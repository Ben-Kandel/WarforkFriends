from string import punctuation
import csv

class FriendMatch:

    def __init__(self, server_name, friend_name, other_name=""):
        self.server_name = server_name
        self.friend_name = friend_name
        self.other_name = other_name

    def __str__(self):
        if self.other_name:
            return f"I found {self.friend_name} playing on {self.server_name}, using the alias {self.other_name}."
        else:
            return f"I found {self.friend_name} playing on {self.server_name}."

class FriendsList:

    def __init__(self):
        self.friends = {}
        with open("friends.csv", "r") as f:
            reader = csv.reader(f)
            next(reader) #skip the header row
            for row in reader:
                if not row: continue #get rid of empty rows
                name = row[0]
                aliases = row[1::]
                self.friends[name] = aliases

    def print_friends(self):
        for k,v in self.friends.items():
            print(f"Name: {k}, Aliases: {v}")

    def save_friends(self):
        with open("friends.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Name", "Aliases"])
        for k,v in self.friends.items():
                writer.writerow([k] + v)

    def tight_search(self, server_list):
        matches = []
        for server in server_list:
            if server.player_list: #if the player list isn't empty
                for k,v in self.friends.items():
                    if k in server.player_list: #check if real name is in
                        matches.append(FriendMatch(server.name, k))
                    else:
                        for alias in v:
                            if alias in server.player_list:
                                matches.append(FriendMatch(server.name, k, other_name=alias))
                                break #dont need to check the rest of the aliases
        return matches


if __name__ == "__main__":
    friends = FriendsList()
    friends.print_friends()
