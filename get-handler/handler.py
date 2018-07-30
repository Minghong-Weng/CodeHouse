import json
import os
def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    
    data = json.loads(req)
    
    university_name = data['university']
    parameter = data['parameter']

    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'university_details.json')
    university_details = {}
    with open(path, 'r') as json_data:
        university_details = json.load(json_data)
        json_data.close()
        
    return university_details[university_name][parameter]
