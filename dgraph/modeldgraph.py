#!/usr/bin/env python3
import pydgraph
import json
import pandas as pd
import random
from datetime import datetime, timedelta



# 1. Schema
def set_schema(client):
    schema = """
    # Types
    type user {
        username
        follower_count
        Follows_before
        Follows_after
        Blocked_after
    }

    type Follows_before {
        username
        followed_user_uid
    }

    type Follows_after {
        username
        followed_user_uid
        when
    }

    type Blocked_after {
        user
        when
    }

    # Predicates
    username: string @index(trigram, hash) .
    follower_count: int .
    followed_user_uid: uid .
    Follows_before: [uid] @reverse .
    Blocked_after: [uid] @reverse .
    interaction: [uid] .
    when: dateTime .
    Follows_after: [uid] @reverse .
    user: uid .
    reach_count: int .
    reach_type: string .
    description: string @index(trigram) .
    type: string .
    """
    print("Setting schema in the database...\n")
    return client.alter(pydgraph.Operation(schema=schema))


def process_users_to_dgraph_format(csv_path):
    names = [
        "Julian", "Tess", "Caroline", "Camila", "Sabrina", "Madaline", "Darcy", "Antony",
        "Kate", "Caroline", "Adrian", "Justin", "Dominik", "Mary", "Lilianna", "Tiana",
        "Lily", "Henry", "Kristian", "Audrey", "Rosie", "Madaline", "Honey", "Sam", "Honey"
    ]
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
        blocked_user = random.choice([u for u in names if u != username])  


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
                'Blocked_user': {'uid': f'_:user{names.index(blocked_user)+1}', 'username': blocked_user}

            }
        )
    
    return data


# 2. Insert Data
def create_data(client):
    # Crear una nueva transacción
    txn = client.txn()
    try:
        data = process_users_to_dgraph_format("../data/dataUnderstanding/social_media_users.csv") #this migth not work

        response = txn.mutate(set_obj=data)

        # Confirmar transacción
        commit_response = txn.commit()
        print(f"Commit Response: {commit_response}")

        print(f"UIDs asignados: {response.uids}")
    finally:
        # Limpiar
        txn.discard()

def search_users_by_regex(client, prefix):
    query = """
    query search_users($regex: string) {
        users(func: regexp(username, $regex)) {
            uid
            username
        }
    }"""
    # Create the full regex string here
    regex = f"/^{prefix}.*/i"
    variables = {"$regex": regex}
    res = client.txn(read_only=True).query(query, variables=variables)
    result = json.loads(res.json)
    print(json.dumps(result, indent=2))

def search_user_by_exact_match(client, username):
    query = """query search_user($username: string) {
        user(func: eq(username, $username)) {
            uid
            username
        }
    }"""

    variables = {"$username": username}
    res = client.txn(read_only=True).query(query, variables=variables)
    result = json.loads(res.json)
    print(json.dumps(result, indent=2))

def query_follows(client, username):
    query = """
    query getUserFollows($username: string) {
        user(func: eq(username, $username)) {
            uid
            username
            follows: Follows_before {
                uid
                username
            }
        }
    }"""
    
    variables = {"$username": username}
    res = client.txn(read_only=True).query(query, variables=variables)
    result = json.loads(res.json)
    print("follows before registration to app:")
    print(json.dumps(result, indent=2))
    query = """
    query getUserFollows($username: string) {
        user(func: eq(username, $username)) {
            uid
            username
            follows: Follows_after {
                uid
                username
                when
            }
        }
    }"""
    
    variables = {"$username": username}
    res = client.txn(read_only=True).query(query, variables=variables)
    result = json.loads(res.json)
    print("follows after registration to app:")
    print(json.dumps(result, indent=2))

def query_followers(client, username):
    query = """
    query getUserFollows($username: string) {
        user(func: eq(username, $username)) {
            uid
            username
            followers: ~Follows_before {
                uid
                username
            }
        }
    }"""
    
    variables = {"$username": username}
    res = client.txn(read_only=True).query(query, variables=variables)
    result = json.loads(res.json)
    print("follows before registration to app:")
    print(json.dumps(result, indent=2))


    query = """
    query getUserFollows($username: string) {
        user(func: eq(username, $username)) {
            uid
            username
            followers: ~Follows_after {
                uid
                username
                when
            }
        }
    }"""
    
    variables = {"$username": username}
    res = client.txn(read_only=True).query(query, variables=variables)
    result = json.loads(res.json)
    print("follows after registration to app:")
    print(json.dumps(result, indent=2))

def query_whoBlockedMe(client, username):
    query = """
    query getUserFollows($username: string) {
        user(func: eq(username, $username)) {
            uid
            username
            followers: ~Blocked_after {
                uid
                username
                when
            }
        }
    }"""
    
    variables = {"$username": username}
    res = client.txn(read_only=True).query(query, variables=variables)
    result = json.loads(res.json)
    print("follows before registration to app:")
    print(json.dumps(result, indent=2))

def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))