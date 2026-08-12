import os
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="AI Text Analysis API", description="A FastAPI wrapper for Google Gemini models")

# Configure Gemini API
# It expects the GEMINI_API_KEY environment variable to be set
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# We use gemini-1.5-flash as the default model as it's the standard for general text tasks
model = genai.GenerativeModel('gemini-1.5-flash')

class TextRequest(BaseModel):
    text: str

class TextResponse(BaseModel):
    result: str

@app.get("/health")
async def health_check():
    """Health check endpoint to verify the service is running."""
    return {"status": "ok"}

@app.post("/analyze", response_model=TextResponse)
async def analyze_text(request: TextRequest):
    """Analyzes the provided text using Gemini."""
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured.")
    try:
        prompt = f"Please analyze the following text in detail and provide insights:\n\n{request.text}"
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

@app.post("/summarize", response_model=TextResponse)
async def summarize_text(request: TextRequest):
    """Summarizes the provided text using Gemini."""
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured.")
    try:
        prompt = f"Please provide a concise summary of the following text:\n\n{request.text}"
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

@app.post("/classify", response_model=TextResponse)
async def classify_text(request: TextRequest):
    """Classifies the provided text using Gemini."""
    if not api_key:
        raise HTTPException(status_code=500, detail="GEMINI_API_KEY is not configured.")
    try:
        prompt = f"Please classify the following text into appropriate categories (e.g., sentiment, topic, tone) and return the categories:\n\n{request.text}"
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")
