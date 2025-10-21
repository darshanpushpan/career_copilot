from flask import Flask, render_template, request, jsonify
import os
import requests
import PyPDF2
from docx import Document
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import io
import json
import re

# Load environment variables
load_dotenv()

# Load configuration
try:
    from config import *
except ImportError:
    # Fallback to environment variables if config.py doesn't exist
    PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
    PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'sonar-reasoning')
    API_PROVIDER = "perplexity"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.6
    ENSURE_COMPLETE_COVER_LETTER = True

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text_from_pdf(file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def extract_text_from_docx(file):
    """Extract text from DOCX file"""
    try:
        doc = Document(file)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text.strip()
    except Exception as e:
        raise Exception(f"Error reading DOCX: {str(e)}")

def extract_text_from_file(file):
    """Extract text from uploaded file based on file type"""
    filename = file.filename.lower()
    
    if filename.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif filename.endswith(('.docx', '.doc')):
        return extract_text_from_docx(file)
    elif filename.endswith('.txt'):
        return file.read().decode('utf-8')
    else:
        raise Exception("Unsupported file type")

def get_api_config():
    """Get API configuration based on the selected provider"""
    if API_PROVIDER == "perplexity":
        return {
            "api_key": PERPLEXITY_API_KEY,
            "api_url": PERPLEXITY_API_URL,
            "default_model": PERPLEXITY_DEFAULT_MODEL,
            "pro_model": PERPLEXITY_PRO_MODEL
        }
    elif API_PROVIDER == "openai":
        return {
            "api_key": OPENAI_API_KEY,
            "api_url": OPENAI_API_URL,
            "default_model": OPENAI_DEFAULT_MODEL,
            "pro_model": OPENAI_PRO_MODEL
        }
    elif API_PROVIDER == "anthropic":
        return {
            "api_key": ANTHROPIC_API_KEY,
            "api_url": ANTHROPIC_API_URL,
            "default_model": ANTHROPIC_DEFAULT_MODEL,
            "pro_model": ANTHROPIC_PRO_MODEL
        }
    elif API_PROVIDER == "custom":
        return {
            "api_key": CUSTOM_API_KEY,
            "api_url": CUSTOM_API_URL,
            "default_model": CUSTOM_DEFAULT_MODEL,
            "pro_model": CUSTOM_PRO_MODEL
        }
    else:
        raise Exception(f"Unsupported API provider: {API_PROVIDER}")

def call_ai_api(prompt, model=None):
    """Call AI API with the given prompt and model - works with multiple providers"""
    config = get_api_config()
    
    if model is None:
        model = config["default_model"]
    
    # Enhanced system prompt for better cover letter generation
    system_prompt = """You are Career Copilot, an expert career coach. You will be given a job description and a resume. Your task is to analyze both documents and provide comprehensive insights.

CRITICAL INSTRUCTIONS:
- You MUST provide ACTUAL content, not descriptions of what you will do
- Do NOT use phrases like "I'll provide", "I'll write", "Here's what I'll do"
- Do NOT explain your process or methodology
- Provide the actual resume suggestions and cover letter content immediately

Your response must have exactly three sections with ACTUAL CONTENT and a compact JSON block:

### Job Match Analysis
Analyze how well the resume matches the job requirements and provide a JSON object with this structure:
{"match": {"score": 75, "strengths": ["Strong experience in required technologies", "Relevant industry experience"], "gaps": ["Limited project management experience", "Missing specific certification"]}}

The score should be a number between 0-100 based on overall fit.

### Resume Enhancement Suggestions
Provide specific, actionable advice to tailor the resume, including:
- Keyword optimization suggestions
- Quantifying achievements recommendations
- Strategic positioning advice
- Format and structure improvements
- Skills and experience alignment tips

### Generated Cover Letter
Write a complete, professional cover letter that:
- Addresses the hiring manager directly
- Demonstrates understanding of the role and company
- Highlights relevant experience and achievements from the resume
- Shows enthusiasm and cultural fit
- Ends with a strong call to action
- Is ready to send without any modifications

Do not invent skills or experiences not found in the resume. Use your reasoning capabilities to identify subtle connections between the candidate's experience and job requirements."""

    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json"
    }
    
    # Prepare data based on API provider
    if API_PROVIDER == "anthropic":
        data = {
            "model": model,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "messages": [
                {
                    "role": "user",
                    "content": f"{system_prompt}\n\n{prompt}"
                }
            ]
        }
    else:
        data = {
            "model": model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }
    
    response = requests.post(config["api_url"], headers=headers, json=data)
    
    if response.status_code != 200:
        raise Exception(f"{API_PROVIDER.title()} API error: {response.status_code} - {response.text}")
    
    return response.json()

