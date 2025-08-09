from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup

facebook_router = Blueprint('facebook_api', __name__)

@facebook_router.route('/', methods=['GET'])
def get_business_data():
    return jsonify({"message":"Hello Facebook Router"})


