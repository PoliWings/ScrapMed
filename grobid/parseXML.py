import os
import csv
from lxml import etree


def process_xml_files(input_folder, output_folder, csv_file):
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

    csv_exists = os.path.exists(csv_file)
    with open(csv_file, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        if not csv_exists:
            csv_writer.writerow(["FILENAME", "TITLE", "URL", "LICENSE"])

        for filename in os.listdir(input_folder):
            if filename.lower().endswith(".xml"):
                xml_path = os.path.join(input_folder, filename)
                try:
                    tree = etree.parse(xml_path)
                    root = tree.getroot()

                    title_element = root.xpath('.//tei:titleStmt/tei:title[@level="a" and @type="main"]', namespaces=ns)
                    title_text = title_element[0].text.strip() if title_element and title_element[
                        0].text else "No Title Found"

                    license_element = root.xpath('.//tei:publicationStmt/tei:availability/tei:licence', namespaces=ns)
                    license_text = license_element[0].text.strip() if license_element and license_element[
                        0].text else "No License Information Found"

                    body_divs = root.xpath('.//tei:text/tei:body/tei:div', namespaces=ns)
                    article_content = []

                    for div in body_divs:
                        div_text = ' '.join(div.itertext()).strip()
                        div_text = ' '.join(div_text.split())

                        if div_text:
                            article_content.append(div_text)

                    base_name = os.path.splitext(filename)[0]
                    base_name = base_name.split(".")[0]
                    txt_file_path = os.path.join(output_folder, base_name + ".txt")
                    with open(txt_file_path, 'w', encoding='utf-8') as txtfile:
                        txtfile.write("\n\n".join(article_content))

                    csv_writer.writerow([base_name, title_text, "", license_text])
                    print(f"Processed {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")


if __name__ == "__main__":
    input_folder = "output"
    output_folder = "parsed"
    os.makedirs(output_folder, exist_ok=True)
    csv_file = os.path.join(output_folder, "results.csv")
    process_xml_files(input_folder, output_folder, csv_file)
    print("Processing completed.")
