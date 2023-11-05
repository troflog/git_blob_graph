import pygit2
import networkx as nx
import matplotlib.pyplot as plt

# def add_tree_blobs_to_graph(tree, commit_graph, blob_hash, path=""):
    
#     tree_hash = tree.hex
#     tree_hash_short = tree_hash[:5]
    
#  tree_hash = entry.hex
#             tree_hash_sub  = tree_hash[:5]
#             commit_graph.add_node(tree_hash_sub, label='tree-'+tree_hash_sub)  # Label tree nodes with their hash
#             commit_graph.add_edge(blob_hash, tree_hash)
#             add_tree_blobs_to_graph(repo, commit_graph, tree_hash, path)

#     #Add this three to the graph
#     for entry in commit.tree:
#         if entry.type == pygit2.GIT_OBJ_TREE:
#            add_tree_blobs_to_graph()
#         elif entry.type == pygit2.GIT_OBJ_BLOB:
#             blob_hash = entry.hex
#             blob_hash_sub = blob_hash[:5]
#             blob_name = entry.name  # File me including the path
#             commit_graph.add_node(blob_hash_sub, label='file-'+blob_name)  # Label blob nodes with file name
#             commit_graph.add_edge(blob_hash_sub, blob_hash_sub)

# Open the Git repository
repo_path = "../trond"
repo = pygit2.Repository(repo_path)



# Create a directed graph using NetworkX
graph = nx.DiGraph()

# Iterate through the commit history
for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_REVERSE):
    commit_hash = commit.hex    
    graph.add_node(commit_hash) #,label='commit-' + commit_hash[:5])
    #if commit.parent_ids
    for parent in commit.parents:        
        graph.add_edge(parent.hex, commit_hash)
        
    
    

print("Nodes in the commit graph:")
print(graph.nodes(data=True))
print("\nEdges in the commit graph:")
print(graph.edges())



# Draw and display the graph
pos = nx.spring_layout(graph, seed=42)
plt.figure(figsize=(12, 12))
node_labels = nx.get_node_attributes(graph, "label")  # Get node labels (file names)
nx.draw(graph, pos, labels=node_labels, node_size=10, font_size=8)
plt.title("Git Commit Graph with File Names")
plt.axis("off")
plt.show()

