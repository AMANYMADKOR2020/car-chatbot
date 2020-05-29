import re
import random
from carbot.brain import Carbot
from carbot.utils import *

confirmation_regex = re.compile(r"\byes\b|yup|right|correct|ok[ay]?")
rejection_regex = re.compile(r"\bno\b|nope|\bnah\b")


class Bot:

    def __init__(self, retrain=False, deep_learning=True):
        self.__user_state = self.__new_user_state()
        self.__brain = Carbot(retrain, deep_learning)


    def __new_user_state(self):
        return {
            "prev_state": None,
            "cur_state": "greetings",
            "car_name": None,
            "intent": None,
            "pending": False
        }


    def __reset_user_state(self):
        self.__user_state['pending'] = False
        self.__user_state['car_name'] = False
        self.__user_state['intent'] = False
        self.__user_state['prev_state'] = self.__user_state['cur_state']
        self.__user_state['cur_state'] = "greetings"


    def __handle_user(self, user_input):
        # check if the prev_state is None 
        intent = self.__brain.intent_prediction(user_input)
        car_name = self.__brain.get_car(user_input)
        if  car_name:
            self.__user_state['car_name']=car_name
        if not self.__user_state['prev_state']:
            self.__user_state['prev_state'] = "greetings"
            self.__user_state['cur_state'] = "greetings"
            return random.choice(response_bank['greetings'])
        # analyze the user input
        if self.__user_state['pending']:
            # user is pending either on car   or reservation
            if self.__user_state['car_name'] and self.__user_state['intent']=="reserve_enq": # the user is pending on reservation
                confirmation = confirmation_regex.findall(user_input)
                if len(confirmation):
                    response = self.__intent_executer("registered", self.__user_state['car_name'])
                else:
                    response = "okay canceled"
                self.__reset_user_state()
                return response
            elif self.__user_state['intent']: # the user is pending on the car_name
                #car_name = self.__brain.get_car(user_input)
                if not self.__user_state['car_name']:
                    self.__reset_user_state()
                    return random.choice(response_bank['unknown'])
                else:
                    response = self.__intent_executer(self.__user_state['intent'], self.__user_state['car_name'])
                   # self.__reset_user_state()#amany
                    return response
        # extract intent and car_name from the user input
        
        #car_name = self.__brain.get_car(user_input)#amany
        if intent in ['greetings', "thanks"]:
            # if the user was doing something, then say thanks
            if self.__user_state['cur_state'] not in ['greetings', 'thanks']:
                self.__user_state['prev_state'] = self.__user_state['cur_state']
                self.__user_state['cur_state'] = 'thanks'
                response = self.__intent_executer("thanks", self.__user_state['car_name'])
            else:
                # else just say hi
                self.__user_state['prev_state'] = intent
                response = self.__intent_executer(intent, self.__user_state['car_name'])
        if intent in ['availability_enq','cost_enq', 'color_enq','reserve_enq', 'options_enq']:
            # the user want to ask about something
            if not self.__user_state['car_name']:
                self.__user_state['prev_state'] = self.__user_state['cur_state']
                self.__user_state['cur_state'] = intent
                self.__user_state['intent'] = intent
                self.__user_state['pending'] = True
                response = "what is your prefered car model ?"
            else:
                self.__user_state['prev_state'] = self.__user_state['cur_state']
                self.__user_state['cur_state'] = intent
                self.__user_state['intent'] = intent
                if intent == "reserve_enq":
                    self.__user_state["pending"] = True
                    #self.__user_state['car_name'] = car_name
                    response = self.__intent_executer(intent, self.__user_state['car_name'])
                else:
                    response = self.__intent_executer(intent, self.__user_state['car_name'])
        return response

    def __intent_executer(self, intent, car_name):
        # now check the intent
        if intent in ["greetings", "thanks"]:
            return random.choice(response_bank[intent])
        else:
            response = random.choice(response_bank[intent])
            # get car info
            car_data = get_car_data(car_name)
            
            response = response.format(car_name=car_name, 
                                       start_date=car_data['start_date'],
                                       price=car_data['price'],
                                       color=car_data['color'],
                                       options=car_data['options'])
            if intent == "registered":
                # increase the registered users
                register_user(car_name)
            return response
    
    def run_blocking(self):
        """
        run the chatbot in the terminal
        """
        user_utterance = ""
        while True:
            response = self.__handle_user(user_utterance)
            print("bot :", response)
            user_utterance = input("user: ")
    
    def user_interaction(self, user_msg, user_state=None):
        if user_state:
            self.__user_state = user_state
        else:
            self.__reset_user_state()
        return self.__handle_user(user_msg), self.__user_state 

        
    