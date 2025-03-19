# CSV generator

## How to run

1. Have `../extractor/parsed` folder with `.txt` files (created by extractor script)
2. Have `../scraper/termedia/output.json` file (created by scraper script)
3. Run the following command to process the files:
    ```bash
    python generateCSV.py
    ```
    Use the `-x` flag to copy .xml files corresponding to the rows added to csv file. They will be copied from grobid output (`../grobid/output`) to `xml` folder. Useful for debug purposes.
4. Result file will be saved as `output.csv`