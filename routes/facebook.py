from flask import Blueprint, jsonify

facebook_router = Blueprint("facebook_router",__name__)


@facebook_router.route("/connect", methods = ["POST"])
def facebook_connection():
    return jsonify([
        "message: Success",
        "Token: abc1234"
    ])


@facebook_router.route("/", methods = ["GET"])
def health_update():
    return jsonify([
        "message: Health Update",
        "status: The route is healthy"
    ])