import unittest
import scraper
import friends

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
        pass
        """ fl = friends.FriendsList()
        fl.friends_list.clear()
        fl.add_friend("Minionsman")
        self.assertEqual(fl.friends_list, ["Minionsman"]) #check adding friend
        fl.add_friend("tintifax")
        self.assertEqual(fl.friends_list, ["Minionsman", "tintifax"]) #check adding another friend
        fl.add_friend("Minionsman")
        self.assertEqual(fl.friends_list, ["Minionsman", "tintifax"]) #check adding duplicate
        fl.remove_friend("Minionsman")
        self.assertEqual(fl.friends_list, ["tintifax"]) #check removing friend
        fl.remove_friend("doesn't exist")
        self.assertEqual(fl.friends_list, ["tintifax"]) #check removing a non-existent friend
         """
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

if __name__ == "__main__":
    unittest.main()