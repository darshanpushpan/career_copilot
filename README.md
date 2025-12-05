
# Career Copilot – AI-Powered Resume Enhancement

[![Railway](https://img.shields.io/badge/Deployed-Railway-3DDC84?logo=railway)](https://careercopilot.up.railway.app/)
[![Flask](https://img.shields.io/badge/Backend-Flask-000000?logo=flask)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/UI-Tailwind%20CSS-38BDF8?logo=tailwindcss)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python)](https://python.org/)
[![MIT License](https://img.shields.io/badge/License-MIT-007EC6?logo=github)](LICENSE)

🔗 **Live App:** [https://careercopilot.up.railway.app/](https://careercopilot.up.railway.app/)  
💻 **GitHub:** [https://github.com/darshanpushpan/career_copilot](https://github.com/darshanpushpan/career_copilot)

Career Copilot is a live web app that helps users tailor their job applications using AI. It compares your resume with a job description and generates personalized suggestions and custom cover letters — instantly.

---

## 🚀 Features

- **AI Resume Analysis** – Evaluates your resume against job descriptions using advanced reasoning models.  
- **Two AI Models** – Choose between **Sonar Reasoning (127K)** or **Sonar Reasoning Pro (200K)**.  
- **Cover Letter Generation** – Creates tailored cover letters aligned with the job role.  
- **Smart File Upload** – Supports PDF, DOCX, DOC, and TXT with drag-and-drop.  
- **Modern Interface** – Responsive UI built with Tailwind CSS.  
- **Real-Time Web Search** – Uses Sonar models to fetch and apply the latest information.  
- **Asynchronous Processing** – Real-time feedback with loading indicators.

---

## 🧭 How to Use

1. Go to [https://careercopilot.up.railway.app](https://careercopilot.up.railway.app)  
2. Select an **AI model**.  
3. Paste the **job description** in the left box.  
4. Add your **resume** by pasting text or uploading a file.  
5. Click **"Generate Suggestions & Cover Letter."**  
6. Review:
   - Left side: Resume suggestions.  
   - Right side: Tailored cover letter.

---

## ⚙️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python (Flask) |
| **Frontend** | HTML, Tailwind CSS, Vanilla JavaScript |
| **AI Models** | Perplexity Sonar Reasoning & Pro |
| **File Parsing** | `PyPDF2`, `python-docx` |
| **Hosting** | Railway |
| **Database** | None (stateless app) |

---

## 📁 Project Structure

```
career-copilot/
├── app.py               # Flask backend
├── config.py            # API & environment configuration
├── requirements.txt     # Dependencies
├── templates/
│   └── index.html       # Main page
├── static/
│   ├── css/
│   └── js/
│       └── main.js
└── README.md
```

---

## 🧑‍💻 Local Development

```
git clone https://github.com/darshanpushpan/career_copilot.git
cd career_copilot
pip install -r requirements.txt
# Set .env variables
flask run
```

---

## 📜 License

Licensed under the **MIT License**.
```
