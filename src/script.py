from lxml import etree
import re

ARABIC_LETTERS = r"[\u0600-\u06FF]+"
DIACRITICS = re.compile(r"[\u064B-\u0652]")


def tei_to_vrt(input_file, output_file):
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(input_file, parser=parser)
    root = tree.getroot()
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    with open(output_file, "w", encoding="utf-8") as out:
        for book_div in root.xpath(".//tei:div[@type='book']", namespaces=ns):
            book_num = book_div.get("n", "_")
            out.write(f'<book n="{book_num}">\n')
            div1_list = book_div.xpath(".//tei:div1", namespaces=ns)
            if div1_list:
                for div1 in div1_list:
                    div1_type = div1.get("type", "div1")
                    div1_num = div1.get("n", "_")
                    out.write(f'<{div1_type} n="{div1_num}">\n')
                    handle_div2(div1, out, ns)
                    out.write(f'</{div1_type}>\n')
            else:
                write_paragraphs(out, book_div, ns)
            out.write(f'</book>\n')


def handle_div2(parent_div, out, ns):
    div2_list = parent_div.xpath(".//tei:div2", namespaces=ns)
    if div2_list:
        for div2 in div2_list:
            div2_type = div2.get("type", "div2")
            div2_num = div2.get("n", "_")
            out.write(f'<{div2_type} n="{div2_num}">\n')
            handle_div3(div2, out, ns)
            out.write(f'</{div2_type}>\n')
    else:
        write_paragraphs(out, parent_div, ns)


def handle_div3(parent_div, out, ns):
    div3_list = parent_div.xpath(".//tei:div3", namespaces=ns)
    if div3_list:
        for div3 in div3_list:
            div3_type = div3.get("type", "div3")
            div3_num = div3.get("n", "_")
            out.write(f'<{div3_type} n="{div3_num}">\n')
            handle_div4(div3, out, ns)
            out.write(f'</{div3_type}>\n')
    else:
        write_paragraphs(out, parent_div, ns)


def handle_div4(parent_div, out, ns):
    div4_list = parent_div.xpath(".//tei:div4", namespaces=ns)
    if div4_list:
        for div4 in div4_list:
            div4_type = div4.get("type", "div4")
            div4_num = div4.get("n", "_")
            out.write(f'<{div4_type} n="{div4_num}">\n')
            write_paragraphs(out, div4, ns)
            out.write(f'</{div4_type}>\n')
    else:
        write_paragraphs(out, parent_div, ns)


def clean_translation(text):
    return re.sub(r"\s+", " ", text).strip()


def write_paragraphs(out, div, ns):
    for p in div.xpath(".//tei:p", namespaces=ns):
        glosses = p.xpath(".//tei:gloss/text()", namespaces=ns)
        translation_attr = clean_translation(glosses[0]) if glosses else "_"
        p_copy = etree.fromstring(etree.tostring(p), parser=etree.XMLParser(recover=True))
        for gloss in p_copy.xpath(".//tei:gloss", namespaces=ns):
            gloss.getparent().remove(gloss)
        text_nodes = list(p_copy.iter())
        if not text_nodes:
            continue
        out.write(f'<p translation="{translation_attr}">\n')
        out.write(process_tokens_list(text_nodes, ns))
        out.write("</p>\n")


def process_tokens_list(nodes, ns):
    tokens_output = []
    for node in nodes:
        if isinstance(node, etree._Element):
            if node.tag == f"{{{ns['tei']}}}term":
                term_text = "".join(node.xpath(".//text()", namespaces=ns)).strip()
                term_type = node.get("type", "_")
                term_translation = node.get("translation", "_")
                for token in arabic_tokenize(term_text):
                    tokens_output.append(f"{token}\t{term_type}\t{term_translation}")
            else:
                if node.text and node.tag != f"{{{ns['tei']}}}gloss":
                    for token in arabic_tokenize(node.text):
                        tokens_output.append(f"{token}\t_\t_")
        else:
            text_str = str(node).strip()
            if text_str:
                for token in arabic_tokenize(text_str):
                    tokens_output.append(f"{token}\t_\t_")
        if isinstance(node, etree._Element) and node.tail:
            for token in arabic_tokenize(node.tail):
                tokens_output.append(f"{token}\t_\t_")
    return "\n".join(tokens_output) + "\n"


def arabic_tokenize(text):
    text = DIACRITICS.sub('', text)
    text = re.sub(r'([.,!?؛،:"«»()\[\]{}])', r' \1 ', text)
    text = re.sub(r'\b([وفبكل])(?=' + ARABIC_LETTERS + ')', r'\1 ', text)
    text = re.sub(r'\b(ال)(?=' + ARABIC_LETTERS + ')', r'\1 ', text)
    return text.split()


# Example usage
tei_to_vrt("corpus_DiCCAS.xml", "corpus_DiCCAS.vrt")
