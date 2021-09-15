#run script from virtual env everytime

from kivy.app import App
from kivy.lang import Builder #allows to connect the python file with the kv file
from kivy.uix.screenmanager import ScreenManager , Screen
from hoverable import HoverBehavior
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
import json, glob
from datetime import datetime
from pathlib import Path
import random
import os





Builder.load_file('design.kv')

#added this so paths can be used dynamically, such as running on someone elses computer
json_file = 'users.json'
quote_files = 'Quotes\\'
fileDir = os.path.dirname(os.path.realpath('__file__'))
json_path = os.path.join(fileDir, json_file)
quote_path = os.path.join(fileDir, quote_files)

#making classes for the different screens in the kv file, 
#also have to have the same exact name as they are in the kv file
class LoginScreen(Screen):#inherits the Screen class that makes a Screen object
    def sign_up(self):
        self.manager.current = "sign_up_screen"# name given to signup screen in kv file, this function is performed when pressing the sign up button on the login page
        #manager is a property of the screen class, and current is a method of manager 
    
    def forgot_pword(self):
        self.manager.current = "forgot_password_screen"



    def login(self,uname,pword):
        with open(json_path) as file:
            users = json.load(file)
        if uname in users and users[uname]['password'] == pword:#if the user and password are both in the users dictionary, then change the screen to the enlighten me app screen
            self.manager.current = "login_screen_success"
        else:
           self.ids.login_wrong.text = "Wrong Username or Password" #accessing the id attribute of the label in the login screen page
           #if the user entered the wrong credentials, then we set the text of the label equal to what we assigned it
            

#any actions that we want to do in the sign up screen will use the methods defined in this class
class SignUpScreen(Screen):#made a class because an error occured saying that there was no existing class SignupScreen in eithe the kv file or main.py
    def add_user(self,uname,pword):#added username and password parameters that get username and password values from the sign up page by using the ids in the kv file
        with open(json_path) as file:
            users = json.load(file)#users is a dictionary
        
        users[uname] = {'username':uname,'password':pword,
                        'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}#This sets the username that the user entered as a key in the users dictionary with a value of a dictionary that contains the username, password, and the date that the username and password was created
        
        with open(json_path,'w') as file:
            json.dump(users,file)#writing onto a new json file the updated users dictionary that contains the current users
        self.manager.current = "sign_up_screen_success"#after storing the user's username and password in the json file, 
        #we want to direct them to a sign up success page when they clicked on the"click to sign up" button

class SignUpScreenSuccess(Screen):
    def back_to_login(self):
        
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"#directs user back to login screen
class ForgotPasswordScreen(Screen):
    def check_user(self,uname):
        global confirmed_user
        with open(json_path) as file:
            users = json.load(file)
        if uname in users:
            confirmed_user = uname
            self.manager.current = "new_password_screen"
        else:
            self.ids.no_user_id.text = "User not found, perhaps you dont have an account with us"


class NewPasswordScreen(Screen):
    def store_new_pword(self,pword):
        with open(json_path) as file:
            users = json.load(file)
        users.pop(confirmed_user, None)#deleting previous password so we can store user's new password

        users[confirmed_user] = {'username':confirmed_user,'password':pword,
                        'created':datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

        with open(json_path,'w') as file:
            json.dump(users, file)
        self.manager.current = "login_screen"
        

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = 'right'
        self.manager.current = "login_screen"
    def get_quote(self,feel):
        feel = feel.lower()#if the user enters a feeling in uppercase, it will always change it to lower case
        available_feelings = glob.glob(quote_path + "*txt")#getting the feeling txt files using the glob module
        

        #from the stem propery of the pathlib module, were going to get the name of each text file from quotes, which were stored in the available feelings variable
        available_feelings = [Path(filename).stem for filename in      #available_feelings is a list of files
                                 available_feelings]                   #place the stem outside parentheses so it wont read it as a string and throw an error
        
        if feel in available_feelings:
            with open(f"{quote_path}{feel}.txt",encoding="utf8") as file:# if the feeling the user entered is in available feelings, then open the file with the corresponding feeling
                quotes = file.readlines()#storing the quotes for the user's feeling
            self.ids.quote.text = random.choice(quotes)#choosing a random quote to display for the user, we reffered to the id of the label where we want to display the quote
        else:
            self.ids.quote.text = "Try another feeling"
        
class ImageButton(ButtonBehavior, HoverBehavior, Image):#not putting them in this order would make the logout button not function
    pass


class RootWidget(ScreenManager):
    pass


class MainApp(App):#inherits the app class and makes an app object
    def build(self):#build method comes from the App class
        return RootWidget()

if __name__ == "__main__":#if our python script's name is equal to main when we run it, which it is
    MainApp().run()#Main app class inherited the App class, so it can use the run method
    





