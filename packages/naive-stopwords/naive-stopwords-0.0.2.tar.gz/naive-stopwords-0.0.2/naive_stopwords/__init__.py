import logging


from .stopwords import Stopwords


__name__ = 'naive_stopwords'
__version__ = '0.0.2'


logging.basicConfig(
    format="%(asctime)s %(levelname)7s %(filename)20s %(lineno)4d] %(message)s",
    level=logging.INFO
)
