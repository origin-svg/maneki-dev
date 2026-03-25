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

# Add a warning note at top of translated docs
warning_note = (
    "> **Note:** Automatic translations are provided for convenience. "
    "They may not be 100% accurate. For the most reliable content, please refer "
    "to the original documentation in English or preset trusted translations.\n\n"
)

# ---------------------------
# Install models via package index
# ---------------------------
# Update package index
argostranslate.package.update_package_index()

# Get all available packages
available_packages = argostranslate.package.get_available_packages()

# List of language pairs we want (from en → XX)
pairs = [( "en", "es" ), ( "en", "fr" ), ( "en", "de" )]

for from_code, to_code in pairs:
    # Find the matching package
    pkg = next(
        (
            p
            for p in available_packages
            if p.from_code == from_code and p.to_code == to_code
        ),
        None
    )
    if pkg:
        path = pkg.download()
        argostranslate.package.install_from_path(path)

# ---------------------------
# Load installed languages
# ---------------------------
installed = argostranslate.translate.get_installed_languages()

# Get English language object
source_lang_list = [lang for lang in installed if lang.code == "en"]
if not source_lang_list:
    raise Exception("English language not installed after package install")
source_lang = source_lang_list[0]

# Helper: split text into chunks
def chunk_text(text, max_len=1000):
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]

# ---------------------------
# Translate files
# ---------------------------
for file_path in files_to_translate:
    if not os.path.exists(file_path):
        print(f"{file_path} not found, skipping")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for lang_code, target_code in languages.items():
        target_lang_list = [lang for lang in installed if lang.code == target_code]
        if not target_lang_list:
            print(f"Target language '{target_code}' missing, skipping")
            continue
        target_lang = target_lang_list[0]

        translation = source_lang.get_translation(target_lang)
        translated_chunks = [translation.translate(chunk) for chunk in chunk_text(content)]
        translated_text = warning_note + "\n".join(translated_chunks)

        out_dir = f"docs/{lang_code}"
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, file_path)

        with open(out_file, "w", encoding="utf-8") as out_f:
            out_f.write(translated_text)

        print(f"{file_path} translated to {lang_code}")
