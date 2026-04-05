import streamlit as st
import os
from pdf_extractor import extract_text_from_pdf
from qa_generator import generate_qa
from doc_exporter import export_to_docx
import tempfile

st.set_page_config(
    page_title="MedStudy AI",
    page_icon="🧬",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=Inter:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main {
        background-color: #0a0e1a;
    }

    h1, h2, h3 {
        font-family: 'Syne', sans-serif !important;
    }

    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00d4ff, #7b2ff7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.1;
        margin-bottom: 0.5rem;
    }

    .hero-sub {
        color: #8892a4;
        font-size: 1.05rem;
        font-weight: 300;
        margin-bottom: 2rem;
    }

    .card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
    }

    .step-badge {
        display: inline-block;
        background: linear-gradient(135deg, #00d4ff22, #7b2ff722);
        border: 1px solid #00d4ff44;
        color: #00d4ff;
        font-family: 'Syne', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        padding: 4px 12px;
        border-radius: 999px;
        margin-bottom: 1rem;
    }

    .qa-block {
        background: #0d1117;
        border-left: 3px solid #7b2ff7;
        border-radius: 0 12px 12px 0;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }

    .qa-question {
        color: #00d4ff;
        font-family: 'Syne', sans-serif;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }

    .qa-answer {
        color: #c9d1d9;
        font-size: 0.9rem;
        line-height: 1.6;
    }

    .stButton > button {
        background: linear-gradient(135deg, #00d4ff, #7b2ff7);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-family: 'Syne', sans-serif;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: opacity 0.2s;
    }

    .stButton > button:hover {
        opacity: 0.85;
    }

    .stFileUploader {
        border-radius: 12px;
    }

    .info-pill {
        display: inline-block;
        background: #1a2236;
        color: #8892a4;
        font-size: 0.8rem;
        padding: 4px 12px;
        border-radius: 999px;
        margin-right: 8px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Hero
st.markdown('<div class="hero-title">MedStudy AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Upload your lecture handout. Get exam-ready Q&A. Export and study.</div>', unsafe_allow_html=True)

# API Key input
with st.expander("🔑 Enter your Anthropic API Key", expanded=not bool(os.environ.get("ANTHROPIC_API_KEY"))):
    api_key_input = st.text_input("API Key", type="password", placeholder="sk-ant-...", label_visibility="collapsed")
    if api_key_input:
        os.environ["ANTHROPIC_API_KEY"] = api_key_input
        st.success("API key set for this session.")

api_key = os.environ.get("ANTHROPIC_API_KEY", "")

st.markdown("---")

# Step 1 - Upload
st.markdown('<div class="step-badge">STEP 01</div>', unsafe_allow_html=True)
st.markdown("### Upload Your Handout")
uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")

if uploaded_file:
    st.success(f"✅ {uploaded_file.name} uploaded")

    # Step 2 - Settings
    st.markdown("---")
    st.markdown('<div class="step-badge">STEP 02</div>', unsafe_allow_html=True)
    st.markdown("### Configure")

    col1, col2 = st.columns(2)
    with col1:
        num_questions = st.slider("Number of questions to generate", min_value=10, max_value=100, value=30, step=5)
    with col2:
        subject = st.text_input("Subject / Topic (optional)", placeholder="e.g. Chemical Pathology")

    # Step 3 - Generate
    st.markdown("---")
    st.markdown('<div class="step-badge">STEP 03</div>', unsafe_allow_html=True)
    st.markdown("### Generate Q&A")

    if st.button("🧬 Generate Exam Q&A"):
        if not api_key:
            st.error("Please enter your Anthropic API key above.")
        else:
            with st.spinner("Extracting text from PDF..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                pdf_text = extract_text_from_pdf(tmp_path)

            if not pdf_text.strip():
                st.error("Could not extract text from this PDF. It may be scanned/image-based.")
            else:
                with st.spinner(f"Generating {num_questions} exam questions with Claude..."):
                    qa_pairs = generate_qa(pdf_text, num_questions, subject, api_key)

                if qa_pairs:
                    st.session_state["qa_pairs"] = qa_pairs
                    st.session_state["subject"] = subject or "Study"
                    st.success(f"✅ {len(qa_pairs)} Q&A pairs generated!")
                else:
                    st.error("Something went wrong generating Q&A. Check your API key and try again.")

# Display Q&A
if "qa_pairs" in st.session_state and st.session_state["qa_pairs"]:
    qa_pairs = st.session_state["qa_pairs"]

    st.markdown("---")
    st.markdown('<div class="step-badge">STEP 04</div>', unsafe_allow_html=True)
    st.markdown("### Your Exam Q&A")

    for i, (q, a) in enumerate(qa_pairs, 1):
        st.markdown(f"""
        <div class="qa-block">
            <div class="qa-question">Q{i}. {q}</div>
            <div class="qa-answer">{a}</div>
        </div>
        """, unsafe_allow_html=True)

    # Export
    st.markdown("---")
    st.markdown('<div class="step-badge">STEP 05</div>', unsafe_allow_html=True)
    st.markdown("### Export")

    if st.button("📄 Download as Word Document"):
        subject_label = st.session_state.get("subject", "Study")
        docx_bytes = export_to_docx(qa_pairs, subject_label)
        st.download_button(
            label="⬇️ Click to Download .docx",
            data=docx_bytes,
            file_name=f"{subject_label}_QA.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
