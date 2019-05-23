class Database:
    def __init__(self, documents, keywords):
        self.documents = documents
        self.keywords = keywords

class Document:
    def __init__(self, path, title, words):
        self.path = path
        self.title = title
        self.words = words

class Keyword:
    def __init__(self, word):
        self.word = word
        self.occurs = []
        self.idf = 0

class KeywordOccurrenceInDocument:
    def __init__(self, document_id, positions):
        self.document_id = document_id
        self.tf = 0
        self.positions = positions
