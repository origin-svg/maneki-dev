import os
import requests
import argostranslate.package
import argostranslate.translate

# ----------------------------
# CONFIGURATION
files_to_translate = ["README.md", "CHANGELOG.md"]

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

# Argos Translate model URLs
model_urls = [
    "https://www.argosopentech.com/packages/translate-en.argosmodel",
    "https://www.argosopentech.com/packages/translate-en_es.argosmodel",
    "https://www.argosopentech.com/packages/translate-en_fr.argosmodel",
    "https://www.argosopentech.com/packages/translate-en_de.argosmodel"
]

# INSTALL MODELS
for url in model_urls:
    package_filename = os.path.basename(url)
    if not os.path.exists(package_filename):
        print(f"Downloading {package_filename}...")
        r = requests.get(url)
        r.raise_for_status()
        with open(package_filename, "wb") as f:
            f.write(r.content)
    print(f"Installing {package_filename}...")
    argostranslate.package.install_from_path(package_filename)

# LOAD INSTALLED LANGUAGES
installed_languages = argostranslate.translate.get_installed_languages()

# Validate source language (English)
source_lang_list = [lang for lang in installed_languages if lang.code == "en"]
if not source_lang_list:
    raise Exception("English source language not installed in Argos Translate")
source_lang = source_lang_list[0]

# ----------------------------
# HELPER
def chunk_text(text, max_len=1000):
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]

# TRANSLATE FILES
for file_path in files_to_translate:
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist, skipping...")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for lang_code, target_code in languages.items():
        # Validate target language
        target_lang_list = [lang for lang in installed_languages if lang.code == target_code]
        if not target_lang_list:
            print(f"Target language '{target_code}' not installed, skipping...")
            continue
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
