from flask import Blueprint, jsonify, request
from models.model import WeeklyModel
import random
from mockdata.mock_post_data import MOCK_POSTS

post_router = Blueprint("post", __name__)

days_of_week = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}

def create_weekly_schedule(payload: WeeklyModel):
    freq = payload.frequency
    preferred_days = payload.days
    
    available_posts = MOCK_POSTS["posts"]
    
    if preferred_days and len(preferred_days) > 0:
        valid_days = [day for day in preferred_days if day in days_of_week.values()]
        if not valid_days:
            return {"error": "Invalid day names provided. Use: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"}
        
        filtered_posts = [post for post in available_posts if post["day"] in valid_days]
        
        if len(filtered_posts) < freq:
            other_posts = [post for post in available_posts if post["day"] not in valid_days]
            filtered_posts.extend(other_posts)
    else:
        filtered_posts = available_posts
    
 
    random.shuffle(filtered_posts)
    
    selected_posts = filtered_posts[:min(freq, len(filtered_posts))]
    
    weekly_schedule = {}
    
    if preferred_days and len(preferred_days) > 0:
        for i, post in enumerate(selected_posts):
            day_index = i % len(preferred_days)
            day = preferred_days[day_index]
            
            if day not in weekly_schedule:
                weekly_schedule[day] = []
            
            weekly_schedule[day].append({
                "post_id": post["id"],
                "caption": post["caption"],
                "scheduled_time": post["scheduledTime"],
                "post_type": post["postType"],
                "platform": post["platform"],
                "engagement_rate": post["engagement_rate"]
            })
    else:
        if freq <= 7:
            for i, post in enumerate(selected_posts):
                day_num = (i % 7) + 1
                day_name = days_of_week[day_num]
                
                if day_name not in weekly_schedule:
                    weekly_schedule[day_name] = []
                
                weekly_schedule[day_name].append({
                    "post_id": post["id"],
                    "caption": post["caption"],
                    "scheduled_time": post["scheduledTime"],
                    "post_type": post["postType"],
                    "platform": post["platform"],
                    "engagement_rate": post["engagement_rate"]
                })
        else:
            posts_per_day = freq // 7
            extra_posts = freq % 7
            
            for i, post in enumerate(selected_posts):
                day_num = (i // posts_per_day) + 1
                if extra_posts > 0 and i >= (posts_per_day * 7):
                    day_num = (i - (posts_per_day * 7)) + 1
                
                day_name = days_of_week[day_num]
                
                if day_name not in weekly_schedule:
                    weekly_schedule[day_name] = []
                
                weekly_schedule[day_name].append({
                    "post_id": post["id"],
                    "caption": post["caption"],
                    "scheduled_time": post["scheduledTime"],
                    "post_type": post["postType"],
                    "platform": post["platform"],
                    "engagement_rate": post["engagement_rate"]
                })
    
    return weekly_schedule

@post_router.route('/week', methods=["POST"])
def get_weekly_schedule():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                "error": "No JSON data provided",
                "message": "Please provide frequency and optional preferred days"
            }), 400
            
        payload = WeeklyModel(**data)
        
        if payload.frequency <= 0:
            return jsonify({
                "error": "Invalid frequency",
                "message": "Frequency must be greater than 0"
            }), 400
        
        if payload.frequency > 21:  # Maximum 3 posts per day for 7 days
            return jsonify({
                "error": "Frequency too high",
                "message": "Maximum frequency allowed is 21 posts per week (3 per day)"
            }), 400
        
        weekly_schedule = create_weekly_schedule(payload)
        
        if "error" in weekly_schedule:
            return jsonify(weekly_schedule), 400
        
        total_posts = sum(len(posts) for posts in weekly_schedule.values())
        days_with_posts = len(weekly_schedule)
        
        return jsonify({
            "success": True,
            "message": f"Weekly schedule created with {total_posts} posts across {days_with_posts} days",
            "weekly_schedule": weekly_schedule,
            "summary": {
                "total_posts": total_posts,
                "days_with_posts": days_with_posts,
                "frequency_requested": payload.frequency,
                "preferred_days": payload.days if payload.days else "Auto-assigned",
                "schedule_type": "Custom" if payload.days else "Auto-generated"
            }
        })
    
    except Exception as e:
        return jsonify({
            "error": "Failed to create weekly schedule",
            "message": str(e)
        }), 500

@post_router.route('/health', methods=["GET"])
def health():
    return jsonify({
        "message": "Weekly Planner API is healthy",
        "status": "Healthy"
    })