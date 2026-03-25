import os
from translate import Translator

## Files to translate
files_to_translate = ["README.md", "CHANGELOG.md"]

## Target languages
languages = {
    "es": "es",  # Spanish
    "fr": "fr",  # French
    "de": "de",  # German
    "en": "en"   # English
}

## Loop through files
for file_path in files_to_translate:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    for lang_code, lang_target in languages.items():
        ## Initialize translator
        translator = Translator(to_lang=lang_target)
        translated_text = translator.translate(content)

        ## Prepare output directory
        output_dir = f"docs/{lang_code}"
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, file_path)

        ## Write translated file
        with open(output_file, "w", encoding="utf-8") as out_f:
            out_f.write(translated_text)

        print(f"{file_path} translated to {lang_code}")
