
class Topic_Candidate(object):

    def __repr__(self):
        return self.title

    def __str__(self):
        return self.title

    def __init__(self, title, strength, label):
        self.title = title
        self.strength = strength
        self.label = label