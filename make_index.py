import argparse
import os
import pickle
import math

import bs4

import utility
from database import Database, Document, Keyword, KeywordOccurrenceInDocument

parser = argparse.ArgumentParser()
parser.add_argument("documents_dir", help="The directory of HTML documents to be searched")
parser.add_argument("database_file", help="The path of file to store the database")
args = parser.parse_args()
db_file = open(args.database_file, "wb")

def load_document(path):
    html = open(path, "rb").read().decode('utf-8-sig')
    dom = bs4.BeautifulSoup(html, "html.parser");
    for extra_tag in dom.find_all(["script", "style"]):
        extra_tag.decompose()

    title_node = dom.find('title')
    title = title_node.text if title_node else ''
    return Document(path, title, utility.cut_words(dom.text))

doc_id = 0
file_list = []
for path, dirs, files in os.walk(args.documents_dir):
    for file in files:
        file_list.append(path + '/' + file)

keywords = {}
documents = []
for file in file_list:
    print("[%d/%d, %d words] Loading file: %s" % (doc_id, len(file_list), len(keywords), file))

    doc = load_document(file)
    for word in set(doc.words):
        if word not in keywords:
            keywords[word] = Keyword(word)
        keywords[word].occurs.append(
            KeywordOccurrenceInDocument(
                doc_id,
                list(filter(lambda x: x != None, [i if doc.words[i] == word else None for i in range(len(doc.words))]))
            )
        )
    doc_id += 1
    documents.append(doc);

for word in keywords:
    keywords[word].idf = math.log10(1 + len(keywords[word].occurs) / len(documents))
    for occur in keywords[word].occurs:
        occur.tf = len(occur.positions) / len(documents[occur.document_id].words)

pickle.dump(Database(
    documents,
    keywords
), db_file)
