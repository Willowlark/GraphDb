# * Created by Eliakah kakou
# Feed.py
# This class allows for more functionality in regards
# to the dictionary entered in the constructor

class Feed:
    # constructor
    def __init__(self, feed):
        self.feed = feed

    # This method returns a subset of the dictionary
    def extract(self):
        return {k: self.feed[k] for k in ('id', 'title', 'link', 'summary')}
