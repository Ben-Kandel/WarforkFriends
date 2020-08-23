from scraper import Scraper, Server
from friends import FriendsList


def main():
    print("Gathering data from livesow.net/livefork, give me a few seconds...", end="")
    scraper = Scraper()
    server_list = scraper.scrape_servers()
    print("done.")
    print()
    server_list = scraper.clean_server_list(server_list)
    for i, server in enumerate(server_list):
        print(f"#{i+1}: {server}")
        print()
    friends = FriendsList()
    print(f"Your saved friends are: {friends.friends_list}")
    print()
    friends_found = friends.loose_search_servers(server_list)
    for thing in friends_found:
        print(thing)
    


if __name__ == "__main__":
    main()