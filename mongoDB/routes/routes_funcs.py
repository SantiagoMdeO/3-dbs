from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
#for object ids
from bson import ObjectId  # Import ObjectId from bson
#for queries as strings
import json
from fastapi.responses import JSONResponse
from model import Post, PostUpdate


def cleanNones(query):
    #clean the nones
    clean_query = {}
    for x in query.keys():
        if query[x] is not None:
            clean_query[x] = query[x]
    return clean_query

def clear_ObjectIDMongo_Errors_In_List(returned_list_of_dict, query):
    if returned_list_of_dict:
        for post in returned_list_of_dict:
            post["_id"] = str(post["_id"])
        return returned_list_of_dict
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Posts with this query {query} not found",
    )

def from_id_string_to_id_object(id):
    try:
        return ObjectId(id)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format")

def process_result_from_delete(delete_result, response):
    if delete_result.acknowledged:
        if delete_result.deleted_count:
            print("Document deleted.")
            response.status_code = status.HTTP_200_OK
            return response
        else:
            print("No document found to delete.")
            response.status_code = status.HTTP_404_NOT_FOUND
            return response
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID {id} not found")

def find_object_by_id(object, id, request):
    foundObject = request.app.database[object].find_one({"_id": id})
    
    # Convert the MongoDB ObjectId to a string before returning
    foundObject["_id"] = str(foundObject["_id"])


