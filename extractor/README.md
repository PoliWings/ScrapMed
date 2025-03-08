# Extractor

## How to run

1. Create `../grobid/output` folder with `.grobid.tei.xml` files
2. Run the following commands:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. Run the following command to process the files:
    ```bash
    python parseXML.py
    ```
   Use `-f` flag to force reparse all files
4. Results will be saved in `parsed/` folder