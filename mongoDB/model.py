#!/usr/bin/env python3
import uuid
from typing import Optional, List

from datetime import datetime
from pydantic import BaseModel, Field

class Post(BaseModel):
    user_id: str = Field(..., description="ID of the user who created the post")
    content: str = Field(..., description="Content of the post")
    visibility_status: str = Field(..., description="Visibility status of the post (e.g., 'public', 'private', 'friends')")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the post was created")
    likes: int = Field(default=0, description="Number of likes on the post")
    comments: List[str] = Field(default_factory=list, description="List of comment IDs associated with the post")

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "8e1b92d2-634e-4b5f-8d53-2fcb62e0a75c",
                "user_id": "12345678-abcd-1234-abcd-1234567890ab",
                "content": "Just had the best coffee ever!",
                "visibility_status": "public",
                "created_at": "2024-11-22T10:30:00Z",
                "likes": 120,
                "comments": [
                    "c1234567-abcd-1234-abcd-1234567890ab",
                    "c9876543-abcd-1234-abcd-0987654321ba"
                ]
            }
        }

class PostUpdate(BaseModel):
    content: Optional[str] = None
    visibility_status: Optional[str] = None
    likes: Optional[int] = None
    comments: Optional[List[str]] = None

    class Config:
        schema_extra = {
            "example": {
                "content": "Updated post content",
                "visibility_status": "friends",
                "likes": 150,
                "comments": [
                    "c1234567-abcd-1234-abcd-1234567890ab",
                    "c9876543-abcd-1234-abcd-0987654321ba",
                    "c4567890-abcd-1234-abcd-234567890123"
                ]
            }
        }
