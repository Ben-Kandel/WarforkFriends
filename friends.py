from string import punctuation

class FriendMatch:

    def __init__(self, server_name, friend_name):
        self.server_name = server_name
        self.friend_name = friend_name

    def __str__(self):
        return "I found {} playing on {}".format(self.friend_name, self.server_name)


class FriendsList:
    
    def __init__(self):
        f = open("friends.txt", "r")
        if f:
            self.friends_list = [x.rstrip() for x in f.readlines()]
        else:
            self.friends_list = []
        f.close()

    def save_friends(self):
        print("writing this to file: {}".format(self.friends_list))
        f = open("friends.txt", "w")
        for friend in self.friends_list:
            f.write("{}\n".format(friend))
        f.close()

    def loose_search_servers(self, server_list):
        answer = []
        for server in server_list:
            for friend in self.friends_list:
                lowered_friend = friend.lower()
                new_player_list = [x.translate(x.maketrans('', '', punctuation)).lower() for x in server.player_list]
                if lowered_friend in new_player_list:
                    answer.append(FriendMatch(server.name, friend))
        return answer

    def search_servers(self, server_list):
        answer = []
        for server in server_list:
            for friend in self.friends_list:
                if friend in server.player_list:
                    answer.append(FriendMatch(server.name, friend))
        return answer

    def remove_friend(self, friend_name):
        try:
            self.friends_list.remove(friend_name)
        except ValueError:
            # print("{} isn't in your friends list.".format(friend_name))
            pass

    def add_friend(self, friend_name):
        if friend_name in self.friends_list:
            # print("{} is already in your friends list!".format(friend_name))
            pass
        else:
            self.friends_list.append(friend_name)

    def add_friends(self, friends_list):
        for friend in friends_list:
            self.add_friend(friend) #just use the other function

if __name__ == "__main__":
    fl = FriendsList()
    print(fl.friends_list)