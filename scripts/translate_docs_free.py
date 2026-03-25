import os
from translate import Translator

MAX_CHARS = 500
files_to_translate = ["README.md", "CHANGELOG.md"]
languages = {
    "es": "es",  # Spanish
    "fr": "fr",  # French
    "de": "de",  # German
    "en": "en"   # English
}

source_lang = "en"  # Original Language

def chunk_text(text, max_len=MAX_CHARS):
    chunks = []
    while text:
        chunk = text[:max_len]
        if len(chunk) == max_len and '\n' in chunk:
            last_newline = chunk.rfind('\n')
            chunk, text = chunk[:last_newline], text[last_newline:]
        else:
            text = text[max_len:]
        chunks.append(chunk)
    return chunks

for file_path in files_to_translate:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for lang_code, lang_target in languages.items():
        if lang_target == source_lang:
            continue  # Dont Translate Same Language

        translator = Translator(from_lang=source_lang, to_lang=lang_target)
        translated_chunks = [translator.translate(chunk) for chunk in chunk_text(content)]
        translated_text = "\n".join(translated_chunks)

        output_dir = f"docs/{lang_code}"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, file_path)

        with open(output_file, "w", encoding="utf-8") as out_f:
            out_f.write(translated_text)

        print(f"{file_path} translated to {lang_code}")
