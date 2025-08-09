from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup

planner_router = Blueprint('planner_api', __name__)

@planner_router.route('/', methods=['GET'])
def get_business_data():
    return jsonify({"message":"Hello planner Router"})


