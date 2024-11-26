#!/usr/bin/env python
import datetime
import logging
import random
import uuid
from cassandra.query import BatchStatement
from cassandra.cluster import Cluster



# Set logger
log = logging.getLogger()


CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {}}}
"""

CREATE_USERS = """
    CREATE TABLE IF NOT EXISTS users (
        user_id UUID PRIMARY KEY,
        username TEXT
    )
"""

CREATE_POSTS = """
    CREATE TABLE IF NOT EXISTS posts (
        post_id UUID,
        user_id UUID,
        content TEXT,
        timestamp TIMESTAMP,
        PRIMARY KEY (user_id, post_id)
    )
"""

USERS = [(uuid.uuid4(), f"user_{i + 1}") for i in range(20)]
POSTS = [(uuid.uuid4(), random.choice(USERS)[0], f"Post_{i + 1}", datetime.datetime.now()) for i in range(15)]

CREATE_USERS_ACTIVITY = """
    CREATE TABLE IF NOT EXISTS user_activity (
        user_id UUID,
        activity_timestamp TIMESTAMP,
        activity_type TEXT,
        activity_details TEXT,
        PRIMARY KEY ((user_id), activity_timestamp)
    ) WITH CLUSTERING ORDER BY (activity_timestamp DESC)
"""

CREATE_ENGAGEMENT_RATE = """
    CREATE TABLE IF NOT EXISTS engagement_rate (
        user_id UUID,
        calculation_timestamp TIMESTAMP,
        engagement_rate DOUBLE,
        PRIMARY KEY ((user_id), calculation_timestamp)
    ) WITH CLUSTERING ORDER BY (calculation_timestamp DESC)
"""

CREATE_INTERACTION_DURATION = """
    CREATE TABLE IF NOT EXISTS interaction_duration (
        user_id UUID,
        other_user_id UUID,
        interaction_start TIMESTAMP,
        interaction_end TIMESTAMP,
        duration_minutes INT,
        PRIMARY KEY ((user_id, other_user_id), interaction_start)
    ) WITH CLUSTERING ORDER BY (interaction_start DESC)
"""

CREATE_TRENDING_CONTENT = """
    CREATE TABLE IF NOT EXISTS trending_content (
        post_id UUID,
        detection_timestamp TIMESTAMP,
        trend_score DOUBLE,
        PRIMARY KEY ((post_id), detection_timestamp)
    ) WITH CLUSTERING ORDER BY (detection_timestamp DESC)
"""

CREATE_USER_SESSION = """
    CREATE TABLE IF NOT EXISTS user_session (
        user_id UUID,
        session_start TIMESTAMP,
        session_end TIMESTAMP,
        session_duration INT,
        PRIMARY KEY ((user_id), session_start)
    ) WITH CLUSTERING ORDER BY (session_start DESC)
"""

CREATE_INACTIVE_USER = """
    CREATE TABLE IF NOT EXISTS inactive_user (
        user_id UUID,
        last_activity_date DATE,
        inactivity_duration INT,
        PRIMARY KEY ((user_id), last_activity_date)
    ) WITH CLUSTERING ORDER BY (last_activity_date DESC)
"""

CREATE_ENGAGEMENT_BY_TIME = """
    CREATE TABLE IF NOT EXISTS engagement_by_time (
        user_id UUID,
        engagement_type TEXT,
        time_of_day TEXT,
        frequency_count INT,
        PRIMARY KEY ((user_id), time_of_day)
    ) WITH CLUSTERING ORDER BY (time_of_day ASC)
