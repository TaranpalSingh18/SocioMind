from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup

news_router = Blueprint('news_api', __name__)

@news_router.route('/', methods=['GET'])
def get_business_data():
    return jsonify({"message":"Hello news Router"})


