import os
import json
import csv
import pathlib

UNALLOWED_LICENSES = ['CC BY-ND', 'CC BY-NC-ND']

def check_license(license):
    for unallowed_license in UNALLOWED_LICENSES:
        if unallowed_license in license:
            return False
    return True

def search_json(json_data, filename):
    for item in json_data:
        path = item['files'][0]['path']
        if pathlib.Path(path).stem == pathlib.Path(filename).stem:
            title = None
            license = None
            url = item['file_urls'][0]
            if 'title' in item and isinstance(item['title'], str):
                title = item['title'].replace('\n', '').replace('\r', '')
            if 'license' in item:
                license = item['license']
            return title, url, license
    return None, None, None
        
def generate_csv(input_folder, input_json, output_csv):
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(".txt")]
    num_files = len(files)
    deleted_files = 0
    print(f"Found {num_files} files")
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["filename", "title", "url", "license"])
    with open(input_json, 'r', encoding='utf-8') as json_file:
        json_data = json.load(json_file)
        with open(output_csv, 'a', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            for idx, filename in enumerate(files):
                title, url, license = search_json(json_data, filename)
                if title == None:
                    title = ""
                if url == None:
                    url = ""
                if license == None:
                    license = ""
                if check_license(license):
                    csv_writer.writerow([filename, title, url, license])
                else:
                    print(f"\r{filename} has unallowed license: {license}. DELETING")
                    os.remove(os.path.join(input_folder, filename))
                    deleted_files += 1
                print(f"\rProcessed {idx + 1}/{num_files} files | {deleted_files} deleted", end="")


if __name__ == "__main__":
    input_folder = "../extractor/parsed"
    input_json = "../scraper/termedia/output.json"
    output_csv = "output.csv"
    generate_csv(input_folder, input_json, output_csv)
