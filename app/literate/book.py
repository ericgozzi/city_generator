import re
import random
from collections import Counter



from data import read_txt_file
from data import export_json
from data import read_json

from metrika import Graph

from metrika import Rule



# NATURAL LANGUAGE TOOLKIT
# pip install nltk
import nltk

# Download WordNet data needed for Lemmatization
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords



import networkx as nx



class Book:
    """
    A class to represent a book.
    """


    def __init__(self, author: str, title: str):
        self.author = author.lower()
        self.title = title.lower()



    def __str__(self):
        return f'Book: author: {self.author.upper()}, title: {self.title}'
    




    def generate_book_data_for_library(self, library_folder: str):
        """
        Export in the folder the book data that the class `Library` needs to compute.

        Args:
            library_folder (str): path to the folder on which to export the book data. 

        Returns:
            None
        """

        concatenation_of_words = self.get_concatenation_of_words()
        graph = Graph()        
        graph.build_graph_from_rules(concatenation_of_words)

        data = {
            'author' : self.author,
            'title' : self.title,

            'content' : self.content,

            'words' : self.get_words(),
            'sentences' : self.get_sentences(),

            'words count' : self.get_words_count(),

            'eigenvector' : graph.eigenvector_centrality
        }
        library_folder = f'{library_folder}/{self.author.upper()}_{self.title}.json'
        
        export_json(data, library_folder)
        
        self.has_json = True
        self.json_path = library_folder


    def read_content(self) -> str:
        """
        Reads the book content from the associated json file. 

        Args:
            None

        Returns:
            str: The content of the book.
        """
        if self.has_json:
            data = read_json(self.json_path)
            content = data['content']
            return content
        else:
            raise FileNotFoundError('The json file associated with this book does not exists yet.')

    def read_words(self) -> list[str]:
        """
        Reads the book words from the associated json file. 

        Args:
            None

        Returns:
            list[str]: List with the words of the book.
        """
        if self.has_json:
            data = read_json(self.json_path)
            words = data['words']
            return words
        else:
            raise FileNotFoundError('The json file associated with this book does not exists yet.')

    
    def read_sentences(self) -> list[str]:
        """
        Reads the book sentences from the associated json file. 

        Args:
            None

        Returns:
            list[str]: List with the sentences of the book.
        """
        if self.has_json:
            data = read_json(self.json_path)
            sentences = data['sentences']
            return sentences
        else:
            raise FileNotFoundError('The json file associated with this book does not exists yet.')

    
    def read_word_count(self) -> dict:
        """
        Reads the word count from the associated json file. 

        Args:
            None

        Returns:
            dict: Dictionary with the words as key and how many time they appears in the book as value.
        """
        if self.has_json:
            data = read_json(self.json_path)
            word_count = data['words count']
            return word_count
        else:
            raise FileNotFoundError('The json file associated with this book does not exists yet.')

    
    def read_eigenvector(self) -> str:
        """
        Reads the eigenvector values from the associated json file. 

        Args:
            None

        Returns:
            dict: Dictionary with the words as key and their eigenvector value as value. 
        """
        if self.has_json:
            data = read_json(self.json_path)
            eigenvector = data['eigenvector']
            return eigenvector
        else:
            raise FileNotFoundError('The json file associated with this book does not exists yet.')



    def from_author_title_and_content(author: str, title: str, file_content: str):
        """
        Creates a book object from author, title and content.

        Args:
            author (str): the author of the book.
            title (str): the title of the book.
            file_content (str): the file path to a .txt file containing the content of the book.

        Returns:
            Book
        """
        book = Book(author, title)
        book.set_content(file_content)
        return book
    

    def from_json_file(file_path: str):
        """
        Creates a book object from a json file.

        Args:
            file_path (str): the location of the json file with the book information.

        Returns:
            Book
        """
        data = read_json(file_path)
        book = Book(data['author'], data['title'])
        book.content = data['content']
        book.has_json = True
        book.json_path = file_path
        return book


    def set_content (self, file_path: str) -> None:
        """
        Set the contents of the book.

        Args:
            file_path (str): the file path to a .txt file containing the content of the book.
        
        Returns:
            None
        """
        self.content = read_txt_file(file_path)


    def curate_book(self):
        """
        Cleans and refines the book content by removing or replacing specific characters 
        and formatting inconsistencies.

        Args:
            None (Operates on the instance's `self.content` attribute).

        Returns:
            None: The cleaned text is stored back in `self.content`.+

        Replacements:
            - `{`, `}` → replaced with a space.
            - `-` → replaced with a space.
            - `\n`, `\r` → replaced with a space.
            - `" ."` → replaced with `"."` (removes space before periods).
            - `" ,"` → replaced with `","` (removes space before commas).
            - Multiple consecutive spaces → replaced with a single space.

        Example:
            Before:
                self.content = "Hello - world!\nThis is {a} test.\rAnother  example."
            
            After calling `curate_book()`:
                self.content = "Hello world! This is a test. Another example."
        """
        text = self.content
        text = text.replace("}", " ")
        text = text.replace("{", " ")
        text = text.replace("-", " ")
        text = text.replace("\n", " ") 
        text = text.replace(" .", ".")
        text = text.replace(" ,", ",")
        text = text.replace("\r", " ")
        text = re.sub(r'\s+', ' ', text)
        self.content = text


    def get_words(self, store_as_variable=False) -> list:   
        """
        Processes the content to extract lemmatized words, excluding stopwords and short words.

        This method takes the content, converts it to lowercase, finds all words using a regular expression, 
        lemmatizes each word, and filters out stopwords and words with fewer than 3 characters. The resulting list
        contains lemmatized words that are not stopwords.

        Args:
            store_as_variable (bool, optional): A flag to indicate whether to store the processed words in a variable.
                                                Default is False.

        Returns:
            list: A list of lemmatized words, excluding stopwords and words shorter than 3 characters.

        Example:
            content = "The quick brown fox jumped over the lazy dog."
            words = get_words(store_as_variable=True)
            print(words)
            # Output: ['quick', 'brown', 'fox', 'jumped', 'lazy', 'dog']
        """
        lemmatizer = WordNetLemmatizer()

        all_words = re.findall(r'\b\w+\b', self.content.lower())

        words = []
        stop_words = set(stopwords.words("english"))
        for word in all_words:

            base_form = lemmatizer.lemmatize(word)

            if base_form not in stop_words and len(base_form)>2:
                words.append(base_form) 
        return words
    

    def get_top_10_words(word_list: list) -> list:
        """
        Returns the top 10 most common words from a given list.

        Args:
            word_list (list): A list of words (strings).

        Returns:
            list: A list of tuples containing the top 10 words and their counts.
        """
        word_counts = Counter(word_list)  # Count occurrences
        return word_counts.most_common(10)
    


    def get_top_100_words(word_list: list) -> list:
        """
        Returns the top 100 most common words from a given list.

        Args:
            word_list (list): A list of words (strings).

        Returns:
            list: A list of tuples containing the top 10 words and their counts.
        """
        word_counts = Counter(word_list)  # Count occurrences
        return word_counts.most_common(100) 
    

    def get_top_n_words(word_list: list, n: int) -> list:
        """
        Returns the top n most common words from a given list.

        Args:
            word_list (list): A list of words (strings).

        Returns:
            list: A list of tuples containing the top 10 words and their counts.
        """
        word_counts = Counter(word_list)  # Count occurrences
        return word_counts.most_common(n) 





    def get_sentences(self) -> list:
        """
        Splits the content into individual sentences and filters out short sentences.

        This method splits the content into sentences by the period followed by a space (". "), 
        then filters out sentences that are shorter than 4 characters. It appends a period to 
        each valid sentence before adding it to the result list.

        Returns:
            list: A list of sentences from the content, each with a period appended, and 
                filtered to include only sentences with more than 3 characters.

        Example:
            content = "This is a sentence. Another one. Short."
            sentences = get_sentences()
            print(sentences)
            # Output: ['This is a sentence.', 'Another one.']
        """
        all_sentences = self.content.split(". ")
        sentences = []
        for sentence in all_sentences:
            if len(sentence) > 3:
                sentence = sentence + "."
                sentences.append(sentence)
                
        return sentences
    




    def get_concatenation_of_words(self) -> list[tuple]:
        """
        Returns a list of consecutive word pairs from the content.

        This method processes the list of words (using `get_words`), and creates pairs of 
        consecutive words. Each pair is represented as a tuple, where the first word is 
        followed by the second word in the pair.

        Returns:
            list: A list of tuples, where each tuple contains two consecutive words from the content.

        Example:
            content = "The quick brown fox"
            word_pairs = get_concatenation_of_words()
            print(word_pairs)
            # Output: [('the', 'quick'), ('quick', 'brown'), ('brown', 'fox')]
        """
        word_connections = []
        words = self.get_words()

        for i in range(len(words) - 1):
            word_connections.append((words[i], words[i+1]))
            

        return Rule(word_connections)
    



    def get_words_count(self):
        """
        Returns the count of each unique word in the content.

        This method uses `get_words` to extract a list of lemmatized words from the content,
        and then counts the frequency of each word using a `Counter`. The result is a dictionary 
        where the keys are the words, and the values are their respective counts.

        Returns:
            dict: A dictionary where the keys are words and the values are their frequencies in the content.

        Example:
            content = "The quick brown fox jumps over the lazy dog."
            word_counts = get_words_count()
            print(word_counts)
            # Output: {'the': 2, 'quick': 1, 'brown': 1, 'fox': 1, 'jumps': 1, 'over': 1, 'lazy': 1, 'dog': 1}
        """
        words = self.get_words()
        words_count = Counter(words)
        return words_count




    def get_words_graph(self):
        graph = nx.Graph()
        for word1, word2 in self.word_connections:
            graph.add_edge(word1, word2)
        self.eigenvector_centrality = nx.eigenvector_centrality(graph)
        self.add_metadata("eigenvector", self.eigenvector_centrality)


    





