import re
import math
from collections import Counter
from nltk.corpus import stopwords
import nltk
import string


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
    sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    word = re.compile(r'\w+')
    words = word.findall(remove_stopwords(text))
    return Counter(words)


def get_cosine_similarity_res(content_a, content_b):
    vector1 = text_to_vector(content_a)
    vector2 = text_to_vector(content_b)

    cosine_result = get_cosine(vector1, vector2)
    return cosine_result


def jaccard_similarity(sentence_a, sentence_b):
    tk_a = nltk.word_tokenize(remove_stopwords(sentence_a))
    tk_b = nltk.word_tokenize(remove_stopwords(sentence_b))
    set_a = set(tk_a)
    set_b = set(tk_b)
    jacc_res = float(len(set_a.intersection(set_b))) / len(set_a.union(set_b))
    return jacc_res


def remove_stopwords(text):
    italian_stopwords = stopwords.words('italian')
    clean_corp = [token.lower() for item in text for token in nltk.word_tokenize(item) if
                  token.lower() not in italian_stopwords if token not in string.punctuation and token.isalpha()]

    return str(clean_corp)


if __name__ == "__main__":
    s1 = ["ciao mi chiamo nicholas garau e lavoro in accenture"]
    s2 = ["ciao mi chiamo nicholas garau e lavoro in accenture"]

    res = get_cosine_similarity_res(s1, s2)
    print(res)

    res1 = jaccard_similarity(s1, s2)
    print(res1)

