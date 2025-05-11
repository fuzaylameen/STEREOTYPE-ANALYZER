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

## Stereotype classification criteria

1. If the movie shows men most of the time, check if it’s about war, prison escape, survival, or police action. If not, and women appear only briefly and are focused on love or care without personal goals, label it as gender-stereotypical.
2. When women try to achieve goals but only succeed with help from a man (often the hero), label it as gender-stereotypical.
3. When a girl falls in love with a man after repeated stalking or harassment, label this romanticization as stereotypical.
4. When a girl admires or loves a man purely because he engages in violence or fights, without knowing him well, label this as a stereotype.
5. When a man says something like "Would you do that to your daughter/sister/mother?" to highlight wrong actions, it reduces women's value to relationships with men — label it as stereotypical.
6. If a normal man (not villain) makes body comments about a woman and it is taken lightly or humorously, mark it as a stereotype.
7. When women are shown dancing in pubs or wearing short dresses in scenes irrelevant to the plot and enjoyed by men (including the hero), label it as objectification.
8. If boys are shown attracted to naive or unknowing girls, as if innocence is the most desirable trait, label this as stereotypical.
9. If a girl talking to or laughing with another man causes the hero to react with jealousy or rage, label it as enforcing possessiveness.
10. Regressive comments (sexist, judgmental) made by men and presented as jokes or accepted by others without pushback, should be marked as normalized stereotypes.
11. If men are portrayed as sad and women as happy after a breakup, without depth or emotional balance, mark it as a stereotype.
12. If women admire or fall in love with rich men mainly due to wealth/status, label that as a stereotype.
13. If rich men are portrayed as arrogant or boastful and it’s glorified, mark it as stereotype.
14. If a man gives advice to a woman who appears confused and she agrees to him due to that confusion (not clarity), label it as manipulative and stereotypical. If both agree happily and clearly, do not label it.

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
