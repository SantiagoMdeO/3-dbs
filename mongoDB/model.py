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


class PostLike(BaseModel):
    post_id: str = Field(..., description="ID of the post")
    user_id: str = Field(..., description="ID of the user who liked the post")
    like_status: bool = Field(..., description="True if liked, False if unliked")
    pseudo_timestamp: Optional[datetime] = Field(
        None, description="Optional timestamp for after-registration likes"
    )

    class Config:
        schema_extra = {
            "example": {
                "post_id": "8e1b92d2-634e-4b5f-8d53-2fcb62e0a75c",
                "user_id": "12345678-abcd-1234-abcd-1234567890ab",
                "like_status": True,
                "pseudo_timestamp": "2024-11-22T10:30:00Z"
            }
        }

class PostLikesUpdate(BaseModel):
    like_status: Optional[bool] = None
    pseudo_timestamp: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "like_status": True,
                "pseudo_timestamp": "2024-11-22T15:00:00Z"
            }
        }




class Comment(BaseModel):
    post_id: str = Field(..., description="ID of the post")
    user_id: str = Field(..., description="ID of the user who made the comment")
    comment_text: str = Field(..., description="Content of the comment")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Time of comment creation")
    sentiment_score: Optional[float] = Field(None, description="Sentiment score of the comment")
    sentiment_category: Optional[str] = Field(None, description="Category of sentiment (e.g., 'positive', 'neutral', 'negative')")
    replies: List[dict] = Field(
        default_factory=list, 
        description="Replies to the comment, with details"
    )

    class Config:
        schema_extra = {
            "example": {
                "post_id": "8e1b92d2-634e-4b5f-8d53-2fcb62e0a75c",
                "user_id": "12345678-abcd-1234-abcd-1234567890ab",
                "comment_text": "This is an amazing post!",
                "timestamp": "2024-11-22T10:30:00Z",
                "sentiment_score": 0.9,
                "sentiment_category": "positive",
                "replies": [
                    {
                        "reply_id": "r1234567",
                        "replier_user_id": "98765432-abcd-1234-abcd-1234567890ba",
                        "reply_text": "Absolutely agree!",
                        "timestamp": "2024-11-22T11:00:00Z"
                    }
                ]
            }
        }

class PostCommentsUpdate(BaseModel):
    comment_text: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_category: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "comment_text": "Updated comment text",
                "sentiment_score": 0.85,
                "sentiment_category": "positive"
            }
        }



class HighlightInteraction(BaseModel):
    highlight_id: str = Field(..., description="ID of the highlight")
    user_id: str = Field(..., description="ID of the user interacting with the highlight")
    view_count: int = Field(default=0, description="Number of views")
    like_status: bool = Field(..., description="True if liked, False otherwise")

    class Config:
        schema_extra = {
            "example": {
                "highlight_id": "h1234567",
                "user_id": "12345678-abcd-1234-abcd-1234567890ab",
                "view_count": 10,
                "like_status": True
            }
        }

class HighlightInteractionsUpdate(BaseModel):
    view_count: Optional[int] = None
    like_status: Optional[bool] = None

    class Config:
        schema_extra = {
            "example": {
                "view_count": 150,
                "like_status": True
            }
        }


class ProfileVisit(BaseModel):
    user_id: str = Field(..., description="ID of the visited user")
    visitor_user_id: str = Field(..., description="ID of the visiting user")
    visit_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the visit")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "12345678-abcd-1234-abcd-1234567890ab",
                "visitor_user_id": "98765432-abcd-1234-abcd-1234567890ba",
                "visit_timestamp": "2024-11-22T10:30:00Z"
            }
        }


class ProfileVisitsUpdate(BaseModel):
    visit_timestamp: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "visit_timestamp": "2024-11-23T14:30:00Z"
            }
        }



class Mention(BaseModel):
    mentioned_user_id: str = Field(..., description="ID of the mentioned user")
    mentioning_user_id: str = Field(..., description="ID of the user who mentioned")
    post_id: Optional[str] = Field(None, description="ID of the post where the mention occurred")
    comment_id: Optional[str] = Field(None, description="ID of the comment where the mention occurred")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the mention")

    class Config:
        schema_extra = {
            "example": {
                "mentioned_user_id": "12345678-abcd-1234-abcd-1234567890ab",
                "mentioning_user_id": "98765432-abcd-1234-abcd-1234567890ba",
                "post_id": "8e1b92d2-634e-4b5f-8d53-2fcb62e0a75c",
                "timestamp": "2024-11-22T10:30:00Z"
            }
        }

class MentionsUpdate(BaseModel):
    timestamp: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "timestamp": "2024-11-23T18:45:00Z"
            }
        }




class Share(BaseModel):
    post_id: Optional[str] = Field(None, description="ID of the shared post")
    highlight_id: Optional[str] = Field(None, description="ID of the shared highlight")
    user_id: str = Field(..., description="ID of the user who shared the content")
    shared_with_user_id: str = Field(..., description="ID of the user with whom the content was shared")
    share_timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the share")

    class Config:
        schema_extra = {
            "example": {
                "post_id": "8e1b92d2-634e-4b5f-8d53-2fcb62e0a75c",
                "highlight_id": None,
                "user_id": "12345678-abcd-1234-abcd-1234567890ab",
                "shared_with_user_id": "98765432-abcd-1234-abcd-1234567890ba",
                "share_timestamp": "2024-11-22T10:30:00Z"
            }
        }

class SharesUpdate(BaseModel):
    share_timestamp: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "share_timestamp": "2024-11-23T19:00:00Z"
            }
        }



class Activity(BaseModel):
    user_id: str = Field(..., description="ID of the user")
    activity_type: str = Field(..., description="Type of activity performed")
    source_device: str = Field(..., description="Device used to perform the activity")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the activity")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "12345678-abcd-1234-abcd-1234567890ab",
                "activity_type": "Login",
                "source_device": "Mobile",
                "timestamp": "2024-11-22T10:30:00Z"
            }
        }

class ActivitiesUpdate(BaseModel):
    activity_type: Optional[str] = None
    source_device: Optional[str] = None
    timestamp: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "activity_type": "login",
                "source_device": "mobile",
                "timestamp": "2024-11-23T20:15:00Z"
            }
        }


class Notification(BaseModel):
    user_id: str = Field(..., description="ID of the user receiving the notification")
    notification_type: str = Field(..., description="Type of notification (e.g., 'like', 'comment')")
    trigger_event: str = Field(..., description="Event that triggered the notification")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of the notification")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "12345678-abcd-1234-abcd-1234567890ab",
                "notification_type": "like",
                "trigger_event": "Your post received a like",
                "timestamp": "2024-11-22T10:30:00Z"
            }
        }

class NotificationsUpdate(BaseModel):
    notification_type: Optional[str] = None
    trigger_event: Optional[str] = None
    timestamp: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "notification_type": "friend_request",
                "trigger_event": "User123 sent a friend request",
                "timestamp": "2024-11-23T21:30:00Z"
            }
        }


