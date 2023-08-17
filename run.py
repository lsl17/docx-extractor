from extraction import process_docx_and_save_to_json
from correction import correct_translation_from_files


def main():
    # Define base file name
    base_filename = "KFS_ISF_ALL_CHINA_EQUITY"
    # Define file paths
    original_docx_path = f"sources/KFS Paired document/{base_filename}_E.docx"
    translation_docx_path = f"sources/KFS Paired document/{base_filename}_C.docx"
    original_json_path = f"{base_filename}_E.json"
    translation_json_path = f"{base_filename}_C.json"
    corrected_translation_json_path = translation_json_path

    # Extract content from the DOCX files and save to JSON files
    process_docx_and_save_to_json(original_docx_path, original_json_path)
    process_docx_and_save_to_json(translation_docx_path, translation_json_path)

    # Correct the translation JSON using the original JSON
    correct_translation_from_files(
        original_json_path, translation_json_path, corrected_translation_json_path)


if __name__ == "__main__":
    main()
