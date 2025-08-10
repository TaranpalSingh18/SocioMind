from flask import Blueprint, jsonify, request
from sqlalchemy.sql.elements import and_
from mockdata.mock_post_data import MOCK_POSTS

preview_router = Blueprint('preview', __name__)

@preview_router.route("/view", methods = ["GET"])
def get_all_week_posts():
    posts = MOCK_POSTS["posts"]

    final_list=[]
    for i in posts:
        if i["scheduled_this_week"] is 1:
            final_list.append(i)

    return jsonify(final_list)

@preview_router.route('/edit/<string:id>', methods=["PUT"])
def edit_post(id: str):
    try:
        posts = MOCK_POSTS["posts"]
        post_found = None
        post_index = -1
        
        for index, post in enumerate(posts):
            if post["id"] == id:
                post_found = post
                post_index = index
                break
        
        if post_found is None:
            return jsonify({"message": "The post of the mentioned id does not exist"}), 404
        
        request_data = request.get_json()
        
        if not request_data:
            return jsonify({"message": "No data provided"}), 400
        
        editable_fields = [
            "caption", "day", "scheduledTime", "platform", 
            "postType", "isPublished", "scheduled_this_week"
        ]
        
        updated_fields = []
        for field in editable_fields:
            if field in request_data:
                post_found[field] = request_data[field]
                updated_fields.append(field)
        
        if "isPublished" in request_data and request_data["isPublished"] == 1:
            if post_found.get("likes", 0) > 0 or post_found.get("comments", 0) > 0 or post_found.get("shares", 0) > 0:
                total_engagement = post_found.get("likes", 0) + post_found.get("comments", 0) + post_found.get("shares", 0)
                estimated_reach = 1000
                post_found["engagement_rate"] = round((total_engagement / estimated_reach) * 100, 1)
        
        if "isPublished" in request_data and request_data["isPublished"] == 0:
            post_found["engagement_rate"] = 0
        
        MOCK_POSTS["posts"][post_index] = post_found
        
        return jsonify({
            "message": "Post updated successfully",
            "updated_fields": updated_fields,
            "post": post_found
        }), 200
        
    except Exception as e:
        return jsonify({"message": f"Error updating post: {str(e)}"}), 500



@preview_router.route('/delete/<string:id>', methods=["DELETE"])
def delete_post(id: str):
    try:
        posts = MOCK_POSTS["posts"]
        post_found = None
        post_index = -1
        
        for index, post in enumerate(posts):
            if post["id"] == id and post["isPublished"] is 0:
                post_found = post
                post_index = index
                break
        
        if post_found is None:
            return jsonify({"message": "The post of the mentioned id does not exist or is already Published"}), 404

        del MOCK_POSTS["posts"][post_index]

        return jsonify({
            "message": f"The post with post_id: {id} has been deleted successfully",
            "remaining_posts": len(MOCK_POSTS["posts"])
        }), 200
        

    except Exception as e:
        return jsonify({
            "message": "An error occurred while deleting the post",
            "error": str(e)
        }), 500
        
   
@preview_router.route('/health', methods=['GET'])
def get_health():
    return jsonify([
        "message: Health Status",
        "status: Server is Healthy"
        ])


