import random
import json
from pprint import pprint
import os
from textblob import TextBlob
import nltk
nltk.download('brown')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

GREETING_KEYWORDS = ("hello", "hi", "greetings", "sup", "what's up","hey", "ola")

GREETING_RESPONSES = ["'sup bro", "hey", "*nods*", "hey you get my snap?"]
PROFESSION_TO_ID = {"Software Engineer": "0", "Data Scientist":"1", "Robotics Engineer":"2", "Aerospace Engineer":"3"}

AVG_SALARIES = [100690, 133000, 81097,107830]

ID_TO_SKILLS ={"0": ["Data structures & Algorithms", "Distributed Systems", "OS/Networking"], "1": ["Statistics","Database Systems", "Data Modeling and Visualisation"],"2": ["Computer Vision", "Planning & Decision-making in robotics", "Mathematics/ Statistical techniques"], "3":["Computer Aided Design","Aerodynamiscs","Propulsion Systems"]}

ID_TO_UNIVERSITY={"0": ["Stanford University", "Massachusetts Institute of Technology", "Carnegie Mellon University", "University of California, Berkeley", "University of Michigan"], "1":["Carnegie Mellon University", "University of Washington", "University of California, Berkeley", "Columbia University", "Stanford University"], "2": ["Carnegie Mellon University", "Georgia Institute of Technology", "Massachusetts Institute of Technology", "University of Michigan", "University of Southern California"], "3":["Massachusetts Institute of Technology", "Stanford University", "Georgia Institute of Technology","California Institute of Technology", "University of Michigan"]}

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
    if req in PROFESSION_TO_ID:
        return profession_info(req)

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
    for pat in patterns:
        index = [x for x in range(len(postags)) if postags[x:x+len(pat)] == pat]
        if len(index) != 0:
            return ' '.join(words[index[0]: index[0]+len(pat)])

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
