# * Created by Eliakah kakou
# Main.py
# This class allows you call and test all classes
import sys

from RssFeedParser import RssFeedParser


def main():
    # gets input from the line and runs accordingly
    id = []
    urls = []
    while True:

        command = prompt()  # gets input

        # stop -
        # run -
        if len(command) > 0 and len(command) == 1:
            if (command[0].lower() == "stop"):
                sys.exit()
            elif (command[0].lower() == "run"):
                if (len(urls) > 0):
                    print "runs all the urls in store"
                else:
                    print "Error: no urls in store"
            else:
                print "Unknown Command: '", command[0], "'"

        # add ___ -
        # remove____-
        elif len(command) > 0:
            if (command[0].lower() == "add"):
                urls.append(command[1])
                print urls
            if (command[0].lower() == "remove"):
                flag = 0
                for i in range(len(urls)):
                    if (urls[i] == command[1]):
                        print command[1], "removed!"
                        flag = 1

                if (flag == 0):
                    print "Error: no such entry"
                urls.append(command[1])
                print urls
            print command


def run():
    print "run"


def remove(url):
    print url


def prompt():
    list = ()
    list = raw_input("Command: ").split()
    return list



    # parser = RssFeedParser('http://popculturebrain.com/rss')
    # #parser.getFields()
    # feeds = parser.getFeeds()
    # summaries = parser.getFeeds()
    # print len( feeds['entries'])
    # #print [field for field in parser.getSummaries()[0]]
    #
    #
    # print "TYPE: ", type(parser.getSummaries())
    # for i in range(len(summaries)):
    #     print "\n id ", summaries[i]['id'], "\n"
    #     print "\n published ", summaries[i]['published'], "\n"
    #     print "\n link ", summaries[i]['link'], "\n"
    #     print "\n title_detail ", summaries[i]['title_detail'], "\n"
    #     print "\n guidislink ", summaries[i]['guidislink'], "\n"
    #     print "\n summary ", summaries[i]['summary'], "\n"
    #     print "\n title ", summaries[i]['title'], "\n"
    #     print "\n links ", summaries[i]['links'], "\n"
    #     print "\n published_parsed ", summaries[i]['published_parsed'], "\n"
    #     print "\n summary_detail ", summaries[i]['summary_detail'], "\n"




main()
