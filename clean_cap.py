import re

def clean_vtt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        if re.match(r"^\d{2}:\d{2}:\d{2}", line) or "-->" in line:
            continue
        line = line.strip()
        if line and not line.isdigit():
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

if __name__ == "__main__":
    input_file = "-8UsDtDsSfw.en.vtt"
    output_file = "hitesh_transcript_clean.txt"

    cleaned = clean_vtt(input_file)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"✅ Transcript saved to: {output_file}")
