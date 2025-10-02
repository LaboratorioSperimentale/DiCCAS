"""
Parse a .vert corpus into paragraph-level JSON.

Outputs:
  - /mnt/data/DiCCAS_paragraphs.jsonl  # one JSON object per line (paragraph)
  - /mnt/data/DiCCAS_paragraphs.json   # JSON array of paragraph objects

Assumes the source file is at:
  /mnt/data/250917corpus_DiCCAS.vert
"""

from pathlib import Path
import json
import sys
import collections

calamities = set()
places = set()
calamities_map = collections.defaultdict(set)
places_map = collections.defaultdict(set)

paragraphs = []

SRC = sys.argv[1]
OUT_JSONL = Path("data/DiCCAS_paragraphs.json")
OUT_JSON = Path("data/DiCCAS_tags.json")


with open(SRC, "r", encoding="utf-8") as f:
	for raw in f:
		if raw.startswith("<book"):
			curr_book = ""
		elif raw.startswith("<p"):
			new_paragraph = {}
		elif raw.startswith("</"):
			print(raw.strip()[2:-1])
		elif raw.startswith("<"):
			pass
		else:
			line = raw.strip().split("\t")
			# print(line)
			form, pos, lemma, tag, values, page = line

			if tag in ["catastrophe", "place"]:
				values = values.split(";")
				for v in values:
					if tag == "catastrophe":
						calamities.add(v)
						if pos in ["noun", "noun_prop", "verb", "adj", "adv"]:
							calamities_map[v].add(lemma)
					if tag == "place":
						places.add(v)
						if pos in ["noun", "noun_prop", "verb", "adj", "adv"]:
							places_map[v].add(lemma)


# print(calamities)