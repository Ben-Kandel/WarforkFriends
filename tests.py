import unittest
import scraper
import friends
from bs4 import BeautifulSoup

class TestProject(unittest.TestCase):

    def test_remove_suffixes(self):
        new_list = scraper.remove_number_suffixes([])
        self.assertEqual(new_list, []) #check empty list
        new_list = scraper.remove_number_suffixes(["Player1", "Player2"])
        self.assertEqual(new_list, ["Player1", "Player2"]) #check with numbers not enclosed in ()
        new_list = scraper.remove_number_suffixes(["Player(1)", "Player(2)"])
        self.assertEqual(new_list, ["Player", "Player"])
        new_list = scraper.remove_number_suffixes(["Pla(1)yer"])
        self.assertEqual(new_list, ["Pla(1)yer"]) #check with numbers enclosed in () not at the end
        new_list = scraper.remove_number_suffixes(["Player(123123)", "P1ay3r(4)"])
        self.assertEqual(new_list, ["Player", "P1ay3r"]) #check with multiple numbers in ()
        new_list = scraper.remove_number_suffixes(["Minionsman", "slice", "farmz0r", "tintifax"])
        self.assertEqual(new_list, ["Minionsman", "slice", "farmz0r", "tintifax"]) #just check regular names

    def test_remove_bots(self):
        test_list = scraper.remove_bots([])
        self.assertTrue(len(test_list) == 0) #check empty list
        test_list = scraper.remove_bots(["Wallie", "Dino"])
        self.assertEqual(test_list, []) #check with two bots
        test_list = scraper.remove_bots(["Player", "Scruffy", "Player2", "Mama"])
        self.assertEqual(test_list, ["Player", "Player2"]) #check with bots and players
        test_list = scraper.remove_bots(["Dino(1)", "Mama"])
        self.assertEqual(test_list, ["Dino(1)"]) #remove_bots does not recognize number suffixes

    def test_friends(self):
        #testing clean_strings:
        FL = friends.FriendsList("tests/test1.csv")
        data = ["HELLO","hEllO","    Hello   "]
        self.assertEqual(FL.clean_strings(data), ["hello", "hello", "hello"]) #test lower() and strip() part
        data = ["he.llo", "hell||o", "  $he$llo$.#$^"]
        self.assertEqual(FL.clean_strings(data), ["hello", "hello", "hello"]) #test removing punctuation
        data = []
        self.assertEqual(FL.clean_strings(data), []) #check with empty list
        data = ["", "    "]
        self.assertEqual(FL.clean_strings(data), []) #check that pure whitespace strings are removed
        data = ["$$(#$(^"]
        self.assertEqual(FL.clean_strings(data), ["$$(#$(^"]) #check that a pure punctuation name is not reduced to an empty string
        data = ["$$$$$$$", "   he$$$$$$llo dude!", "   "]
        self.assertEqual(FL.clean_strings(data), ["$$$$$$$", "hello dude"]) #does it all work together?

        #testing loading of friends list
        answer = {"Player" : [], "Player1" : [], "Player2" : []}
        self.assertEqual(FL.friends, answer) #testing with no extra aliases in friends
        FL2 = friends.FriendsList("tests/test2.csv")
        answer = {"Player" : ["other_name", "lolol"], "Player1" : [], "Player2" : ["PlayerTwo", "PlayerToo"]}
        self.assertEqual(FL2.friends, answer) #testing with some aliases

        #testing friend search
        # s1 = scraper.Server("Server1", 3, ["Player", "test123", "tESt123"])
        # FL3 = friends.FriendsList("tests/test3.csv")
        # answer = [friends.FriendMatch("Server1", "Player"), friends.FriendMatch("Server1", "Test", "test123")]
        # self.assertEqual(FL3.tight_search([s1]), answer)

    def test_servers(self):
        s1 = scraper.Server("Server1", 0, [])
        self.assertTrue(s1.is_empty()) #check that it is indeed empty
        self.assertTrue(s1.is_only_bots()) #check that it has only bots (technically true)
        s2 = scraper.Server("Server2", 2, ["Player", "Wallie"])
        self.assertFalse(s2.is_only_bots()) #there is a real player, so this should pass
        s3 = scraper.Server("Server3", 2, ["Wallie", "Dino", "Scruffy"])
        self.assertTrue(s3.is_only_bots()) #check only bots
        s4 = scraper.Server("Server4", 3, ["Wallie", "Wallie(2)", "Mama(2323)", "Dino(9)"])
        self.assertTrue(s4.is_only_bots()) #check only bots with number suffixes
        s5 = scraper.Server("Server5", 3, ["Wallie", "Wallie(2)", "Mama(2323)", "Dino(9)", "Player"])
        self.assertFalse(s5.is_only_bots()) #check with one player and bots with number suffixes

    def test_scraper(self):
        
        def assert_things(server, e_name, e_gm, e_map, e_player_list):
            self.assertEqual(server.name, e_name)
            self.assertEqual(server.gamemode, e_gm)
            self.assertEqual(server.map, e_map)
            self.assertEqual(server.player_list, e_player_list)
        
        #this file contains servers in the same layout as livesow.net/livefork
        #this lets us test our scraper with known data to see if it is working
        with open("tests/testservers.html", "r") as f:
            contents = f.read()
            sp = scraper.Scraper()
            sp._soup = BeautifulSoup(contents, "html.parser")
            server_list = sp.scrape_servers()
            #testing that we gathered information correctly:
            assert_things(server_list[0], "Test1", "ffa", "wfdm1", ["Name1", "Name2", "Name3", "Name4", "Name5", "Name6"])
            assert_things(server_list[1], "Test2", "nca", "wfca1", ["NightBot", "Name1", "Name2"])
            assert_things(server_list[2], "Test3", "ffa", "wfdm11", ["Maddie", "Oscar", "Dyllan", "Mama", "Biscuit", "Mama(1)"])
            #testing bot-related things:
            self.assertFalse(server_list[0].is_only_bots())
            self.assertFalse(server_list[1].is_only_bots())
            self.assertTrue(server_list[2].is_only_bots())
            self.assertTrue(server_list[0].get_bot_count() == 0)
            self.assertTrue(server_list[1].get_bot_count() == 1)
            self.assertTrue(server_list[2].get_bot_count() == 6)

if __name__ == "__main__":
    unittest.main()