# DiCCAS

## Pipeline:

1. Create virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Create intermediate VRT file from TEI XML:

```bash
python src/read_tei_new.py --input_file data/260126corpus_DiCCAS_final.xml --output_file data/DiCCAS.vrt
```