from typing import Optional
from dataclasses import dataclass


@dataclass
class User:
    id: str
    permanent_id: int
    name: str
    profile_image_url: str
    team_only: bool
    followees_count: int
    followers_count: int
    items_count: int
    description: Optional[str] = None
    organization: Optional[str] = None
    location: Optional[str] = None
    facebook_id: Optional[str] = None
    github_login_name: Optional[str] = None
    linkedin_id: Optional[str] = None
    twitter_screen_name: Optional[str] = None
    website_url: Optional[str] = None


@dataclass
class Comment:
    body: str
    created_at: str
    id: str
    rendered_body: str
    updated_at: str
    user: User