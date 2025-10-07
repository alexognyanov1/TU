# Description: This script filters a list of cities from one JSON file based on matching names found in another JSON file, saving the result to a new file.
# Tags: Data Filtering, JSON Processing, Data Comparison, City Data

import json

# Paths to your files
FIRST_JSON_PATH = "ek_atte.json"   # JSON with ekatte, name, etc.
SECOND_JSON_PATH = "cities_bulgaria.json"  # JSON with lat/lon data
OUTPUT_JSON_PATH = "filtered_cities.json"


def normalize_name(name: str) -> str:
    """Normalize city/town names for comparison (case-insensitive, stripped)."""
    return name.strip().lower()


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    # Load both files
    first_data = load_json(FIRST_JSON_PATH)
    second_data = load_json(SECOND_JSON_PATH)

    # Build a set of valid names from the first dataset
    valid_names = set()
    for entry in first_data:
        if "name" in entry:
            valid_names.add(normalize_name(entry["name"]))
        if "name_en" in entry:
            valid_names.add(normalize_name(entry["name_en"]))

    # Filter second dataset
    filtered = []
    for entry in second_data:
        city = normalize_name(entry.get("city", ""))
        alt_names = [normalize_name(n) for n in entry.get("alt_names", [])]

        # Keep if city or any alt_name is in valid names
        if city in valid_names or any(alt in valid_names for alt in alt_names):
            filtered.append(entry)

    # Save filtered dataset
    save_json(filtered, OUTPUT_JSON_PATH)
    print(f"Filtered dataset saved to {OUTPUT_JSON_PATH}")
    print(
        f"Original count: {len(second_data)}, Filtered count: {len(filtered)}")


if __name__ == "__main__":
    main()