import sys
import html

def parse_header_line(line: str):
	"""
	Parses a header line like:
	@BOOK@\tn="1"\tbook_title="The Noble Qur'ān"\tbook_type="religious"
	Returns: tag (e.g. 'BOOK'), attrs dict
	"""
	parts = line.strip().split('\t')
	if not parts:
		return None, {}

	tag = parts[0].strip()
	# tag is like "@BOOK@" -> "BOOK"
	if tag.startswith("@") and tag.endswith("@") and len(tag) >= 3:
		tag = tag[1:-1]
	else:
		# Not a recognized header tag
		return None, {}

	attrs = {}
	for piece in parts[1:]:
		piece = piece.strip()
		if not piece or '=' not in piece:
			continue
		key, val = piece.split('=', 1)
		key = key.strip()
		val = val.strip()
		if len(val) >= 2 and val[0] == '"' and val[-1] == '"':
			val = val[1:-1]
		attrs[key] = val

	return tag, attrs

def xml_min_escape(s: str) -> str:
    # Minimal escaping to keep <tag attr="..."> lines parseable.
    # Leaves apostrophes and Unicode untouched.
    return (
        s.replace("&", "&amp;")
         .replace("<", "&lt;")
         .replace(">", "&gt;")
         .replace('"', "&quot;")
    )

def build_attr_string(attrs: dict) -> str:
	"""
	Turn a dict into XML attribute string, escaping values.
	Skips None values.
	"""
	bits = []
	for k, v in attrs.items():
		# print(k, v)
		# input()
		if v is None:
			print("ERROR, empty attr value", k, v)
		# v_esc = html.escape(str(v), quote=True)
		# v_esc = html.escape(str(v), quote=False).replace('"', "&quot;")
		v_esc = xml_min_escape(str(v))
		bits.append(f'{k}="{v_esc}"')
	return " ".join(bits)

def main(in_path: str, out_path: str):
	context = {
		"book_title": None,
		"book_n": None,
		"book_type": None,
		"sura_title": None,
		"sura_n": None,
		"section_title": None,
		"section_n": None,
		"chapter_title": None,
		"chapter_n": None,
		"subchapter_title": None,
		"subchapter_n": None,
		"subsubchapter_title": None,
		"subsubchapter_n": None,
	}

	in_p = False
	in_book = False

	with open(in_path, "r", encoding="utf-8") as fin, \
		 open(out_path, "w", encoding="utf-8") as fout:
		# fout.write('<?xml version="1.0" encoding="UTF-8"?>\n')
		for raw_line in fin:
			line = raw_line.rstrip('\n')

			# Header lines now start with "@"
			if line.startswith("@"):
				tag, attrs = parse_header_line(line)
				if tag is None:
					print("ERROR")

				# Any new header closes an open <p>
				if in_p:
					fout.write("</s>\n</p>\n")
					in_p = False

				if tag == "BOOK":
					# Close previous book if open
					if in_book:
						fout.write("</book>\n")
						in_book = False

					# Update context
					context["book_title"] = attrs.get("book_title")
					context["book_n"] = attrs.get("n")
					context["book_type"] = attrs.get("book_type")

					# Emit <book>
					book_attrs = {
						"book_type": context["book_type"],
						"n": context["book_n"],
						"book_title": context["book_title"],
					}
					fout.write(f'<text type="book" {build_attr_string(book_attrs)}>\n')
					in_book = True

					# Reset lower-level context when a new book starts
					context["sura_title"] = None
					context["sura_n"] = None
					context["section_title"] = None
					context["chapter_title"] = None
					context["chapter_n"] = None
					context["subchapter_title"] = None

				if tag == "SURA":
					context["sura_title"] = attrs.get("sura_title")
					context["sura_n"] = attrs.get("n")

				if tag == "SECTION":
					context["section_title"] = attrs.get("section_title")
					context["section_n"] = attrs.get("n")

				if tag == "CHAPTER":
					context["chapter_title"] = attrs.get("chapter_title")
					context["chapter_n"] = attrs.get("n")

				if tag == "SUBCHAPTER":
					context["subchapter_title"] = attrs.get("subchapter_title")
					context["subchapter_n"] = attrs.get("n")

				if tag == "SUBSUBCHAPTER":
					context["subsubchapter_title"] = attrs.get("subsubchapter_title")
					context["subsubchapter_n"] = attrs.get("n")

				if tag == "P":
					p_n = attrs.get("n")
					p_id = attrs.get("id")
					if p_n:
						p_n = [x.strip() for x in p_n.split(",")]
						p_n = '/'.join(p_n)
						p_n += f"({p_id})"
					else:
						p_n = f"({p_id})"
					combined_n = ""
					# Combine sura_n + p_n if sura_n exists, else keep p_n
					if context.get('sura_n') and context['sura_n'] not in ["_", "-"]:
						combined_n += f"{context['sura_n']}."
					if context.get('section_n') and context['section_n'] not in ["_", "-"]:
						combined_n += f"{context['section_n']}."
					if context.get('chapter_n') and context['chapter_n'] not in ["_", "-"]:
						combined_n += f"{context['chapter_n']}."
					if context.get('subchapter_n') and context['subchapter_n'] not in ["_", "-"]:
						combined_n += f"{context['subchapter_n']}."
					if context.get('subsubchapter_n') and context['subsubchapter_n'] not in ["_", "-"]:
						combined_n += f"{context['subsubchapter_n']}."
					combined_n += p_n

					p_attrs = {
						# "book_title": context.get("book_title"),
						# "sura_title": context.get("sura_title"),
						# "section_title": context.get("section_title"),
						# "chapter_title": context.get("chapter_title"),
						# "subchapter_title": context.get("subchapter_title"),
						# "subsubchapter_title": context.get("subsubchapter_title"),
						"n": combined_n,
						"id": attrs.get("id"),
					}
					book_title = context.get("book_title")
					sura_title = context.get("sura_title")
					section_title = context.get("section_title")
					chapter_title = context.get("chapter_title")
					subchapter_title = context.get("subchapter_title")
					subsubchapter_title = context.get("subsubchapter_title")
					pages = attrs.get("pages")
					if pages:
						p_attrs["pages"] = pages

					if book_title and not book_title in ["_", "-"]:
						p_attrs["book_title"] = book_title
					if sura_title and not sura_title in ["_", "-"]:
						p_attrs["sura_title"] = sura_title
					if section_title and not section_title in ["_", "-"]:
						p_attrs["section_title"] = section_title
					if chapter_title and not chapter_title in ["_", "-"]:
						p_attrs["chapter_title"] = chapter_title
					if subchapter_title and not subchapter_title in ["_", "-"]:
						p_attrs["subchapter_title"] = subchapter_title
					if subsubchapter_title and not subsubchapter_title in ["_", "-"]:
						p_attrs["subsubchapter_title"] = subsubchapter_title

		#             # Keep translation if present
					if "translation" in attrs and not attrs["translation"] in ["_", "-"]:
						p_attrs["translation"] = attrs["translation"]

					fout.write(f"<p {build_attr_string(p_attrs)}>\n")
					fout.write("<s>\n")
					in_p = True

			else:
				# Normal/token line
				if in_p and line.strip() != "":
					fout.write(line + "\n")
				else:
					# outside <p>, ignore (adjust if you need to keep stray lines)
					print("ERROR", line)

		# Close any open tags at EOF
		if in_p:
			# fout.write("</s>\n")
			fout.write("</s>\n</p>\n")
		if in_book:
			fout.write("</text>\n")

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: python tab2vert.py input.txt output.xml")
		sys.exit(1)
	main(sys.argv[1], sys.argv[2])
