from flask import Blueprint, request, jsonify
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
import os
import json
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
print(groq_api_key)
hf_token = os.getenv('HF_TOKEN')

def extract_business_info(url: str):
    try:
        loader = WebBaseLoader(url)
        documents = loader.load()
        
        if not documents:
            return {"error": "No content found at the provided URL"}
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=100
        )
        split_documents = text_splitter.split_documents(documents)
        
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        vectorstore = FAISS.from_documents(split_documents, embeddings)
        
        retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 10}
        )
        
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=groq_api_key,
            temperature=0.1
        )
        
        prompt = PromptTemplate(
            template="""You are an assistant that extracts a succinct business profile from website text.
Return strictly a JSON object with these keys: 
- name: string (name of the company)
- industry: string (the industry the company belongs to)
- services: array of strings (services provided by the company)
- tone: string (the tone in which the text is written on the website)

You have to return the above values using the website text given below only.

Website text:
---
{context}
---

Return ONLY the JSON object with no additional text or formatting. If uncertain about any field, use empty string or empty array.
""",
            input_variables=["context"]
        )
     
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            chain_type_kwargs={"prompt": prompt}
        )
        
        relevant_docs = retriever.get_relevant_documents("company information services industry")
        context = "\n".join([doc.page_content for doc in relevant_docs])
        
        response = llm.invoke(prompt.format(context=context))
        
        try:
            response_text = response.content if hasattr(response, 'content') else str(response)

            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response_text[start_idx:end_idx]
                business_info = json.loads(json_str)
            else:
                business_info = json.loads(response_text)
            
            return business_info
            
        except json.JSONDecodeError as e:
            return {
                "error": "Failed to parse business information",
                "raw_response": response_text,
                "json_error": str(e)
            }
            
    except Exception as e:
        return {"error": f"An error occurred while processing the URL: {str(e)}"}

business_router = Blueprint('business_api', __name__)


@business_router.route('/extract', methods=['POST'])
def extract_business_data():
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            return jsonify({
                "error": "Missing 'url' parameter in request body"
            }), 400
        
        url = data['url']
        
        if not url.startswith(('http://', 'https://')):
            return jsonify({
                "error": "Invalid URL format. URL must start with http:// or https://"
            }), 400
        
        result = extract_business_info(url)
        
        # Check if there was an error
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Unexpected error: {str(e)}"
        }), 500

@business_router.route('/extract-get', methods=['GET'])
def extract_business_data_get():

    try:
        url = request.args.get('url')
        
        if not url:
            return jsonify({
                "error": "Missing 'url' query parameter"
            }), 400
        
        if not url.startswith(('http://', 'https://')):
            return jsonify({
                "error": "Invalid URL format. URL must start with http:// or https://"
            }), 400
    
        result = extract_business_info(url)
        
        if 'error' in result:
            return jsonify(result), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "error": f"Unexpected error: {str(e)}"
        }), 500

@business_router.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "Business Information Extractor API"
    }), 200