#!/usr/bin/env python3
import csv
import requests
from datetime import datetime


BASE_URL = "http://localhost:8000"

def posts_populate():
    with open("posts.csv", encoding="utf-8") as fd:  # Specify UTF-8 encoding
        posts_csv = csv.DictReader(fd)
        for post in posts_csv:
            # Convert the `comments` field from semicolon-separated string to a list
            if post["comments"]:
                post["comments"] = post["comments"].split(";")
            else:
                post["comments"] = []

            # Convert likes to an integer
            post["likes"] = int(post["likes"])
            print(post)
            print("we about to upload it\n\n")
            # Post the data to the API
            
            response = requests.post(BASE_URL + "/posts", json=post)
            if response.ok:
                created_post = response.json()
                print(f"Successfully posted: {created_post['_id']}")
            else:
                print(f"Failed to post post {response.status_code} - {response.json()}")

# Function to read the CSV and upload the data
def likes_populate():
    with open("likes.csv", encoding="utf-8") as fd:  # Specify UTF-8 encoding
        likes_csv = csv.DictReader(fd)
        for like in likes_csv:
            # Convert `like_status` to a boolean
            like["like_status"] = like["like_status"] == "True"  # True/False as boolean
            
            # Convert `pseudo_timestamp` to a datetime object
            #like["pseudo_timestamp"] = datetime.strptime(like["pseudo_timestamp"], "%Y-%m-%dT%H:%M:%SZ")
            
            # Print the item before uploading (optional)
            print(like)            
            # Post the data to the API
            response = requests.post(BASE_URL + "/likes", json=like)
            print("we got it")
            if response.ok:
                created_post = response.json()
                print(f"Successfully posted: {str(created_post['_id'])}")
            else:
                print(f"Failed to post like {response.status_code} - {response.json()}")




def main():
    # Call the function to upload data from the CSV
    likes_populate()
    posts_populate()
    

if __name__ == "__main__":
    main()

