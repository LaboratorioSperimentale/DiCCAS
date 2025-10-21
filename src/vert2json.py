from pathlib import Path
import json
import sys
import collections
import copy
import regex as re

calamities = set()
places = set()
calamities_map = collections.defaultdict(set)
places_map = collections.defaultdict(set)

calamities_paragraphs = collections.defaultdict(set)
places_paragraphs = collections.defaultdict(set)

paragraphs = []

SRC = sys.argv[1]
OUT_JSONL = Path("data/DiCCAS_paragraphs.json")
OUT_JSON = Path("data/DiCCAS_tags.json")

p_id = 0
new_paragraph = {  # book, [sura, section], chapter, subchapter, subsubchapter
		"id": p_id,
		"titles": {
			"book": "",
			"section": "",
			"chapter": "",
			"subchaper": "",
			"subsubchapter": ""
		},
		"pages": [],
		"translation": "",
		"text": [],
		"occurrences": collections.defaultdict(list)
}

with open(SRC, "r", encoding="utf-8") as f:
	for raw in f:
		if raw.startswith("<book"):
			m = re.search(r'\btitle\s*=\s*([\'"])(.*?)\1', raw)
			title = m.group(2) if m else None
			new_paragraph["titles"]["book"] = title
		elif raw.startswith("<sura") or raw.startswith("<section"):
			m = re.search(r'\btitle\s*=\s*([\'"])(.*?)\1', raw)
			title = m.group(2) if m else None
			new_paragraph["titles"]["section"] = title
		elif raw.startswith("<chapter"):
			m = re.search(r'\btitle\s*=\s*([\'"])(.*?)\1', raw)
			title = m.group(2) if m else None
			new_paragraph["titles"]["chapter"] = title
		elif raw.startswith("<subchapter"):
			m = re.search(r'\btitle\s*=\s*([\'"])(.*?)\1', raw)
			title = m.group(2) if m else None
			new_paragraph["titles"]["subchapter"] = title
		elif raw.startswith("<subsubchapter"):
			m = re.search(r'\btitle\s*=\s*([\'"])(.*?)\1', raw)
			title = m.group(2) if m else None
			new_paragraph["titles"]["subsubchapter"] = title

		elif raw.startswith("<p"):
			p_id += 1
			t_id = 0
			new_paragraph["id"] = p_id
			m = re.search(r'\btranslation\s*=\s*([\'"])(.*?)\1', raw)
			translation = m.group(2) if m else None
			new_paragraph["translation"] = translation

			m = re.search(r'\bpages\s*=\s*([\'"])(.*?)\1', raw)
			pages = m.group(2) if m else None
			new_paragraph["pages"] = pages

		elif raw.startswith("</p>"):
			if len(new_paragraph["text"]) > 0:
				# print(new_paragraph)
				# input()
				paragraphs.append(new_paragraph)
				new_paragraph = {
					"id": p_id,
					"titles": copy.deepcopy(new_paragraph["titles"]),
					"pages": [],
					"translation": "",
					"text": [],
					"occurrences": collections.defaultdict(list)
				}
		elif raw.startswith("</"):
			pass
			# print(raw.strip()[2:-1])
		elif raw.startswith("<"):
			pass
		else:
			line = raw.strip().split("\t")
			form, pos, lemma, tag, values, page = line
			new_paragraph["text"].append((form, pos, lemma, tag, values))
			if tag in ["catastrophe", "place"]:
				values = values.split(";")
				for v in values:
					if tag == "catastrophe":
						calamities.add(v)
						if pos in ["noun", "noun_prop", "verb", "adj", "adv"]:
							calamities_map[v].add(lemma)
							calamities_paragraphs[lemma].add(p_id)
							new_paragraph["occurrences"][v].append(t_id)

					if tag == "place":
						places.add(v)
						if pos in ["noun", "noun_prop", "verb", "adj", "adv"]:
							places_map[v].add(lemma)
							places_paragraphs[lemma].add(p_id)
							new_paragraph["occurrences"][v].append(t_id)
			t_id += 1

kwic = {}
for paragraph in paragraphs:
    for tag in paragraph["occurrences"]:
        if not tag in kwic:
            kwic[tag] = {}
        for id in paragraph["occurrences"][tag]:
            # print(id)
            # print(paragraph["text"])
            len_text = len(paragraph["text"])
            preceding_ctx = paragraph["text"][max(0, id-10):id]
            following_ctx = paragraph["text"][id+1:min(len_text-1, id+10)]

            kwic[tag][f"{paragraph['id']}-{id}"] = (preceding_ctx, paragraph["text"][id], following_ctx)

with open("data/json/calamities.json", "w") as fout:
    fout.write(json.dumps(calamities, indent=2, ensure_ascii=False, default=list))

with open("data/json/places.json", "w") as fout:
    fout.write(json.dumps(places, indent=2, ensure_ascii=False, default=list))

with open("data/json/calamities_map.json", "w") as fout:
    fout.write(json.dumps(calamities_map, indent=2, ensure_ascii=False, default=list))

with open("data/json/places_map.json", "w") as fout:
    fout.write(json.dumps(places_map, indent=2, ensure_ascii=False, default=list))

with open("data/json/calamities_paragraphs.json", "w") as fout:
    fout.write(json.dumps(calamities_paragraphs, indent=2, ensure_ascii=False, default=list))

with open("data/json/places_paragraphs.json", "w") as fout:
    fout.write(json.dumps(places_paragraphs, indent=2, ensure_ascii=False,  default=list))

with open("data/json/paragraphs.json", "w") as fout:
    fout.write(json.dumps(paragraphs, ensure_ascii=False, indent=2))

with open("data/json/kwic.json", "w") as fout:
    fout.write(json.dumps(kwic, ensure_ascii=False))