def clean_cover_letter(cover_letter_text):
    """Clean and format the cover letter to ensure it's complete and professional"""
    if not cover_letter_text:
        return ""
    
    # Remove common AI explanatory phrases
    unwanted_phrases = [
        "Here's a cover letter",
        "Here is a cover letter",
        "The cover letter should",
        "This cover letter",
        "I'll write a cover letter",
        "Let me create a cover letter",
        "Here's what the cover letter should include",
        "The cover letter would",
        "This is a cover letter",
        "Below is a cover letter",
        "I'll provide",
        "I'll write",
        "Here's what I'll do",
        "I will provide",
        "I will write",
        "The cover letter will",
        "This will be a cover letter"
    ]
    
    cleaned_text = cover_letter_text
    
    # Remove unwanted phrases
    for phrase in unwanted_phrases:
        if phrase.lower() in cleaned_text.lower():
            # Find the position and remove everything before the actual letter
            pos = cleaned_text.lower().find(phrase.lower())
            if pos != -1:
                # Look for the start of the actual letter (usually after a colon or newline)
                remaining = cleaned_text[pos + len(phrase):]
                # Find the first line that looks like a greeting
                lines = remaining.split('\n')
                for i, line in enumerate(lines):
                    line = line.strip()
                    if (line.startswith('Dear') or 
                        line.startswith('To Whom It May Concern') or
                        line.startswith('Hiring Manager') or
                        line.startswith('Dear Hiring Manager')):
                        cleaned_text = '\n'.join(lines[i:])
                        break
    
    # Check if the text is just a description rather than actual content
    if any(phrase in cleaned_text.lower() for phrase in [
        "i'll provide specific, actionable advice",
        "i'll write a complete, professional cover letter",
        "addresses the hiring manager directly",
        "demonstrates understanding of the role",
        "highlights relevant experience",
        "shows enthusiasm and cultural fit",
        "ends with a strong call to action"
    ]):
        # This is a description, not actual content - return empty to trigger regeneration
        return ""
    
    # Ensure proper formatting
    lines = cleaned_text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if line and not line.startswith('**') and not line.startswith('*'):
            formatted_lines.append(line)
    
    # Join lines and ensure proper spacing
    result = '\n\n'.join(formatted_lines)
    
    # If the result is too short or doesn't look like a cover letter, return empty
    if len(result) < 200 or not any(greeting in result for greeting in ['Dear', 'To Whom It May Concern']):
        return ""
    
    return result

def clean_resume_suggestions(suggestions_text):
    """Clean and format the resume suggestions to ensure they're actionable advice"""
    if not suggestions_text:
        return ""

    # Remove common AI explanatory phrases
    unwanted_phrases = [
        "i'll provide specific, actionable advice",
        "i'll write specific, actionable advice",
        "here's what i'll do",
        "i will provide",
        "i will write",
        "here's the advice",
        "the suggestions are",
        "i'll give you"
    ]

    cleaned_text = suggestions_text

    # Remove unwanted phrases
    for phrase in unwanted_phrases:
        if phrase.lower() in cleaned_text.lower():
            # Find the position and remove everything before the actual suggestions
            pos = cleaned_text.lower().find(phrase.lower())
            if pos != -1:
                # Look for the start of actual suggestions (usually after a colon or newline)
                remaining = cleaned_text[pos + len(phrase):]
                # Find the first line that looks like actual advice
                lines = remaining.split('\n')
                for i, line in enumerate(lines):
                    line = line.strip()
                    if (line.startswith('-') or
                        line.startswith('•') or
                        line.startswith('1.') or
                        line.startswith('*') or
                        len(line) > 20):  # Likely actual content
                        cleaned_text = '\n'.join(lines[i:])
                        break

    # Check if the text is just a description rather than actual content
    if any(phrase in cleaned_text.lower() for phrase in [
        "i'll provide specific, actionable advice",
        "keyword optimization suggestions",
        "quantifying achievements recommendations",
        "strategic positioning advice",
        "format and structure improvements"
    ]) and len(cleaned_text) < 300:
        # This is a description, not actual content - return empty to trigger regeneration
        return ""

    # Format suggestions as bullet points for better readability
    formatted_suggestions = format_suggestions_as_bullets(cleaned_text)

    return formatted_suggestions.strip()

