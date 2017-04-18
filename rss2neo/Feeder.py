import feedparser
import validators
import sys
import pprint
import fnmatch
import platform
import time
import os



class Feed:
    """
    `Author`: Eliakah kakou
    
    This class allows for more functionality in regards
    to the dictionary entered in the constructor
    """

    def __init__(self, feed):
        """
        `Author`: Eliakah kakou
        
        The constructor 
        
        `feed`: dict instance containing set of information about feed
        """
        self.feed = feed

    def extract(self):
        """
        `Author`: Eliakah kakou

        This method returns a subset of the dictionary
        """
        return {k: self.feed[k] for k in ('id', 'published', 'title', 'link', 'summary')}

    def record_content(self):
        return self.feed['link']


class Feeder:
    """
    `Author`: Bill Clark

    An interface to fulfill a strategy pattern design in the Grapher with feeders.
    An implementation of this interface will be usable with the Grapher so long as
    it provides the appropriate returns. 

    Feeder instances should be created with a link to some sort of file. The result
    to come out of it's methods will be used by the Parser Module to generate topics
    about the information in the Feed. A Feed represents a single article of related
    data. The implementation should generate Feed objects as defined above in order
    to be encapsulated. 
    """

    def __init__(self, file):
        """
        A feeder should be initialized to read from it's source when commanded to
        via the load_feeds method. Feeds is a list of Feed objects specifically, 
        and is interacted with in the feeds generator call. 

        `file`: The file to process later. 
        """
        self.feeds = []
        self.path = file

    def feeds(self):
        """
        Returns the feeds the Feeder is holding on to via a generator structure.  
        """
        for feed in self.feeds:
            yield feed
            # feeds = []

    def fetch(self):
        """
        Calling this method should retrieve information using the file provided
        at initialization. Following that, that information will be standardized
        into a Feed object and stored in the feeds instance variable. This is going
        to be implemented in very different ways, depending on the file type used. 
        """
        pass


class RssFeeder(Feeder):
    """ 
    `Author`: Eliakah kakou

    This class generates a list of feed instances containing relevant data about the file 
    """

    def __init__(self, file):
        """
        `Author`: Eliakah kakou
        
        The constructor, initializes the RssFeeded instance 
        
        `file`: path to file containing list of links 
        """
        Feeder.__init__(self, file)
        self.feeds = []
        self.links = []
        self.path = file
        self.__getLinks(file)

    def load_feeds(self):
        """
        `Author`: Eliakah kakou
        
        returns 'feeds' which contains all of the feed instances 
        """
        self.fetch()
        return self.feeds

    def __getLinks(self, file):
        """
        `Author`: Eliakah kakou
        
        This method inserts each link from the file as an entry into the 'links' list 
        
        `file`:path to file containing list of links 
        """
        input_file = open(file)
        try:
            for i, line in enumerate(input_file):
                self.links.append(line)
                # print line,
        finally:
            input_file.close()

    def fetch(self):
        """
        `Author`: Eliakah kakou
        
        This method appends all of the feed instances to 'feeds'
        """
        for i in range(len(self.links)):
            self.feeds.extend(self.__getFeeds(self.links[i]))

    def __getFeeds(self, url):
        """
        `Author`: Eliakah kakou
        
        This method generates a Feed instance from the url given
        
        `file`: full file path
        
        `return`: Feed generated from file
        """
        flag = validators.url(url)
        if flag:
            feeds = feedparser.parse(url)
        else:
            sys.exit("Invalid Url: Please try again!")

        list = feeds['entries']
        for i in range(len(list)):
            list[i] = Feed(list[i])
            feeds = list

        return feeds


class DocFeeder(Feeder):
    """ 
     `Author`: Eliakah kakou
     
     This class recursively access each file in a given directory,
     then generates a list of feed instances containing relevant data about the file 
    """

    def __init__(self, file):
        """
        `Author`: Eliakah kakou
        
        The constructor, initializes the DocFeeded instance 
        
        `file`: directory path
        """
        Feeder.__init__(self, file)
        self.feeds = []
        self.paths = []
        self.path = file
        self.__getPaths(file)

    def __getPaths(self, file):
        """
        `Author`: Eliakah kakou
        
        This method inserts each link from the file as an entry into the 'paths' list
        
        `file`: path to original directory
        """
        print "getting Paths"
        matches = []
        for filename in self.__find_files(file, "*.*"):
            matches.append(filename)
        self.paths = matches

    def __find_files(self, directory, pattern):
        """
        `Author`: Eliakah kakou
        
        This method yields every single file in the directory matching the pattern
        
        `directory`: directory path
        
        `pattern`: file name pattern
        
        `return`: file paths matching pattern
        """
        print "finding files"
        for root, dirs, files in os.walk(directory):
            for basename in files:
                if fnmatch.fnmatch(basename, pattern):
                    filename = os.path.join(root, basename)
                    yield filename

    def fetch(self):
        """
        `Author`: Eliakah kakou
        
        This method appends all of the feed instances to 'feeds'
        """
        print "fetching ..."
        for i in range(len(self.paths)):
            self.feeds.append(self.__getFeeds(self.paths[i]))

    def load_feeds(self):
        """
        `Author`: Eliakah kakou
        
        `return`: 'feeds' which contains all of the feed instances 
        """
        print "Loading feeds"
        self.fetch()
        return self.feeds

    def __getFileName(self, path):
        """
        `Author`: Eliakah kakou
        
        This method extracts the file name from the path
        
        `path`: full path to the file 
        
        `return`: the file name 
        """
        drive, path = os.path.splitdrive(path)
        path, filename = os.path.split(path)
        name = filename.split(".")
        return name[0]

    def __getFeeds(self, file):
        """
        `Author`: Eliakah kakou
        
        This method generates a Feed instance from the file given
        
        `file`: full file path
        
        `return`: Feed generated from file
        """
        title = self.__getFileName(file)
        input_file = open(file)
        try:
            content = input_file.read()
        finally:
            input_file.close()

        stamp = time.ctime(self.__creation_date(file))

        f = {'id': file, 'published': stamp, 'title': title, 'link': file, 'summary': content}
        f = Feed(f)
        return f

    def __creation_date(self, file):
        """
        `Author`: Eliakah kakou
        
        This method returns the creation date of the file, 
        or replaces with the last modified if the former is unavailable 
        
        `return`: date on which file was created
    ...
        """
        if platform.system() == 'Windows':
            return os.path.getctime(file)
        else:
            stat = os.stat(file)
            try:
                return stat.st_birthtime
            except AttributeError:
                return stat.st_mtime


if __name__ == "__main__":
    feeder = RssFeeder('links.txt')
    feeder.fetch()
    feeds = feeder.feeds

    for i in range(len(feeds)):
        pprint.pprint(feeds[i].extract())

        # feeder = DocFeeder('C:\Users\Research\Desktop\parking')
        # feeds = feeder.load_feeds()
        #
        # for i in range(len(feeds)):
        #     pprint.pprint(feeds[i].extract())
