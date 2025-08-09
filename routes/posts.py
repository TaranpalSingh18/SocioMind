from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup

post_router = Blueprint('post_api', __name__)

@post_router.route('/', methods=['GET'])
def get_business_data():
    return jsonify({"message":"Hello Post Router"})


