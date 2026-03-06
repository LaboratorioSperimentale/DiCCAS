import re
import unicodedata as ud
from lxml import etree
from lxml.etree import _Element

from camel_tools.utils.normalize import normalize_unicode
from camel_tools.utils.dediac import dediac_ar
from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.disambig.mle import MLEDisambiguator
from camel_tools.tagger.default import DefaultTagger


mle = MLEDisambiguator.pretrained()
tagger = DefaultTagger(mle, 'pos')


ARABIC_LETTERS = r"[\u0600-\u06FF]+"
DIACRITICS = re.compile(r"[\u064B-\u0652\u06D6]")
OTHER_DIACRITICS = re.compile(r"[\u0616\u06D6\u06D7\u0615\u0617\u06D8\u06D9\u06DA\u06DB\u06DC\u06DF\u06E0\u06E1\u06E2\u06E4\u06E7\u06E8\u0898\u08CA\u08CB\u08CC\u08CD\u08D4\u08D5\u08D6\u08D7\u08D8\u08DA\u08DB\u08DC\u08DD\u08DE\u08DF\u08E0\u08E1\u08F3\u0674\u0675\u0676\u0678\u06EB\u06EC\u0656\u0670\u06e6]")
SENTENCE_SPLIT_REGEX = re.compile(r"(?<=[.؟!])\s+")
QUOTE_SET = "\"'‘’“”«»‹›„‟‚‛＂＇`´ˈʹˋˮ"

ARABIC_SMALL_LETTERS = {'\u06E5', '\u06E6'}  # SMALL WAW, SMALL YEH
ARABIC_QURANIC_SIGNS = {
	'\u06DD',  # END OF AYAH (Cf)
	'\u06DE',  # START OF RUB EL HIZB (So)
	'\u06E9',  # PLACE OF SAJDAH (So)
	'\u08E2',  # DISPUTED END OF AYAH (Cf)
}

def strip_arabic_diacritics(text, *,
							remove_tatweel=True,
							remove_supersubs=True,
							remove_small_letters=True,
							remove_quranic_signs=True):
	"""Removes Arabic diacritics and optionally other marks from the input text.
	By default, it removes:
	- Harakat (Fatha, Damma, Kasra, etc.)
	- Tatweel (kashida)
	- Superscript and subscript characters
	- Arabic "small letters" (like SMALL WAW and SMALL YEH)
	- Common Qur'anic signs that aren't categorized as Mn (like END OF AYAH)
	"""
	# Decompose so base letters + marks separate
	t = ud.normalize('NFD', text)
	out = []
	for ch in t:
		cat = ud.category(ch)

		# All combining/enclosing marks (harakat, small signs, superscript alef, Arabic Extended-A marks)
		if cat in ('Mn', 'Me'):
			continue

		# Tatweel (kashida)
		if remove_tatweel and ch == '\u0640':
			continue

		# Superscripts/Subscripts block
		if remove_supersubs and '\u2070' <= ch <= '\u209F':
			continue

		# Arabic "small letters" (Lm) like ۥ ۦ
		if remove_small_letters and ch in ARABIC_SMALL_LETTERS:
			continue

		# Common Qur'anic signs that aren't Mn (So/Cf)
		if remove_quranic_signs and ch in ARABIC_QURANIC_SIGNS:
			continue

		name = ud.name(ch, '')
		if name.startswith('ARABIC SMALL '):
			continue
		out.append(ch)

	return ud.normalize('NFC', ''.join(out))

# file_output_prova = open("data/prova.txt", "w", encoding="utf-8")

# Keep track of used structure tags for .vrt.struct
div_tags_used = set()

def handle_divs(parent,
				vrt_lines,
				ns, sentence_id, context):
	"""
	Recursively processes nested <div> elements in the TEI XML,
	extracting relevant information and writing to VRT lines.
	"""

	for child in parent:

		if not isinstance(child.tag, str):
			continue  # skip comments, processing instructions, etc.

		tag = etree.QName(child.tag).localname

		if tag.startswith("div"):

			div_type = child.get("type", tag)
			div_num = child.get("n", "-")

			div_title = get_head_text(child, ns)
			div_tags_used.add(div_type)

			vrt_lines.append(f'@{div_type.upper()}@\tn="{div_num}"\t{div_type}_title="{div_title}"')
			new_context = context.copy()
			new_context[div_type] = (div_num, div_title)
			sentence_id = handle_divs(child, vrt_lines, ns, sentence_id, new_context)

		elif tag == "p":
			sentence_id = write_paragraph(child, vrt_lines, ns, sentence_id)

	return sentence_id


