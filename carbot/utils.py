from datetime import datetime
import re
import os
import sqlite3

DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cars_db.sqlite")
connection = sqlite3.connect(DATABASE_PATH)

#cars_name_regex = {
#    "CROSSLAND_ELEGANCE": re.compile(r"\bcrossland\b|\bcross\sland\b[elegance|first|first\scategory]"),
#    "GRANDLAND_ELEGANCE": re.compile(r"\bgrandland\b|\bgrand\sland\b[elegance|first|first\scategory]"),
 #   "CROSSLAND_TOP_LINE": re.compile(r"\bcrossland\b|\bcross\sland\b[topline|second|second\scategory]"),
 #   "GRANDLAND_HIGH_LINE":re.compile(r"\bgrandland\b|\bgrand\sland\b[highline|second|second\scategory]")    }
cars_name_regex = {
    "CROSSLAND_ELEGANCE": re.compile(r"(?=.*crossland)(?=.*elegance)"),
    "GRANDLAND_ELEGANCE": re.compile(r"(?=.*grandland)(?=.*elegance)"),
    "CROSSLAND_TOP_LINE": re.compile(r"(?=.*crossland)(?=.*topline)"),
    "GRANDLAND_HIGH_LINE":re.compile(r"(?=.*grandland)(?=.*highline)")    }



# build a bank request to make things fun
response_bank = {
    "greetings": ["hello there!, how can i help?", "Hi i am carbot how can i help?", "Hi iam here for any help! "],
    "thanks": ["Feel free to contact us anytime", "I am happy to help", "More than happy to help"],
    "availability_enq": ["we have {car_name} car available on  {start_date} you are welcome at CAR SHOWROOM", "would like to test drive one at our CAR SHOWROOM?",
                         "{car_name} will be at our CAR SHOWROOM on {start_date} happy to visit us to see the car"],
    "cost_enq": [" {car_name} car will cost only {price}L.E.", "the price for {car_name} is only {price}L.E."],
    "color_enq": ["The available color for {car_name} is {color} ", "{color} color is available for{car_name} car"],
    "reserve_enq": ["Sure, you would like to confirm your booking to {car_name} car?", "Would you please confirm your {car_name} booking?"],
    "options_enq": ["you will find all details aboute options in this link {options} ", "this link {options} will show you all details aboute{car_name}"],
    "unknown": ["i didn't get that sorry", "kindly would you try again, i didn't get this one", "sorry could you try this again"],
    "registered": ["you have booked {car_name} car!, it will be available on {start_date} !!"]
}


examples = [
    # greetings
    "hello there",
    "good morning",
    "welcome",
    "hi!, how are you",
    "Hi there !!",
    
    # thanks
    "thanks",
    "that's it",
    "goodbye",
    "bye",
    "okay",
    
    # cost examples
    "How much is grandland second category?",
    "what is the cost of cross land elegance?",
    "can you tell me the price of grandland highline",
    "what is the price of that car?",
    "how much will i pay for this?",
    
    # color_enq examples
    "what is the available colors?",
    "what colors do you have?",
    "can you tell me the color of grandland high line?",
    "what are the colors in crossland elegance?",
    "which colors?",
    
    # availability examples
    "do you have opel grandland?",
    "i want to know if you have opel models",
    "do you have the second category of opel grand land?",
    "i want to see crossland car",
    "i want to test drive opel grand?",
    
    # options examples
    "what are the options of granland?",
    "can i find the Maintenance schedule for crossland",
    "can you tell me the options of that car",
    "what is the power of that car?",
    "can you explain the Installment system?",
    
    # reservation
    "i want to book grey crossland car",
    "i want to buy opel grandland",
    "let me reserve this car",
    "book one for me",
    "sign me up to buy this car"
]

labels = [
    # greetings
    "greetings",
    "greetings",
    "greetings",
    "greetings",
    "greetings",
    
    # thanks
    "thanks",
    "thanks",
    "thanks",
    "thanks",
    "thanks",
    
    # cost labels
    "cost_enq",
    "cost_enq",
    "cost_enq",
    "cost_enq",
    "cost_enq",
    
    # color labels
    "color_enq",
    "color_enq",
    "color_enq",
    "color_enq",
    "color_enq",
    
    
    # availability labels
    "availability_enq",
    "availability_enq",
    "availability_enq",
    "availability_enq",
    "availability_enq",
    
    # options date 
    "options_enq",
    "options_enq",
    "options_enq",
    "options_enq",
    "options_enq",
    
    # reservation labels
    "reserve_enq",
    "reserve_enq",
    "reserve_enq",
    "reserve_enq",
    "reserve_enq"
]


    
#knowldge back ~ our database
KB = {
    "CROSSLAND_ELEGANCE":
    {
        "price": 319990,
        "brand": "opel",
        "power":1200,
        "color":"red",
        "options":"https://eg.hatla2ee.com/en/new-car/opel/Crossland/19485",
        "start-date": datetime(2020, 5, 5),
        "registered": 0
    },
    "GRANDLAND_ELEGANCE":
    {
        "price": 430000,
        "brand": "opel",
        "power":1600,
        "color":"white",
        "options":"https://eg.hatla2ee.com/en/new-car/opel/Grandland/20877",
        "start-date": datetime(2020, 5, 10),
        "registered": 0
    },
    "CROSSLAND_TOP_LINE":
    {
        "price": 339990,
        "brand": "opel",
        "power":1200,
        "color":"black",
        "options":"https://eg.hatla2ee.com/en/new-car/opel/Crossland/19488",
        "start-date": datetime(2020, 7, 5),
        "registered": 0
    },
    "GRANDLAND_HIGH_LINE":
    {
        "price": 470000,
        "brand": "opel",
        "power":1600,
        "color":"grey",
        "options":"https://eg.hatla2ee.com/en/new-car/opel/Grandland/20881",
        "start-date": datetime(2020, 10, 5),
        "registered": 0
    },
    
}


def load_data_to_db():
    connection.execute("delete from cars")
    for car_name in KB.keys():
        price = KB[car_name]['price']
        brand = KB[car_name]['brand']
        power = KB[car_name]['power']
        color = KB[car_name]['color']
        options = KB[car_name]['options']
        start_date = KB[car_name]['start-date'].strftime("%d-%m-%Y")
        register = KB[car_name]['registered']
        connection.execute(f"insert into cars (name, price,brand,power,color,options, start_date, registered)\
            values ('{car_name}', '{price}', '{brand}', '{power}','{color}','{options}', '{start_date}', '{register}')")
    connection.commit()
    print("all done !")

def get_car_data(car_name):
    res = connection.execute(f"select * from cars  where name = '{car_name}'").fetchall()[0]
    car_info = {
        "name": res[0],
        "price": res[2],
        "brand": res[3],
        "power": res[4],
        "color": res[5],
        "options": res[6],
        "start_date": res[7],
        "registered": res[8]
    }
    return car_info

def register_user(car_name):
    connection.execute(f"update cars set registered=registered+1 where name = '{car_name}'")
    connection.commit()

    


if __name__ == "__main__":
    load_data_to_db()
   # car_info= get_car_data("GRANDLAND_HIGH_LINE")
   # print (car_info)
   # register_user("GRANDLAND_HIGH_LINE")