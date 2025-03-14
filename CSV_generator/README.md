# CSV generator

## How to run

1. Have `../extractor/parsed` folder with `.txt` files (created by extractor script)
2. Have `../scraper/termedia/output.json` file (created by scraper script)
3. Run the following command to process the files:
    ```bash
    python generateCSV.py
    ```
4. Result file will be saved as `output.csv`