class Quote:

    def __init__(self, quote: str, book: Book):
        self.quote: str = quote
        self.book: Book = book

    def __str__(self):
        return f'{self.author.upper()}, {self.book_title.title()}:\n\t\t{self.quote}\n---'

    @property
    def book_title(self) -> str:
        return self.book.title.title()

    @property
    def author(self) -> str:
        return self.book.author.upper()


    def from_quote_and_book(quote: str, book: Book):
        return Book(quote, book)
    

    def from_ask_library_ouput(quote: str):
        book, quote = quote.split("\n\t\t")
        author, title = book.split(", ")
        title = title.replace(":", "")
        quote = quote.replace('\t', "")
        quote = quote.replace('\n---', "")
        book = Book(author, title)
        return Quote(quote, book)


            





class Quotebook:
    
    def __init__(self, quotes: list[Quote]):
        self.quotes = quotes
    
    @property
    def number(self):
        return len(self.quotes)
    
    def from_collection_of_quotes(file_path: str):
        data = read_txt_file(file_path)
        raw_quotes = data.split("---")
        quotes = []
        for rq in raw_quotes:
            try:
                quote = Quote.from_ask_library_ouput(rq)
                quotes.append(quote)
            except:
                continue
        quotebook = Quotebook(quotes)
        return quotebook
    

    def build_text(self, create_title=False, n=10):
        quotes = self.quotes.copy()
        text = ""
        footnotes = ""
        for i in range(min(len(quotes), n)):
            text_snippet = quotes[i].quote
            text_snippet = text_snippet.replace('\n', ' ')
            
            author = quotes[i].author
            author = author.replace('\n', '')
            author = author.replace('\t','')
            author = author.replace('  ', ' ')

            title = quotes[i].book_title
            title = title.replace('\n', ' ')

            text += f'{text_snippet}[{i}] '
            footnotes += f'[{i}]: {author}, {title} \t'  

        title = None
        if create_title:
            words = get_most_popular_word(text)
            word_counts = Counter(words)
            most_common = word_counts.most_common(1)
            title = f'{most_common[0][0]}'


        return text, footnotes, title
    



def get_most_popular_word(text):
    lemmatizer = WordNetLemmatizer()
    all_words = re.findall(r'\b\w+\b', text)
    words = []
    stop_words = set(stopwords.words("english"))
    for word in all_words:
        base_form = lemmatizer.lemmatize(word)
        if base_form not in stop_words and len(base_form)>2:
            words.append(base_form) 
    return words


