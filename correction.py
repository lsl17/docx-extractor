import json
from typing import Any, List, Dict, Optional, Union


def load_json(filename: str) -> Union[List[Any], Dict[str, Any]]:
    """
    Load JSON data from a file.

    :param filename: Path to the JSON file.
    :return: Loaded JSON data.
    :raises FileNotFoundError: If the file is not found.
    :raises json.JSONDecodeError: If there's an issue decoding the JSON.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
        raise
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from {filename}.")
        raise


def save_json(filename: str, data: Union[List[Any], Dict[str, Any]]) -> None:
    """
    Save data to a JSON file.

    :param filename: Path to save the JSON data.
    :param data: Data to be saved.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def count_headers(data: List[Dict[str, Any]]) -> int:
    """
    Count the number of headers in the data.

    :param data: List of content items.
    :return: Number of headers.
    """
    return sum(1 for item in data if item.get('location') == 'header')


def get_first_header_index(data: List[Dict[str, Any]]) -> Optional[int]:
    """
    Get the index of the first header in the data.

    :param data: List of content items.
    :return: Index of the first header or None if not found.
    """
    for index, item in enumerate(data):
        if item.get('location') == 'header':
            return index
    return None


def correct_headers(origin: List[Dict[str, Any]], translation: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Correct the headers in the translated data based on the original.

    :param origin: List of original content items.
    :param translation: List of translated content items.
    :return: Corrected list of translated content items.
    """
    origin_header_count = count_headers(origin)
    translation_header_count = count_headers(translation)
    header_difference = origin_header_count - translation_header_count
    corrected_items = []

    if header_difference > 0:
        for i in range(header_difference):
            if translation[i]['location'] == 'body':
                translation[i]['location'] = 'header'
                translation[i]['modified'] = True
                corrected_items.append(translation[i])
        translation = translation[header_difference:]
        first_header_index = get_first_header_index(translation)
        if first_header_index is not None:
            translation[first_header_index:first_header_index] = corrected_items
        else:
            translation.extend(corrected_items)

    return translation


def correct_translation_from_files(original_url: str, translation_url: str, output_path: str = 'corrected_translation.json') -> None:
    """
    Load JSON from original and translation URLs, correct the headers, 
    and save the corrected translation to an output file.

    :param original_url: Path to the original JSON file.
    :param translation_url: Path to the translated JSON file.
    :param output_path: Path to save the corrected translation. Defaults to 'corrected_translation.json'.
    """
    try:
        origin = load_json(original_url)
        translation = load_json(translation_url)
        corrected_translation = correct_headers(origin, translation)
        save_json(output_path, corrected_translation)
    except Exception as e:
        print(f"Error during the correction process: {e}")


# Usage example:
if __name__ == '__main__':
    original_path = 'KFS - CT European Fund_E.json'
    translation_path = 'KFS - CT European Fund_C.json'
    correct_translation_from_files(original_path, translation_path)
