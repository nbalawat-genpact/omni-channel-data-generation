import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from intializejourneys import get_graph


def generate_random_graph_data(journey_type="Payment Journey", init_value=10000):

    G1 = get_graph(type=journey_type, n=init_value)

    for n, node_attributes in list(G1.nodes(data=True)):
        # get the node value
        node_value = node_attributes["value"]

        # get the successors to the node
        succ = list(G1.successors(n))

        # generate random numbers and percentages
        k = np.random.rand(len(succ))
        perc = k / sum(k)

        # initiate dictionary to store edge and node properties
        update_edges_dict = {}
        update_nodes_dict = {}

        # Update  the percentage and the counts
        if len(succ) > 0:
            for ind, s in enumerate(succ):
                # print(f'successor - {s} - {ind} - {G1[s]}')
                update_edges_dict[(n, s)] = {"perc": perc[ind], "count": perc[ind] * node_value}
                update_nodes_dict[s] = {"value": perc[ind] * node_value}
            nx.set_node_attributes(G1, update_nodes_dict)
            nx.set_edge_attributes(G1, update_edges_dict)
    # convert this into a list of lists and send the output
    return [[from_node, to_node, attrib["count"]] for from_node, to_node, attrib in list(G1.edges(data=True))]


def generate_graph_combinations(journey_types=["Payment Journey"]):
    # Intialize the combinations
    segments = ["Segment1", "Segment2", "Segment3", "Segment4"]
    lobs = ["Credit Cards", "Checking account", "Retail Loans"]
    geos = ["North America", "Latin America", "Asia", "Europe", "Australia"]
    months = [
        "Jan-19",
        "Feb-19",
        "Mar-19",
        "Apr-19",
        "May-19",
        "Jun-19",
        "Jul-19",
        "Aug-19",
        "Sep-19",
        "Oct-19",
        "Nov-19",
        "Dec-19",
    ]
    start_channels = ["web"]

    init_numbers = np.arange(10000, 50000, 500)

    # create place holder for all combinations

    final_list = []
    for lob in lobs:
        for geo in geos:
            for mnth in months:
                for seg in segments:
                    for chnl in start_channels:
                        for jrny in journey_types:
                            k = generate_random_graph_data(
                                journey_type=jrny, init_value=np.random.choice(init_numbers, 1)[0]
                            )
                            final_list.append((lob, geo, mnth, seg, chnl, jrny, k))

    # create a data frame and return the data frame
    df = pd.DataFrame(final_list, columns=["lob", "geo", "month", "seg", "startchannel", "journey", "sankey"])
    return df
