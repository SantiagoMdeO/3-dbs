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

    type post {
        user
        description
        reach_count
        reach_type
        interaction
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

    type interaction {
        type
        user
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
    Follows_before: [uid] .
    Blocked_after: [uid] .
    interaction: [uid] .
    when: dateTime .
    Follows_after: [uid] .
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

def search_user_by_prefix(client, prefix: str):
    query = f"""
    {{
      users(func: has(username)) @filter(regex(username, "^{prefix}.*")) {{
        uid
        username
      }}
    }}
    """
    
    response = client.txn(read_only=True).query(query)
    result = json.loads(response.json)
    print(json.dumps(result, indent=2))


# 3. Follow Tracking Before Registration
def query_follow_tracking_before(client):
    query = """
    {
        followsBefore(func: has(Follows_before)) {
            uid
            username
            Follows_before {
                uid
                username
            }
        }
    }
    """
    response = client.txn(read_only=True).query(query)
    result = json.loads(response.json)
    print(json.dumps(result, indent=2))

# 4. New Follower Tracking
def query_new_follower_tracking(client):
    query = """
    {
        followsAfter(func: has(Follows_after)) {
            uid
            username
            Follows_after @facets {
                uid
                username
                when
            }
        }
    }
    """
    response = client.txn(read_only=True).query(query)
    result = json.loads(response.json)
    print(json.dumps(result, indent=2))

# 5. Unfollow Tracking
def query_unfollow_tracking(client):
    query = """
    {
        unfollows(func: has(Blocked_after)) {
            uid
            username
            Blocked_after @facets {
                uid
                when
            }
        }
    }
    """
    response = client.txn(read_only=True).query(query)
    result = json.loads(response.json)
    print(json.dumps(result, indent=2))

# 6. Follower Growth Analytics
# def query_follower_growth_analytics(client):

# 7. Content Reach Analysis
def query_content_reach_analysis(client):
    query = """
    {
        reach(func: has(reach_count)) {
            uid
            description
            reach_count
            reach_type
            interaction {
                type
            }
        }
    }
    """
    response = client.txn(read_only=True).query(query)
    result = json.loads(response.json)
    print(json.dumps(result, indent=2))

# 8. Profile Interaction Mapping
def query_profile_interaction_mapping(client):
    query = """
    {
        interactions(func: has(interaction)) {
            uid
            username
            interaction @facets {
                type
                when
                user {
                    uid
                    username
                }
            }
        }
    }
    """
    response = client.txn(read_only=True).query(query)
    result = json.loads(response.json)
    print(json.dumps(result, indent=2))

# 9. User Block Tracking
def query_user_block_tracking(client):
    query = """
    {
        blocked(func: has(Blocked_after)) {
            uid
            username
            Blocked_after @facets {
                uid
                when
            }
        }
    }
    """
    response = client.txn(read_only=True).query(query)
    result = json.loads(response.json)
    print(json.dumps(result, indent=2))


# 10. Delete todito
def drop_all(client):
    return client.alter(pydgraph.Operation(drop_all=True))