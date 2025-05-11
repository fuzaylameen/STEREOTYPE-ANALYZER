import streamlit as st
import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import subprocess
import tempfile

# --- Hardcoded stereotype analysis prompt ---
GENDER_STEREOTYPE_PROMPT = """
"Please analyze the following movie script and detect any gender stereotypes based on the patterns provided. For each scene that is gender-stereotypical, list the following:

Scene Description: A brief summary of the scene.

Dialogue/Action: Any dialogue or action that matches the gender stereotype pattern.

Character(s): List the characters involved, specifying their gender where possible (use 'Male' or 'Female').

Reason for Stereotypical Label: Explain why this scene fits the gender stereotype, based on the following patterns:

Gender Stereotypical Patterns:

If the movie shows men most of the time, check if it’s about war, prison escape, survival, or police action. If not, and women appear only briefly and are focused on love or care without personal goals, label it as gender-stereotypical.

When women try to achieve goals but only succeed with help from a man (often the hero), label it as gender-stereotypical.

When a girl falls in love with a man after repeated stalking or harassment, label this romanticization as stereotypical.

When a girl admires or loves a man purely because he engages in violence or fights, without knowing him well, label this as a stereotype.

When a man says something like "Would you do that to your daughter/sister/mother?" to highlight wrong actions, it reduces women's value to relationships with men — label it as stereotypical.

If a normal man (not villain) makes body comments about a woman and it is taken lightly or humorously, mark it as a stereotype.

When women are shown dancing in pubs or wearing short dresses in scenes irrelevant to the plot and enjoyed by men (including the hero), label it as objectification.

If boys are shown attracted to naive or unknowing girls, as if innocence is the most desirable trait, label this as stereotypical.

If a girl talking to or laughing with another man causes the hero to react with jealousy or rage, label it as enforcing possessiveness.

Regressive comments (sexist, judgmental) made by men and presented as jokes or accepted by others without pushback, should be marked as normalized stereotypes.

If men are portrayed as sad and women as happy after a breakup, without depth or emotional balance, mark it as a stereotype.

If women admire or fall in love with rich men mainly due to wealth/status, label that as a stereotype.

If rich men are portrayed as arrogant or boastful and it’s glorified, mark it as stereotype.

If a man gives advice to a woman who appears confused and she agrees to him due to that confusion (not clarity), label it as manipulative and stereotypical. If both agree happily and clearly, do not label it."
"""

# --- Text extraction using pdfplumber and OCR ---
def extract_text_from_pdf(pdf_file_path):
    full_text = []
    with pdfplumber.open(pdf_file_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                full_text.append(f"--- Page {i+1} ---\n{text}")
    return "\n\n".join(full_text)

def extract_text_with_ocr(pdf_path):
    images = convert_from_path(pdf_path)
    full_text = []
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        if text.strip():
            full_text.append(f"--- OCR Page {i+1} ---\n{text}")
    return "\n\n".join(full_text)

# --- Fixed subprocess handler for Ollama ---
def query_ollama(prompt, model_name="llama3.2"):
    try:
        st.info("⏳ Sending prompt to LLaMA 3.2 via Ollama...")
        result = subprocess.run(
            ["ollama", "run", model_name],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=300  # 5 minutes for large input
        )
        if result.returncode != 0:
            return f"❌ Ollama Error:\n{result.stderr.decode('utf-8')}"
        return result.stdout.decode("utf-8")
    except subprocess.TimeoutExpired:
        return "❌ Ollama timed out. Try a shorter prompt or smaller input."
    except Exception as e:
        return f"❌ Unexpected Error: {str(e)}"

# --- Streamlit UI ---
st.set_page_config(page_title="🎬 Gender Stereotype Detector", layout="centered")
st.title("🎬 Detect Gender Stereotypes in Movie Scripts")

uploaded_pdf = st.file_uploader("Upload a movie script in PDF format", type=["pdf"])

if uploaded_pdf:
    if st.button("🔍 Analyze for Gender Stereotypes"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_pdf.read())
            tmp_path = tmp_file.name

        with st.spinner("📖 Extracting text from PDF..."):
            pdf_text = extract_text_from_pdf(tmp_path)
            if not pdf_text.strip():
                st.warning("⚠️ No readable text found via pdfplumber. Attempting OCR...")
                pdf_text = extract_text_with_ocr(tmp_path)

            if not pdf_text.strip():
                st.error("❌ No readable text found, even with OCR.")
                st.stop()

        with st.expander("📄 Preview Extracted Script Text"):
            st.text(pdf_text[:3000])  # Show first 3000 characters

        # Limit prompt size to avoid overflow (approx. 7,000 characters)
        MAX_CHARS = 7000
        shortened_text = pdf_text[:MAX_CHARS]
        full_prompt = f"{GENDER_STEREOTYPE_PROMPT}\n\nScript:\n\"\"\"\n{shortened_text}\n\"\"\""

        # Show prompt length for debugging
        st.caption(f"📏 Prompt Length: {len(full_prompt)} characters")

        with st.spinner("🤖 Analyzing script with LLaMA 3.2..."):
            result = query_ollama(full_prompt)

        st.subheader("🧠 LLaMA 3 Analysis Result")
        st.write(result)