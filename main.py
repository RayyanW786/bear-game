from utils import Bear, UserUtils, UserData
import json
from random import shuffle, sample, choice


class Game(object):
    def __init__(self, bear, utils):
        self.bear: Bear = bear() # creating a instance of bear class within the Game
        self.userutils: UserUtils = utils() # instance of UserUtils Class allows us to login etc
        self.choices = [
            'the first room had strange noises coming from it, however the second room was pitch black, which room do you go into?',
            'room 1 was very very cold, however room 2 had a bad feeling about it, which room do you go into?',
            'room 1 seems to be full of food, room 2 contains the worlds best drinks, which room do you go into?',
            'room 1 and 2 both have a mirror, in both the mirrors you can see the bear, which room do you go to?']
        # choices which the Game will randomize and loop over, its easy to add a level by just adding to this list
        self.restart() #adds thhe variables also we can call reset later on to override the current Game attributes
        self.first_menu() #starts the main login loop

    def restart(self):
        self.lives = 3
        self.gold = 0
        self.highscore = 0
        shuffle(self.choices) #randomizes self.choice

    def first_menu(self): #displays menu and allows users to log in, register or start the game, log out or view stats
        while True:
            try:
                try:
                    getattr(self, "userdata")
                    user_input = input(
                        "\n____________________\n1. Start Game\n2. Log Out\n3. Your Stats\n___________________\nEnter your choice 1-3: ")
                    user_input = int(user_input)
                    if user_input == 1:
                        self.main()
                    elif user_input == 2:
                        delattr(self, "userdata")
                        print("You have been Logged out...")
                    elif user_input == 3:
                        self.get_stats()


                except AttributeError: #getattr raises AttributeError when the Attribute doesnt exist
                    user_input = input(
                        "\n____________________\n1. Register\n2. Log in\n___________________\nEnter your choice 1-2: ")
                    user_input = int(user_input)
                    if user_input == 1:
                        self.user_creation()
                    elif user_input == 2:
                        self.login()
                    else:
                        print("Please enter a valid option\nTo quit type quit, exit or stop!")
            except ValueError: #value error means the program doesnt stop if they input a non integer type
                if str(user_input).lower() in ["quit", "exit", "stop"]:
                    exit()

    def user_creation(self):
        res = self.userutils.create() #calls the create function for more info look at the comment made in utils.py line 74
        if res == None: #None means they typed exit
            self.first_menu() #puts the user back to the orginal menu loop
        else:
            self.userdata = res #sets userdata attr which changes the first menu options to now display start game etc

    def login(self):
        res = self.userutils.login() #calls the login function for more info look at the comment made in utils.py line 135
        if res == None: #user typed exit
            self.first_menu() #puts them back on the orginal loop
        else:
            self.userdata = res #sets userdata attr which changes the first menu options to now display start game etc

    def gen_gold(self) -> True | False:
        if self.highscore >= 50:
            return choice([True, False]) #generates the chance of gold appearing
        return False #we dont need to use else we can simple just return False if the if statement conditions are not met

    def get_stats(self): #displays the stats of the user if they have any
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
        self.restart() #reset the game variables each time they play
        while run == True:
            for choice in sample(self.choices, len(self.choices)): #looping though the choices (randomized)
                res = input(f"{choice}\nReply with 1, 2, exit or restart!")
                if res.lower() == "exit":
                    with open('profiles.json', 'r+') as f: #saving data if they have any
                        fdata = json.load(f)
                        sdata = fdata[self.userdata.username]
                        if self.highscore > sdata['highscore']:
                            fdata[self.userdata.username]['highscore'] = self.highscore
                        fdata[self.userdata.username]['goldscore'] += self.gold
                    with open('profiles.json', 'r+') as f:
                        json.dump(fdata, f)
                    self.first_menu()
                if res.lower() == 'restart': #resets game variables
                    #self.restart() #we dont need this
                    #run = False #same with this calling self.main() is enough
                    self.main() #re calling function
                    #break #the code shouldnt reach this and so this is useless
                if res not in ['1', '2']:
                    print('invalid option, You died') #user dies if they enter an invalid option regardless of lives
                    self.first_menu()
                else:
                    res = self.bear.generate() #generates if the bear is in the room or not
                    if res == True: #True means the bear is infact in the room
                        feeling = self.bear.feeling() #feeling tells us if the bear wants to kill them or not and why
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

                print(
                    f"Your current score: {self.highscore:,}\nYou have {self.lives} {'lives' if self.lives > 1 else 'life'} left!\n")
            if run != False:
                res = self.gen_gold() #generate chance of gold after every loop of self.choices
                if res == True:
                    user_input = input(
                        "You have found the Gold, do you want to pick it up? y/n\nPicking it up means you win the Game!")
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
    Game(Bear, UserUtils) #calling Game and passing Bear and UserUtils class.