def format_suggestions_as_bullets(text):
    """Format suggestions text as bullet points for better readability"""
    if not text:
        return ""

    lines = text.split('\n')
    formatted_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Skip if already a header or section title
        if line.startswith('###') or line.isupper():
            formatted_lines.append(line)
            continue

        # Check if line is already a bullet point
        if (line.startswith('- ') or
            line.startswith('• ') or
            line.startswith('* ') or
            line.startswith('•') or
            line.startswith('◦') or
            (line.startswith('1.') and len(line) < 50)):  # Numbered lists that are short
            formatted_lines.append(line)
        else:
            # Convert to bullet point if it's a substantial suggestion
            if len(line) > 10:  # Only convert substantial lines
                # Add bullet point formatting
                formatted_lines.append(f"• {line}")
            else:
                formatted_lines.append(line)

    # Join lines with proper spacing
    result = '\n'.join(formatted_lines)

    # Clean up multiple consecutive bullet points
    result = re.sub(r'\n•\s*\n•', '\n•', result)

    return result

@app.route('/')
def index():
    """Serve the main index.html page"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze job description and resume, return suggestions and cover letter"""
    try:
        job_description = ""
        resume_text = ""
        
        # Get selected model (from form data or JSON)
        config = get_api_config()
        selected_model = None
        
        # Check if it's a file upload or JSON request
        if 'resume_file' in request.files:
            # Handle file upload
            job_description = request.form.get('job_description', '')
            model_choice = request.form.get('ai_model', 'default')
            resume_file = request.files['resume_file']
            
            if resume_file.filename == '':
                return jsonify({'error': 'No resume file selected'}), 400
            
            if not allowed_file(resume_file.filename):
                return jsonify({'error': 'Invalid file type. Please upload PDF, DOCX, DOC, or TXT files only.'}), 400
            
            # Extract text from uploaded file
            resume_text = extract_text_from_file(resume_file)
            
        else:
            # Handle JSON request (text input)
            data = request.get_json()
            job_description = data.get('job_description', '')
            resume_text = data.get('resume_text', '')
            model_choice = data.get('ai_model', 'default')
        
        # Determine which model to use
        if model_choice == 'sonar-reasoning-pro' or model_choice == 'pro':
            selected_model = config['pro_model']
        else:
            selected_model = config['default_model']
        
        # Validate input
        if not job_description or not resume_text:
            return jsonify({'error': 'Both job description and resume are required'}), 400
        
        # Construct the prompt for AI API
        user_prompt = f"""
[JOB_DESCRIPTION]
{job_description}

[MY_RESUME]
{resume_text}
"""
        
        # Make API call with selected model
        response = call_ai_api(user_prompt, selected_model)
        
        # Get the AI response based on API provider
        if API_PROVIDER == "anthropic":
            ai_response = response['content'][0]['text']
        else:
            ai_response = response['choices'][0]['message']['content']
        
        # Parse the response to separate suggestions, cover letter, and match analysis
        suggestions = ""
        cover_letter = ""
        match = None
        
        # Enhanced parsing to ensure we get complete sections
        if "### Job Match Analysis" in ai_response:
            parts = ai_response.split("### Job Match Analysis")
            if len(parts) > 1:
                match_part = parts[1]
                if "### Resume Enhancement Suggestions" in match_part:
                    match_text, suggestions_part = match_part.split("### Resume Enhancement Suggestions", 1)
                    
                    # Extract JSON from match analysis section
                    try:
                        json_match = re.search(r'\{[\s\S]*"match"\s*:\s*\{[\s\S]*?\}[\s\S]*\}', match_text)
                        if json_match:
                            match_obj = json.loads(json_match.group(0))
                            if isinstance(match_obj, dict) and 'match' in match_obj:
                                match = match_obj['match']
                    except Exception:
                        match = None
                    
                    if "### Generated Cover Letter" in suggestions_part:
                        suggestions, cover_letter_part = suggestions_part.split("### Generated Cover Letter", 1)
                        cover_letter = cover_letter_part.strip()
                        
                        # Clean up both sections - remove any explanatory text
                        if ENSURE_COMPLETE_COVER_LETTER:
                            cover_letter = clean_cover_letter(cover_letter)
                            suggestions = clean_resume_suggestions(suggestions)
                    else:
                        suggestions = clean_resume_suggestions(suggestions_part.strip())
                else:
                    # Extract JSON from match analysis section
                    try:
                        json_match = re.search(r'\{[\s\S]*"match"\s*:\s*\{[\s\S]*?\}[\s\S]*\}', match_part)
                        if json_match:
                            match_obj = json.loads(json_match.group(0))
                            if isinstance(match_obj, dict) and 'match' in match_obj:
                                match = match_obj['match']
                    except Exception:
                        match = None
        else:
            # Fallback: if format is not as expected, return the whole response as suggestions
            suggestions = ai_response
        
        # Check if we got actual content or just descriptions
        if (suggestions and any(phrase in suggestions.lower() for phrase in [
            "i'll provide", "i'll write", "here's what i'll do", "i will provide"
        ])) or (cover_letter and any(phrase in cover_letter.lower() for phrase in [
            "i'll provide", "i'll write", "here's what i'll do", "i will provide"
        ])):
            # We got descriptions instead of actual content, try again with a more direct prompt
            retry_prompt = f"""
Write the actual job match analysis, resume suggestions and cover letter for this job application. Do not describe what you will do - provide the actual content.

Job Description: {job_description}

Resume: {resume_text}

Provide three sections:

### Job Match Analysis
{{"match": {{"score": 75, "strengths": ["List 2-3 key strengths"], "gaps": ["List 2-3 key gaps"]}}}}

### Resume Enhancement Suggestions
[Write specific, actionable advice here]

### Generated Cover Letter
[Write the complete cover letter here]
"""
            try:
                retry_response = call_ai_api(retry_prompt, selected_model)
                if API_PROVIDER == "anthropic":
                    retry_ai_response = retry_response['content'][0]['text']
                else:
                    retry_ai_response = retry_response['choices'][0]['message']['content']
                
                # Parse the retry response
                if "### Job Match Analysis" in retry_ai_response:
                    retry_parts = retry_ai_response.split("### Job Match Analysis")
                    if len(retry_parts) > 1:
                        retry_match_part = retry_parts[1]
                        if "### Resume Enhancement Suggestions" in retry_match_part:
                            retry_match_text, retry_suggestions_part = retry_match_part.split("### Resume Enhancement Suggestions", 1)
                            
                            # Extract JSON from match analysis section
                            try:
                                json_match = re.search(r'\{[\s\S]*"match"\s*:\s*\{[\s\S]*?\}[\s\S]*\}', retry_match_text)
                                if json_match:
                                    match_obj = json.loads(json_match.group(0))
                                    if isinstance(match_obj, dict) and 'match' in match_obj:
                                        match = match_obj['match']
                            except Exception:
                                match = None
                            
                            if "### Generated Cover Letter" in retry_suggestions_part:
                                suggestions, retry_cover_letter_part = retry_suggestions_part.split("### Generated Cover Letter", 1)
                                cover_letter = retry_cover_letter_part.strip()
                            else:
                                suggestions = retry_suggestions_part.strip()
                        else:
                            # Extract JSON from match analysis section
                            try:
                                json_match = re.search(r'\{[\s\S]*"match"\s*:\s*\{[\s\S]*?\}[\s\S]*\}', retry_match_part)
                                if json_match:
                                    match_obj = json.loads(json_match.group(0))
                                    if isinstance(match_obj, dict) and 'match' in match_obj:
                                        match = match_obj['match']
                            except Exception:
                                match = None
                else:
                    suggestions = retry_ai_response
            except Exception as e:
                # If retry fails, use original response
                pass
        
        return jsonify({
            'suggestions': suggestions.strip(),
            'cover_letter': cover_letter.strip(),
            'match': match
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
