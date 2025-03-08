# GROBID

## How to run

1. Create `input/` folder with `.pdf` files to process
2. Run the following commands:
    ```bash
    docker compose up -d
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
3. Run the following command to process the `.pdf` files:
    ```bash
    python processPDF.py
    ```
4. Results will be saved in `output/` folder
5. Corrupted or big files will be saved in `corrupted/` folder

### Test if gpu is available

```bash
docker run --rm -it --gpus=all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark
```

- [Full model](https://kermitt2-grobid.hf.space/)
- [Lite model](https://kermitt2-grobid-crf.hf.space/)
- [GROBID docker documentation](https://grobid.readthedocs.io/en/latest/Run-Grobid/)

### Increase wsl2 memory

```bash
wsl --shutdown
```

Open `C:\Users\username\.wslconfig` and add the following:

```bash
[wsl2]
memory=12GB
swap=25GB
```