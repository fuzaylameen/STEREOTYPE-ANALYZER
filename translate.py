import pdfplumber
import re
from langdetect import detect
from deep_translator import GoogleTranslator
import warnings
warnings.filterwarnings("ignore")


def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:   
                text += "\n" + page_text
    return text

def clean_text(raw_text):
    text = re.sub(r'[^\x00-\x7F\u0900-\u097F\sA-Za-z0-9.,;:\-!?\'\"\n]', '', raw_text)
    text = re.sub(r'\n{2,}', '\n', text)
    text = re.sub(r'[ ]{2,}', ' ', text)
    return text

def is_duplicate(line1, line2):
    return line1.strip().lower() == line2.strip().lower()

def translate_line(line):
    try:
        lang = detect(line)
        if lang in ['hi', 'mr', 'ur']: 
            translated = GoogleTranslator(source='auto', target='en').translate(line)
            return translated
        elif lang == 'en':  
            return line
        else:  
            return line
    except:
        return line  

def remove_duplicates_and_translate(text):
    lines = text.split('\n')
    cleaned_lines = []
    prev_line = ""
    
    for line in lines:
        line = line.strip()
        if len(line) < 2:
            continue

        if not is_duplicate(prev_line, line):
            translated_line = translate_line(line)
            cleaned_lines.append(translated_line)
            prev_line = line
    return "\n".join(cleaned_lines)

def process_pdf(pdf_path, output_path="scripts/cleaned_translated_script.txt"):
    raw = extract_text_from_pdf(pdf_path)
    cleaned = clean_text(raw)
    translated = remove_duplicates_and_translate(cleaned)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(translated)
    
    print(f"[✓] Cleaned and translated script saved to: {output_path}")
