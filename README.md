# Career Copilot

A **live web application** that helps users tailor their job applications by analyzing a job description and resume, then generating personalized resume suggestions and cover letters using advanced AI reasoning models.

## 🌐 Live Site

**Career Copilot is now live and accessible at:** [Your Railway Deployment URL](https://your-deployment-url.railway.app)

**GitHub Repository:** [https://github.com/darshanpushpan/career_copilot](https://github.com/darshanpushpan/career_copilot)

No installation required - simply visit the Railway deployment URL to start using the application!

## Features

- **Advanced AI Analysis**: Powered by Sonar Reasoning models for deep, comprehensive resume analysis
- **Model Selection**: Choose between Sonar Reasoning (127K context) and Sonar Reasoning Pro (200K context)
- **Resume Analysis**: Analyzes your resume against job requirements with advanced reasoning capabilities
- **Personalized Suggestions**: Provides specific, actionable advice to improve your resume
- **Cover Letter Generation**: Creates professional cover letters tailored to the job
- **File Upload Support**: Upload PDF, DOCX, DOC, or TXT resume files
- **Dual Input Methods**: Choose between pasting text or uploading files
- **Modern UI**: Clean, responsive interface built with Tailwind CSS
- **Real-time Processing**: Asynchronous form submission with loading indicators
- **Drag & Drop**: Easy file upload with drag and drop functionality
- **Real-time Web Search**: Sonar models can access current information for enhanced analysis

## How to Use

1. **Visit the live site**: Navigate to [Your Railway Deployment URL](https://your-deployment-url.railway.app)
2. **Select AI Model**: Choose between Sonar Reasoning or Sonar Reasoning Pro
3. **Paste the job description** in the left textarea
4. **Choose your resume input method**:
   - **Paste Text**: Enter your resume content in the text area
   - **Upload File**: Upload a PDF, DOCX, DOC, or TXT file (drag & drop supported)
5. **Click "Generate Suggestions & Cover Letter"**
6. **Review the results**:
   - Resume enhancement suggestions will appear on the left
   - Generated cover letter will appear on the right

## Technology Stack

- **Backend**: Python with Flask (running on live server)
- **Frontend**: HTML, Tailwind CSS, Vanilla JavaScript
- **AI Integration**: Perplexity API with Sonar Reasoning models
- **File Processing**: PyPDF2, python-docx for document parsing
- **Deployment**: [Your hosting platform - e.g., Heroku, Railway, Render, etc.]
- **Database**: [If applicable - or state "No persistent database required"]

## Project Structure

```
career-copilot/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── config.py             # Application configuration
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── css/
    │   └── output.css    # (Not used - Tailwind via CDN)
    └── js/
        └── main.js       # Frontend JavaScript logic
```

## API Endpoints

- `GET /` - Serves the main application page
- `POST /analyze` - Analyzes job description and resume, returns suggestions and cover letter

## Configuration

The live application uses the following configuration:

- **AI Provider**: Perplexity API with Sonar Reasoning models
- **File Size Limit**: 16MB maximum upload size
- **Rate Limiting**: [If applicable]
- **Security**: HTTPS enabled, secure API key management

## Development & Deployment

This project is actively deployed and maintained. For development purposes:

### Local Development (Optional)

If you want to run the application locally for development:

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Configure environment variables** in `.env` file
4. **Run locally**: `flask run`

### Deployment

The application is deployed using [deployment platform] with:
- Automatic deployments on git push
- Environment variable management
- SSL certificate management
- CDN for static assets

## Support & Contact

For questions or support regarding the live application, please [contact method].

## License

This project is open source and available under the MIT License.
