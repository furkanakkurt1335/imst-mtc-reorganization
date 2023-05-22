import stanza

nlp = stanza.Pipeline(lang='tr', processors='tokenize')
doc = nlp('This is a test sentence for stanza. This is another sentence.')
for i, sentence in enumerate(doc.sentences):
    print(sentence.text)