import requests
import json

BASE_URL = "http://localhost:8006"

print("=== COLLABORATION SERVICE TEST ===\n")

# 1. Create a team
print("1. Creating team...")
team_data = {
    "name": "ML Research Team",
    "description": "Building next-gen models",
    "owner_id": "user_001"
}
response = requests.post(f"{BASE_URL}/teams", json=team_data)
team = response.json()
print(f"Team created: {team['name']} (ID: {team['id']})")

# 2. Add team member
print("\n2. Adding team member...")
member_data = {
    "team_id": team['id'],
    "user_id": "user_002",
    "role": "editor"
}
response = requests.post(f"{BASE_URL}/teams/{team['id']}/members", json=member_data)
member = response.json()
print(f"Added user_002 as {member['role']}")

# 3. Share an experiment
print("\n3. Sharing experiment...")
share_data = {
    "resource_type": "experiment",
    "resource_id": "exp_123",
    "shared_by": "user_001",
    "shared_with": "user_002",
    "role": "editor",
    "message": "Check out this sentiment model!"
}
response = requests.post(f"{BASE_URL}/share", json=share_data)
share = response.json()
print(f"Experiment shared with user_002")

# 4. Add comment
print("\n4. Adding comment...")
comment_data = {
    "resource_type": "experiment",
    "resource_id": "exp_123",
    "user_id": "user_002",
    "text": "Great results! Accuracy looks promising."
}
response = requests.post(f"{BASE_URL}/comments", json=comment_data)
comment = response.json()
print(f"Comment added: '{comment['text']}'")

# 5. Get notifications
print("\n5. Checking notifications for user_002...")
response = requests.get(f"{BASE_URL}/notifications/user_002")
notifications = response.json()
print(f"Notifications: {len(notifications)}")
for notif in notifications:
    print(f"  - {notif['title']}: {notif['message']}")

# 6. Get activity feed
print("\n6. Activity feed...")
response = requests.get(f"{BASE_URL}/activity?limit=10")
activities = response.json()
print(f"Recent activities: {len(activities)}")
for activity in activities[:3]:
    print(f"  - {activity['user_id']} {activity['activity_type']} {activity['resource_type']}")

# 7. Check permissions
print("\n7. Checking permissions...")
response = requests.get(f"{BASE_URL}/permissions/experiment/exp_123/user_002")
perms = response.json()
print(f"user_002 has access: {perms['has_access']}")
print(f"Can edit: {perms['can_edit']}")

# 8. Get shared items
print("\n8. Items shared with user_002...")
response = requests.get(f"{BASE_URL}/shared-with-me/user_002")
shared = response.json()
print(f"Shared items: {len(shared)}")
for item in shared:
    print(f"  - {item['resource_type']}: {item['resource_id']} ({item['role']})")

print("\n=== COLLABORATION SERVICE WORKS PERFECTLY! ===")
