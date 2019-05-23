# Search Engine
The task of Advanced Programming class on 2019/04/16. Text search engine using inversed index and TF-IDF.

# Requirements
* Python3 (>= 3.4)

# Installation
```bash
sudo pip3 install -r requirements.txt
```

# Usage
Crawl a website with [web-crawler](https://github.com/Menci/web-crawler) (or another crawler), put only HTML documents (path preserved) in a directory. Build index database with:

```bash
python3 make_index.py [documents_dir] [database_file]
```

Then start search with:

```bash
python3 search.py [database_file]
```

After finish initializing, it will give a REPL to enter keywords to search.

```bash
Search> 搜索关键词
```
