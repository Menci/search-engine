import pickle
import argparse
import statistics
import readline
import time

import termcolor

start_time = time.clock()

print('Loading jieba...')

import utility
from database import Database, Document, Keyword, KeywordOccurrenceInDocument

parser = argparse.ArgumentParser()
parser.add_argument("database_file", help="The path of file to store the database")
args = parser.parse_args()

print('Loading index database...')

database = pickle.load(open(args.database_file, "rb"))

print('\nInitizlized in %s second(s).\n' % termcolor.colored("%.3lf" % (time.clock() - start_time), color="green", attrs=["bold"]))

def do_search(search_keywords):
    if database.keywords.get(search_keywords[0]) == None:
        return []

    def check_following_words(keyword_occur):
        document = database.documents[keyword_occur.document_id]
        for pos in keyword_occur.positions:
            mismatch = False
            try:
                for i in range(1, len(search_keywords)):
                    if search_keywords[i] != document.words[pos + i]:
                        mismatch = True
                        break
            except IndexError:
                mismatch = True

            if not mismatch:
                return True
        return False
    occurs = filter(check_following_words, database.keywords[search_keywords[0]].occurs)
    document_ids = map(lambda occur: occur.document_id, occurs)

    weight = {}
    for document_id in document_ids:
        weight[document_id] = 0
    
    for word in search_keywords:
        for occur in database.keywords[word].occurs:
            try:
                weight[occur.document_id] += occur.tf * database.keywords[word].idf
            except KeyError:
                pass

    results = list(zip(weight.keys(), weight.values()))
    results.sort(key=lambda x: x[1], reverse=True)

    return results

def generate_snippet(document, search_keywords):
    found_pos = -1
    for i in range(len(document.words) - len(search_keywords)):
        mismatch = False
        for j in range(len(search_keywords)):
            if document.words[i + j] != search_keywords[j]:
                mismatch = True
                break
        if not mismatch:
            found_pos = i
            break
    
    result = []
    for i in range(found_pos - 20, found_pos + len(search_keywords) + 20):
        try:
            result.append(document.words[i])
        except IndexError:
            pass
    
    return result

def process_input(input):
    search_keywords = utility.cut_words(input)

    print("\nKeywords to search: %s\n" % ' '.join([
        termcolor.colored(word, color="yellow", attrs=["bold"])
        for word in search_keywords
    ]))

    results = do_search(search_keywords)

    print("%s result(s) found.\n" % termcolor.colored(len(results), color="green", attrs=["bold"]))

    for i in range(len(results)):
        result = results[i]
        document = database.documents[result[0]]
        print("%s (TF-IDF weight = %s): %s (%s)" % (
            termcolor.colored("Result #%d" % (i + 1), color="green", attrs=["bold"]),
            termcolor.colored("%.6lf" % result[1], attrs=["bold"]),
            termcolor.colored(document.title, color="magenta", attrs=["bold"]),
            document.path
        ))
        print(' '.join([
            termcolor.colored(word, color="yellow", attrs=["bold"]) if word in search_keywords else word
            for word in generate_snippet(document, search_keywords)
        ]))
        print('')

try:
    while True:
        try:
            input_keywords = input('Search> ').strip()
            if not input_keywords:
                continue

            start_time = time.clock()
            process_input(input_keywords)
            end_time = time.clock()

            print('Query finished in %s second(s).\n' % termcolor.colored('%.6lf' % (end_time - start_time), color="green", attrs=["bold"]))
        except KeyboardInterrupt:
            print('')
            continue
except EOFError:
    print('')
