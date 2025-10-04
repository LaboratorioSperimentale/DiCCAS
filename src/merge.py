def merge_vert_and_conllu_preserve_structure(vert_file, conllu_file, output_file):
    # Step 1: Read lemma and upos from conllu
    conllu_tokens = []
    with open(conllu_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            fields = line.split("\t")
            if len(fields) == 10:
                conllu_tokens.append((fields[2], fields[3], fields[4]))  # lemma, upos, xpos

    # Step 2: Open vert and write merged output
    with open(vert_file, "r", encoding="utf-8") as fin, open(output_file, "w", encoding="utf-8") as fout:
        token_index = 0
        for line in fin:
            line = line.rstrip()
            if not line or line.startswith("<"):
                # Structural or blank line
                fout.write(line + "\n")
            else:
                line = line.split("\t")
                adversity = ';'.join([x.strip() for x in line[3].split(",")])
                if token_index >= len(conllu_tokens):
                    raise ValueError("More token lines in .vert than in .conllu")
                lemma, upos, xpos = conllu_tokens[token_index]
                fout.write(f"{line[0]}\t{lemma}\t{upos}\t{xpos}\t{adversity}\n")
                token_index += 1

    print(f"✅ Merged file written to: {output_file}")



merge_vert_and_conllu_preserve_structure(
    vert_file="data/250917corpus_DiCCAS.vert",
    conllu_file="data/DICCAS1.conllu",
    output_file="data/corpus_DiCCAS_merged.vert"
)