def get_head_text(div, ns):
	"""
	Extracts and cleans the text from the <head> element of a TEI <div>.
	If no <head> or <title> is found, returns "_".
	"""
	head = div.find("tei:head", namespaces=ns)
	if head is not None:
		title = head.find("tei:title", namespaces=ns)
		if title is not None and title.text:
			ret = title.text.strip()
			return clean_translation(ret)
	return "_"


def clean_translation(text):
	"""
	Cleans translation text by normalizing whitespace and replacing double quotes with single quotes.
	"""
	ret = re.sub(r"\s+", " ", text).strip()
	ret = re.sub(r'"', "'", ret)
	return ret


def walk_node(node,
			current_role="_", current_term_type="_", current_term_subtype = "_",
			current_term_translation=["_"], ns=None):
	"""
	Recursively walks an XML node, extracting tokens and their annotations.
	Handles page breaks, glosses, terms, and place names, and applies morphological analysis
	to the text content. Returns a list of token tuples with their annotations.
	"""
	page_numbers = []
	tokens = []
	if not isinstance(node, _Element):
		return tokens

	tag = node.tag if isinstance(node.tag, str) else ""

	if tag.endswith("pb"):
		page_number = node.get("n", "_")
		page_numbers.append(page_number)
		tokens.append(("[PAGEBREAK]", page_number, '_', '_', '_', '_', '_'))

	if tag.endswith("gloss"):
		return tokens

	if tag.endswith("term"):
		current_term_type = node.get("type", "_")
		current_term_subtype = node.get("subtype", "_")
		current_term_translation = [x.strip() for x in node.get("translation", "_").split(',')]

	if tag.endswith("placename"):
		current_term_type = 'place'
		current_term_translation = [x.strip() for x in node.get("translation", "_").split(',')]

	if node.text:
		# print(node.text, file=file_output_prova)
		# print(strip_arabic_diacritics(re.sub(r"\s+", ' ', node.text)), file=file_output_prova)
		text_stripped = strip_arabic_diacritics(re.sub(r"\s+", ' ', node.text))
		text = dediac_ar(normalize_unicode(text_stripped))
		text = simple_word_tokenize(text)
		disambig = mle.disambiguate(text)
		if len(disambig):
			diacritized = [d.analyses[0].analysis['diac'] for d in disambig]
			pos_tags = [d.analyses[0].analysis['pos'] for d in disambig]
			lemmas = [d.analyses[0].analysis['lex'] for d in disambig]
			for triplet in zip(diacritized, pos_tags, lemmas):
				word, pos, lemma = triplet
				tokens.append((word, pos, lemma,
						current_role, current_term_type,
				  		current_term_subtype,
						current_term_translation))

	for child in node:
		tokens.extend(walk_node(child, current_role, current_term_type, current_term_subtype, current_term_translation, ns))
		if child.tail:
			# print(child.tail, file=file_output_prova)
			# print(strip_arabic_diacritics(re.sub(r"\s+", ' ', child.tail)), file=file_output_prova)

			text_stripped = strip_arabic_diacritics(re.sub(r"\s+", ' ', child.tail))
			text = dediac_ar(normalize_unicode(text_stripped))
			text = simple_word_tokenize(text)
			disambig = mle.disambiguate(text)
			if len(disambig):
				diacritized = [d.analyses[0].analysis['diac'] for d in disambig]
				pos_tags = [d.analyses[0].analysis['pos'] for d in disambig]
				lemmas = [d.analyses[0].analysis['lex'] for d in disambig]
				for triplet in zip(diacritized, pos_tags, lemmas):
					word, pos, lemma = triplet
					tokens.append((word, pos, lemma, current_role, current_term_type, current_term_subtype, current_term_translation))

	return tokens

