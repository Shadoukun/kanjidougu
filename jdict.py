#* coding: utf-8

import tinysegmenter
from cjklib.dictionary import EDICT
import re
import sys
reload(sys)
sys.setdefaultencoding('utf8')




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

jdict = EDICT()

def trydef(text):
    jdict = EDICT()
    jdict.db.registerUnicode = True

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
