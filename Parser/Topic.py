
class Topic(object):

    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return self.get_text()

    def __eq__(self, other):
        return self.get_text() == other.get_text()

    def __str__(self):
        return self.text

    def get_text(self):
        return self.text