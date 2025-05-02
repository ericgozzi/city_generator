from collections import defaultdict

from .book import Book
from .book import Quote

from data import get_all_file_names_in_a_folder




class Library:
    """
    A class to represent a library of books.
    """

    def __init__(self, books: list[Book], library_folder: str):
        self.books = books
        self.library_folder = library_folder
    

    def __str__(self):
        return f'LIBRARY; {len(self.books)} books'
       

    def from_list_of_books(books: list[Book], library_name: str):
        """
        Creates a library object starting from a list of `Book` objects. It will create a folder which will contain the books as a json file. 

        Args:
            books (list[`Book`]): list containing `Book` objects.
            library_name (str): name of the library.
        
        Returns:
            Library
        """
        for book in books:
            book.generate_book_data_for_library(library_name)
        return Library(books, library_name)


    def from_library_folder(library_folder: str):
        """
        Create a Library object starting from a list of json files representing 'Book' objects.
        
        Args:
            library_folder (str): a string indicating the location of the folder.
        
        Returns:
            Library
        """
        json_books = get_all_file_names_in_a_folder(library_folder)
        books = []
        for json_book in json_books:
            book = Book.from_json_file(f'{library_folder}/{json_book}')
            books.append(book)
        library = Library(books, library_folder)
        return library
            


    def sort_books_by_topic(self, topic: str) -> None:
        """
        Sort the book in by the eigenvector centrality of a topic. 

        Args:
            topic (str): the topic on which to sort the books.
        
        Returns:
            None
        """
        sorted_books = {}
        for book in self.books:
            eigenvector = book.read_eigenvector()
            try:
                vector = eigenvector[topic]
            except:
                vector = 0
            sorted_books[book] = vector

        self.books_dictionary = dict(sorted(sorted_books.items(), key=lambda item: item[1], reverse=True))




    def get_answers_to_question(self, question: list[str]) -> list[str]:
        """
        Query the sentences of each book in the library saving the ones containing the words in the question.

        Args:
            question (str): the words on which to query the books in the library.
        
        Returns:
            list[str]: a the sentences containig the anwers to the question.
        """
        answer = []
        for i, book in enumerate(self.books.keys()):
            sentences_list = book.get_sentences()

            results = []
            for sentence in sentences_list:
                if all(word in sentence.split() for word in question):
                    results.append(sentence)
            

            if len(results) != 0:
                answer.append(f"{book.author.upper()}, {book.title} \n \n")
                for j, result in enumerate(results):
                    answer.append(f"\t{result}\n\n ")
                answer.append("\n\n\n\nß")

        return answer
    

    def get_quotes_to_question(self, question: list[str]) -> list[Quote]:
        """
        Query the sentences of each book in the library saving the ones containing the words in the question.

        Args:
            question (str): the words on which to query the books in the library.
        
        Returns:
            Quote[str]: a the sentences containig the anwers to the question.
        """
        answer = []
        for i, book in enumerate(self.books_dictionary.keys()):
            sentences_list = book.get_sentences()

            results = []
            for sentence in sentences_list:
                if all(word in sentence.split() for word in question):
                    results.append(sentence)
            

            if len(results) != 0:
                for result in results:
                    quote = Quote(result, book)
                    answer.append(quote)
        return answer



    def ask(self, topic: str, question: str, **kwargs) -> list[list[str]]:
        """
        Ask theka about a certain topic and question. The order of books are by centrality of the topic inside that book. The quotes of the books come from the book chronology.

        Args:
            topic (str): the topic on which to sort the books.
            question (list[str]): a list of words on which to get the quotes to. 
        
        Returns:
            list[str] : the answers to the question. The first item of the list always show the author and the book from which the quotes come from. 
        """

        print_answers = kwargs.get('print_answers', True)

        topic = topic.lower()
        question = question.lower()
        question = question.split()

        self.sort_books_by_topic(topic)
        answers = self.get_quotes_to_question(question)

        if print_answers:
            print(f'Number of answers: {len(answers)} \n-------------\n\n')
            for answer in answers: 
                print(answer)
                print(f'\n\n')


        return answers
    


    def get_topics(self) -> set[str]:
        """
        Returns a set of strings containing all the topics of the library
        """
        topics: set = set()
        for book in self.books:
            words = book.read_words()
            topics.update(words)
        return topics
    

    def get_most_popular_words(self, n: int):
        words_dictionary = self.get_words_count_dictionary()

        # Calculate total count for each word
        total_counts = {word: sum(counts) for word, counts in words_dictionary.items()}

        # Sort the words by total count in descending order
        sorted_words = sorted(total_counts.items(), key=lambda item: item[1], reverse=True)

        # Get the n most popular words
        top_n_words = sorted_words[:n]
        words = [tnw[0] for tnw in top_n_words]

        return words
    
    def get_eigenvector_dictionary_of_n_most_popular_worlds(self, n:int):
        eigenvector = self.get_eigenvector_dictionary()
        words = self.get_most_popular_words(n)

        limited_dict = defaultdict(float)
        for word in words:
            limited_dict[word] = eigenvector[word]

        return limited_dict


    def get_eigenvector_dictionary(self) -> dict:
        eigen_dictionary = defaultdict(list)
        for book in self.books:
            eigen_values = book.read_eigenvector()

            # For each word in the current book's word counts
            for word, count in eigen_values.items():
                eigen_dictionary[word].append(count)
        
        # To ensure all words have counts for all books (add 0 for missing words)
        for word in eigen_dictionary:
            while len(eigen_dictionary[word]) < len(self.books):
                eigen_dictionary[word].append(0)

        # Convert defaultdict to a regular dict if needed
        eigen_dictionary = dict(eigen_dictionary)

        return eigen_dictionary


    def get_words_dictionary_of_n_popular_words(self, n:int)->dict:
        dict = self.get_eigenvector_dictionary()
        words = self.get_most_popular_words(n)

        limited_dict = defaultdict(list)
        for word in words:
            limited_dict[word] = dict[word]

        return limited_dict


    def get_words_count_dictionary(self) -> dict:
        words_dictionary = defaultdict(list)
        for book in self.books:
            word_counts = book.read_word_count()

            # For each word in the current book's word counts
            for word, count in word_counts.items():
                words_dictionary[word].append(count)
        
        # To ensure all words have counts for all books (add 0 for missing words)
        for word in words_dictionary:
            while len(words_dictionary[word]) < len(self.books):
                words_dictionary[word].append(0)

        # Convert defaultdict to a regular dict if needed
        words_dictionary = dict(words_dictionary)

        return words_dictionary

