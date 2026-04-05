# MedStudy AI 🧬

An AI-powered study tool that turns your lecture handouts into exam-ready Q&A, using only your handout as the source of truth.

## Features
- Upload any lecture PDF
- Claude generates exam-style questions and answers from the handout only
- Preview all Q&A in the app
- Export to Word document (.docx)

## Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/medstudy-ai.git
cd medstudy-ai
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run locally
```bash
streamlit run app.py
```

## Deploy on Streamlit Community Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select this repo and set `app.py` as the main file
5. Add your Anthropic API key as a **Secret**:
   - Key: `ANTHROPIC_API_KEY`
   - Value: `sk-ant-...`
6. Deploy!

## How to use
1. Enter your Anthropic API key (or set it as a secret in deployment)
2. Upload your lecture handout PDF
3. Set how many questions you want
4. Click **Generate Exam Q&A**
5. Review and download as Word doc

## Tech Stack
- [Streamlit](https://streamlit.io) — UI
- [Anthropic Claude](https://anthropic.com) — AI Q&A generation
- [PyMuPDF](https://pymupdf.readthedocs.io) — PDF text extraction
- [python-docx](https://python-docx.readthedocs.io) — Word export
