from flask import Flask
from flask_cors import CORS

from routes.business_api import business_router
from routes.content import content_router
from routes.facebook import facebook_router
from routes.news_api import news_router
from routes.planner import planner_router
from routes.posts import post_router

app = Flask(__name__)
CORS(app)

app.register_blueprint(business_router, url_prefix='/business')
app.register_blueprint(content_router, url_prefix='/content')
app.register_blueprint(facebook_router, url_prefix='/facebook')
app.register_blueprint(news_router, url_prefix='/news')
app.register_blueprint(planner_router, url_prefix='/planner')
app.register_blueprint(post_router, url_prefix='/post')

app.get('/')
async def home():
    return {"message":"Hello World"}

if __name__ == '__main__':
    app.run(debug=True)