"""

def execute_batch(session, stmt, data):
    batch_size = 10
    for i in range(0, len(data), batch_size):
        batch = BatchStatement()
        for item in data[i : i+batch_size]:
            batch.add(stmt, item)
        session.execute(batch)
    session.execute(batch)


def bulk_insert(session):
    users_stmt = session.prepare("INSERT INTO users (user_id, username) VALUES (?, ?)")
    posts_stmt = session.prepare("INSERT INTO posts (post_id, user_id, content, timestamp) VALUES (?, ?, ?, ?)")
    user_activity_stmt = session.prepare("INSERT INTO user_activity (user_id, activity_timestamp, activity_type, activity_details) VALUES (?, ?, ?, ?)")
    engagement_rate_stmt = session.prepare("INSERT INTO engagement_rate (user_id, calculation_timestamp, engagement_rate) VALUES (?, ?, ?)")
    interaction_duration_stmt = session.prepare("INSERT INTO interaction_duration (user_id, other_user_id, interaction_start, interaction_end, duration_minutes) VALUES (?, ?, ?, ?, ?)")
    trending_content_stmt = session.prepare("INSERT INTO trending_content (post_id, detection_timestamp, trend_score) VALUES (?, ?, ?)")
    user_session_stmt = session.prepare("INSERT INTO user_session (user_id, session_start, session_end, session_duration) VALUES (?, ?, ?, ?)")
    inactive_user_stmt = session.prepare("INSERT INTO inactive_user (user_id, last_activity_date, inactivity_duration) VALUES (?, ?, ?)")
    engagement_by_time_stmt = session.prepare("INSERT INTO engagement_by_time (user_id, engagement_type, time_of_day, frequency_count) VALUES (?, ?, ?, ?)")

    #Users
    data = [(user_id, username) for user_id, username in USERS]
    execute_batch(session, users_stmt, data)

    # Insert Posts Data
    data = [(post_id, user_id, content, timestamp)
        for post_id, user_id, content, timestamp in POSTS]
    execute_batch(session, posts_stmt, data)

    # Insert User Activity Data
    data = []
    for i in range(20):
        user_id, username = random.choice(USERS)
        timestamp = datetime.datetime.now()
        activity_type = random.choice(['like', 'comment', 'share'])
        activity_details = f"{activity_type} post by {random.choice(USERS)[1]}"
        data.append((user_id, timestamp, activity_type, activity_details))
    execute_batch(session, user_activity_stmt, data)
    
    # Insert Engagement Rate Data
    data = []
    for i in range(20):
        user_id, _ = random.choice(USERS)
        timestamp = datetime.datetime.now()
        engagement_rate = random.uniform(0, 1)
        data.append((user_id, timestamp, engagement_rate))
    execute_batch(session, engagement_rate_stmt, data)
    
    # Insert Interaction Duration Data
    data = []
    for i in range(20):
        user_id, _ = random.choice(USERS)
        other_user_id, _ = random.choice(USERS)
        interaction_start = datetime.datetime.now()
        interaction_end = interaction_start + datetime.timedelta(minutes=random.randint(1, 30))
        duration_minutes = (interaction_end - interaction_start).seconds // 60
        data.append((user_id, other_user_id, interaction_start, interaction_end, duration_minutes))
    execute_batch(session, interaction_duration_stmt, data)

    # Insert Trending Content Data
    data = []
    for post_id, _, _, _ in POSTS:
        detection_timestamp = datetime.datetime.now()
        trend_score = random.uniform(0, 10)
        data.append((post_id, detection_timestamp, trend_score))
    execute_batch(session, trending_content_stmt, data)
    
    # Insert User Session Data
    data = []
    for i in range(20):
        user_id, _ = random.choice(USERS)
        session_start = datetime.datetime.now()
        session_end = session_start + datetime.timedelta(minutes=random.randint(10, 180))
        session_duration = (session_end - session_start).seconds // 60
        data.append((user_id, session_start, session_end, session_duration))
    execute_batch(session, user_session_stmt, data)
    
    # Insert Inactive User Data
    data = []
    for i in range(10):
        user_id, _ = random.choice(USERS)
        last_activity_date = datetime.date.today() - datetime.timedelta(days=random.randint(1, 30))
        inactivity_duration = random.randint(1, 60)
        data.append((user_id, last_activity_date, inactivity_duration))
    execute_batch(session, inactive_user_stmt, data)

    # Insert Engagement by Time Data
    data = []
    for i in range(15):
        user_id, _ = random.choice(USERS)
        engagement_type = random.choice(['like', 'comment', 'share'])
        time_of_day = random.choice(['morning', 'afternoon', 'evening'])
        frequency_count = random.randint(1, 10)
        data.append((user_id, engagement_type, time_of_day, frequency_count))
    execute_batch(session, engagement_by_time_stmt, data)

def create_keyspace(session, keyspace, replication_factor):
    log.info(f"Creating keyspace: {keyspace} with replication factor {replication_factor}")
    session.execute(CREATE_KEYSPACE.format(keyspace, replication_factor))

def print_all_users(session):
    query = "SELECT user_id, username FROM users"
    rows = session.execute(query)
    
    print("Users & UUIDs:")
    for row in rows:
        print(f"User: {row.username}, UUID: {row.user_id}")

def print_all_posts(session):
    query = "SELECT post_id, user_id, content, timestamp FROM posts"
    rows = session.execute(query)
    
    print("Posts Details:")
    for row in rows:
        print(f"Post ID: {row.post_id}, User ID: {row.user_id}, Content: {row.content}, Timestamp: {row.timestamp}")


def create_schema(session):
    log.info("Creating model schema")
    session.execute(CREATE_USERS) #0
    session.execute(CREATE_USERS_ACTIVITY) #1
    session.execute(CREATE_ENGAGEMENT_RATE) #2
    session.execute(CREATE_INTERACTION_DURATION) #3
    session.execute(CREATE_TRENDING_CONTENT) #4
    session.execute(CREATE_USER_SESSION) #5
    session.execute(CREATE_INACTIVE_USER) #6
    session.execute(CREATE_ENGAGEMENT_BY_TIME) #7
    session.execute(CREATE_POSTS) #8

# Retrieve all activities for a specific user ordered by timestamp. REQ 13
def get_user_activity(session, user_id):
    log.info(f"Retrieving activity for user {user_id}")
    
    stmt = session.prepare("""
        SELECT user_id, activity_timestamp, activity_type, activity_details
        FROM user_activity
        WHERE user_id = ?
        ORDER BY activity_timestamp DESC
    """)
    
    rows = session.execute(stmt, [user_id])
    if rows: 
        for row in rows:
            print(f"=== Activity: {row.activity_type} ===")
            print(f"- Timestamp: {row.activity_timestamp}")
            print(f"- Details: {row.activity_details}\n")
    else:
        print("No data found for the given user ID.")

# Retrieve the engagement rate fot a specific user at a particular time. REQ 16
def get_engagement_rate(session, user_id):
    log.info(f"Retrieving engagement rate for user {user_id}")
    
    stmt = session.prepare("""
        SELECT user_id, calculation_timestamp, engagement_rate
        FROM engagement_rate
        WHERE user_id = ?
        ORDER BY calculation_timestamp DESC
    """)
    
    rows = session.execute(stmt, [user_id])
    if rows:
        for row in rows:
            print(f"=== Engagement Rate: {row.engagement_rate} ===")
            print(f"- Timestamp: {row.calculation_timestamp}\n")
    else:
        print("No data found for the given user ID.")

# Retrieve interaction durations for a specific user, with filtering by the other user and sorting by the interaction time. REQ 9
def get_interaction_duration(session, user_id, other_user_id):
    log.info(f"Retrieving interaction duration between user {user_id} and {other_user_id}")
    
    stmt = session.prepare("""
        SELECT user_id, other_user_id, interaction_start, interaction_end, duration_minutes
        FROM interaction_duration
        WHERE user_id = ? AND other_user_id = ?
        ORDER BY interaction_start DESC
    """)
    
    rows = session.execute(stmt, [user_id, other_user_id])
    if rows: 
        for row in rows:
            print(f"=== Interaction with {row.other_user_id} ===")
            print(f"- Start: {row.interaction_start}")
            print(f"- End: {row.interaction_end}")
            print(f"- Duration (minutes): {row.duration_minutes}\n")
    else:
        print("No data found for the given user ID.")

# Retrieve the trend score for a specific post over time. REQ 18
def get_trending_content(session, post_id):
    log.info(f"Retrieving trending content for post {post_id}")
    
    stmt = session.prepare("""
        SELECT post_id, detection_timestamp, trend_score
        FROM trending_content
        WHERE post_id = ?
        ORDER BY detection_timestamp DESC
    """)
    
    rows = session.execute(stmt, [post_id])
    if rows: 
        for row in rows:
            print(f"=== Trending Content: {row.trend_score} ===")
            print(f"- Timestamp: {row.detection_timestamp}\n")
    else:
        print("No data found for the given post ID.")

# Retrieve all sessions for a specific user, ordered by the start time. REQ 27
def get_user_sessions(session, user_id):
    log.info(f"Retrieving sessions for user {user_id}")
    
    stmt = session.prepare("""
        SELECT user_id, session_start, session_end, session_duration
        FROM user_session
        WHERE user_id = ?
        ORDER BY session_start DESC
    """)
    
    rows = session.execute(stmt, [user_id])
    if rows: 
        for row in rows:
            print(f"=== Session ===")
            print(f"- Start: {row.session_start}")
            print(f"- End: {row.session_end}")
            print(f"- Duration (minutes): {row.session_duration}\n")
    else:
        print("No data found for the given user ID.")

# Retrieve users who have been inactive for a specific duration. REQ 35
def get_inactive_users(session, user_id):
    log.info(f"Retrieving inactive user data for user {user_id}")
    
    stmt = session.prepare("""
        SELECT user_id, last_activity_date, inactivity_duration
        FROM inactive_user
        WHERE user_id = ?
        ORDER BY last_activity_date DESC
    """)
    
    rows = session.execute(stmt, [user_id])
    if rows: 
        for row in rows:
            print(f"=== Inactive User ===")
            print(f"- Last Activity: {row.last_activity_date}")
            print(f"- Inactivity Duration (days): {row.inactivity_duration}\n")
    else:
        print("No data found for the given user ID.")

# Retrieve engagement frequency for a specific user grouped by time of day. REQ 24
def get_engagement_by_time(session, user_id):
    log.info(f"Retrieving engagement by time for user {user_id}")
    
    stmt = session.prepare("""
        SELECT user_id, engagement_type, time_of_day, frequency_count
        FROM engagement_by_time
        WHERE user_id = ?
    """)
    
    rows = session.execute(stmt, [user_id])
    if rows: 
        for row in rows:
            print(f"=== Engagement at {row.time_of_day} ===")
            print(f"- Engagement Type: {row.engagement_type}")
            print(f"- Frequency Count: {row.frequency_count}\n")
    else:
        print("No data found for the given user ID.")