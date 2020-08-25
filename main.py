from scraper import Scraper, Server
from friends import FriendsList


def main():
    print("Gathering data from livesow.net/livefork, give me a few seconds...", end="")
    scraper = Scraper()
    server_list = scraper.scrape_servers()
    print("done.")
    print()
    server_list = scraper.clean_server_list(server_list)
    if server_list:
        for i, server in enumerate(server_list):
            print(f"#{i+1}: {server}")
            print()
    else:
        print("There are no players online Warfork.")
        return
    friends = FriendsList()
    matches = friends.tight_search(server_list)
    for match in matches:
        print(match)

if __name__ == "__main__":
    main()