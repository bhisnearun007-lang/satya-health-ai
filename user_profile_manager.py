# A simple JSON database for our users
user_db = {
    "user_001": {
        "name": "Rahul",
        "conditions": ["Celiac Disease", "Lactose Intolerance"],
        "severity": "High"
    },
    "user_002": {
        "name": "Priya",
        "conditions": ["Type 2 Diabetes"],
        "severity": "Medium"
    }
}

def get_user_profile(user_id):
    return user_db.get(user_id, {"conditions": ["General Health"], "severity": "Low"})