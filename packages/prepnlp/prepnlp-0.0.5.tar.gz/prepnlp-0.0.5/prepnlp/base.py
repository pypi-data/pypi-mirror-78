class AspectTerm(object):
    """
    represent a token for absa
    """

    def __init__(self, term: str, bio: str = None, offset_start: int = None, offset_end: int = None, polarity: str = None,
                 doc_id: int = None):
        self.term = term
        self.bio = bio
        self.offset_start = offset_start
        self.offset_end = offset_end
        self.sentiment = polarity
        self.doc_id = doc_id

    def __str__(self) -> str:
        return '{}/{}/{} ({}, {})'.format(self.term, self.bio, self.sentiment, self.offset_start, self.offset_end)


class AbsaDoc(object):
    """
    represent a document
    """
    DEFAULT_VOCABULARY = {
        'O': 0,
        'B-ASPECT-POS': 1,
        'I-ASPECT-POS': 2,
        'B-ASPECT-NEG': 3,
        'I-ASPECT-NEG': 4,
        'B-ASPECT-NEU': 5,
        'I-ASPECT-NEU': 6,
    }

    def __init__(self, text: str, doc_id: int = None, aspect_category: str = None,
                 aspect_category_sentiment: str = None):
        self.doc_id = doc_id
        self.text = text
        self.aspect_terms = list()
        self.aspect_category = None
        self.aspect_category_sentiment = None

    def has_aspect_terms(self):
        return len(self.aspect_terms) > 0

    def add_aspect_term(self, token: AspectTerm):
        self.aspect_terms.append(token)

    def to_bio_aspect(self, suffix: str = 'ASPECT') -> list:
        pass

    def to_bio_aspect_sentiment(self, suffix: str = 'ASPECT', sentiments: list = {'POS', 'NEG', 'NEU'}) -> list:
        pass
