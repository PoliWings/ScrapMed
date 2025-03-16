import os
import json
import csv
import pathlib

UNALLOWED_LICENSES = ['CC BY-ND', 'CC BY-NC-ND']

def check_license(license):
    if not license:
        return True
    return all(unallowed not in license for unallowed in UNALLOWED_LICENSES)

def normalize_url(url):
    return url.replace(' ', '%20')

def search_json(json_data, filename):
    for item in json_data:
        path = item['files'][0]['path']
        if pathlib.Path(path).stem == pathlib.Path(filename).stem:
            title = item.get('title', '') or ""
            title = title.replace('\n', '').replace('\r', '') if isinstance(title, str) else ""
            license = item.get('license', "") or ""
            url = normalize_url(item['file_urls'][0]) if 'file_urls' in item and item['file_urls'] else ""
            return title, url, license
    return "", "", ""

def generate_csv(input_folder, input_json, output_csv):
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
    num_files = len(files)
    deleted_files = 0
    print(f"Found {num_files} files")

    with open(input_json, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)

    results = []

    for idx, filename in enumerate(files):
        title, url, license = search_json(json_data, filename)
        if check_license(license):
            results.append([filename, title, url, license])
        else:
            print(f"\r{filename} has unallowed license: {license}. DELETING")
            os.remove(os.path.join(input_folder, filename))
            deleted_files += 1
        print(f"\rProcessed {idx + 1}/{num_files} files | {deleted_files} deleted", end="")

    results.sort(key=lambda x: x[0])

    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["filename", "title", "url", "license"])
        csv_writer.writerows(results)

    print("\nCSV file generated and sorted successfully.")

if __name__ == "__main__":
    input_folder = "../extractor/parsed"
    input_json = "../scraper/termedia/output.json"
    output_csv = "output.csv"
    generate_csv(input_folder, input_json, output_csv)
