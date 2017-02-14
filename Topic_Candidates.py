class Topic_Candidate(object):

    def __repr__(self):
        return self.topic

    def __str__(self):
        return self.topic

    def __init__(self, topic, strength, label):
        self.title = topic
        self.strength = strength
        self.label = label


