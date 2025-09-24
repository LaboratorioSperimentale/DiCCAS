import xml.etree.ElementTree as ET



tree = ET.parse('data/250917corpus_DiCCAS.xml')
root = tree.getroot()
ns = {'ns': root.tag.split('}')[0].strip('{')}
books = root.findall("ns:text", ns)[0].findall("ns:body", ns)[0].findall("ns:div", ns)


interesting_book = books[3]
head = interesting_book.findall("ns:head", ns)[0]
print(''.join(head.itertext()))
sections = interesting_book.findall("ns:div1", ns)

for section in sections:
	subtitle = section.findall("ns:head", ns)[0]
	print(''.join(subtitle.itertext()))
	chapters = section.findall("ns:div2", ns)

	for chapter in chapters:
		subsubtitle = chapter.findall("ns:head", ns)[0]
		print(''.join(subsubtitle.itertext()))
		subchapters = chapter.findall("ns:div3", ns)

		for subchap in subchapters:
			subsubsubtitle = subchap.findall("ns:head", ns)[0]
			print(''.join(subsubsubtitle.itertext()))
			ps = subchap.findall("ns:p", ns)

			for p in ps:
				print(''.join(p.itertext()).split())
				input()

