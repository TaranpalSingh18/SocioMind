from flask import Flask, Blueprint, jsonify, request
import requests
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import os 
from dotenv import load_dotenv
from models.model import ContentModel
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')

def get_response(payload: ContentModel):
    business_profile = payload.business_profile
    industry_news = payload.industry_news
    tone = payload.tone
    frequency = payload.frequency
    post_type = payload.post_type

    prompt = PromptTemplate(
        template="""You are a professional social media content creator.  
Your task is to create {frequency} ready-to-publish post captions per week for {business_profile}.  

**Inputs**:
- Business profile: {business_profile}
- Industry news or trends: {industry_news}
- Tone: {tone}  (e.g., professional, witty, friendly)
- Post type: {post_type}  (e.g., promotional offer, tip, update, seasonal greeting)
- Frequency : {frequency}

**Instructions**:
1. Create a list of short, engaging, and platform-friendly post captions.
2. Match the {tone} specified.
3. Ensure each caption aligns with the selected {post_type}.
4. Incorporate any relevant {industry_news} naturally into the captions.
5. Include relevant hashtags when suitable (2–5 per post).
6. Make each caption unique — avoid repetitive wording.
7. Output the posts in a numbered list, each on a new line.

**Output format**:
Post 1: <caption>
Post 2: <caption> 
.
.
till you reach the value of frequency 
...""", 
        input_variables=["business_profile", "industry_news", "tone", "post_type", "frequency"]
    )

    llm = ChatGroq(model="llama-3.1-8b-instant", api_key=groq_api_key)

    chain = prompt | llm | StrOutputParser()
    result = chain.invoke({
        "business_profile": business_profile,
        "industry_news": industry_news,
        "tone": tone,
        "post_type": post_type,
        "frequency": frequency
    })
    format_resulted = format_text(result)

    return format_resulted

def format_text(text: str) -> dict:
    lines = text.strip().split('\n\n')
    
    if len(lines) <= 1:
        lines = text.strip().split('\n')
    
    captions = []
    
    for j, line in enumerate(lines):
        line = line.strip()  
        if line and len(line) > 10: 
            if line.startswith('Post ') and ':' in line:
                line = line.split(':', 1)[1].strip()
            
            caption_dict = {f"POST {j+1}": line}
            captions.append(caption_dict)  
    
    return {
        "captions": captions,
        "total_posts": len(captions)
    }

content_router = Blueprint('content_api', __name__)

@content_router.route('/captions', methods=["POST"])
def get_content():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        payload = ContentModel(**data)
        response = get_response(payload)
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@content_router.route('/health', methods=['GET'])
def get_business_data():
    return jsonify({
        "message": "System Health Checker",
        "status": "healthy"
    })