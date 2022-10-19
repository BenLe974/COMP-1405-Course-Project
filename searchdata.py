from webbrowser import get
import parse_functions
import os
import webdev

def get_outgoing_links(url):
    if webdev.read_url(url) == "":
        return None
    
    filepath = os.path.join("search_results", parse_functions.find_title(url))

    if os.path.isdir(filepath) and os.path.exists(os.path.join(filepath,"page_address.txt")):
        filein = open(os.path.join(filepath,"page_address.txt"),"r")
        if filein.read().strip() == url and os.path.exists(os.path.join(filepath,"outgoing_links.txt")):
            filein.close()
            references = open(os.path.join(filepath,"outgoing_links.txt"),"r")
            outgoing = references.read().strip()
            references.close()
            return outgoing
        else:
            return None     
    else:
        return None

def get_incoming_links(url):
    
    return None
print(get_outgoing_links("http://people.scs.carleton.ca/~davidmckenney/tinyfruits/N-0.html"))