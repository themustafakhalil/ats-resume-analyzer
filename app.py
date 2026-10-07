import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import io
api_key = st.secrets.get("GOOGLE_API_KEY", "")
# Page configuration
st.set_page_config(
    page_title="ATS Score Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 10px 0;
    }
    .score-number {
        font-size: 48px;
        font-weight: bold;
        margin: 10px 0;
    }
    .improvement-box {
        background: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📄 ATS Resume Analyzer")
st.markdown("Upload your resume and get instant ATS score + improvement suggestions powered by AI")

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "Enter your Google API Key",
        type="password",
        help="Get it from: https://makersuite.google.com/app/apikey"
    )
    st.markdown("---")
    st.markdown("### About ATS Score")
    st.info("""
    **ATS (Applicant Tracking System)** score measures how well your resume
    can be parsed by automated systems used by recruiters.

    **Score Range:**
    - 90-100: Excellent
    - 70-89: Good
    - 50-69: Average
    - Below 50: Poor
    """)

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file"""
    try:
        pdf_reader = PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {str(e)}")
        return None

def analyze_ats_score(resume_text, api_key):
    """Analyze resume using Gemini API"""
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)

        # Create the prompt for ATS analysis
        prompt = f"""
Analyze this resume for ATS (Applicant Tracking System) compatibility and provide a detailed report.

RESUME CONTENT:
{resume_text}

Please provide:
1. ATS SCORE (0-100): A single number representing how well this resume will be parsed by ATS systems
2. SCORE EXPLANATION: Brief explanation of why this score was given
3. STRENGTHS: List 3-5 ATS-friendly aspects of this resume
4. IMPROVEMENTS: List 5-7 specific improvements to increase ATS score
5. CRITICAL ISSUES: Any major ATS incompatibilities (if any)
6. KEYWORDS: Top 10 important keywords that should be in this resume for ATS

Format your response as follows:
SCORE: [number]
EXPLANATION: [explanation]
STRENGTHS:
- [point 1]
- [point 2]
- [point 3]
IMPROVEMENTS:
- [improvement 1]
- [improvement 2]
- [improvement 3]
- [improvement 4]
- [improvement 5]
CRITICAL_ISSUES:
- [issue 1 or "None"]
KEYWORDS:
- [keyword 1]
- [keyword 2]
- [keyword 3]
"""

        # Call Gemini Flash model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return response.text

    except Exception as e:
        st.error(f"Error analyzing resume: {str(e)}")
        return None

def parse_analysis(analysis_text):
    """Parse the analysis response into structured data"""
    lines = analysis_text.split('\n')
    result = {
        'score': None,
        'explanation': '',
        'strengths': [],
        'improvements': [],
        'critical_issues': [],
        'keywords': []
    }

    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("SCORE:"):
            try:
                result['score'] = int(''.join(filter(str.isdigit, line.split("SCORE:")[1])))
            except:
                result['score'] = 0

        elif line.startswith("EXPLANATION:"):
            result['explanation'] = line.split("EXPLANATION:")[1].strip()

        elif line.startswith("STRENGTHS:"):
            current_section = 'strengths'

        elif line.startswith("IMPROVEMENTS:"):
            current_section = 'improvements'

        elif line.startswith("CRITICAL_ISSUES:"):
            current_section = 'critical_issues'

        elif line.startswith("KEYWORDS:"):
            current_section = 'keywords'

        elif line.startswith("-") and current_section:
            item = line[1:].strip()
            if current_section == 'strengths':
                result['strengths'].append(item)
            elif current_section == 'improvements':
                result['improvements'].append(item)
            elif current_section == 'critical_issues':
                if item.lower() != "none":
                    result['critical_issues'].append(item)
            elif current_section == 'keywords':
                result['keywords'].append(item)

    return result

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📤 Upload Your Resume")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf",
        help="Upload your resume in PDF format"
    )

if uploaded_file and api_key:
    with st.spinner("🔍 Analyzing your resume..."):
        # Extract text from PDF
        resume_text = extract_text_from_pdf(uploaded_file)

        if resume_text:
            # Analyze with Gemini
            analysis = analyze_ats_score(resume_text, api_key)

            if analysis:
                # Parse the analysis
                parsed = parse_analysis(analysis)

                # Display results
                st.markdown("---")
                st.subheader("📊 ATS Analysis Results")

                # Score display
                score = parsed['score']
                if score is None:
                    score = 0

                # Color coding for score
                if score >= 90:
                    color = "🟢"
                    rating = "Excellent"
                elif score >= 70:
                    color = "🟡"
                    rating = "Good"
                elif score >= 50:
                    color = "🟠"
                    rating = "Average"
                else:
                    color = "🔴"
                    rating = "Poor"

                # Score card
                st.markdown(f"""
                <div class="metric-box">
                    <div>{color} {rating}</div>
                    <div class="score-number">{score}/100</div>
                    <div style="font-size: 14px;">{parsed['explanation']}</div>
                </div>
                """, unsafe_allow_html=True)

                # Create tabs for different sections
                tab1, tab2, tab3, tab4 = st.tabs(
                    ["💪 Strengths", "✨ Improvements", "⚠️ Issues", "🎯 Keywords"]
                )

                with tab1:
                    st.markdown("### Current ATS-Friendly Aspects")
                    for i, strength in enumerate(parsed['strengths'], 1):
                        st.success(f"**{i}. {strength}**")

                with tab2:
                    st.markdown("### How to Improve Your ATS Score")
                    for i, improvement in enumerate(parsed['improvements'], 1):
                        st.markdown(f"""
                        <div class="improvement-box">
                        <b>{i}. {improvement}</b>
                        </div>
                        """, unsafe_allow_html=True)

                with tab3:
                    if parsed['critical_issues']:
                        st.markdown("### Critical Issues to Fix")
                        for issue in parsed['critical_issues']:
                            st.error(f"🔴 {issue}")
                    else:
                        st.success("✅ No critical ATS issues detected!")

                with tab4:
                    st.markdown("### Important Keywords for Your Field")
                    cols = st.columns(2)
                    for i, keyword in enumerate(parsed['keywords']):
                        with cols[i % 2]:
                            st.info(f"🏷️ {keyword}")

                # Download button with tips
                st.markdown("---")
                st.subheader("💡 Quick Tips")
                tips = [
                    "Use standard fonts (Arial, Calibri, Times New Roman)",
                    "Keep formatting simple - avoid tables and graphics",
                    "Use standard section headings (Experience, Education, Skills)",
                    "Use bullet points instead of paragraphs",
                    "Include relevant keywords from job descriptions",
                    "Avoid unusual characters and symbols"
                ]

                for tip in tips:
                    st.info(tip)

elif uploaded_file and not api_key:
    st.warning("⚠️ Please enter your Google API Key in the sidebar to continue")

elif not uploaded_file:
    st.info("👆 Upload a PDF resume to get started")
