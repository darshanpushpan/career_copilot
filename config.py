# Career Copilot Configuration File
# Update these settings to change API providers or modify behavior

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_PROVIDER = "perplexity"  # Options: "perplexity", "openai", "anthropic", "custom"

# Perplexity API Settings - Load from environment variable
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

# --- DEBUGGING: Print the loaded API key to help diagnose deployment issues ---
print(f"DEBUG: Attempting to load PERPLEXITY_API_KEY...")
print(f"DEBUG: Value found: '{PERPLEXITY_API_KEY}'")
if not PERPLEXITY_API_KEY:
    print("DEBUG: PERPLEXITY_API_KEY is not set. The application will fail when an API call is made.")
else:
    print("DEBUG: PERPLEXITY_API_KEY loaded successfully.")
# --- END DEBUGGING ---

# Note: We will not raise an error here to allow the app to start on Railway.
# The app will fail gracefully when it tries to make an API call if the key is missing.
# if not PERPLEXITY_API_KEY:
#     raise ValueError("PERPLEXITY_API_KEY environment variable is required. Please check your .env file.")

PERPLEXITY_API_URL = "https://api.perplexity.ai/chat/completions"
PERPLEXITY_DEFAULT_MODEL = "sonar-reasoning"
PERPLEXITY_PRO_MODEL = "sonar-reasoning-pro"

# OpenAI API Settings (if switching to OpenAI)
OPENAI_API_KEY = ""  # Add your OpenAI API key here
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_DEFAULT_MODEL = "gpt-4"
OPENAI_PRO_MODEL = "gpt-4-turbo"

# Anthropic API Settings (if switching to Anthropic)
ANTHROPIC_API_KEY = ""  # Add your Anthropic API key here
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_DEFAULT_MODEL = "claude-3-sonnet-20240229"
ANTHROPIC_PRO_MODEL = "claude-3-opus-20240229"

# Custom API Settings (if using a custom endpoint)
CUSTOM_API_KEY = ""  # Add your custom API key here
CUSTOM_API_URL = ""  # Add your custom API endpoint here
CUSTOM_DEFAULT_MODEL = ""
CUSTOM_PRO_MODEL = ""

# Application Settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'txt'}

# AI Model Settings
MAX_TOKENS = 4000  # Maximum tokens for AI response
TEMPERATURE = 0.6  # AI creativity level (0.0 to 1.0)

# Cover Letter Generation Settings
COVER_LETTER_STYLE = "professional"  # Options: "professional", "casual", "creative"
COVER_LETTER_LENGTH = "medium"  # Options: "short", "medium", "long"
ENSURE_COMPLETE_COVER_LETTER = True  # Always generate complete cover letter, not outline
