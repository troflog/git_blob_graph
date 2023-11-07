import networkx as nx
import time

def generate_mermaid_from_digraph(G, filename='output.mmd'):
    mermaid_code = "```mermaid\ngraph TD;\n"

    # Add nodes
    for node in G.nodes():
        mermaid_code += f"  {node}({node})\n"

    # Add edges
    for edge in G.edges():
        mermaid_code += f"  {edge[0]} --> {edge[1]}\n"

    mermaid_code +="```"
    
    # Write the Mermaid code to a file
    with open(filename, 'w') as file:
        file.write(mermaid_code)

if __name__ == "__main__":
    # Create a sample DiGraph
    graph = nx.DiGraph()        
    graph.add_edges_from([(1, 2), (1, 3), (2, 4) ])
    for i in range(3):  
        graph.add_edge(i+4,i+5)
        # Generate Mermaid code and save to a file
        generate_mermaid_from_digraph(graph, filename='output.md')
        time.sleep(5)
    