#!/usr/bin/env python3
import os

from fastapi import FastAPI 
from pymongo import MongoClient 

from routes.posts import router as posts_router
from routes.likes import router as likes_router
from routes.comments import router as comments_router
from routes.highlights import router as highlights_router
from routes.profile_visits import router as profile_visits_router
from routes.mentions import router as mentions_router
from routes.shares import router as shares_router
from routes.activity import router as activity_router
from routes.notifications import router as notifications_router


MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
DB_NAME = os.getenv('MONGODB_DB_NAME', 'iteso')

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(MONGODB_URI)
    app.database = app.mongodb_client[DB_NAME]
    print(f"Connected to MongoDB at: {MONGODB_URI} \n\t Database: {DB_NAME}")
    
    # Ensure indexes for the "posts" collection
    app.database["posts"].create_index(
        [("user_id", 1), ("visibility_status", 1), ("created_at", -1)],
        name="user_visibility_created_at_idx",
    )  # Compound index for user_id, visibility_status, created_at
    


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("Bye bye...!!")


# List of tuples (name, router, prefix)
routes = [
    ("posts", posts_router),
    ("likes", likes_router),
    ("comments", comments_router),
    ("highlights", highlights_router),
    ("profile_visits", profile_visits_router),
    ("mentions", mentions_router),
    ("shares", shares_router),
    ("activity", activity_router),
    ("notifications", notifications_router),
]

# Dynamically include all routers
for name, router in routes:
    app.include_router(router, tags=[name], prefix=f"/{name}")
