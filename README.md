# 🎬 STEREOTYPE-ANALYZER

**AI-Powered Tool to Detect Gender Stereotypes in Bollywood Content (1970–2017)**

---

##  Objective

This project aims to identify, quantify, and reduce gender-based stereotypes in Bollywood films using Artificial Intelligence and Machine Learning. The system analyzes various media inputs such as scripts, trailers, and posters to highlight gender bias in character roles, dialogue, emotions, and screen time.

---

##  Key Features

### Script Analysis
- Extracts dialogues from PDF movie scripts.
- Translates non-English content to English.
- Cleans and merges multiline dialogues.
- Matches content against known stereotype phrases using sentence embeddings.

### Trailer Analysis
- Processes video files to detect faces and identify gender/emotion via facial recognition.
- Calculates gender-wise screen time and emotional diversity.

### Bias Detection
- Uses sentence-transformers and cosine similarity to match text with stereotypical roles or patterns.
- Flags content with potential gender bias.
- Recommends improvements for inclusive representation.

---

## Technologies & Libraries

- `streamlit` – Frontend interface
- `pdfplumber` – Extract text from movie scripts (PDF)
- `langdetect` – Detect language
- `deep-translator` – Translate Hindi/Hinglish to English
- `sentence-transformers` – Sentence embedding generation
- `torch` – Deep learning support
- `opencv-python` – Video frame processing
- `deepface` – Facial recognition and emotion detection
- `numpy` – Data manipulation

---

## 📁 Project Structure
```
STEREOTYPE-ANALYZER/
├── app.py  Streamlit frontend
├── cleaner.py Script cleaning and dialogue parser
├── main.py Core processing logic
├── translate.py Language detection and translation
├── test_doc.pdf Sample script for testing
├── test_vdo.mp4 Sample trailer for testing
├── demo_vdo.mp4  Demo video showing how the app works
├── scripts/ [Create this folder to store trained models or embeddings] 
```
---
## ⚙ Getting Started

###  Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR-USERNAME/STEREOTYPE-ANALYZER.git
   cd STEREOTYPE-ANALYZER2
   ```
2. **Install required packages**
```bash
pip install -r requirements.txt
```
3. **Create scripts/ folder (if not already present)**
```bash
mkdir scripts
```

4. **This is used to store model embeddings, processed data, and intermediate results.**
Run the Streamlit App
```bash
streamlit run app.py
```

---

 Demo

Watch demo.mp4 for a quick walkthrough of the application’s features and usage.

---

 Test Files

test_doc.pdf and test_vdo.pdf: Sample movie scripts for testing analysis modules.


---

 Notes

Ensure that required pre-trained models for DeepFace and sentence-transformers are downloaded when first used.
The tool is in active development—poster and Wikipedia summary analysis modules will be added in future versions.
