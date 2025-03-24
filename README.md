# ScrapMed

## About
A tool for automated collection and extraction of Polish medical texts from open sources, compliant with selected CC licenses, for language model training.

## Project Structure

- **CSV_generator/** – Contains a CSV file generator with license detection.
- **extractor/** – Responsible for extracting data from Grobid XML files in Polish.
- **grobid/** – Processes PDF files into XML format.
- **scraper/** – Downloads data from the source website.

## Functionality

1. **Scraping** – The scraper module collects medical text data from various open sources.
2. **PDF Processing** – Grobid converts PDF files into structured XML documents.
3. **Data Extraction** – The extractor module processes the XML files, extracting relevant information in Polish.
4. **CSV Generation** – The CSV generator compiles the extracted data into a structured CSV file while detecting the associated licenses.

## Usage

1. Run the scraper to collect raw data.
2. Use Grobid to convert PDFs into XML.
3. Process the XML files using the extractor to obtain structured text.
4. Generate a CSV file with the extracted data and detected licenses using the CSV_generator module.

## License

This project is licensed under the [MIT](LICENSE) License.

## Authors

- **[Damian Jankowski](https://github.com/pingwin02)**
- **[Jan Barczewski](https://github.com/JJayJohnny)**
- **[Maciej Sikora](https://github.com/Trol3k)**
- **[Radosław Gajewski](https://github.com/Hunrax)**
