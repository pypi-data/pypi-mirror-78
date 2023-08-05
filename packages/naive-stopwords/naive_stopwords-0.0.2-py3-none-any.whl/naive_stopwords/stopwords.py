import abc

import os

from naive_stopwords import files


class AbstractStopwords(abc.ABC):

    def add(self, word):
        raise NotImplementedError()

    def remove(self, word):
        raise NotImplementedError()

    def contains(self, word):
        raise NotImplementedError()

    def size(self):
        raise NotImplementedError()

    def is_empty(self):
        raise NotImplementedError()

    def dump(self, path):
        raise NotImplementedError()


class Stopwords(AbstractStopwords):

    def __init__(self, stopwords_files=None):
        self.stopwords_files = stopwords_files or []
        default_stopwords_files = files.all_stopwords_files
        self.stopwords_files.extend(default_stopwords_files)

        self.stopwords_set = set()
        self._load_stopwords()

    def _load_stopwords(self):
        for f in self.stopwords_files:
            if not os.path.exists(f):
                continue
            with open(f, mode='rt', encoding='utf8') as fin:
                for line in fin:
                    word = line.rstrip('\n').strip()
                    if not word:
                        continue
                    self.stopwords_set.add(word)

    def add(self, word):
        self.stopwords_set.add(word)

    def remove(self, word):
        if word not in self.stopwords_set:
            return
        self.stopwords_set.remove(word)

    def contains(self, word):
        return True if word in self.stopwords_set else False

    def size(self):
        return len(self.stopwords_set)

    def is_empty(self):
        return self.size() == 0

    def dump(self, path):
        with open(path, mode='wt', encoding='utf8') as fout:
            for w in sorted(self.stopwords_set):
                fout.write(w + '\n')
