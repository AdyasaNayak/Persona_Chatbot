def read_transcript(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def chunk_text(text, max_tokens=500):
    # Simple word-based chunking
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_tokens):
        chunk = " ".join(words[i:i + max_tokens])
        chunks.append(chunk)

    return chunks


def save_chunks(chunks, output_file="hitesh_chunks.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks, 1):
            f.write(f"--- Chunk {i} ---\n")
            f.write(chunk + "\n\n")


if __name__ == "__main__":
    text = read_transcript("hitesh_transcript_clean.txt")
    chunks = chunk_text(text, max_tokens=500)  # adjust tokens as needed
    save_chunks(chunks)
    print(f"✅ Chunking done. Total chunks: {len(chunks)}")
