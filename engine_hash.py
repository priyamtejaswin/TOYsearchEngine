import urllib2
import urllib
###################-------CONVERT THE SOURCE TO LOWER CASE!!!!
def splitf(source,splitlist):#a better split function
    i=0
    words = []
    while i < len(source):
        if source[i] in splitlist:
            words.append(source[:i])
            source = source[i+1:]
            i=0
        else:
            i= i+1
    return words

###building index code starts here
def add_to_index(index,keyword,url):#the inputs are for each ENTRY of the list
    if keyword in index:
        if url not in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword] = [url]
        ### HOW ARE RECURRING LINKS ELIMINATED??(fixed it) but is my engine still reading these links!?!
def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def add_page_to_index(index,url,page_content):#inputs are for the LIST ITSELF, hence contains the text
    temp_string = splitf(page_content,' ,.;:"!?*()/\<>[]{}@#$%^&*')# using the splitf function----with delimiters
    for word in temp_string:
        add_to_index(index,word,url)

    return index
###building index code ends here

def union(l1,l2):
    for e in l2:
        if e not in l1:
            l1.append(e)
    return l1

def get_link(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None,0
    else:
        start_quote = page.find('"',start_link)
        end_quote = page.find('"',start_quote+1)
        url = page[start_quote+1:end_quote]

        return url,end_quote

def get_all_links(page):
    links = []
    while True:
        url,end_link = get_link(page)

        if url:
            links.append(url)
            #print url
            page = page[end_link:]

        else:
            break

    return links

def crawl(seed_page,max_depth=10):
    to_crawl = [seed_page]
    crawled = []
    next_depth = []#replacing with to_crawl, draw diagram for more understanding
    index = {}
    graph={}
    depth =0 

    while to_crawl and depth<=max_depth:
        temp_link = to_crawl.pop()
        if temp_link not in crawled:
            ## adding page content
            content = get_source(temp_link).lower()
            add_page_to_index(index,temp_link,content)
            ##done

            #for graph
            out_links = get_all_links(content)
            graph[temp_link] = out_links
            
            union(next_depth,out_links)
            crawled.append(temp_link)
        if not to_crawl:#--- for depth'''
            to_crawl,next_depth = next_depth,[]
            depth = depth+1#ends here

    return index,graph

def get_source(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10

    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages

    for i in range(0, numloops):
        newranks = {}
        for page in graph:

            #Insert Code Here
            inLinks = (node for node in graph if page in graph[node])
            newrank = ( (1 - d) / npages ) + d*sum(ranks[node]/len(graph[node]) for node in inLinks)

            newranks[page] = newrank
        ranks = newranks
    return ranks


def main():
    #s = raw_input("enter seed url-")
    #n= input("enter max depth-")
    #print get_all_links(get_source(s))
    #print "crawling the page---"
    #print crawl(s)
    s=''#enter SEED url
    
    index,graph = crawl(s)
    print graph
    print compute_ranks(graph)
    key = raw_input("enter lookup query-")
    print lookup(index,key) 
    
