#!/usr/bin/env python3
import argparse
import logging
import os
import requests
import json
from pprint import pprint

from model import PostUpdate

#this we update each time =======================================
#from model import Post, PostUpdate
#this was a desperate attempt at the last code, so i dont think i need it now



# Set logger
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('post.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Read env vars related to API connection
POSTS_API_URL = os.getenv("POSTS_API_URL", "http://localhost:8000")

BASE_API_URL = os.getenv("BASE_API_URL", "http://localhost:8000")



def processingJsonResponse(response, containsIDTrouble):
    if response and response.status_code == 200:
        print("Request was successful! Validating and printing response...\n")
        
        # Parse the response JSON
        try:
            data = response.json()
        except json.JSONDecodeError:
            print("not JSON?.")
            try:
                print(response)
            except:
                print("coudnt directy, print it")
        else:
            if containsIDTrouble:
                # Validate the structure of the data
                if isinstance(data, list) and all("_id" in post for post in data):
                    print("Response data is valid!")
                    
                    # Pretty-print the data
                    print(json.dumps(data, indent=4))
                else:
                    print("Error: Response structure is not as expected.")
            else:
                # Pretty-print the data
                print(json.dumps(data, indent=4))
    else:
        print(response)
        print(f"Request failed with status code: {response.status_code if response else 'No response received'}")




def make_request(collection, action, id=None, query=None, params='', json_data=None):
    url = f"{BASE_API_URL}/{collection}"
    if id:
        url += f"/id/{id}"
    if query:
        url += "/query/"
    if params != '':
        params_dictionary = {}
        for p in params:
            temp = str.split(p, '+')
            params_dictionary[temp[0]] = temp[1]
        print(params_dictionary)
        # book_update_instance = BookUpdate(**params_dictionary)
        postDatatypeIncomplete = PostUpdate(**params_dictionary)
        params = postDatatypeIncomplete.dict()

    print(url)
    print(params)

    if action == "GET":
        return requests.get(url, json=params)
    elif action == "POST":
        return requests.post(url, json=params)
    elif action == "PUT":
        return requests.put(url, json=params)
    elif action == "DELETE":
        return requests.delete(url)
    else:
        raise ValueError("Invalid action type")

def print_entity(entity):
    for k, v in entity.items():
        print(f"{k}: {v}")
    print("=" * 50)

def list_entities(collection, filter_params=None):

    response = make_request(collection, "GET", params=filter_params)
    if response.ok:
        for entity in response.json():
            print_entity(entity)
    else:
        print(f"Error: {response.text}")








def main():
    log.info(f"Welcome to books catalog. App requests to: {POSTS_API_URL}")

    parser = argparse.ArgumentParser()
    parser.add_argument("collection", choices=["posts", "likes", "comments", "highlights", "profile_visits", "mentions", "shares", "activity", "notifications"], help="Target collection")
    parser.add_argument("action", choices=["list", "get", "create", "update", "delete"], help="Action to perform")
    parser.add_argument("-i", "--id", help="Entity ID for actions that require it")
    parser.add_argument("-p", "--parameters",
            nargs='+', #aqui si le pedi ayuda a chat, estaba la opcion de mandarlos como param1,param2, y luego spliteaba el string, pero esto se ve mas pro
            help="add them like this: -p language_code+spn", default=None)
    args = parser.parse_args()

    #params = {k: v for k, v in [p.split("=") for p in args.params]} if args.params else None
    

    if args.action == "list":
        list_entities(args.collection, filter_params='')
    elif args.action == "get" and args.id and not args.parameters:
        response = make_request(args.collection, "GET", id=args.id)
        if response.ok:
            print_entity(response.json())
        else:
            print(f"Error: {response.text}")
    elif args.action == "get" and args.parameters:
        response = make_request(args.collection, "GET", params=args.parameters, query=True)
        processingJsonResponse(response, 1)
    elif args.action == "update" and args.id and args.parameters:
        print("we called put\n\n:)\n")
        response = make_request(args.collection, "PUT", params=args.parameters, id=args.id)
        processingJsonResponse(response, None)
    elif args.action == "delete" and args.id:
        print("we called put\n\n:)\n")
        response = make_request(args.collection, "DELETE", id=args.id)
        processingJsonResponse(response, None)

    # Handle create, update, delete similarly


if __name__ == "__main__":
    main()