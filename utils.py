import random
import typing
import json
from dataclasses import dataclass

class Bear(object):
    """

    generates chance of bear being in the room, and weather the bear wants to eat them or not!

    """
    def __init__(self):
        self.feelings = {'good': ["pitty", "sad", "bad", "merciful"], 'bad': ['hungry', 'angry', 'lonely', 'happy', 'over the moon', 'aggravated']}

    def feeling(self, *, Force: str = None, fmt_with: bool = True) -> list[str, bool]:
        keys = random.choice(list(self.feelings.keys()))
        if Force:
            if fmt_with == False:
                return random.choice(self.feelings[Force]) # will be on me to choose wording
            else:
                if Force == "good":
                    return f"the bear felt {random.choice(self.feelings[Force])} for you and left!\nLucky You!"
                else:
                    return f"the bear felt {random.choice(self.feelings[Force])} when they saw you...\nYou died!"

        if keys == "good":
            fmt = f"the bear felt {random.choice(self.feelings[keys])} for you and left!\nLucky You!"
            return [fmt, True] #True means their alive so we can reference later when we need to take away a life or add a point.
        else:
            fmt = f"the bear felt {random.choice(self.feelings[keys])} when they saw you...\nYou died!"
            return [fmt, False] #False to show they have died.

    def generate(self) -> bool: #generates the chance of the bear being in the room or not, if they are in the room we call self.feeling which will determine what the bear will do.
        chance = random.randint(1, 100)
        if chance >= 50:
            return True
        else:
            return False


@dataclass
class UserData(object):
    username: str
    highscore: int = 0
    gold_score: int = 0


class UserUtils(object):
    def encrypt(self, words: str) -> str: #would not recommend using this, please use hashes instead! 
        seqeven = [words[x] for x in range(len(words)) if x % 2 == 0]
        seqodd = [words[x] for x in range(len(words)) if x % 2 != 0]
        return f"{''.join(seqodd)}{''.join(seqeven)}"


    def decrypt(self, words: str) -> str:
        midpoint = int(len(words) / 2)
        even = True if len(words) % 2 == 0 else False
        first_half, second_half = words[midpoint:], words[:midpoint]
        res = ""
        for x in range(midpoint):
            res += first_half[x]
            res += second_half[x]
        if even == False:
            res += first_half[midpoint:]
        return res
    
    def create(self) -> typing.Union[None, UserData]:
        with open('profiles.json', 'r+') as f:
            data = json.load(f)
        
        print("Type \"exit\" at any point to exit!")
        
        while True:
            username = input("enter a username: ")
            if username in data.keys():
                print("Invalid: Username Taken!")
            else:
                break
        
        if username.lower() == "exit":
            print("exiting...")
            return 
        
        while True:
            #password should have 1 digit, 1 uppercase, 1 lower case and be a length of 8, and cannot contain the username!
            password = input("enter your password: ")
            if password.lower() == "exit":
                print("exiting...")
                return
            if len(password) < 8:
                print("Your password must be a length of 8 characters or more!")
                continue
            if username in password:
                print("Your username cannot be in your password!")
                continue
            flags = [False, False, False] #should be True True True, order being digit check, uppercase check and lowercase check
            for chr in password:
                if all(flags):
                    break
                if chr.isdigit() == True:
                    flags[0] = True
                if chr.isupper():
                    flags[1] = True
                if chr.islower():
                    flags[2] = True
            if not all(flags):
                print("Your password is missing the following criteria:")
                for index, val in enumerate(flags):
                    if val == False:
                        if index == 0:
                            print("\tpassword must have at least one digit!")
                        elif index == 1:
                            print("\tpassword must have at least one uppercase!")
                        elif index == 2:
                            print("\tpassword must have at least one lowercase!")
            else:
                password = self.encrypt(password)
                with open('profiles.json', 'r+') as f:
                    data[username] = {}
                    data[username]['pwd'] = password
                    data[username]['highscore'] = 0
                    data[username]['goldscore'] = 0
                    json.dump(data, f)
                print("account created!")
                return UserData(username)
    
    def login(self) -> typing.Union[None, UserData]:
        with open('profiles.json', 'r+') as f:
            data = json.load(f)
        
        print("Type \"exit\" at any point to exit!")

        while True:
            username = input("enter a username: ")
            if username.lower() == "exit":
                print("exiting...")
                return
            if username in data.keys():
                userdata = data.get(username, {})
                if userdata == {}:
                    print("Invalid Username or Password!")
                    continue
                else:
                    break
            else:
                input("enter your password: ") #throwoff!
                print("Invalid Username or Password!")
        
        while True:
            password = input("enter your password: ")
            if password.lower() == "exit":
                print("exiting...")
                return
            if len(password) < 8:
                print("Invalid Username or Password!")
                continue
            pwd = userdata['pwd']
            if password == self.decrypt(pwd):
                print("Logged In Successfully!")
                return UserData(username, highscore=userdata['highscore'], gold_score = userdata['goldscore'])
            else:
                print("Invalid Username or Password!")