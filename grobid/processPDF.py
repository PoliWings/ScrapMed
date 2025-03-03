import os
from grobid_client.grobid_client import GrobidClient

input_dir = 'input'
output_dir = 'output'
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

client = GrobidClient(config_path="config.json")

print(f"Processing all PDFs in folder {input_dir} ...")
client.process("processFulltextDocument",
               input_path=input_dir,
               output=output_dir,
               force=False,
               verbose=True
               )
print(f"TEI XML files saved in {output_dir}")
