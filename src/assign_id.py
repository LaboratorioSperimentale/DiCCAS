import sys
from lxml import etree

parser = etree.XMLParser(remove_blank_text=False)
tree = etree.parse(sys.argv[1], parser)
root = tree.getroot()

# TEI namespace
ns = {"tei": "http://www.tei-c.org/ns/1.0"}

counter = 1
for p in root.xpath(".//tei:p", namespaces=ns):
    # if p.get("id", "") == "":
	p.set("id", str(counter))
	counter += 1


tree.write(
    "output.xml",
    encoding="UTF-8",
    xml_declaration=True,
    pretty_print=True
)