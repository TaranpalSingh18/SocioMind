from flask import Blueprint, request, jsonify
import requests
from bs4 import BeautifulSoup

content_router = Blueprint('content_api', __name__)


@content_router.route('/', methods=['GET'])
def get_business_data():
    return jsonify({"message":"Hello Content Router"})


