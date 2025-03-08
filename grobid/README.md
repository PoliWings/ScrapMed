# GROBID

```bash
docker compose up -d
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

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