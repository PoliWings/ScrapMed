import os

from grobid_client.grobid_client import GrobidClient

input_dir = "input"
output_dir = "output"
os.makedirs(input_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

client = GrobidClient(config_path="config.json")

print(f"Removing leftover files in folder {output_dir} ...")
for file in os.listdir(output_dir):
    if file.endswith(".txt"):
        os.remove(os.path.join(output_dir, file))

print(f"Add .pdf extension to all files in folder {input_dir} ...")
for file in os.listdir(input_dir):
    if not (file.endswith(".pdf") or file.endswith(".json")):
        os.rename(os.path.join(input_dir, file), os.path.join(input_dir, file + ".pdf"))

print(f"Processing all PDFs in folder {input_dir} ...")
client.process("processFulltextDocument",
               input_path=input_dir,
               output=output_dir,
               force=False,
               verbose=True
               )
print(f"TEI XML files saved in {output_dir}")

print(f"List of files not processed:")
for file in os.listdir(output_dir):
    if file.endswith(".txt"):
        bad_file = file.split("_")[0] + ".pdf"
        os.makedirs("corrupted", exist_ok=True)
        os.rename(os.path.join(input_dir, bad_file), os.path.join("corrupted", bad_file))
        os.rename(os.path.join(output_dir, file), os.path.join("corrupted", file))
        print(bad_file)
