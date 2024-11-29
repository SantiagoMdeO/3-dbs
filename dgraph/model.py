#!/usr/bin/env python3
import pydgraph
import json

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
    username: string @index(trigram) .
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

# 2. Insert Data
def create_data(client):
    # Crear una nueva transacción
    txn = client.txn()
    try:
        data = [
            {
                'uid': '_:user1',
                'dgraph.type': 'user',
                'username': 'Nata',
                'follower_count': 1200,
                'Follows_before': [
                    {'uid': '_:user2', 'username': 'Ale'}
                ],
                'Follows_after': [
                    {'uid': '_:user3', 'username': 'Tato', 'when': '2024-11-24T10:00:00Z'}
                ]
            },
            {
                'uid': '_:user2',
                'dgraph.type': 'user',
                'username': 'Ale',
                'follower_count': 950,
                'Blocked_after': [
                    {'uid': '_:user3', 'when': '2024-11-23T15:30:00Z'}
                ]
            },
            {
                'uid': '_:user3',
                'dgraph.type': 'user',
                'username': 'Tato',
                'follower_count': 500
            },
            {
                'uid': '_:post1',
                'dgraph.type': 'post',
                'description': 'Excited to share my first post!',
                'reach_count': 100,
                'reach_type': 'organic',
                'interaction': [
                    {'uid': '_:interaction1', 'type': 'like', 'user': {'uid': '_:user2'}, 'when': '2024-11-24T11:00:00Z'}
                ]
            },
            {
                'uid': '_:interaction1',
                'dgraph.type': 'interaction',
                'type': 'like',
                'user': {'uid': '_:user2'},
                'when': '2024-11-24T11:00:00Z'
            }
        ]

        response = txn.mutate(set_obj=data)

        # Confirmar transacción
        commit_response = txn.commit()
        print(f"Commit Response: {commit_response}")

        print(f"UIDs asignados: {response.uids}")
    finally:
        # Limpiar
        txn.discard()

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