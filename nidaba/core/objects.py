from bs4 import BeautifulSoup
from .util import Text


class SEObject(object):
    """
    Base Object for SE Objects
    """
    def __init__(self, data):
        self._data = data


class User(SEObject):
    """
    Stack Overflow User object which will hold information for use in
    Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: dict containing user information.
        :return: None
        """
        super().__init__(data)


class Post(SEObject):
    """
    Base object for Question, Answer, Comments
    """

    def __init__(self, data):
        """
        :param data: Dict containing Post information.
        :return: None
        """
        super().__init__(data)
        self.body = self._data.get('body', '')
        self.soup = BeautifulSoup(self.body)

        self.text = self._get_text()
        self.code = self._get_code()

    def _get_code(self):
        """
        Extract code without markup tags from a given html content.
        :param html: String
        :return List of code strings in the given content
        """

        return [i.get_text() for i in self.soup.find_all('code')]

    def _get_text(self):
        """
        Extract text from html content by removing markup tags & code.
        :param html: String
        :return List of strings in the given content
        """

        # Hacky. But the official docs say that to remove tags (such as <code></code>) you should use
        # the LC method below. Unfortunately that ruins self.soup for any other methods. Making a
        # new soup seemed the best choice.
        soup = BeautifulSoup(self.body)

        [s.extract() for s in soup('code')]

        text = Text(soup.get_text().strip())

        return text


class Comment(Post):
    """
    Stack Overflow Comment object which will hold information for use in
    Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: Dict containing comment information.
        :return: None
        """
        super().__init__(data)


class Answer(Post):
    """
    Stack Overflow Answer object which will hold information for use in
    Nidaba analysis.
    """

    def __init__(self, data):
        """
        :param data: dict containing answer information.
        :return: None
        """
        super().__init__(data)


class Question(Post):
    """
    Stack Overflow Question object which will hold information for use in
    Nidaba analysis.
    """

    def __init__(self, data, answers=None, comments=None):
        """
        :param data: Dict containing question information.
        :param answers: List of dicts containing answer information.
        :param comments: List of dicts containing comment information
        :return: None
        """
        super().__init__(data)

        if answers is None:
            self.answers = []
        else:
            self.answers = [Answer(ans) for ans in answers]

        if comments is None:
            self.comments = []
        else:
            self.comments = [Comment(comm) for comm in comments]
