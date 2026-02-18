from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum
import uuid

app = FastAPI(title="AI-DOS Collaboration Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class Role(str, Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"

class ResourceType(str, Enum):
    EXPERIMENT = "experiment"
    DATASET = "dataset"
    MODEL = "model"
    DEPLOYMENT = "deployment"

class ActivityType(str, Enum):
    CREATED = "created"
    SHARED = "shared"
    COMMENTED = "commented"
    DEPLOYED = "deployed"
    UPDATED = "updated"

# Models
class Team(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    owner_id: str
    created_at: Optional[str] = None

class TeamMember(BaseModel):
    team_id: str
    user_id: str
    role: Role
    joined_at: Optional[str] = None

class ShareRequest(BaseModel):
    resource_type: ResourceType
    resource_id: str
    shared_by: str
    shared_with: str
    role: Role
    message: Optional[str] = None

class Comment(BaseModel):
    id: Optional[str] = None
    resource_type: ResourceType
    resource_id: str
    user_id: str
    text: str
    created_at: Optional[str] = None

class Activity(BaseModel):
    id: Optional[str] = None
    user_id: str
    activity_type: ActivityType
    resource_type: ResourceType
    resource_id: str
    resource_name: str
    team_id: Optional[str] = None
    timestamp: Optional[str] = None

class Notification(BaseModel):
    id: Optional[str] = None
    user_id: str
    title: str
    message: str
    read: bool = False
    created_at: Optional[str] = None

# Storage
teams = {}
team_members = {}
shares = {}
comments = {}
activities = []
notifications = {}

@app.get("/")
def root():
    return {
        "service": "AI-DOS Collaboration Service",
        "version": "1.0.0",
        "status": "running",
        "features": [
            "teams",
            "sharing",
            "comments",
            "activity_feed",
            "notifications"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "collab"}

# Teams
@app.post("/teams")
def create_team(team: Team):
    team.id = f"team_{uuid.uuid4().hex[:8]}"
    team.created_at = datetime.utcnow().isoformat()
    teams[team.id] = team
    
    # Add owner as member
    member = TeamMember(
        team_id=team.id,
        user_id=team.owner_id,
        role=Role.OWNER,
        joined_at=datetime.utcnow().isoformat()
    )
    if team.id not in team_members:
        team_members[team.id] = []
    team_members[team.id].append(member)
    
    return team

@app.get("/teams")
def list_teams(user_id: Optional[str] = None):
    if user_id:
        user_teams = []
        for team_id, members in team_members.items():
            if any(m.user_id == user_id for m in members):
                user_teams.append(teams[team_id])
        return user_teams
    return list(teams.values())

@app.get("/teams/{team_id}")
def get_team(team_id: str):
    if team_id not in teams:
        raise HTTPException(status_code=404, detail="Team not found")
    return teams[team_id]

@app.post("/teams/{team_id}/members")
def add_team_member(team_id: str, member: TeamMember):
    if team_id not in teams:
        raise HTTPException(status_code=404, detail="Team not found")
    
    member.team_id = team_id
    member.joined_at = datetime.utcnow().isoformat()
    
    if team_id not in team_members:
        team_members[team_id] = []
    team_members[team_id].append(member)
    
    # Create notification
    notif = Notification(
        id=f"notif_{uuid.uuid4().hex[:8]}",
        user_id=member.user_id,
        title="Added to Team",
        message=f"You've been added to {teams[team_id].name}",
        created_at=datetime.utcnow().isoformat()
    )
    if member.user_id not in notifications:
        notifications[member.user_id] = []
    notifications[member.user_id].append(notif)
    
    return member

@app.get("/teams/{team_id}/members")
def get_team_members(team_id: str):
    if team_id not in teams:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_members.get(team_id, [])

# Sharing
@app.post("/share")
def share_resource(share: ShareRequest):
    share_id = f"share_{uuid.uuid4().hex[:8]}"
    share_data = {
        "id": share_id,
        **share.dict(),
        "shared_at": datetime.utcnow().isoformat()
    }
    
    key = f"{share.resource_type}_{share.resource_id}"
    if key not in shares:
        shares[key] = []
    shares[key].append(share_data)
    
    # Create notification
    notif = Notification(
        id=f"notif_{uuid.uuid4().hex[:8]}",
        user_id=share.shared_with,
        title=f"{share.resource_type.value.title()} Shared",
        message=f"A {share.resource_type.value} has been shared with you" + (f": {share.message}" if share.message else ""),
        created_at=datetime.utcnow().isoformat()
    )
    if share.shared_with not in notifications:
        notifications[share.shared_with] = []
    notifications[share.shared_with].append(notif)
    
    # Log activity
    activity = Activity(
        id=f"activity_{uuid.uuid4().hex[:8]}",
        user_id=share.shared_by,
        activity_type=ActivityType.SHARED,
        resource_type=share.resource_type,
        resource_id=share.resource_id,
        resource_name=f"{share.resource_type.value}_{share.resource_id}",
        timestamp=datetime.utcnow().isoformat()
    )
    activities.append(activity)
    
    return share_data

@app.get("/share/{resource_type}/{resource_id}")
def get_shares(resource_type: str, resource_id: str):
    key = f"{resource_type}_{resource_id}"
    return shares.get(key, [])

@app.get("/shared-with-me/{user_id}")
def get_shared_with_me(user_id: str):
    shared_items = []
    for key, share_list in shares.items():
        for share in share_list:
            if share["shared_with"] == user_id:
                shared_items.append(share)
    return shared_items

# Comments
@app.post("/comments")
def create_comment(comment: Comment):
    comment.id = f"comment_{uuid.uuid4().hex[:8]}"
    comment.created_at = datetime.utcnow().isoformat()
    
    key = f"{comment.resource_type}_{comment.resource_id}"
    if key not in comments:
        comments[key] = []
    comments[key].append(comment)
    
    # Log activity
    activity = Activity(
        id=f"activity_{uuid.uuid4().hex[:8]}",
        user_id=comment.user_id,
        activity_type=ActivityType.COMMENTED,
        resource_type=comment.resource_type,
        resource_id=comment.resource_id,
        resource_name=f"{comment.resource_type.value}_{comment.resource_id}",
        timestamp=datetime.utcnow().isoformat()
    )
    activities.append(activity)
    
    return comment

@app.get("/comments/{resource_type}/{resource_id}")
def get_comments(resource_type: str, resource_id: str):
    key = f"{resource_type}_{resource_id}"
    return comments.get(key, [])

# Activity Feed
@app.post("/activity")
def log_activity(activity: Activity):
    activity.id = f"activity_{uuid.uuid4().hex[:8]}"
    activity.timestamp = datetime.utcnow().isoformat()
    activities.append(activity)
    return activity

@app.get("/activity")
def get_activity_feed(user_id: Optional[str] = None, team_id: Optional[str] = None, limit: int = 50):
    filtered = activities
    
    if user_id:
        filtered = [a for a in filtered if a.user_id == user_id]
    
    if team_id:
        filtered = [a for a in filtered if a.team_id == team_id]
    
    # Sort by timestamp descending
    filtered = sorted(filtered, key=lambda x: x.timestamp, reverse=True)
    
    return filtered[:limit]

# Notifications
@app.get("/notifications/{user_id}")
def get_notifications(user_id: str, unread_only: bool = False):
    user_notifs = notifications.get(user_id, [])
    
    if unread_only:
        user_notifs = [n for n in user_notifs if not n.read]
    
    return sorted(user_notifs, key=lambda x: x.created_at, reverse=True)

@app.put("/notifications/{notification_id}/read")
def mark_notification_read(notification_id: str, user_id: str):
    user_notifs = notifications.get(user_id, [])
    
    for notif in user_notifs:
        if notif.id == notification_id:
            notif.read = True
            return notif
    
    raise HTTPException(status_code=404, detail="Notification not found")

@app.get("/notifications/{user_id}/unread-count")
def get_unread_count(user_id: str):
    user_notifs = notifications.get(user_id, [])
    unread = len([n for n in user_notifs if not n.read])
    return {"count": unread}

# Permissions Check
@app.get("/permissions/{resource_type}/{resource_id}/{user_id}")
def check_permissions(resource_type: str, resource_id: str, user_id: str):
    key = f"{resource_type}_{resource_id}"
    share_list = shares.get(key, [])
    
    for share in share_list:
        if share["shared_with"] == user_id:
            return {
                "has_access": True,
                "role": share["role"],
                "can_edit": share["role"] in [Role.OWNER, Role.EDITOR],
                "can_view": True
            }
    
    return {
        "has_access": False,
        "role": None,
        "can_edit": False,
        "can_view": False
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
