from string import punctuation
import csv
import copy

class FriendMatch:

    def __init__(self, server_name, friend_name, server_index, other_name=""):
        self.server_name = server_name
        self.friend_name = friend_name
        self.other_name = other_name
        self.index = server_index
        
    def __str__(self):
        if self.other_name:
            return f"I found {self.friend_name} playing on {self.server_name}, using the alias {self.other_name}."
        else:
            return f"I found {self.friend_name} playing on {self.server_name}."

class FriendsList:

    def __init__(self, filename="friends.csv"):
        self.friends = {}
        with open(filename, "r") as f:
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


    def _search(self, server_list, friend_dict):
        matches = []
        for i,server in enumerate(server_list):
            if server.player_list: #if the player list isn't empty
                for k,v in friend_dict.items():
                    if k in server.player_list:
                        matches.append(FriendMatch(server.name, k, i))
                    else:
                        for alias in v:
                            if alias in server.player_list:
                                matches.append(FriendMatch(server.name, k, i, other_name=alias))
                                break
        return matches

    def tight_search(self, server_list):
        return self._search(server_list, self.friends)
    
    def loose_search(self, server_list):
        #we have clean_strings(), let's use it!
        new_dict = {}
        for k,v in self.friends.items():
            new_dict[k] = self.clean_strings(v)
        return self._search(server_list, new_dict)

    def clean_strings(self, string_list):
        #takes a string, removes leading/trailing whitespace, and removes all punctuation
        answer = []
        for thing in string_list:
            thing = thing.strip()
            if thing: #if there any characters left after doing .strip()
                thing = thing.lower()
                no_punc = thing.translate(thing.maketrans('', '', punctuation))
                if no_punc:
                    answer.append(no_punc)
                else:
                    answer.append(thing)
        return answer

if __name__ == "__main__":
    friends = FriendsList()
    answer = friends.clean_strings(["Hello", " Hello ", "|||Spoo.$#n@@)#*)!@#%&"])
    print(answer)
