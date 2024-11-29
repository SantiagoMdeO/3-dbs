import pandas as pd
import random


def generateData():
    num_users = 25
    max_friends = 13


    # Generate data for 25 users
    data = []
    for i in range(num_users):
        popularity_score = random.randint(0, 100)  # Popularity score (0–100)
        num_posts = 3 + int(5*popularity_score/100)# Posts scaled with some variability
        num_followers = int((popularity_score/100)*max_friends)  # More followers for higher popularity
        num_following = int((popularity_score/100)*max_friends)+3  # Following proportional to followers
        activity_level = (
            "high" if popularity_score > 75 else "medium" if popularity_score > 25 else "low"
        )
        names = [
        "Julian", "Tess", "Caroline", "Camila", "Sabrina", "Madaline", 
        "Darcy", "Antony", "Kate", "Caroline", "Adrian", "Justin", 
        "Dominik", "Mary", "Lilianna", "Tiana", "Lily", "Henry", 
        "Kristian", "Audrey", "Rosie", "Madaline", "Honey", "Sam", "Honey"
        ]
        username = f"{names[i]}{i+1}"

        data.append(
            {
                "username": username,
                "popularity_score": popularity_score,
                "num_posts": num_posts,
                "num_followers": num_followers,
                "num_following": num_following,
                "activity_level": activity_level,
            }
        )

    # Create DataFrame
    df = pd.DataFrame(data)

    # Save to CSV
    output_path = "social_media_users.csv"
    df.to_csv(output_path, index=False)


from datetime import datetime, timedelta





import pandas as pd
import random
from datetime import datetime, timedelta

def process_users_to_dgraph_format(csv_path):
    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Prepare the final data format
    data = []
    user_list = [
        {"uid": f"_:user{i+1}", "username": row["username"]}
        for i, row in df.iterrows()
    ]
    
    for index, row in df.iterrows():
        user_uid = f"_:user{index+1}"
        username = row["username"]
        follower_count = row["num_followers"]
        num_following = row["num_following"]

        # Randomly sample users for "Follows_before" and "Follows_after"
        following_users = random.sample(
            [u for u in user_list if u["uid"] != user_uid], num_following
        )
        half = num_following // 2
        follows_before = following_users[:half]
        follows_after = following_users[half:]

        # Add timestamps to "Follows_after"
        follows_after_with_time = [
            {
                "uid": u["uid"],
                "username": u["username"],
                "when": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat() + "Z",
            }
            for u in follows_after
        ]

        # Append user data to the final structure
        data.append(
            {
                "uid": user_uid,
                "dgraph.type": "user",
                "username": username,
                "follower_count": follower_count,
                "Follows_before": follows_before,
                "Follows_after": follows_after_with_time,
            }
        )
    
    return data

generateData()

# # Example usage
# csv_path = "social_media_users.csv"  # Replace with your CSV file path
# result_data = process_users_to_dgraph_format(csv_path)

# # Print or save the result as needed
# import json
# print(json.dumps(result_data, indent=4))

