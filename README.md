# CAR SHOWROOM Center chat-bot

```raw
bot : Hi i am carbot how can i help?
user: hi i need to know some info aboute opel grandland elegance
bot : would like to test drive one at our CAR SHOWROOM?
user: yes
bot : More than happy to help
user: how much does it cost
bot : the price for GRANDLAND_ELEGANCE is only 430000L.E.
user: which colors avilable
bot : white color is available forGRANDLAND_ELEGANCE car
user: i need to know about the options
bot : GRANDLAND_ELEGANCE will be at our CAR SHOWROOM on 10-05-2020 happy to visit us to see the car
user: options
bot : this link https://eg.hatla2ee.com/en/new-car/opel/Grandland/20877 will show you all details abouteGRANDLAND_ELEGANCE
user: ok i need to book one
bot : Would you please confirm your GRANDLAND_ELEGANCE booking?
user: yes
bot : you have booked GRANDLAND_ELEGANCE car!, it will be available on 10-05-2020 !!
user: thank you
bot : Feel free to contact us anytime
```

the bot helps users to know about some information aboute cars in the CAR SHOWROOM
like price , colors , options , booking a car 
```bash
the bot answer questions aboute only 4 models of cars "as a start"
1. Opel grandland highline
2. Opel grandland elegance
3. Opel crossland elegance
4. Opel crossland topline
```
## Usage and installation

to use the model with your own system, you can create an object of the Bot class and choose if you want it to retrain, it as follows

```python
from carbot import Bot

# if you want it to retrain, set retrain=True
# you can choose which approach deep_learning or machine learning
bot = Bot(retrain=False, deep_learning=True)
# run the bot loop
bot.run_blocking()
```

Don't forget to create a virtual environment to run the code

```bash
$python -m venv venv
$source venv/bin/activate
$pip install -r requirements.txt
```
