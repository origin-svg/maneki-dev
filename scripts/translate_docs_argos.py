import os
import argostranslate.package
import argostranslate.translate

# Files to translate
files_to_translate = ["README.md", "CHANGELOG.md"]

# Target languages
languages = {
    "es": "es",  # Spanish
    "fr": "fr",  # French
    "de": "de"   # German
}

# Load installed languages
installed_languages = argostranslate.translate.get_installed_languages()
source_lang = [lang for lang in installed_languages if lang.code == "en"][0]

def chunk_text(text, max_len=1000):
    """Split text into chunks to avoid extremely long translations."""
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]

for file_path in files_to_translate:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for lang_code, target_code in languages.items():
        target_lang = [lang for lang in installed_languages if lang.code == target_code][0]
        translation = source_lang.get_translation(target_lang)
        
        translated_chunks = [translation.translate(chunk) for chunk in chunk_text(content)]
        translated_text = "\n".join(translated_chunks)

        output_dir = f"docs/{lang_code}"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, file_path)

        with open(output_file, "w", encoding="utf-8") as out_f:
            out_f.write(translated_text)

        print(f"{file_path} translated to {lang_code}")