def write_paragraph(p, vrt_lines, ns, sentence_id):
	"""
	Processes a <p> element, extracting tokens and their annotations,
	and appending them to the VRT lines. Also handles page breaks and paragraph-level metadata
	"""

	pos_map = {
		"abbrev": "b",
		"adj": "a",
		"adv": "r",
		"adv_interrog": "i",
		"adv_rel": "s",
		"conj": "c",
		"conj_sub": "k",
		"digit": "0",
		"foreign": "2",
		"interj": "1",
		"noun": "n",
		"noun_prop": "o",
		"noun_quant": "q",
		"part": "h",
		"part_det": "d",
		"part_focus": "z",
		"part_fut": "u",
		"part_interrog": "j",
		"part_neg": "e",
		"part_verb": "l",
		"part_voc": "m",
		"prep": "p",
		"pron": "f",
		"pron_dem": "t",
		"pron_interrog": "y",
		"pron_rel": "g",
		"punc": "x",
		"verb": "v",
		"verb_pseudo": "w"
	}

	glosses = p.xpath(".//tei:gloss/text()", namespaces=ns)
	translation_attr = clean_translation(glosses[0]) if glosses else "_"
	p_id = p.get("id", "-")
	p_n = p.get("n", "-")
	p_copy = etree.fromstring(etree.tostring(p), parser=etree.XMLParser(recover=True))

	for hi in p_copy.xpath(".//tei:hi", namespaces=ns):
		hi.tag = "span"

	token_tuples = walk_node(p_copy, ns=ns)

	sentences = []
	current_sentence = []

	for tok in token_tuples:
		current_sentence.append(tok)
	if current_sentence:
		sentences.append(current_sentence)

	pos_paragraph = len(vrt_lines)
	paragraph_pages = []
	vrt_lines.append(f'@P@\tn="{p_n}"\tid="{p_id}"\ttranslation="{translation_attr}"')

	last_seen_page = "_"
	for sentence in sentences:
		sent_pages = [pos for (token, pos, lemma, role, term_type, term_subtype, term_translation) in sentence if token == "[PAGEBREAK]"]
		paragraph_pages.extend(sent_pages)

		for idx, (token, pos, lemma, role, term_type, term_subtype, term_translation) in enumerate(sentence):
			if token == "[PAGEBREAK]" and not pos == "_":
				last_seen_page = int(pos)
			else:
				ded_token = dediac_ar(token)
				if term_subtype != "_":
					term_type = term_type+":"+term_subtype
				vrt_lines.append('\t'.join([ded_token, pos, lemma, term_type, ';'.join(term_translation), f"{ded_token}-{pos_map[pos]}", f"{lemma}-{pos_map[pos]}"]))
		sentence_id += 1

	if len(paragraph_pages):
		vrt_lines[pos_paragraph] += f'\tpages="{",".join(paragraph_pages)}"'
	return sentence_id


def write_vrt_idx(idx_file):
	with open(idx_file, "w", encoding="utf-8") as f:
		f.write("word\n")
		f.write("role\n")
		f.write("term_type\n")
		f.write("term_translation\n")


def write_vrt_struct(struct_file):
	"""
	Writes the .vrt.struct file based on the div tags used in the TEI XML.
	For <p> tags, it includes the 'translation' attribute.
	For other div types, it includes 'n' and 'title' attributes.
	"""
	with open(struct_file, "w", encoding="utf-8") as f:
		for tag in sorted(div_tags_used):
			if tag == "p":
				f.write(f"{tag}\tattributes:translation\n")
			else:
				f.write(f"{tag}\tattributes:n,title\n")


def tei_to_vrt(input_file, output_file):
	"""Main function to convert TEI XML to VRT format.
	Parses the XML, processes the structure, and writes the output.
	"""

	parser = etree.XMLParser(recover=True)
	tree = etree.parse(input_file, parser=parser)
	root = tree.getroot()
	ns = {"tei": "http://www.tei-c.org/ns/1.0"}

	vrt_lines = []

	sentence_id = 1

	print("1.  ###########", "Processing books...")

	for book_div in root.xpath(".//tei:div[@type='book']", namespaces=ns):
		book_num = book_div.get("n", "-")
		book_type = book_div.get("ana", "-")
		book_title = get_head_text(book_div, ns)

		vrt_lines.append(f'@BOOK@\tn="{book_num}"\tbook_title="{book_title}"\tbook_type="{book_type}"')

		sentence_id = handle_divs(book_div, vrt_lines,
								ns, sentence_id,
								{"book": (book_num, book_title, book_type)})

	print("2.  ###########", "Finished processing. Writing output...")
	with open(output_file, "w", encoding="utf-8") as out:
		out.write("\n".join(vrt_lines))

	write_vrt_idx("data/corpus_DiCCAS.vrt.idx")


if __name__ == "__main__":
	import argparse
	parser = argparse.ArgumentParser(description="Convert TEI XML to VRT format")
	parser.add_argument("--input_file", help="Path to input TEI XML file")
	parser.add_argument("--output_file", help="Path to output VRT file")
	args = parser.parse_args()

	tei_to_vrt(args.input_file, args.output_file)