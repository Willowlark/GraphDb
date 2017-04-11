"""
This module is used to interact with a neo4j DB. It records information given to it
into the DB, hence the name. It operates as a Class and uses py2neo to turn information
into graph objects. 
"""

from py2neo import Graph
from py2neo import Node
from py2neo import Relationship


class Recorder:
    """
    `Author`: Bill Clark

    A module to handle the neo4j interactions in Grapher. Methods are specific to
    that class, but are basic enough to be reused easily. Most return subgraphs.

    `graph`: The global for the graph to connect to.

    `immediate_mode`: A flag that can be set to 1) prevent the adding methods from adding
    to the graph, limiting them to only returning the created node; and 2) require a user
    input for push operation. For safety mostly, unlikely needed.
    """
    graph = None
    immediate_mode = True  # Bit slower, but eliminates duplicates in the same article.
    confirm_mode = False

    def initialize(self, graph_address):
        """
        `Author`: Bill Clark

        Connects to a graph for operations. Required before anything else.
        ToDo: Something with authentication

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

    def _add_topics(self, topic_candidates):
        """
        `Author`: Bill Clark

        Adds a list of topics to the graph as new nodes. This doesn't check if the node
        already exists; use get_or_add_topics for that. The nodes are returned regardless,
        but are only pushed if immediate_mode is off.

        `topics`: A list of string Topics to be added. The string value will be the name
        property of the node, while the label will be Topic.

        `return`: a subgraph containing all the new nodes.
        """
        listing = []
        for topic in topic_candidates:
            n = Node("Topic", title=topic.title)
            topic.update_properties(n)
            if self.immediate_mode: self.graph.create(n)
            listing.append(n)
        return self._subgraphify(listing)

    def _fetch_topics(self, topic_candidates):
        """
        `Author`: Bill Clark

        Retrieves topics from the graph. Assumes the topics are in the graph, use has_topic
        beforehand. Takes the first found instance, but names should be singleton anyway.

        `topic_candidates`: List of string topic names to retrieve.

        `return`: subgraph of the topics retrieved.
        """
        listing = []
        for topic in topic_candidates:
            match = self.graph.find_one("Topic", property_key='title', property_value=topic.title)
            if not match: return False # Not in the DB
            listing.append(topic.update_properties(match))
        return self._subgraphify(listing)

    def get_or_add_topics(self, topic_candidates):
        """
        `Author`: Bill Clark

        Control method. This method takes each topic given and either creates it if it
        doesn't exist or retrieves it if it does not. This should be used over the
        individual add and fetch operations.

        `topic_candidates`: List of topic strings to be added or retrieved. The value of the string
        is the name property of the node.

        `return`: a subgraph of the fetched and added nodes.
        """
        listing = []
        for topic in topic_candidates:
            fetch = self._fetch_topics([topic])
            if not fetch:
                fetch = self._add_topics([topic])
            listing.append(fetch)
        return self._subgraphify(listing)

    def add_record(self, data):
        """
        `Author`: Bill Clark

        Adds a node in the same manner as add topic. This does not accommodate lists.
        This is used for adding records, made separate so Topics can be expanded on.
        Will not add to the graph if confirm mode is off, only return the created node.

        `data`: The data to store in the content field of the node.

        `return`: the node created.
        """
        if self.has_record(data): return False
        n = Node("Record", content=data)
        if self.immediate_mode: self.graph.create(n)
        return n

    def has_record(self, data):
        """
        `Author`: Bill Clark
        
        Checks if a record with content field data is in the database. If it is found,
        we return True. If it's not found, we return false. 
        
        `data`: The value in the content field to check against.
        
        `return`: Boolean True or False
        """
        if self.graph.find_one("Record", property_key="content", property_value=data):
            return True
        else: return False

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
            r = Relationship(record_node, 'Related', node)
            for key in node:
                if key != 'title': r[key] = node[key]
            listing.append(r)
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
        self._scrub_topics(subgraph)
        self.graph.push(subgraph)
        self.graph.create(subgraph)

    def _scrub_topics(self, subgraph):
        approved = ['timestamp', 'title']
        for node in subgraph.nodes():
            title = node['title']
            timestamp = node['timestamp']
            node.clear()
            node['title'] = title
            node['timestamp'] = timestamp



if __name__ == "__main__":
    rec = Recorder()
    rec.initialize('http://localhost:7474/db/data/')