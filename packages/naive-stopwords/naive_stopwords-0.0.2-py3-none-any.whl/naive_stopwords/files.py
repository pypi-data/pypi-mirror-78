import os


pwd = os.path.abspath(os.path.dirname(__file__))

stopword_dir = os.path.join(pwd, 'data')

all_stopwords_files = [os.path.join(pwd, 'data', f) for f in os.listdir(stopword_dir)]
