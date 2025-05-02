from .book import *
from .theka import *
from .functions import *

from .database import *

from data import *


# NATURAL LANGUAGE TOOLKIT
# pip install nltk
import nltk

# Download WordNet data needed for Lemmatization
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords


# Download WordNet data needed for Lemmatization
from nltk.downloader import Downloader

d = Downloader()

# Check and download 'wordnet'
if not d.is_installed("wordnet"):
    nltk.download("wordnet")

# Check and download 'omw-1.4'
if not d.is_installed("omw-1.4"):
    nltk.download("omw-1.4")

# Check and download 'stopwords'
if not d.is_installed("stopwords"):
    nltk.download("stopwords")