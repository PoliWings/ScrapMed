import os
import csv
import shutil
import sys
import re
import concurrent.futures
from lxml import etree
from langdetect import detect_langs, DetectorFactory
import threading

DetectorFactory.seed = 0


def process_divs(element, ns, stop_event):
    text_content = ""
    for div in element.xpath('.//tei:div', namespaces=ns):
        div_text = " ".join(div.itertext()).strip()
        if div_text:
            sentences = re.split(r'(?<=[.!?"])\s', div_text)
            for sentence in sentences:
                try:
                    if re.search(r'\b[a-zA-Zą-żĄ-Ż]\w*\b', sentence):
                        langs = detect_langs(sentence)
                        # print(f"Detected langs: {langs} for sentence: {sentence}")
                        if langs and langs[0].lang == 'pl' and langs[0].prob >= 0.9:
                            text_content += sentence.strip() + " "
                except Exception as e:
                    print(f"Language detection failed for sentence: {e}")
            text_content += "\n"

    if text_content:
        return text_content
    return ""


def process_file(filename, input_folder, output_folder, ns, stop_event):
    xml_path = os.path.join(input_folder, filename)
    try:
        tree = etree.parse(xml_path)
        root = tree.getroot()

        title_element = root.xpath('.//tei:titleStmt/tei:title[@level="a" and @type="main"]', namespaces=ns)
        title_text = title_element[0].text.strip() if title_element and title_element[0].text else "No Title Found"

        license_element = root.xpath('.//tei:publicationStmt/tei:availability/tei:licence', namespaces=ns)
        license_text = license_element[0].text.strip() if license_element and license_element[
            0].text else "No License Information Found"

        abstract_element = root.xpath('.//tei:teiHeader/tei:profileDesc/tei:abstract', namespaces=ns)
        abstract_text = ""
        if abstract_element:
            abstract_text = process_divs(abstract_element[0], ns, stop_event)

        article_content = []

        if abstract_text:
            article_content.append(abstract_text)

        body = root.xpath('.//tei:text/tei:body', namespaces=ns)
        if body:
            body_text = process_divs(body[0], ns, stop_event)
            if body_text:
                article_content.append(body_text)

        if stop_event.is_set():
            return

        if article_content and any(content.strip() for content in article_content):
            base_name = os.path.splitext(filename)[0].split(".")[0]
            txt_file_path = os.path.join(output_folder, base_name + ".txt")
            with open(txt_file_path, 'w', encoding='utf-8') as txtfile:
                txtfile.write("\n".join(article_content))
            print(f"Processed {filename}")
            return (base_name, title_text, license_text)
        else:
            print(f"Skipped {filename} because no valid Polish text was found.")
            return None
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return None


def process_xml_files(input_folder, output_folder, csv_file):
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    os.makedirs(output_folder, exist_ok=True)
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(".xml")]

    stop_event = threading.Event()

    results = []
    detect_langs("Initialize langdetect...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        futures = [executor.submit(process_file, filename, input_folder, output_folder, ns, stop_event) for filename in
                   files]

        try:
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is not None:
                    results.append(result)
        except KeyboardInterrupt:
            print("Stopping processing...")
            stop_event.set()
            for future in futures:
                future.cancel()

    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['filename', 'title', 'url', 'license'])

    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        for base_name, title_text, license_text in results:
            csv_writer.writerow([base_name, title_text, "", license_text])

    print("Processing completed.")


if __name__ == "__main__":
    input_folder = "../grobid/output"
    output_folder = "parsed"
    if "-f" in sys.argv:
        if os.path.exists(output_folder):
            print(f"Removing existing folder: {output_folder}")
            shutil.rmtree(output_folder)
    csv_file = os.path.join(output_folder, "metadata.csv")
    process_xml_files(input_folder, output_folder, csv_file)
