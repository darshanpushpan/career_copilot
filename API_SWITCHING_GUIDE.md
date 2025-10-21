# API Switching Guide for Career Copilot

This guide explains how to switch between different AI API providers in Career Copilot.

## Quick Setup

All API configuration is centralized in the `config.py` file. To switch APIs, simply:

1. **Edit `config.py`**
2. **Change the `API_PROVIDER` setting**
3. **Add your API credentials**
4. **Restart the Flask application**

## Supported API Providers

### 1. Perplexity AI (Current Default)
```python
API_PROVIDER = "perplexity"
PERPLEXITY_API_KEY = "your-perplexity-api-key"
```

### 2. OpenAI
```python
API_PROVIDER = "openai"
OPENAI_API_KEY = "your-openai-api-key"
```

### 3. Anthropic (Claude)
```python
API_PROVIDER = "anthropic"
ANTHROPIC_API_KEY = "your-anthropic-api-key"
```

### 4. Custom API
```python
API_PROVIDER = "custom"
CUSTOM_API_KEY = "your-custom-api-key"
CUSTOM_API_URL = "https://your-api-endpoint.com/v1/chat/completions"
```

## Step-by-Step Switching Process

### Example: Switching to OpenAI

1. **Get OpenAI API Key**
   - Go to https://platform.openai.com/api-keys
   - Create a new API key

2. **Update config.py**
   ```python
   API_PROVIDER = "openai"
   OPENAI_API_KEY = "sk-your-openai-api-key-here"
   ```

3. **Restart the application**
   ```bash
   flask run
   ```

### Example: Switching to Anthropic (Claude)

1. **Get Anthropic API Key**
   - Go to https://console.anthropic.com/
   - Create a new API key

2. **Update config.py**
   ```python
   API_PROVIDER = "anthropic"
   ANTHROPIC_API_KEY = "sk-ant-your-anthropic-api-key-here"
   ```

3. **Restart the application**

## Configuration Options

### Model Selection
Each provider has default and pro models:
- **Default Model**: Used for standard analysis
- **Pro Model**: Used when "Sonar Reasoning Pro" is selected

### Customization Options
```python
MAX_TOKENS = 4000          # Maximum response length
TEMPERATURE = 0.6          # AI creativity (0.0-1.0)
COVER_LETTER_STYLE = "professional"  # professional, casual, creative
ENSURE_COMPLETE_COVER_LETTER = True  # Always generate complete letters
```

## Troubleshooting

### Common Issues

1. **API Key Not Working**
   - Verify the API key is correct
   - Check if you have sufficient credits/quota
   - Ensure the API key has the right permissions

2. **Model Not Found**
   - Check if the model name is correct for your API provider
   - Some models may not be available in all regions

3. **Rate Limiting**
   - Reduce the number of requests
   - Consider upgrading your API plan

### Testing Your Setup

1. Start the Flask application
2. Go to http://127.0.0.1:5000
3. Try analyzing a resume and job description
4. Check the terminal for any error messages

## Security Notes

- Never commit API keys to version control
- Use environment variables for production deployments
- Consider using a secrets management service for production

## Cost Considerations

Different APIs have different pricing:
- **Perplexity**: Pay-per-request model
- **OpenAI**: Token-based pricing
- **Anthropic**: Token-based pricing with different rates for different models

Check each provider's pricing page for current rates.

## Need Help?

If you encounter issues:
1. Check the Flask application logs
2. Verify your API credentials
3. Test with a simple request first
4. Check the API provider's documentation
