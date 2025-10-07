# Description: This script reads city data from a tab-separated text file, extracts and processes geographical and administrative information, quantizes latitude and longitude values, and then exports the structured data into a JSON file.
# Tags: Data Transformation, File Parsing, Data Extraction, JSON Export, Geographical Data, Data Cleaning

import csv
import json
import math

# Input and output file paths
input_file = "BG.txt"   # your space-separated file
output_file = "cities_bulgaria.json"

data = []


def q(x, d=4):  # quantize to d decimals
    return round(float(x), d)


with open(input_file, "r", encoding="utf-8") as f:
    # use tab or space depending on actual delimiter
    reader = csv.reader(f, delimiter="\t")
    for row in reader:
        if not row or len(row) < 15:
            continue  # skip malformed rows

        city = row[1].strip()
        alt_names = row[3].split(",") if row[3] else []
        lat = row[4].strip()
        lng = row[5].strip()
        iso2 = row[9].strip()
        admin_name = row[12].strip() if len(row) > 12 else ""
        if admin_name == "":
            continue

        entry = {
            "city": city,
            "alt_names": [name.strip() for name in alt_names if name.strip()],
            "lat": q(lat, 4),
            "lng": q(lng, 4),
            "admin_name": row[12].strip() if len(row) > 12 else "",
        }
        data.append(entry)

# Write to JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Saved {len(data)} records to {output_file}")