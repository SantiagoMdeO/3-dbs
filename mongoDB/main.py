#!/usr/bin/env python3
import os

from fastapi import FastAPI 
from pymongo import MongoClient 

from routes.posts import router as posts_router


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

app.include_router(posts_router, tags=["posts"], prefix="/posts")
