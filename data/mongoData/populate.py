#!/usr/bin/env python3
import csv
import requests

BASE_URL = "http://localhost:8000"

def main():
    with open("posts.csv", encoding="utf-8") as fd:  # Specify UTF-8 encoding
        posts_csv = csv.DictReader(fd)
        for post in posts_csv:
            print(post)
            # Convert the `comments` field from semicolon-separated string to a list
            if post["comments"]:
                post["comments"] = post["comments"].split(";")
            else:
                post["comments"] = []

            # Convert likes to an integer
            post["likes"] = int(post["likes"])
            
            print("we about to upload it\n\n")
            # Post the data to the API
            response = requests.post(BASE_URL + "/post", json=post)
            if response.ok:
                print(f"Successfully posted: {post['post_id']}")
            else:
                print(f"Failed to post post {response.status_code} - {response.json()}")

if __name__ == "__main__":
    main()

