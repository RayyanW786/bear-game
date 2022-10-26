from utils import Bear, UserUtils
import json
from random import shuffle, sample, choice
class Game(object):
    def __init__(self, bear, utils):
        self.bear: Bear = bear()
        self.userutils: UserUtils = utils()
        self.choices = ['the first room had strange noises coming from it, however the second room was pitch black, which room do you go into?', 'room 1 was very very cold, however room 2 had a bad feeling about it, which room do you go into?', 'room 1 seems to be full of food, room 2 contains the worlds best drinks, which room do you go into?', 'room 1 and 2 both have a mirror, in both the mirrors you can see the bear, which room do you go to?']
        self.restart()
        self.first_menu()

    def restart(self):
        self.lives = 3
        self.gold = 0
        self.highscore = 0
        shuffle(self.choices)

    def first_menu(self):
        while True:
            try:
                try:
                    getattr(self, "userdata")
                    user_input = input("\n____________________\n1. Start Game\n2. Log Out\n3. Your Stats\n___________________\nEnter your choice 1-3: ")
                    user_input = int(user_input)
                    if user_input == 1:
                        self.main()
                    elif user_input == 2:
                        delattr(self, "userdata")
                        print("You have been Logged out...")
                    elif user_input == 3:
                        self.get_stats()
                        

                except AttributeError:
                    user_input = input("\n____________________\n1. Register\n2. Log in\n___________________\nEnter your choice 1-2: ")                 
                    user_input = int(user_input)
                    if user_input == 1:
                        self.user_creation()
                    elif user_input == 2:
                        self.login()
                    else:
                        print("Please enter a valid option\nTo quit type quit, exit or stop!")
            except ValueError:
                if str(user_input).lower() in ["quit", "exit", "stop"]:
                    exit()
    
    def user_creation(self):
        res = self.userutils.create()
        if res == None:
            self.first_menu()
        else:
            self.userdata = res
    
    def login(self):
        res = self.userutils.login()
        if res == None:
            self.first_menu()
        else:
            self.userdata = res

    def gen_gold(self) -> True | False:
        if self.highscore >= 50:
            return choice([True, False])
        return False
    
    def get_stats(self):
        with open('profiles.json', 'r+') as f:
            data = json.load(f)
        data = data[self.userdata.username]
        print("________________________________________________________________________________________________")
        print(f"{self.userdata.username}\'s stats")
        print(f"HighScore: {data['highscore']}")
        print(f"GoldScore: {data['goldscore']}")
        print("________________________________________________________________________________________________")

    def main(self):
        run = True
        self.restart()
        while run == True:
            for choice in sample(self.choices, len(self.choices)):
                res = input(f"{choice}\nReply with 1, 2, exit or restart!")
                if res.lower() == "exit":
                    with open('profiles.json', 'r+') as f:
                        fdata = json.load(f)
                        sdata= fdata[self.userdata.username]
                        if self.highscore > sdata['highscore']:
                            fdata[self.userdata.username]['highscore'] = self.highscore
                        fdata[self.userdata.username]['goldscore'] += self.gold
                    with open('profiles.json', 'r+') as f:
                        json.dump(fdata, f)
                    self.first_menu()
                if res.lower() == 'restart':
                    self.restart()
                    run = False
                    self.main()
                    break
                if res not in ['1', '2']:
                    print('invalid option, You died')
                    self.first_menu()
                else:
                    res = self.bear.generate()
                    if res == True:
                        feeling = self.bear.feeling()
                        if feeling[1] == False:
                            print(feeling[0])
                            self.lives -= 1
                            if self.lives <= 0:
                                print("GAME OVER!!!")
                                with open('profiles.json', 'r+') as f:
                                    fdata = json.load(f)
                                    if self.highscore > fdata[self.userdata.username]['highscore']:
                                        fdata[self.userdata.username]['highscore'] = self.highscore
                                    fdata[self.userdata.username]['goldscore'] += self.gold
                                with open("profiles.json", "r+") as f:
                                    json.dump(fdata, f)    
                                run = False
                            
                        else:
                            self.highscore += 10
                            print(feeling[0])

                    else:
                        self.highscore += 10
                        print("Your survived this round!")
                
                print(f"Your current score: {self.highscore:,}\nYou have {self.lives} {'lives' if self.lives > 1 else 'life'} left!\n")
            if run != False:
                res = self.gen_gold()
                if res == True:
                    user_input = input("You have found the Gold, do you want to pick it up? y/n\nPicking it up means you win the Game!")
                    if user_input.lower() == 'y':
                        self.gold += 1
                        with open('profiles.json', 'r+') as f:
                            fdata = json.load(f)
                            if self.highscore > fdata[self.userdata.username]['highscore']:
                                fdata[self.userdata.username]['highscore'] = self.highscore
                            fdata[self.userdata.username]['goldscore'] += self.gold
                        with open("profiles.json", "r+") as f:
                            json.dump(fdata, f)
                        print("GAME ENDED! CONGRATS")
                        run = False 
                    
                

if __name__ == "__main__":
    Game(Bear, UserUtils)