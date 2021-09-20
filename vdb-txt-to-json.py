import codecs
import json
import re


def main():
    file = codecs.open("sources/vocabolario di base pulito.txt", 'r', 'utf-8')
    wordlist = {}
    used_abbr = {}
    abbr_not_found = {}
    abbr = json.load(codecs.open('sources/abbr.json', 'r', 'utf-8'))
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
                        wordlist[list(wordlist.keys())[-1]][-1]['features'] += ", "
                        for k in word:
                            wordlist[list(wordlist.keys())[-1]][-1]['features'] += f"{k} "

    for i in wordlist.keys():
        for j in wordlist[i]:
            exp_features = ''
            j['features'] = j['features'].strip()
            comma_split = j['features'].split(',')
            for el in comma_split:
                el = el.strip()
                if el in abbr:
                    exp_features += abbr[el] + ", "
                    used_abbr[el] = abbr[el]
                else:
                    for x in el.split('.'):
                        x = x.strip()
                        y = x + "."
                        if y in abbr:
                            exp_features += abbr[y] + " "
                            used_abbr[y] = abbr[y]
                        else:
                            y = y.split(' ')
                            for z in y:
                                z = z.strip()
                                if z in abbr:
                                    exp_features += abbr[z] + " "
                                    used_abbr[z] = abbr[z]
                                elif z not in ['.', ',', ' ']:
                                    exp_features += z + " "
                                    if z in abbr_not_found:
                                        abbr_not_found[z] = abbr_not_found[z] + 1
                                    else:
                                        abbr_not_found[z] = 0
                    exp_features = exp_features.strip() + ", "
            exp_features = exp_features.strip()
            if exp_features[-1] == ',':
                exp_features = exp_features[:-1]
            j['features_string'] = exp_features

    with codecs.open("vocabolario_di_base/vdb.json", "w", "utf-8") as f:
        f.write(json.dumps(wordlist))
    with codecs.open("useful_data/used_abbr.json", "w", "utf-8") as g:
        g.write(json.dumps(used_abbr))
    with codecs.open("useful_data/not_found_abbr.json", "w", "utf-8") as h:
        h.write(json.dumps(abbr_not_found))


def clean_vdb_txt():
    with codecs.open("sources/vocabolario di base.txt", "r", "utf-8") as f:
        cleaned = re.sub(r"- ", '', f.read())
        with codecs.open("sources/vocabolario di base pulito.txt", "w", "utf-8") as o:
            o.write(cleaned)


if __name__ == '__main__':
    main()
