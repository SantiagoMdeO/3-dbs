import random
import string
import csv
from datetime import datetime, timedelta

# Function to generate a random user ID (hexadecimal string)
def generate_user_id():
    return "0x" + "".join(random.choices("0123456789ABCDEF", k=random.randint(2, 4)))

# Function to generate random content
def generate_content():
    options = ["Here at the beach", "Just had the best coffee ever!", 
               "Exploring the mountains this weekend!", 
               "Loving the new album from my favorite artist!"]
    return random.choice(options)

# Function to generate random visibility status
def generate_visibility_status():
    return random.choice(["public", "friends", "private"])

# Function to generate a random date
def generate_created_at():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 11, 23)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days),
                                         seconds=random.randint(0, 86400))  # Random seconds in the day
    return random_date.strftime("%Y-%m-%dT%H:%M:%SZ")

# Function to generate a random number of likes
def generate_likes():
    return random.randint(0, 500)

# Function to generate dummy comment IDs
def generate_comments():
    comment_ids = [f"c{random.randint(1000000, 9999999)}-mongoID" for _ in range(random.randint(1, 5))]
    return ";".join(comment_ids)

# Function to generate a single entry
def generate_entry():
    return {
        "user_id": generate_user_id(),
        "content": generate_content(),
        "visibility_status": generate_visibility_status(),
        "created_at": generate_created_at(),
        "likes": generate_likes(),
        "comments": generate_comments(),
    }

# Generate multiple entries and write to CSV
def generate_csv(filename, num_entries):
    fieldnames = ["user_id", "content", "visibility_status", "created_at", "likes", "comments"]
    entries = [generate_entry() for _ in range(num_entries)]
    
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(entries)

# Example usage
generate_csv("posts.csv", 12)
print("CSV generated successfully!")