import regex

tagmap = {}

with open("/Users/ludovica/Documents/projects/DiCCAS/places_to_tag.txt") as fin:
	for line in fin:
		line = line.strip().split("\t")
		tagmap[line[0].strip()] = line[1].strip()

patterns = {}
for el in tagmap:
    patterns[el] = regex.compile(
    	rf'(\p{{Arabic}}*{regex.escape(el)}\p{{M}}*)(?!\p{{Arabic}})', flags=regex.V0
	)

subs = {el:0 for el in tagmap}
with open("/Users/ludovica/Documents/projects/DiCCAS/251111corpus_DiCCAS_ids.xml") as fin:
    # <placename translation="Kufa"><hi rendition="bold">
    for line in fin:
        for el in tagmap:
            # print(el)
            pattern = patterns[el]
            # print(pattern)
            # input()
            if pattern.search(line):
                # print(pattern.search(line))
                replacement = (
					rf'<placenameTMP translation="{tagmap[el]}">'
					r'<hi rendition="bold">\1</hi></placename>'
				)
                # print(line)
                line = pattern.sub(replacement, line)
                subs[el]+=1
                # print(line)
                # input()
        print(line.strip("\n"))

for el in subs:
    print(el, subs[el])