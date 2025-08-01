from lxml import etree
import re
import os
from lxml.etree import _Element

ARABIC_LETTERS = r"[\u0600-\u06FF]+"
DIACRITICS = re.compile(r"[\u064B-\u0652]")
SENTENCE_SPLIT_REGEX = re.compile(r"(?<=[.؟!])\s+")

# Keep track of used structure tags for .vrt.struct
div_tags_used = set()

def tei_to_vrt(input_file, output_file):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(input_file, parser=parser)
    root = tree.getroot()
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    vrt_lines = []
    conllu_lines = []

    sentence_id = 1

    for book_div in root.xpath(".//tei:div[@type='book']", namespaces=ns):
        book_num = book_div.get("n", "_")
        book_title = get_head_text(book_div, ns)
        vrt_lines.append(f'<book n="{book_num}" title="{book_title}">')
        div_tags_used.add("book")
        sentence_id = handle_divs(book_div, vrt_lines, conllu_lines, ns, sentence_id, {"book": (book_num, book_title)})
        vrt_lines.append(f'</book>\n')

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("\n".join(vrt_lines))

    with open("corpus_DiCCAS.conllu", "w", encoding="utf-8") as f:
        f.write("\n".join(conllu_lines))

    write_vrt_idx("corpus_DiCCAS.vrt.idx")
    write_vrt_struct("corpus_DiCCAS.vrt.struct")

def handle_divs(parent, vrt_lines, conllu_lines, ns, sentence_id, context):
    for child in parent:
        if not isinstance(child.tag, str):
            continue  # skip comments, processing instructions, etc.
        tag = etree.QName(child.tag).localname
        if tag.startswith("div"):
            div_type = child.get("type", tag)
            div_num = child.get("n", "_")
            div_title = get_head_text(child, ns)
            div_tags_used.add(div_type)
            vrt_lines.append(f'<{div_type} n="{div_num}" title="{div_title}">')
            new_context = context.copy()
            new_context[div_type] = (div_num, div_title)
            sentence_id = handle_divs(child, vrt_lines, conllu_lines, ns, sentence_id, new_context)
            vrt_lines.append(f'</{div_type}>\n')
        elif tag == "p":
            sentence_id = write_paragraph(child, vrt_lines, conllu_lines, ns, sentence_id, context)
    return sentence_id

def get_head_text(div, ns):
    head = div.find("tei:head", namespaces=ns)
    if head is not None:
        title = head.find("tei:title", namespaces=ns)
        if title is not None and title.text:
            ret = title.text.strip().replace('"', "'")
            return clean_translation(ret)
    return "_"

def clean_translation(text):
    return re.sub(r"\s+", " ", text).strip()

def walk_node(node, current_role="_", current_term_type="_", current_term_translation="_", ns=None):
    tokens = []
    if not isinstance(node, _Element):
        return tokens

    tag = node.tag if isinstance(node.tag, str) else ""

    if tag.endswith("gloss"):
        return tokens

    if tag.endswith("term"):
        current_term_type = node.get("type", "_")
        current_term_translation = node.get("translation", current_term_translation)

    if tag.endswith("persName"):
        local_role = node.get("role", current_role)
        if node.text:
            for word in arabic_tokenize(node.text):
                tokens.append((word, local_role, current_term_type, current_term_translation))
        for child in node:
            tokens.extend(walk_node(child, local_role, current_term_type, current_term_translation, ns))
            if child.tail:
                for word in arabic_tokenize(child.tail):
                    tokens.append((word, current_role, current_term_type, current_term_translation))
        return tokens

    if node.text:
        for word in arabic_tokenize(node.text):
            tokens.append((word, current_role, current_term_type, current_term_translation))

    for child in node:
        tokens.extend(walk_node(child, current_role, current_term_type, current_term_translation, ns))
        if child.tail:
            for word in arabic_tokenize(child.tail):
                tokens.append((word, current_role, current_term_type, current_term_translation))

    return tokens

def write_paragraph(p, vrt_lines, conllu_lines, ns, sentence_id, context):
    glosses = p.xpath(".//tei:gloss/text()", namespaces=ns)
    translation_attr = clean_translation(glosses[0]) if glosses else "_"
    p_copy = etree.fromstring(etree.tostring(p), parser=etree.XMLParser(recover=True))

    for hi in p_copy.xpath(".//tei:hi", namespaces=ns):
        hi.tag = "span"

    token_tuples = walk_node(p_copy, ns=ns)

    sentences = []
    current_sentence = []
    for tok in token_tuples:
        current_sentence.append(tok)
        if tok[0] in ['.', '؟', '!']:
            sentences.append(current_sentence)
            current_sentence = []
    if current_sentence:
        sentences.append(current_sentence)

    vrt_lines.append(f'<p translation="{translation_attr}">')
    div_tags_used.add("p")

    for sentence in sentences:
        vrt_lines.append("<s>")
        conllu_lines.append(f"# sent_id = s{sentence_id}")
        conllu_lines.append(f"# translation = {translation_attr}")
        for k, (num, title) in context.items():
            conllu_lines.append(f"# {k} = {num}")
            conllu_lines.append(f"# {k}_title = {title}")
        for idx, (token, role, term_type, term_translation) in enumerate(sentence, 1):
            vrt_lines.append(f"{token}\t{role}\t{term_type}\t{term_translation}")
            misc = []
            if role != "_":
                misc.append(f"Role={role}")
            if term_type != "_":
                misc.append(f"TermType={term_type}")
            if term_translation != "_":
                misc.append(f"TermTranslation={term_translation}")
            misc_str = "|".join(misc) if misc else "_"
            conllu_lines.append(f"{idx}\t{token}\t_\t_\t_\t_\t_\t_\t_\t{misc_str}")
        vrt_lines.append("</s>")
        conllu_lines.append("")
        sentence_id += 1

    vrt_lines.append("</p>")
    return sentence_id

def arabic_tokenize(text):
    text = DIACRITICS.sub('', text)
    text = re.sub(r'([.,!?؛،:\"«»()\[\]{}])', r' \1 ', text)
    text = re.sub(r'\b([وفبكل])(?=' + ARABIC_LETTERS + ')', r'\1 ', text)
    text = re.sub(r'\b(ال)(?=' + ARABIC_LETTERS + ')', r'\1 ', text)
    return text.split()

def write_vrt_idx(idx_file):
    with open(idx_file, "w", encoding="utf-8") as f:
        f.write("word\n")
        f.write("role\n")
        f.write("term_type\n")
        f.write("term_translation\n")

def write_vrt_struct(struct_file):
    with open(struct_file, "w", encoding="utf-8") as f:
        for tag in sorted(div_tags_used):
            if tag == "p":
                f.write(f"{tag}\tattributes:translation\n")
            else:
                f.write(f"{tag}\tattributes:n,title\n")

# Example usage
tei_to_vrt("corpus_DiCCAS.xml", "corpus_DiCCAS.vert")
