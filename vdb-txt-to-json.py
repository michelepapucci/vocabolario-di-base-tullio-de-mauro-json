import codecs
import json
import re


def main():
    file = codecs.open("sources/vocabolario di base pulito.txt", 'r', 'utf-8')
    wordlist = {}
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
                            # add a space split to get stuff after "e". Ex: s.f. e m. with a . split you get:
                            # [s] [f] [e m] I need to divide [e] and [m] with a space split.
                            y = y.split(' ')
                            for z in y:
                                z = z.strip()
                                if z in abbr:
                                    exp_features += abbr[z] + " "
                                elif z not in ['.', ',', ' ']:
                                    exp_features += z + " "
                    exp_features = exp_features.strip() + ", "
            exp_features = exp_features.strip()
            if exp_features[-1] == ',':
                exp_features = exp_features[:-1]
            j['features_string'] = exp_features

    with codecs.open("vocabolario_di_base/vdb.json", "w", "utf-8") as f:
        f.write(json.dumps(wordlist))


def clean_vdb_txt():
    with codecs.open("sources/vocabolario di base.txt", "r", "utf-8") as f:
        cleaned = re.sub(r"- ", '', f.read())
        with codecs.open("sources/vocabolario di base pulito.txt", "w", "utf-8") as o:
            o.write(cleaned)


if __name__ == '__main__':
    main()
