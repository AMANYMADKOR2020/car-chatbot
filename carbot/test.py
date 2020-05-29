import re
text="i want to know aboute opel grandland highline options"
cars_name_regex = {
    "CROSSLAND_ELEGANCE": re.compile(r"(?=.*crossland)(?=.*elegance)"),
    "GRANDLAND_ELEGANCE": re.compile(r"(?=.*grandland)(?=.*elegance)"),
    "CROSSLAND_TOP_LINE": re.compile(r"(?=.*crossland)(?=.*topline)"),
    "GRANDLAND_HIGH_LINE":re.compile(r"(?=.*grandland)(?=.*highline)")    }


text = text.lower()
for key in cars_name_regex.keys():
    results = cars_name_regex[key].findall(text)
    if len(results):
        print(key) 
     