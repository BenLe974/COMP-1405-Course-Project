import parse_functions
import os
import webdev
import math

def get_outgoing_links(url):
    if webdev.read_url(url) == "":
        return None
    
    filepath = os.path.join("search_results", parse_functions.find_title(url))

    if os.path.isdir(filepath) and os.path.exists(os.path.join(filepath,"page_address.txt")):
        filein = open(os.path.join(filepath,"page_address.txt"),"r")
        if filein.read().strip() == url and os.path.exists(os.path.join(filepath,"outgoing_links.txt")):
            filein.close()
            references = open(os.path.join(filepath,"outgoing_links.txt"),"r")
            outgoing = references.read().strip().split()
            references.close()
            return outgoing
        else:
            return None     
    else:
        return None

def get_incoming_links(url):
    if webdev.read_url(url) == "":
        return None
    filepath = os.path.join("search_results", parse_functions.find_title(url))
    if os.path.isdir(filepath) and os.path.exists(os.path.join(filepath,"page_address.txt")):
        filein = open(os.path.join(filepath,"page_address.txt"),"r")
        if filein.read().strip() == url:
            filein.close()
            titles = os.listdir("search_results")
            incoming = []
            for title in titles:
                filepath = os.path.join("search_results", title)
                filein = open(os.path.join(filepath,"outgoing_links.txt"),"r")
                links = filein.read().strip()
                if url in links:
                    address = open(os.path.join(filepath,"page_address.txt"),"r")
                    incoming.append(address.read().strip())
                    address.close()
                filein.close()
            return incoming
        else:
            return None
    else:
        return None

def get_page_rank(url):
    if webdev.read_url(url) == "":
        return -1
    filepath = os.path.join("search_results", parse_functions.find_title(url))
    if os.path.exists(filepath) and os.path.isdir(filepath):
        filein = open(os.path.join(filepath, "page_rank.txt"),"r")
        pagerank = float(filein.read().strip())
        filein.close()
    else:
        return -1
    return pagerank

def get_idf(word):
    titles = os.listdir("search_results")
    docnumber = len(titles)
    frequency = 0
    for title in titles:
        filepath = os.path.join("search_results",title)
        if os.path.exists(os.path.join(filepath, word + ".txt")):
            frequency += 1
    if frequency == 0:
        return 0
    idf = math.log2(docnumber/(1+frequency))
    return idf

def get_tf(url,word):
    if webdev.read_url(url) == "":
        return 0
    title = parse_functions.find_title(url)
    filepath = os.path.join("search_results",title)
    if os.path.exists(os.path.join(filepath,word + ".txt")):
        filein = open(os.path.join(filepath,word + ".txt"),"r")     
        tf = float(filein.read().strip())
    else:
        return 0
    return tf        
          

def get_tf_idf(url,word):
    words = open("words_found.txt","r")
    idfs = open("idf.txt","r")
    search = words.read().strip().split()
    if word in search:
        idf = float(idfs.read().strip().split()[search.index(word)])
    else:
        idf = math.log2((len(os.listdir("search_results"))/1))
    tf = get_tf(url,word)
    tf_idf = math.log2(1+tf)*idf
    return tf_idf
