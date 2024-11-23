#!/usr/bin/env python3
import argparse
import logging
import os
import requests

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

def make_request(collection, action, id=None, params='', json_data=None):
    url = f"{BASE_API_URL}/{collection}"
    if id:
        url += f"/{id}"

    if action == "GET":
        print(url)
        return requests.get(url, params=params)
    elif action == "POST":
        return requests.post(url, json=json_data)
    elif action == "PUT":
        return requests.put(url, json=json_data)
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
    parser.add_argument("collection", choices=["posts", "likes", "comments"], help="Target collection")
    parser.add_argument("action", choices=["list", "get", "create", "update", "delete"], help="Action to perform")
    parser.add_argument("-i", "--id", help="Entity ID for actions that require it")
    parser.add_argument("-p", "--params", nargs="+", help="Parameters for the request (key=value)", default=None)
    args = parser.parse_args()

    params = {k: v for k, v in [p.split("=") for p in args.params]} if args.params else None
    

    if args.action == "list":
        list_entities(args.collection, filter_params=params)
    elif args.action == "get" and args.id:
        response = make_request(args.collection, "GET", id=args.id)
        if response.ok:
            print_entity(response.json())
        else:
            print(f"Error: {response.text}")
    # Handle create, update, delete similarly


if __name__ == "__main__":
    main()