import pygit2
import networkx as nx
import matplotlib.pyplot as plt

# def find_branch_for_commit(repo_path, commit_hash):
#     repo = pygit2.Repository(repo_path)
#
#     commit = repo[commit_hash]
#
#     for branch in repo.branches.local:
#         try:
#             branch_commit = repo.revparse_single(branch.name)
#             if branch_commit.id == commit.id:
#                 return branch.name
#         except KeyError:
#             # Handle the case where a branch may point to a non-existent commit
#             pass

def small_hash(hash,length=5):
    return hash[:length]

def get_all_branches(repo):    
    branch_heads = []
    for branch in repo.branches.local:
        try:
            branch_commit = repo.revparse_single(branch)
            branch_heads.append((branch, branch_commit.hex))
        except KeyError:
            # Handle the case where a branch may point to a non-existent commit
            pass

    return dict(branch_heads)

def populate_tree(tree,parent_hash_short,graph):
    
    #Add the conncect tree
    tree_hash = tree.hex
    tree_hash_short = small_hash(tree_hash)
    graph.add_node(tree_hash_short,bname = tree_hash_short,btype='Tree')  # Label tree nodes with their hash
    graph.add_edge(parent_hash_short,tree_hash_short)
    #Add all blob to the connected tree
    #Add this three to the graph
    for entry in tree:
        if entry.type == pygit2.GIT_OBJ_TREE:
           populate_tree(entry,tree_hash,graph)
        elif entry.type == pygit2.GIT_OBJ_BLOB:
            blob_hash = entry.hex
            blob_hash_short = small_hash(blob_hash)
            blob_name = entry.name  # File me including the path
            graph.add_node(blob_hash_short,bname=blob_hash_short,btype='Blob',name=blob_name)
            graph.add_edge(tree_hash_short,blob_hash_short)


# Open the Git repository
repo_path = "../trond"
repo = pygit2.Repository(repo_path)
#Make a graph
graph = nx.DiGraph()
# # Iterate through the commit history
for branch_name in repo.branches.local:
    # Get the commit at the tip of the branch
    commit = repo.revparse_single(branch_name)
    for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL):
        commit_hash = commit.hex    
        commit_hash_short = small_hash(commit_hash)
        graph.add_node(commit_hash_short,bname = commit_hash_short,btype='Commit',message=commit.message)
        for parent in commit.parents:        
            graph.add_edge(commit_hash_short,small_hash(parent.hex))
        populate_tree(commit.tree,commit_hash_short,graph)

# #Add branch pointers
branches = get_all_branches(repo)
for branch_name,commit_hash in branches.items():
    graph.add_node(branch_name,bname = branch_name,btype='Branch')
    graph.add_edge(branch_name,small_hash(commit_hash))

#Print the graph#Print the graph
print("Nodes in the commit graph:")
for node in graph.nodes(data=True):
    print(node[0]+':'+node[1].get('message',''))
# print(graph.nodes(data=True))
print("\nEdges in the commit graph:")
print(graph.edges())

# Draw and display the graph
pos = nx.spring_layout(graph, seed=42)
plt.figure(figsize=(12, 12))
node_labels = nx.get_node_attributes(graph, "bname")  # Get node labels (file names)
n = {}
for k,v in dict(list(graph.nodes(data=True))).items():
    n[k] =v.get('btype','')+':'+v['bname']+'\n'+v.get('message','')+v.get('name','')
nx.draw(graph, pos, labels=n)
plt.title("Git Commit Graph with File Names")
plt.axis("off")
plt.show()
#
