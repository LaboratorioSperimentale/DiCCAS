# DiCCAS

## Description:
The corpus contains overall extracts from 10 books, for a total of 889 paragraphs and 289,035 tokens. The original TEI XML files were processed to create verticalized VRT files, which include Part of Speech tags for each token. The pipeline consists of two main steps: first, the TEI XML is converted into an intermediate VRT format; then, this VRT file is further processed to add POS tags and produce the final VRT file.

The tools used to annotate the corpus linguistically are part of the [Camel Tools suite](https://github.com/CAMeL-Lab/camel_tools), specifically [v1.5.7](https://github.com/CAMeL-Lab/camel_tools/tree/v1.5.7)

## Pipeline:

1. Create virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Create intermediate VRT file from TEI XML:

```bash
python src/read_tei.py --input_file data/input/DiCCAS_tei.xml --output_file data/output/DiCCAS.txt
```

3. Create final VRT file with POS tags:

```bash
python src/tab2vert.py --input_file data/output/DiCCAS.txt --output_file data/output/DiCCAS_final.vert
```

## Tagsets

As far as Part of Speech tags are concerned, we rely on camel_tools for the analysis of Arabic text. For more information on the tagset, see the camel_tools documentation: https://camel-tools.readthedocs.io/
These are converted to one-letter tags in the final VRT file, following the mapping provided in the `pos_map.py` dictionary in `src/`.


-----

Everything is released under CC-BY-NC-SA 4.0.