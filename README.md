# STEREOTYPE-ANALYZER

**AI-Powered Tool to Detect Gender Stereotypes in Bollywood Scripts (1970–2017)**

---

## Objective

This tool leverages AI and NLP to detect gender stereotypes in Bollywood movie scripts. It extracts text from PDFs, processes the content, and uses a prompt-based LLM (via Ollama and LLaMA 3.2) to highlight scenes, dialogues, and characters that may portray biased gender representations.

---

## Features

### Script Analysis
- Extracts text from PDF scripts using `pdfplumber` and fallback OCR via `pytesseract`.
- Accepts both clean and scanned PDF formats.
- Sends analyzed script data to a local LLM using the `ollama` interface.
- Highlights dialogues/actions reinforcing traditional or harmful gender stereotypes.

### LLM Integration
- Communicates with LLaMA 3.2 running via `ollama`.
- Uses a detailed prompt containing predefined stereotype patterns.
- Outputs human-readable findings including:
  - **Scene Description**
  - **Dialogue/Action**
  - **Involved Characters**
  - **Reason for Stereotypical Label**

---

## Technologies & Libraries

- `streamlit` – Interactive frontend
- `pdfplumber` – Text extraction from PDFs
- `pytesseract` – OCR for scanned pages
- `pdf2image` – Convert PDF pages to images for OCR
- `subprocess` – Interface with Ollama (LLM backend)
- `tempfile` – Securely handle uploaded PDFs

---

## Project Structure

```
STEREOTYPE-ANALYZER/
├── app.py # Main Streamlit app
├── test_doc.pdf # Sample movie script
├── requirements.txt # Python dependencies
├── README.md # Project documentation
```


> *Note:* This version is focused solely on script analysis. Future updates will expand to include trailer and poster analysis.

---

## Installation & Usage

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR-USERNAME/STEREOTYPE-ANALYZER.git
cd STEREOTYPE-ANALYZER
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Streamlit App
```bash
streamlit run app.py
```

Ollama must be installed and running locally with LLaMA 3.2 pulled.
You can install it from https://ollama.com

### Sample Output

Once a script is uploaded and analyzed, the tool outputs structured sections like:

Scene Description: [Brief text...]
Dialogue/Action: "She only falls for him after he fights the goons."
Characters: Male (Hero), Female (Love Interest)
Reason: Romanticization of violence and submission.

### Requirements

Make sure your requirements.txt includes:
```bash
streamlit
pdfplumber
pytesseract
pdf2image
```

Also ensure:

Tesseract OCR is installed on your system.
Ollama is installed and configured with a model like llama3.

### Test Script

Use test_doc.pdf included in the repo to test the tool’s functionality.

### Future Work

Poster Analysis – Detect objectification or visual bias.
Trailer Analysis – Emotion detection, screen time stats.
Wikipedia Summary Bias – NLP-based summary checks.
