import main_folder.ctakes_types as ct


# Prints a CAS
def print_cas(cas):
    for sentence in cas.select(ct.Sentence):
        print(sentence.get_covered_text())
        for token in cas.select_covered(ct.WordToken, sentence):
            # Annotation values can be accessed as properties
            print(
                "Token: Text={0}, begin={1}, end={2}, pos={3}".format(
                    token.get_covered_text(), token.begin, token.end, token.partOfSpeech
                )
            )
