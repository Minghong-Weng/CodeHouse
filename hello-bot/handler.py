import random
import json
from pprint import pprint
import os
from textblob import TextBlob
import nltk
import requests
nltk.download('brown')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up","hey", "ola")

GREETING_RESPONSES = ["'sup bro", "hey", "*nods*", "hey you get my snap?"]
PROFESSION_TO_ID = {"Software Engineer": "0", "Data Scientist":"1", "Robotics Engineer":"2", "Aerospace Engineer":"3"}

AVG_SALARIES = [100690, 133000, 81097,107830]

ID_TO_SKILLS ={"0": ["Data structures & Algorithms", "Distributed Systems", "OS/Networking"], "1": ["Statistics","Database Systems", "Data Modeling and Visualisation"],"2": ["Computer Vision", "Planning & Decision-making in robotics", "Mathematics/ Statistical techniques"], "3":["Computer Aided Design","Aerodynamiscs","Propulsion Systems"]}

ID_TO_UNIVERSITY={"0": ["Stanford University", "Massachusetts Institute of Technology", "Carnegie Mellon University", "University of California, Berkeley", "University of Michigan"], "1":["Carnegie Mellon University", "University of Washington", "University of California, Berkeley", "Columbia University", "Stanford University"], "2": ["Carnegie Mellon University", "Georgia Institute of Technology", "Massachusetts Institute of Technology", "University of Michigan", "University of Southern California"], "3":["Massachusetts Institute of Technology", "Stanford University", "Georgia Institute of Technology","California Institute of Technology", "University of Michigan"]}


BUDGET_RESPONSES = [['It costs about', 'USD a year'], ['The Tuition Fee is around',  'USD per annum'], ['The cost of attending this university would be',  'US Dollars yearly']]

LOCATION_RESPONSES = ['Sure, The college is at', 'Definitely! It is in', 'Of Course, The university is located in ',  'Oh! Good question, It is in']

DESCRIPTION_RESPONSES = ['Oh yeah, Ofcourse. Here is some information from Wikipedia. \n',' Sure, I have got some details from Wikipedia for you! \n', "This is what Wikipedia has to say about it! \n"]
WEBSITE_RESPONSES = ["Check out more at ", "More information is provided on their website. I have got that for you ", "Feel free to check them out on their website"]
BYE_KEYWORDS = ("bye", "exit", "quit")
BYE_RESPONSES = ["bye, take care!", "see you soon", "hope we helped you, bye now!"]

def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """

    ## GREETING MESSAGE
    sentence=req
   
    ## get details about profession

    for profession in PROFESSION_TO_ID.keys():
        if profession.lower() in req.lower():
            return profession_info(profession)


    ## GET UNIVERSITY DETAILS

    # blob = TextBlob(sentence)
    # nouns = []
    # nouns = blob.noun_phrases

    is_noun = lambda pos: pos[:2] == 'NN'
    # do the nlp stuff
    tokenized = nltk.word_tokenize(sentence)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
    postags = [pos for (word, pos) in nltk.pos_tag(tokenized)]
    words =  [word for (word, pos) in nltk.pos_tag(tokenized) ]

    patterns = [['NNP', 'IN', 'NNP', 'NNP'], ['NNP','NNP','IN', 'NNP'],['NNP','IN','NNP'], ['NNP', 'NNP', 'NNP'],['NNP', 'NNP']]
    university_name =""
    for pat in patterns:
        index = [x for x in range(len(postags)) if postags[x:x+len(pat)] == pat]
        if len(index) != 0:
            university_name = ' '.join(words[index[0]: index[0]+len(pat)])
    
    if len(university_name) != 0:
        if "budget" in sentence.lower() or sentence.lower().startswith("how much") or "cost" in sentence.lower():
            json_obj = {}
            json_obj["university"] = university_name
            json_obj["parameter"] = "budget"
            budget_res = random.choice(BUDGET_RESPONSES)
            
            r = requests.get("http://gateway:8080/function/get-handler", data=json.dumps(json_obj))
            result = r.json()
            return budget_res[0]+" "+str(result)+ " " + budget_res[1]

        if "location" in sentence.lower() or "where" in sentence.lower() or "address" in sentence.lower() or "located in" in sentence.lower()  or sentence.lower().startswith("what part") :
            json_obj = {}
            json_obj["university"] = university_name
            json_obj["parameter"] = "location"
            location_res = random.choice(LOCATION_RESPONSES)
            
            r = requests.get("http://gateway:8080/function/get-handler", data=json.dumps(json_obj))
            result = r.json()
            return location_res+" "+result["city"]+random.choice([" , ", " in ", " in the state of "])+result["state"]
        
        if "tell me " in sentence.lower() or "about" in sentence.lower() or "details" in sentence.lower() or "information" in sentence.lower():
            json_obj = {}
            json_obj["university"] = university_name
            json_obj["parameter"] = "description"
            desc_res = random.choice(DESCRIPTION_RESPONSES)
            
            r = requests.get("http://gateway:8080/function/get-handler", data=json.dumps(json_obj))
            result = r.json()
            return desc_res+str(result)

        if "contact" in sentence.lower() or "reach" in sentence.lower() or "website" in sentence.lower() or "email" in sentence.lower():
            json_obj = {}
            json_obj["university"] = university_name
            json_obj["parameter"] = "website"
            website_res = random.choice(WEBSITE_RESPONSES)
            
            r = requests.get("http://gateway:8080/function/get-handler", data=json.dumps(json_obj))
            result = r.json()
            return website_res+str(result)


    for word in sentence.split(' '):
        if word.lower() in GREETING_KEYWORDS:
            return random.choice(GREETING_RESPONSES)

    for word in sentence.split(' '):
        if word.lower() in BYE_KEYWORDS:
            return random.choice(BYE_RESPONSES)

    return "Sorry I do not understand!"


def profession_info(profession):
    id = PROFESSION_TO_ID.get(profession)
    skills = ID_TO_SKILLS.get(id)
    for i in range(1,4):
        skills[i-1] = str(i)+' '+skills[i-1]

    univs = ID_TO_UNIVERSITY.get(id)
    for i in range(1,6):
        univs[i-1] = str(i)+' '+univs[i-1]
    SKILL_RESPONSES = ["Okay, I did a little research for you! Here are the top skills needed for a "+profession+":",
                       "These are the skills a "+profession+" needs to acquire: "]
    UNIV_RESPONSES = ["These universities have the highest rankings for the above skills: ",
                      "For acquiring the above skills consider going to the following schools: "]

    return random.choice(SKILL_RESPONSES)+'\n' + '\n'.join(skills) + '\n' + random.choice(UNIV_RESPONSES)+'\n' + '\n'.join(univs)



#university_details = 
