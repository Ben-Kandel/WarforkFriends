from scraper import Scraper, Server
from friends import FriendsList
import PySimpleGUI as sg

""" remember, im making a gui. theres a main window, and a server list window.
to do list: make sure we can do html.render() again in scraper.py, we want to reload the server list easily.
make a friends window so we can modify our friends list like that
i want the server list window to have inputs to search for a friends name or something like that """

def make_main_win():
    layout = [[sg.Text("Warfork Server List and Friend Finder")], 
    [sg.Button("Fetch", key="FETCH_SERVERS")]]
    return sg.Window("WarforkFriends", layout, finalize=True, location=(800,400), size=(300,100))

def make_server_win(server_list):

    def should_hide_vertical_scroll(data):
        if len(data) > 15:
            return False
        return True

    data = []
    #crashes when there are no players online btw.
    if server_list:
        for server in server_list:
            data.append([server.name, server.map, server.gamemode, server.player_list])
    else:
        data = ["There are no players online Warfork.", "None", "None", "None"]
    header = ["Server Name", "Map", "Gamemode", "Players"]
    tbl = sg.Table(values=data, headings=header, k="ServerList",
                   row_height=25,
                   auto_size_columns=True,
                   background_color="light blue",
                   header_background_color="light blue",
                   text_color="black",
                   selected_row_colors="black on green",
                   num_rows=len(data),
                   hide_vertical_scroll=should_hide_vertical_scroll(data))
    layout = [[sg.Text("Here is what I found...")],
              [tbl],
              [sg.Text("Servers with friends in them are highlighted in green.", key="FRIEND_STATUS")]]
    return sg.Window("Server List", layout, finalize=True, size=(600,500))

def main():
    main_win = make_main_win()
    server_win = None
    scraper = Scraper()
    friends_list = FriendsList()
    server_list = []
    while True:
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event == "Exit":
            window.close()
            if window == server_win: #if closing the second window,
                server_win = None
            elif window == main_win: #if closing the main window,
                break #close everything
        elif event == "FETCH_SERVERS":

            def get_friend_rows(loose, tight):
                if loose: #if there were any matches,
                    return [x.index for x in loose]
                elif tight:
                    return [x.index for x in tight]
                else:
                    return None #don't select any rows.

            scraper.load_page()
            server_list = get_servers(scraper)
            server_win = make_server_win(server_list)
            
            loose_matches = friends_list.loose_search(server_list)
            tight_matches = friends_list.tight_search(server_list)
            indices = get_friend_rows(loose_matches, tight_matches)
            server_win["ServerList"].Update(select_rows=indices) #update the table
            if indices:
                server_win["FRIEND_STATUS"].Update(value="Servers with friends in them are highlighted in green.")
            else:
                server_win["FRIEND_STATUS"].Update(value="There are no friends online.")
        else:
            print("Event not recognized.")

    main_win.close()


def print_servers(server_list):
    if server_list:
        for i, server in enumerate(server_list):
            print(f"#{i+1}: {server}")
            print()
    else:
        print("There are no players online Warfork.")

def get_servers(scraper):
    return scraper.clean_server_list(scraper.scrape_servers())


if __name__ == "__main__":
    main()