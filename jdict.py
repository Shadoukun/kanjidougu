#* coding: utf-8

import tinysegmenter
from cjklib.dictionary import EDICT
import re



#text = u'これは一例のです。'

def tokenize(text):
    outtokens = []
    segmenter = tinysegmenter.TinySegmenter()
    tokens = segmenter.tokenize(text)
    for token in tokens:
        token = (token, segmenter._ctype(token))
        outtokens.append(token)
    return outtokens
    # return [token for token in tokens]


def search(text):
    # Takes text and runs tokenize() and then runs headword()
    output = []
    jdict = EDICT()
    tokens = tokenize(text)
    for t in tokens:
        defs = jdict.getFor(t[0])
        for line in defs:
            line = ''.join(line)
            output.append(line)

    return output


#tokens = tokenize(text)
#word = tokens[0]
#print word[0]
jdict = EDICT()

def trydef(text):
    output = []
    outdict = jdict.getForHeadword(text)
    for line in outdict:
        output.append(line)
    if len(output) < 1:
        output = []
        outdict = jdict.getForReading(text)
        for line in outdict:
            output.append(line)
    return output

def parsedef(inlist):
    re1 = re.compile(r'(?:\(.*?\))')
    #print tuples
    outline = []
    for t in inlist:
        head, reading = t[0:2]
        trans = t[2]
        trans = re.sub(re1, '', trans)
        trans = re.sub('\W{2,}', ' ', trans)
        trans = trans.replace('/', ' ')
        outline.extend((head, reading, trans))
    return [outline[i:i+3] for i in xrange(0, len(outline), 3)]

text = trydef(u'愛')
print(parsedef(text))
#print parsedef(text)
#test = parsedef(blah)
#print '||'.join(test)
#for t in tuples:

# blah2 = []
# blah = search(text)   ``
# pprint.pprint([l for l in blah])
#

#for outset in blah:
#    for line in outset:
#        blah2.append([l for l in line])
#print blah2
# print '|'.join(tokens)
