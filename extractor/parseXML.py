import os
import shutil
import sys
import re
import concurrent.futures
from lxml import etree
from langdetect import detect_langs, DetectorFactory
import threading

DetectorFactory.seed = 0

MIN_CONTENT_LENGTH = 500
EXCLUDED_PHRASE = "wszelkie prawa zastrzeżone"
MAX_SPACE_RATIO = 0.18
MAX_SPACE_HEAD_RATIO = 0.25

def check_space_ratio(text, ratio):
    spaces = text.count(' ')
    chars = len(text) + 1 
    spaces_ratio = spaces / chars     
    if spaces_ratio > ratio:
        return True
    return False


def replace_characters(text):
    # windows-1252 to windows-1250
    text = (text.replace("¹", "ą")
            .replace("ae", "ć")
            .replace("ê", "ę")
            .replace("³", "ł")
            .replace("ñ", "ń")
            # .replace("ó", "ó")
            .replace("oe", "ś")
            .replace("Ÿ", "ź")
            .replace("¿", "ż")
            .replace("¥", "Ą")
            .replace("AE", "Ć")
            .replace("Ê", "Ę")
            .replace("£", "Ł")
            .replace("Ñ", "Ń")
            # .replace("Ó", "Ó")
            .replace("OE", "Ś")
            # .replace("", "Ź")
            .replace("¯", "Ż"))
    return text


def process_divs(element, ns, stop_event):
    text_content = ""
    for div in element.xpath('.//tei:div', namespaces=ns):
        for head in element.xpath('.//tei:head', namespaces=ns):
            head_text = " ".join(head.itertext()).strip()
            
            if head_text:   
                if check_space_ratio(head_text, MAX_SPACE_HEAD_RATIO):
                    print(f"Skipped head because of high spaces ratio.")
                    head.getparent().remove(head)
                    continue

        for ref in div.xpath('.//tei:ref', namespaces=ns):
            ref.getparent().remove(ref)
        div_text = " ".join(div.itertext()).strip()
        if div_text:
            if check_space_ratio(div_text, MAX_SPACE_RATIO):
                print(f"Skipped div because of high spaces ratio.")
                continue
            sentences = re.split(r'(?<=[.!?"])\s', div_text)
            for sentence in sentences:
                try:
                    if re.search(r'\b[a-zA-Zą-żĄ-Ż]\w*\b', sentence):
                        langs = detect_langs(sentence)
                        if langs and langs[0].lang == 'pl' and langs[0].prob >= 0.9:
                            text_content += sentence.strip() + " "
                except Exception as e:
                    print(f"Language detection failed for sentence: {e}")
            if text_content:
                text_content += "\n"

    return replace_characters(text_content.strip())


def process_file(filename, input_folder, output_folder, ns, stop_event):
    xml_path = os.path.join(input_folder, filename)
    try:
        tree = etree.parse(xml_path)
        root = tree.getroot()

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

        full_text = "\n".join(article_content).strip()
        if len(full_text) < MIN_CONTENT_LENGTH:
            print(f"Skipped {filename} because content is too short.")
            return None

        if EXCLUDED_PHRASE in full_text.lower():
            print(f"Skipped {filename} because it contains restricted rights notice.")
            return None

        if full_text:
            base_name = os.path.splitext(filename)[0].split(".")[0]
            txt_file_path = os.path.join(output_folder, base_name + ".txt")
            with open(txt_file_path, 'w', encoding='utf-8') as txtfile:
                txtfile.write("\n".join(article_content))
            print(f"Processed {filename}")
        else:
            print(f"Skipped {filename} because no valid Polish text was found.")
            return None
    except Exception as e:
        print(f"Error processing {filename}: {e}")
        return None


def process_xml_files(input_folder, output_folder):
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    os.makedirs(output_folder, exist_ok=True)
    files = [f for f in os.listdir(input_folder) if f.lower().endswith(".xml")]

    stop_event = threading.Event()

    detect_langs("Initialize langdetect...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
        futures = [executor.submit(process_file, filename, input_folder, output_folder, ns, stop_event) for filename in
                   files]

        try:
            for future in concurrent.futures.as_completed(futures):
                future.result()
        except KeyboardInterrupt:
            print("Stopping processing...")
            stop_event.set()
            for future in futures:
                future.cancel()

    print("Processing completed.")


if __name__ == "__main__":
    input_folder = "../grobid/output"
    output_folder = "parsed"
    if "-f" in sys.argv:
        if os.path.exists(output_folder):
            print(f"Removing existing folder: {output_folder}")
            shutil.rmtree(output_folder)
    process_xml_files(input_folder, output_folder)
