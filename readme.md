# 📄 ATS Resume Analyzer

An AI-powered web app that analyzes your resume's ATS (Applicant Tracking System) score and provides detailed improvement suggestions. Built with **Streamlit** and **Google Gemini AI**.

## Features

✅ **ATS Score Analysis** - Get a 0-100 score on how well your resume works with ATS systems
✅ **AI-Powered Feedback** - Detailed suggestions using Google's Gemini Flash model
✅ **Strengths Identification** - See what's working well in your resume
✅ **Improvement Tips** - Get specific, actionable improvements
✅ **Keyword Analysis** - Find important keywords for your industry
✅ **Critical Issues** - Know what ATS systems might struggle with
✅ **Simple UI** - Clean, modern interface with tabs and organized sections

## What is ATS?

**Applicant Tracking Systems (ATS)** are software used by recruiters to scan and parse resumes. If your resume doesn't format well for ATS, it might not even reach a human recruiter.

### ATS Score Ranges:
- **90-100** 🟢 Excellent - Your resume is ATS-friendly
- **70-89** 🟡 Good - Most systems will read it fine
- **50-69** 🟠 Average - Some parsing issues
- **Below 50** 🔴 Poor - Major ATS compatibility issues

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ats-resume-analyzer.git
cd ats-resume-analyzer
```

### Step 2: Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Mac/Linux
python -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Get Google API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key" in "Get your API Key" section
3. Copy your API key (you'll need this to run the app)

### Step 5: Run the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## How to Use

1. **Open the app** in your browser (usually `http://localhost:8501`)
2. **Enter your Google API Key** in the sidebar configuration
3. **Upload your resume** as a PDF file
4. **Wait for analysis** - The app will analyze your resume using Gemini AI
5. **Review results** in different tabs:
   - 💪 **Strengths** - What's working well
   - ✨ **Improvements** - How to increase your score
   - ⚠️ **Issues** - Critical problems to fix
   - 🎯 **Keywords** - Industry-relevant terms to include

## Project Structure

```
ats-resume-analyzer/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .gitignore         # Git ignore file
```

## Dependencies

- **streamlit** - Web app framework
- **google-generativeai** - Google's Gemini API
- **PyPDF2** - PDF text extraction

## How It Works

1. **PDF Upload** - You upload a PDF resume
2. **Text Extraction** - PyPDF2 extracts all text from the PDF
3. **AI Analysis** - Gemini Flash model analyzes the text
4. **Scoring** - AI assigns an ATS score (0-100)
5. **Feedback** - Structured feedback on strengths, improvements, and keywords

## Deployment on Streamlit Cloud

### Step 1: Push to GitHub

1. Create a GitHub repository
2. Initialize git in your project folder:
```bash
git init
git add .
git commit -m "Initial commit: ATS Resume Analyzer"
git branch -M main
git remote add origin https://github.com/yourusername/ats-resume-analyzer.git
git push -u origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Click "New app" button
3. Select your GitHub repository
4. Select the branch (main) and file (app.py)
5. Click "Deploy"

### Step 3: Add Secrets (API Key)

1. Once deployed, click "settings" (⚙️) in the top-right corner
2. Go to "Secrets"
3. Add your Google API Key:
```
GOOGLE_API_KEY = "your-api-key-here"
```

4. Update your app.py to use the secret:
```python
api_key = st.secrets.get("GOOGLE_API_KEY") or st.text_input("Enter your Google API Key", type="password")
```

## How to Push Code Using GitHub Web UI

### Simple Method (No Git Command Line)

1. **Create GitHub Repository**
   - Go to [GitHub.com](https://github.com)
   - Click "+" → "New repository"
   - Name it: `ats-resume-analyzer`
   - Click "Create repository"

2. **Upload Files Using Web Interface**
   - Click "Add file" → "Upload files"
   - Drag and drop your files (app.py, requirements.txt, README.md)
   - Click "Commit changes"

3. **Or Use GitHub Desktop App** (Easiest for Beginners)
   - Download [GitHub Desktop](https://desktop.github.com)
   - Sign in with your GitHub account
   - Click "New" → "Create a New Repository"
   - Choose folder with your code
   - Click "Create Repository"
   - Click "Publish repository"
   - Fill in repository name and description
   - Click "Publish Repository"

### Terminal Method (Recommended)

```bash
# Initialize git repository
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit: ATS Resume Analyzer app"

# Rename branch to main (if needed)
git branch -M main

# Add your GitHub repository (replace with your URL)
git remote add origin https://github.com/yourusername/ats-resume-analyzer.git

# Push to GitHub
git push -u origin main
```

## ATS Best Practices

✅ **DO:**
- Use standard fonts (Arial, Calibri, Times New Roman)
- Keep formatting simple and clean
- Use standard section headings (Experience, Education, Skills)
- Use bullet points for descriptions
- Include relevant keywords from job descriptions
- Save as PDF to preserve formatting

❌ **DON'T:**
- Use tables, graphics, or images
- Use unusual fonts or symbols
- Use colored text or backgrounds
- Use multiple columns
- Use headers/footers with important info
- Use templates with heavy formatting
- Use non-standard section names

## Troubleshooting

### "Error reading PDF"
- Make sure your PDF is not password-protected
- Try converting your resume to PDF with a different tool
- Ensure the PDF contains selectable text (not a scanned image)

### "API Key Error"
- Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
- Create a new API key
- Make sure you have Google Generative AI API enabled
- Check that your API key is pasted correctly

### "ModuleNotFoundError"
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt` again
- Check that all dependencies installed without errors

## Environment Variables (Optional)

For better security, use a `.env` file:

1. Create `.env` file:
```
GOOGLE_API_KEY=your-api-key-here
```

2. Update app.py:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY") or st.text_input("Enter Google API Key", type="password")
```

3. Install python-dotenv:
```bash
pip install python-dotenv
```

## Security Notes

⚠️ **Never commit your API key to GitHub!**

Create `.gitignore` file:
```
.env
__pycache__/
*.pyc
.streamlit/secrets.toml
venv/
```

## License

MIT License - feel free to use this project!

## Support

If you face any issues:
1. Check the Troubleshooting section
2. Read error messages carefully
3. Make sure all dependencies are installed
4. Try with a different resume (in case it's a PDF issue)

## Future Enhancements

- Support for different resume formats (DOCX, TXT)
- Resume optimization suggestions
- Comparison with job descriptions
- Historical score tracking
- Export detailed reports

---

**Made with ❤️ for job seekers | Powered by Gemini AI**
