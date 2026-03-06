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
python src/read_tei.py --input_file data/input/DiCCAS.xml --output_file data/output/DiCCAS.vrt
```

3. Create final VRT file with POS tags:

```bash
python src/tab2vert.py --input_file data/output/DiCCAS.vrt --output_file data/output/DiCCAS_final.vrt
```

## Tagsets

As far as Part of Speech tags are concerned, we rely on camel_tools for the analysis of Arabic text. For more information on the tagset, see the camel_tools documentation: https://camel-tools.readthedocs.io/
These are converted to one-letter tags in the final VRT file, following the mapping provided in the `pos_map.py` dictionary in `src/`.


-----

Everything is released under CC-BY-NC-SA 4.0.