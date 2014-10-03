def compute_ranks(graph):
    d=0.8
    numloops = 10
    
    ranks={}
    newranks={}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0/npages

    for i in range(0,numploops):
        newranks={}
        for page in graph:
            newrank = (1-d)/npages
            for node in graph:
                if page in graph[node]:
                    newrank= newrank + d*(ranks[p]/len(graph[node]))
            
            newranks[page] = newrank
        ranks = newranks
    return ranks
