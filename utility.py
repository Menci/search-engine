import re

import jieba

from stopwords import stopwords

jieba.setLogLevel(20)
jieba.initialize()

def cut_words(text):
    # Remove punctuations
    text = re.sub("[\.\!\/_,$%^;*()<>\\\[\]+\"\':\|\-+—！，：。？、~@#￥%……&©*；（）【】《》『』「」“”']+", "", text)
    # Remove extra spaces
    text = re.sub('\s+', ' ', text).strip()

    words = []
    for temp in text.split(' '):
        for word in jieba.cut(temp):
            if word not in stopwords:
                words.append(word)

    return words
