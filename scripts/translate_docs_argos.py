import os
import argostranslate.package
import argostranslate.translate

# Files to translate
files_to_translate = ["README.md", "CHANGELOG.md"]

# Languages to translate into
target_languages = ["es", "fr", "de"]  # Spanish, French, German

# Warning note
warning_note = (
    "> **Note:** Automatic translations are provided for convenience. "
    "They may not be 100% accurate. For reliable content, please refer to the "
    "original English documentation or verified translations.\n\n"
)

print("Updating Argos Translate package index...")
argostranslate.package.update_package_index()

available_packages = argostranslate.package.get_available_packages()
print(f"Found {len(available_packages)} packages in index")

# Install only the needed ones
for pkg in available_packages:
    # only install if it's a translation from English to our target
    if pkg.from_code == "en" and pkg.to_code in target_languages:
        print(f"Installing model: {pkg.from_code} → {pkg.to_code}")
        download_path = pkg.download()
        argostranslate.package.install_from_path(download_path)

# Load the installed languages
installed_languages = argostranslate.translate.get_installed_languages()
print(f"Installed language codes: {[lang.code for lang in installed_languages]}")

# find English source language
source_lang_list = [lang for lang in installed_languages if lang.code == "en"]
if not source_lang_list:
    raise Exception("English source language not installed")
source_lang = source_lang_list[0]

# split large text into chunks
def chunk_text(text, max_len=1000):
    return [text[i:i+max_len] for i in range(0, len(text), max_len)]

for file_path in files_to_translate:
    if not os.path.exists(file_path):
        print(f"Skipping {file_path}: file not found")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for target_code in target_languages:
        target_lang_list = [lang for lang in installed_languages if lang.code == target_code]
        if not target_lang_list:
            print(f"Target language '{target_code}' not installed — skipping")
            continue
        target_lang = target_lang_list[0]

        translation = source_lang.get_translation(target_lang)

        translated_chunks = [translation.translate(chunk) for chunk in chunk_text(content)]
        translated_text = warning_note + "\n".join(translated_chunks)

        out_dir = f"docs/{target_code}"
        os.makedirs(out_dir, exist_ok=True)
        out_file = os.path.join(out_dir, file_path)

        with open(out_file, "w", encoding="utf-8") as out_f:
            out_f.write(translated_text)

        print(f"Translated {file_path} → {target_code}")
