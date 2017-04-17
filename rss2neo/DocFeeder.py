import fnmatch
import os
from RssFeeder import Feeder, Feed


class DocFeeder(Feeder):
    """ 
     `Author`: Eliakah kakou
     DocFeeder.py
     This class recursively access each file in a given directory,
      then generates a list of feed instances containing relevant data about the file 
    """

    def __init__(self, file):
        """
        The constructor, initializes the DocFeeded instance 
        :param file: directory path
        """
        Feeder.__init__(self, file)
        self.feeds = []
        self.paths = []
        self.path = file
        self.__getPaths(file)

    def __getPaths(self, file):
        """
        This method inserts each link from the file as an entry into the 'paths' list
        :param file: path to original directory
        :return: none
        """
        print "getting Paths"
        matches = []
        for filename in self.__find_files(file, "*.*"):
            matches.append(filename)
        self.paths = matches

    def __find_files(self, directory, pattern):
        """
        This method yields every single file in the directory matching the pattern
        :param directory: directory path
        :param pattern: file name pattern
        :return: file paths matching pattern
        """
        print "finding files"
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    yield filename

    def fetch(self):
        """
        This method appends all of the feed instances to 'feeds'
        :return: none
        """
        print "fetching ..."
        for i in range(len(self.paths)):
            self.feeds.append(self.__getFeeds(self.paths[i]))

    def load_feeds(self):
        """
        returns 'feeds' which contains all of the feed instances 
        :return: self.feeds
        """
        print "Loading feeds"
        self.fetch()
        return self.feeds

    def __getFileName(self, path):
        """
        This method extracts the file name from the path
        :param path: full path to the file 
        :return: the file name 
        """
        drive, path = os.path.splitdrive(path)
        path, filename = os.path.split(path)
        name = filename.split(".")
        return name[0]

    def __getFeeds(self, file):
        """
         This method generates a Feed instance from the file given
        :param file: full file path
        :return: Feed generated from file
        """
        title = self.__getFileName(file)
        input_file = open(file)
        try:
            content = input_file.read()
        finally:
            input_file.close()

        f = {'id': file, 'title': title, 'link': file, 'summary': content}
        f = Feed(f)
        return f


if __name__ == "__main__":
    feeder = DocFeeder('C:\Users\Research\Desktop\parking')
    feeds = feeder.load_feeds()

    for i in range(len(feeds)):
        print  feeds[i].extract()
