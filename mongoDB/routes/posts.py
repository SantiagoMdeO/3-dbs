from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

#for object ids
from bson import ObjectId  # Import ObjectId from bson

#for queries as strings
import json



from model import Post, PostUpdate

router = APIRouter()


#response = requests.post(BASE_URL + "/posts", json=post)
@router.post("/", response_description="Post a new post", status_code=status.HTTP_201_CREATED)
def create_post(request: Request, post: Post = Body(...)):
    post = jsonable_encoder(post)
    new_post = request.app.database["posts"].insert_one(post)
    created_post = request.app.database["posts"].find_one({"_id": new_post.inserted_id})
    
    # Convert the MongoDB ObjectId to a string before returning
    created_post["_id"] = str(created_post["_id"])
    return created_post


# Get all posts with optional filters
#response = make_request(collection, "GET", params=filter_params)
@router.get("/", response_description="List all posts", response_model=List[Post])
def list_posts(request: Request, visibility_status: str = ''):
    print("we started\n\n\n")
    query = {}
    if visibility_status != '':
        query["visibility_status"] = visibility_status
    
    posts = list(request.app.database["posts"].find(query))
    print("we finished\n\n\n")
    return posts










@router.get("/id/{id}", response_description="Get a single post by ID", response_model=Post)
def find_post(id: str, request: Request):
    try:
        # Convert the string ID to ObjectId
        object_id = ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid post ID format")

    # Find the post by ObjectId
    if (post := request.app.database["posts"].find_one({"_id": object_id})) is not None:
        post["_id"] = str(post["_id"])  # Convert ObjectId back to string for the response
        return post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found")











#func that recieves a string json, and then makes it back to a dictionary to pass a
@router.get("/{queryString}", response_description="get many posts by your query(not by _id)", response_model=Post)
def find_post(queryString: str, request: Request):
    reconstructed_dict = json.loads(queryString)
    if (post := request.app.database["posts"].find_many(reconstructed_dict)) is not None:
        return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with this query {reconstructed_dict}\n not found")


#we'll verify these later
# Update a post
@router.put("/{id}", response_description="Update a post", response_model=Post)
def update_post(id: str, request: Request, post_update: PostUpdate = Body(...)):
    post_data = {k: v for k, v in post_update.dict().items() if v is not None}

    if len(post_data) >= 1:
        update_result = request.app.database["posts"].update_one(
            {"_id": id}, {"$set": post_data}
        )

        if update_result.modified_count == 1:
            if (updated_post := request.app.database["posts"].find_one({"_id": id})) is not None:
                return updated_post

    if (existing_post := request.app.database["posts"].find_one({"_id": id})) is not None:
        return existing_post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found")

# Delete a post
@router.delete("/{id}", response_description="Delete a post")
def delete_post(id: str, request: Request, response: Response):
    delete_result = request.app.database["posts"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found")

