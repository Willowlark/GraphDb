from py2neo import Graph

class Recorder:
    graph = None

    def initialize(self, graph_address):
        self.graph = Graph(self, graph_address)

    def add_topic(self, topics):
        pass

    def fetch_topics(self, topics):
        pass

    def add_record(self, data):
        pass

    def has_node(self, topics):
        pass

    def relate_then_push(self, topic_nodes, record_node):
        pass

    def relate(self, topic_nodes, record_node):
        pass

    def push(self, *nodes):
        pass

