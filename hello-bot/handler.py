import random
import json
from pprint import pprint
import os

GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up",)

GREETING_RESPONSES = ["'sup bro", "hey", "*nods*", "hey you get my snap?"]
PROFESSION_TO_ID = {"Software Engineer": 0, "Data Scientist":1, "Robotics Engineer":2, "Aerospace Engineer":3}

AVG_SALARIES = [100690, 133000, 81097,107830]

ID_TO_SKILLS ={"0": ["Data structures & Algorithms", "Distributed Systems", "OS/Networking"], "1": ["Statistics","Database Systems", "Data Modeling and Visualisation"],"2": ["Computer Vision", "Planning & Decision-making in robotics", "Mathematics/ Statistical techniques"], "3":["Computer Aided Design","Aerodynamiscs","Propulsion Systems"]}

ID_TO_UNIVERSITY={"0": ["Stanford University", "Massachusetts Institute of Technology", "Carnegie Mellon University", "University of California, Berkeley", "University of Michigan"], "1":["Carnegie Mellon University", "University of Washington", "University of California, Berkeley", "Columbia University", "Stanford University"], "2": ["Carnegie Mellon University", "Georgia Institute of Technology", "Massachusetts Institute of Technology", "University of Michigan", "University of Southern California"], "3":["Massachusetts Institute of Technology", "Stanford University", "Georgia Institute of Technology","California Institute of Technology", "University of Michigan"]}

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'university_details.json')

    with open(path, 'r') as json_data:
        d = json.load(json_data)
        json_data.close()
        return pprint(d)

# sentence=req
# for word in sentence.split(' '):
#     if word.lower() in GREETING_KEYWORDS:
#         return random.choice(GREETING_RESPONSES)
    




#university_details = 
