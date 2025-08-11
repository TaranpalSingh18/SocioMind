from flask import Flask
from flask_cors import CORS

from routes.business_api import business_router
from routes.content_api import content_router
from routes.facebook import facebook_router
from routes.news import news_router
from routes.preview import preview_router
from routes.posts import post_router
# from routes.testing import testing_router

app = Flask(__name__)
CORS(app)

app.register_blueprint(business_router, url_prefix='/business')
app.register_blueprint(content_router, url_prefix='/content')
app.register_blueprint(facebook_router, url_prefix='/facebook')
app.register_blueprint(news_router, url_prefix='/news')
app.register_blueprint(preview_router, url_prefix='/preview')
app.register_blueprint(post_router, url_prefix='/post')
# app.register_blueprint(testing_router, url_prefix='/testing')

app.get('/')
async def home():
    return {"message":"Hello World"}

if __name__ == '__main__':
    app.run(debug=True)




