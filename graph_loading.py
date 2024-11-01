import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import os
from colour_mappings import line_colours, line_names

def load_graph():
    stations_list = pd.read_excel("All Stations.xlsx")
    index_to_station_name = {}
    station_name_to_index = {}
    for i,station in enumerate(stations_list['Station']):
        index_to_station_name[i] = station
        station_name_to_index[station] = i

    df = pd.DataFrame()
    for filename in os.listdir("Lines"):
        if filename.endswith('.xlsx'):
            file = os.path.join("Lines", filename)
            df_new = pd.read_excel(file)
            df_new["Line"] = filename.split(".")[0]
            df = pd.concat([df, df_new], ignore_index=True)

    # Use MultiDiGraph instead of DiGraph
    G = nx.MultiDiGraph()

    for _, row in df.iterrows():
        start_index = station_name_to_index[row['Start']]
        end_index = station_name_to_index[row['End']]
        if row['Directed'] == 1:  # Directed edge
            G.add_edge(start_index, end_index, 
                    weight=row['Time'], 
                    color=line_colours[row["Line"]], 
                    line=row["Line"])
        else:  # Undirected edge
            G.add_edge(start_index, end_index, 
                    weight=row['Time'], 
                    color=line_colours[row["Line"]], 
                    line=row["Line"])
            G.add_edge(end_index, start_index, 
                    weight=row['Time'], 
                    color=line_colours[row["Line"]], 
                    line=row["Line"])

    # Get edge weights and colours - modified for MultiDiGraph
    weights = []
    colors = []
    for u, v, key, data in G.edges(data=True, keys=True):
        weights.append(data['weight'])
        colors.append(data['color'])

    positions_df = pd.read_excel("Station Coordinates.xlsx") 
    pos = {}
    for i, row in positions_df.iterrows():
        station_index = station_name_to_index[row["Station"]]
        pos[station_index] = (float(row["Point"].split(" ")[1][1:]), float(row["Point"].split(" ")[2][:-1]))
    return G, pos, colors, weights, index_to_station_name, station_name_to_index