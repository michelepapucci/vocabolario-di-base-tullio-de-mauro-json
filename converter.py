import codecs
import json
import re


def old_main():
    file = codecs.open("vocabolario di base.txt", 'r', 'utf-8')
    wordlist = {}
    abbr = json.load(codecs.open('abbr.json', 'r', 'utf-8'))
    for line in file:
        text = line.split(',')

        for word in text:
            word = word.strip()
            word = word.split('.')
            word.pop()
            features = ""
            if len(word) > 0:
                if word[0] not in abbr:
                    w = word[0]
                    w_space = w.split(' ')
                    for i in range(1, len(w_space)):
                        w_space[i] = w_space[i].replace(']', '')
                        w_space[i] = w_space[i].replace(')', '')
                        features += w_space[i] + " "
                    w = w_space[0]
                    w = re.sub(r"\d", '', w)
                    word_features = {}

                    if '(' in w:
                        w = w.replace('(', '')
                        word_features['cat'] = 'FO'
                    elif '[' in w:
                        w = w.replace('[', '')
                        word_features['cat'] = 'AD'
                    else:
                        word_features['cat'] = 'AU'

                    for i in range(1, len(word)):
                        features += word[i] + " "
                    features.strip()
                    word_features['features'] = features
                    if w in wordlist:
                        wordlist[w].append(word_features)
                    else:
                        wordlist[w] = list()
                        wordlist[w].append(word_features)
                else:
                    for k in word:
                        wordlist[list(wordlist.keys())[-1]][-1]['features'] += k + " "


# il trova stronzi: "features": ""
def main():
    file = codecs.open("vocabolario di base.txt", 'r', 'utf-8')
    wordlist = {}
    abbr = json.load(codecs.open('n_abbr.json', 'r', 'utf-8'))
    for line in file:
        text = line.split(',')

        for word in text:
            word = word.strip()
            word = word.split(' ')
            features = ""
            if len(word) > 0:
                if word[0] not in abbr and word[0] != "":
                    w = word[0]
                    w = re.sub(r"\d", '', w)
                    word_features = {}

                    if '(' in w:
                        w = w.replace('(', '')
                        word_features['cat'] = 'FO'
                    elif '[' in w:
                        w = w.replace('[', '')
                        word_features['cat'] = 'AD'
                    else:
                        word_features['cat'] = 'AU'

                    for i in range(1, len(word)):
                        word[i] = word[i].replace(']', '')
                        word[i] = word[i].replace(')', '')
                        features += word[i] + " "
                    features = features
                    word_features['features'] = features
                    if w in wordlist:
                        wordlist[w].append(word_features)
                    else:
                        wordlist[w] = list()
                        wordlist[w].append(word_features)
                else:
                    if len(word) > 0:
                        for k in word:
                            wordlist[list(wordlist.keys())[-1]][-1]['features'] = \
                                wordlist[list(wordlist.keys())[-1]][-1]['features'].strip()
                            wordlist[list(wordlist.keys())[-1]][-1]['features'] += f", {k} "

    for i in wordlist.keys():
        for j in wordlist[i]:
            exp_features = ''
            j['features'] = j['features'].strip()
            comma_split = j['features'].split(',')
            for el in comma_split:
                el = el.strip()
                if el in abbr:
                    exp_features += abbr[el] + ", "
                else:
                    for x in el.split('.'):
                        x = x.strip()
                        y = x + "."
                        if y in abbr:
                            exp_features += abbr[y] + " "
                        else:
                            exp_features += x + " "
                    exp_features = exp_features.strip() + ", "
            exp_features = exp_features.strip()
            if exp_features[-1] == ',':
                exp_features = exp_features[:-1]
            j['features_string'] = exp_features

    with codecs.open("n_vdb.json", "w", "utf-8") as f:
        f.write(json.dumps(wordlist))


def convert_abbr():
    file = codecs.open("n_abbr.txt", 'r', 'utf-8')
    doc = {}
    for line in file:
        text = line.split(' ')
        abbr = text[0].strip()
        descr = ''
        for i in range(1, len(text)):
            descr += text[i].strip() + " "
        descr = descr.replace('\n', '')
        descr = descr.replace('\r', '')
        doc[abbr] = descr.strip()
    j = json.dumps(doc)
    file.close()
    with codecs.open("n_abbr.json", 'w', 'utf-8') as f:
        f.write(j)


if __name__ == '__main__':
    main()
