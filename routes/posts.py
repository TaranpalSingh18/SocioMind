from flask import Blueprint, jsonify, request
from models.model import WeeklyModel
import random

post_router = Blueprint("post", __name__)

days_of_week = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}

def post_frequency(payload: WeeklyModel):
    freq = payload.frequency
    days = payload.days

    day_list = []
    posts_list = []
    
    if days is None or len(days) == 0:
        random.seed(42)  
        day_numbers = random.sample(range(1, 8), min(freq, 7)) 
        
        for j, day_num in enumerate(day_numbers, 1):
            posts_list.append({
                days_of_week[day_num]: {
                    f"Post Number: {j}": f"Content of Post {j}"
                }
            })
    else:
        for j, day in enumerate(days, 1):
            posts_list.append({
                day: {
                    f"Post Number: {j}": f"Content of Post {j}"
                }
            })

    return posts_list  

@post_router.route('/week', methods=["POST"])
def get_content_api():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        payload = WeeklyModel(**data)
        result = post_frequency(payload)
        
        return jsonify({
            "success": True,
            "posts": result,
            "total_posts": len(result)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@post_router.route('/health', methods=["GET"])
def health():
    return jsonify({
        "message": "health update",
        "status": "Healthy Condition"
    })