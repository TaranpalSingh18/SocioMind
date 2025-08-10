from flask import Blueprint, jsonify, request
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import JsonOutputParser
import json
import os

content_router = Blueprint("content", __name__)

def get_news(keywords: list):
    final_list = []
    
    print(f"Processing keywords: {keywords}")
    
    for keyword in keywords:
        try:
            url = f"https://news.google.com/search?q={keyword}&hl=en&gl=US"
            print(f"Processing URL: {url}")
            
            documents = WebBaseLoader(url)
            docs = documents.load()
            print(f"Loaded {len(docs)} documents for keyword: {keyword}")

            text_docs = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            text_splitter = text_docs.split_documents(docs)
            print(f"Split into {len(text_splitter)} chunks")
            
            for chunk in text_splitter:
                if chunk.page_content and chunk.page_content.strip():
                    final_list.append(chunk.page_content.strip())
                    
        except Exception as e:
            print(f"Error processing keyword '{keyword}': {str(e)}")
            continue
        
    if not final_list:
        return {"error": "No content retrieved from any source"}
    
    print(f"Total chunks collected: {len(final_list)}")
    
    try:
        context_chunks = final_list[:5]
        context = "\n\n".join(context_chunks)
        
        print(f"Context length: {len(context)} characters")
        prompt_text = f"""
        You are a helpful AI assistant. Based on the context provided, extract the top 5 most relevant news items.
        
        Context:
        {context}
        
        IMPORTANT: You must respond with ONLY valid JSON, no additional text before or after. Use this exact format:

        {{"news": [{{"title": "News title here", "summary": "Brief summary here", "relevance_score": "High"}}]}}

        Extract up to 5 news items from the context. If you find fewer than 5, that's fine.
        """

        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0
        )

        print("Invoking LLM...")
        response = llm.invoke(prompt_text)
        print(f"LLM Response type: {type(response)}")
        
        if hasattr(response, 'content'):
            result_text = response.content
        elif isinstance(response, str):
            result_text = response
        else:
            result_text = str(response)
        
        print(f"Result text: {result_text[:200]}...")
        try:
            result_text = result_text.strip()
            if '{' in result_text and '}' in result_text:
                start_idx = result_text.find('{')
                end_idx = result_text.rfind('}') + 1
                json_text = result_text[start_idx:end_idx]
            else:
                json_text = result_text
            
            print(f"Attempting to parse JSON: {json_text[:100]}...")
            
            # Parse JSON
            result = json.loads(json_text)
            print("Successfully parsed JSON")
            return result
            
        except json.JSONDecodeError as je:
            print(f"JSON parsing error: {je}")
            print(f"Raw response: {result_text}")
            
            return {
                "news": [{
                    "title": "News retrieval completed",
                    "summary": result_text[:500] + "..." if len(result_text) > 500 else result_text,
                    "relevance_score": "Medium"
                }],
                "raw_response": result_text,
                "parse_error": str(je)
            }

    except Exception as e:
        print(f"Exception in processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return {"error": f"Error in processing: {str(e)}", "traceback": traceback.format_exc()}


@content_router.route('/health', methods=["GET"])
def health_check():
    return jsonify({
        "response": "Content Router Health Check",
        "status": "Healthy"
    })


@content_router.route('/news', methods=["POST"])
def get_news_endpoint():
    try:
        data = request.get_json()
        if not data or 'keywords' not in data:
            return jsonify({"error": "Keywords are required in request body"}), 400
        
        keywords = data['keywords']
        if not isinstance(keywords, list) or len(keywords) == 0:
            return jsonify({"error": "Keywords must be a non-empty list"}), 400
        
        news_result = get_news(keywords)
        
        if "error" in news_result:
            return jsonify(news_result), 500
        
        return jsonify(news_result), 200
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500


@content_router.route('/news/<keyword>', methods=["GET"])
def get_single_keyword_news(keyword):
    """
    Endpoint to get news for a single keyword via URL parameter
    """
    try:
        if not keyword:
            return jsonify({"error": "Keyword is required"}), 400
        
        news_result = get_news([keyword])
        
        if "error" in news_result:
            return jsonify(news_result), 500
        
        return jsonify(news_result), 200
        
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500