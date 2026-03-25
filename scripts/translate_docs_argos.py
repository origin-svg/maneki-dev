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

# Warning note to prepend to translations
warning_note = (
    "> **Note:** Automatic translations are provided for convenience. "
    "They may not be 100% accurate. For the most reliable content, please refer "
    "to the original documentation in English or the preset translations.\n\n"
)

# Load installed languages
installed_languages = argostranslate.translate.get_installed_languages()

# Validate source language (English)
source_lang_list = [lang for lang in installed_languages if lang.code == "en"]
if not source_lang_list:
    raise Exception("English source language not installed in Argos Translate")
source_lang = source_lang_list[0]

def chunk_text(text, max_len=1000):
    """Split text into chunks for safety."""
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]

for file_path in files_to_translate:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for lang_code, target_code in languages.items():
        # Validate target language
        target_lang_list = [lang for lang in installed_languages if lang.code == target_code]
        if not target_lang_list:
            raise Exception(f"Target language '{target_code}' not installed in Argos Translate")
        target_lang = target_lang_list[0]

        translation = source_lang.get_translation(target_lang)
        translated_chunks = [translation.translate(chunk) for chunk in chunk_text(content)]
        translated_text = warning_note + "\n".join(translated_chunks)

        output_dir = f"docs/{lang_code}"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, file_path)

        with open(output_file, "w", encoding="utf-8") as out_f:
            out_f.write(translated_text)

        print(f"{file_path} translated to {lang_code}")
