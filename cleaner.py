def clean_script_lines(lines):
    dialogues = []
    current_dialogue = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.isupper() and len(line.split()) <= 4:
            if current_dialogue:
                dialogues.append(" ".join(current_dialogue).strip())
                current_dialogue = []
        else:
            current_dialogue.append(line)

    if current_dialogue:
        dialogues.append(" ".join(current_dialogue).strip())

    return dialogues


def process_script(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_lines = f.readlines()

    cleaned_dialogues = clean_script_lines(raw_lines)

    with open(output_path, 'w', encoding='utf-8') as f:
        for dialogue in cleaned_dialogues:
            f.write(dialogue + '\n')



if __name__ == "__main__":
    input_file = "cleaned_translated_script.txt"        # Replace with your input file
    output_file = "cleaned_dialogues.txt"  # Output will be saved here
    process_script(input_file, output_file)
    print(f"✅ Cleaned dialogues saved to: {output_file}")
