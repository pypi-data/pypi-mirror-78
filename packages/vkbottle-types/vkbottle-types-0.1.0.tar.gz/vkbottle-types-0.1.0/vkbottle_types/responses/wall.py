from .base_response import BaseResponse
from vkbottle_types.objects import users, wall, groups
from typing import Optional, Any, List, Union
import typing


class CreateCommentResponse(BaseResponse):
    response: Optional["CreateCommentResponseModel"] = None


class EditResponse(BaseResponse):
    response: Optional["EditResponseModel"] = None


class GetByIdExtendedResponse(BaseResponse):
    response: Optional["GetByIdExtendedResponseModel"] = None


class GetByIdResponse(BaseResponse):
    response: Optional["GetByIdResponseModel"] = None


class GetCommentExtendedResponse(BaseResponse):
    response: Optional["GetCommentExtendedResponseModel"] = None


class GetCommentResponse(BaseResponse):
    response: Optional["GetCommentResponseModel"] = None


class GetCommentsExtendedResponse(BaseResponse):
    response: Optional["GetCommentsExtendedResponseModel"] = None


class GetCommentsResponse(BaseResponse):
    response: Optional["GetCommentsResponseModel"] = None


class GetRepostsResponse(BaseResponse):
    response: Optional["GetRepostsResponseModel"] = None


class GetExtendedResponse(BaseResponse):
    response: Optional["GetExtendedResponseModel"] = None


class GetResponse(BaseResponse):
    response: Optional["GetResponseModel"] = None


class PostAdsStealthResponse(BaseResponse):
    response: Optional["PostAdsStealthResponseModel"] = None


class PostResponse(BaseResponse):
    response: Optional["PostResponseModel"] = None


class RepostResponse(BaseResponse):
    response: Optional["RepostResponseModel"] = None


class SearchExtendedResponse(BaseResponse):
    response: Optional["SearchExtendedResponseModel"] = None


class SearchResponse(BaseResponse):
    response: Optional["SearchResponseModel"] = None


class CreateCommentResponseModel(BaseResponse):
    comment_id: Optional[int] = None


class EditResponseModel(BaseResponse):
    post_id: Optional[int] = None


class GetByIdExtendedResponseModel(BaseResponse):
    items: Optional[List["wall.WallpostFull"]] = None
    profiles: Optional[List["users.UserFull"]] = None
    groups: Optional[List["groups.GroupFull"]] = None


GetByIdResponseModel = List["wall.WallpostFull"]


class GetCommentExtendedResponseModel(BaseResponse):
    items: Optional[List["wall.WallComment"]] = None
    profiles: Optional[List["users.User"]] = None
    groups: Optional[List["groups.Group"]] = None


class GetCommentResponseModel(BaseResponse):
    items: Optional[List["wall.WallComment"]] = None


class GetCommentsExtendedResponseModel(BaseResponse):
    count: Optional[int] = None
    items: Optional[List["wall.WallComment"]] = None
    show_reply_button: Optional[bool] = None
    can_post: Optional[bool] = None
    groups_can_post: Optional[bool] = None
    current_level_count: Optional[int] = None
    profiles: Optional[List["users.User"]] = None
    groups: Optional[List["groups.Group"]] = None


class GetCommentsResponseModel(BaseResponse):
    count: Optional[int] = None
    items: Optional[List["wall.WallComment"]] = None
    can_post: Optional[bool] = None
    groups_can_post: Optional[bool] = None
    current_level_count: Optional[int] = None


class GetRepostsResponseModel(BaseResponse):
    items: Optional[List["wall.WallpostFull"]] = None
    profiles: Optional[List["users.User"]] = None
    groups: Optional[List["groups.Group"]] = None


class GetExtendedResponseModel(BaseResponse):
    count: Optional[int] = None
    items: Optional[List["wall.WallpostFull"]] = None
    profiles: Optional[List["users.UserFull"]] = None
    groups: Optional[List["groups.GroupFull"]] = None


class GetResponseModel(BaseResponse):
    count: Optional[int] = None
    items: Optional[List["wall.WallpostFull"]] = None


class PostAdsStealthResponseModel(BaseResponse):
    post_id: Optional[int] = None


class PostResponseModel(BaseResponse):
    post_id: Optional[int] = None


class RepostResponseModel(BaseResponse):
    success: Optional[int] = None
    post_id: Optional[int] = None
    reposts_count: Optional[int] = None
    likes_count: Optional[int] = None


class SearchExtendedResponseModel(BaseResponse):
    count: Optional[int] = None
    items: Optional[List["wall.WallpostFull"]] = None
    profiles: Optional[List["users.UserFull"]] = None
    groups: Optional[List["groups.GroupFull"]] = None


class SearchResponseModel(BaseResponse):
    count: Optional[int] = None
    items: Optional[List["wall.WallpostFull"]] = None
