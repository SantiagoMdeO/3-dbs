from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from bson import ObjectId  # Import ObjectId from bson
import json
from fastapi.responses import JSONResponse
from model import Post, PostUpdate
from routes.routes_funcs import cleanNones, clear_ObjectIDMongo_Errors_In_List, from_id_string_to_id_object, from_id_string_to_id_object, process_result_from_delete, find_object_by_id

router = APIRouter()


#THIS IS REALLY IMPORTANT AAAAAA
which_collection = "posts"

#post
#get all
#get single id
#get with filters
#update
#delete


#response = requests.post(BASE_URL + "/posts", json=post)
@router.post("/", response_description="Post a new post", status_code=status.HTTP_201_CREATED)
def create_post(request: Request, post: Post = Body(...)):
    post = jsonable_encoder(post)
    new_post = request.app.database[which_collection].insert_one(post)

    return find_object_by_id(which_collection, new_post.inserted_id, request)


# Get all posts with optional filters
#response = make_request(collection, "GET", params=filter_params)
@router.get("/", response_description="List all posts", response_model=List[Post])
def list_posts(request: Request, visibility_status: str = ''):
    query = {}
    if visibility_status != '':
        query["visibility_status"] = visibility_status
    
    posts = list(request.app.database[which_collection].find(query))
    return JSONResponse(clear_ObjectIDMongo_Errors_In_List(posts, query))


#this works
@router.get("/id/{id}", response_description="Get a single post by ID", response_model=Post)
def find_post(id: str, request: Request):
    object_id = from_id_string_to_id_object(id)
    
    # Find the post by ObjectId
    if (post := request.app.database[which_collection].find_one({"_id": object_id})) is not None:
        post["_id"] = str(post["_id"])  # Convert ObjectId back to string for the response
        return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found")


#func that recieves a string json, and then makes it back to a dictionary to pass a
@router.get("/query/", response_description="get many posts by your query(not by _id)", response_model=Post)
def find_post(request: Request, post: PostUpdate = Body(...)):
    
    post = jsonable_encoder(post)

    #clean the nones
    post_clean_query = cleanNones(post)

    returned_posts = list(request.app.database[which_collection].find(post_clean_query))

    #this also raises an eror if it is empty.
    finalResponse = clear_ObjectIDMongo_Errors_In_List(returned_posts, post_clean_query)

    return JSONResponse(content=finalResponse)

#we'll verify these later
# Update a post
@router.put("/id/{id}", response_description="Update a post", response_model=Post)
def update_post(id: str, request: Request, post_update: PostUpdate = Body(...)):
    post_update = jsonable_encoder(post_update)

    #clean the nones
    post_clean_query = cleanNones(post_update)

    # Convert the string ID to an ObjectId
    id = from_id_string_to_id_object(id)


    if len(post_clean_query) >= 1:
        update_result = request.app.database[which_collection].update_one({"_id": id}, {"$set": post_clean_query})

        #confirm it exists
        if update_result.modified_count == 1:
            if (updated_post := request.app.database[which_collection].find_one({"_id": id})) is not None:
                return updated_post

    if (existing_post := request.app.database[which_collection].find_one({"_id": id})) is not None:
        return existing_post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found")

# Delete a post
@router.delete("/id/{id}", response_description="Delete a post")
def delete_post(id: str, request: Request, response: Response):

    id_obj = from_id_string_to_id_object(id)

    delete_result = request.app.database[which_collection].delete_one({"_id": id_obj})

    return process_result_from_delete(delete_result, response)

