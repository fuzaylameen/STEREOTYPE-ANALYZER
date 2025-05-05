import translate 
from sentence_transformers import SentenceTransformer, util
import torch
import csv
import warnings
import cleaner
warnings.filterwarnings("ignore")


def is_valid_sentence(line):
    words = line.split()
    if len(words) < 3:
        return False
    if line.isupper() or line.istitle(): 
        return False
    return True

def process_pdf_and_analyze(pdf_path):
    translate.process_pdf(pdf_path)
    cleaner.process_script("scripts/cleaned_translated_script.txt", "cleaned_dialogues.txt")
    cleaned_script_path = "cleaned_dialogues.txt"

    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    stereotype_lines = [
        "Ladkiyon ko sundar aur shaant hona chahiye.",
        "Usne uski madad ki kyunki woh akeli thi.",
        "Uska sapna sirf shaadi karna hai.",
        "Woh leader nahi ban sakti, woh bahut emotional hai.",
        "Veera is getting her mehendi applied",
        "Main sirf achhi achhi cheezein hi sochna chahti hoon.",
        "Tum ladki ho, shaadi hone waali hai.",
        "Bahut paisa hai na tum log ke paas!",
        "Main tumhare saath jaana chahti hoon.",
        "Main toot gayi thi... par kisi ne dekha hi nahi.",
        "Shaadi ke baad sab theek ho jaata hai",
        "He never shows sadness but constantly erupts in rage.",
        "She frequently cries or breaks down",
        "He is introduced wielding a gun and shouting.",
        "Veera begins to fall for Mahabir during their escape.",
        "Tum ladki ho, shaadi hone waali hai.",
        "Main sirf achhi achhi cheezein hi sochna chahti hoon.",
        "Shaadi ke baad sab theek ho jaata hai.",
        "Main toot gayi thi... par kisi ne dekha hi nahi.",
        "Tumhare jaisi ladkiyaan kya jaane zindagi kya hoti hai?",
        "Aisi ladkiyon ke saath toh aisa hi hota hai.",
        "Ladkiyon ko zyada bolna nahi chahiye.",
        "Main tumhare saath jaana chahti hoon.",
        "Tum logon ke paas paisa hai, izzat hai, sab kuch hai!",
        "Mahabir is introduced holding a gun and barking orders.",
        "Veera breaks down crying alone in the van.",
        "Mahabir never shows emotions, only rage.",
        "Veera is shown trying on wedding clothes, surrounded by jewelry.",
        "Usne tujhe kuch kiya toh nahi? (Did he do anything to you?)",
        "Aurat ki izzat sabse badi hoti hai.",
        "Women and children should not interfere in men’s matters.",
        "Tum logon ka kaam sirf rona hai.",
        "Mard ko dard nahi hota.",
        "Tum to aurat ho, tum kya samjhogi.",
        "Larki ko thoda seedha hi rehna chahiye.",
        "Woh to maa hai, uska farz hai sab kuchh bardasht karna.",
        "Shaadi ke baad ladkiyon ke sapne waise bhi khatam ho jaate hain.",
        "Tum ladki ho, tumhein zyada samajhna nahi chahiye.",
        "Main apni zindagi ki train mein kisi aur ke saath chali gayi thi.",
        "Tum jaise ladkiyon ko toh ghar sambhalna chahiye, na ki akele safar karna.",
        "Kisi ladki ko ghar se bhaagte hue kabhi khushi nahi milti.",
        "Tumhe toh shaadi aur bachche sambhalne chahiye, career chhodo.",
        "Ek achhi ladki apne maa-baap ka ghar nahi chhodti.",
        "Ladkiyon ko itna khula nahi chhodna chahiye.",
        "Shaadi toh har ladki ka sapna hota hai.",
        "Itni bindass mat bano, ladkiyan aise nahi hoti.",
        "Ladkiyan jab roti hain tab hi achhi lagti hain.",
        "Ladki ka asli sukh toh pati ke saath hota hai.",
        "Tum ladki ho, tumhein kuch hadh mein rehna chahiye.",
        "Shaadi ke baad toh ladki apne ghar mein adjust karti hi hai.",
        "Ladkiyon ka kaam hota hai samjhauta karna.",
        "He looks lost. Doesnt speak much. She keeps talking.",
        "Tumhare jaise ladkiyan sirf shaadi ke liye hoti hain.",
        "Aurat ka asli kaam to ghar sambhalna hota hai.",
        "Ladki ghar mein rahe to hi izzat bani rehti hai.",
        "Tu ladki hai, tere bas ki baat nahi hai.",
        "Main teri izzat ke liye sab kuch kar sakta hoon.",
        "Ladkiyan toh chhoti chhoti baaton pe ro padti hain.",
        "Usne ek ladki ke liye apna sab kuch daav pe laga diya.",
        "Aurat ke liye sabse zaroori cheez uska pati hota hai.",
        "Kya samjhti hai apne aap ko? Ek ladki hokar itna attitude?",
        "Maa baap ne tujhe padhne ke liye nahi, shaadi ke liye paala hai.",
        "Usne mujhe dhoka diya, jaise sab ladkiyan deti hain.",
        "Ladkiyan zyada samajhdar nahi hoti.",
        "Teri izzat to ab usi din chali gayi thi jab tu us ladke ke saath pakdi gayi.",
        "Ladki jaat ko to apne paanv kabhi zameen pe nahi rakhne chahiye.",
        "Kisi se kuch kehna mat... warna koi shaadi nahi karega tujhse.",
        "Ladka hai... thoda bahut to chalta hai.",
        "Ladki ho, padhai likhai se kya hoga? Ghar hi to sambhalna hai.",
        "Kumari ladkiyan agar aise photo khinchvaayein to badnaam ho jaati hain.",
        "Tune hamari naak katwa di.",
        "A beautiful white lady enters",
        "Muscular hard passionate man"
        
    ]

    stereotype_embeddings = model.encode(stereotype_lines, convert_to_tensor=True)

    with open(cleaned_script_path, "r", encoding="utf-8") as file:
        content = file.read()

    
    script_lines = [line.strip() for line in content.splitlines() if line.strip() and is_valid_sentence(line)]
    script_embeddings = model.encode(script_lines, convert_to_tensor=True)

    results = []
    for i, line in enumerate(script_lines):
        similarities = util.cos_sim(script_embeddings[i], stereotype_embeddings)
        max_sim = float(torch.max(similarities))
        best_match_idx = int(torch.argmax(similarities))
        matched_example = stereotype_lines[best_match_idx]

        results.append({
            "Script Line": line,
            "Matched Stereotype": matched_example,
            "Similarity Score": round(max_sim, 3)
        })

    csv_file = "similarity_results.csv"
    with open(csv_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Script Line", "Matched Stereotype", "Similarity Score"])
        writer.writeheader()
        writer.writerows(results)

    print(f"\n✅ Results written to {csv_file}")

    stereotype_threshold = 0.8
    stereotype_only_file = "stereotypical_lines.csv"

    with open(stereotype_only_file, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Script Line", "Matched Stereotype", "Similarity Score"])
        writer.writeheader()
        for row in results:
            if row["Similarity Score"] >= stereotype_threshold:
                writer.writerow(row)

    print(f"✅ Stereotypical lines (score ≥ {stereotype_threshold}) written to {stereotype_only_file}")


if __name__ == "__main__":
    user_input = input("Enter the path to the PDF file: ").strip()
    process_pdf_and_analyze(user_input)
