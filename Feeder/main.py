# * Created by Eliakah kakou
# Main.py
# This class allows you call and test all classes

from RssFeedParser import RssFeedParser
def main():
    parser = RssFeedParser('http://popculturebrain.com/rss')
    # parser.getFields()
    feeds = parser.getFeeds()
    summaries = parser.getFeeds()
    print len( feeds['entries'])
    # print [field for field in parser.getSummaries()[0]]


    print "TYPE: ", type(parser.getSummaries())
    for i in range(len(summaries)):
        print "\n id ", summaries[i]['id'], "\n"
        print "\n published ", summaries[i]['published'], "\n"
        print "\n link ", summaries[i]['link'], "\n"
        print "\n title_detail ", summaries[i]['title_detail'], "\n"
        print "\n guidislink ", summaries[i]['guidislink'], "\n"
        print "\n summary ", summaries[i]['summary'], "\n"
        print "\n title ", summaries[i]['title'], "\n"
        print "\n links ", summaries[i]['links'], "\n"
        print "\n published_parsed ", summaries[i]['published_parsed'], "\n"
        print "\n summary_detail ", summaries[i]['summary_detail'], "\n"


main()