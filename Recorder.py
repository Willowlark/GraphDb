from py2neo import Graph
from py2neo import Node
from py2neo import Relationship
from Topic_Candidates import Topic_Candidate
import Parser

class Recorder:
    """
    `Author`: Bill Clark

    A module to handle the neo4j interactions in RssGrapher. Methods are specific to
    that class, but are basic enough to be reused easily. Most return subgraphs.

    `graph`: The global for the graph to connect to.

    `confirm_mode`: A flag that can be set to 1) prevent the adding methods from adding
    to the graph, limiting them to only returning the created node; and 2) require a user
    input for push operation. For safety mostly, unlikely needed.
    """
    graph = None
    confirm_mode = False

    def initialize(self, graph_address):
        """
        `Author`: Bill Clark

        Connects to a graph for operations. Required before anything else.

        `graph_address`: web address of neo4j instance.
        """
        self.graph = Graph(self, graph_address)

    def _subgraphify(self, graph_list):
        """
        `Author`: Bill Clark

        Converts a list of py2neo objects into a py2neo subgraph.

        `graph_list`: A list of nodes, relationships, or subgraphs.

        `return`: the subgraph made from the list elements.
        """
        base = graph_list.pop(0)
        for graph in graph_list:
            base = base | graph
        return base

    def add_topic(self, topic_candidates):
        """
        `Author`: Bill Clark

        Adds a list of topics to the graph as new nodes. This doesn't check if the node
        already exists; use get_or_add_topics for that. The nodes are returned regardless,
        but are only pushed if confirm_mode is off.

        `topics`: A list of string Topics to be added. The string value will be the name
        property of the node, while the label will be Topic.

        `return`: a subgraph containing all the new nodes.
        """
        listing = []
        for topic in topic_candidates:
            n = Node("Topic", name=topic.title)
            if self.confirm_mode: self.graph.create(n)
            listing.append(n)
        return self._subgraphify(listing)

    def fetch_topics(self, topic_candidates):
        """
        `Author`: Bill Clark

        Retrieves topics from the graph. Assumes the topics are in the graph, use has_topic
        beforehand. Takes the first found instance, but names should be singleton anyway.

        `topic_candidates`: List of string topic names to retrieve.

        `return`: subgraph of the topics retrieved.
        """
        listing = []
        for topic in topic_candidates:
            match = self.graph.find_one("Topic", property_key='name', property_value=topic.title)
            listing.append(match)
        return self._subgraphify(listing)

    def get_or_add_topics(self, topic_candidates):
        """
        `Author`: Bill Clark

        Control method. This method takes each topic given and either creates it if it
        doesn't exist or retrieves it if it does not. This should be used over the
        individual add and fetch operations.

        `topic_candidates`: List of topic strings to be added or retieved. The value of the string
        is the name property of the node.

        `return`: a subgraph of the fetched and added nodes.
        """
        listing = []
        for topic in topic_candidates:
            if self.has_topic([topic]):
                listing.append(self.fetch_topics([topic]))
            else:
                listing.append(self.add_topic([topic]))
        return self._subgraphify(listing)

    def add_record(self, data):
        """
        `Author`: Bill Clark

        Adds a node in the same manner as add topic. This does not accomodate lists.
        This is used for adding records, made seperate so Topics can be expanded on.
        Will not add to the graph if confirm mode is off, only return the created node.

        `data`: The data to store in the content field of the node.

        `return`: the node created.
        """
        n = Node("Record", content=data)
        if self.confirm_mode: self.graph.create(n)
        return n

    def has_topic(self, topic_candidates):
        """
        `Author`: Bill Clark

        Checks a list of topics for existence in the graph. One failure in the list
        fails the list. Can only be used with Topics.

        `topic_candidates`: list of topics (string holding name value) to confirm existence of.

        `return`: boolean, true iff all topics are contained.
        """
        for topic in topic_candidates:
            if not self.graph.find_one("Topic", property_key="name", property_value=topic.title):
                return False
        return True

    def relate_then_push(self, topic_subgraph, record_node):
        """
        `Author`: Bill Clark

        Control method. This method streamlines relation into a push. calls push
        with the result of the relation.

        `topic_subgraph`: A subgraph containing topic nodes to be related to the record.

        `record_node`: A node to relate to each topic in the topic_subgraph.
        """
        related = self.relate(topic_subgraph, record_node)
        self.push(related)

    def relate(self, topic_subgraph, record_node):
        """
        `Author`: Bill Clark

        Takes a subgraph of topics and relates them to a singular record. Will be
        modified, eventually.

        `topic_subgraph`: A subgraph containing topic nodes to be related to the record.

        `record_node`: A node to relate to each topic in the topic_subgraph.

        `return`: A subgraph containing the record, the topic_subgraph, and the new
        relationships.
        """
        listing = []
        for node in topic_subgraph.nodes():
            listing.append(Relationship(record_node, 'Related', node))
        return self._subgraphify(listing) | record_node

    def push(self, subgraph):
        """
        `Author`: Bill Clark

        Pushes changes to the graph database, as well as creates any new nodes in the
        subgraph. Contains a user input check mode only activated when the confirm_mode
        flag is true.

        `subgraph`: The subgraph to update and create.

        `return`: -1 on a failure, else None.
        """
        if self.confirm_mode:
            print subgraph
            if raw_input("Confirm with y: ") != "y":
                return -1
        self.graph.push(subgraph)
        self.graph.create(subgraph)

if __name__ == "__main__":
    rec = Recorder()
    rec.initialize('http://localhost:7474/db/data/')

    ctopics = Parser.main()

    tops = rec.get_or_add_topics(ctopics)
    print tops
    recs = Node("Record", content="cats")

    rec.relate_then_push(tops, recs)
